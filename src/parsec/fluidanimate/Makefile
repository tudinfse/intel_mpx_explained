NAME := fluidanimate
SRC := serial cellpool

VPATH := src
CXXFLAGS += -Wno-invalid-offsetof -D_GNU_SOURCE -D_XOPEN_SOURCE=600

ifneq ($(strip $(NUM_THREADS)),1)
    SRC := $(filter-out serial,$(SRC))
    SRC += pthreads parsec_barrier
endif

include common.mk
include $(ACTION_MAKEFILE)
include ../parsec_common.mk

all: $(BUILD_PATH)/$(NAME)
