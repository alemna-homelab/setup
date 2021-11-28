"""Application code for copying persistent_files contents over to their 
persistent locations on the Raspberry Pi.
"""

__all__ = ["setup_systemuser_home", "setup_usr_local"]

import shutil
from pathlib import Path

import rpi_ubuntu.persistent_files.usr_local


def setup_systemuser_home(username: str):
    """If the file containing this function exists in the same directory as a
    folder named `home_username`, this function copies that directory's contents
    over to `/home/username`.
    """
    this_dir = Path(__file__).parent.resolve()  # reporoot/../persistent_files/
    this_home_dir = this_dir / f"home_{username}"

    home_dir = Path(f"/home/{username}")
    if home_dir.exists() is False:
        raise FileNotFoundError
    elif home_dir.is_dir() is False:
        raise NotADirectoryError

    # str() because copytree needs the Paths as strings
    shutil.copytree(src=str(this_home_dir), dst=str(home_dir), dirs_exist_ok=True)


def setup_usr_local():
    rpi_ubuntu.persistent_files.usr_local.setup()
