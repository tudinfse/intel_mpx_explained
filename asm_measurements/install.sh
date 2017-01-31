#!/usr/bin/env bash

while true; do
    read -p "Are you sure you've read the README? " yn
    case $yn in
        [Yy]* ) break;;
        [Nn]* ) exit;;
        * ) echo "Please answer yes or no.";;
    esac
done

apt-get install g++-multilib
cd /root/bin/
wget http://www.nasm.us/pub/nasm/releasebuilds/2.12.02/nasm-2.12.02.tar.gz
tar xf nasm-2.12.02.tar.gz
rm nasm-2.12.02.tar.gz
cd nasm-2.12.02/

./configure
make
make install


cd $COMP_BENCH/asm_measurements/

rm -rf ./drv/
mkdir drv
cd drv/
unzip ../DriverSrcLinux.zip
chmod a+x *.sh
make
./install.sh

cd ../PMCTest/
chmod a+x *.sh

cd TestScripts/
chmod a+x *.sh
./init.sh
