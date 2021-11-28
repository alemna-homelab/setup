#!/bin/bash

source script_msg

# Installing Ansible
script_msg "RUNNING apt-add-repository ppa:ansible/ansible --yes"
sudo apt-add-repository ppa:ansible/ansible --yes
script_msg "RUNNING apt-get update"
sudo apt-get update
script_msg "RUNNING apt-get install ansible --assume-yes"
sudo apt-get install ansible ansible-lint --assume-yes
script_msg "INSTALLING required ansible-galaxy collections"
sudo ansible-galaxy collection install \
    community.general \
    community.docker
