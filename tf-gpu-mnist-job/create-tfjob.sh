#!/bin/bash

for i in {1..5}
do

  echo "* Create job ${i}"
  sed "s|name: tf-gpu-mnist-job-0|name: tf-gpu-mnist-job-${i}|" manifests/tf-gpu-mnist-job.yaml  | oc apply -f -

done



