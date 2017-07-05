#!/usr/bin/env bash

echo "Downloading inputs..."
cd ${DATA_PATH}/

if [ -d "inputs" ]; then
    rm -rf inputs/parsec/
fi
mkdir -p inputs/

set +e
wget -nc https://wwwpub.zih.tu-dresden.de/~s7030030/parsec-inputs.tar.gz
set -e

tar xf parsec-inputs.tar.gz -C inputs/
rm parsec-inputs.tar.gz

echo "Inputs installed"

cd -
