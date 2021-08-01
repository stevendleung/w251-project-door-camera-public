import paho.mqtt.client as mqtt
import sys
from datetime import datetime, timedelta
import os
from twilio.rest import Client

LOCAL_MQTT_HOST= "mosquitto"
LOCAL_MQTT_PORT= 1883
LOCAL_MQTT_TOPIC= "model_output_topic"

local_mqttclient = mqtt.Client()

# Define MQTT callbacks
def on_connect_local(client, userdata, flags, rc):
  print("connected to local broker with rc: " + str(rc))
  client.subscribe(LOCAL_MQTT_TOPIC)

def on_disconnect_local(client, userdata, flags, rc): 
  print("Disconnected from local broker, result code" + str(rc))
  local_mqttclient.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_PORT, 60)

def on_message(client, userdata, msg):
  try:
#    TEST PIPELINE TIMING HERE- logs are delayed but writing txt is not
#    with open("timefile.txt", "w") as file:
#      time = str(datetime.now()) + ' ' + str(msg.payload)
#      file.write(time)
#      file.close()
    
    print("message: ", str(msg.payload))
    #print("message received: ",str(msg.payload.decode("utf-8"))) 
  except:
    print("Unexpected error:", sys.exc_info()[0])
  
# Make connections to edge/local broker
local_mqttclient.on_connect = on_connect_local
local_mqttclient.on_message = on_message
local_mqttclient.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_PORT, 60)


# Loop listener forever
local_mqttclient.loop_forever()
