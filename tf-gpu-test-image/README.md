# 

cat build.Dockerfile | oc new-build --name python-container --dockerfile='-'


docker build -t $DOCKERHUB_USERNAME/tf-gpu-test-job:v0.0.1 .
docker run $DOCKERHUB_USERNAME/tf-gpu-test-job:v0.0.1


oc new-project ubi-build
oc new-build https://github.com/grantomation/rhel-build.git --context-dir ubi-build --name ubi-build
oc logs -f build/ubi-build-1