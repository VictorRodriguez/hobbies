import os

pkg_name = "krita"
filepath = 'krita/krita.spec'
repo_path = "/etc/my_yumrepo"
log_file = "/tmp/log"
build_requirements = []
pkgs_affected = []

with open(filepath) as fp:
    line = fp.readline()
    while line:
       if "BuildRequires" in line:
           build_requirements.append((line.split(":")[1].strip()))
       line = fp.readline()

for r, d, f in os.walk(repo_path):
    for file_name in f:
        if '.rpm' in file_name:
            file_name_path = os.path.join(repo_path,file_name)
            cmd = "rpm -qp %s --requires > %s" % (file_name_path,log_file)
            os.system(cmd)
            with open(log_file) as fp:
                line = fp.readline()
                while line:
                    if pkg_name in line:
                        pkgs_affected.append(file_name)
                    line = fp.readline()

if build_requirements:
    print("The build requirements of package: %s are:\n" % (pkg_name))
    for req in build_requirements:
        print(req)
if pkgs_affected:
    print("By rebuilding package: %s you might need to rebuild these ones:" % (pkg_name))
    for pkg in pkgs_affected:
        print(pkg)
