import subprocess
import inspect
import os
import sys

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
    if not ret:
        sys.exit(ret)

def build_basic():
    """
    build basic mpi hellow world
    """
    function_name = inspect.currentframe().f_code.co_name
    ret = os.system("cd mpi/ && make")
    print(function_name + " : " + str(bool(not(ret))))
    if ret:
        sys.exit(ret)
    ret = os.system("cd mpi/ && make clean")

def run_basic():
    """
    run basic mpi hellow world
    """
    function_name = inspect.currentframe().f_code.co_name
    ret = os.system("cd mpi/ && make")
    ret = os.system("cd mpi/ && mpiexec ./mpi_hello_world")
    print(function_name + " : " + str(bool(not(ret))))
    if ret:
        sys.exit(ret)
    ret = os.system("cd mpi/ && make clean")

def main():
    print("Basic MPI Test Cases:\n")
    get_version()
    build_basic()
    run_basic()

if __name__== "__main__":
  main()


