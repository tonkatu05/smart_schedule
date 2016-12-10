from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

CHANNEL_ACCESS_TOKEN = "Ntaj7mJX7ND9t/w/oyx2AHswL/Sw2SeQov8nXnuBrHOAm/Z/GprbxZ7/RAzcSNEEYkU3Jqt5o8ded9wvNP+F+sgZFdtV2wos8kcAk9ooV3VdS5V7eg7k1hR68GKNXb2fQ++vvjBqB7S7Tlq2UnFhRQdB04t89/1O/w1cDnyilFU="
CHANNEL_SECRET = "35bd4afd5d85a5ae77a1d84aa3cfb7ec"

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    print("Called")

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text)
    )


if __name__ == "__main__":
    app.run()