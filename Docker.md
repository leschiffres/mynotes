# A Docker Tutorial

Docker is a way to package an application into a single component so that it can be launched in any kind of machine. This is really essential in the web development, since one can develop a web application locally and then can launch the app in a different server without having to install all of the dependencies.

Docker consists mainly of two components, images and containers.

- A Docker image is a set of files that has no state.
- A Docker container is the instantiation of docker image or the run time of images.

Considering the example of the web application, if an application consists of Node.js and a postgres database, the docker image would contain all of the files and libraries needed. In order to run this image we have to use a docker container that will launch the app. Thus, docker images can be thought of as templates that will be used repeatedly by any number of containers.

Docker containers are similar in nature to virtual machines. However, a virtual machine has an extra OS which which makes it impractical to use. When using a virtual machine two entirely different operating systems run on the same machine. A Docker container, on the other hand, does not have its own internal OS. The container runs directly inside the host operating system. It uses the host's kernel which is shared by the container and the operating system running on the machine. Kernel is the core of the operating system that controls low level operations. Docker uses special features of the file system to create these isolated environments. 

## Building an image

Generally we can build our own images by configuring appropriately a file called Dockerfile. In order to build our own images, we must build them on top of existing images that contain an operating system. However the fastest way of using docker is to download an existing image from the [docker hub](https://hub.docker.com/). Using the command `docker pull [image-name]` we can download an existing image and then using the docker run command we can build a docker container on this image, so that we can use it. More details and examples follow.

## Let's get our hands dirty.


------------------------------------------------------
## docker run
------------------------------------------------------

In order to initiate a docker container we use the docker run command. Let us consider the following command:

```docker run -v $(pwd):/src python:3 python3 src/hello.py```

This is an example on how you can create a docker container on an image. Concretely, the above command places a file named "hello.py" in the src folder of the docker container. Then just runs the command `python3 src/hello.py` Let's break it down step by step.

In order to run a docker container we need an existing docker image. If we specify a docker image that is not in our system, dockerhub will download it automatically. In this case we start a container using the python image with version 3. Once we download it for the first time and is in our system then next time we build a container, there will be no need to download it again.

However the docker image does not contain any files. With the option -v $(pwd):/src we mount the current directory into the src folder of the container (basically add file hello.py into the src folder of the container). The container does not have access to the actual host machine. so when we start a python3 container,  all it has access to is what was present in that image. but we need it to run a file that's on the host. So to do this we can basically mount host folders on a folder on the container. So the -v command mounts the current directory (pwd) onto the slash source of the container. Using the python3 src/hello.py command we run the file hello.py in the container.

------------------------------------------------------
Examples of docker run commands
------------------------------------------------------

```docker run -it --name=python_interpreter python:3 python```
Starts an interactive container (this means that we will run commands into the container) and it is named python_interpreter. Then starts a
python interpreter (running the command python into the container's terminal). 

Once we exit from the interpreter the docker interpreter  it stops but still exists. We can start it again with the following command:
```docker start -i python_interpreter```

```docker run -it ubuntu bash```
Starts an ubuntu terminal.

```docker run --rm -d -v $(pwd):/usr/share/nginx/html -p 8010:80 nginx:latest```
Starts a container on an nginx image that will basically run a website. It will run in the background and publishes the port 80 into the 8010 of the localhost. If we have in the current directory a simple index.html file, it will be mounted into the specified folder and a website is launched. We can have access to this website by opening a browser at http://localhost:8010 or at http://127.0.0.1:8010.

`docker exec -it container_id /bin/bash`
Opening teminal inside a docker container.

------------------------------------------------------
Some of the options that can be given to the run command are the following:
------------------------------------------------------
-it
For interactive processes (like a shell) we have to add this option.

-d
Detached vs foreground
When starting a Docker container, you must first decide if you want to run the container in the background in a “detached” mode or in the default foreground mode:

-v
The mount option, basically imports the files of a directory to the desired folder inside the container.

:tag
With the tag we can specify a version of an image that we'd like to run the container with by adding image[:tag] to the command. For example, docker run ubuntu:14.04.

-p
The -p option publishes a containers port to the host. So the command

--rm 
Deletes the container after it stops.

--name
Specifies the name of a container.

------------------------------------------------------
## Dockerfile
------------------------------------------------------

In the previous examples we used existing docker images in the docker hub. However, we might want to build our own images. In order to do so we have to use something called a Dockerfile. The dockerfile contains commands that are interpreted by the docker to build the image. For instance

```dockerfile
FROM nginx
ADD . /usr/share/nginx/html
```

This Dockerfile contains two instructions:

- First, create this image from an existing image, which is named nginx. The FROM instruction is a requirement for all Dockerfiles and establishes the base image. Subsequent instructions are executed on the base image.
- Second, add into the folder /usr/share/nginx/html the files lying on our current working directory.

The next step is to build the image using the command docker build:
docker build -t mynginx .

This command builds the image by assigning the name mynginx to the image. The . indicates that the Dockerfile is in the current directory.

RUN is an image build step, the state of the container after a RUN command will be committed to the container image. A Dockerfile can have many RUN steps that layer on top of one another to build the image.

CMD is the command the container executes by default when you launch the built image. A Dockerfile can only have one CMD. The CMD can be overridden when starting a container with docker run $image $other_command.

## Useful stuff

------------------------------------------------------
Installing vi in a docker container.
------------------------------------------------------

Open bash in the container: ```docker exec -it container_name_or_id /bin/bash```
In the container terminal run:
```apt-get update```
```apt-get -y install vim```

------------------------------------------------------
Copy files externally into the container.
------------------------------------------------------

`docker cp new_file container_id:container_folder `


------------------------------------------------------------------------------------------------------------------------------
Running a java program in a docker container.
------------------------------------------------------------------------------------------------------------------------------

Inside the Dockerfile:
```Dockerfile
FROM java:8
WORKDIR /app
COPY hello.java .
RUN javac hello.java
CMD ["java","hello"]
```

Create the image:
`docker build -t java_app .`

Start a container using the image
`docker run -it --name=java_app java_app bash`

Add a new file into the container
`docker cp new_hello.java java_app:/app`

Open a terminal:
`docker exec -it java_app:latest /bin/bash`


------------------------------------------------------------------------------------------------------------------------------
FLASK APP
------------------------------------------------------------------------------------------------------------------------------
https://runnable.com/docker/python/dockerize-your-flask-application

```python
# app.py

from flask import Flask
import os
import socket

app = Flask(__name__)
@app.route("/")

def hello():
    html = "<h3>Hello {name}!</h3> <b>Hostname:</b> {hostname}<br/>"
    return html.format(name=os.getenv("NAME", "world"), hostname=socket.gethostname())

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4000)
```

This script creates a web server listening on port 4000 and serves a small HTML document with a greeting and the container’s hostname.

Dockerfile

```dockerfile
FROM python:2.7-slim
WORKDIR /app
ADD . /app
RUN pip install --trusted-host pypi.python.org Flask
ENV NAME World
CMD ["python", "app.py"]
```

This Dockerfile starts with an image that contains a Python runtime. We can see from the name that it provides version 2.7 in a slim configuration that contains a minimal number of Python packages.

Next, it establishes a WORKDIR (working directory) named /app and ADDs the current working directory to it.

After adding the script to the image, we need to install the Flask Python package, the library we use for the web server. The RUN instruction executes pip install for this. Dockerfiles can run commands as part of the image build process.

Next, it sets the environment variable NAME, which is used in the HTML page returned by app.py

And finally, the Dockerfile specifies the command to run when the image is run. CMD accepts a command and a list of arguments to pass to the command. This image executes the Python interpreter, passing it app.py.

Build the image
`docker build -t mypyweb .`

Build the container and transfer port 4000 of the container to our localhost port 8011
`docker run --name webapp -p 8011:4000 mypyweb`

Build the container and transfer port 4000 of the container to our localhost port 8080 by changing the environment variable name
`docker run --name webapp -p 8080:4000 -e NAME="Dude" mypyweb`

------------------------------------------------------------------------------------------------------------------------------
## Hosting a Postgres Database in a Docker Container
------------------------------------------------------------------------------------------------------------------------------

Fetch an image from the docker hub:
`docker pull postgres`

Now we can build an arbitrary number of containers using this image.

`docker run -d  -p 1283:5432 postgres:latest`

The above command instantiates a docker container based on the postgres image that runs in the background (-d option). Also, we link the port 5432 of the container to another port in our localhost (or a different host machine). By default the port of a postgres database is the 5432. 

You can access the database through the following commands.

```
docker exec -ti [db-container] bash
su postgres
psql
```

Or much quicker with:
`psql -h localhost -p1283 -U postgres`


## References

- http://tutorials.jenkov.com/docker/index.html
- https://www.youtube.com/watch?v=YFl2mCHdv24 : A short version description of docker.
- https://www.youtube.com/watch?v=6aBsjT5HoGY : A clear explanation of docker commands with different examples. 
- https://www.youtube.com/watch?v=fqMOX6JJhGo : Extensive Docker Tutorial
 

 ## Next step: Kubernetes:
 - https://www.udacity.com/course/scalable-microservices-with-kubernetes--ud615
 - https://courses.edx.org/courses/course-v1:LinuxFoundationX+LFS158x+2T2019/course/
