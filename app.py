from typing import AnyStr
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,ImageSendMessage,PostbackEvent,
)
from config import *
from Function import *
from random_speak import  *
import os
import requests
import json
from bs4 import BeautifulSoup
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.chrome.options import Options
import datetime
from QnAMaker import *
from SendPicture import *
from RichMenu import *
from mqtt_pub import *
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
@handler.add(PostbackEvent)    
def handle_postback(event):
        print('data =',event.postback.data)
    # =================    飛場位置    =============================================================
        if event.postback.data == 'FlyField':
            message = field_location()
            line_bot_api.reply_message(event.reply_token, message)
    # =================    搖桿功能圖    =============================================================
        elif event.postback.data == 'StickFun':
            image_message = ImageSendMessage(
            original_content_url='https://i.imgur.com/kD4D0Zi.jpg',
            preview_image_url='https://i.imgur.com/kD4D0Zi.jpg')
            line_bot_api.reply_message(event.reply_token, image_message)
    # =================    韌體版本查詢    ===========================================================
        elif event.postback.data == 'FirmwareVer':
            message = firmware_version()
            line_bot_api.reply_message(event.reply_token, message)
            # ===== BetaFlight ======
        elif event.postback.data == 'BetaVersion':
            r = requests.get('https://github.com/betaflight/betaflight/releases')
            soup = BeautifulSoup(r.text,"html.parser")
            results = soup.find_all('a',class_ = "Link--primary",attrs={"data-view-component": "true"})
            msg = results[0].string
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=msg))
        elif event.postback.data == 'InaVersion':
            r = requests.get('https://github.com/iNavFlight/inav/releases')
            soup = BeautifulSoup(r.text,"html.parser")
            results = soup.find_all('a',class_ = "Link--primary",attrs={"data-view-component": "true"})
            msg = results[0].string
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=msg))
        # =================    雷達回波    ===========================================================
        elif event.postback.data == 'ladar':
            r = requests.get('https://www.cwb.gov.tw/V8/C/W/OBS_Radar.html')
            soup = BeautifulSoup(r.text,'html')
            x = soup.find_all('meta')
            png_url = x[5].get('content')
            line_bot_api.reply_message(event.reply_token, ImageSendMessage(original_content_url=png_url, preview_image_url=png_url))

        
        
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    ans = event.message.text
    
    # ans = QnAMaker(msg)

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

    elif ans.lower() == "選單":
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
    elif ans == '骰子':
        dice = ['1','2','3','4','5','6']
        ans = "您擲到的骰子點數為：{}點。".format(random.choice(dice))
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=ans))
    elif ans == 'ELRS':
        url = "官網 ： https://github.com/ExpressLRS/ExpressLRS\n刷韌體軟體 ： https://github.com/ExpressLRS/ExpressLRS-Configurator/releases/\n設定教學 ： https://www.youtube.com/watch?v=SVSJg7AAK0U&t=617s"
              
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=url))
    elif ans == '晚餐':
        ls = ['麥當勞','雞滷飯','火鍋','炒飯','泡麵','水果吃到飽','鍋貼','滷味']
        ans = random.choice(ls)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=ans))
    elif ans == '時間':
        time = '現在時間：'+ datetime.datetime.now().ctime()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=time))
    elif ans == '地震':
        r = requests.get('https://www.cwb.gov.tw/V8/C/E/MOD/EQ_ROW.html?T=2021112514-4')
        soup = BeautifulSoup(r.text,"html.parser")
        results = soup.find_all('a',attrs={'aria-label':'點此看更多詳細資訊'})

        time = location = results[0].find_all('span')[0].text[:-3]
        location = results[0].find('li').text
        maximum = soup.find_all('td',class_='eq_lv-1')[0].text
        depth = results[0].find_all('li')[1].text[2:]
        scale = results[0].find_all('li')[2].text[4:]
        url  = 'https://www.cwb.gov.tw/' + results[0].get('href')
        string = "最近一次地震：\n時間：{}\n地點：{}\n最大震度：{}\n深度：{}\n規模：{}\n點我看更多：{}".format(time, location, maximum, depth, scale, url)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=string))
    elif ans == '電扇開':
        fan_control("1")
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="電扇開"))
    elif ans == '電扇關':
        fan_control("0")
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text="電扇關"))

    elif ans == '烏日飛場':
        location_message = LocationSendMessage(
            title='烏日飛場',
            address='烏日飛場',
            latitude=24.1088411,
            longitude=120.6016898
        )
        line_bot_api.reply_message(event.reply_token, location_message)
    elif ans == '芬園飛場':
        location_message = LocationSendMessage(
            title='芬園飛場',
            address='入口位置',
            latitude=24.0087000,
            longitude=120.6794389
        )
        line_bot_api.reply_message(event.reply_token, location_message)
    elif ans == '一江橋飛場':
        location_message = LocationSendMessage(
            title='一江橋飛場',
            address='台中市太平區新城路',
            latitude=24.1324936,
            longitude=120.7387336
        )
        line_bot_api.reply_message(event.reply_token, location_message)
    elif ans == '員林飛場':
        location_message = LocationSendMessage(
            title='員林飛場',
            address='員林市自行車主題園區',
            latitude=23.9613639,
            longitude=120.6056722
        )
        line_bot_api.reply_message(event.reply_token, location_message)
    
    else:      
        pass
        # if ans != '':    
        #     line_bot_api.reply_message(event.reply_token,TextSendMessage(text=ans))
        # talk = random_talk()   
        # if talk != "":
        #     line_bot_api.reply_message(event.reply_token,TextSendMessage(text=talk))
        # else:
        #     pass

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)