#!/bin/bash

source script_msg
source python_is_python3

# Create symlink from python -> python3
python_is_python3

script_msg "INSTALLING apt-transport-https,  ca-certificates"
apt-get install --assume-yes \
    apt-transport-https \
    ca-certificates
script_msg "RUNNING apt-get update"
apt-get update
script_msg "RUNNING apt-get upgrade --assume-yes"
apt-get upgrade --assume-yes
script_msg "ENSURING various useful packages (git, openssh-server, speedtest-cli)"
apt-get install --assume-yes \
    apt-utils \
    curl \
    git \
    network-manager \
    openssh-server \
    speedtest-cli \
    ufw
script_msg "RUNNING apt-get install software-properties-common --assume-yes"
apt-get install software-properties-common --assume-yes

# DOCKER

script_msg "INSTALLING docker pre-reqs for rootless mode"
sudo apt-get install --assume-yes \
    uidmap \
    dbus-user-session
script_msg "INSTALLING docker"
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
    
dockerd-rootless-setuptool.sh install

script_msg "INSTALLING python 'docker' module (for later ansible use)"
sudo apt-get install --assume-yes \
    python3-pip
sudo python3 -m pip install \
    docker
    docker-compose

# Setting up separate user for non-root Docker
script_msg "RUNNING useradd --system --create-home --shell /bin/false sysusr"
useradd \
    --system \
    --create-home \
    --groups sudo,docker \
    --shell /bin/false \
    ansible

script_msg "SWITCHING USER to sysusr"
su ansible

dockerd-rootless-setuptool.sh install

# ANSIBLE
script_msg "RUNNING apt-add-repository ppa:ansible/ansible --yes"
sudo apt-add-repository ppa:ansible/ansible --yes
script_msg "RUNNING apt-get update"
sudo apt-get update
script_msg "RUNNING apt-get install ansible --assume-yes"
sudo apt-get install ansible ansible-lint --assume-yes
script_msg "INSTALLING required ansible-galaxy collections"
sudo ansible-galaxy collection install community.general community.docker

script_msg "REMOVING ansible user from sudo group"
exit  # from su ansible
deluser ansible sudo

# SETUP VIA ANSIBLE
script_msg "RUNNING ANSIBLE PLAYBOOK: __setup__.yaml"
ansible-playbook playbooks/__setup__.yaml --verbose

script_msg "RUNNING ANSIBLE PLAYBOOK: setup_users.yaml"
ansible-playbook playbooks/setup_users.yaml --verbose

script_msg "RUNNING ANSIBLE PLAYBOOK: setup_docker_pihole.yaml"
ansible-playbook playbooks/setup_docker_pihole.yaml --verbose
