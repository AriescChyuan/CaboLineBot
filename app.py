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
from random_speak import  *
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
    response = talk_to_you(msg)
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=response))
    url = give_picture(msg)
    line_bot_api.reply_message(event.reply_token,ImageSendMessage(original_content_url=url, preview_image_url=url))
    # if msg.find('咖波')!= -1 and msg.find('笨') != -1  :
    #     line_bot_api.reply_message(event.reply_token,TextSendMessage(text=('哭么阿！！')))
    # elif msg.find('咖波')!= -1 and msg.find('智障') != -1  :
    #     line_bot_api.reply_message(event.reply_token,TextSendMessage(text=('你才低能兒 凸！！')))
    # elif msg.find('咖波')!= -1 and msg.find('白目') != -1  :
    #      line_bot_api.reply_message(event.reply_token,TextSendMessage(text=('你才白目')))
    # elif msg.find('咖波')!= -1 and msg.find('醜') != -1  :
    #     line_bot_api.reply_message(event.reply_token,TextSendMessage(text=('你有照過鏡子嗎？ 還敢說我')))
    # elif msg.find('咖波')!= -1 and msg.find('肥') != -1 or msg.find('胖') != -1 or msg.find('豬') != -1:
    
    #     if msg.find('肥')!=-1:
    #         talk = '你才肥'
    #     elif msg.find('胖')!=-1:
    #         talk = '你才大胖子'
    #     elif msg.find('豬')!=-1:
    #         talk = '你爸媽是豬，才生你這個豬兒子！！'
    #     line_bot_api.reply_message(event.reply_token,TextSendMessage(text=talk))
    # elif msg.find('咖波')!=-1 or msg.find('卡波')!=-1 or msg.find('cabo')!=-1 :
    #     x =int(random.random()*5)
    #     if x == 0:
    #         talk = '幹嘛？'
    #     elif x == 1:
    #         talk = '???'
    #     elif x == 2 :
    #         talk = '請問有什麼事嗎？'
    #     elif x ==3 :
    #         talk = '什麼？'
    #     elif x == 4 :
    #         talk = '沒空啦'
    #     elif x ==5:
    #         talk = 'zZZ'

    #     line_bot_api.reply_message(event.reply_token,TextSendMessage(text=talk))

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
    elif msg == "電影":
        url = 'https://movies.yahoo.com.tw/'
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser') 
        x = soup.select('ul.ranking_list_r a')
        movie_ranking = '近期前五名電影:\n'

        for index, i in enumerate(x) :
            if index == 5:
                break
            # title = i.find('span').text
            link = i['href']
            # movie_ranking += "{}\n{}\n".format(title,link)
            movie_ranking += link+'\n'
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=movie_ranking))
    elif msg == "新聞":
       url = 'https://news.google.com/topics/CAAqKggKIiRDQkFTRlFvSUwyMHZNRFZxYUdjU0JYcG9MVlJYR2dKVVZ5Z0FQAQ?hl=zh-TW&gl=TW&ceid=TW%3Azh-Hant'
       res = requests.get(url)
       soup = BeautifulSoup(res.text, 'html.parser') 
       x = soup.select('article.MQsxIb.xTewfe.R7GTQ.keNKEd.j7vNaf.Cc0Z5d.EjqUne a.VDXfz')
       news =''
       for index, data in enumerate(x):
           if index==5:
               break
           url = data['href']
           news += "https://news.googlÇÇe.com/{}\n".format(url)
       line_bot_api.reply_message(event.reply_token,TextSendMessage(text=news))

    else:        
        talk = random_talk()   
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=talk))


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)