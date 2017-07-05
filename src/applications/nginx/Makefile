# Nginx version 1.4.0
NAME := nginx
SRC_PATH := $(BIN_PATH)/nginx/src

SSL_PATH := $(PROJ_ROOT)/src/libs/ssl/src/
SSL_OPT := threads no-zlib no-dso no-shared no-test no-apps no-asm

include Makefile.$(BUILD_TYPE)

$(eval $(call expand-ccflags))
CC := $(CC) $(CFLAGS)  # this is for OpenSSL
export

CONFIG_OPTS := --with-cc="$(CC)" \
			   --with-cc-opt="$(INCLUDE_HEADER_DIRS) $(INCLUDE_LIB_DIRS)" \
			   --with-ld-opt="$(LIBS)" \
			   --with-openssl=$(SSL_PATH) \
			   --with-openssl-opt="$(SSL_OPT)"  \
			   --without-http_rewrite_module \
			   --without-http_gzip_module \
			   --with-http_ssl_module \
			   --with-debug \
			   --prefix=$(BUILD_PATH)

all:
	cd $(SRC_PATH) && ./configure $(CONFIG_OPTS) > $(CONFIG_SCRIPT_LOG)
	make -C $(SRC_PATH)  > $(CONFIG_SCRIPT_LOG)
	make install -C $(SRC_PATH)  > $(CONFIG_SCRIPT_LOG)
