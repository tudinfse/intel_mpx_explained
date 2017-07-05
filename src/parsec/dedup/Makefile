NAME := dedup
SRC := binheap decoder dedup encoder hashtable queue rabin tree util

VPATH := src

CCFLAGS += -DMD32_REG_T=int -D_REENTRANT -DL_ENDIAN -DUSE_MMAP -D_XOPEN_SOURCE=600 -U_FORTIFY_SOURCE

INC_DIR += $(PROJ_ROOT)/src/parsec/dedup/src/include
LIB_DIRS += $(PROJ_ROOT)/build/libs/zlib/$(BUILD_TYPE)/lib \
            $(PROJ_ROOT)/build/libs/ssl/$(BUILD_TYPE)/lib
LIBS += -lssl -lz -lcrypto

include Makefile.$(BUILD_TYPE)
include ../parsec_common.mk

.PHONY: buildlibs

all:
	@${MAKE} buildlibs
	@${MAKE} $(BUILD_PATH)/$(NAME)

buildlibs: export BENCH_SUITE=libs

buildlibs:
	$(MAKE) BUILD_TYPE=$(BUILD_TYPE) -I $(PROJ_ROOT)/makefiles -C $(PROJ_ROOT)/src/$(BENCH_SUITE)/zlib
	$(MAKE) BUILD_TYPE=$(BUILD_TYPE) -I $(PROJ_ROOT)/makefiles -C $(PROJ_ROOT)/src/$(BENCH_SUITE)/ssl

