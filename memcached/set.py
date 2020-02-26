#!/usr/bin/python

from pymemcache.client import base
import sys
import inspect

value = 'some value'
key= 'some_key'



def set_test(client,key,value):
    ret_val = False
    ret = client.set(key, value)
    if ret:
        print("SET PASS")
        print("Value stored on key %s = %s" % (key,value))
        ret_val = True
    else:
        print("SET FAIL")
    return ret_val


def test_set_get_basic(client):
    print("\n" + inspect.currentframe().f_code.co_name)
    ret_set = set_test(client,key,value)

    if ret_set:
        print("TEST PASS")
    else:
        print("TEST FAIL")
        sys.exit(-1)

def main():

    client = base.Client(('localhost', 11211))
    test_set_get_basic(client)
    sys.exit(0)

if __name__== "__main__":
    main()

