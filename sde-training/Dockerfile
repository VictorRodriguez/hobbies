# Use a Debian-based image that includes glibc
FROM debian:latest

# Set the working directory inside the container
WORKDIR /app

# Copy the binary into the container
COPY fft_stress .

# Ensure the binary has execute permissions
RUN chmod +x fft_stress

# Copy the entrypoint script into the container
COPY entrypoint.sh .

# Ensure the entrypoint script has execute permissions
RUN chmod +x entrypoint.sh

# Use the entrypoint script to run the binary
ENTRYPOINT ["./entrypoint.sh"]

