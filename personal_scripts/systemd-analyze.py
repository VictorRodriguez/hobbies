#!/usr/bin/python3
import subprocess

out, err = subprocess.Popen(["systemd-analyze"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
alllines = out.decode("latin-1")
lines =  alllines.split("\n")

kernel_time =0
userspace_time = 0

count = 0
for line in lines:
    if "kernel" in line and "userspace" in line:
        for item in (line.split(" ")):
            if "kernel" in item:
                kernel_time = (line.split(" ")[count-1]).replace("s","")
            if "userspace" in item:
                userspace_time = (line.split(" ")[count-1]).replace("s","")
            count+=1

total_time = 0

total_time = float(kernel_time) + float(userspace_time)

print("kernel_time : " + kernel_time + " sec")
print("userspace_time: " + userspace_time + " sec")
print("total_time: " + str(total_time) + " sec")
