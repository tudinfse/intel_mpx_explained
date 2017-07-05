NAME := swaptions
SRC := CumNormalInv MaxFunction RanUnif icdf HJM_SimPath_Forward_Blocking HJM HJM_Swaption_Blocking HJM_Securities nr_routines

VPATH := src

CCFLAGS += -fstrict-aliasing -fkeep-inline-functions

include Makefile.$(BUILD_TYPE)
include ../parsec_common.mk


all: $(BUILD_PATH)/$(NAME)
