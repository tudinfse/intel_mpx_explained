NAME := pca
SRC := pca-seq

ifneq ($(strip $(NUM_THREADS)),1)
	SRC := pca-pthread
	LIBS += -pthread
endif

INC_DIR += ${PROJ_ROOT}/src/phoenix/include
VPATH := src

CFLAGS := $(CFLAGS)

include Makefile.$(BUILD_TYPE)

all: $(BUILD_PATH)/$(NAME)
