#!/bin/bash

for i in {1..5}
do

  echo "* Create job ${i}"
  sed "s|name: tf-gpu-test-job-0|name: tf-gpu-test-job-${i}|" manifests/tf-gpu-test-job.yaml  | oc apply -f -

done



