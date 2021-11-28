# Raspberry Pi Ubuntu

The overall goal of everything in the `rpi_ubuntu` folder is to set up Ubuntu Server 20.04 on a Raspberry Pi. So far, I've only been working with a 32-bit version of Ubuntu Server on a Raspberry Pi 3 B, so your mileage may vary.

## Overview and configuration

These scripts install Ansible, Docker

- Ansible config
- Ansible host

## Directory structure

```ini
rpi_ubuntu/  # This directory
    ├── install_ansible/  # Python module
    |   # All the Python logic is in __init__.py, the rest of the
    |   # files are shell scripts called from __init__.py.
    ├── install_docker/  # Python module
    |   # Same concept as the install_ansible module. It's just
    |   # an __init__.py plus shell scripts.
    |
    └── persistent_files/
    |   # While we recommend setting this repo up in the /tmp
    |   # directory in order to save space, these folders will
    |   # be copied over to persistent locations on the Pi.
    |       ├── home_dockusr/   # --> /home/dockusr
    |       |       └── pihole/.docker-compose.yaml
    |       ├── home_ubuntu/    # --> /home/ubuntu
    |       |       ├── playbooks/
    |       |       ├── .ansible.cfg
    |       |       └── inventory.yaml
    |       └── usr_local/
    |               └── bin/    # --> /usr/local/bin
    |
    ├── __init__.py
    ├── initial_setup.sh
    ├── post_initial_setup.dockerfile
    ├── README.md  # You are here
    └── ubuntu_server.dockerfile
```
