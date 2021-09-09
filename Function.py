from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *

import requests
from bs4 import BeautifulSoup

#TemplateSendMessage - ButtonsTemplate (按鈕介面訊息)
def buttons_message():
    message = TemplateSendMessage(
        alt_text='Hello ~*',
        template=ButtonsTemplate(
            thumbnail_image_url="https://shoplineimg.com/5b792cc067962300148050a5/5fe1be2fa88493003b811c4a/x200.webp?source_format=png",
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
                URITemplateAction(
                    label="SweetHouse官方網站",
                    uri="https://www.sweethousetw.com/"
                ),
                MessageTemplateAction(
                    label="抽IU",
                    text="IU"
                ),
                MessageTemplateAction(
                    label="抽SweetHouse商品",
                    text="抽sweethouse商品"
                ),
                MessageTemplateAction(
                    label="查看雷達回波圖",
                    text="雷達"
                ),
                
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