# apr-util-1.5.4, taken from http://mirror.symnds.com/software/Apache/apr/apr-util-1.5.4.tar.gz
NAME := apr-util

# undefine variables from recursive calls
undefine BUILD_PATH

# import type-specific configuration
include Makefile.$(BUILD_TYPE)
$(eval $(call expand-ccflags))


# apr & openssl are always compiled before apr-util, so we can rely on files existing
ifdef REBUILD
all: pre_clean
endif
all:
	cd src && ./configure --prefix=$(BUILD_PATH) --with-apr=$(BUILD_ROOT)/libs/apr/$(BUILD_TYPE) --without-pgsql --with-openssl=$(BUILD_ROOT)/libs/ssl/$(BUILD_TYPE) > $(CONFIG_SCRIPT_LOG)
	sed -i "s/--mode=link \$$(CC)/--mode=link \$$(CC) -all-static/g" src/Makefile
	if [ -a src/xml/expat/Makefile ] ; then sed -i "s/) -no-undefined/) -all-static -no-undefined/g" src/xml/expat/Makefile ; fi;
	$(MAKE) -C src > $(CONFIG_SCRIPT_LOG)
	$(MAKE) -C src install > $(CONFIG_SCRIPT_LOG)

pre_clean:
	$(MAKE) -C src distclean > $(CONFIG_SCRIPT_LOG) || true
