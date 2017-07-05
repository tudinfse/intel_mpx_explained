#!/usr/bin/env bash

source ${PROJ_ROOT}/install/common.sh
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
