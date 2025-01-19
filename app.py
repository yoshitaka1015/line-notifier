from flask import Flask, request, abort
import requests
import os

# Flaskアプリケーションの初期化
app = Flask(__name__)

# 環境変数からLINE Notifyのアクセストークンを取得
LINE_NOTIFY_TOKEN = os.getenv('LINE_NOTIFY_TOKEN')

# LINE Notifyのエンドポイント
LINE_NOTIFY_API = "https://notify-api.line.me/api/notify"

@app.route("/callback", methods=['POST'])
def callback():
    # リクエストボディを取得
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # 固定メッセージをLINE Notifyで送信
    fixed_message = "埼玉県の県立コートに空きが出ました！"
    try:
        headers = {
            "Authorization": f"Bearer {LINE_NOTIFY_TOKEN}"
        }
        data = {
            "message": fixed_message
        }
        response = requests.post(LINE_NOTIFY_API, headers=headers, data=data)
        if response.status_code == 200:
            app.logger.info("メッセージをLINE Notifyで送信しました！")
        else:
            app.logger.error(f"LINE Notify送信時にエラーが発生しました: {response.status_code}, {response.text}")
    except Exception as e:
        app.logger.error(f"メッセージ送信時に例外が発生しました: {e}")

    return 'OK'

if __name__ == "__main__":
    # アプリケーションを0.0.0.0:5000で起動
    app.run(host='0.0.0.0', port=5000)
