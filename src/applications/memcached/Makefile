# Memcached version 1.4.15
NAME := memcached

MEMCACHED_SRC := ${BIN_PATH}/memcached/src/
LIBEVENT_BUILD := $(COMP_BENCH)/experiments/build/parsec_libs/libevent/$(ACTION)

CONFIG_OPT := --prefix=$(BUILD_PATH) \
				--with-libevent==$(LIBEVENT_BUILD) \
				--mandir=/tmp --disable-coverage

include common.mk
include $(ACTION_MAKEFILE)

CCOMFLAGS += -std=gnu99 -DHAVE_CONFIG_H -Wall -I/usr/include/x86_64-linux-gnu
CFLAGS += $(CCOMFLAGS)
CXXFLAGS += $(CCOMFLAGS)
export

.PHONY: buildlibs

ifdef REBUILD
all: pre_clean
endif

all:
	@${MAKE} buildlibs
	@${MAKE} buildmemcached

buildmemcached:
	cd $(MEMCACHED_SRC) && ACLOCAL=aclocal AUTOMAKE=automake ./autogen.sh > $(CONFIG_SCRIPT_LOG) || true
	cd $(MEMCACHED_SRC) && ./configure $(CONFIG_OPT) > $(CONFIG_SCRIPT_LOG)
	make -C $(MEMCACHED_SRC)  > $(CONFIG_SCRIPT_LOG)
	make install -C $(MEMCACHED_SRC)  > $(CONFIG_SCRIPT_LOG)

buildlibs: export BENCH_SUITE=parsec_libs
buildlibs:
	$(MAKE) ACTION=$(ACTION) -I $(COMP_BENCH)/experiments/makefiles -C $(COMP_BENCH)/src/parsec_libs/libevent

pre_clean:
	$(MAKE) -C $(MEMCACHED_SRC) clean > $(CONFIG_SCRIPT_LOG) || true

