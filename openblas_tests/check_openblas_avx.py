#!/usr/bin/env python3

import os
import subprocess

def build_cblastest():
    cmd = "gcc cblas_ddot.c -o cblas_ddot -lopenblas"
    ret = os.system(cmd)
    return not ret

def find_avx_cblas_lib():
    cmd = "ldd ./cblas_ddot | grep blas | grep avx"
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    output = p.stdout.read()
    if str(output).strip() != 0:
        return True
    else:
        return False

def main():
    if build_cblastest():
        if find_avx_cblas_lib():
            print("PASS")
        else:
            print("FAIL")

if __name__ == "__main__":
    main()
