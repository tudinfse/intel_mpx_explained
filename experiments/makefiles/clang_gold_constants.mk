# Clang with Gold linker
include clang_constants.mk

# GOLD_PATH is defined in local.mk
CCOMFLAGS += "-flto"
export PATH="$GOLD_PATH/bin:$PATH"

RANLIB=/bin/true #ranlib is not needed, and doesn't support .bc files in .a

