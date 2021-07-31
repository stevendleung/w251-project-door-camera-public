import cv2
import numpy as np
import paho.mqtt.client as mqtt
import sys
from datetime import datetime, timedelta
import os
import secrets

import argparse
import time
from pathlib import Path

# Mosquitto 
# LOCAL_MQTT_HOST= "mosquitto-service"
LOCAL_MQTT_HOST= "localhost"
LOCAL_MQTT_PORT= 31126
LOCAL_IMAGE_TOPIC= "image_topic"
LOCAL_NOTIF_TOPIC= "model_output_topic"
LISTEN_TO_TOPIC = LOCAL_IMAGE_TOPIC
#LISTEN_TO_TOPIC = LOCAL_NOTIF_TOPIC

local_mqttclient = mqtt.Client()

# Define Local Sender MQTT callbacks
def on_connect_local(client, userdata, flags, rc):
    if rc == 0:
        print("Successfully connected to local broker with rc: " + str(rc))
        local_mqttclient.subscribe(LISTEN_TO_TOPIC)
    else: 
        print("Error - Couldn't connect to local broker, rc code: " + str(rc))

def on_disconnect_local(client, userdata, flags, rc): 
    print("Disconnected from local broker, result code" + str(rc))
    local_mqttclient.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_PORT, 60)

def on_publish_local(client, userdata, msg_id, rc):
    print("Message successfully published: {}".format(msg_id))

def on_subscribe_local(client, userdata, msg_id, rc):
    if rc == 0:
        print("Successfully subscribed to local topic with rc: " + str(rc))
    else:
        print("Failed to subscribe to local topic with rc: " + str(rc))

def on_message(client, userdata, msg):
    # parse the input message
    new_msg = msg.payload.decode("utf-8")

    print("Message Received: ", new_msg)

    return

def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--topic', type=str, default='image_topic', help='image_topic and model_output_topic are topic options')
    opt = parser.parse_args()
    return opt

def main(topic='image_topic',  # default topic
        ):
    # Assign topic name to the global variable
    global LISTEN_TO_TOPIC
    LISTEN_TO_TOPIC = topic
    print("Topic name listening to: ", LISTEN_TO_TOPIC)
    # linking the CallBacks
    local_mqttclient.on_connect = on_connect_local
    local_mqttclient.on_publish = on_publish_local
    local_mqttclient.on_disconnect = on_disconnect_local
    local_mqttclient.on_message = on_message
    local_mqttclient.on_subscribe = on_subscribe_local

    local_mqttclient.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_PORT, 60)
    local_mqttclient.loop_forever()

if __name__ == "__main__":
    cmd_options = parse_opt()
    main(**vars(cmd_options))