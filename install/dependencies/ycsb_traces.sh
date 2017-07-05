#!/usr/bin/env bash

echo "Downloading traces..."
cd ${DATA_PATH}/

if [ -d "inputs" ]; then
    rm -rf inputs/ycsb-traces/
fi
mkdir -p inputs/

set +e
wget -nc https://wwwpub.zih.tu-dresden.de/~s7030030/ycsb-traces.tar.gz
set -e

tar xf ycsb-traces.tar.gz -C inputs/
rm ycsb-traces.tar.gz

echo "Traces installed"

cd -
