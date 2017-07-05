#!/usr/bin/env bash

echo "Installing GCC..."

apt-get install -y libgmp3-dev libmpfr-dev libmpfr-doc libmpfr4 libmpfr4-dbg libmpc-dev build-essential libc6-dev-i386 zlib1g-dev libncurses-dev libtool


set -e
source ${PROJ_ROOT}/install/common.sh

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

install_dependency "BinUtils" "${PROJ_ROOT}/install/dependencies/binutils.sh"

set +e

echo "GCC installed"
