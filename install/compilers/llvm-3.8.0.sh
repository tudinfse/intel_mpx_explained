#!/usr/bin/env bash

echo "Installing LLVM..."

#apt-get install -y
set -e
source ${PROJ_ROOT}/install/common.sh

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


install_dependency "Gold Linker" "${PROJ_ROOT}/install/dependencies/gold-linker.sh"

set +e

echo "LLVM installed"
