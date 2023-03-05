aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin 408386168496.dkr.ecr.us-west-2.amazonaws.com

docker build -t pro305_users_patch .

docker tag pro305_users_patch:latest 408386168496.dkr.ecr.us-west-2.amazonaws.com/pro305_users_patch:latest

docker push 408386168496.dkr.ecr.us-west-2.amazonaws.com/pro305_users_patch:latest