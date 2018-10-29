import wget
import os
import git
import shutil


def clone_autospec():
    gitrepo="https://github.com/clearlinux/autospec.git"
    local_repo_path='/tmp/autospec'
    if os.path.isdir(local_repo_path):
        shutil.rmtree(local_repo_path)
    git.Repo.clone_from(gitrepo,local_repo_path, depth=1)

def clone_repo(pkg):
    gitrepo = 'http://starlingx-koji.zpn.intel.com/cgit/packages/' + pkg 
    local_repo_path='/tmp/' + pkg
    if os.path.isdir(local_repo_path):
        shutil.rmtree(local_repo_path)
    git.Git("/tmp/").clone(gitrepo)

def check_autospec(pkg):
    local_repo_path='/tmp/' + pkg
    savedpath = os.getcwd()
    os.chdir(local_repo_path)
    cmd = 'python ../autospec/autospec/autospec.py'
    ret = os.system(cmd)
    os.chdir(savedpath)
    return ret

def main():

    data = {}
    pkgs = []

    filename='/tmp/stx_pkg.log'
    outputfile='/tmp/output.csv'
    url='http://starlingx-koji.zpn.intel.com/misc/projects.list'

    if os.path.isfile(filename):
        pass
    else:
        filename = wget.download(url=url,out=filename)

    if os.path.isfile(outputfile):
        os.remove(outputfile)

    if os.path.isfile(filename):
        with open(filename) as f:
            lines = f.readlines()
            for line in lines:
                if 'packages' in line and 'common' not in line \
                        and 'projects' not in line:
                    pkg = line.split("/")[1].strip()
                    pkg = pkg.replace(".git","")
                    pkgs.append(pkg)

    print("Cloning autospec")
    clone_autospec()

    for pkg in pkgs:
        print("Clonning: " + pkg)
        clone_repo(pkg)
        if check_autospec(pkg):
            print(pkg + " Fail")
            print(pkg + ",Fail", file=open(outputfile,"a"))
            data[pkg] = "Fail"
        else:
            print(pkg + "Pass")
            print(pkg + ",Pass", file=open(outputfile,"a"))
            data[pkg] = "Pass"

    print(data)

if __name__ == '__main__':
    main()
