# Knock-Knock!
### Steven Leung, Juan Ramirez and Javed Roshan
 
A deep learning powered door camera.

[Technical Paper]()        
    
[Presentation]()



## Goal:
* Knock-knock is a novel door camera that recognizes common personnel at the door and notifies a user, implementing these capablities:
   - Facial Recognition to identify known individuals
   - Full body recognition to identify delivery vs non-delivery personnel



## Abstract:
<p align="center"> 
  <img src="https://github.com/stevendleung/w251-project-door-camera/blob/main/images/knock-knock.png" alt="knock-knock" width="700">
</p>

We present a dual model deep learning door camera system that is able to recognize known individuals through facial recognition and identify whether an individual is a delivery (USPS, UPS, Amazon) or non-delivery personnel. Two pre-trained models are used as the engines for these recognition tasks- [dlib's face recognition](https://face-recognition.readthedocs.io/en/latest/readme.html) model and [YOLOv5s](https://zenodo.org/record/4679653#.YQlL01NKhqsDlib) for delivery-non delivery recognition. We leverage the dlib model's one-shot ability out of the box to recognize known individuals from a single reference image while Yolov5 is fine-tuned on our dataset to discriminate between delivery and non-delivery individuals. We used Amazon Web Services (AWS) elastic cloud compute (EC2) to perform this fine-tuning. On the inference side, we use the Nvidia Jetson Xavier NX connected to a standard webcam to take in live streaming video, process video frames through both models, and provide an appropriate notification to a user. This process is consolidated into an easily maintainable kubernetes-docker framework that users can spin up with few pre-requisites.

## Training to Inference- Data Pipeline:
<p align="center"> 
  <img src="https://github.com/stevendleung/w251-project-door-camera/blob/main/images/data_pipeline.png" alt="data-pipeline" width="700">
</p>
The recognition engine for knock-knock is made up of two components- Personnel Recognition and Facial Recognition.
<br/>
<br/>
<h3>Delivery Non-Delivery (DND) Recognition</h3>
<b>Image Collection and Annotation</b><br>
We leveraged youtube videos licensed under the creative commons license for training images. We identified these videos using two sets of search queries- the first set related to delivery personnel, for example "Door Camera Delivery", "Ring Delivery", etc. and the second related to non-delivery personnel. By doing some further manual review and clean-up of the videos, we verified that individuals appearing in the first set of videos could be labelled as delivery personnel while individuals in the second set could be labelled non-delivery. 
<br/>
<br/>
  <img align="left" src="https://github.com/stevendleung/w251-project-door-camera/blob/main/images/segmentation.png" alt="image captioning" width="300"> 
Frames were extracted at a 1 frame per second (fps) rate from each video. These frames served as our training, validation and test data. We used [deeplab segmentation](https://arxiv.org/pdf/1606.00915.pdf) to identify the pixel cooridinates of personnel in each images. These coordinates were converted to the correct format for Yolov5 to accept in the model. Through this method of annnotation, we were able to annotate ~10k images in a semi-automated fashion.
<br/>
<br/>
<b>Yolov5</b><br>
Yolo (You Only Look Once) v5 is a state-of-the-art convolutional neural network (CNN) based object detection model trained on the Imagenet dataset. It has 24 convolutional layers with 2 fully connected layers. V5 is the first version written in Pytorch framework, allowing for more general usability. We fine-tuned YOLOv5s on our curateed dataset. See the subsequent section for training details.
<br/>
<br/>
<h3> Facial recognition </h3>
Dlib's face-recognition python api provides one-shot capabilities for highly accurate face-recognition, performaing at 99.38% accuracy on the [Labeled Faces in the Wild](http://vis-www.cs.umass.edu/lfw/) dataset. The library provides the option to run a Histogram Oriented Gradient (HOG) + Support Vector Machine (SVM) based model or a slightly more performant and resource intensive Convolutional Neural Network (CNN) based model. After testing both options and not finding a significant difference in performance for our use case, we opted for the less resource intensive HOG + SVM option in Knock-Knock.

## Evaluation Results:
<p align="center"> 
  <img src="https://github.com/stevendleung/w251-project-door-camera/blob/main/images/performance.png" alt="performance" width="700">
</p>
We trained the model twice for 250 epochs each, first on a limited dataset and finally on our full dataset. The mAP@0.5 was 0.582 on our first run and 0.607 on our second. Each training run took around 22 hours.

## Edge Inference:
<p align="center"> 
  <img src="https://github.com/stevendleung/w251-project-door-camera/blob/main/images/edge_inference.png" alt="edge" width="700">
</p>
Inference is done on the Nvidia Jetson Xavier NX. The entire process is designed to run within docker containers in a kubernetes cluster. The architecture accomodates for the dual model system. First, the live video stream is processed into frames stored locally. We use [Eclipse Mosquitto](https://mosquitto.org/) message broker to publish messages to "Image Topic" in the format shown above, with the key information being the file path of the latest stored image. 
<br/>
<br/>
The facial recognition and DND models both subscribe to the "Image Topic". Upon message receipt, the models concurrently run inference on the image identified in the message. If the models recognize a person in the image, the output is published to the "Model Output" topic in the format show. If a person is not recognized, not message is published.
<br/>
<br/>
The notification container is subscribed to the "Model Output" topic. Upon receipt of a message the notification adds the classification in the message to the cache. The cache is read every 20 seconds with the majority classifications received being output. We use [Twilio](https://www.twilio.com/) services to send SMS notifications to the registered user.

<h2>Demo</h2>
<p align="center"> 
  <img src="https://github.com/stevendleung/w251-project-door-camera/blob/main/demo/knock_knock_demo.gif" alt="demo"/>
</p>
<br/>
<h2> To Run:</h2>
Tested on Nvidia Jetson Xavier NX.<br/><br/>
Prerequisites:

 - K8s installed
 - Webcam available
 - For facial recognition, add a frontal image of your face to docker/face_rec/facial_images
 
```
xhost +
export DISPLAY=:0
 
git clone https://github.com/stevendleung/w251-project-door-camera.git
 
#make directory to store video frames
sudo mkdir -p /data/door_cam_images/images

cd w251-project-door-camera/docker
 
sh launch_k8s.sh 
```

Notification system is commented out by default in docker/notification/notify.py. To use this component of Knock-Knock, please register an account at (twilio)[https://www.twilio.com/], fill in details in sample/RegisteredUsers.json, copy RegisteredUsers.json to /data on jetson, and uncomment lines 109-123 and 177 i notify.py/
 

