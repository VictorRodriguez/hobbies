# Compiler and flags
CC       = gcc -g
CFLAGS   = -O0 -Wall -I../
OPTFLAGS = -O3 -funroll-loops -fpeel-loops -funswitch-loops
AVXFLAGS = -Ofast -march=native -mavx2 -funroll-loops -ffast-math
LDFLAGS  = -lm

# Targets
SRC         = unroll.c
TARGET      = unroll
OPT_TARGET  = unroll_opt
FAST_TARGET = unroll_fast_avx

# Default rule: build non-optimized version
all: $(TARGET)

# Non-optimized build
$(TARGET): $(SRC)
	$(CC) $(CFLAGS) $(SRC) -o $(TARGET) $(LDFLAGS)

# Optimized (unrolled) build
opt: $(SRC)
	$(CC) $(OPTFLAGS) $(SRC) -o $(OPT_TARGET) $(LDFLAGS)

# Fast AVX2 build (uses YMM, aggressive optimization)
fast_avx: $(SRC)
	$(CC) $(AVXFLAGS) $(SRC) -o $(FAST_TARGET) $(LDFLAGS)

# Clean build artifacts
clean:
	rm -f $(TARGET) $(OPT_TARGET) $(FAST_TARGET)

# Run all versions for comparison
run: all opt fast_avx
	@echo "\n--- Running Non-Optimized Version ---"
	@./$(TARGET)
	@echo "\n--- Running Optimized Unrolled Version ---"
	@./$(OPT_TARGET)
	@echo "\n--- Running Fast AVX (YMM) Version ---"
	@./$(FAST_TARGET)

.PHONY: all clean run opt fast_avx

