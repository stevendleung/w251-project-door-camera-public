#!/bin/bash

# Cleanup stragglers
docker rmi $(docker images -f "dangling=true" -q)
docker system prune -a

# Change permissions
chmod 0755 ./build_notif_container.sh

# Docker build (Alpine OS)
docker build --no-cache -t jramirez0508/notification -f Dockerfile.notification .

# Docker push to DockerHub
# docker push jramirez0508/notification