#!/bin/bash

source script_msg

# Installing Docker
script_msg "INSTALLING docker"
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

script_msg "INSTALLING python 'docker' module (for later ansible use)"
sudo apt-get install --assume-yes \
    python3-pip
sudo python3 -m pip install \
    docker \
    docker-compose
