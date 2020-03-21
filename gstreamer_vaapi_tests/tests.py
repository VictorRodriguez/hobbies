import os
import inspect
import distro
from os import path
from os import listdir
from os.path import isfile, join

os_name = "general"

plugin_location = "/usr/local/lib64/gstreamer-1.0"
plugin_location_ubuntu = "/usr/lib/x86_64-linux-gnu/gstreamer-1.0"


def inspect_plugin():
    """
    gst-inspect-1.0 <path to .so> must return 0 as RC
    """
    function_name = inspect.currentframe().f_code.co_name

    path_lib = "/usr/lib/x86_64-linux-gnu/gstreamer-1.0/"
    libs = os.listdir(path_lib)
    for lib in libs:
        cmd = "gst-inspect-1.0 %s" % join(path_lib, lib)
        if os.system(cmd + " > /dev/null 2>&1"):
            ret = False
            break
        else:
            ret = True
    print(function_name + " : " + str(ret))
    return ret

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

if __name__== "__main__":
  main()

