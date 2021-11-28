#!/bin/bash

source script_msg

function python_is_python3 {
    # Create symlink from python -> python3
    source script_msg
    if [[ $(which python | wc -l) -eq 0 ]]; then
        PY=$(which python3)
        DIR=$(dirname $PY)
        ln -s "$PY" "$DIR/python"
        script_msg "Created symlink from $DIR/python to $PY"
    else
        # do nothing
        :  
    fi 
}

python_is_python3

script_msg "RUNNING apt-get update"
apt-get update
script_msg "RUNNING apt-get upgrade --assume-yes"
apt-get upgrade --assume-yes
script_msg "ENSURING various useful packages (git, openssh-server, speedtest-cli)"
apt-get install --assume-yes \
    apt-transport-https \
    apt-utils \
    ca-certificates \
    curl \
    git \
    network-manager \
    openssh-server \
    software-properties-common \
    speedtest-cli \
    ufw
