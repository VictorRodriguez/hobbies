#!/usr/bin/env python

import tensorflow as tf
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
tf.add(1, 2).numpy()
hello = tf.constant('Hello, TensorFlow!')
hello.numpy()
