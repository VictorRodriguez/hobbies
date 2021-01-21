#!/bin/bash
while :; do
  # Get the first line with aggregate of all CPUs
  cpu_now=($(head -n1 /proc/stat))
  # Get all columns but skip the first (which is the "cpu" string)
  cpu_sum="${cpu_now[@]:1}"
  # Replace the column seperator (space) with +
  cpu_sum=$((${cpu_sum// /+}))
  # Get the delta between two reads
  cpu_delta=$((cpu_sum - cpu_last_sum))
  # Get the idle time Delta
  cpu_idle=$((cpu_now[4]- cpu_last[4]))
  # Calc time spent working
  cpu_used=$((cpu_delta - cpu_idle))
  # Calc percentage
  cpu_usage=$((100 * cpu_used / cpu_delta))

  # Keep this as last for our next read
  cpu_last=("${cpu_now[@]}")
  cpu_last_sum=$cpu_sum

  echo "CPU usage at $cpu_usage%"

  # Wait a second before the next read
  sleep 1
done
