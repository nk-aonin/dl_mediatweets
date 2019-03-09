# coding:utf-8
from selenium.webdriver import Chrome, ChromeOptions
from bs4 import BeautifulSoup
from urllib import request, robotparser, error
from os import makedirs
import os.path, re, sys, time, chromedriver_binary

if __name__ == "__main__":
    args = sys.argv
    user_id = ''
    # 引数をチェック
    if len(args) <= 1:
        # 引数が存在しない（user_idが指定されていない）場合は終了
        sys.exit("Please type 'python ./dl_mediatweets.py 'user_id''!")
    else:
        if len(args) == 2:
            user_id = args[1]
        else:
            # 引数が多すぎる(user_idが特定出来ない）場合は終了
            sys.exit("Please type 'python ./dl_mediatweets.py 'user_id''!")

    print("user_id='%s'" % user_id)
    target_url = "https://twitter.com/" + user_id + "/media"

    # Twitterのrobots.txtをチェックする
    print("Checking 'robots.txt'...")
    rp = robotparser.RobotFileParser()
    rp.set_url("https://twitter.com/robots.txt")
    rp.read()

    # クローラがURLを見れるかチェックする。
    if not rp.can_fetch("*", target_url):
        # 見れない場合は終了
        print("It is forbidden to crawl Twitter page.")
        sys.exit(2)

    # クローラの遅延時間指定パラメータの取得
    # デフォルトは1秒とし、robots.txtで1秒以上が定められていた場合はその設定に従う
    delay_sec = 1
    if rp.crawl_delay("*"):
        delay_sec = rp.crawl_delay("*")
    if rp.request_rate("*"):
        rpquest_rate = rp.request_rate("*").seconds / rp.request_rate("*").requests
        if rpquest_rate > delay_sec:
            delay_sec = rpquest_rate

    # TwitterページのHTTPヘッダーのX-Robots-Tag内に、
    # "nofollow"または"noarchive"が有るかチェック。
    print("Checking 'X-Robots-Tag'...")
    r = request.urlopen(target_url)
    if "nofollow" in str(r.headers.get("X-Robots-Tag")) \
        or "noarchive" in str(r.headers.get("X-Robots-Tag")):
        # 存在する場合はクローリングが禁止されているので終了
        print("It is forbidden to crawl Twitter page.")
        sys.exit(2)

    # Twitterページのmetaタグに、
    # "nofollow"または"noarchive"が有るかチェックする。
    print("Checking 'Meta Tag'...")
    soup = BeautifulSoup(r, "html.parser")
    meta = soup.find_all('meta',
                     attrs={"name":"robots"},
                     content=lambda x: "nofollow" in str(x).lower() or "noarchive" in str(x).lower())
    if len(meta) > 0:
        # 存在する場合はクローリングが禁止されているので終了
        print("It is forbidden to crawl Twitter page.")
        sys.exit(2)

    # GoogleChromeのヘッドレスモードを有効化する
    options = ChromeOptions()
    options.add_argument("--headless")

    # GoogleChromeを起動
    driver = Chrome(options=options)

    # 指定したユーザIDのTwitterページを開く
    driver.get(target_url)

    # TwitterページのタイトルにユーザIDが存在しない場合、
    # 該当ユーザが存在しないと判断し終了
    if not re.match(r".*@" + user_id + ".*$", driver.title):
        sys.exit("Error! Not Found Twitter User Page!")

    # 非公開ユーザかどうかチェックするため、非公開ユーザのみ存在する要素を取得する
    # 非公開ユーザの場合、ツイートを取得できないため、終了
    protect_check_elems = driver.find_elements_by_css_selector("#page-container > div.AppContainer > div > div > div.Grid-cell.u-size1of3.u-lg-size1of4 > div > div > div > div.ProfileHeaderCard > h1 > span > a")
    if len(protect_check_elems) > 0:
        if re.match(r".*protected.*",protect_check_elems[0].get_attribute('href')):
            sys.exit("Error! This User is Protected User!")

    # メディアツイートを全て表示し、ツイート数をカウントする
    print("Checking media tweets...")
    media_tweets = driver.find_elements_by_css_selector("#stream-items-id > li")

    # メディアツイートが無い場合は終了
    if len(media_tweets) == 0:
        print( "'%s' not found media tweets." % user_id)
        sys.exit(1)

    # メディアツイートを全て表示するまでSelenium上のTwitterページを下にスクロールする
    while True:
        media_end_elem = driver.find_element_by_css_selector("#timeline > div > div.stream > div.stream-footer > div > div.stream-end")
        if media_end_elem is None or media_end_elem.is_displayed():
            break
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(delay_sec)

    # メディアツイートを取得する
    media_tweets = driver.find_elements_by_css_selector("#stream-items-id > li")
    media_tweet_count = len(media_tweets)
    print("Media tweets count:", media_tweet_count)

    # カレントディレクトリ/ユーザID/を保存ディレクトリとする
    savedir = os.path.dirname("./" + user_id + "/")
    if not os.path.exists(savedir):
        # ディレクトリが無い場合は作成
        makedirs(savedir)

    # メディアツイートに存在する画像をすべて保存する
    for media_tweet in media_tweets:
        tweet_id = media_tweet.get_attribute("data-item-id")
        print("Checking ID:%s '%s'" % (tweet_id, "https://twitter.com/" + user_id + "/status/" + tweet_id))
        media_elem = media_tweet.find_elements_by_css_selector("div > div.content > div.AdaptiveMediaOuterContainer > div > div > div")
        if len(media_elem) == 0:
            print("ID:%s is not image tweet." % tweet_id)
            continue
        img_elems = media_elem[0].find_elements_by_tag_name("img")
        for i, img_elem in enumerate(img_elems):
            img_url = img_elem.get_attribute("src")
            img_ext = re.search(r"^.*(\.[0-9|a-z|A-Z]+)$", img_url).group(1)
            if len(img_elems) ==  1:
                # 1ツイートに対して、画像が１つの場合は、
                # [ツイートID].[基画像の拡張子]をファイル名とする
                savepath = savedir + "/" + tweet_id + img_ext
            else:
                # 1ツイートに対して、画像が複数存在する場合は、
                # [ツイートID_連番].[基画像の拡張子]をファイル名とする
                savepath = savedir + "/" + tweet_id + "_" + str(i+1) + img_ext
            if os.path.exists(savepath):
                # 既に保存している場合はスキップ
                print("ID:%s is Already Download.(url:'%s')" % (tweet_id, img_url))
                continue

            # 画像を保存する
            print("Download: from '%s' to '%s'" % (img_url,savepath))
            try:
                # 画像のダウンロードは失敗する可能性があるのでエラーをキャッチする
                request.urlretrieve(img_url, savepath)
            except error.HTTPError as e:
                # HTTP Errorとなった場合はエラーコードを表示
                print("Failed download:'%s' (Error Code:%s)" % (img_url, e.code))
            except error.URLError as e:
                # URL Errorとなった場合はエラーメッセージを表示
                print("Failed download:'%s' (Error Message:%s)" % (img_url, e.reason))

            # robots.txtに従ってウェイト
            time.sleep(delay_sec)

    print("Complete.")
    driver.quit()
