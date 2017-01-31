# Dockerfile for LLVM, enhanced by Elzar pass

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
                       python-dev \
                       python-pip \
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

RUN pip install argcomplete coloredlogs nose2 && \
    pip3 install argcomplete coloredlogs nose2 && \
    activate-global-python-argcomplete --dest=/etc/bash_completion.d/

# add colors
RUN echo 'export PS1="\[\033[38;5;172m\][${ID}] \t\[$(tput sgr0)\]\[\033[38;5;15m\]:\[$(tput sgr0)\]\[\033[38;5;33m\]\W\[$(tput sgr0)\]\[\033[38;5;15m\] \[$(tput sgr0)\]\[\033[38;5;1m\]>\[$(tput sgr0)\]\[\033[38;5;11m\]>\[$(tput sgr0)\]\[\033[38;5;40m\]>\[$(tput sgr0)\]\[\033[38;5;15m\] \[$(tput sgr0)\]"  && return' > ~/.bashrc

# get correct perf
RUN list=( /usr/lib/linux-tools/*-generic/perf ) && \
    ln -sf ${list[-1]} /usr/bin/perf

# setup the environment
ENV LD_LIBRARY_PATH=/lib:/usr/lib64:/usr/lib/:/usr/local/lib64/:/usr/local/lib/:$LD_LIBRARY_PATH \
    DATA_PATH=/data/ \
    COMP_BENCH=/root/code/compiler-bench/ \
    BIN_PATH=/root/bin/

RUN mkdir -p /root/bin/benchmarks

# sources
COPY ./ ${COMP_BENCH}
RUN chmod -R 755 ${COMP_BENCH}/install

# ssh
RUN mkdir -p /root/.ssh/ && \
    cp ${COMP_BENCH}/install/ssh/id_rsa /root/.ssh/ && \
    chmod 700 /root/.ssh/id_rsa && \
    ssh-keygen -y -f /root/.ssh/id_rsa > /root/.ssh/id_rsa.pub

# == Interface ==
VOLUME /data
WORKDIR ${COMP_BENCH}
ENTRYPOINT ["/bin/bash"]
