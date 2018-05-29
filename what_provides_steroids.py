import os
import subprocess


exe = 'libwebp.so'

count = 0 
for root, dirs, files in os.walk(r'/usr/'):
    for name in files:
        if name.endswith(exe):
            count+=1
            bin_path = os.path.abspath(os.path.join(root, name))
            print("path of the file with SSE instructions" + bin_path)

if count == 1 :
    out, err = subprocess.Popen(["sudo","dnf", "whatprovides",bin_path],\
            stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    alllines = out.decode("latin-1")
    lines =  alllines.split("\n")
    for line in lines:
        if ".x86_64" in line:
            pkg =(line.strip().split("-"))[0]
    print("Binary is in package = " + pkg)

    fname = "/home/vrodri3/clearlinux/packages/%s/%s.spec" % (pkg,pkg)
    count_hsw = 0
    with open(fname) as f:
        content = f.readlines()
        for line in content:
            if "haswell" in line:
                count_hsw +=1
    if count_hsw:
        print("PKG already has AVX2 support:    OK!")
    else:
        print("PKG already has AVX2 support:    FAIL!")
