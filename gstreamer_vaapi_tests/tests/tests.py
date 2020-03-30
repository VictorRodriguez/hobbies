#!/usr/bin/env python3
import os
import inspect
import distro
from os import path
from os import listdir
from os.path import isfile, join

os_name = "general"

plugin_location = "/usr/local/lib64/gstreamer-1.0"
plugin_location_ubuntu = "/usr/lib/x86_64-linux-gnu/gstreamer-1.0"

def vaapijpegenc():
    """
    vaapijpegenc: VA-API JPEG enc
    """
    function_name = inspect.currentframe().f_code.co_name
    cmd = "bash /tests/vaapijpegenc.sh"
    ret = os.system(cmd + " > /dev/null 2>&1")
    print(function_name + " : " + str(bool(not ret)))

def inspect_vaapih264enc():
    """
    gst-inspect-1.0 vaapih264enc must return 0 as RC
    """
    function_name = inspect.currentframe().f_code.co_name
    cmd = "gst-inspect-1.0 vaapih264enc"
    ret = os.system(cmd + " > /dev/null 2>&1")
    print(function_name + " : " + str(bool(not ret)))

def inspect_plugin_elements():
    """
    gst-inspect-1.0 /usr/local/lib64/gstreamer-1.0/libgstvaapi.so
    """
    ret = False
    function_name = inspect.currentframe().f_code.co_name
    plugin_location = check_plugin_location()
    path_lib = join(plugin_location,"libgstvaapi.so")
    if isfile(path_lib):
        cmd = "gst-inspect-1.0 " + path_lib + " > log"
        os.system(cmd)
        fp = open("log", 'r')
        lines = fp.readlines()
        for line in lines:
            if "Name" in line and "vaapi" in line:
                ret = True

    print(function_name + " : " + str(ret))

def inspect_plugin():
    """
    gst-inspect-1.0 <path to .so> must return 0 as RC
    """
    function_name = inspect.currentframe().f_code.co_name
    plugin_location = check_plugin_location()
    libs = os.listdir(plugin_location)
    for lib in libs:
        if lib.endswith(".so"):
            cmd = "gst-inspect-1.0 %s" % join(plugin_location, lib)
            if os.system(cmd + " > /dev/null 2>&1"):
                ret = False
                print(cmd)
                break
            else:
                ret = True
    print(function_name + " : " + str(ret))

def check_plugin_location():
    """
    check that file /usr/local/lib64/gstreamer-1.0 exist
    """
    function_name = inspect.currentframe().f_code.co_name
    if os_name == "ubuntu":
        location = plugin_location_ubuntu
    else:
        location = plugin_location
    ret = path.exists(location)
    print(function_name + " : " + str(ret))

    return location

def get_os_name():
    global os_name
    if "Ubuntu" in distro.linux_distribution():
        os_name = "ubuntu"

    return distro.linux_distribution()

def main():
    print("System Info: " + str(get_os_name()))
    print("Basic Gstreamer vaapi Test Cases:\n")
    check_plugin_location()
    inspect_plugin()
    inspect_plugin_elements()
    inspect_vaapih264enc()
    vaapijpegenc()

if __name__== "__main__":
  main()

