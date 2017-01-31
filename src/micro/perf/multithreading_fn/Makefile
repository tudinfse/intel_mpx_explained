NAME := multithreading_fn
SRC := multithreading_fn

LIBS += -pthread

include common.mk
include $(ACTION_MAKEFILE)

# less optimizations for simplicity
CCOMFLAGS := $(filter-out -O3,$(CCOMFLAGS))
CCOMFLAGS := $(filter-out -O2,$(CCOMFLAGS))
CCOMFLAGS += -O1

all: $(BUILD_PATH)/$(NAME)
