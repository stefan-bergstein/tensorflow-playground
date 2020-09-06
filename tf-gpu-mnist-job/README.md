# Tensorflow GPU Training Jobs with MNIST

This scenario is just for showcasing K8S jobs with Tensorflow


## Prerequisites - before you start

- GPU enabled OCP
- Free GPU resources
- Clone this repo
- Cuda S2I build image

### Build Cuda S2I build image

```
oc new-project gpu-mnist-jobs
oc process -f https://raw.githubusercontent.com/harshad16/cuda/master/cuda.yaml CUDA_VERSION=10.2 SOURCE_REPOSITORY=https://github.com/harshad16/cuda.git | oc apply -f -
```

Note, several images are built. It will take some time.
```
oc get builds
...
NAME                         TYPE     FROM          STATUS     STARTED          DURATION
10.2-rhel7-base-1            Docker   Git@4450352   Complete   13 minutes ago   1m9s
10.2-rhel7-runtime-1         Docker   Git@4450352   Complete   11 minutes ago   2m5s
10.2-rhel7-devel-1           Docker   Git@4450352   Complete   9 minutes ago    2m57s
10.2-rhel7-cudnn7-devel-1    Docker   Git@4450352   Complete   6 minutes ago    2m24s
10.2-s2i-base-rhel7-cuda-1   Docker   Git@12e5227   Complete   4 minutes ago    3m59s
```

# Build and Run Test Job
```
cd tensorflow-playground/tf-gpu-mnist-job
oc apply -k manifests
```

Watch the build:
```
oc logs -f bc/tf-gpu-mnist-bc
...
Push successful
```

## Check the MNIST traininf job outout

You might have devel the pod ```tf-gpu-mnist-job-0``` in case you run into a ```ImagePullBackoff```.

```
oc logs -l job-name=tf-gpu-mnist-job-0 --tail=-1

...
-> physical GPU (device: 0, name: Tesla K20Xm, pci bus id: 0000:03:00.0, compute capability: 3.5)
Model: "sequential"
_________________________________________________________________
Layer (type)                 Output Shape              Param #   
=================================================================
conv2d (Conv2D)              (None, 26, 26, 32)        320       
_________________________________________________________________
max_pooling2d (MaxPooling2D) (None, 13, 13, 32)        0         
_________________________________________________________________
conv2d_1 (Conv2D)            (None, 11, 11, 64)        18496     
_________________________________________________________________
max_pooling2d_1 (MaxPooling2 (None, 5, 5, 64)          0         
_________________________________________________________________
flatten (Flatten)            (None, 1600)              0         
_________________________________________________________________
dropout (Dropout)            (None, 1600)              0         
_________________________________________________________________
dense (Dense)                (None, 10)                16010     
=================================================================
Total params: 34,826
Trainable params: 34,826
Non-trainable params: 0
_________________________________________________________________
Epoch 1/15
2020-09-06 12:59:57.172538: I tensorflow/stream_executor/platform/default/dso_loader.cc:48] Successfully opened dynamic library libcublas.so.10
2020-09-06 12:59:57.340302: I tensorflow/stream_executor/platform/default/dso_loader.cc:48] Successfully opened dynamic library libcudnn.so.7
422/422 [==============================] - 3s 8ms/step - loss: 0.3616 - accuracy: 0.8905 - val_loss: 0.0823 - val_accuracy: 0.9775
Epoch 2/15
422/422 [==============================] - 3s 7ms/step - loss: 0.1081 - accuracy: 0.9673 - val_loss: 0.0532 - val_accuracy: 0.9850
Epoch 3/15
422/422 [==============================] - 3s 7ms/step - loss: 0.0822 - accuracy: 0.9746 - val_loss: 0.0474 - val_accuracy: 0.9870
Epoch 4/15
422/422 [==============================] - 3s 7ms/step - loss: 0.0667 - accuracy: 0.9789 - val_loss: 0.0416 - val_accuracy: 0.9892
Epoch 5/15
422/422 [==============================] - 3s 7ms/step - loss: 0.0604 - accuracy: 0.9809 - val_loss: 0.0393 - val_accuracy: 0.9893
Epoch 6/15
422/422 [==============================] - 3s 7ms/step - loss: 0.0548 - accuracy: 0.9831 - val_loss: 0.0333 - val_accuracy: 0.9912
Epoch 7/15
422/422 [==============================] - 3s 7ms/step - loss: 0.0507 - accuracy: 0.9843 - val_loss: 0.0365 - val_accuracy: 0.9897
Epoch 8/15
422/422 [==============================] - 3s 7ms/step - loss: 0.0449 - accuracy: 0.9858 - val_loss: 0.0330 - val_accuracy: 0.9907
Epoch 9/15
422/422 [==============================] - 3s 7ms/step - loss: 0.0446 - accuracy: 0.9854 - val_loss: 0.0318 - val_accuracy: 0.9920
Epoch 10/15
422/422 [==============================] - 3s 7ms/step - loss: 0.0432 - accuracy: 0.9865 - val_loss: 0.0288 - val_accuracy: 0.9920
Epoch 11/15
422/422 [==============================] - 3s 7ms/step - loss: 0.0364 - accuracy: 0.9884 - val_loss: 0.0309 - val_accuracy: 0.9905
Epoch 12/15
422/422 [==============================] - 3s 7ms/step - loss: 0.0376 - accuracy: 0.9876 - val_loss: 0.0289 - val_accuracy: 0.9922
Epoch 13/15
422/422 [==============================] - 3s 7ms/step - loss: 0.0341 - accuracy: 0.9893 - val_loss: 0.0265 - val_accuracy: 0.9927
Epoch 14/15
422/422 [==============================] - 3s 7ms/step - loss: 0.0329 - accuracy: 0.9892 - val_loss: 0.0278 - val_accuracy: 0.9922
Epoch 15/15
422/422 [==============================] - 3s 7ms/step - loss: 0.0344 - accuracy: 0.9890 - val_loss: 0.0255 - val_accuracy: 0.9925
Test loss: 0.02143179066479206
Test accuracy: 0.9922000169754028


```

# Demo multiple jobs

Strat jobs ...

```
./create-tfjob.sh 

* Create job 1
job.batch/tf-gpu-mnist-job-1 created
* Create job 2
job.batch/tf-gpu-mnist-job-2 created
* Create job 3
job.batch/tf-gpu-mnist-job-3 created
* Create job 4
job.batch/tf-gpu-mnist-job-4 created
* Create job 5
job.batch/tf-gpu-mnist-job-5 created
```

Monitor progress ...
```
oc get jobs
NAME                 COMPLETIONS   DURATION   AGE
tf-gpu-mnist-job-0   1/1           9m46s      4h21m
tf-gpu-mnist-job-1   1/1           62s        4h5m
tf-gpu-mnist-job-2   1/1           117s       4h5m
tf-gpu-mnist-job-3   1/1           2m50s      4h5m
tf-gpu-mnist-job-4   1/1           4m47s      4h5m
tf-gpu-mnist-job-5   1/1           3m48s      4h5m
```

