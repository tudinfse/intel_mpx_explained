NAME := kmeans
SRC := kmeans-seq

ifneq ($(strip $(NUM_THREADS)),1)
	SRC := kmeans-pthread
	LIBS += -pthread
endif

INC_DIR := ${PROJ_ROOT}/src/phoenix/include
VPATH := src

include Makefile.$(BUILD_TYPE)

all: $(BUILD_PATH)/$(NAME)
