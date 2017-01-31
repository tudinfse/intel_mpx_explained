#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

apt-get install -y pkg-config gettext \
                   libbsd-dev libx11-dev x11proto-xext-dev libxext-dev libxt-dev libxi-dev libxmu-dev \
                   libglib2.0-dev

echo "=== Downloading inputs ==="
rsync -r alex@141.76.44.133:shared/inputs/parsec/  "${DATA_PATH}/inputs/parsec/"
rsync -r alex@141.76.44.133:shared/include/vips/  ${COMP_BENCH}/src/parsec/vips/src/include/
echo "Parsec installed"
