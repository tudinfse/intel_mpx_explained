ifndef PIN_ROOT
$(error specify PIN_ROOT to point to the PIN kit root directory)
endif

override PIN_ROOT := $(PIN_ROOT)
CONFIG_ROOT := $(PIN_ROOT)/source/tools/Config

include $(CONFIG_ROOT)/makefile.config
include Makefile.rules
include $(TOOLS_ROOT)/Config/makefile.default.rules
