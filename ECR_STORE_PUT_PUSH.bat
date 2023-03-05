aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin 408386168496.dkr.ecr.us-west-2.amazonaws.com

docker build -t pro305_store_put .

docker tag pro305_store_put:latest 408386168496.dkr.ecr.us-west-2.amazonaws.com/pro305_store_put:latest

docker push 408386168496.dkr.ecr.us-west-2.amazonaws.com/pro305_store_put:latest