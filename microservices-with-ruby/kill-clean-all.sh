#!/bin/bash

# kill running docker containers
docker container kill $(docker ps -q)
# prune all dead containers
echo y | docker container prune
