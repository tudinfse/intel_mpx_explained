NAME := x264
SRC := x264 matroska muxers \
  mc predict pixel macroblock frame dct cpu cabac common mdate set quant vlc \
  encoder_analyse encoder_me encoder_ratecontrol encoder_set encoder_macroblock encoder_cabac encoder_cavlc encoder_encoder

VPATH := src

INC_DIR += $(COMP_BENCH)/src/parsec/x264/src/
CCOMFLAGS += -pthread -ffast-math -Wno-aggressive-loop-optimizations -Wno-int-conversion -DHAVE_MALLOC_H -DARCH_X86_64 -DSYS_LINUX -DHAVE_PTHREAD -fomit-frame-pointer
LIBS += -lm

include common.mk
include $(ACTION_MAKEFILE)
include ../parsec_common.mk

all: $(BUILD_PATH)/$(NAME)

