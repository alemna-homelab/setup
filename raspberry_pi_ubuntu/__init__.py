import os
from pathlib import Path


def run_setup():
    DIR = Path(__file__).parent
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
