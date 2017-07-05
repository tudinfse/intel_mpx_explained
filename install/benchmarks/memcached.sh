#!/usr/bin/env bash
set -e

echo "Installing Memcached..."

apt-get install -y automake autogen autoconf libtool

source ${PROJ_ROOT}/install/common.sh

SRC_PATH="${BIN_PATH}/memcached/src"
VERSION="1.4.15"

# download
mkdir -p ${BIN_PATH}/memcached
clone_github_and_link memcached-${VERSION} https://github.com/memcached/memcached.git ${SRC_PATH} ${VERSION} ${PROJ_ROOT}/install/benchmarks/memcached/memcached.1.4.15.patch

install_dependency "Memslap" "${PROJ_ROOT}/install/dependencies/memslap.sh"

echo "Memcached installed"
