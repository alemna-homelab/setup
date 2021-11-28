#!/bin/bash

source script_msg

script_msg "INSTALLING docker pre-reqs for rootless mode"
sudo apt-get install --assume-yes \
    uidmap \
    dbus-user-session
