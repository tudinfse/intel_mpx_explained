NAME := facesim
SRC := main FACE_DRIVER FACE_LANDMARK_OPTIMIZATION_GOAL FACE_OPTIMIZATION LANDMARK_PROXIMITY_OPTIMIZATION taskQ

VPATH := src

CXXFLAGS += -fexceptions
INC_DIR += $(PROJ_ROOT)/src/parsec/facesim/src/ \
 		   $(PROJ_ROOT)/src/parsec/facesim/src/TaskQ/include

LIB_DIRS += $(PROJ_ROOT)/src/parsec/facesim/src/lib/
LIBS += -lPhysBAM


ifneq ($(strip $(NUM_THREADS)),1)
	CCFLAGS += -DENABLE_PTHREADS
else
	CCFLAGS += -DNEW_SERIAL_IMPLEMENTATIOM
endif

include Makefile.$(BUILD_TYPE)
include ../parsec_common.mk

ifeq ($(CC),icc)
    CFLAGS += -D__thread=___thread -Kc++
endif

export

.PHONY: prebuild

# enforce build order
all:
	@${MAKE} prebuild
	@${MAKE} $(BUILD_PATH)/$(NAME)

prebuild:
	$(MAKE) -C src/TaskQ/lib
	$(MAKE) -C src/Public_Library
