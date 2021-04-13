# Installing Docker on Linux

This is a [link](https://docs.docker.com/install/linux/docker-ce/fedora/) to the official docker website documentation for installing docker on fedora linux.

In short run these commands in the terminal:

```console
sudo dnf -y install dnf-plugins-core

sudo dnf config-manager \
    --add-repo \
    https://download.docker.com/linux/fedora/docker-ce.repo

sudo dnf install docker-ce

sudo systemctl start docker
```

To make sure everything works properly, run this command and you should see a greeting:

```console
sudo docker run hello-world
```

# Install and Manage MySQL Server docker image

1. Pull the image from docker hub by running `docker pull mysql`.
2. Create and run a docker container by running `docker run --name test-container -e MYSQL_ROOT_PASSWORD=root -d mysql` where `test-container` is the container's name and the root password is set to `root`. Run `docker logs test-container` to see the logs and whether MySQL server started.
3. To see on which port MySQL Server is listening inside the docker container, run `docker ps` and look for `test-container`.
4. To get the IP Address of the docker container, you can run `docker inspect test-container` and look for it under `NetworkSettings`, `Networks`, `bridge`, `IPAddress`.
5. If you have installed MySQL workbench, you can connect to the database by providing the IP Address in as in point **4** and the port (*not the forwarded port*) of the docker container on which MySQL server is listening as in point **3**.
6. To create a new database run the following: `docker exec -it test-container mysql --user=root --password=root --execute="CREATE DATABASE productsdb;"`. In general, to run any command: `docker exec -it <container-name> mysql --user=<user> --password=<password> --execute="<command>"`
7. To use MySQL's old authentication for a user (this is for MySQL8) run the following: `docker exec -it test-container mysql --user=root --password=root --execute="ALTER USER root IDENTIFIED WITH mysql_native_password BY 'root';"`