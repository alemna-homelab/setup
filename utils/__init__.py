from syslog import syslog, LOG_INFO
from pathlib import Path


def msg(text: str, priority: int = LOG_INFO, file=__file__):
    # Priority levels are (high to low):
    #   LOG_EMERG, LOG_ALERT, LOG_CRIT, LOG_ERR, LOG_WARNING,
    #   LOG_NOTICE, LOG_INFO, LOG_DEBUG
    _msg = f"SETUP @ {Path(file).resolve()}: {text}"
    print(_msg)
    syslog(priority, _msg)
