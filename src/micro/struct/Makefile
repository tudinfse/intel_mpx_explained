NAME := struct
SRC := struct

include Makefile.$(BUILD_TYPE)

CCFLAGS := $(filter-out -O3,$(CCFLAGS))
CCFLAGS += -O2

all: $(BUILD_PATH)/$(NAME)
