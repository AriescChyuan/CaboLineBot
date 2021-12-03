import paho.mqtt.client as mqtt
# import random
import json  
import datetime 
import time

def fan_control():
    # 設置日期時間的格式
    ISOTIMEFORMAT = '%m/%d %H:%M:%S'

    # 連線設定
    # 初始化地端程式
    client = mqtt.Client()

    # 設定登入帳號密碼
    client.username_pw_set("Bruce","Aries19920321")

    # 設定連線資訊(IP, Port, 連線時間)
    client.connect("337d8bc43b214494bf2990e1f5d1e905.s2.eu.hivemq.cloud", 8883, 60)

    while True:
        # t0 = random.randint(0,30)
        t = datetime.datetime.now().strftime(ISOTIMEFORMAT)
        payload = {'message' : 'on' , 'Time' : t}
        print (json.dumps(payload))
        #要發布的主題和內容
        client.publish("linebot/linebot", json.dumps(payload))
        # time.sleep(5)
        break