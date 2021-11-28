from pathlib import Path

DIR = Path(__file__).parent  # should be ./rpi_ubuntu from this repo's root

DEFAULT_ROOT_USER = "ubuntu"
DEFAULT_ROOT_HOME = Path(f"/home/{DEFAULT_ROOT_USER}")

ANSIBLE_PLAYBOOK_DIR = DEFAULT_ROOT_HOME / "playbooks"
ANSIBLE_INVENTORY_FILE = DEFAULT_ROOT_HOME / "inventory.yaml"
