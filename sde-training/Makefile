CC ?= gcc

TARGET := fftw_fft_stress
SRC := fftw_fft_stress.c

# FFTW install prefix (your local build)
FFTW_ROOT ?= $(HOME)/fftw-avx512

# IWPS / Sniper root
SNIPER_ROOT ?= /home/centos/intelwps-internal-conf-25.12-2025-12-08-lin

# FFTW include/lib
FFTW_INCS := -I$(FFTW_ROOT)/include
FFTW_LIBS := -L$(FFTW_ROOT)/lib -lfftw3 -lm -lpthread
FFTW_RPATH := -Wl,-rpath,$(FFTW_ROOT)/lib

# Sniper include/lib
SNIPER_INCS := -I$(SNIPER_ROOT)/include
SNIPER_LIBS := -L$(SNIPER_ROOT)/lib -lsim_api
SNIPER_RPATH := -Wl,-rpath,$(SNIPER_ROOT)/lib

CFLAGS_BASE := -O3 -ffast-math -fno-math-errno

.PHONY: all avx2_sniper avx512_sniper avx2 avx512 clean

all: avx2_sniper avx512_sniper

# --- Sniper ROI builds (what you asked for)
avx2_sniper:
	$(CC) $(CFLAGS_BASE) -DUSE_SNIPER -mavx2 \
	$(SNIPER_INCS) $(FFTW_INCS) \
	$(SRC) \
	$(FFTW_LIBS) $(SNIPER_LIBS) \
	$(FFTW_RPATH) $(SNIPER_RPATH) \
	-o $(TARGET)_avx2_sniper

avx512_sniper:
	$(CC) $(CFLAGS_BASE) -DUSE_SNIPER -march=skylake-avx512 \
	$(SNIPER_INCS) $(FFTW_INCS) \
	$(SRC) \
	$(FFTW_LIBS) $(SNIPER_LIBS) \
	$(FFTW_RPATH) $(SNIPER_RPATH) \
	-o $(TARGET)_avx512_sniper

# --- Optional non-sniper builds
avx2:
	$(CC) $(CFLAGS_BASE) -mavx2 \
	$(FFTW_INCS) $(SRC) $(FFTW_LIBS) $(FFTW_RPATH) \
	-o $(TARGET)_avx2

avx512:
	$(CC) $(CFLAGS_BASE) -march=skylake-avx512 \
	$(FFTW_INCS) $(SRC) $(FFTW_LIBS) $(FFTW_RPATH) \
	-o $(TARGET)_avx512

clean:
	rm -f $(TARGET)_*

