import math
import tensorflow as tf
import numpy as np

a = 5.0
b = 4.99998
print(math.isclose(a, b, rel_tol=1e-5))

a_m = tf.constant([2.0, 3.0, 4.0], dtype=tf.float64)
b_m = tf.constant([5.0, 6.0, 7.0], dtype=tf.float64)

c_m = tf.divide(a_m, b_m)

result = [0.4,0.5,0.5714286]

print(c_m)

print(tf.equal(result,c_m))
print(np.allclose(result,c_m,rtol=1e-05, atol=1e-08))
