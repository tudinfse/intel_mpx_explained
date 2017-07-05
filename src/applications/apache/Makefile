# Apache (httpd) version 2.4.18, taken from https://archive.apache.org/dist/httpd/httpd-2.4.18.tar.gz
NAME := apache

APACHE_SRC := ${BIN_PATH}/httpd/src/
SSL_BUILD := $(BUILD_ROOT)/libs/ssl/$(BUILD_TYPE)
APR_BUILD := $(BUILD_ROOT)/libs/apr/$(BUILD_TYPE)/bin
APRUTIL_BUILD := $(BUILD_ROOT)/libs/apr-util/$(BUILD_TYPE)/bin
PCRE_BUILD := $(BUILD_ROOT)/libs/pcre/$(BUILD_TYPE)/bin/pcre-config

CONFIG_OPT := --prefix=$(BUILD_PATH) \
				--with-apr=$(APR_BUILD) \
				--with-apr-util=$(APRUTIL_BUILD) \
				--with-pcre=$(PCRE_BUILD) \
				--with-ssl=$(SSL_BUILD) \
				--disable-shared \
				--enable-ssl \
				--enable-static-support \
				--enable-static-htpasswd \
				--enable-static-htdigest \
				--enable-static-rotatelogs \
				--enable-static-logresolve \
				--enable-static-htdbm \
				--enable-static-ab \
				--enable-static-checkgid \
				--enable-static-htcacheclean \
				--enable-static-httxt2dbm \
				--enable-static-fcgistarter \
				--enable-mod_authn_file \
				--enable-mod_authn_core \
				--enable-mod_authz_host \
				--enable-mod_authz_groupfile \
				--enable-mod_authz_user \
				--enable-mod_authz_core \
				--enable-mod_access_compat \
				--enable-mod_auth_basic \
				--enable-mod_reqtimeout \
				--enable-mod_filter \
				--enable-mod_mime \
				--enable-mod_log_config \
				--enable-mod_env \
				--enable-mod_headers \
				--enable-mod_setenvif \
				--enable-mod_version \
				--enable-mod_unixd \
				--enable-mod_status \
				--enable-mod_autoindex \
				--enable-mod_dir \
				--enable-mod_alias \
				--enable-mod_rewrite \
				--enable-mods-static='ssl authn_file authn_core authz_host authz_groupfile authz_user authz_core \
					  access_compat auth_basic reqtimeout filter mime log_config env headers setenvif \
					  version unixd status autoindex dir alias'

include Makefile.$(BUILD_TYPE)


$(eval $(call expand-ccflags))
LIBS += -ldl
export

# Targets
.PHONY: buildlibs

ifdef REBUILD
all: pre_clean
endif
all:
	@${MAKE} buildlibs
	@${MAKE} buildapache

buildapache:
	cd $(APACHE_SRC) && ./configure $(CONFIG_OPT) > $(CONFIG_SCRIPT_LOG)
	sed -i 's/--mode=link \$$(CC) \$$(ALL_CFLAGS)/--mode=link \$$(CC) -all-static \$$(ALL_CFLAGS)/g' $(APACHE_SRC)/build/rules.mk
	make -C $(APACHE_SRC) > $(CONFIG_SCRIPT_LOG)
	make install -C $(APACHE_SRC) > $(CONFIG_SCRIPT_LOG)

buildlibs: export BENCH_SUITE=libs
buildlibs:
	$(MAKE) BUILD_TYPE=$(BUILD_TYPE) -I $(PROJ_ROOT)/makefiles -C $(PROJ_ROOT)/src/libs/ssl
	$(MAKE) BUILD_TYPE=$(BUILD_TYPE) -I $(PROJ_ROOT)/makefiles -C $(PROJ_ROOT)/src/libs/apr
	$(MAKE) BUILD_TYPE=$(BUILD_TYPE) -I $(PROJ_ROOT)/makefiles -C $(PROJ_ROOT)/src/libs/apr-util
	$(MAKE) BUILD_TYPE=$(BUILD_TYPE) -I $(PROJ_ROOT)/makefiles -C $(PROJ_ROOT)/src/libs/pcre

pre_clean:
	$(MAKE) -C $(APACHE_SRC) distclean > $(CONFIG_SCRIPT_LOG) || true
