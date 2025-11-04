# Compiler and flags
CC = gcc
CFLAGS = -O0 -Wall -I../          # -I../ adds include path for headers in parent dir
OPTFLAGS = -O3 -funroll-loops -fpeel-loops -funswitch-loops
LDFLAGS = -lm                     # Link math library for sin, cos, log, etc.

# Targets
SRC = unroll.c
TARGET = unroll
OPT_TARGET = unroll_opt

# Default rule: build non-optimized version
all: $(TARGET)

# Non-optimized build
$(TARGET): $(SRC)
	$(CC) $(CFLAGS) $(SRC) -o $(TARGET) $(LDFLAGS)

# Optimized (unrolled) build
opt: $(SRC)
	$(CC) $(OPTFLAGS) $(SRC) -o $(OPT_TARGET) $(LDFLAGS)

# Clean build artifacts
clean:
	rm -f $(TARGET) $(OPT_TARGET)

# Run both versions for comparison
run: all opt
	@echo "\n--- Running Non-Optimized Version ---"
	@./$(TARGET)
	@echo "\n--- Running Optimized Version ---"
	@./$(OPT_TARGET)

.PHONY: all clean run opt

