# we use version different from supplied in PARSEC: openssl-1.0.1f
# NOTE: we disable asm because most compiler mechanisms cannot work with it
NAME := ssl

include common.mk
include $(ACTION_MAKEFILE)

CFLAGS += $(CCOMFLAGS) -DPEDANTIC -pedantic
CXXFLAGS += $(CCOMFLAGS)
CC := $(CC) $(CFLAGS)
export

ifdef REBUILD
all: pre_clean
endif

all:
	cd src && ./config threads no-zlib no-dso no-shared no-test no-apps no-asm --prefix=$(BUILD_PATH) > $(CONFIG_SCRIPT_LOG) && cd -
# 	$(MAKE) -C src -j1 depend  # SSL has to be build using 1 thread
	$(MAKE) -C src -j1 > $(CONFIG_SCRIPT_LOG)
	$(MAKE) -C src -j1 install_sw > $(CONFIG_SCRIPT_LOG)

pre_clean:
	$(MAKE) -C src clean > $(CONFIG_SCRIPT_LOG)  || true
