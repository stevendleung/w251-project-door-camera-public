import numpy
import cv2
import sys
import time
import paho.mqtt.client as mqtt
import base64

LOCAL_MQTT_HOST="mosquitto-service"
LOCAL_MQTT_PORT=1883
LOCAL_MQTT_TOPIC="test_topic"

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

faceCascade = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')
video_capture = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray,1.3,5)

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        face_snapshot = gray[y:y+h, x:x+w]
        _, png = cv2.imencode('.png', face_snapshot)
        msg = base64.b64encode(png)

        # Publish message
        local_mqttclient.publish(LOCAL_MQTT_TOPIC, msg)
        print('Face captured')

    # Display the resulting frame
    #cv2.imshow('Video', face_snapshot)

    #if cv2.waitKey(1) & 0xFF == ord('q'):
        #break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()

