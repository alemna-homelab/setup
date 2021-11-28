import io
import os
from pathlib import Path
from syslog import LOG_CRIT, LOG_NOTICE

try:
    # 'lsb_release' is not part of the standard library, it's a
    # convenience package included in some linux distros
    import lsb_release as lsb

    _dict = lsb.get_distro_information()
    LSB_ID = _dict["ID"]  # on Ubuntu, will return "Ubuntu"
except ImportError:
    LSB_ID = None


from utils import msg

SUPPORTED_OSs = ["Ubuntu"]


def is_raspberry_pi():
    # Checks for a environmental variable. If it's present and == 0,
    # this function will skip the rest of the checks and return True.
    # Useful for debugging in a docker container, etc.
    env_var_name = "CHECK_FOR_RPI"
    print()
    print(os.environ)
    print()
    if env_var_name in os.environ and os.environ[env_var_name] == "0":
        return True
    # SOURCE: https://raspberrypi.stackexchange.com/a/118473
    try:
        with io.open("/sys/firmware/devicetree/base/model", "r") as m:
            if "raspberry pi" in m.read().lower():
                return True
    except Exception:
        pass
    return False


def setup_rpi_ubuntu():
    """Calls the scripts defined in the `rpi_ubuntu` directory."""
    import rpi_ubuntu

    rpi_ubuntu.setup(rootless_docker=True)


def main():
    msg("Starting script.", priority=LOG_NOTICE, file=__file__)

    setup_repo = Path("__file__").parent.resolve()
    os.environ["SETUP_REPO"] = str(setup_repo)
    os.system("export SETUP_REPO")  # will be used by ./utils/script_msg

    is_raspi = is_raspberry_pi()

    try:
        if is_raspi is True and LSB_ID in SUPPORTED_OSs:
            msg(
                "Device is Raspberry Pi running Ubuntu. "
                + "Running relevant setup scripts now.",
                file=__file__,
            )
            setup_rpi_ubuntu()
        else:
            raise NotImplementedError

    except NotImplementedError:
        msg(
            "ERROR: The operating system or platform is not recognized.",
            priority=LOG_CRIT,
            file=__file__,
        )


if __name__ == "__main__":
    main()
