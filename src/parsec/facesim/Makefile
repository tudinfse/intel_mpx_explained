NAME := facesim
SRC := main FACE_DRIVER FACE_LANDMARK_OPTIMIZATION_GOAL FACE_OPTIMIZATION LANDMARK_PROXIMITY_OPTIMIZATION taskQ

VPATH := src

CXXFLAGS += -fexceptions
INC_DIR += $(COMP_BENCH)/src/parsec/facesim/src/
INC_DIR += $(COMP_BENCH)/src/parsec/facesim/src/TaskQ/include

LIB_DIRS += $(COMP_BENCH)/src/parsec/facesim/src/lib/
LIBS += -lPhysBAM


ifneq ($(strip $(NUM_THREADS)),1)
	CCOMFLAGS += -DENABLE_PTHREADS
else
	CCOMFLAGS += -DNEW_SERIAL_IMPLEMENTATIOM
endif

include common.mk
include $(ACTION_MAKEFILE)
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
