# apr-1.5.2, taken from http://mirror.softaculous.com/apache/apr/apr-1.5.2.tar.gz
NAME := apr

include common.mk
include $(ACTION_MAKEFILE)

CFLAGS += $(CCOMFLAGS)
CXXFLAGS += $(CCOMFLAGS)
export

ifdef REBUILD
all: pre_clean
endif

# the `> $(CONFIG_SCRIPT_LOG)` redirection is nessesary to shut the f... ehm, to silence the build process
all:
	cd src && ./configure --prefix=$(BUILD_PATH) --disable-shared --disable-dso > $(CONFIG_SCRIPT_LOG)
	sed -i 's/#define APR_HAS_MMAP              1/#define APR_HAS_MMAP              0/g' src/include/apr.h
	$(MAKE) -C src > $(CONFIG_SCRIPT_LOG)
	$(MAKE) -C src install > $(CONFIG_SCRIPT_LOG)

pre_clean:
	$(MAKE) -C src distclean > $(CONFIG_SCRIPT_LOG) || true
