NAME := histogram
SRC := histogram-seq

ifneq ($(strip $(NUM_THREADS)),1)
	SRC := histogram-pthread
	LIBS += -pthread
endif

INC_DIR := ${COMP_BENCH}/src/phoenix_pthread/include
VPATH := src

include common.mk
include $(ACTION_MAKEFILE)

all: $(BUILD_PATH)/$(NAME)
