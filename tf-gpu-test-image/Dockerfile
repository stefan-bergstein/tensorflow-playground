FROM registry.access.redhat.com/ubi8/python-36:latest

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install --no-cache-dir -r requirements.txt

RUN wget https://developer.download.nvidia.com/compute/cuda/repos/rhel8/x86_64/cuda-repo-rhel8-10.2.89-1.x86_64.rpm
RUN rpm -i cuda-repo-*.rpm
RUN yum install cuda

COPY . .

ENTRYPOINT ["python"] 
CMD ["tf-gpu-test-job.py"]



