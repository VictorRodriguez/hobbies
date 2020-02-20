from pymemcache.client import base
import sys

value = 'some value'
key= 'some_key'

set_flag = False
get_flag = False


def set_test(client):
    global set_flag
    ret = client.set(key, value)
    if ret:
        print("SET PASS")
        print("Value stored on key %s = %s" % (key,value))
        set_flag = True
    else:
        print("SET FAIL")

def get_test(client):
    global get_flag
    ret = client.get(key)
    ret_str = ret.decode("utf-8")
    if value in ret_str:
        print("GET PASS")
        print("Value retrieve from key %s = %s" % (key,ret_str))
        get_flag = True
    else:
        print("GET FAIL")

def main():
    try:
        client = base.Client(('localhost', 11211))
    except Exception as e:
        print(e)
        sys.exit(-1)

    set_test(client)
    get_test(client)

    if set_flag and get_flag:
        print("TEST PASS")
        sys.exit(0)
    else:
        print("TEST FAIL")
        sys.exit(-1)

if __name__== "__main__":
    main()

