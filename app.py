import os
import requests
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from linebot.exceptions import InvalidSignatureError
from flask import Flask, request, abort

app = Flask(__name__)

# LINE Botのチャンネルアクセストークンとチャンネルシークレット
CHANNEL_ACCESS_TOKEN = os.environ.get("CHANNEL_ACCESS_TOKEN")
CHANNEL_SECRET = os.environ.get("CHANNEL_SECRET")

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

# DeepL APIキー
DEEPL_API_KEY = os.environ.get("DEEPL_API_KEY")

# ユーザーごとの言語設定を保存する辞書
user_language_preferences = {}

def translate_text(text, target_language):
    # DeepL APIにテキストを送信して翻訳する
    url = "https://api.deepl.com/v2/translate"
    params = {
        "auth_key": DEEPL_API_KEY,
        "text": text,
        "target_lang": target_language
    }
    response = requests.post(url, data=params)
    translation = response.json()["translations"][0]["text"]
    return translation

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
    user_id = event.source.user_id
    user_input = event.message.text

    if user_input.startswith("/translate"):
        # ユーザーが言語を指定した場合
        _, target_language = user_input.split(" ", 1)
        user_language_preferences[user_id] = target_language
        response_message = f"言語を {target_language} に設定しました。"
    else:
        # ユーザーがテキストを送信した場合
        if user_id in user_language_preferences:
            target_language = user_language_preferences[user_id]
        else:
            target_language = "EN"  # デフォルトの翻訳言語

        translation = translate_text(user_input, target_language)
        response_message = f"翻訳結果 ({target_language}): {translation}"

    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=response_message))

if __name__ == "__main__":
    app.run()