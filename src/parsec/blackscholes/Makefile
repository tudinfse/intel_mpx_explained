NAME := blackscholes
SRC := blackscholes

VPATH := src

CFLAGS += -DNCO=2 -DN=960
CXXFLAGS += -DNCO=2 -DN=960

include common.mk
include $(ACTION_MAKEFILE)
include ../parsec_common.mk

all: $(BUILD_PATH)/$(NAME)
