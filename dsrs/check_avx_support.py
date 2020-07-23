#!/usr/bin/env python
import os
import subprocess

def find_libraries(root_path):
    libraries = []
    for root, dirs, files in os.walk(root_path, topdown=True):
        for name in files:
            if ".so" in name:
                library = os.path.join(root, name)
                libraries.append(library)
    return libraries

def check_avx(library,registry_kind):
    cmd = "objdump -d %s | grep %s | wc -l" % (library, registry_kind)
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    output = p.stdout.read()
    if str(output).strip() != 0:
        return True
    else:
        return False

def main():
    root_path = "/usr/lib64/haswell"
    avx2_libraries = []
    avx512_libraries = []
    libraries = find_libraries(root_path)
    for library in libraries:
        if check_avx(library, "ymm"):
            avx2_libraries.append(library)
        if check_avx(library, "zmm"):
            avx512_libraries.append(library)

    print(avx2_libraries)
    print(avx512_libraries)

if __name__ == "__main__":
    main()

