To install dependencies and run the program to receive the desired output, you will start by building a docker image and running the program inside of a docker container. 


If you do not have docker installed please follow the links for install instructions for your operating system.

Docker Install Instructions:
- Mac https://docs.docker.com/docker-for-mac/install/
- Windows https://docs.docker.com/docker-for-windows/install/
- Linux
    - CentOS https://docs.docker.com/engine/install/centos/
    - Debian https://docs.docker.com/engine/install/debian/
    - Ubuntu https://docs.docker.com/engine/install/ubuntu/

If you already have docker great.

clone this repository to your local machine

```
git clone ____________
```

Change to the proto app directory 
```
cd proto_app
```

Build the docker image, this will take a few moments but it will update you when finished. 
```
docker build -t proto_app .
```

Now run the program to get the desired output. This mounts the directory to your container, names the container proto_app for easy removal, it also tags the conatiner as proto_app for easy removal
```
docker run -it --rm -v "$(pwd):/app" --name proto_app proto_app python3 app/runit.py
```



### When you are finished

1. Stop the container

```
docker stop proto_app
```


2. Remove the image
```
docker rmi proto_app 
```
