import subprocess
import inspect

version = "4.0.2"

def get_version():
    """
    get and check version
    """
    function_name = inspect.currentframe().f_code.co_name
    process = subprocess.Popen(['mpiexec', '--version'],
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if version in str(stdout):
        ret = True
    else:
        ret = False
    print(function_name + " : " + str(bool(ret)))

def main():
    print("Basic MPI Test Cases:\n")
    get_version()

if __name__== "__main__":
  main()


