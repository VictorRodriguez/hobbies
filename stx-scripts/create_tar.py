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

proc = subprocess.Popen(['find','.','-d','-name','centos'],stdout=subprocess.PIPE)

src_dirs = []
pkg_info_files = []

while True:


    line = proc.stdout.readline()
    if line != '':
        dir_path =  line.rstrip().replace("centos","")
        for item in os.listdir(dir_path):
            if os.path.isdir(os.path.join(dir_path,item)):
                if "centos" not in item:
                    src_dir = os.path.join(dir_path,item)
                    if src_dir in src_dirs:
                        pass
                    else:
                        src_dirs.append(src_dir)
                    #print(src_dir)
        for item in os.listdir(dir_path):
            if os.path.isfile(os.path.join(dir_path, item)):
                if "PKG-INFO" in item:
                    pkg_info_file= os.path.join(dir_path,item)
                    if pkg_info_file in pkg_info_files:
                        pass
                    else:
                        pkg_info_files.append(pkg_info_file)
                    #print(pkg_info_file)
    else:
        break

for item in pkg_info_files:
    print(item)

print()
print()

for item in src_dirs:
    print(item)
