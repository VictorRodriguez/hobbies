#!/bin/python
import os
import sys
import argparse
import datetime
import subprocess
import socket
import getpass

def debug_log():

    test_name = args.test.split("/")[1]
    ip = socket.gethostbyname(socket.gethostname())
    datetime = str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))

    result_name = "%s-%s-%s" % (test_name,ip,datetime)
    result_identifier = result_name
    result_description = result_name

    """
    Documentation:

    http://www.phoronix-test-suite.com/documentation/phoronix-test-suite.html
    TEST_RESULTS_NAME

    When this variable is set, the value will be used \
            as the name for automatically saving the \
            test results.

    TEST_RESULTS_IDENTIFIER

    When this variable is set, the value will be used \
            as the test identifier when automatically \
            saving the test results.

    TEST_RESULTS_DESCRIPTION

    When this variable is set, the value will be used \
            as the test results description when saving \
            the test results.
    """
    os.environ['TEST_RESULTS_NAME'] = result_name
    os.environ['TEST_RESULTS_IDENTIFIER'] = result_identifier
    os.environ['TEST_RESULTS_DESCRIPTION'] = result_description

    print("\n Variables \n")
    print(test_name)
    print(ip)
    print(datetime)

    print("\n Command line \n")
    print(cmd_name)
    print(cmd_identifier)
    print(cmd_description)
    print(cmd)

def print_log(out):
    alllines = out.decode("latin-1")
    lines =  alllines.split("\n")
    for line in lines:
        print(line)

if __name__ == "__main__":

    cmd = ""

    parser = argparse.ArgumentParser()

    parser.add_argument("--test", help="Test name ",\
            type=str,dest='test',required=True)
    parser.add_argument("--logpath", help="Path where to save logfiles",\
            type=str,dest='logpath')
    parser.add_argument("--verbose", help="Verbose",\
             dest="verbose", action="store_true")

    args = parser.parse_args()

    if args.verbose:
        debug_log()

    # set up phoronix
    home = os.path.expanduser('~')
    tmp = os.path.join(home,".phoronix-test-suite/test-results/")
    if os.path.isdir(tmp):
        base_path = tmp
        pass
    elif os.path.isdir("/var/lib/phoronix-test-suite/"):
        base_path = "/var/lib/phoronix-test-suite/"
        pass
    else:
        print("Seting up phoronix")
        if getpass.getuser() == "root":
            os.system("mkdir -p /var/lib/phoronix-test-suite/")
            os.system("cp user-config.xml /var/lib/phoronix-test-suite/")
            base_path = "/var/lib/phoronix-test-suite/"
        else:
            os.system("mkdir -p /var/lib/phoronix-test-suite/")
            tmp = os.path.join(home,".phoronix-test-suite/")
            os.system("cp user-config.xml %s",tmp)
            base_path = tmp

    ret = os.system("phoronix-test-suite")
    if not ret:
        print("\nSET UP TEST = OK !")
        print(base_path)


    # install test
    out, err = subprocess.Popen(["phoronix-test-suite","install", args.test], \
            stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    if not err:
        print("\nINSTALLi TEST = OK !")
    print_log(out)

    # run
    out, err = subprocess.Popen(["phoronix-test-suite","batch-run", args.test], \
            stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    if not err:
        print("\nRUNNING = OK !")
    print_log(out)

    sys.exit(0)
