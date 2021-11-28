"""TEST"""

import os
from pathlib import Path
from syslog import LOG_INFO, syslog


def msg(text: str, priority: int = LOG_INFO, file=__file__):
    # Priority levels are (high to low):
    #   LOG_EMERG, LOG_ALERT, LOG_CRIT, LOG_ERR, LOG_WARNING,
    #   LOG_NOTICE, LOG_INFO, LOG_DEBUG
    _msg = f"SETUP @ {Path(file).resolve()}: {text}"
    print(_msg)
    syslog(priority, _msg)


def run_shell_script(script_path) -> int:
    if isinstance(script_path, Path) is False:
        script_path = Path(script_path)

    with script_path.open("r") as f:
        # see if first line is a hashbang, and respect it, or else
        # run using /bin/sh
        line1 = f.readline()
        if line1[0:2] == "#!":
            shell_path = line1[2:].strip()
        else:
            shell_path = "/bin/bash"

    if Path(shell_path).is_file() is False:
        shell_path = "/bin/sh"

    exit_code = os.system(f"sudo {shell_path} {script_path}")
    return exit_code
