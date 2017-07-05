FROM ubuntu:16.04

MAINTAINER Oleksii Oleksenko (oleksii.oleksenko@tu-dresden.de)

# Use bash!
RUN rm /bin/sh && \
    ln -s /bin/bash /bin/sh


# == Basic packages ==
RUN apt-get update && \
    apt-get install -y git \
                       texinfo \
                       vim \
                       libxml2-dev \
                       cmake \
                       python3-dev\
                       python3-pip \
                       gcc \
                       build-essential \
                       flex \
                       bison \
                       linux-tools-generic \
                       wget \
                       psmisc \
                       time

RUN pip3 install coloredlogs nose2 py-cpuinfo

# add colors
RUN echo 'export PS1="\[\033[38;5;172m\][${ID}] \t\[$(tput sgr0)\]\[\033[38;5;15m\]:\[$(tput sgr0)\]\[\033[38;5;33m\]\W\[$(tput sgr0)\]\[\033[38;5;15m\] \[$(tput sgr0)\]\[\033[38;5;1m\]>\[$(tput sgr0)\]\[\033[38;5;11m\]>\[$(tput sgr0)\]\[\033[38;5;40m\]>\[$(tput sgr0)\]\[\033[38;5;15m\] \[$(tput sgr0)\]"  && return' > ~/.bashrc

# get correct perf
RUN list=( /usr/lib/linux-tools/*-generic/perf ) && \
    ln -sf ${list[-1]} /usr/bin/perf

# setup the environment
ENV LD_LIBRARY_PATH=/lib:/usr/lib64:/usr/lib/:/usr/local/lib64/:/usr/local/lib/:$LD_LIBRARY_PATH \
    DATA_PATH=/data/ \
    PROJ_ROOT=/root/code/fex/ \
    BIN_PATH=/root/bin/

RUN mkdir -p /root/bin/benchmarks

# sources
COPY ./ ${PROJ_ROOT}
RUN chmod -R 755 ${PROJ_ROOT}/install

# == Interface ==
VOLUME /data
WORKDIR ${PROJ_ROOT}
ENTRYPOINT ["/bin/bash"]
