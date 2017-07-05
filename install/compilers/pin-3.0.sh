#!/usr/bin/env bash

set -e
source ${PROJ_ROOT}/install/common.sh

# ============
# Intel Pin
# ============
ULRNAME="pin-3.0-76991-gcc-linux"
NAME="pin"

# download
mkdir -p ${BIN_PATH}
cd ${BIN_PATH}
wget -nc http://software.intel.com/sites/landingpage/pintool/downloads/${ULRNAME}.tar.gz
tar xf ${ULRNAME}.tar.gz
rm -rf ${NAME}
mv ${ULRNAME} ${NAME}

export PIN_ROOT=${BIN_PATH}/${NAME}

cd -
make -C ${PROJ_ROOT}/install/compilers/pintool
ln -s ${PROJ_ROOT}/install/compilers/pintool/obj-intel64/mpxinscount.so ${PIN_ROOT}/mpxinscount.so

set +e
