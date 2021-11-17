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
    # print('event= ', event)
    # print('event.message= ',event.message)
    msg = event.message.text

    url = give_picture(msg)
    response = talk_to_you(msg)

    if url != None:
        line_bot_api.reply_message(event.reply_token,ImageSendMessage(original_content_url=url, preview_image_url=url))
    elif response != None:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=response))
    elif msg.lower().find('#') == 0:
        texturl = parse.quote(str(msg[1:]))
        header = {      
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
            'Cookie': 'wluuid=66;  ',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-encoding': 'gzip, deflate, br',
            'Accept-language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'connection': 'keep-alive'
            , 'Host': 'stock.tuchong.com',
            'Upgrade-Insecure-Requests': '1'
            }
        url="https://stock.tuchong.com/search?term={}".format(texturl)
        req=requests.get(url,headers=header)
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
        line_bot_api.reply_message(event.reply_token, ImageSendMessage(original_content_url=url, preview_image_url=url))
    # elif msg.lower().find('#') == 0:
    #     # print('driver_path : ',os.environ.get("CHROMEDRIVER_PATH"))
    #     # print('CHROMEDRIVER_VERSION: ',os.environ.get("CHROMEDRIVER_VERSION"))
    #     chrome_options = webdriver.ChromeOptions()
    #     #設定瀏覽器的語言為utf-8中文
    #     #chrome_options.add_argument("--lang=zh-CN.UTF8")
    #     #無頭模式
    #     #chrome_options.add_argument("--headless") 
    #     #設定瀏覽器的user agent
    #     # chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0')
    #     chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36')
    #     # chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    #     # chrome_options.add_argument("--disable-dev-shm-usage")
    #     # chrome_options.add_argument("--no-sandbox")
    #     # chrome = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    #     chrome = webdriver.Chrome(options=chrome_options)
    #     target = msg
    #     url_list=[]
    #     try:
    #         chrome.get("https://www.instagram.com/")
    #         print('page_source = ',chrome.page_source)
    #         WebDriverWait(chrome, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="loginForm"]/div/div[1]/div/label/input')))
    #         username_input = chrome.find_elements_by_name('username')[0]
    #         password_input = chrome.find_elements_by_name('password')[0]
    #         username_input.send_keys('jetliayu@gmail.com')
    #         password_input.send_keys('Aries19920321')
    #         print("inputing username and password...")
    #         # ------ 登入 ------
    #         WebDriverWait(chrome, 30).until(EC.presence_of_element_located((By.XPATH,'//*[@id="loginForm"]/div/div[3]/button/div')))
    #         # ------ 網頁元素定位 ------
    #         login_click = chrome.find_elements_by_xpath('//*[@id="loginForm"]/div/div[3]/button/div')[0]
    #         # ------ 點擊登入鍵 ------
    #         login_click.click()
    #         data_save_windows = WebDriverWait(chrome, 5).until(
    #             EC.element_to_be_clickable((By.XPATH, '//*[@id="react-root"]/section/main/div/div/div/section/div/button'))
    #         ).click()
    #         # notify_windows = WebDriverWait(chrome, 5).until(
    #         #     EC.element_to_be_clickable((By.XPATH, '/html/body/div[5]/div/div/div/div[3]/button[2]'))
    #         # ).click()
    #         search = WebDriverWait(chrome, 5).until(
    #             EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input'))
    #         )   
    #         search.send_keys(target)
    #         time.sleep(5)
    #         search.send_keys(Keys.RETURN)
    #         time.sleep(5)
    #         search.send_keys(Keys.RETURN)
    #         WebDriverWait(chrome, 5).until(
    #             EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/section/main/header/div[2]/div/div[1]/h1'))
    #         )
    #         imgs = chrome.find_elements_by_class_name("FFVAD")
    #         for img in imgs:
    #             url_list.append(img.get_attribute('src'))
    #         random_index = random.randrange(len(url_list))
    #         line_bot_api.reply_message(event.reply_token,ImageSendMessage(original_content_url=url_list[random_index], preview_image_url=url_list[random_index]))
    #     finally:
    #         chrome.quit()

    elif msg.lower() == "menu":
        message = buttons_message()
        line_bot_api.reply_message(event.reply_token, message)
    # elif msg == "抽sweethouse商品":
    #     r = requests.get('https://www.sweethousetw.com/products/')
    #     soup = BeautifulSoup(r.text,'html')
    #     x = soup.find_all('a',href=re.compile('^/products/'))
    #     product_url__list = []
    #     product_photo_list = []
    #     for i in range(len(x)):
    #         product_url__list.append(x[i].get('href'))
    #         if x[i].find(class_ = "boxify-image center-contain sl-lazy-image") == None:
    #             product_photo_list.append('None')
    #         else:
    #             product_photo_list.append(x[i].find(class_ = "boxify-image center-contain sl-lazy-image").get('style').split('(')[-1][:-2])
    #     random_index = random.randrange(len(product_url__list))
    #     line_bot_api.reply_message(event.reply_token,ImageSendMessage(original_content_url=product_photo_list[random_index], preview_image_url=product_photo_list[random_index]))
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
        r = requests.get('https://www.ettoday.net/news/hot-news.htm')
        soup = BeautifulSoup(r.text,"html.parser")
        results = soup.select('.piece > .pic',limit=5)
        news = ''
        for i in results:
            news += 'https://www.ettoday.net{}\n'.format(i.get('href')+'l')
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=news))

    else:        
        talk = random_talk()   
        if talk != "":
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=talk))
        else:
            pass


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)