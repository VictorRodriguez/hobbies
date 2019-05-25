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

def find_src_to_build(master_path):
    build_srpm_data = "%s/centos/build_srpm.data" % (master_path)
    if os.path.isfile(build_srpm_data):
        if grep(build_srpm_data,"SRC_DIR"):
            src_dir = grep(build_srpm_data,"SRC_DIR").strip().split('=')[1]
            src_dir = src_dir.strip('"')
            if src_dir == ".":
                src_dir = ""
            if "PKG_BASE" in src_dir:
                src_dir = src_dir.split("/")[1]
            if os.path.isdir(master_path + src_dir):
                return (master_path + src_dir)
            else:
                print("ERROR: path does not exist %s" % \
                    os.path.join(master_path + src_dir))
        else:
            print("ERROR: no src dir found in %s" % (master_path))
            return None

def find_tis_version(master_path):
    build_srpm_data = "%s/centos/build_srpm.data" % (master_path)
    if os.path.isfile(build_srpm_data):
        if grep(build_srpm_data,"TIS_PATCH_VER"):
            tis_patch_version = grep(build_srpm_data,"TIS_PATCH_VER").strip()
            tis_patch_version = tis_patch_version.split('=')[1]
            return tis_patch_version
def main():
    clone_repos()
    patern = "PKG-INFO"
    pkg_info_files = find_pkgs_to_build(patern)
    pkg_info_files = filter(None, pkg_info_files)
    for item in pkg_info_files:
        pkg_info = {}
        pkg_info["pkg_info_path"] = item
        pkg_info["pkg_path"] = item.replace(patern,"")
        if (grep(item,"Name")):
            pkg_info["pkg_name"] = pkg_name = grep(item,"Name").\
                split(":")[1].strip()
        if (grep(item,"Version")):
            pkg_info["pkg_version"] = pkg_name = grep(item,"Version").\
                split(":")[1].strip()
        if (find_src_to_build(pkg_info["pkg_path"])):
            pkg_info["pkg_src"] = find_src_to_build(pkg_info["pkg_path"])
        if (find_tis_version(pkg_info["pkg_path"])):
            pkg_info["pkg_tis_version"] = find_tis_version(pkg_info["pkg_path"])

        print(pkg_info)

        # TODO now that we have all the info create the tar ball and mock :)
if __name__== "__main__":
    main()

