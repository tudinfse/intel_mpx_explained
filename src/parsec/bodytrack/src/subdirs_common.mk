include common.mk
BUILD_PATH = $(COMP_BENCH)/experiments/build/$(BENCH_SUITE)/bodytrack/$(ACTION)/$(NAME)
include $(ACTION_MAKEFILE)
include $(COMP_BENCH)/src/parsec/parsec_common.mk

all: $(BUILD_PATH)/../$(NAME).$(OBJ_EXT)

$(BUILD_PATH)/../$(NAME).$(OBJ_EXT): $(LLS)
	$(LD) $(LDRELOC) $^ -o $@

