import io
from syslog import syslog, LOG_NOTICE, LOG_INFO, LOG_CRIT
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


SUPPORTED_OSs = ["Ubuntu"]


def msg(text: str, priority: int = LOG_INFO):
    # Priority levels are (high to low):
    #   LOG_EMERG, LOG_ALERT, LOG_CRIT, LOG_ERR, LOG_WARNING,
    #   LOG_NOTICE, LOG_INFO, LOG_DEBUG
    _msg = f"SETUP @ {Path(__file__).resolve()}: {text}"
    print(_msg)
    syslog(priority, _msg)


def is_raspberry_pi():
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
    msg(f"Adding {lib_dir} to PATH...")
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
        msg(f"Removing {lib_dir} from PATH...")
        sys_path.remove(lib_dir)
        os.environ["PATH"] = os.pathsep.join(sys_path)
        os.system("export PATH")
    else:
        msg(f"Verified {lib_dir} not in PATH...")


def setup_rpi_ubuntu():
    """Calls the scripts defined in the `raspberry_pi_ubuntu` directory."""
    import raspberry_pi_ubuntu

    raspberry_pi_ubuntu.run_setup()


def main():
    msg("Starting script.", priority=LOG_NOTICE)
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
                + "Running relevant setup scripts now."
            )
            setup_rpi_ubuntu()
        else:
            raise NotImplementedError

    except NotImplementedError:
        msg(
            "ERROR: The operating system or platform is not recognized.",
            priority=LOG_CRIT,
        )

    finally:
        remove_lib(lib_dir)
        os.chdir(starting_dir)


if __name__ == "__main__":
    main()
