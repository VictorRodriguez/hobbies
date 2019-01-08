# Docker Tutorial

First example

```
$ docker build .
Sending build context to Docker daemon  2.048kB
Step 1/2 : FROM debian:stretch-slim
stretch-slim: Pulling from library/debian
177e7ef0df69: Pull complete
Digest: sha256:6c31161e090aa3f62b9ee1414b58f0a352b42b2b7827166e57724a8662fe4b38
Status: Downloaded newer image for debian:stretch-slim
 ---> bd04d03c4529
 Step 2/2 : CMD ["echo", "hola mundo desde mi pc"]
  ---> Running in 6cc6c383efe6
  Removing intermediate container 6cc6c383efe6
   ---> 702d6b306afb
   Successfully built 702d6b306afb

$ docker run 702d6b306afb
hola mundo desde mi pc

## Links

* https://docker-curriculum.com/


