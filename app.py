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

line_bot_api = LineBotApi('qy1Mjg+YSTKKmHoN48DY4x8mDLS+AdduLt5LJJNXu4/F0fCL5bYpp41B3Cw6C6TxoUGyYOTTWZiQ6DymN1rXkgeaiFYLdXMqc4MvzFEIRPkAFwI97TPY59jid/2SQ4XrnwpBnmfaqZu2vuIBi3xRtwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('6967c7157355d0d827398b6968821f71')


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()


