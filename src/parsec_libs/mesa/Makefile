NAME := mesa

include common.mk
include $(ACTION_MAKEFILE)

CFLAGS += -I$(COMP_BENCH)/src/parsec_libs/mesa

CFLAGS += $(CCOMFLAGS)
CXXFLAGS += $(CCOMFLAGS)
export

ifdef REBUILD
all: pre_clean
endif

# the `> $(CONFIG_SCRIPT_LOG)` redirection is nessesary to silence the build process
all:
	ln -s /usr/include/X11 X11 || true  # dirty hack to include X11 headers even under SGX (assumes `/usr/include/X11` exists)
	$(MAKE) -C src clean > $(CONFIG_SCRIPT_LOG)  || true
	cd src && ./configure --with-driver=xlib --enable-glut --enable-static --disable-shared --prefix=$(BUILD_PATH) > $(CONFIG_SCRIPT_LOG)
	$(MAKE) -C src > $(CONFIG_SCRIPT_LOG)
	$(MAKE) -C src install > $(CONFIG_SCRIPT_LOG)

pre_clean:
	$(MAKE) -C src clean > $(CONFIG_SCRIPT_LOG)  || true
