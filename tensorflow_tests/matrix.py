#!/usr/bin/env python

import tensorflow as tf
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# Construct a `Session` to execute the graph.
with tf.compat.v1.Session() as sess:
    x1 = tf.constant([1,2,3,4])
    x2 = tf.constant([5,6,7,8])

    res = sess.run(x1)
    print(res)

    res = sess.run(x2)
    print(res)

    result = tf.multiply(x1, x2)

    res = sess.run(result)
    print(res)

    expected = tf.constant([5,12,21,32])

    compare = tf.equal(expected,result)
    res = sess.run(compare)
    if res.all():
        print("PASS")
    else:
        print("FAIL")

