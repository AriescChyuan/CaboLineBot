import time
import paho.mqtt.client as paho
from paho import mqtt
# import json  
# import datetime 
def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)

def on_publish(client, userdata, mid, properties=None):
    print("mid: " + str(mid))

def fan_control():
    client = paho.Client(client_id="123", userdata=None, protocol=paho.MQTTv5)
    client.on_connect = on_connect
    client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
    client.username_pw_set("Bruce", "Aries19920321")
    client.connect("337d8bc43b214494bf2990e1f5d1e905.s2.eu.hivemq.cloud", 8883)
    client.on_publish = on_publish

    while True:
        
        print('hi')
        client.publish("linebot/linebot", payload="on", qos=1)
        time.sleep(2)
        break