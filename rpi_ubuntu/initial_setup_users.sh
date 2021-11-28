#!/bin/bash

source script_msg

# USERS
# While we're set up other users with Ansible later, we're going to 
# create some system users now.

# separate user for non-root Docker
script_msg "CREATING dockusr"
useradd \
    --system \
    --create-home \
    --shell /bin/false \
    dockusr
