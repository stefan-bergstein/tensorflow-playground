# Tensorflow GPU Test Job
Run a simple K8S Jab for GPU testing.

## Prerequisites - before you start

- GPU enabled OCP
- Free GPU resources
- Cuda S2I build image

### Build Cuda S2I build image

```
oc process -f https://raw.githubusercontent.com/harshad16/cuda/master/cuda.yaml CUDA_VERSION=10.2 SOURCE_REPOSITORY=https://github.com/harshad16/cuda.git | oc apply -f -
```

# Build and Run Test Job
oc apply -f manifests


## Successfull result
```
oc logs -l job-name=tf-gpu-mnist-job

0 - CPU:  1.10, GPU:  0.16, Factor:6
1 - CPU:  1.08, GPU:  0.15, Factor:7
2 - CPU:  1.13, GPU:  0.16, Factor:6
3 - CPU:  1.14, GPU:  0.15, Factor:7
4 - CPU:  1.10, GPU:  0.16, Factor:6
5 - CPU:  1.09, GPU:  0.16, Factor:6
6 - CPU:  1.36, GPU:  0.17, Factor:7
7 - CPU:  1.50, GPU:  0.16, Factor:9
8 - CPU:  1.41, GPU:  0.16, Factor:8
9 - CPU:  1.33, GPU:  0.17, Factor:7
```

# Demo multiple jobs

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


