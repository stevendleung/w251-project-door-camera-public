"""Run inference with a YOLOv5 model on images

Usage:
    $ python3 path/to/detect_delivery.py --source path/to/img.jpg --weights model.pt

Author:
    Javed Roshan
    Modified the code from yolov5's detect.py
"""

import argparse
import sys
import time
from pathlib import Path

import cv2
import torch
import torch.backends.cudnn as cudnn

# import for MQTT connectivity
import paho.mqtt.client as mqtt
import numpy as np

import numpy as np

FILE = Path(__file__).absolute()
sys.path.append(FILE.parents[0].as_posix())  # add yolov5/ to path

from models.experimental import attempt_load
from utils.augmentations import letterbox
from utils.general import check_img_size, colorstr, non_max_suppression, scale_coords, xyxy2xywh, set_logging
from utils.torch_utils import select_device, time_synchronized

model = None        # trained model to be loaded once
cmd_options = None  # command options to be used in the MQTT message loop

# config for the MQTT messages
LOCAL_MQTT_HOST="mosquitto-service"
# LOCAL_MQTT_HOST="localhost"
LOCAL_MQTT_PORT=1883
LOCAL_MQTT_TOPIC_IN="image_topic"
LOCAL_MQTT_TOPIC_OUT="model_output_topic"
connected_flag = False

# setup MQTT client object
local_mqttclient = mqtt.Client()

# callback functions for MQTT setup
def on_connect_local(client, userdata, flags, rc): 
    global connected_flag
    if rc == 0:
        print("Successfully connected to local broker with rc: " + str(rc))
        client.subscribe(LOCAL_MQTT_TOPIC_IN)
    else: 
        print("Error - Couldn't connect to local broker, rc code: " + str(rc))

def on_disconnect_local(client, userdata, flags, rc): 
    print("Disconnected from local broker, result code" + str(rc))
    local_mqttclient.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_PORT, 60)

def on_publish_local(client, userdata, msg_id):
    print("Message successfully published: {}".format(msg_id))

def modelLoad(
        weights='yolov5s.pt',  # model.pt path(s)
        source='data/images',  # not relevant with MQTT
        imgsz=640,  # inference size (pixels)
        half=False,  # use FP16 half-precision inference
        ):

    global model
    # Initialize
    set_logging()
    device = select_device('')
    half &= device.type != 'cpu'  # half precision only supported on CUDA

    # Load model
    model = attempt_load(weights, map_location=device)  # load FP32 model
    stride = int(model.stride.max())  # model stride
    imgsz = check_img_size(imgsz, s=stride)  # check image size
    if half:
        model.half()  # to FP16

@torch.no_grad()
def run(filename, # include path of the file
        weights='yolov5s.pt',  # model.pt path(s)
        source='data/images',  # not relevant with MQTT
        imgsz=640,  # inference size (pixels)
        half=False,  # use FP16 half-precision inference
        ):
    global model
    ret_msg = ''
    device = select_device('')

    # Read image
    path = source
    path = filename
    img0 = cv2.imread(path)  # BGR
    im0s = img0
    assert img0 is not None, 'Image Not Found ' + path

    stride = int(model.stride.max())  # model stride

    # # Padded resize
    img = letterbox(img0, imgsz, stride=stride)[0]

    # Convert
    img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, to 3x416x416
    img = np.ascontiguousarray(img)

    t0 = time.time()
    img = torch.from_numpy(img).to(device)
    img = img.half() if half else img.float()  # uint8 to fp16/32
    img /= 255.0  # 0 - 255 to 0.0 - 1.0
    if img.ndimension() == 3:
        img = img.unsqueeze(0)

    # Inference
    t1 = time_synchronized()
    pred = model(img, augment=False, visualize=False)[0]

    # Apply NMS
    pred = non_max_suppression(pred, 0.25, 0.45, None, False, max_det=1000)
    t2 = time_synchronized()

    # Process detections
    for i, det in enumerate(pred):  # detections per image
        p, s, im0 = path, '', im0s.copy()

        gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
        if len(det):
            # Rescale boxes from img_size to im0 size
            det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()

            # get the predictions to return
            for *xyxy, conf, cls in reversed(det):
                xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn).view(-1).tolist()  # normalized xywh
                line = str(cls.item()) + '; ' + ','.join(map(str,xywh)) + ';'
                ret_msg += str(line)

    return ret_msg

# Publishing message to the Notification Queue as an output from the model
# Message Structure:
#   Video Source Id: 1 (default)
#   Type of Report: 0 (FaceRec); 1 (Del[ivery]Nodel[ivery])
#   Classification: 
#       If Type of Report = 0 (FaceRec)
#           0 (Known Person)
#           1 (Unknown Person)
#       If Type of Report = 1 (DelNodel)
#           0 (Delivery)
#           1 (Non-Delivery)
#   Person Name: string
#   Filename: string
#   Box Coordinates: x, y, w, h 
#   
#   Example: 1; 0; 0; Steven; image_380.jpg; 0.234,0.123,0.346,0.778
#   Example: 1; 1; 0; ; image_480.jpg; 0.234,0.123,0.346,0.778

def on_message(client, userdata, msg):
    # Action to perform upon receiving message from video streamer. Takes image path message and runs delivery/no-delivery model. Output is sent to notification
    global cmd_options
    # parse the input message
    new_msg = msg.payload.decode("utf-8")
    mesg_items = new_msg.split(';')
    vid_source = mesg_items[0]
    type_of_report = 1
    classification = 0
    person_name = ''
    filename = mesg_items[1] + mesg_items[2]
    face_locations = '0,0,0,0'

    mesg = run(filename, **vars(cmd_options))

    # publish the message to the notification queue
    model_output_msg = "{};{};{};{};{};{}".format(vid_source, type_of_report, classification,
                                                person_name, current_msg, face_locations)
    local_mqttclient.publish(LOCAL_RECEIVER_MQTT_TOPIC, model_output_msg)
    return

def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=str, default='data/images', help='file/dir/URL/glob, 0 for webcam')
    parser.add_argument('--weights', nargs='+', type=str, default='yolov5s.pt', help='model.pt path(s)')
    parser.add_argument('--half', action='store_true', help='use FP16 half-precision inference')
    opt = parser.parse_args()
    return opt

def main(cmd_opts):
    global local_mqttclient
    global cmd_options
    cmd_options = cmd_opts
    # Loop listener forever
    modelLoad(**vars(cmd_options))

    # linking the CallBacks
    local_mqttclient.on_connect = on_connect_local
    local_mqttclient.connect(LOCAL_MQTT_HOST, LOCAL_MQTT_PORT, 60)
    local_mqttclient.on_publish = on_publish_local
    local_mqttclient.on_disconnect = on_disconnect_local
    local_mqttclient.on_message = on_message
    local_mqttclient.loop_forever()

if __name__ == "__main__":
    # update cmd_options global variable
    cmd_opts = parse_opt()
    main(cmd_opts)