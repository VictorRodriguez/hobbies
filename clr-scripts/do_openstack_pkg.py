#!/usr/bin/python3
import sys
import typing
from bs4 import BeautifulSoup
import urllib3
import certifi
import os
import subprocess
import re
from time import sleep

#http = urllib3.PoolManager()
http = urllib3.ProxyManager('http://proxy-server.bla.com:port/', cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())

processed = dict()
recursionlimit = 20

def find_url(package : str) -> str:
    response = http.request("GET", "https://pypi.org/project/" + package + "/#files")
    html = response.data
    soup = BeautifulSoup(html, "lxml")
    for link in soup.findAll("a"):
        target = link.get("href")
        if target != None and package in target and ".tar.gz" in target:
            return target
    for link in soup.findAll("a"):
        target = link.get("href")
        if target != None and package in target and ".zip" in target:
            return target
#        print(link.get("href"))
    return ""

def generate_directory(package : str, url : str) -> None:
    try:
        result = subprocess.run(['rm', '-rf', package])
        result = subprocess.run(['git', 'clone', 'gitolite3@kojiclear.jf.intel.com:packages/'+package])
    except:
        print("GIT failed")

    try:
        os.mkdir(package)
    except:
        print("[info] Directory for package", package, "already exists")


    with open(package+"/Makefile", "w") as f:
        f.write("PKG_NAME := " + package +"\n" +
                "URL = " + url + "\n\n" + "include ../common/Makefile.common")

    with open(package+"/build_pattern", "w") as f:
        f.write("distutils36")

    with open(package+"/buildreq_add", "w") as f:
        f.write("openstack-setuptools")

    return

def run_autospec(package : str):
    result = subprocess.run(['sed', '-i', '-e', 's/verify_required = true/verify_required = false/', 'options.conf'],  cwd = package+"/")
    result = subprocess.run(['make', 'autospec'], cwd = package+"/")
    print("Result is ", result.returncode)
    return result.returncode

def git_push(package : str) -> None:
    result = subprocess.run(['sed', '-i', '-e', 's/autoupdate = false/autoupdate = true/', 'options.conf'],  cwd = package+"/")
    result = subprocess.run(['git', 'commit', 'options.conf', '-m', 'autoupdate'], cwd = package+"/")
    result = subprocess.run(['git', 'push', '-u', 'gitolite3@kojiclear.jf.intel.com:packages/'+package, 'master'], cwd = package+"/")

def koji_add(package : str, sync : int) -> None:
    result = subprocess.run(['koji', 'add-pkg', 'dist-clear', '--owner=avandeve', package], cwd = package+"/")
    if sync == 0:
        result = subprocess.run(['make', 'koji-nowait'], cwd = package+"/")
    else:
        result = subprocess.run(['make', 'koji'], cwd = package+"/")

def do_package(package : str, sync : int, openstack: int) -> None:
    global recursionlimit
    global processed

    clr = package
    print("Processing package", package, "("+ clr+")")

    if package in processed:
        print("Package ", package, "already processed")
        return

    processed[package] = 1
    if recursionlimit < 1:
        return
    recursionlimit = recursionlimit - 1


    # step 1 : check if it is already in packages (if it is, we're done)

    # step 2 : find the CRAN URL
    if "openstack-" in package:
        package = package.replace("openstack-","")
    url = find_url(package)
    if url == "":
        return
    print("Package found at ", url)

    # step 3 : create directory and Makefile
    generate_directory(clr, url)

    # step 4 : run autospec
    if run_autospec(clr) != 0:
        return

    # step 5 : parse build logs and recurse if needed

    # step 6 : finish up (git push & koji)
    git_push(clr)
    # koji_add(clr, sync)


def main():
    openstack = 0
    if len(sys.argv) < 2:
        print("Usage:\n\t%s PACKAGE <openstack>\n" % (sys.argv[0]))
        print(" if <openstack> then python 3.6 is ussed")
        return

    package = sys.argv[1]

    if sys.argv[2]:
        if sys.argv[2] == "openstack":
            package_name = "openstack-"+ package
        else:
            package_name = package

    package = package_name

    do_package(package, 0, openstack)
#   do_package(package, 1)
    return


if __name__ == '__main__':
    main()

