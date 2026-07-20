CC ?= gcc
CFLAGS ?= -O2 -std=c11 -Wall -Wextra -Wpedantic \
          -fno-if-conversion -fno-if-conversion2 \
          -fno-tree-vectorize -fno-unroll-loops \
          -fno-omit-frame-pointer
LDFLAGS ?= -static

TARGET := branch_predictor_stress
SRC := branch_predictor_stress.c

.PHONY: all clean

all: $(TARGET)

$(TARGET): $(SRC)
	$(CC) $(CFLAGS) $(SRC) -o $@ $(LDFLAGS)

clean:
	rm -f $(TARGET)

