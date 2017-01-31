#!/usr/bin/env bash

#apt-get install -y
set -e
source ${COMP_BENCH}/install/common.sh

# ============
# LLVM
# ============
NAME="llvm"
VERSION="3.8.0"

SRC_PATH="${BIN_PATH}/${NAME}/llvm"
BUILD_PATH="${BIN_PATH}/${NAME}/build"
CLANG_PATH="${SRC_PATH}/tools"
RT_PATH="${SRC_PATH}/tools"

# download
mkdir -p ${BIN_PATH}/${NAME}
download_and_link llvm-${VERSION}.src http://llvm.org/releases/${VERSION}/llvm-${VERSION}.src.tar.xz ${SRC_PATH}

# configure
mkdir -p ${BUILD_PATH}
cd ${BUILD_PATH}
cmake -G "Unix Makefiles" -DCMAKE_BUILD_TYPE="Release" -DLLVM_TARGETS_TO_BUILD="X86" -DCMAKE_INSTALL_PREFIX=${BUILD_PATH} ../llvm

# install
make -j8
make -j8 install

# ============
# CLang
# ============
NAME="llvm"
VERSION="3.8.0"

SRC_PATH="${BIN_PATH}/${NAME}/llvm"
BUILD_PATH="${BIN_PATH}/${NAME}/build"
CLANG_PATH="${SRC_PATH}/tools"
RT_PATH="${SRC_PATH}/tools"

# download
mkdir -p ${BIN_PATH}/${NAME}
download_and_link cfe-${VERSION}.src http://llvm.org/releases/${VERSION}/cfe-${VERSION}.src.tar.xz ${CLANG_PATH}
download_and_link compiler-rt-${VERSION}.src http://llvm.org/releases/${VERSION}/compiler-rt-${VERSION}.src.tar.xz ${RT_PATH}

# configure
mkdir -p ${BUILD_PATH}
cd ${BUILD_PATH}
cmake -G "Unix Makefiles" -DCMAKE_BUILD_TYPE="Release" -DLLVM_TARGETS_TO_BUILD="X86" -DCMAKE_INSTALL_PREFIX=${BUILD_PATH} ../llvm

# install
make -j8
make -j8 install


# ============
# Gold Linker
# ============
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

set +e
