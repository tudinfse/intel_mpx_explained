NAME := word_count
SRC := word_count-seq

ifneq ($(strip $(NUM_THREADS)),1)
	SRC := word_count-pthread sort-pthread
	LIBS += -pthread
endif

INC_DIR := ${COMP_BENCH}/src/phoenix_pthread/include
VPATH := src

include common.mk
include $(ACTION_MAKEFILE)

all: $(BUILD_PATH)/$(NAME)
