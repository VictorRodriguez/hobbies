import tensorflow as tf
x_float = tf.constant([1.8, 2.2], dtype=tf.float32)
x_bfloat16 = tf.cast(x_float, tf.bfloat16)
x_float_2 = tf.cast(x_bfloat16, tf.float32)

print("x_float =")
print(x_float)
print("x_bfloat16")
print(x_bfloat16)
print("x_float_2")
print(x_float_2)

