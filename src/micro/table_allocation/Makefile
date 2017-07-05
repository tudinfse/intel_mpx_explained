NAME := table_allocation
SRC := table_allocation

include Makefile.$(BUILD_TYPE)

CCFLAGS := $(filter-out -O3,$(CCFLAGS))
CCFLAGS += -O0  # we measure OS influence and therefore, the optimization level should be minimized

# uncomment to enable freeing memory
# CCFLAGS += -DFREE=1


all: $(BUILD_PATH)/$(NAME)
