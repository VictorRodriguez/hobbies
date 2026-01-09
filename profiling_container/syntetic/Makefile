# -------------------------------------------------
# Compiler
# -------------------------------------------------
CC = gcc

# -------------------------------------------------
# Sniper root (must be exported in your environment)
# -------------------------------------------------
export SNIPER_ROOT=/home/centos/intelwps-internal-conf-25.12-2025-12-08-lin/

SNIPER_INC = $(SNIPER_ROOT)/include
SNIPER_LIB = $(SNIPER_ROOT)/lib

# -------------------------------------------------
# Flags
# -------------------------------------------------
CFLAGS  = -O2 -Wall -fno-tree-vectorize -DENABLE_SNIPER \
          -I$(SNIPER_INC)

LDFLAGS = -L$(SNIPER_LIB) -lsim_api

# -------------------------------------------------
# Target
# -------------------------------------------------
TARGET = synthetic_char

all: $(TARGET)

$(TARGET): synthetic_char.c
	$(CC) $(CFLAGS) $< -o $@ $(LDFLAGS)

clean:
	rm -f $(TARGET)

