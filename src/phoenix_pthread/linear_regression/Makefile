NAME := linear_regression
SRC := linear_regression-seq

ifneq ($(strip $(NUM_THREADS)),1)
	SRC := linear_regression-pthread
	LIBS += -pthread
endif

INC_DIR := ${COMP_BENCH}/src/phoenix_pthread/include
VPATH := src

CFLAGS += -fno-unroll-loops

include common.mk
include $(ACTION_MAKEFILE)

all: $(BUILD_PATH)/$(NAME)
