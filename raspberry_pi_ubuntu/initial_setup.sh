#!/bin/bash

source script_msg
source python_is_python3

# Create symlink from python -> python3
python_is_python3

script_msg "RUNNING apt-get update"
apt-get update
script_msg "RUNNING apt-get -y upgrade"
apt-get -y upgrade
script_msg "RUNNING apt-get -y install software-properties-common"
apt-get -y install software-properties-common
script_msg "RUNNING apt-add-repository -y ppa:ansible/ansible"
apt-add-repository -y ppa:ansible/ansible
script_msg "RUNNING apt-get update"
apt-get update
script_msg "RUNNING apt-get -y install ansible"
apt-get -y install ansible
