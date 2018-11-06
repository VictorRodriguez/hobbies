import wget
import os
import git
import shutil

logs_directory = os.path.join(os.getcwd(), 'logs')

def clone_autospec():
    gitrepo="https://github.com/clearlinux/autospec.git"
    local_repo_path='/tmp/clearlinux/projects/autospec'
    if os.path.isdir(local_repo_path):
        shutil.rmtree(local_repo_path)
    git.Repo.clone_from(gitrepo,local_repo_path, depth=1)

def clone_repo(pkg):
    gitrepo = 'http://starlingx-koji.zpn.intel.com/cgit/packages/' + pkg 
    local_repo_path='./clearlinux/packages/' + pkg
    if os.path.isdir(local_repo_path):
        savedpath = os.getcwd()
        os.chdir(local_repo_path)
        cmd = "git fetch origin & git reset --hard origin/master & git pull"
        ret = os.system(cmd)
        os.chdir(savedpath)
        if ret:
            shutil.rmtree(local_repo_path)
            git.Git(local_repo_path).clone(gitrepo)
    else:
        try:
            git.Git(local_repo_path).clone(gitrepo)
            return True
        except:
            print("clone fail !!!!")
            return False


def check_autospec(pkg):
    data = {}
    local_repo_path='./clearlinux/packages/' + pkg
    savedpath = os.getcwd()

    if not os.path.isdir(local_repo_path):
        return -1,"N/A"

    os.chdir(local_repo_path)
    cmd = 'git show --name-only &> /tmp/log'
    os.system(cmd)
    with open('/tmp/log') as f:
        content = f.readlines()
        for line in content:
            if "Author" in line:
                author =  line.strip()
    cmd = 'make autospec &> %s/%s-build.log' % (logs_directory,pkg)
    print("Building %s ..." % (pkg))
    ret = os.system(cmd)
    
    
    os.chdir(savedpath)
    return ret,author

def main():

    pkgs = []

    filename='stx_pkg.log'
    outputfile='output.csv'
    url='http://starlingx-koji.zpn.intel.com/misc/projects.list'

    if os.path.isfile(filename):
        pass
    else:
        filename = wget.download(url=url,out=filename)

    if os.path.isfile(outputfile):
        os.remove(outputfile)

    clone_flag = False
    if os.path.isfile('clone_flag'):
        clone_flag = True

    if not os.path.exists(logs_directory):
        os.makedirs(logs_directory)

    if not os.path.isdir('./clearlinux/projects/common-internal'):
        print("ERROR, please run user-setup.sh to set up a clear dev system")
        return -1

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
        if clone_flag:
            print("Clonning: " + pkg)
            clone_repo(pkg)
        else:
            ret,author = check_autospec(pkg)
            if ret:
                print(pkg + "   Fail")
                print(pkg + ",Fail," + author, file=open(outputfile,"a"))
            else:
                print(pkg + "   Pass")
                print(pkg + ",Pass," + author, file=open(outputfile,"a"))

if __name__ == '__main__':
    main()
