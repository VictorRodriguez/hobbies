CC ?= gcc

TARGET := gemm_stress
SRC := gemm_stress.c

SNIPER_ROOT ?= /home/centos/intelwps-internal-conf-25.12-2025-12-08-lin

CFLAGS_BASE := -O3 -static -pipe -fno-plt -fno-math-errno -fno-trapping-math -ffast-math \
               -fomit-frame-pointer -Wall -Wextra -Wno-unused-function -static

SNIPER_INC   := -I$(SNIPER_ROOT)/include
SNIPER_LIB   := -L$(SNIPER_ROOT)/lib -lsim_api
SNIPER_RPATH := -Wl,-rpath,$(SNIPER_ROOT)/lib

.PHONY: all avx2_sniper avx512_sniper avx2 avx512 clean

all: avx2_sniper avx512_sniper

avx2_sniper:
	$(CC) $(CFLAGS_BASE) -DUSE_SNIPER -mavx2 -mfma \
	$(SNIPER_INC) $(SRC) \
	$(SNIPER_LIB) $(SNIPER_RPATH) \
	-o $(TARGET)_avx2_sniper

avx512_sniper:
	$(CC) $(CFLAGS_BASE) -DUSE_SNIPER -march=skylake-avx512 -mfma \
	$(SNIPER_INC) $(SRC) \
	$(SNIPER_LIB) $(SNIPER_RPATH) \
	-o $(TARGET)_avx512_sniper

# Optional non-sniper builds
avx2:
	$(CC) $(CFLAGS_BASE) -mavx2 -mfma $(SRC) -o $(TARGET)_avx2

avx512:
	$(CC) $(CFLAGS_BASE) -march=skylake-avx512 -mfma $(SRC) -o $(TARGET)_avx512

clean:
	rm -f $(TARGET)_*

