# Compile and run experiments

Here, we provide a guide to compiling and running our experiments using our Docker image.

Please file an [issue on GitHub](https://github.com/jgh9094/GPTP-2021-Exploration-Of-Exploration/issues) if something is unclear or does not work.

## Docker

You'll need [Docker](https://docs.docker.com/get-docker/) to follow this guide. This guide was written using `Docker version 20.10.2, build 20.10.2-0ubuntu1~20.10.1`.

### Getting the right image

We've already built a Docker image for this project with everything needed to compile and run our code inside: <https://hub.docker.com/repository/docker/amlalejini/gptp-2021-an-exploration-of-exploration>

You can pull our Docker image from DockerHub:

```
docker pull amlalejini/gptp-2021-an-exploration-of-exploration
```

Now, if you run `docker image ls`, you should see something like

```
REPOSITORY                                           TAG       IMAGE ID       CREATED       SIZE
amlalejini/gptp-2021-an-exploration-of-exploration   latest    d0f392bfe129   3 hours ago   2.67GB
```

### Spinning up a container

You can spin up a container with the image we just pulled from DockerHub, using `docker run -it <IMAGE>`.
Note that `<IMAGE>` corresponds to the `IMAGE ID` field for the image we want to run with (which you can get from `docker image ls`).
In this example, I would run:

```
docker run -it d0f392bfe129
```

This will drop you inside a container made with the correct docker image. You can see everything that's been installed/included in the container by looking through [this DockerFile](https://github.com/jgh9094/GPTP-2021-Exploration-Of-Exploration/blob/main/Dockerfile). Most importantly, the container already has [our GitHub repository](https://github.com/jgh9094/GPTP-2021-Exploration-Of-Exploration) and the correct version of the [Empirical library](https://github.com/devosoft/Empirical) included. Even more conveniently, we've already compiled the experiment for you (`/opt/GPTP-2021-Exploration-Of-Exploration/dia_world`).

### Running inside the container

Inside the container, navigate to `/opt/GPTP-2021-Exploration-Of-Exploration` and run `./dia_world`. Done! You're running the software used to conduct our experiments!

To generate a configuration file (`Dia.cfg`), you can run `./dia_world --gen`. You can also run `./dia_world --help` for a list of configuration options. The executable will default to the parameters specified in a `Dia.cfg` file (in the same directory), but you can override any setting on the command line. E.g., `./dia_world -POP_SIZE 42` will configuration the population size to be 42.

You can exit the container at any time with `exit`.

### Copying content from the container

To copy files out of the container to your local machine, [use the `docker cp` command](https://docs.docker.com/engine/reference/commandline/cp/).