#!/usr/bin/env bash
set -e

apt-get install -y automake autogen autoconf libtool

source ${COMP_BENCH}/install/common.sh

# below are installation instructions for libmemcached & memaslap client (install on client machine)
#wget https://launchpad.net/libmemcached/1.0/1.0.16/+download/libmemcached-1.0.16.tar.gz
#tar xvf libmemcached-1.0.16.tar.gz
#cd libmemcached-1.0.16
#CFLAGS=-pthread LDFLAGS=-pthread LIBS=-levent ./configure --enable-memaslap
#sed -i "s/#am__append_42 = clients\/memaslap/am__append_42 = clients\/memaslap/g" Makefile
#sed -i "s/#am__EXEEXT_2 = clients\/memaslap/am__EXEEXT_2 = clients\/memaslap/g" Makefile
#make
#sudo make install

SRC_PATH="${BIN_PATH}/memcached/src"
VERSION="1.4.15"

# download
mkdir -p ${BIN_PATH}/memcached
clone_github_and_link memcached-${VERSION} https://github.com/memcached/memcached.git ${SRC_PATH} ${VERSION} ${COMP_BENCH}/install/benchmarks/memcached/memcached.1.4.15.patch
