NAME := glib

include common.mk
include $(ACTION_MAKEFILE)

# zlib is always compiled before glib, so we can rely on files existing
CFLAGS  += -I$(COMP_BENCH)/experiments/build/parsec_libs/zlib/$(ACTION)/include
LDFLAGS += -L$(COMP_BENCH)/experiments/build/parsec_libs/zlib/$(ACTION)/lib

CFLAGS += $(CCOMFLAGS)
CXXFLAGS += $(CCOMFLAGS)
export

# Note: We always compile with thread support enabled because
# the serial version of glib is broken.

ifdef REBUILD
all: pre_clean
endif

# the `> $(CONFIG_SCRIPT_LOG)` redirection is nessesary to shut the f... ehm, to silence the build process
all:
	cd src && ./configure --disable-shared --enable-threads --with-threads=posix --prefix=$(BUILD_PATH) > $(CONFIG_SCRIPT_LOG)
	$(MAKE) -C src > $(CONFIG_SCRIPT_LOG)
	$(MAKE) -C src install > $(CONFIG_SCRIPT_LOG)

pre_clean:
	$(MAKE) -C src distclean > $(CONFIG_SCRIPT_LOG) || true
