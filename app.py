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

line_bot_api = LineBotApi('nU5RAEvJdjbjMPuvemDBYMsB1XSU+0mwS01/hR38amqqR8HtKiPdEBIGKfdnEg2mj7t+90PraaDEHzO5NmYuUlhShLc/O7hkw9E6OTO2+UcUUZ0OQ0pzdWzCplqawZC1T5OIX7fD7TBWi6NrUwOzugdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('4a98903311f5786863511cea1569ecf7')


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
    app.run( port=5000)