# Run stand-along docker containers

# Door Cam Publisher
docker run -e DISPLAY --rm --privileged --runtime nvidia --net=host -v $(pwd)/door_cam_images:/door_cam_images door_cam_publisher

# Face Rec
docker run -e DISPLAY=$DISPLAY --rm --privileged -v /tmp:/tmp -ti face_rec5

# Docker build/push commands
# Door Cam Publisher
cd door_cam_publisher && docker build -t stevendleung/door_cam_publisher -f Dockerfile.door_cam_publisher . && docker push stevendleung/door_cam_publisher && cd ..

# Face Rec Model
cd face_rec && docker build -t stevendleung/face_rec -f Dockerfile.face_rec . && docker push stevendleung/face_rec && cd ..

# Delivery Model


# Listener Test WILL BE REMOVED
cd face_rec_listener_test && docker build -t stevendleung/face_rec_listener_test -f Dockerfile.face_rec_listener_test . && docker push stevendleung/face_rec_listener_test && cd ..

# Detector WILL BE REMOVED
docker build -t jramirez0508/detector -f Dockerfile.detector . 
docker push jramirez0508/detector

# Notification
cd notification && docker build -t stevendleung/notify -f Dockerfile.notify . && docker push stevendleung/notify && cd ..

docker run -it -p 1883:1883 -v /home/steven/w251-project-door-camera/docker/mosquitto/mosquitto.conf:/mosquitto/config/mosquitto.conf eclipse-mosquitto