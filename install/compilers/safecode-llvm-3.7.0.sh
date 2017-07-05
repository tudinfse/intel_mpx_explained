#!/usr/bin/env bash

apt-get install -y subversion
set -e
source ${PROJ_ROOT}/install/common.sh

# check Gold linker
if [ ! -d "${BIN_PATH}/binutils_gold/build" ]; then
    echo "Install normal LLVM first:"
    echo "    ./fex.py install -n llvm-3.8.0"
    exit 1
fi

# ============
# SAFECode
# ============
NAME="safecode"
VERSION="llvm37"
BRANCH="master"

SRC_PATH="${BIN_PATH}/${NAME}/src"
BUILD_PATH="${BIN_PATH}/${NAME}/build"
GOLD_PATH="${BIN_PATH}/binutils_gold/install"

# download
mkdir -p ${BIN_PATH}/${NAME}
download_github_and_link ${NAME} https://github.com/jcranmer/${NAME}/archive/${BRANCH}.zip ${SRC_PATH} ${BRANCH}

# configure
mkdir -p $BUILD_PATH && cd $BUILD_PATH
${SRC_PATH}/configure --enable-optimized --prefix=${GOLD_PATH} --with-binutils-include=${BIN_PATH}/binutils_gold/src/include

# build
MAKE="make -j8"
$MAKE
#$MAKE tools-only
$MAKE install
#
$MAKE -C ./projects/poolalloc
$MAKE -C ./projects/poolalloc install
#
$MAKE -C ./projects/safecode
$MAKE -C ./projects/safecode install


set +e
