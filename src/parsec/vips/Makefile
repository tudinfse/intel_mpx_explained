NAME := vips
SRC := vips dummy im_clamp bool_dispatch boolean

SUB_DIRS := iofuncs arithmetic resample colour conversion deprecated convolution format freq_filt histograms_lut \
            inplace mask morphology mosaicing other relational video
SRC += $(SUB_DIRS)

VPATH := src

INC_DIR += $(PROJ_ROOT)/src/parsec/vips/src/include
CCFLAGS += -DG_DISABLE_CAST_CHECKS -DHAVE_CONFIG_H -D restrict=__restrict__  -pthread
CFLAGS += -Wno-int-conversion -Wno-incompatible-pointer-types -Wno-implicit-function-declaration -Wno-int-to-pointer-cast \
		  -funroll-loops -fprefetch-loop-arrays
CXXFLAGS += -fexceptions

LIB_DIRS += $(PROJ_ROOT)/build/libs/zlib/$(BUILD_TYPE)/lib \
			$(PROJ_ROOT)/build/libs/glib/$(BUILD_TYPE)/lib \
			$(PROJ_ROOT)/build/libs/libxml2/$(BUILD_TYPE)/lib
LIBS += -lgmodule-2.0 -lxml2 -lgobject-2.0 -lgthread-2.0 -lglib-2.0 -lz -ldl

include Makefile.$(BUILD_TYPE)
include ../parsec_common.mk

.PHONY: buildlibs prebuild

# enforce build order
all:
	@${MAKE} buildlibs
	@${MAKE} prebuild
	@${MAKE} $(BUILD_PATH)/$(NAME)

buildlibs: export BENCH_SUITE=libs
buildlibs:
	$(MAKE) BUILD_TYPE=$(BUILD_TYPE) -I $(PROJ_ROOT)/makefiles -C $(PROJ_ROOT)/src/$(BENCH_SUITE)/zlib
	$(MAKE) BUILD_TYPE=$(BUILD_TYPE) -I $(PROJ_ROOT)/makefiles -C $(PROJ_ROOT)/src/$(BENCH_SUITE)/glib
	$(MAKE) BUILD_TYPE=$(BUILD_TYPE) -I $(PROJ_ROOT)/makefiles -C $(PROJ_ROOT)/src/$(BENCH_SUITE)/libxml2

prebuild: export INC_DIR:=$(INC_DIR)
prebuild: export CFLAGS:=$(CFLAGS) $(CCFLAGS)
prebuild: export CXXFLAGS:=$(CXXFLAGS) $(CCFLAGS)
prebuild: export LIB_DIRS:=$(LIB_DIRS)
prebuild: export LIBS:=$(LIBS)
prebuild:
	$(foreach dir,$(SUB_DIRS),$(MAKE) -C src/$(dir) &&) printf ""

