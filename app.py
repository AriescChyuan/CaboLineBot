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
import random
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
from  urllib import  parse
from QnAMaker import *

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
    if ans.lower().find('#') == 0:
        texturl = parse.quote(msg[1:])
        # header = {      
        #     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
        #     # 'Cookie': 'wluuid=66;  ',
        #     # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        #     # 'Accept-encoding': 'gzip, deflate, br',
        #     # 'Accept-language': 'zh-CN,zh;q=0.9',
        #     # 'Cache-Control': 'max-age=0',
        #     # 'connection': 'keep-alive'
        #     # , 'Host': 'stock.tuchong.com',
        #     # 'Upgrade-Insecure-Requests': '1'
        #     }
        url="https://stock.tuchong.com/search?term={}".format(texturl)
        req=requests.get(url)
        soup=BeautifulSoup(req.text,'html.parser')
        js=soup.select('script')
        pattern = re.compile(r'(image_id\":(\"\d+\"))')
        va = pattern.findall(str(js))
        # imageid = va.replace("\"",'')
        # x = 'https://weiliicimg9.pstatp.com/weili/l/'+str(imageid)+'.webp'
        # x
        url_list=[]
        for i in range(len(va)):
            url = 'https://weiliicimg9.pstatp.com/weili/l/'+va[i][1].strip('\"')+'.webp'
            url_list.append(url)
        url = random.choice(url_list)
        # url = url_list[random.randint(0,len(url_list)-1)]
        line_bot_api.reply_message(event.reply_token, ImageSendMessage(original_content_url=url, preview_image_url=url))

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
    else:       
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=ans))
        # talk = random_talk()   
        # if talk != "":
        #     line_bot_api.reply_message(event.reply_token,TextSendMessage(text=talk))
        # else:
        #     pass

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)