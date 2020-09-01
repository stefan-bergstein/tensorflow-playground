FROM registry.access.redhat.com/ubi8/python-36:latest

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["python"] 
CMD ["tf-gpu-test-job.py"]



