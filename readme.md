# Download Media Tweets
## 概要
このプログラムはTwitter上に存在するユーザのメディアツイートに存在する画像を全てダウンロードするPythonプログラムです。

**利用は自己責任**でお願いします。

## 動作環境
動作はWindows 10でのみ動作確認しています。

動作には[Python本体](https://www.python.jp/)、以下のPythonパッケージ、[Google Chrome](https://www.google.com/intl/ja_ALL/chrome/)、[ChromeDriver - WebDriver for Chrome](https://sites.google.com/a/chromium.org/chromedriver/home)が必要となります。
```
beautifulsoup4==4.7.1
selenium==3.141.0
```

また、ChromeDriverのパスを、環境変数のPATHに設定しないと動作しません。

## 本プログラムについて
本プログラムはSeleniumとBeautifulSoupを用いてクローリングを行うことで画像を検索しているため、robots.txt、metaタグ、HTTPヘッダーのX-Robots-Tagをチェックしています。

2019/3/7現在、Twitterのツイート及び画像に対するクローリングは禁止されていないので問題なく動作しますが、今後上記内容に変更があった場合は動作しなくなりますがご了承ください。

また、必ず1画像につき1秒以上のウェイトを挟んでおります。

## 使い方
コマンドラインから実行してください。

また、コマンドライン引数として、対象となるユーザのユーザIDを指定してください。
```code
python ./dl_mediatweets.py [twitter_id]
```
