# Download Twitter Media Tweets
## 概要
このプログラムはTwitter上に存在するユーザがツイートした画像を、全てダウンロードするPythonプログラムです。

非公開となっているユーザには対応しておりません。

また、ダウンロードするのは画像のみで、動画は対応しておりません。

**利用は自己責任**でお願いします。

## 動作環境
動作はWindows 10でのみ動作確認しています。

動作には[Python本体](https://www.python.jp/)、以下のPythonパッケージ、[Google Chrome](https://www.google.com/intl/ja_ALL/chrome/)が必要となります。
```
beautifulsoup4==4.7.1
chromedriver-binary==73.0.3683.68.0
selenium==3.141.0
soupsieve==1.8
urllib3==1.24.1
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

実行するとカレントディレクトリに対して「ユーザID/ツイートID.拡張子」で保存していきます。

1ツイートに対して複数画像が存在する場合は、「ユーザID/ツイートID_連番.拡張子」で保存します。
