#!/usr/bin/env bash
# Replace ICC libraries with GCC ones in order for them to work correctly with MPX

LIBMPX_DIR=$(dirname $(which icc))/../../compiler/lib/intel64_lin/
mv $LIBMPX_DIR/libmpx.so $LIBMPX_DIR/libmpx.old.so