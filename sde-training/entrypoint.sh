#!/bin/sh

# Default argument
DEFAULT_ARG=100

# Use the provided argument or the default
ARG=${1:-$DEFAULT_ARG}

# Run the binary with the argument
exec ./fft_stress "$ARG"

