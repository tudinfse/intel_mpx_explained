#!/usr/bin/env bash

source ${PROJ_ROOT}/install/common.sh

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
