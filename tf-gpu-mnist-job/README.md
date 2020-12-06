# Tensorflow GPU Training Jobs with MNIST

This scenario is just for showcasing K8S jobs with Tensorflow


## Prerequisites - before you start

- GPU enabled OCP
- Free GPU resources
- Clone this repo

# Prep

## Clone this repo

```
git clone https://github.com/stefan-bergstein/tensorflow-playground.git
cd tensorflow-playground/tf-gpu-mnist-job
```

## Create a namespace 
```
oc new-project gpu-mnist-jobs
```

## Check the availability of the GPU

Start a pod that runs the nvidia-smi CLI

```
oc apply -f manifests/gpu-container.yaml
...
pod/check-gpu created
```
Inspect the logs:

```
oc logs check-gpu
```

Expected output:
```
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 450.80.02    Driver Version: 450.80.02    CUDA Version: 11.0     |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|                               |                      |               MIG M. |
|===============================+======================+======================|
|   0  Tesla K20Xm         On   | 00000000:00:08.0 Off |                    0 |
| N/A   30C    P8    17W / 235W |      0MiB /  5700MiB |      0%      Default |
|                               |                      |                  N/A |
+-------------------------------+----------------------+----------------------+
                                                                               
+-----------------------------------------------------------------------------+
| Processes:                                                                  |
|  GPU   GI   CI        PID   Type   Process name                  GPU Memory |
|        ID   ID                                                   Usage      |
|=============================================================================|
|  No running processes found                                                 |
+-----------------------------------------------------------------------------+
```

## Validate Tensorflow GPU images 

Start a Tensorflow pod that uses an GPU 
```
oc apply -f manifests/tensorflow-gpu-test.yaml
```
Inspect the logs:
```
oc logs tensorflow-gpu
```

Expected output:
```
...
2020-12-06 17:58:02.288129: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1402] Created TensorFlow device (/job:localhost/replica:0/task:0/device:GPU:0 with 5225 MB memory) -> physical GPU (device: ..
TEST: tf.Tensor(-457.37344, shape=(), dtype=float32)
```

# Build and Run Test Job
```
oc apply -k manifests
...

job.batch/tf-gpu-mnist-job-0 created
buildconfig.build.openshift.io/tf-gpu-mnist-job created
imagestream.image.openshift.io/tf-gpu-mnist created
```

Watch the build:
```

oc logs -f bc/tf-gpu-mnist-job
...
Storing signatures
Successfully pushed image-registry.openshift-image-registry.svc:5000/gpu-mnist-jobs/tf-gpu-mnist@sha256:...
Push successful
```

## Check the MNIST traininf job outout

You might have to delete the pod ```tf-gpu-mnist-job-0``` in case you run into a ```ImagePullBackoff```.
```
oc delete pod -l job-name=tf-gpu-mnist-job-0
```

Watch the TF job:
```
oc logs -l job-name=tf-gpu-mnist-job-0 --follow

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

