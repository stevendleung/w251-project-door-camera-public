#!/bin/bash

# Define camera id display
export DISPLAY=:0

# docker stop all containers
docker kill $(docker ps -q)
docker rm $(docker ps --filter status=exited -q)


# kubectl delete deployment/service <app_name>
kubectl delete deployment notification
kubectl delete deployment detector
kubectl delete deployment door-cam-publisher
kubectl delete deployment face-rec
kubectl delete deployment face-rec-listener-test #TEMP
kubectl delete deployment mosquitto-deployment
kubectl delete service mosquitto-service

# Launch edge k3s deployments and services
kubectl apply -f mosquitto/ # deployment, configmap and Service - allows across container comms
kubectl apply -f door_cam_publisher/door_cam_publisher.yaml
kubectl apply -f face_rec/face_rec.yaml
kubectl apply -f face_rec_listener_test/face_rec_listener_test.yaml #TEMP
#kubectl apply -f notification/notification.yaml
# kubectl apply -f face_detector.yaml #TEMP
# kubectl apply -f yolov5.yaml
kubectl get pods 

# kubectl get deployment
# kubectl get services

# build docker container
# push docker container
# run k8s  