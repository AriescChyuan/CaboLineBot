import random
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,ImageSendMessage
)
import requests
import os
from bs4 import BeautifulSoup
import random
import re
def talk_to_you(msg):
    if msg.find('咖波')!=-1 or msg.find('卡波')!=-1 or msg.find('cabo')!=-1 :
        # 被罵反應
        if msg.find('笨') != -1  :
            talk = '哭么阿！！'
        elif  msg.find('智障') != -1  :
            talk = '你才低能兒 凸！！'
        elif  msg.find('白目') != -1  :
            talk = '你才白目'
        elif  msg.find('醜') != -1  :
            talk = '你有照過鏡子嗎？ 還敢說我'
        elif  msg.find('廢') != -1  :
            talk = '你也沒多有用阿！'
        elif  msg.find('呆') != -1  :
            talk = '你才呆啦 ！！'
        elif  msg.find('去死') != -1  :
            talk = '你才去死啦 哼！！'
        elif  msg.find('肥') != -1 or msg.find('胖') != -1 or msg.find('豬') != -1:
    
            if msg.find('肥')!=-1:
                talk = '你才肥'
            elif msg.find('胖')!=-1:
                talk = '你才大胖子'
            elif msg.find('豬')!=-1:
                talk = '你爸媽是豬，才生你這個豬兒子！！'
        else :
            x =int(random.random()*5)
            if x == 0:
                talk = '幹嘛？'
            elif x == 1:
              talk = '???'
            elif x == 2 :
              talk = '請問有什麼事嗎？'
            elif x ==3 :
              talk = '什麼？'
            elif x == 4 :
              talk = '沒空啦'
            elif x ==5:
              talk = 'zZZ'
    

    return talk 
def give_picture(msg):
    if msg.find('咖波')!=-1 or msg.find('卡波')!=-1 or msg.find('cabo')!=-1 :
        if (msg.find('照片') != -1 or  msg.find('圖片') !=-1) and msg.find('的') !=-1:
            goal = msg[msg.index('張')+1 : msg.index('的')]
        elif msg.find('照片') != -1:
            goal = msg[msg.index('張')+1 : msg.index('照')]
        elif msg.find('圖片') !=-1:
            goal = msg[msg.index('張')+1 : msg.index('圖')]
#         elif (msg.find('照') != -1 or  msg.find('圖') !=-1) and msg.find('美') != -1 and msg.find('的') != -1:
#             goal = msg[msg.index('張')+1 : msg.index('的')]
#         elif (msg.find('照') != -1 or  msg.find('圖') !=-1) and msg.find('美') != -1:
#             goal = msg[msg.index('張')+1 : msg.rfind('美')]
        elif msg.find('照') != -1 :
            goal = msg[msg.index('張')+1 : msg.find('照')]
        elif msg.find('圖') !=-1:
            goal = msg[msg.index('張')+1 : msg.find('圖')]

        r = requests.get('https://unsplash.com/s/photos/{}'.format(goal))
        soup = BeautifulSoup(r.text, "html.parser") 
        x = soup.find_all('img',{'class','oCCRx'})
        url_list =  [u.get('src') for u in x]
        random_index = random.randrange(len(url_list))
        return url_list[random_index]
def random_talk():
    x =int(random.random()*2500)
    print('x= ',x)
    talk = ''
    if x < 5:
        talk = '嘻嘻'
    elif x >= 10 and x < 20:
        talk = '好無聊 Q_Q'
    elif x >=20 and x <30:
        talk = "想便便 >O< " 
    elif x >=30 and x <40:
        talk = '好想看電影～'
    elif x >=40 and x< 50:
        talk = '剛剛夢到 好吃的甜甜圈耶 XD'
    elif x >= 50 and x <60:
        talk = '妮妮喜歡什麼動物呢？'
    elif x >= 60 and x <70:
        talk = '剛剛振銓好像又偷吃餅乾耶...'
    elif x >= 70 and x < 75:
        talk = '聽說曾經有一隻可愛又乖巧的老鼠～ 牠叫 跑跑 @@a'
    elif x >= 75  and x <80:
        talk = '嘻嘻 我不用上班～'
    elif x >= 80  and x <85:
        talk = '冷氣是不是有點冷 >o<'
    elif x >= 85  and x <90:
        talk = '噓！ 我要睡覺了zZZ'
    elif x >= 90  and x <95:
        talk = '幹麻？'
    elif x >= 95  and x <100:
        talk = '垃圾不能亂丟呦 留著丟討厭的人 ㄒㄒ'
    elif x >= 100  and x <105:
        talk = '有沒有認真運動呀！！'
    elif x >= 105  and x <110:
        talk = '守宮餵了嗎？'
    elif x >= 110  and x <115:
        talk = '銓銓這禮拜要飛飛機嗎？ 我想跟去看！！'
    elif x >= 115  and x <120:
        talk = '哈揪～～～ >3<'
    elif x >= 120  and x <125:
        talk = '晚安囉 zZZ'
    elif x >= 125 and x <130:
        talk = '聽說明天會下雨耶！'
    elif x >= 130 and x <135:
        talk = 'Hi~'
    elif x >= 135 and x <140:
        talk = '什麼時候我也會收到禮物呀！！'
    elif x >= 140 and x <145:
        talk = '小布丁把餅乾吃完了...'

    return talk
