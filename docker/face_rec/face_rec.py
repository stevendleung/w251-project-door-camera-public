import face_recognition
import cv2
import numpy as np
import paho.mqtt.client as mqtt
import sys
from datetime import datetime, timedelta
import os

###Face Recognition

##Load pictures of known people
# Load a sample picture and learn how to recognize it.
steven_image = face_recognition.load_image_file("facial_rec_images/steven.jpg")
steven_face_encoding = face_recognition.face_encodings(steven_image)[0]

# Load a second sample picture and learn how to recognize it.
sarah_image = face_recognition.load_image_file("facial_rec_images/sarah.jpg")
sarah_face_encoding = face_recognition.face_encodings(sarah_image)[0]

# Create arrays of known face encodings and their names
known_face_encodings = [
    steven_face_encoding,
    sarah_face_encoding
]
known_face_names = [
    "Steven Leung",
    "Sarah Duru Leung"
]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []


def face_rec_process(image_path): 
    '''Takes image path and reads in image. Preprocesses image for face rec. Runs face rec to
return list of names and list of coordinates of face. If no person, returns empty lists, if Unknown person, returns Unknown. If known person/people, returns list of their names.'''

    img = cv2.imread(image_path)
    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    face_names = []
    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"

        # # If a match was found in known_face_encodings, just use the first one.
        # if True in matches:
        #     first_match_index = matches.index(True)
        #     name = known_face_names[first_match_index]

        # Or instead, use the known face with the smallest distance to the new face
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]

        face_names.append(name)
    return (face_names, face_locations)

#Mosquitto 
LOCAL_MQTT_HOST= "mosquitto-service"
LOCAL_MQTT_PORT= 1883
LOCAL_SENDER_MQTT_TOPIC= "image_topic"
LOCAL_RECEIVER_MQTT_TOPIC= "model_output_topic"

local_mqttclient = mqtt.Client()

# Define Local Sender MQTT callbacks
def on_connect_local(client, userdata, flags, rc):
  print("connected to local sender with rc: " + str(rc))
  client.subscribe(LOCAL_SENDER_MQTT_TOPIC)

def on_disconnect_local(client, userdata, flags, rc): 
  print("Disconnected from local broker, result code" + str(rc))
  local_sender_mqttclient.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_PORT, 60)

def on_publish_local(client, userdata, msg_id):
    print("Message successfully published: {}".format(msg_id))

# Run model and transmit on message receipt
def on_message(client, userdata, msg):
  '''Action to perform upon receiving message from broker. Takes image path message and runs face_rec model on that image. Publishes model output to new topic.'''
  
  #Current implementation is to check if current message is different than previous message before
  #running model. This is because the camera is sending a message for every frame (even though we 
  #are only capturing images every 30 frames. This is an issue with MQTT that we may need to work through
  global previous_msg
  current_msg = msg.payload.decode("utf-8")
  print(current_msg)
  if current_msg != previous_msg:
    try:
      face_names_locations = face_rec_process(current_msg)
      
      vid_source = 0
      type_of_report = 'face_rec'
      
      #Classification logic- for now only dealing with case of single person on camera
      if len(face_names_locations[0]) == 0:
        classification = 'None'
        person_name = ''
      elif 'Unknown' in face_names_locations[0]:
        classification = 'Unknown'
        person_name = ''
      else:
        classification = 'Known Person'
        person_name = face_names_locations[0][0]

      face_locations = face_names_locations[1]

      model_output_msg = "{};{};{};{};{};{}".format(vid_source, type_of_report, classification,
                                                 person_name, current_msg, face_locations)
      local_mqttclient.publish(LOCAL_RECEIVER_MQTT_TOPIC,model_output_msg)
    except:
      print("Unexpected error:", sys.exc_info()[0])
  previous_msg = current_msg
  
# Make connections to local broker
local_mqttclient.on_connect = on_connect_local

local_mqttclient.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_PORT, 60)
previous_msg= ''
local_mqttclient.on_message = on_message
local_mqttclient.on_publish = on_publish_local
local_mqttclient.on_disconnect = on_disconnect_local


# Loop listener forever
local_mqttclient.loop_forever()


