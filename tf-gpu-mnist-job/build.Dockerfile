FROM tensorflow/tensorflow:latest-gpu
COPY * /tmp/
CMD ["python", "/tmp/mnist_convnet.py"]