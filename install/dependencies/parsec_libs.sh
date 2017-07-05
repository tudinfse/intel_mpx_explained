#!/usr/bin/env bash

echo "Downloading libraries..."
cd ${DATA_PATH}/

if [ -d "parsec_libs" ]; then
    rm -rf parsec_libs/
fi
mkdir parsec_libs/

set +e
wget -nc https://wwwpub.zih.tu-dresden.de/~s7030030/parsec_libs.tar.gz
set -e

tar xf parsec_libs.tar.gz -C parsec_libs/
rm parsec_libs.tar.gz

cd -

echo "Preparing libraries..."
cd ${DATA_PATH}/parsec_libs/

for lib in *; do
    if [ -d "${lib}" ]; then
        cp -r ${lib}/src/ ${PROJ_ROOT}/src/libs/${lib}/src/
    fi
done

echo "Libraries installed"
