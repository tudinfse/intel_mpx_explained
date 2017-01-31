NAME := table_allocation
SRC := table_allocation

include common.mk
include $(ACTION_MAKEFILE)

CCOMFLAGS := $(filter-out -O3,$(CCOMFLAGS))
CCOMFLAGS += -O0  # we measure OS influence and therefore, the optimization level should be minimized

# uncomment to enable freeing memory
# CCOMFLAGS += -DFREE=1


all: $(BUILD_PATH)/$(NAME)
