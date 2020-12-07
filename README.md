# tensorflow-playground

- [Play with Tensorflow GPU Dummy K8S Jobs](tf-gpu-test-job/README.md)
- [Play with Tensorflow GPU MNIST K8S Jobs](tf-gpu-mnist-job/README.md)
- [Check GPUs](#check-gpus)
- [Who has the GPUs?](#who-has-the-gpus)

## Check GPUs

Check the availability of GPUs before you start

### Quick view at the operator

Check pods in ```gpu-operator-resources``` namespace:

```
oc get pods -n gpu-operator-resources

## Expected output:
NAME                                       READY   STATUS      RESTARTS   AGE
gpu-operator-59847dc475-8tck7              1/1     Running     0          6d3h
nfd-master-gmwlz                           1/1     Running     0          8d
nfd-master-qcj9k                           1/1     Running     0          8d
nfd-master-tcl8r                           1/1     Running     0          8d
nfd-operator-9946ddc57-cx4nj               1/1     Running     0          8d
nfd-worker-cmlsb                           1/1     Running     5          8d
nvidia-container-toolkit-daemonset-8qc2l   1/1     Running     0          8d
nvidia-dcgm-exporter-bskqk                 1/1     Running     3          8d
nvidia-device-plugin-daemonset-ng2zg       1/1     Running     0          6d2h
nvidia-device-plugin-validation            0/1     Completed   0          6d2h
nvidia-driver-daemonset-c8h5w              1/1     Running     0          8d
nvidia-driver-validation                   0/1     Completed   0          6d2h
```

Have a look at the driver and plugin validation:


```
oc logs nvidia-driver-validation -n gpu-operator-resources

## Expected output:
> Using CUDA Device [0]: Tesla K20Xm
> GPU Device has SM 3.5 compute capability
[Vector addition of 50000 elements]
Copy input data from the host memory to the CUDA device
CUDA kernel launch with 196 blocks of 256 threads
Copy output data from the CUDA device to the host memory
Test PASSED
Done
```
```
oc logs nvidia-device-plugin-validation -n gpu-operator-resources

## Expected output:
> Using CUDA Device [0]: Tesla K20Xm
> GPU Devicegpu-mnist-jobs below:

launch with 196 blocks of 256 threads
Copy output data from the CUDA device to the host memory
Test PASSED
Done
```

### View GPU utilization

To view GPU utilization, run nvidia-smi from a pod in the GPU operator daemonset.
```
oc get pods -l app=nvidia-driver-daemonset -n gpu-operator-resources
NAME                            READY   STATUS    RESTARTS   AGE
nvidia-driver-daemonset-c8h5w   1/1     Running   0          8d

oc exec -it nvidia-driver-daemonset-c8h5w nvidia-smi
```

Expected results with a idle GPU:
```gpu-mnist-jobs below:


+-----------------------------------------------------------------------------+
| NVIDIA-SMI 440.64.00    Driver Version: 440.64.00    CUDA Version: 10.2     |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|===============================+======================+======================|
|   0  Tesla K20Xm         On   | 00000000:03:00.0 Off |                    0 |
| N/A   46C    P8    18W / 235W |     11MiB /  5700MiB |      0%      Default |
+-------------------------------+----------------------+----------------------+
                                                                               
+-----------------------------------------------------------------------------+
| Processes:                                                       GPU Memory |
|  GPU       PID   Type   Process name                             Usage      |
|=============================================================================|
|  No running processes found                                                 |
+-----------------------------------------------------------------------------+

```

Expected results with a busy GPU:
```
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 440.64.00    Driver Version: 440.64.00    CUDA Version: 10.2     |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|===============================+======================+======================|
|   0  Tesla K20Xm         On   | 00000000:03:00.0 Off |                    0 |
| N/A   54C    P0    97W / 235W |     78MiB /  5700MiB |     91%      Default |
+-------------------------------+----------------------+----------------------+
                                                                               
+-----------------------------------------------------------------------------+
| Processes:                                                       GPU Memory |
|  GPU       PID   Type   Process name                             Usage      |
|=============================================================================|
|    0   2097235      C   .../64bit/22-0.0.11/Core_22.fah/FahCore_22    66MiB |
+-----------------------------------------------------------------------------+
```

### View the nodes

```
oc describe nodes | grep "nvidia.com/gpu" -B10

  Hostname:    storm5.coe.muc.redhat.com
Capacity:
  cpu:                              44
  devices.kubevirt.io/kvm:          110
  devices.kubevirt.io/tun:          110
  devices.kubevirt.io/vhost-net:    110
  ephemeral-storage:                125277164Ki
  hugepages-1Gi:                    0
  hugepages-2Mi:                    0
  memory:                           792513288Ki
  nvidia.com/gpu:                   1
--
  pods:                             250
Allocatable:
  cpu:                              43500m
  devices.kubevirt.io/kvm:          110
  devices.kubevirt.io/tun:          110
  devices.kubevirt.io/vhost-net:    110
  ephemeral-storage:                114381692328
  hugepages-1Gi:                    0
  hugepages-2Mi:                    0
  memory:                           791362312Ki
  nvidia.com/gpu:                   1
--
Allocated resources:
  (Total limits may be over 100 percent, i.e., overcommitted.)
  Resource                         Requests          Limits
  --------                         --------          ------
  cpu                              2243m (5%)        99700m (229%)
  memory                           16119784001 (1%)  5396126208 (0%)
  ephemeral-storage                0 (0%)            0 (0%)
  devices.kubevirt.io/kvm          2                 2
  devices.kubevirt.io/tun          1                 1
  devices.kubevirt.io/vhost-net    1                 1
  nvidia.com/gpu                   1                 1
                         Busy GPU ^^^               ^^^
```
```
oc describe nodes | grep "nvidia.com/gpu" -B10

Allocated resources:
  (Total limits may be over 100 percent, i.e., overcommitted.)
  Resource                         Requests          Limits
  --------                         --------          ------
  cpu                              2143m (4%)        700m (1%)
  memory                           11824816705 (1%)  1101158912 (0%)
  ephemeral-storage                0 (0%)            0 (0%)
  devices.kubevirt.io/kvm          2                 2
  devices.kubevirt.io/tun          1                 1
  devices.kubevirt.io/vhost-net    1                 1
  nvidia.com/gpu                   0                 0
                         Free GPU ^^^               ^^^
```


##  Who has the GPUs?

```
oc get pods -A -o jsonpath="{range .items[*]}{@.metadata.namespace}{'\t'}{@.metadata.name}{'\t'}{@.spec.containers[*].resources.requests}{'\t'}{@.status.phase}{'\n'}" | grep nvidia.com/gpu
```

Example output:
```
gpu-operator-resources	nvidia-device-plugin-validation	map[nvidia.com/gpu:1]	Succeeded
stefan-gpu-docs	jupyterhub-nb-admin	map[cpu:500m memory:1Gi nvidia.com/gpu:1]	Running
```