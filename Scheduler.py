# from apscheduler.schedulers.blocking import BlockingScheduler

# scheduler = BlockingScheduler()
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()
@scheduler.scheduled_job('cron', hour='8-23')
def request_update_status():
    print('Doing job')

scheduler.start()