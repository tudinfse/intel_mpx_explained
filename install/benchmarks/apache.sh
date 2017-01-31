#!/usr/bin/env bash
set -e

apt-get install -y libtext-lorem-perl apache2-utils

source ${COMP_BENCH}/install/common.sh

# ============
# apache
# ============
SRC_PATH="${BIN_PATH}/httpd/src"
VERSION="2.4.18"

mkdir -p ${BIN_PATH}/httpd
download_and_link httpd-${VERSION} https://archive.apache.org/dist/httpd/httpd-${VERSION}.tar.gz ${SRC_PATH}

