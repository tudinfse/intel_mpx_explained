NAME := swaptions
SRC := CumNormalInv MaxFunction RanUnif icdf HJM_SimPath_Forward_Blocking HJM HJM_Swaption_Blocking HJM_Securities nr_routines

VPATH := src

CCOMFLAGS += -fstrict-aliasing -fkeep-inline-functions

include common.mk
include $(ACTION_MAKEFILE)
include ../parsec_common.mk


all: $(BUILD_PATH)/$(NAME)
