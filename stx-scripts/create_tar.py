import os
import subprocess
import re


fname = 'repos'

def grep(file_path,word):
    FILE = open(file_path, "r")
    for line in FILE:
        if re.search(word, line):
            return line
    return None

def clone_repos():
    with open(fname) as f:
        content = f.readlines()
    for line in content:
        line = line.strip()
        directory = line.split("/")[-1]
        if (not os.path.isdir(directory)):
            cmd = "git clone --depth 1 " + line
            os.system(cmd)


def find_pkgs_to_build(patern):

    proc = subprocess.Popen(['find','.','-d','-name',patern]
        ,stdout=subprocess.PIPE)

    pkg_info_files = []

    line = proc.stdout.readline()
    while line != '':
        line = proc.stdout.readline().strip()
        pkg_info_files.append(line)

    return pkg_info_files

def main():
    clone_repos()
    pkg_info_files = find_pkgs_to_build("PKG-INFO")
    pkg_info_files = filter(None, pkg_info_files)
    for item in pkg_info_files:
        pkg_info = {}
        pkg_info["pkg_info_path"] = item
        if (grep(item,"Name")):
            pkg_info["pkg_name"] = pkg_name = grep(item,"Name").\
                split(":")[1].strip()

        if (grep(item,"Version")):
            pkg_info["pkg_version"] = pkg_name = grep(item,"Version").\
                split(":")[1].strip()
if __name__== "__main__":
    main()

