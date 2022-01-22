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
                PostbackTemplateAction(
                    label="雷達回波圖",
                    # text="雷達"
                    data="ladar"
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
                    # text="InavVersion",
                    data="InaVersion"
                ),
                PostbackTemplateAction(
                    label="OpenTX",
                    # text="OpenTxVersion",
                    data="OpenTxVersion"
                ),
                PostbackTemplateAction(
                    label="EdgeTX",
                    # text="EdgeTxVersion",
                    data="EdgeTxVersion"
                ),
            ]
        )
    )
    return message
#TemplateSendMessage - ConfirmTemplate(確認介面訊息)
def carousel_template():
    carousel_template_message = TemplateSendMessage(
    alt_text='Carousel template',
    template=CarouselTemplate(
        columns=[
            CarouselColumn(
                thumbnail_image_url='https://dflyvision.com/wp-content/uploads/2020/10/cinematic-fpv-drone-spain-3.jpg',
                title='穿越機相關',
                text='穿越機相關',
                actions=[
                    URIAction(
                        label='招式教學(初級)',
                        uri='https://www.youtube.com/watch?v=VnKg2aCTPtk&list=PLj23ZLg5V56prLy-r3-GVd_9wBU4iVC7H'
                    ),
                    URIAction(
                        label='招式教學(中級)',
                        uri='https://www.youtube.com/watch?v=FamqCNGrq2M&list=PLj23ZLg5V56qvExRVYQkBq6bUsJjwHQqZ'
                    ),
                    URIAction(
                        label='招式教學(高級)',
                        uri='https://www.youtube.com/watch?v=rsA_llKYtSE&list=PLj23ZLg5V56q99molL1nY1XVa0j42cnzl'
                    ),
                    URIAction(
                        label='測試',
                        uri=''
                    ),
                    
                ]
            ),
            CarouselColumn(
                thumbnail_image_url='https://example.com/item2.jpg',
                title='this is menu2',
                text='description2',
                actions=[
                    PostbackAction(
                        label='postback2',
                        display_text='postback text2',
                        data='action=buy&itemid=2'
                    ),
                    MessageAction(
                        label='message2',
                        text='message text2'
                    ),
                    URIAction(
                        label='uri2',
                        uri='http://example.com/2'
                     )
                    ]
             )
            ]
        )
    )
    return carousel_template_message
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
