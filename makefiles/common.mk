###############################
# Common functionality:
# - variables and default values
# - targets
# - helper functions
###############################

# check that required variables are specified
ifndef PROJ_ROOT
$(error PROJ_ROOT is not specified)
endif

ifndef BUILD_TYPE
$(error BUILD_TYPE is not specified)
endif

ifndef NAME
$(error NAME is not specified)
endif

# ======== Main variables ========
# directories
ifndef BUILD_ROOT
BUILD_ROOT = $(PROJ_ROOT)/build
endif

ifndef BUILD_PATH
BUILD_PATH = $(BUILD_ROOT)/$(BENCH_SUITE)/$(NAME)/$(BUILD_TYPE)
endif

TYPE_MAKEFILE = Makefile.$(BUILD_TYPE)

# build flags
CCFLAGS += -O3

ifdef DEBUG
    CCFLAGS += -ggdb
else
    CCFLAGS += -DNODPRINTF -DNDEBUG
endif

ifdef VERBOSE
    CONFIG_SCRIPT_LOG := /dev/stdout
else
    CONFIG_SCRIPT_LOG := /dev/null 2>&1
    MAKE += -s
endif

# programs
M4 := m4

# ======== LIBS ========
# sources to be linked together and processed by custom passes (makes sense only for Clang/LLVM)
LLS = $(addprefix $(BUILD_PATH)/, $(addsuffix .$(OBJ_EXT), $(SRC)))

# included directories
INCLUDE_HEADER_DIRS = $(addprefix -I,$(INC_DIR))
INCLUDE_LIB_DIRS = $(addprefix -L,$(LIB_DIRS))


# ============= OS ================
OS = -D_LINUX_
ARCHTYPE = $(shell uname -p)

ifeq ($(shell uname -m),x86_64)
ARCH = -D__x86_64__
endif

CCFLAGS += $(OS) $(ARCH)

# ======== Common build targets ========
.PHONY: all clean make_dirs

all: make_dirs

make_dirs:
	-mkdir -p $(BUILD_PATH)
	@echo "" > $(BUILD_PATH)/.need_cxx

clean:
	rm -rf $(BUILD_PATH)

# ======== File-type-specific build targets ========
# headers
%.h: %.H
	$(M4) $(M4FLAGS) $(MACROS) $^ > $(BUILD_PATH)/$@

# object files
$(BUILD_PATH)/%.$(OBJ_EXT): %.c
	$(CC) $(CCFLAGS) $(CFLAGS) -c $< -o $@ $(INCLUDE_HEADER_DIRS)

$(BUILD_PATH)/%.$(OBJ_EXT): %.C
	$(CC) $(CCFLAGS) $(CFLAGS) -c $< -o $@ $(INCLUDE_HEADER_DIRS)

$(BUILD_PATH)/%.$(OBJ_EXT): %.cpp
	$(CXX) $(CCFLAGS) $(CXXFLAGS) -c $< -o $@ $(INCLUDE_HEADER_DIRS)

$(BUILD_PATH)/%.$(OBJ_EXT): %.cxx
	$(CXX) $(CCFLAGS) $(CXXFLAGS) -c $< -o $@ $(INCLUDE_HEADER_DIRS)

$(BUILD_PATH)/%.$(OBJ_EXT): %.cc
	$(CXX) $(CCFLAGS) $(CXXFLAGS) -c $< -o $@ $(INCLUDE_HEADER_DIRS)

# executable
$(BUILD_PATH)/$(NAME): $(LLS)
	$(CXX) $(CCFLAGS) $(CXXFLAGS) -o $@ $^ $(INCLUDE_HEADER_DIRS) $(INCLUDE_LIB_DIRS) $(LIBS)


# ======== Helper functions ========
# $(eval $(call expand-ccflags))
define expand-ccflags
	CFLAGS += $(CCFLAGS)
	CXXFLAGS += $(CCFLAGS)
	export
endef

