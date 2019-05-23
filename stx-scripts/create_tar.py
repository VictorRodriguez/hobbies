import os
import subprocess

fname = 'repos'

with open(fname) as f:
    content = f.readlines()

for line in content:
    line = line.strip()
    directory = line.split("/")[-1]
    if (not os.path.isdir(directory)):
        cmd = "git clone --depth 1 " + line
        os.system(cmd)

dirs = []

proc = subprocess.Popen(['find','.','-d','-name','centos'],stdout=subprocess.PIPE)
while True:
    line = proc.stdout.readline()
    if line != '':
        dir_path =  line.rstrip().replace("centos","")
        dirs.append(dir_path)
        for item in os.listdir(dir_path):
            if os.path.isdir(os.path.join(dir_path, item)):
                if "centos" not in item:
                    print(os.path.join(dir_path, item))
    else:
        break

