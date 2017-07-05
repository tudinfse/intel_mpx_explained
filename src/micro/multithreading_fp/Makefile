NAME := multithreading_fp
SRC := multithreading_fp

LIBS += -pthread

include Makefile.$(BUILD_TYPE)

# less optimizations for simplicity
CCFLAGS := $(filter-out -O3,$(CCFLAGS))
CCFLAGS := $(filter-out -O2,$(CCFLAGS))
CCFLAGS += -O1

all: $(BUILD_PATH)/$(NAME)
