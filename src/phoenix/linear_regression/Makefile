NAME := linear_regression
SRC := linear_regression-seq

ifneq ($(strip $(NUM_THREADS)),1)
	SRC := linear_regression-pthread
	LIBS += -pthread
endif

INC_DIR := ${PROJ_ROOT}/src/phoenix/include
VPATH := src

CFLAGS += -fno-unroll-loops

include Makefile.$(BUILD_TYPE)

all: $(BUILD_PATH)/$(NAME)
