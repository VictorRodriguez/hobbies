import os 
import argparse
import re

log_file = "/tmp/log"
libraries = []
binaries = []

def add_binary(binary):
    if os.path.isfile(binary):
        if binary not in binaries:
            binaries.append(binary)

def add_lib(lib):
    if os.path.isfile(lib):
        if lib not in libraries:
            libraries.append(lib)

def whatprovides(file_name):

    cmd = "sudo dnf-3 --releasever=clear "
    cmd = cmd + " --config=/home/clearlinux/projects/common-internal/conf/dnf.conf provides "
    cmd = cmd + file_name
    os.system(cmd)


def analize():
    if os.path.isfile(log_file):
        with open(log_file) as f:
            content = f.readlines()
            for line in content:
                if "openat" in line or "access" in line:
                    if "/usr/lib" in line:
                        m = re.search('<(.+?)>', line)
                        if m:
                            lib = m.group(1)
                            add_lib(lib)
                    if "/usr/bin" in line:
                        m = re.search('/usr/bin/(.+?)"',line)
                        if m:
                            binary = "/usr/bin/" + m.group(1)
                            add_binary(binary)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--run', dest='run_mode', action='store_true')
    parser.add_argument('--analize', dest='analize_mode', action='store_true')
    args = parser.parse_args()

    if args.run_mode:
        if os.path.isfile(log_file):
            os.remove(log_file)
        os.environ['EXECUTE_BINARY_PREPEND'] = "strace -o /tmp/log"

        benchmark="pts/pybench"
        cmd = "phoronix-test-suite batch-run " + benchmark
        os.system(cmd)
        
        analize()

    if args.analize_mode:
        analize()

        for lib in libraries:
            print(lib)
            whatprovides(lib)

        for binary in binaries:
            print(binary)
            whatprovides(binary)
if __name__ == "__main__":
    main()
