#!/usr/bin/env bash
set -e

echo "Installing Apache..."

apt-get install -y libtext-lorem-perl apache2-utils automake

source ${PROJ_ROOT}/install/common.sh

SRC_PATH="${BIN_PATH}/httpd/src"
VERSION="2.4.18"

mkdir -p ${BIN_PATH}/httpd
download_and_link httpd-${VERSION} https://archive.apache.org/dist/httpd/httpd-${VERSION}.tar.gz ${SRC_PATH}

install_dependency "Apache libraries" "${PROJ_ROOT}/install/dependencies/apache_libs.sh"

echo "Apache installed"
