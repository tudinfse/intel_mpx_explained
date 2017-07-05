# apr-1.5.2, taken from http://mirror.softaculous.com/apache/apr/apr-1.5.2.tar.gz
NAME := apr

# undefine variables from recursive calls
undefine BUILD_PATH

# import type-specific configuration
include Makefile.$(BUILD_TYPE)
$(eval $(call expand-ccflags))


ifdef REBUILD
all: pre_clean
endif
all:
	cd src && ./configure --prefix=$(BUILD_PATH) --disable-shared --disable-dso > $(CONFIG_SCRIPT_LOG)
	sed -i 's/#define APR_HAS_MMAP              1/#define APR_HAS_MMAP              0/g' src/include/apr.h
	$(MAKE) -C src > $(CONFIG_SCRIPT_LOG)
	$(MAKE) -C src install > $(CONFIG_SCRIPT_LOG)

pre_clean:
	$(MAKE) -C src distclean > $(CONFIG_SCRIPT_LOG) || true
