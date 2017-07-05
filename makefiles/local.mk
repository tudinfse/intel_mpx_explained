# path to native clang/llvm build with executables
CLANG_PATH := ${BIN_PATH}/llvm/build/bin

# Gold plugin
GOLD_PATH := ${BIN_PATH}/binutils_gold/install

# SouftBound directories
CLANG_SOFTBOUND_PATH := ${BIN_PATH}/softboundcets/build/llvm/Release+Asserts/bin
SOFTBOUND_RUNTIME_PATH := ${BIN_PATH}/softboundcets/src/softboundcets-lib/lto

# SAFECode directories
CLANG_SAFECODE_PATH := ${GOLD_PATH}/bin/

# path to sgx-musl repository
SGXMUSL_PATH := $(HOME)/code/sgx/sgx-musl

