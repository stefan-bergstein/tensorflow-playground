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

def gpu():
  with tf.device('/device:GPU:0'):
    random_image_gpu = tf.random.normal((100, 100, 100, 3))
    net_gpu = tf.keras.layers.Conv2D(32, 7)(random_image_gpu)
    return tf.math.reduce_sum(net_gpu)

def main():

    device_name = tf.test.gpu_device_name()
    if device_name != '/device:GPU:0':
        raise SystemError('GPU device not found')
    print('Found GPU at: {}'.format(device_name))
    
    print('CPU and GPU warming ...')
    cpu()
    gpu()
    
    cpu_time_list = []
    gpu_time_list = []
    for x in range(5):
        cpu_time = timeit.timeit('cpu()', number=10, setup="from __main__ import cpu")
        cpu_time_list.append(cpu_time)
        gpu_time = timeit.timeit('gpu()', number=10, setup="from __main__ import gpu")
        gpu_time_list.append(gpu_time)
        print('{0:} - CPU: {1:5.2f}, GPU: {2:5.2f}, Factor:{3:}'.format(x, cpu_time, gpu_time, int(cpu_time/gpu_time)))
        

if __name__ == '__main__':
    main()
