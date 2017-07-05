# RIPE
NAME := ripe
SRC  := ripe_attack_generator_64

VPATH := src

include Makefile.$(BUILD_TYPE)

CCFLAGS += -O0 -g -fno-stack-protector -Wl,-z,execstack -U_FORTIFY_SOURCE -D_FORTIFY_SOURCE=0
CCFLAGS += -Wno-int-conversion -Wno-incompatible-pointer-types -Wno-format
ifneq (,$(findstring clang,$(CC)))
    CCFLAGS += -fno-vectorize
endif

ifneq (,$(findstring icc,$(CC)))
    CCFLAGS += -wd144,556,167
endif

all: $(BUILD_PATH)/$(NAME)

