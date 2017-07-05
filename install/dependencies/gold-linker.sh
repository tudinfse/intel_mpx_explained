#!/usr/bin/env bash

echo "Installing Gold Linker..."

NAME="binutils_gold"

SRC_PATH="${BIN_PATH}/${NAME}/src"
BUILD_PATH="${BIN_PATH}/${NAME}/build"
INSTALL_PATH="${BIN_PATH}/${NAME}/install"

# download
mkdir -p ${BIN_PATH}/${NAME}
cd /data/

set +e
git clone git://sourceware.org/git/binutils-gdb.git
set -e

ln -s /data/binutils-gdb ${SRC_PATH}

cd -

# configure
mkdir -p ${BUILD_PATH}
cd ${BUILD_PATH}
${SRC_PATH}/configure --enable-gold --enable-plugins --disable-werror --prefix=${INSTALL_PATH}

# build
make
make install

# replace the linker
rm $INSTALL_PATH/bin/ld
ln $INSTALL_PATH/bin/ld.gold $INSTALL_PATH/bin/ld

cd -

echo "Linker installed"
