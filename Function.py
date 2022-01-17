from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *

import requests
from bs4 import BeautifulSoup


#TemplateSendMessage - ButtonsTemplate (按鈕介面訊息)
def buttons_message():
    message = TemplateSendMessage(
        alt_text='功能列表',
        template=ButtonsTemplate(
            thumbnail_image_url="https://images.pexels.com/photos/6427953/pexels-photo-6427953.jpeg?cs=srgb&dl=pexels-tom-fisk-6427953.jpg&fm=jpg",
            title="功能列表",
            text="想要什麼功能呢？",
            actions=[
                # DatetimePickerTemplateAction(
                #     label="請選擇生日",
                #     data="input_birthday",
                #     mode='date',
                #     initial='1990-01-01',
                #     max='2019-03-10',
                #     min='1930-01-01'
                # ),
                # 
                MessageTemplateAction(
                    label="今日前五大新聞",
                    text="新聞"
                ),
                MessageTemplateAction(
                    label="近期排行前五名電影",
                    text="電影"
                ),
                MessageTemplateAction(
                    label="雷達回波圖",
                    text="雷達"
                )
                
            ]
        )
    )
    return message

#TemplateSendMessage - ConfirmTemplate(確認介面訊息)
def Confirm_Template():

    message = TemplateSendMessage(
        alt_text='是否註冊成為會員？',
        template=ConfirmTemplate(
            text="是否註冊成為會員？",
            actions=[
                PostbackTemplateAction(
                    label="馬上註冊",
                    text="現在、立刻、馬上",
                    data="會員註冊"
                ),
                MessageTemplateAction(
                    label="查詢其他功能",
                    text="查詢其他功能"
                )
            ]
        )
    )
    return message