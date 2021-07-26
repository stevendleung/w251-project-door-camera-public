#!/bin/bash

# Define camera id display
export DISPLAY=:0

# docker stop all containers
docker kill $(docker ps -q)

# kubectl delete deployment/service <app_name>
kubectl delete deployment notification
kubectl delete deployment detector
kubectl delete deployment mosquitto-deployment
kubectl delete service mosquitto-service

# build 
docker build --no-cache -t jramirez0508/notification -f Dockerfile.notification .
docker push jramirez0508/notification

docker build -t jramirez0508/detector -f Dockerfile.detector . 
docker push jramirez0508/detector

# Launch edge k3s deployments and services
kubectl apply -f mosquitto.yaml
kubectl apply -f mosquittoService.yaml # Service - allows across container comms
kubectl apply -f detector.yaml
kubectl apply -f notification.yaml
# kubectl apply -f face_detector.yaml
# kubectl apply -f yolov5.yaml
kubectl get pods 

# kubectl get deployment
# kubectl get services

# build docker container
# push docker container
# run k8s  