import paho.mqtt.client as mqtt
import numpy as np
import cv2
  

LOCAL_MQTT_HOST="mosquitto-service"
LOCAL_MQTT_PORT=1883
LOCAL_MQTT_TOPIC="test_topic"

def on_connect_local(client, userdata, flags, rc):
        print("connected to local broker with rc: " + str(rc))

local_mqttclient = mqtt.Client()
local_mqttclient.on_connect = on_connect_local
local_mqttclient.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_PORT, 60)

#publish the message
local_mqttclient.publish(LOCAL_MQTT_TOPIC,"Hello MQTT...")

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    print('face')
    for (x,y,w,h) in faces:
    	# Display the resulting frame

	    crop_img = frame[y:y+h, x:x+w]
    
    #Don't display image in container implementation
    #cv2.imshow("cropped", crop_img)
    rc,png = cv2.imencode('.png', crop_img)
    msg = png.tobytes()

    #publish the message
    local_mqttclient.publish(LOCAL_MQTT_TOPIC,msg, qos=1)

    #if cv2.waitKey(1) & 0xFF == ord('q'):
    #    break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
