#!/usr/bin/env bash

apt-get install -y unzip
set -e
source ${COMP_BENCH}/install/common.sh

# ============
# SoftBound
# ============
NAME="softboundcets"
VERSION="3.8.0"

SRC_PATH="${BIN_PATH}/${NAME}/src"
BUILD_PATH="${BIN_PATH}/${NAME}/build"

LLVM_SRC_PATH="${SRC_PATH}/llvm-38"
LLVM_BUILD_PATH="${BUILD_PATH}/llvm"

RT_SRC_PATH="${SRC_PATH}/runtime"

# download
mkdir -p ${BIN_PATH}/${NAME}
download_github_and_link ${NAME}-${VERSION} https://github.com/santoshn/${NAME}-${VERSION}/archive/master.zip ${SRC_PATH}

# build LLVM
mkdir -p ${LLVM_BUILD_PATH}
cd ${LLVM_BUILD_PATH}
cmake ${LLVM_SRC_PATH}
make -j8

# build runtime
export PATH=${LLVM_BUILD_PATH}/bin:$PATH
cd ${RT_SRC_PATH}
make

set +e
