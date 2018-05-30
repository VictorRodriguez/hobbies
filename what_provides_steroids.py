import os
import subprocess

binary_list = []

binary_list.append("libwebp.so")
binary_list.append("libvulkan_radeon.so")
binary_list.append("libclangARCMigrate.so")
binary_list.append("librsvg-2.so")
binary_list.append("librustc_save_analysis-d3fb0e87c4a6833f.so")
binary_list.append("libclangStaticAnalyzerCheckers.so")
binary_list.append("libclangAST.so")
binary_list.append("libLLVMX86CodeGen.so")
binary_list.append("libLLVMCodeGen.so")
binary_list.append("librustc_reso")
binary_list.append("libm-2.27.so")
binary_list.append("librustc_driver-3163d9fca1cf728b.so")
binary_list.append("libQt5Gui.so")
binary_list.append("libmozjs-52.so")
binary_list.append("libvulkan_intel.so")
binary_list.append("librustc_typeck-7c1d49c584f4b735.so")
binary_list.append("libLLVMSelectionDAG.so")
binary_list.append("librustc_metadata-8671c18130c60598.so")
binary_list.append("libclangCodeGen.so")
binary_list.append("libz3.so")
binary_list.append("libclangSema.so")
binary_list.append("libopencv_calib3d.so")
binary_list.append("libpixman-1.so")
binary_list.append("libopencv_core.so")
binary_list.append("librustc_mir-8f021bbd0465cbb0.so")
binary_list.append("libXvMCnouveau.so")
binary_list.append("libXvMCr600.so")
binary_list.append("libgfortran.so")
binary_list.append("libopencv_imgproc.so")
binary_list.append("libsyntax-a0f8084e7d2e8f23.so")
binary_list.append("libswrAVX2.so")
binary_list.append("libfftw3.so")
binary_list.append("libswrAVX.so")
binary_list.append("libOSMesa.so")
binary_list.append("libfftw3f.so")
binary_list.append("librustc-276311b1d0544da9.so")
binary_list.append("libopenblas_nehalemp-r0.3.0.dev.so")
binary_list.append("libopenblas.so")

for binary in binary_list:
    count = 0 
    for root, dirs, files in os.walk(r'/usr/'):
        for name in files:
            if name.endswith(binary):
                count+=1
                bin_path = os.path.abspath(os.path.join(root, name))
                print("path of the file with SSE instructions : " + bin_path)

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
