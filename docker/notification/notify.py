import numpy as np
import paho.mqtt.client as mqtt
import sys
from datetime import datetime, timedelta
import os
import secrets
import json

import argparse
import time
from apscheduler.schedulers.background import BackgroundScheduler
from twilio.rest import Client

# Mosquitto 
LOCAL_MQTT_HOST= "mosquitto-service"
# LOCAL_MQTT_HOST= "localhost"
# LOCAL_MQTT_PORT= 31126
LOCAL_MQTT_PORT= 1883
LOCAL_NOTIF_TOPIC= "model_output_topic"

local_mqttclient = mqtt.Client()

# Registered Users
registeredUsers = None
# All cached messages
allMessages = [[],[]]

# Define Local Sender MQTT callbacks
def on_connect_local(client, userdata, flags, rc):
    if rc == 0:
        print("Successfully connected to local broker with rc: " + str(rc))
        local_mqttclient.subscribe(LOCAL_NOTIF_TOPIC)
    else: 
        print("Error - Couldn't connect to local broker, rc code: " + str(rc))

def on_disconnect_local(client, userdata, flags, rc): 
    print("Disconnected from local broker, result code" + str(rc))
    local_mqttclient.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_PORT, 60)

def on_publish_local(client, userdata, msg_id):
    print("Message successfully published: {}".format(msg_id))

def on_subscribe_local(client, userdata, msg_id, rc):
    if rc == 0:
        print("Successfully subscribed to local topic with rc: " + str(rc))
    else:
        print("Failed to subscribe to local topic with rc: " + str(rc))

def loadRegisteredUsers(users):
    # load registered users from the store
    global registeredUsers

    # read file
    file_handler = open(users, "r")
    data = file_handler.read()

    # load json
    items = json.loads(data)

    # store data
    registeredUsers = items

    return

def buildMessage(ndx, mesg):
    text_msg = ''    
    # create text based on the report type
    if len(mesg) > 0:
        class0, class1 = 0, 0
        for items in mesg:
            if (items['classification'] == "0.0" or items['classification'] == "0" ):
                class0 += 1
            else:
                class1 += 1
        if class0 > class1:
            if ndx == 0:
                text_msg = "Known Person at door: " + mesg[0]['person_name']
            else:
                text_msg = "Delivery person at door"
        else:
            if ndx == 0:
                text_msg = "Unknown Person at door"
            else:
                text_msg = "Non-Delivery person at door"
    return text_msg

def sendNotification():
    global registeredUsers
    global allMessages
    try:

        # get registered user details
        print("All Messages: ", allMessages[1])
        account_sid = registeredUsers['account_sid']
        auth_token = registeredUsers['token']
        phone_number = registeredUsers['phone_number']
        for (ndx,item) in enumerate(allMessages):
#            client = Client(account_sid, auth_token)
            txt_msg = buildMessage(ndx, item)
#            message = client.messages \
#                        .create(
#                            body=txt_msg,
#                            from_='+15017122661',
#                            to=phone_number
#                        )
            #print("message: ", str(message.payload))
            print("message: ", txt_msg)
        # Clear Cache
        allMessages = [[],[]]
    except:
        print("Unexpected error:", sys.exc_info()[0])

def processMessage(new_msg):
    message = new_msg.split(';')
    ndx = int(message[1]) # type of report is 0 for FD & 1 for DND

    allMessages[ndx].append({
        'classification' : message[2],
        'person_name' : message[3],
        'file_name' : message[4],
    })
    
    return

def runScheduler():
    # Start the scheduler
    sched = BackgroundScheduler()
    sched.add_job(sendNotification, 'interval', seconds=5)
    sched.start()

def on_message(client, userdata, msg):
    # parse the input message
    new_msg = msg.payload.decode("utf-8")
    print("Message Received: ", new_msg)

    flag = processMessage(new_msg)

    return

def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--topic', type=str, default='model_output_topic', help='use model_output_topic')
    parser.add_argument('--users', type=str, default='/data/RegisteredUsers.json', help='get the registered users data')
    opt = parser.parse_args()
    return opt

def main(topic='model_output_topic',  # default topic
         users='/data/RegisteredUsers.json'
        ):
    # Assign topic name to the global variable
    global LOCAL_NOTIF_TOPIC
    LOCAL_NOTIF_TOPIC = topic
    print("Topic name listening to: ", LOCAL_NOTIF_TOPIC)

    # load the registered users
    loadRegisteredUsers(users)

    # linking the CallBacks
    local_mqttclient.on_connect = on_connect_local
    local_mqttclient.on_publish = on_publish_local
    local_mqttclient.on_disconnect = on_disconnect_local
    local_mqttclient.on_message = on_message
    local_mqttclient.on_subscribe = on_subscribe_local

    local_mqttclient.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_PORT, 60)
    
    # Run the scheduler
    runScheduler()

    local_mqttclient.loop_forever()

if __name__ == "__main__":
    cmd_options = parse_opt()
    main(**vars(cmd_options))
