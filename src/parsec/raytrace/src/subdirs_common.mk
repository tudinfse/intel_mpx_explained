include common.mk
BUILD_PATH = $(COMP_BENCH)/experiments/build/$(BENCH_SUITE)/raytrace/$(ACTION)/$(NAME)
include $(ACTION_MAKEFILE)
include $(COMP_BENCH)/src/parsec/parsec_common.mk

# enforce build order
all:
	@${MAKE} make_sub_dirs
	@${MAKE} $(BUILD_PATH)/../$(NAME).$(OBJ_EXT)

make_sub_dirs:
	$(foreach dir,$(SUB_DIRS),mkdir -p $(BUILD_PATH)/$(dir) &&) touch .

$(BUILD_PATH)/../$(NAME).$(OBJ_EXT): $(LLS)
	$(LD) $(LDRELOC) $^ -o $@
