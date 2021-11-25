from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
import urllib
import urllib.request
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,ImageSendMessage
)
from linebot.exceptions import LineBotApiError
from config import *

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
line_bot_userid = USERID

sched = BlockingScheduler()

# 定義排程 : 在周一至周五，每 20 分鐘就做一次 def scheduled_jog()
@sched.scheduled_job('cron', day_of_week='mon-fri', minute='*/20')
def scheduled_job():
    url = "https://linebot-bruce.herokuapp.com/"
    connect = urllib.request.urlopen(url)

@sched.scheduled_job('cron', day_of_week='mon-sun', hour='11',minute='35')
def scheduled_job():
    try:
        text = '早安！！'
        line_bot_api.push_message(line_bot_userid, TextSendMessage(text=text))
    except LineBotApiError as e:
        print('MessagePush Error:',e)

 
sched.start()  





