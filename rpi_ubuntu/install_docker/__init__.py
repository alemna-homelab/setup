import os

from rpi_ubuntu.constants import DIR


def setup(with_rootless_user=None):
    this_dir = DIR / "install_docker"
    os.system(f"/bin/bash {this_dir / 'install_docker.sh'}")
    if with_rootless_user:
        # TODO: switch to user
        os.system(f"/bin/bash {this_dir / 'install_docker_rootless_reqs.sh'}")
        os.system(f"/bin/bash {this_dir / 'install_docker_rootless.sh'}")
