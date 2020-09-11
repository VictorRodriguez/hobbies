# Optimized Python Docker image based Centos/Ubuntu OS

These are Docker images based on Ubuntu and CentOS that compile and install an optimized python 3.8 ready to use:
 
## Features and scalability
 
They are based on Ubuntu and CentOS plus:
* Clear Linux patches to implement Intel® Advanced Vector Extensions compiler flags for distutils and math library
* Compiler flags to build CPython code
* The distutils package provides the end user with a vast list of Python libraries for multiple development tools, some of which allow users to build and install additional modules into a Python installation. To build Python libraries for packages that use the upstream Python provided distutils optimized for x86-64 systems, the Clear Linux team modified the distutils tool scripts with the following patch: 
* This part of the patch builds two more versions of the Python libraries using these flags:

  * -march=haswell
  * -march=skylake-avx512
 
With this patch each library compiled on this docker image with these flags ends with the suffix .avx2 and .avx512 respectively. They are installed in the /usr/lib/python3.7/site-packages/ directory as the pandas library file as follows: 
 
```
pandas/_libs/skiplist.cpython-37m-x86_64-linux-gnu.so.avx2
```

In addition, we added support for dynamic loading of extension modules. This is done with a hack on the file dynload_shlib.c. This change enables dynamic loading of extension modules based on the platform where our Python module is running. More information about this on Clear Linux documentation
 
## Performance optimizations
 
The performance boost could go form 2x up to 30% in some benchmarks in comparison to python provided by base Ubuntu and CentOS images.
These images provides libraries with avx2 and avx512 instructions :
 
```
# objdump -d /build/lib/python3.8/lib-dynload/_sha256.cpython-38-x86_64-linux-gnu.so.avx512 | grep zmm
    13d1:   62 f1 fd 48 6f 4c 24    vmovdqa64 0x40(%rsp),%zmm1
    13d9:   62 f2 75 48 00 05 5d    vpshufb 0x3f5d(%rip),%zmm1,%zmm0 
    13e3:   62 f1 fd 48 7f 44 24    vmovdqa64 %zmm0,0x40(%rsp)
 
root@8f7fd5f2497a:/Python-3.8.3# objdump -d /build/lib/python3.8/lib-dynload/_sha256.cpython-38-x86_64-linux-gnu.so.avx2 | grep ymm
    142a:   c5 fd 6f 15 0e 4f 00    vmovdqa 0x4f0e(%rip),%ymm2 
    1452:   c5 fd 6f 64 24 60       vmovdqa 0x60(%rsp),%ymm4
    1458:   c5 fd 6f 5c 24 40       vmovdqa 0x40(%rsp),%ymm3
    145e:   c4 e2 5d 00 ea          vpshufb %ymm2,%ymm4,%ymm5
    1463:   c4 e2 65 00 c2          vpshufb %ymm2,%ymm3,%ymm0
 ```
 
Multiple external benchmarks has shown that the correct use of AVX technology could boost the performance of numerical applications ( Deep learning, data analytics and other examples ) up to 3X
 
## How to build:
 
```
# make ubuntu
# make centos
```

## TODOs:
 
Do multistage for size reduction
Build GLIBC with CLR optimizations on top of these stacks
Build Open Blas with CLR optimizations on top of these stacks
Build ZLIB with CLR optimizations on top of these stacks
Build NumPy/Panda/Sci-kit learn with CLR optimizations on top of these stacks
