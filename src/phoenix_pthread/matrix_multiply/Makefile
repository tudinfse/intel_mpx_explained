NAME := matrix_multiply
SRC := matrix_multiply-seq

ifneq ($(strip $(NUM_THREADS)),1)
	SRC := matrix_multiply-pthread
	LIBS += -pthread
endif

INC_DIR := ${COMP_BENCH}/src/phoenix_pthread/include
VPATH := src

include common.mk
include $(ACTION_MAKEFILE)

all: $(BUILD_PATH)/$(NAME)
