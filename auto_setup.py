import io
from syslog import LOG_NOTICE, LOG_CRIT
from pathlib import Path
import os

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


def ensure_lib(lib_dir: str):
    # (1) Make sure ./lib is in the path
    msg(f"Adding {lib_dir} to PATH...", file=__file__)
    sys_path = os.environ["PATH"].split(os.pathsep)
    if lib_dir not in sys_path:
        os.environ["PATH"] = lib_dir + os.pathsep + os.environ["PATH"]
        os.system("export PATH")

    # (2) Make sure all the shell scripts in ./lib are executable
    os.chdir(lib_dir)
    for item in os.listdir(lib_dir):
        # os.listdir() returns only files
        if Path(item).suffix != ".py":
            os.chmod(item, mode=0o555)


def remove_lib(lib_dir: str):
    sys_path = os.environ["PATH"].split(os.pathsep)
    if lib_dir in sys_path:
        # reconstruct $PATH without lib_dir
        msg(f"Removing {lib_dir} from PATH...", file=__file__)
        sys_path.remove(lib_dir)
        os.environ["PATH"] = os.pathsep.join(sys_path)
        os.system("export PATH")
    else:
        msg(f"Verified {lib_dir} not in PATH...", file=__file__)


def setup_rpi_ubuntu():
    """Calls the scripts defined in the `raspberry_pi_ubuntu` directory."""
    import raspberry_pi_ubuntu as rpu

    rpu.run_setup()
    rpu.ensure_playbooks()
    rpu.ensure_inventory()


def main():
    msg("Starting script.", priority=LOG_NOTICE, file=__file__)
    starting_dir = os.getcwd()

    setup_repo = Path("__file__").parent.resolve()
    os.environ["SETUP_REPO"] = str(setup_repo)
    os.system("export SETUP_REPO")  # will be used by ./utils/script_msg

    lib_dir = str(setup_repo / "utils")
    ensure_lib(lib_dir)
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

    finally:
        remove_lib(lib_dir)
        os.chdir(starting_dir)


if __name__ == "__main__":
    main()
