import os
import openai
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from linebot.exceptions import InvalidSignatureError

# LINE Botのチャンネルアクセストークンとチャンネルシークレット
CHANNEL_ACCESS_TOKEN = os.environ.get("CHANNEL_ACCESS_TOKEN")
CHANNEL_SECRET = os.environ.get("CHANNEL_SECRET")

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

# OpenAI APIキー
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

app = Flask(__name__)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    try:
        handler.handle(request.data.decode('utf-8'), signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_input = event.message.text

    # OpenAI GPT-3にテキストを送信して応答を取得
    response = openai.Completion.create(
        engine="davinci",
        prompt=user_input,
        max_tokens=50
    )
    ai_response = response.choices[0].text

    # LINE Botに応答を送信
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=ai_response))

if __name__ == "__main__":
    app.run()
