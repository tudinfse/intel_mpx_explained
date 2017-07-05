BUILD_PATH = $(BUILD_ROOT)/$(BENCH_SUITE)/bodytrack/$(BUILD_TYPE)/$(NAME)
include Makefile.$(BUILD_TYPE)
include $(PROJ_ROOT)/src/parsec/parsec_common.mk

all: $(BUILD_PATH)/../$(NAME).$(OBJ_EXT)

$(BUILD_PATH)/../$(NAME).$(OBJ_EXT): $(LLS)
	$(LD) $(LDRELOC) $^ -o $@

