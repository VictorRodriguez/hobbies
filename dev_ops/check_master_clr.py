"""Print HTML report."""
import json
import os
import wget
import shutil
import git
from jinja2 import Environment, FileSystemLoader

def print_html_doc(dictionary_data):
    """Generate the html index."""
    THIS_DIR = os.path.dirname(os.path.abspath(__file__))
    j2_env = Environment(loader=FileSystemLoader(THIS_DIR),
                         trim_blocks=True)
    print(j2_env.get_template('test_template.html').
          render(data=dictionary_data),
          file=open("index.html", "w"))

def get_clr_status(pkg):

    local_repo_path='/tmp/' + pkg
    if os.path.isdir(local_repo_path):
        shutil.rmtree(local_repo_path)
    gitrepo = 'http://starlingx-koji.zpn.intel.com/cgit/packages/' + pkg 
    git.Git("/tmp/").clone(gitrepo)
    savedpath = os.getcwd()
    os.chdir(local_repo_path)
    os.system('git remote rm origin')
    os.system('git remote add origin git://kojiclear.jf.intel.com/packages/'+pkg)
    ret = os.system('git fetch')
    os.chdir(savedpath)
    return ret


def get_build_status():
    return True
def get_qa_status():
    return True
def get_last_commit():
    return True

def add_pkg(data,pkg,clr_status,build_status,qa_status,last_commit):
    
    data[pkg] = []
    data[pkg].append({
        'clr_status':str(clr_status),
        'build_status':str(build_status),
        'qa_status':str(qa_status),
        'last_commit':str(last_commit)
        })
    return data

def main():

    data = {}
    pkgs = []

    filename='/tmp/stx_pkg.log'
    url='http://starlingx-koji.zpn.intel.com/misc/projects.list'
    filename = wget.download(url=url,out=filename)
    with open(filename) as f:
        lines = f.readlines()
        for line in lines:
            if 'packages' in line and 'common' not in line:
                pkgs.append(line.split("/")[1].split(".")[0].strip())

    for pkg in pkgs:
        clr_status = get_clr_status(pkg)


if __name__ == '__main__':
    main()
