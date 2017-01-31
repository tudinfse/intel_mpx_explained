#!/usr/bin/env bash

apt-get install -y libgmp3-dev libmpfr-dev libmpfr-doc libmpfr4 libmpfr4-dbg libmpc-dev build-essential libc6-dev-i386 zlib1g-dev libncurses-dev


set -e
source ${COMP_BENCH}/install/common.sh

# ============
# gcc
# ============
SRC_PATH="${BIN_PATH}/gcc/src"
BUILD_PATH="${BIN_PATH}/gcc/build"
INSTALL_PATH="/usr/"
VERSION="6.1.0"

# download
mkdir -p ${BIN_PATH}/gcc
download_and_link gcc-${VERSION} ftp://ftp.fu-berlin.de/unix/languages/gcc/releases/gcc-${VERSION}/gcc-${VERSION}.tar.gz ${SRC_PATH}

# isl
cd /data/
wget ftp://gcc.gnu.org/pub/gcc/infrastructure/isl-0.15.tar.bz2
tar xf isl-0.15.tar.bz2
mv isl-0.15 ${SRC_PATH}/isl/
cd -

# configure
mkdir -p ${BUILD_PATH}
cd ${BUILD_PATH}
${SRC_PATH}/configure --enable-languages=c,c++ --enable-libmpx --enable-multilib --prefix=${INSTALL_PATH} --with-system-zlib

# install
make -j8
make install

cd -

# ============
# binutils
# ============
SRC_PATH="${BIN_PATH}/binutils/src"
BUILD_PATH="${BIN_PATH}/binutils/build"
VERSION="2.26.1"

mkdir -p ${BIN_PATH}/binutils
download_and_link binutils-${VERSION} http://ftp.gnu.org/gnu/binutils/binutils-${VERSION}.tar.gz ${SRC_PATH}

# configure
mkdir -p ${BUILD_PATH}
cd ${BUILD_PATH}
CXXFLAGS="-Wno-unused-function -O2" ${SRC_PATH}/configure --enable-gold=yes --enable-ld=yes

# install
make -j8
make install

# ============
# gdb
# ============
SRC_PATH="${BIN_PATH}/gdb/src"
BUILD_PATH="${BIN_PATH}/gdb/build"
VERSION="7.11"

mkdir -p ${BIN_PATH}/gdb
download_and_link gdb-${VERSION} http://ftp.gnu.org/gnu/gdb/gdb-${VERSION}.tar.gz ${SRC_PATH}

# configure
mkdir -p ${BUILD_PATH}
cd ${BUILD_PATH}
${SRC_PATH}/configure --enable-tui --enable-gold --enable-lto

# install
make -j8
make install


cd -
set +e
