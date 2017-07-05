NAME := bodytrack
SRC := AnnealingFactor BodyGeometry BodyPose CameraModel CovarianceMatrix ImageMeasurements ImageProjection \
       RandomGenerator TrackingModel main

SUB_DIRS := FlexImageLib


ifneq ($(strip $(NUM_THREADS)),1)
	SRC += AsyncIO TrackingModelPthread
	SUB_DIRS += threads
	CCFLAGS += -DHAVE_LIBPTHREAD
endif

SRC += $(SUB_DIRS)

VPATH := src
INC_DIR += $(PROJ_ROOT)/src/parsec/bodytrack/src/FlexImageLib $(PROJ_ROOT)/src/parsec/bodytrack/src
CCFLAGS += -DHAVE_CONFIG_H -std=c++98
CXXFLAGS += -fexceptions

include Makefile.$(BUILD_TYPE)
include ../parsec_common.mk

export  # make sure that makefiles in the subdirectories have the same environment

# enforce build order
all:
	@${MAKE} prebuild
	@${MAKE} $(BUILD_PATH)/$(NAME)

.PHONY: prebuild
prebuild:
	$(foreach dir,$(SUB_DIRS),$(MAKE) -C src/$(dir) &&) printf ""
