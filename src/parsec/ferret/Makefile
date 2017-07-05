NAME := ferret
SRC := ferret-serial arena assign bench bitmap cass cass_dist cass_reg cuckoo_hash dataset dist emd env error \
       hash hash_table heap import map matrix raw stat table timer topk tp  util edge extract image srm \
       local LSH LSH_query_batch LSH_query perturb recall

VPATH := src

INC_DIR += $(PROJ_ROOT)/src/parsec/ferret/src/include
CCFLAGS += -Wno-int-conversion -Wno-incompatible-pointer-types -Wno-implicit-function-declaration -Wno-int-to-pointer-cast

LIB_DIRS += $(PROJ_ROOT)/build/libs/gsl/$(BUILD_TYPE)/lib \
			$(PROJ_ROOT)/build/libs/libjpeg/$(BUILD_TYPE)/lib
LIBS += -lrt -lm -lgsl -lgslcblas -ljpeg

ifneq ($(strip $(NUM_THREADS)),1)
    SRC := $(filter-out ferret-serial,$(SRC))
    SRC += ferret-pthreads tpool queue
endif

include Makefile.$(BUILD_TYPE)
include ../parsec_common.mk

.PHONY: buildlibs

all:
	@${MAKE} buildlibs
	@${MAKE} $(BUILD_PATH)/$(NAME)

buildlibs: export BENCH_SUITE=libs

buildlibs:
	$(MAKE) BUILD_TYPE=$(BUILD_TYPE) -I $(PROJ_ROOT)/makefiles -C $(PROJ_ROOT)/src/$(BENCH_SUITE)/gsl
	$(MAKE) BUILD_TYPE=$(BUILD_TYPE) -I $(PROJ_ROOT)/makefiles -C $(PROJ_ROOT)/src/$(BENCH_SUITE)/libjpeg

