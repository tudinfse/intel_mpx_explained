#!/bin/bash

declare -a libs=("glib" "gsl" "libjpeg" "libxml2" "mesa" "ssl" "zlib" "apr" "apr-util" "pcre" "libevent")

for lib in "${libs[@]}"; do
  pushd ${lib}/src
  make clean || true
  make distclean || true
  popd
done

rm -rf mesa/X11  # remove symbolic link
rm -rf mesa/src/lib

find . -type f -name *.debug -exec rm -f {} \;
