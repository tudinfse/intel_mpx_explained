NAME := arraywrite
SRC := arraywrite

# let's forbid GCC do some weird stuff
CCOMFLAGS += -fno-tree-vectorize

include common.mk
include $(ACTION_MAKEFILE)

all: $(BUILD_PATH)/$(NAME)
