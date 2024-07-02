#!/bin/bash

# Get AWS repo url from Terraform outputs
export REPO=$(terraform output --raw demo_app_repo_url)
# Login to AWS ECR
aws ecr get-login-password | docker login --username AWS --password-stdin $REPO

# Pull docker image & push to our ECR
# /!\ you need to do the following to be able to use docker without sudo.
# Using docker with sudo will create a "no basic auth credentials" (root is not $USER, hence has not access to the above credentials)

# sudo groupadd docker
# sudo gpasswd -a $USER docker
# newgrp docker
# Check with:
# docker run hello-world

docker pull --platform linux/amd64 strm/helloworld-http:latest
docker tag strm/helloworld-http:latest $REPO:latest
docker push $REPO:latest

for i in {1..10}
do
    echo "+++ Curl number $i +++"
    curl $(terraform output --raw alb_url)
done