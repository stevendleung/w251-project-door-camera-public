#!/bin/bash

# Define camera id display
export DISPLAY=:0

# kubectl delete deployment/service <app_name>
kubectl delete service mosquitto
kubectl delete deployment mosquitto
kubectl delete deployment door-cam-publisher
kubectl delete deployment face-rec
kubectl delete deployment detect-delivery
kubectl delete deployment notify
#kubectl delete deployment test-publisher #for using test images


# Launch edge k3s deployments and services
kubectl apply -f mosquitto/ # deployment, configmap and Service - allows across container comms
kubectl apply -f door_cam_publisher/door_cam_publisher.yaml
kubectl apply -f face_rec/face_rec.yaml
kubectl apply -f detect_delivery/detect_delivery.yaml
kubectl apply -f notification/notify.yaml
#kubectl apply -f test_publisher/test_publisher.yaml #for using test images 

# docker stop and remove all containers
#docker kill $(docker ps -q)
#docker rm $(docker ps --filter status=exited -q)

#SSH into k8s docker container
# kubectl exec --stdin --tty POD_NAME -- /bin/bash