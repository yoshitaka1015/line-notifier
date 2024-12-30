from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os

# Flaskアプリケーションの初期化
app = Flask(__name__)

# 環境変数からLINEのチャネルアクセストークン、シークレット、グループIDを取得
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')
LINE_GROUP_ID = os.getenv('LINE_GROUP_ID')

# LINE Bot APIとWebhookHandlerの初期化
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    # リクエストヘッダーから署名検証のための値を取得
    signature = request.headers['X-Line-Signature']

    # リクエストボディを取得
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    try:
        # 署名を検証し、問題なければハンドラーに渡す
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # Webhookイベントを受け取ったら、固定メッセージをグループに送信
    fixed_message = "こんにちは、これはグループへの固定メッセージです！"
    try:
        line_bot_api.push_message(LINE_GROUP_ID, TextSendMessage(text=fixed_message))
        app.logger.info("メッセージをグループに送信しました！")
    except Exception as e:
        app.logger.error(f"メッセージ送信時にエラーが発生しました: {e}")

if __name__ == "__main__":
    # アプリケーションを0.0.0.0:5000で起動
    app.run(host='0.0.0.0', port=5000)
