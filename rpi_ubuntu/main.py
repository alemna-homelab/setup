__all__ = ["setup"]

import os

import utils

import rpi_ubuntu.install_ansible
import rpi_ubuntu.install_docker
import rpi_ubuntu.persistent_files
from rpi_ubuntu.constants import (
    ANSIBLE_INVENTORY_FILE,
    ANSIBLE_PLAYBOOK_DIR,
    DEFAULT_ROOT_USER,
    DIR,
)


def setup_using_ansible():
    playbooks_for_setup = [
        f"{ANSIBLE_PLAYBOOK_DIR}/__setup__.yaml",
        f"{ANSIBLE_PLAYBOOK_DIR}/setup_users.yaml",
    ]
    for playbook in playbooks_for_setup:
        os.system(f"ansible-playbook {playbook} -i {ANSIBLE_INVENTORY_FILE}")
        # LOG


def setup(system_user: str = DEFAULT_ROOT_USER, rootless_docker: bool = True):
    if system_user is None or system_user == "":
        system_user = DEFAULT_ROOT_USER

    # ROOT: Setup /usr/local
    # ROOT: Initial setup
    # ROOT: Setup files in home folders
    rpi_ubuntu.persistent_files.setup_usr_local()
    for script in ["initial_setup.sh", "initial_setup_users.sh"]:
        utils.run_shell_script(script_path=(DIR / script))
    rpi_ubuntu.persistent_files.setup_systemuser_home(username=system_user)
    rpi_ubuntu.persistent_files.setup_systemuser_home(username="dockusr")

    # ROOT: Install Ansible
    # ROOT: Run __setup__ playbook to setup hostname, etc.
    # ROOT: Run setup_users playbook to setup users
    rpi_ubuntu.install_ansible.setup()
    setup_using_ansible()

    # DOCKUSR: Install docker rootless
    # DOCKUSR: Setup pihole (docker-compose up!)
    rpi_ubuntu.install_docker.setup(with_rootless_user="dockusr")


if __name__ == "__main__":
    setup()
