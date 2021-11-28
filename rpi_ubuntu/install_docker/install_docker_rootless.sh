#!/bin/bash

source script_msg

script_msg "INSTALLING Docker to run in rootless mode"
dockerd-rootless-setuptool.sh install
