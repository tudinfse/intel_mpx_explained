#!/usr/bin/env bash

echo "Installing Phoenix..."

source ${PROJ_ROOT}/install/common.sh
apt-get install -y wget libc6-dev-i386

install_dependency "Phoenix inputs" "${PROJ_ROOT}/install/dependencies/phoenix_inputs.sh"

echo "Phoenix installed"
