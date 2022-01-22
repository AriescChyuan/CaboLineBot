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
            thumbnail_image_url="https://i.imgur.com/QPc6mx8.jpg",
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
                PostbackTemplateAction(
                    label="各飛場位置",
                    # text="飛場位置",
                    data='FlyField'
                ),
                PostbackTemplateAction(
                    label="遙控器撥桿功能(BetaFlight)",
                    data="StickFun"
                ),
                PostbackTemplateAction(
                    label="各韌體目前版本",
                    # text="各韌體目前版本",
                    data="FirmwareVer"
                ),
                MessageTemplateAction(
                    label="雷達回波圖",
                    text="雷達"
                )
                
            ]
        )
    )
    return message
def field_location():
    message = TemplateSendMessage(
        alt_text='飛場位置',
        template=ButtonsTemplate(
            thumbnail_image_url="https://i.imgur.com/QPc6mx8.jpg",
            title="飛場位置",
            text="選擇您想去的位置",
            actions=[
                MessageTemplateAction(
                    label="烏日",
                    text="烏日飛場",
                ),
                MessageTemplateAction(
                    label="芬園",
                    text="芬園飛場"
                ),
                MessageTemplateAction(
                    label="一江橋",
                    text="一江橋飛場"
                ),
                MessageTemplateAction(
                    label="員林",
                    text="員林飛場"
                ),
                # MessageTemplateAction(
                #     label="下一頁",
                #     text="飛場位置下一頁"
                # )
                
            ]
        )
    )
    return message
def firmware_version():
    message = TemplateSendMessage(
        alt_text='目前韌體版本',
        template=ButtonsTemplate(
            thumbnail_image_url="https://i.imgur.com/QPc6mx8.jpg",
            title="查看韌體當前版本",
            text="選擇您想知道的韌體",
            actions=[
                PostbackTemplateAction(
                    label="BetaFlight",
                    # text="Beta_Version",
                    data='BetaVersion'
                ),
                PostbackTemplateAction(
                    label="Inav",
                    text="InavVersion",
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
