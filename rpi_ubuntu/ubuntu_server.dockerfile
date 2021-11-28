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

CMD ["/bin/bash"]
