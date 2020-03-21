from os import path
import inspect

plugin_location = "/usr/local/lib64/gstreamer-1.0"

def check_plugin_location():
    function_name = inspect.currentframe().f_code.co_name
    ret = path.exists(plugin_location)
    print(function_name + " : " + str(ret))

def main():
  print("Basic Gstreamer vaapi Test Cases:")
  check_plugin_location()

if __name__== "__main__":
  main()

