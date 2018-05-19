import subprocess
import argparse


def analyse_avx(line):
    if "ymm" in line:
        print("ymm registers = OK")
        return True
    if "xmm" in line:
        print("xmm registers = OK")
        return True

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    parser.add_argument("filename", help = "The filename to inspect")
    args = parser.parse_args()

    filename = args.filename
    out, err = subprocess.Popen(["objdump","-d", filename], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    alllines = out.decode("latin-1")
    lines =  alllines.split("\n")
    
    for line in lines:
        if args.verbose:
            print(line)
        if analyse_avx(line):
            print("System already build for AVX")
            break

if __name__ == '__main__':
    main()

