from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,ImageSendMessage
)

from Function import *
import os
import requests
from bs4 import BeautifulSoup
import random

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
    # print('event= ', event)
    # print('event.message= ',event.message)

    msg = event.message.text

    if msg == "喵":
        r = requests.get('https://www.google.com/search?q=cat&sxsrf=AOaemvImC7MDwPJ1pYHw4NJkvRuabzvPug:1631091057322&source=lnms&tbm=isch&sa=X&ved=2ahUKEwid_8TY_-7yAhUHBZQKHdNFCGsQ_AUoAnoECAEQBA&biw=1440&bih=638')
        soup = BeautifulSoup(r.text, 'html.parser')
        imgs = soup.find_all('img')
        imgs_list = []
        for i in imgs:
            imgs_list.append(i.get('src'))
        random_index = random.randrange(len(imgs_list))
        line_bot_api.reply_message(event.reply_token,ImageSendMessage(original_content_url=imgs_list[random_index], preview_image_url=imgs_list[random_index]))
    elif msg == "功能":
        message = buttons_message()
        line_bot_api.reply_message(event.reply_token, message)

    else:            
        line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=event.message.text + ' @_@a'))


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)