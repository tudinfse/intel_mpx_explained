#!/usr/bin/env bash

source ${PROJ_ROOT}/install/common.sh

echo "Downloading libraries..."
cd ${DATA_PATH}/

if [ -d "apache_libs" ]; then
    rm -rf apache_libs/
fi
mkdir apache_libs/

set +e
wget -nc https://wwwpub.zih.tu-dresden.de/~s7030030/apache_libs.tar.gz
set -e

tar xf apache_libs.tar.gz -C apache_libs/
rm apache_libs.tar.gz

cd -

echo "Preparing libraries..."
cd ${DATA_PATH}/apache_libs/

for lib in *; do
    if [ -d "${lib}" ]; then
        cp -r ${lib}/src/ ${PROJ_ROOT}/src/libs/${lib}/src/
    fi
done

# add missing files
cd ${PROJ_ROOT}/src/libs
mkdir -p pcre/src/doc
touch pcre/src/doc/perltest.txt pcre/src/doc/index.html.src

echo "Libraries installed"
