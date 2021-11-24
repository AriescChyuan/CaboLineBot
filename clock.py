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
from config import *

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
scheduler = BackgroundScheduler()
# sched = BlockingScheduler()

# 定義排程 : 在周一至周五，每 20 分鐘就做一次 def scheduled_jog()
@scheduler.scheduled_job('cron', day_of_week='mon-fri', minute='*/20')
def scheduled_job():
    url = "https://linebot-bruce.herokuapp.com/"
    connect = urllib.request.urlopen(url)
@scheduler.test_job('cron', day_of_week='mon-fri', minute='*/20')
def test_job():
    url = "https://linebot-bruce.herokuapp.com/"
    connect = urllib.request.urlopen(url)
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=movie_ranking))
scheduler.start()  # 啟動排程