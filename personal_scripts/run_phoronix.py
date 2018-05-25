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


if __name__ == "__main__":

    cmd = ""

    parser = argparse.ArgumentParser()

    parser.add_argument("--test", help="Test name ",\
            type=str,dest='test')
    parser.add_argument("--logpath", help="Path where to save logfiles",\
            type=str,dest='logpath')
    parser.add_argument("--verbose", help="Verbose",\
             dest="verbose", action="store_true")
    parser.add_argument("--checkup", help="Check that phoronix is well \
            installed", dest="checkup", action="store_true")

    args = parser.parse_args()

    if args.verbose:
        debug_log()

    # check if phoronix is installed
    if args.checkup:
        tmp = "/usr/bin/phoronix-test-suite"
        if os.path.isfile(tmp):
            print("\nINSTALL = OK !")

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


    if args.test:
        # install test
        ret = os.system("phoronix-test-suite install %s" % args.test)
        if not ret:
            print("\nINSTALLi TEST = OK !")

        # run
        ret = os.system("phoronix-test-suite batch-run %s" % args.test)
        if not ret:
            print("\nRUNNING = OK !")

    sys.exit(0)
