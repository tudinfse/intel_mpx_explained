# Clang constants

# object file extension
OBJ_EXT := o

# == make constants
# CLANG_PATH is defined in local.mk
# but we use = instead of := to make sure that CLANG_PATH can be changed afterwards
CC  = $(CLANG_PATH)/clang
CXX = $(CLANG_PATH)/clang++
LD  := ld
LDRELOC := -r
RANLIB := ranlib

