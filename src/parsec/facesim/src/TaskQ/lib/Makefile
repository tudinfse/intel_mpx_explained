NAME := taskQ
SRC := taskQDistCommon

CCFLAGS += -DTASKQ_DIST_FIXED

include common.mk
BUILD_PATH = $(BUILD_ROOT)/$(BENCH_SUITE)/facesim/$(BUILD_TYPE)
include $(TYPE_MAKEFILE)
include $(PROJ_ROOT)/src/parsec/parsec_common.mk

all: $(BUILD_PATH)/$(NAME).$(OBJ_EXT)

$(BUILD_PATH)/$(NAME).$(OBJ_EXT): $(LLS)
	mv $^ $@

