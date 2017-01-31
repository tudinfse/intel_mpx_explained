NAME := raytrace
# SRC is empty - no files are build directly

SUB_DIRS := LRT MiniView RTTL
SRC += $(SUB_DIRS)

VPATH := src
CCOMFLAGS += -pthread -DUSE_PBOS=1

MESA_BUILD_PATH:=$(COMP_BENCH)/experiments/build/parsec_libs/mesa/$(ACTION)
LIB_DIRS += $(MESA_BUILD_PATH)/lib
LIBS += -lglut -lGL -lGLU -lXmu -lXext -lXau -lX11 -ldl

INC_DIR += $(COMP_BENCH)/src/parsec/raytrace/src \
	       $(COMP_BENCH)/src/parsec/raytrace/src/RTTL/ $(COMP_BENCH)/src/parsec/raytrace/src/RTTL/common/ \
	       $(COMP_BENCH)/src/parsec/raytrace/src/RTTL/BVH/ $(COMP_BENCH)/src/parsec/raytrace/src/SG \
	       $(COMP_BENCH)/src/parsec/raytrace/src/LRT/include $(COMP_BENCH)/src/parsec/raytrace/src/LRT/
INC_DIR += $(MESA_BUILD_PATH)/include

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
	$(MAKE) ACTION=$(ACTION) -I $(COMP_BENCH)/experiments/makefiles -C $(COMP_BENCH)/src/$(BENCH_SUITE)/mesa

prebuild: export INC_DIR:=$(INC_DIR)

prebuild: export CCOMFLAGS:=$(CCOMFLAGS)

prebuild: export CFLAGS:=$(CFLAGS)

prebuild: export CXXFLAGS:=$(CXXFLAGS)

prebuild: export LIB_DIRS:=$(LIB_DIRS)

prebuild: export LIBS:=$(LIBS)

prebuild:
	$(foreach dir,$(SUB_DIRS),$(MAKE) -C src/$(dir) &&) echo ""

