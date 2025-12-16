# Makefile for synthetic latency microbenchmarks (Sniper-friendly)
# Focus: preserve load-to-use dependencies and control MLP

CC      ?= gcc
CFLAGS_COMMON = -Wall -Wextra -std=c11

# ------------------------------------------------------------
# 1. Strict latency calibration (MLP = 1, no hiding)
# ------------------------------------------------------------
CFLAGS_LATENCY = \
	-O2 \
	-fno-unroll-loops \
	-fno-peel-loops \
	-fno-tree-vectorize \
	-fno-prefetch-loop-arrays \
	-fno-builtin \
	-march=x86-64

# ------------------------------------------------------------
# 2. Ultra-clean (even fewer transformations, easier CPI fitting)
# ------------------------------------------------------------
CFLAGS_CLEAN = \
	-O1 \
	-fno-unroll-loops \
	-fno-tree-vectorize \
	-fno-prefetch-loop-arrays \
	-fno-inline \
	-fno-builtin

# ------------------------------------------------------------
# 3. Controlled MLP experiment (intentional latency hiding)
# ------------------------------------------------------------
CFLAGS_MLP = \
	-O2 \
	-funroll-loops \
	-fno-tree-vectorize \
	-fno-prefetch-loop-arrays \
	-fno-builtin \
	-march=x86-64

# ------------------------------------------------------------
# Targets
# ------------------------------------------------------------

SRC = latency_test.c

all: latency_strict latency_clean latency_mlp

latency_strict: $(SRC)
	$(CC) $(CFLAGS_COMMON) $(CFLAGS_LATENCY) $< -o $@

latency_clean: $(SRC)
	$(CC) $(CFLAGS_COMMON) $(CFLAGS_CLEAN) $< -o $@

latency_mlp: $(SRC)
	$(CC) $(CFLAGS_COMMON) $(CFLAGS_MLP) $< -o $@

# ------------------------------------------------------------
# Assembly inspection (sanity check)
# ------------------------------------------------------------
asm: $(SRC)
	$(CC) $(CFLAGS_COMMON) $(CFLAGS_LATENCY) -S $< -o latency_test.s

# ------------------------------------------------------------
# Utility
# ------------------------------------------------------------
clean:
	rm -f latency_strict latency_clean latency_mlp latency_test.s

.PHONY: all clean asm

