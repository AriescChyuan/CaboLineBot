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
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time

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

    url = give_picture(msg)
    response = talk_to_you(msg)

    if url != None:
        line_bot_api.reply_message(event.reply_token,ImageSendMessage(original_content_url=url, preview_image_url=url))
    elif response != None:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=response))

    elif msg.lower().find('#') == 0:
        # print('driver_path : ',os.environ.get("CHROMEDRIVER_PATH"))
        print('CHROMEDRIVER_VERSION: ',os.environ.get("CHROMEDRIVER_VERSION"))
        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        chrome_options.add_argument("--headless") #無頭模式
        # chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        chrome = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
        chrome = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"))
        print('chrome: ',chrome)
        # chrome = webdriver.Chrome('./chromedriver')
        target = msg
        url_list=[]
        try:
            chrome.get("https://www.instagram.com/")
            username = WebDriverWait(chrome, 30).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            print('username:',username)
            # username.send_keys('jetliayu@gmail.com')
            # password = WebDriverWait(chrome, 10).until(
            #     EC.presence_of_element_located((By.NAME, "password"))
            # )
            # password.send_keys('Aries19920321')
            # password.submit()
            # data_save_windows = WebDriverWait(chrome, 10).until(
            #     EC.element_to_be_clickable((By.XPATH, '//*[@id="react-root"]/section/main/div/div/div/section/div/button'))
            #  ).click()
            # time.sleep(1)
            # search = WebDriverWait(chrome, 10).until(
            #     EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input'))
            # )   
            # search.send_keys(target)
            # time.sleep(0.5)
            # search.send_keys(Keys.RETURN)
            # time.sleep(0.5)
            # search.send_keys(Keys.RETURN)
            # WebDriverWait(chrome, 10).until(
            #     EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/section/main/header/div[2]/div/div[1]/h1'))
            # )
            # imgs = chrome.find_elements_by_class_name("FFVAD")
            # for img in imgs:
            #     url_list.append(img.get_attribute('src'))
            # random_index = random.randrange(len(url_list))
            # line_bot_api.reply_message(event.reply_token,ImageSendMessage(original_content_url=url_list[random_index], preview_image_url=url_list[random_index]))
        finally:
            chrome.quit()


    elif msg == "喵":
        r = requests.get('https://www.tooopen.com/img/89_869.aspx')

        IU_URL = requests.get('https://imgur.com/search/score?q=cat')
        soup = BeautifulSoup(IU_URL.text,'html')
        x = soup.find_all('img')
        cat_img_list = []
        for i in x[3:]:
            cat_img_list.append('https:' + i.get('src'))
        random_index = random.randrange(len(cat_img_list))
        line_bot_api.reply_message(event.reply_token,ImageSendMessage(original_content_url=cat_img_list[random_index], preview_image_url=cat_img_list[random_index]))

    elif msg.lower() == "menu":
        message = buttons_message()
        line_bot_api.reply_message(event.reply_token, message)
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
        if talk != "":
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=talk))
        else:
            pass


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)