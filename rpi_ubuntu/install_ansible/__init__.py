"""Installs Ansible."""

import os

from rpi_ubuntu.constants import DIR


def setup():
    this_dir = DIR / "install_docker"
    os.system(f"/bin/bash {this_dir / 'install_ansible.sh'}")
