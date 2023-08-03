from typing import AnyStr
from flask import Flask, request, abort


# from linebot.v3 import (
#     WebhookHandler
# )
# from linebot.v3.webhook import WebhookHandler
import linebot

from linebot.v3.exceptions import (
    InvalidSignatureError
)
# from linebot.models import (
#     MessageEvent, TextMessage, TextSendMessage,ImageSendMessage,PostbackEvent,
# )

from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)

from linebot.v3.webhooks import (
    MessageEvent,
    PostbackEvent,
    TextMessageContent

)

# from config import *
from Function import *
from random_speak import  *
import os
import requests
import re
from bs4 import BeautifulSoup
import random
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
import openai
import json

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
CHANNEL_ACCESS_TOKEN = os.getenv('CHANNEL_ACCESS_TOKEN')
CHANNEL_SECRET = os.getenv('CHANNEL_SECRET')

app = Flask(__name__)

# line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
# handler = WebhookHandler(CHANNEL_SECRET)

configuration = Configuration(access_token=CHANNEL_ACCESS_TOKEN)
# handler = WebhookHandler(CHANNEL_SECRET)
handler = handler = linebot.v3.WebhookHandler(CHANNEL_SECRET)

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
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
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
    # =================    飛場位置 第二頁   ======================================================
        elif event.postback.data == 'FlyField2':
            message = field_location_2()
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
            # ===== Inav ======
        elif event.postback.data == 'InaVersion':
            r = requests.get('https://github.com/iNavFlight/inav/releases')
            soup = BeautifulSoup(r.text,"html.parser")
            results = soup.find_all('a',class_ = "Link--primary",attrs={"data-view-component": "true"})
            msg = results[0].string
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=msg))
            # ===== OpenTX ======
        elif event.postback.data == 'OpenTxVersion':
            r = requests.get('https://www.open-tx.org/downloads')
            soup = BeautifulSoup(r.text, 'html.parser')
            msg = soup.find('div',class_='post_info').select_one('a').string
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=msg))
        elif event.postback.data == 'EdgeTxVersion':
            r = requests.get('https://github.com/EdgeTX/edgetx')
            soup = BeautifulSoup(r.text,"html.parser")
            msg = soup.find('span',class_ = "css-truncate css-truncate-target text-bold mr-2").string
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=msg))
        # =================    選單第二頁    ========================================================== 
        elif event.postback.data == 'to_menu2':
            message = menu2()
            line_bot_api.reply_message(event.reply_token, message)
        elif event.postback.data == 'droneInfo':
            message = carousel_template()
            line_bot_api.reply_message(event.reply_token, message)
        # =================    雷達回波    ===============
        elif event.postback.data == 'ladar':
            r = requests.get('https://www.cwb.gov.tw/V8/C/W/OBS_Radar.html')
            soup = BeautifulSoup(r.text,'html')
            x = soup.find_all('meta')
            png_url = x[5].get('content')
            line_bot_api.reply_message(event.reply_token, ImageSendMessage(original_content_url=png_url, preview_image_url=png_url))

        
        
@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    ans = event.message.text
    app.logger.info("-------------"+ans+"------------------")
    print("-------------"+ans+"------------------")
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)

        if ans == '正妹' or ans.lower() =='beauty' or ans == '抽' or ans == "美女" or ans == "振銓前女友":

            response = requests.get('https://www.jkforum.net/type-736-1940.html?forumdisplay&typeid=1940&filter=typeid&typeid=1940&forumdisplay=&page=1')
            soup = BeautifulSoup(response.text, 'html.parser')
            # max_page = soup.find_all('label')[0].find('span').string.split(' ')[2]
            max_page = int(soup.find_all(title=re.compile('共\s\d+\s頁'))[0].string.split(' ')[2])
            random_page = random.randint(1, int(max_page)-2)

            # url = f"https://www.jkforum.net/forum-736-{random_page}.html"
            url = f"https://www.jkforum.net/type-736-1940.html?forumdisplay&typeid=1940&filter=typeid&typeid=1940&forumdisplay=&page={random_page}"
            res = requests.get(url)
            soup = BeautifulSoup(res.text, 'html.parser')
            images = soup.find_all("img", src=re.compile("https://www.my"))[:-3]
            images_len = len(images)
            image_url = soup.find_all("img", src=re.compile("https://www.my"))[:-3][random.randint(0, images_len-1)].get("src")

            line_bot_api.reply_message(event.reply_token, ImageSendMessage(original_content_url=image_url, preview_image_url=image_url))
        elif ans == "振銓的女友" or ans == "振銓的女朋友" or ans == "振銓女友" :
            print("girl friend called")
            image_url = "https://pic3.zhimg.com/v2-e0aec76fb91e6d788b3cfe3cfa4afc8e_b.jpg"
            line_bot_api.reply_message(event.reply_token, ImageSendMessage(original_content_url=image_url, preview_image_url=image_url))
        elif ans.lower() == "選單":
            print("menu called")
            message = menu1()
            # line_bot_api.reply_message(event.reply_token, message)
            
            line_bot_api.reply_message(ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=message
            ))

        elif ans == "雷達":
            r = requests.get('https://www.cwb.gov.tw/V8/C/W/OBS_Radar.html')
            soup = BeautifulSoup(r.text,'html')
            x = soup.find_all('meta')
            png_url = x[5].get('content')
            line_bot_api.reply_message(event.reply_token, ImageSendMessage(original_content_url=png_url, preview_image_url=png_url))

        elif re.match(r'\w{3}天氣', ans) != None:
            county_Id_map = {"新北市":"65", "台北市":"63", "桃園市":"68","新竹市":"10018","新竹縣":"10004","苗栗縣":"10005", "台中市":"66","彰化市": "10007",
                    "雲林縣":"10009", "嘉義縣":"10010", "嘉義市":"10020","南投縣":"10008","台南市":"67", "高雄市":"64","屏東縣":"10013", "台東縣":"10014",
                    "花蓮縣":"10015", "宜蘭縣":"10002", "基隆市":"10017", "澎湖縣":"10016","金門縣":"09020","連江縣":"09007"}
            headers = {'user-agent': 'Mozilla/5.0'}
            res = requests.get(f'https://www.cwb.gov.tw/V8/C/W/County/MOD/Week/{county_Id_map[ans[0:3]]}_Week_m.html', headers = headers)
            soup = BeautifulSoup(res.text, 'html.parser')
            date_ls =[]
            day_ls = [] 
            nights_ls = []
            All = f"「{ans[0:3]}」一週天氣預測：\n"
            dates = soup.find_all('span', class_="date")
            for i in range(7):
                date_ls.append(dates[i].text)
                
            days = soup.find_all('span',class_='Day')
            for i in range(7):
                day_ls.append(days[i].find('img').get('alt'))
                
            nights = soup.find_all('span',class_='Night')
            for i in range(7):
                nights_ls.append(nights[i].find('img').get('alt'))

            for i in range(7):
                All+=f"{date_ls[i][0:3]}({date_ls[i][3:]}):\n白天: {day_ls[i]} , 晚上: {nights_ls[i]}。 \n\n"
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=All))

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
        elif ans == '埔里飛場':
            location_message = LocationSendMessage(
                title='埔里內埔飛場',
                address='545南投縣埔里鎮內埔路15-9號',
                latitude=23.980823,
                longitude=120.997347
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
        elif ans == '遠雄之星':
            location_message = LocationSendMessage(
                title='遠雄之星',
                address='436台中市清水區槺榔里',
                latitude=24.264597,
                longitude=120.540203
            )
            line_bot_api.reply_message(event.reply_token, location_message)
        elif ans == 'test':
             line_bot_api.reply_message(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[TextMessage(text="測試成功")]
                    )
                )
        elif ans[0:2] == "AI" and (ans[2] ==":" or ans[2] == "："):
            # print("openai get it ") 
            openai.api_key = OPENAI_API_KEY
            ans = ans[3:]
            print(ans)
            response = openai.Completion.create(
            model='text-davinci-003',
            prompt= ans + ' ,請用繁體中文回答' ,
            max_tokens=1024,
            temperature=0.5)

            # 接收到回覆訊息後，移除換行符號
            reply_msg = response["choices"][0]["text"].replace('\n','')
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=reply_msg))
        elif ans == "喵":
            url = "https://unsplash.com/s/photos/kitten"
            r = requests.get(url)
            soup = BeautifulSoup(r.text,'html.parser')
            x = soup.find_all('div', class_ = "MorZF")
            temp =[]
            for i in x:
                temp.append(i.select('img')[0].get('src'))
            img_url = temp[random.randint(0,len(temp)-1)]
            line_bot_api.reply_message(event.reply_token, ImageSendMessage(original_content_url=img_url, preview_image_url=img_url))
        elif ans == "汪":
            url = "https://unsplash.com/s/photos/doggy"
            r = requests.get(url)
            soup = BeautifulSoup(r.text,'html.parser')
            x = soup.find_all('div', class_ = "MorZF")
            temp =[]
            for i in x:
                temp.append(i.select('img')[0].get('src'))
            img_url = temp[random.randint(0,len(temp)-1)]
            line_bot_api.reply_message(event.reply_token, ImageSendMessage(original_content_url=img_url, preview_image_url=img_url))
        elif ans == "穿越機介紹":
            url = "https://www.youtube.com/watch?v=iM3R4Imulj0"
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=url))
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