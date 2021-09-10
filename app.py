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
import re

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
        r = requests.get('https://www.tooopen.com/img/89_869.aspx')

        # soup = BeautifulSoup(r.text, 'html.parser')
        # imgs = soup.find_all('img',limit=None)
        # imgs_list = []
        # for i in imgs[2:]:
        #     imgs_list.append(i.get('src'))
        # random_index = random.randrange(len(imgs[2:]))
        # line_bot_api.reply_message(event.reply_token,ImageSendMessage(original_content_url=imgs_list[random_index], preview_image_url=imgs_list[random_index]))
        IU_URL = requests.get('https://imgur.com/search/score?q=cat')
        soup = BeautifulSoup(IU_URL.text,'html')
        x = soup.find_all('img')
        cat_img_list = []
        for i in x[3:]:
            cat_img_list.append('https:' + i.get('src'))
        random_index = random.randrange(len(cat_img_list))
        line_bot_api.reply_message(event.reply_token,ImageSendMessage(original_content_url=cat_img_list[random_index], preview_image_url=cat_img_list[random_index]))

    elif msg == "功能":
        message = buttons_message()
        line_bot_api.reply_message(event.reply_token, message)

    elif msg == "IU":
        IU_URL = requests.get('https://imgur.com/search/score?q=iu')
        soup = BeautifulSoup(IU_URL.text,'html')
        x = soup.find_all('img')
        IU_img_list = []
        for i in x[3:]:
            IU_img_list.append('https:' + i.get('src'))
        random_index = random.randrange(len(IU_img_list))
        line_bot_api.reply_message(event.reply_token,ImageSendMessage(original_content_url=IU_img_list[random_index], preview_image_url=IU_img_list[random_index]))
    elif msg == "抽sweethouse商品":
        r = requests.get('https://www.sweethousetw.com/products/')
        soup = BeautifulSoup(r.text,'html')
        x = soup.find_all('a',href=re.compile('^/products/'))
        product_url__list = []
        product_photo_list = []
        for i in range(len(x)):
            product_url__list.append(x[i].get('href'))
            if x[i].find(class_ = "boxify-image center-contain sl-lazy-image") == None:
                product_photo_list.append('None')
            else:
                product_photo_list.append(x[i].find(class_ = "boxify-image center-contain sl-lazy-image").get('style').split('(')[-1][:-2])
        random_index = random.randrange(len(product_url__list))
        line_bot_api.reply_message(event.reply_token,ImageSendMessage(original_content_url=product_photo_list[random_index], preview_image_url=product_photo_list[random_index]))
        # line_bot_api.reply_message(event.reply_token,TextSendMessage('https://www.sweethousetw.com/' + product_url__list[random_index]))

    elif msg == "雷達":
        r = requests.get('https://www.cwb.gov.tw/V8/C/W/OBS_Radar.html')
        soup = BeautifulSoup(r.text,'html')
        x = soup.find_all('meta')
        png_url = x[5].get('content')
        line_bot_api.reply_message(event.reply_token, ImageSendMessage(original_content_url=png_url, preview_image_url=png_url))

    else:            
        line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=event.message.text + ' @_@a'))
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event,destination):
    print('event',event)
    print('destination',destination)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)