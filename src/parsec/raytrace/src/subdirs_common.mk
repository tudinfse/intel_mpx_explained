BUILD_PATH = $(BUILD_ROOT)/$(BENCH_SUITE)/raytrace/$(BUILD_TYPE)/$(NAME)
include Makefile.$(BUILD_TYPE)
include $(PROJ_ROOT)/src/parsec/parsec_common.mk

# enforce build order
all:
	@${MAKE} make_sub_dirs
	@${MAKE} $(BUILD_PATH)/../$(NAME).$(OBJ_EXT)

make_sub_dirs:
	$(foreach dir,$(SUB_DIRS),mkdir -p $(BUILD_PATH)/$(dir) &&) touch .

$(BUILD_PATH)/../$(NAME).$(OBJ_EXT): $(LLS)
	$(LD) $(LDRELOC) $^ -o $@
