NAME := struct
SRC := struct

include common.mk
include $(ACTION_MAKEFILE)

CCOMFLAGS := $(filter-out -O3,$(CCOMFLAGS))
CCOMFLAGS += -O2

all: $(BUILD_PATH)/$(NAME)
