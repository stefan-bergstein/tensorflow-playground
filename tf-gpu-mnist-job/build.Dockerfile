FROM tensorflow/tensorflow:latest-gpu
COPY * /tmp/
USER 1001
CMD ["python", "/tmp/mnist_convnet.py"]