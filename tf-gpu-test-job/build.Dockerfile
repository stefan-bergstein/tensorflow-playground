FROM tensorflow/tensorflow:latest-gpu
COPY * /tmp/
USER 1001
ENTRYPOINT ["python", "/tmp/tf-gpu-test-job.py"]