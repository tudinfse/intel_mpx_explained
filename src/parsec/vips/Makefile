NAME := vips
SRC := vips dummy im_clamp bool_dispatch boolean

SUB_DIRS := iofuncs arithmetic resample colour conversion deprecated convolution format freq_filt histograms_lut \
            inplace mask morphology mosaicing other relational video
SRC += $(SUB_DIRS)

VPATH := src

INC_DIR += $(COMP_BENCH)/src/parsec/vips/src/include
CFLAGS += -Wno-int-conversion -Wno-incompatible-pointer-types -Wno-implicit-function-declaration -Wno-int-to-pointer-cast
CFLAGS += -funroll-loops -fprefetch-loop-arrays -D restrict=__restrict__
CFLAGS += -DG_DISABLE_CAST_CHECKS -DHAVE_CONFIG_H -pthread
CXXFLAGS += -DG_DISABLE_CAST_CHECKS -DHAVE_CONFIG_H -fexceptions -D restrict=__restrict__ -pthread

LIB_DIRS += $(COMP_BENCH)/experiments/build/parsec_libs/zlib/$(ACTION)/lib
LIB_DIRS += $(COMP_BENCH)/experiments/build/parsec_libs/glib/$(ACTION)/lib
LIB_DIRS += $(COMP_BENCH)/experiments/build/parsec_libs/libxml2/$(ACTION)/lib
LIBS += -lgmodule-2.0 -lxml2 -lgobject-2.0 -lgthread-2.0 -lglib-2.0 -lz -ldl

include common.mk
include $(ACTION_MAKEFILE)
include ../parsec_common.mk

.PHONY: buildlibs prebuild

# enforce build order
all:
	@${MAKE} buildlibs
	@${MAKE} prebuild
	@${MAKE} $(BUILD_PATH)/$(NAME)

buildlibs: export BENCH_SUITE=parsec_libs
buildlibs:
	$(MAKE) ACTION=$(ACTION) -I $(COMP_BENCH)/experiments/makefiles -C $(COMP_BENCH)/src/$(BENCH_SUITE)/zlib
	$(MAKE) ACTION=$(ACTION) -I $(COMP_BENCH)/experiments/makefiles -C $(COMP_BENCH)/src/$(BENCH_SUITE)/glib
	$(MAKE) ACTION=$(ACTION) -I $(COMP_BENCH)/experiments/makefiles -C $(COMP_BENCH)/src/$(BENCH_SUITE)/libxml2

prebuild: export INC_DIR:=$(INC_DIR)
prebuild: export CFLAGS:=$(CFLAGS)
prebuild: export CXXFLAGS:=$(CXXFLAGS)
prebuild: export LIB_DIRS:=$(LIB_DIRS)
prebuild: export LIBS:=$(LIBS)
prebuild:
	$(foreach dir,$(SUB_DIRS),$(MAKE) -C src/$(dir) &&) echo ""

