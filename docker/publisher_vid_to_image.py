import paho.mqtt.client as mqtt
import numpy as np
import cv2
import sys
import time
  

LOCAL_MQTT_HOST="mosquitto-service"
LOCAL_MQTT_PORT=1883
LOCAL_MQTT_TOPIC="image_topic"

connected_flag = False

# Client declaration
local_mqttclient = mqtt.Client()

def on_connect_local(client, userdata, flags, rc): 
    global connected_flag
    if rc == 0:      
        print("Successfully connected to local broker with rc: " + str(rc))
        connected_flag = True
    else: 
        print("Error - Couldn't connect to local broker, rc code: " + str(rc))

def on_disconnect_local(client, userdata, flags, rc): 
    print("Disconnected from local broker, result code" + str(rc))
    local_mqttclient.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_PORT, 60)

def on_publish_local(client, userdata, msg_id):
    print("Message successfully published: {}".format(msg_id))

# MQTT CallBacks
local_mqttclient.on_connect = on_connect_local
local_mqttclient.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_PORT, 60)
local_mqttclient.on_publish = on_publish_local
local_mqttclient.on_disconnect = on_disconnect_local


cap = cv2.VideoCapture(0)

frame_count = 0
image_count = 0

while cap.isOpened():

    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if ret:
    #Don't display image in container implementation
        #cv2.imshow("cropped", frame)
        path = "/data/door_cam_images/frame{}.jpg".format(image_count)
        cv2.imwrite(path, frame)
        frame_count += 120 #at 30fps, advances 1 second
        image_count += 1

        cap.set(1,frame_count)

    	#publish the message
        msg = path
        local_mqttclient.publish(LOCAL_MQTT_TOPIC,msg, qos=1)
        print('Image processed')

    else:
        cap.release()
        break

    if image_count == 100:
        image_count = 0



#    if cv2.waitKey(1) & 0xFF == ord('q'):
#        break


# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
