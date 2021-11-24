from typing import AnyStr
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
from config import *
from Function import *
from random_speak import  *
import os
import requests
from bs4 import BeautifulSoup
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.chrome.options import Options

from QnAMaker import *
from SendPicture import *
from RichMenu import *
app = Flask(__name__)

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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text

    ans = QnAMaker(msg)

    # url = give_picture(msg)
    # response = talk_to_you(msg)
    # greeting_resp = greeting(msg)
    # if url != None:
        # line_bot_api.reply_message(event.reply_token,ImageSendMessage(original_content_url=url, preview_image_url=url))
    # elif response != None:
    #     line_bot_api.reply_message(event.reply_token,TextSendMessage(text=response))
    # elif greeting_resp != None:
    #     line_bot_api.reply_message(event.reply_token,TextSendMessage(text=greeting_resp))
    if ans == '正妹':
        img = sendPicture(ans)
        line_bot_api.reply_message(event.reply_token, ImageSendMessage(original_content_url=img, preview_image_url=img))

    elif ans == '帥哥':
        img = sendPicture(ans)
        line_bot_api.reply_message(event.reply_token, ImageSendMessage(original_content_url=img, preview_image_url=img))

    elif ans.lower() == "menu":
        message = buttons_message()
        line_bot_api.reply_message(event.reply_token, message)

    elif ans == "雷達":
        r = requests.get('https://www.cwb.gov.tw/V8/C/W/OBS_Radar.html')
        soup = BeautifulSoup(r.text,'html')
        x = soup.find_all('meta')
        png_url = x[5].get('content')
        line_bot_api.reply_message(event.reply_token, ImageSendMessage(original_content_url=png_url, preview_image_url=png_url))

    elif ans == "電影":
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

    elif ans == "新聞":
        r = requests.get('https://www.ettoday.net/news/hot-news.htm')
        soup = BeautifulSoup(r.text,"html.parser")
        results = soup.select('.piece > .pic',limit=5)
        news = ''
        for i in results:
            news += 'https://www.ettoday.net{}\n'.format(i.get('href')+'l')
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=news))
    elif ans == '測試':
        pass
    elif ans == '晚餐':
        ls = ['麥當勞','雞滷飯','火鍋','炒飯','泡麵','水果吃到飽']
        ans = random.choice(ls)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=ans))
    else:       
        if ans != '':    
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=ans))
        # talk = random_talk()   
        # if talk != "":
        #     line_bot_api.reply_message(event.reply_token,TextSendMessage(text=talk))
        # else:
        #     pass

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)