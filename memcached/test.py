#!/usr/bin/python

from pymemcache.client import base
import sys

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

def get_test(client,key):
    ret = client.get(key)
    ret_str = ret.decode("utf-8")
    return ret_str

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

    ret_set = set_test(client,key,value)
    ret_str = get_test(client,key)

    ret_coherency = check_coherency(value,ret_str)

    if ret_set and ret_coherency:
        print("TEST PASS")
    else:
        print("TEST FAIL")
        sys.exit(-1)

def test_set_get_existing(client):
    new_value = 'over writing'
    ret_set = set_test(client,key,new_value)
    ret_str = get_test(client,key)

    ret_coherency = check_coherency(new_value,ret_str)

    if ret_set and ret_coherency:
        print("TEST PASS")
    else:
        print("TEST FAIL")
        sys.exit(-1)

def main():

    client = base.Client(('localhost', 11211))
    test_set_get_basic(client)
    test_set_get_existing(client)

    sys.exit(0)


if __name__== "__main__":
    main()

