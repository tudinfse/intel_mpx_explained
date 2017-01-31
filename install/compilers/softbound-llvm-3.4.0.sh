#!/usr/bin/env bash

apt-get install -y unzip
set -e
source ${COMP_BENCH}/install/common.sh

# check Gold linker
if [ ! -d "${BIN_PATH}/binutils_gold/build" ]; then
    echo "Install normal LLVM first:"
    echo "    ./fex.py install -n llvm-3.8.0"
    exit 1
fi

# ============
# SoftBound
# ============
NAME="softboundcets"
VERSION="34"

SRC_PATH="${BIN_PATH}/${NAME}/src"
BUILD_PATH="${BIN_PATH}/${NAME}/build"
GOLD_PATH="${BIN_PATH}/binutils_gold/install"

LLVM_SRC_PATH="${SRC_PATH}/softboundcets-llvm-clang34"
LLVM_BUILD_PATH="${BUILD_PATH}/llvm"

RT_SRC_PATH="${SRC_PATH}/softboundcets-lib"

# download
mkdir -p ${BIN_PATH}/${NAME}
download_github_and_link ${NAME}-${VERSION} https://github.com/santoshn/${NAME}-${VERSION}/archive/master.zip ${SRC_PATH}

# build LLVM
mkdir -p ${LLVM_BUILD_PATH}
cd ${LLVM_BUILD_PATH}

${LLVM_SRC_PATH}/configure --enable-assertions --enable-optimized --disable-bindings --with-binutils-include=${GOLD_PATH}/include/
make -j8

# build runtime
export PATH=${LLVM_BUILD_PATH}/Release+Asserts/bin:$PATH
export LLVM_GOLD=${LLVM_BUILD_PATH}/Release+Asserts/lib/LLVMgold.so
cd ${RT_SRC_PATH}
make clean && make

set +e
