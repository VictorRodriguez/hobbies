# -------------------------------------------------
# Compiler
# -------------------------------------------------
CC = gcc

# -------------------------------------------------
# Flags
# -------------------------------------------------
CFLAGS  = -g -O2 -Wall -fno-tree-vectorize

CFLAGS_O = -g -O3 -march=native -funroll-loops \
           -ftree-vectorize -ffast-math \
           -ftree-vectorizer-verbose=2

# -------------------------------------------------
# Target
# -------------------------------------------------
TARGET = synthetic_char

all: $(TARGET) synthetic_char_o

$(TARGET): synthetic_char.c
	$(CC) $(CFLAGS) $< -o $@

synthetic_char_o: synthetic_char.c
	$(CC) $(CFLAGS_O) $< -o $@

clean:
	rm -f $(TARGET) synthetic_char_o
