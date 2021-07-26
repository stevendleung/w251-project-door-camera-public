#!/bin/bash

# Define camera id display
export DISPLAY=:0

# docker stop all containers
docker kill $(docker ps -q)

# Launch edge k3s deployments and services
kubectl apply -f mosquitto.yaml
kubectl apply -f notification.yaml
# kubectl apply -f face_detector.yaml
# kubectl apply -f yolov5.yaml

# kubectl get deployment
# kubectl get services