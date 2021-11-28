"""The 'usr_local' module handles files which are destined for the
`/usr/local` directory on the Raspberry Pi.
"""

import shutil
from pathlib import Path

# The /usr/local directory is for programs and data installed by the
# system administrator. It is safe from being overridden by system
# software updates.
DIR = Path("/usr/local/")

# The /usr/local directory generally contains the folders:
#   bin     --> Traditionally contained the locally-installed programs
#               themselves (the compiled binaries). Now contains locally-
#               installed programs expected to be called by the user,
#               regardless of if they're 'binaries' or not.
#   etc     --> Configuration files for the programs in /usr/local/bin.
#   share   --> THIS IS WHERE ANSIBLE MODULES & PLUGINS GO
BIN_DIR = DIR / "bin"
ETC_DIR = DIR / "etc"
SHARE_DIR = DIR / "share"


def setup():
    """If the file containing this function exists in the same directory as
    folders named `bin`, `etc`, and `share`, this function copies those files
    over to `/usr/local/bin`, `/usr/local/etc/`, and `/usr/local/share`
    respectively.
    """
    this_dir = Path(__file__).parent.resolve()  # reporoot/../usr_local/
    this_bin = this_dir / "bin"
    this_etc = this_dir / "etc"
    this_share = this_dir / "share"

    # str() because copytree needs the Paths as strings
    if this_bin.exists():
        shutil.copytree(src=str(this_bin), dst=str(BIN_DIR), dirs_exist_ok=True)
    if this_etc.exists():
        shutil.copytree(src=str(this_etc), dst=str(ETC_DIR), dirs_exist_ok=True)
    if this_share.exists():
        shutil.copytree(src=str(this_share), dst=str(SHARE_DIR), dirs_exist_ok=True)
