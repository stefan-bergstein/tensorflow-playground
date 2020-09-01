#! /usr/bin/env python3

import time
import os
import tensorflow as tf
import timeit

def cpu():
  with tf.device('/cpu:0'):
    random_image_cpu = tf.random.normal((100, 100, 100, 3))
    net_cpu = tf.keras.layers.Conv2D(32, 7)(random_image_cpu)
    return tf.math.reduce_sum(net_cpu)

def main():
    
    print('CPU  warming ...')
    cpu()

    for x in range(5):
        cpu_time = timeit.timeit('cpu()', number=10, setup="from __main__ import cpu")
        print('{0:} - CPU: {1:5.2f}'.format(x, cpu_time))
        
if __name__ == '__main__':
    main()
