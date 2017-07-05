NAME := histogram
SRC := histogram-seq

ifneq ($(strip $(NUM_THREADS)),1)
	SRC := histogram-pthread
	LIBS += -pthread
endif

INC_DIR := ${PROJ_ROOT}/src/phoenix/include
VPATH := src

include Makefile.$(BUILD_TYPE)

all: $(BUILD_PATH)/$(NAME)
