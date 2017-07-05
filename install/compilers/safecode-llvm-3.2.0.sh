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
# LLVM 3.2
# ============
NAME="llvm-32"
VERSION="3.2"

SRC_PATH="${BIN_PATH}/${NAME}/llvm"
BUILD_PATH="${BIN_PATH}/${NAME}/build"
CLANG_PATH="${SRC_PATH}/tools/clang"

# download
mkdir -p ${BIN_PATH}/${NAME}
download_and_link llvm-${VERSION}.src http://llvm.org/releases/${VERSION}/llvm-${VERSION}.src.tar.gz ${SRC_PATH}
download_and_link clang-${VERSION}.src http://llvm.org/releases/${VERSION}/clang-${VERSION}.src.tar.gz ${CLANG_PATH}

# configure
mkdir -p ${BUILD_PATH}
cd ${BUILD_PATH}
cmake -G "Unix Makefiles" -DCMAKE_BUILD_TYPE="Release" -DLLVM_TARGETS_TO_BUILD="X86" ../llvm

# install
make -j8
make -j8 install

# ============
# SAFECode
# ============
NAME="safecode"
VERSION="32"

SRC_PATH="${BIN_PATH}/${NAME}/src"
BUILD_PATH="${BIN_PATH}/${NAME}/build"
GOLD_PATH="${BIN_PATH}/binutils_gold/install"

# download
mkdir -p ${BIN_PATH}/${NAME}
cd /data/

set +e
svn co http://llvm.org/svn/llvm-project/llvm/branches/release_32 ${NAME}
cd - && cd /data/${NAME}/projects

svn co http://llvm.org/svn/llvm-project/poolalloc/branches/release_32 poolalloc
svn co http://llvm.org/svn/llvm-project/safecode/branches/release_32 safecode
set -e

# Update the sources!

rm -f ${SRC_PATH}
ln -s /data/${NAME} ${SRC_PATH}
cd -

# configure
mkdir -p $BUILD_PATH && cd $BUILD_PATH
${SRC_PATH}/configure --enable-optimized --prefix=${GOLD_PATH} --with-binutils-include=${BIN_PATH}/binutils_gold/src/include

# build
MAKE="make -j8"
$MAKE tools-only
$MAKE install

$MAKE -C ./projects/poolalloc
$MAKE -C ./projects/poolalloc install

$MAKE -C ./projects/safecode
$MAKE -C ./projects/safecode install


set +e
