#!/usr/bin/env bash
set -e

source ${COMP_BENCH}/install/common.sh
apt-get install -y libssl-dev libtext-lorem-perl apache2-utils

# nginx requires X permission for all users on the path: http://stackoverflow.com/questions/6795350/nginx-403-forbidden-for-all-files
chmod o+x /root

# ============
# nginx
# ============
SRC_PATH="${BIN_PATH}/nginx/src"
VERSION="1.4.0"

mkdir ${BIN_PATH}/nginx
download_and_link nginx-${VERSION} http://nginx.org/download/nginx-${VERSION}.tar.gz ${SRC_PATH}

sed -i "s/name\[1\]/name\[0\]/g" $SRC_PATH/src/core/ngx_hash.h
