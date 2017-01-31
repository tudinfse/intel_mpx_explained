# apr-util-1.5.4, taken from http://mirror.symnds.com/software/Apache/apr/apr-util-1.5.4.tar.gz
NAME := apr-util

include common.mk
include $(ACTION_MAKEFILE)

CFLAGS += $(CCOMFLAGS)
CXXFLAGS += $(CCOMFLAGS)
export

ifdef REBUILD
all: pre_clean
endif

# the `> $(CONFIG_SCRIPT_LOG)` redirection is nessesary to shut the f... ehm, to silence the build process
# apr & openssl are always compiled before apr-util, so we can rely on files existing
all:
	cd src && ./configure --prefix=$(BUILD_PATH) --with-apr=$(COMP_BENCH)/experiments/build/parsec_libs/apr/$(ACTION) --without-pgsql --with-openssl=$(COMP_BENCH)/experiments/build/parsec_libs/ssl/$(ACTION) > $(CONFIG_SCRIPT_LOG)
	sed -i "s/--mode=link \$$(CC)/--mode=link \$$(CC) -all-static/g" src/Makefile
	if [ -a src/xml/expat/Makefile ] ; then sed -i "s/) -no-undefined/) -all-static -no-undefined/g" src/xml/expat/Makefile ; fi;
	$(MAKE) -C src > $(CONFIG_SCRIPT_LOG)
	$(MAKE) -C src install > $(CONFIG_SCRIPT_LOG)

pre_clean:
	$(MAKE) -C src distclean > $(CONFIG_SCRIPT_LOG) || true
