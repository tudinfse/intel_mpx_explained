# RIPE
NAME := ripe
SRC  := ripe_attack_generator_64

VPATH := src

include common.mk
include $(ACTION_MAKEFILE)

CCOMFLAGS += -O0 -g -fno-stack-protector -Wl,-z,execstack -U_FORTIFY_SOURCE -D_FORTIFY_SOURCE=0
CCOMFLAGS += -Wno-int-conversion -Wno-incompatible-pointer-types -Wno-format
ifneq (,$(findstring clang,$(CC)))
    CCOMFLAGS += -fno-vectorize
endif

ifneq (,$(findstring icc,$(CC)))
    CCOMFLAGS += -wd144,556,167
endif

all: $(BUILD_PATH)/$(NAME)

