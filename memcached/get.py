#!/usr/bin/python

from pymemcache.client import base
import sys
import inspect

value = 'some value'
key= 'some_key'


def get_test(client,key):
    ret = client.get(key)
    if ret:
        ret_str = ret.decode("utf-8")
        return ret_str
    else:
        return False

def check_coherency(value,ret_str):
    if value in ret_str:
        print("GET PASS")
        print("Value retrieve from key %s = %s" % (key,ret_str))
        print("Is the same as : %s" % (value))
        ret = True
    else:
        print("GET FAIL")
        ret = False

    return ret

def test_set_get_basic(client):
    print("\n" + inspect.currentframe().f_code.co_name)
    ret_str = get_test(client,key)

    ret_coherency = check_coherency(value,ret_str)

    if ret_coherency:
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

