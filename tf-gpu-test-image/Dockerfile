FROM nvcr.io/nvidia/cuda:10.2-base-centos8

WORKDIR /usr/src/

RUN yum install python36 -y

COPY requirements.txt ./
RUN pip3 install --upgrade pip
RUN pip3 install --upgrade setuptools
RUN pip3 install --no-cache-dir -r requirements.txt

RUN ln -s /usr/local/cuda-10.2/targets/x86_64-linux/lib/libcudart.so.10.2 /usr/local/cuda-10.2/targets/x86_64-linux/lib/libcudart.so.10.1

ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda-10.2/targets/x86_64-linux/lib/

COPY . .

ENTRYPOINT ["python3"] 
CMD ["tf-gpu-test-job.py"]




