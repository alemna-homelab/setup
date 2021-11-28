import os
from pathlib import Path
import shutil
from glob import glob

from utils import msg

DIR = Path(__file__).parent  # should be ./raspberry_pi_ubuntu from this repo's root


def run_setup():
    FILE = DIR / "initial_setup.sh"
    with FILE.open("r") as f:
        # see if first line is a hashbang, and respect it, or else
        # run using /bin/sh
        line1 = f.readline()
        if line1[0:2] == "#!":
            SHELL = line1[2:].strip()
        else:
            SHELL = "/bin/bash"

    if Path(SHELL).is_file() is False:
        SHELL = "/bin/sh"

    exit_code = os.system(f"sudo {SHELL} {FILE}")
    return exit_code


def ensure_playbooks():
    ansible_home = Path("/home/sysusr")
    ansible_home.mkdir(exist_ok=True)
    msg(f"Moving playbooks into {ansible_home}", file=__file__)
    shutil.copytree(
        src=f"{DIR / 'playbooks'}",
        dst=f"{ansible_home / 'playbooks'}",
        dirs_exist_ok=True,
    )


def ensure_inventory(inventory_file: Path = None):
    system_ansible_inventory = Path("/etc/ansible/hosts")
    if system_ansible_inventory.exists() is True:
        with system_ansible_inventory.open("r") as f:
            line1 = f.readline().strip()
        if line1 == "# This is the default ansible 'hosts' file.":
            # it's default, change it to hosts.default and proceed
            system_ansible_inventory.rename(f"{system_ansible_inventory}.default")
        else:
            # stop immediately, we don't want to overwrite existing data
            msg(
                f"Found existing inventory file at /etc/ansible/hosts, "
                + "no need to replace it",
                file=__file__,
            )
            return
    if inventory_file is None:
        if (DIR / "hosts").exists():
            inventory_file = DIR / "hosts"
        elif (DIR / "hosts.yml").exists():
            inventory_file = DIR / "hosts.yml"
        elif (DIR / "hosts.yaml").exists():
            inventory_file = DIR / "hosts.yaml"
        else:
            # glob("hosts.y*ml") matches both hosts.yml and hosts.yaml
            hostfile_list = glob(f"{DIR}/hosts.y*ml")
            if len(hostfile_list) == 0:
                inventory_file = DIR / "hosts.example.yaml"
            else:
                # inventory file is the first file found
                inventory_file = Path(hostfile_list[0])
    else:
        inventory_file = inventory_file.resolve()
    msg(f"Copying inventory file {inventory_file} to /etc/ansible/hosts", file=__file__)
    shutil.copy(src=str(inventory_file), dst="/etc/ansible/hosts")
