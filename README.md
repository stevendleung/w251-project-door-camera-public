# Knock-knock!
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

We present a dual model deep learning door camera system that is able to recognize known individuals through facial recognition and identify whether an individual is a delivery (USPS, UPS, Amazon) or non-delivery personnel. Two pre-trained models are used as the engines for these recognition tasks- [dlib's face recognition](https://face-recognition.readthedocs.io/en/latest/readme.html) model and [YOLOv5s](https://zenodo.org/record/4679653#.YQlL01NKhqsDlib) for delivery personnel recognition. We leverage the dlib model's one-shot ability out of the box to recognize known individuals from a single reference image while Yolov5 is fine-tuned on our dataset to discriminate between delivery and non-delivery individuals. We used Amazon Web Services (AWS) elastic cloud compute (EC2) to perform this fine-tuning. On the inference side, we use the Nvidia Jetson Xavier NX connected to a standard webcam to take in live streaming video, process video frames through both models, and provide an appropriate notification to a user. This process is consolidated into an easily maintainable kubernetes-docker framework that users can spin up with few pre-requisites.

## Overall Architecture:
![data-pipeline](https://github.com/stevendleung/w251-project-door-camera/blob/main/images/data_pipeline.png)


## Dataset:


## Image Captioning Models:
![knock-knock](https://github.com/stevendleung/w251-project-door-camera/blob/main/images/segmentation.png)

## Evaluation Results:
![knock-knock](https://github.com/stevendleung/w251-project-door-camera/blob/main/images/performance.png)

## Edge Inference:
![knock-knock](https://github.com/stevendleung/w251-project-door-camera/blob/main/images/edge_inference.png)

#### Demo
![knock-knock demo](https://github.com/stevendleung/w251-project-door-camera/blob/main/demo/knock_knock_demo.gif)

## Conclusion:


## Acknowledgements:




# w251-project-door-camera
Final project for W251- Steven Leung, Juan Ramirez, Javed Roshan

# Files and Directories (prelim)

- <ins>**Folder:**</ins> **docker**
