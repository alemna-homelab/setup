# Setup, and set equivalent to ubuntu-server
FROM ubuntu:20.04 AS ubuntu-server
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && apt-get install --assume-yes ubuntu-server
RUN apt-get install --assume-yes sudo apt-utils
RUN apt-get clean
# If $CHECK_FOR_RPI is present and is anything other than 0, 
# auto_setup.py will check if running on Raspberry Pi.
ENV CHECK_FOR_RPI=0
RUN export CHECK_FOR_RPI

# Setup my stuff
FROM ubuntu-server
ENV DEBIAN_FRONTEND noninteractive
RUN git clone https://github.com/alemna-homelab/setup.git /tmp/setup
# Docker suggests use of reverse DNS notation for labels using a domain
# you own, in order to avoid conflict with labels that may be added by
# other automated tools
LABEL org.alexanderlemna.branch "wip-playbooks"

# Comment out the line below if you want to stay on main branch, or
# replace 'wip-playbooks' with different branch name as needed.
RUN cd /tmp/setup && git checkout wip-playbooks && sudo --preserve-env python3 auto_setup.py

CMD ["/bin/bash"]
