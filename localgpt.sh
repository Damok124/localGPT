#!/bin/bash

IMAGE_NAME="localgpt"
CONTAINER_NAME="localgpt_container"
PORT=8000

case "$1" in
  build)
    echo "Building the Docker image..."
    docker build -t $IMAGE_NAME .
    ;;
  start)
    echo "Starting the Docker container..."
    docker run -d -p $PORT:$PORT --name $CONTAINER_NAME $IMAGE_NAME
    ;;
  stop)
    echo "Stopping and removing the Docker container..."
    docker stop $CONTAINER_NAME
    docker rm $CONTAINER_NAME
    ;;
  remove-images)
    echo "Removing all Docker images..."
    docker rmi $(docker images -q)
    ;;
  clean)
    echo "Stopping all containers and removing all images..."
    docker stop $(docker ps -aq)
    docker rm $(docker ps -aq)
    docker rmi $(docker images -q)
    ;;
  logs)
    echo "Displaying logs for the container..."
    docker logs $CONTAINER_NAME
    ;;
  *)
    echo "Usage: $0 {build|start|stop|remove-images|clean|logs}"
    exit 1
    ;;
esac
