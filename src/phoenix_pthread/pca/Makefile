NAME := pca
SRC := pca-seq

ifneq ($(strip $(NUM_THREADS)),1)
	SRC := pca-pthread
	LIBS += -pthread
endif

INC_DIR += ${COMP_BENCH}/src/phoenix_pthread/include
VPATH := src

CFLAGS := $(CFLAGS)

include common.mk
include $(ACTION_MAKEFILE)

all: $(BUILD_PATH)/$(NAME)
