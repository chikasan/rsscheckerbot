# rsscheckerbot
RSSの更新があればDiscordのチャンネルに書き込んでくれるbotです

## 実行手順

1. 下記コマンドを実行
```
pip install -r requirements.txt
```
1. config.yamlを編集
    * channelに通知内容を書き込むDiscordのチャンネルIDを記載
    * urlにはRSSのURLを記載
    * lastupdatedに記載されている日時以降を通知するので、初回実行時はそれより少し前の時間を指定する
1. 環境変数 TOKEN にdiscordのbotトークンを記載
1. 下記コマンドを実行
```
python3 rsscheckerbot.py
```
1. 起動に成功すると60分に1回、config.yamlに記載したURLの更新を確認します。
    * 更新が見つかった場合は、その情報をDiscordのチャンネルに書き込みます。
