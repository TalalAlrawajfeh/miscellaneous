#!/bin/bash


#
# mysql database setup
#

ROOT_PASSWORD="root"

# kill running docker containers
docker container kill $(docker ps -q)
# prune all dead containers
echo y | docker container prune

# pull latest mysql docker image
docker pull mysql
# create and run a mysql docker container
docker run --name test-container -e MYSQL_ROOT_PASSWORD=$ROOT_PASSWORD -d mysql

# wait until mysql service is running to proceed
while true
do
    log=$(docker exec -it test-container mysql --user=root --password=$ROOT_PASSWORD --execute="USE sys;")
    error=$(echo $log | grep ERROR)
    if [[ -z $error ]]
    then
        break
    fi
    sleep 1
done

# get the ip address of the mysql container
E_DATABASE_HOST=$(docker inspect -f "{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}" test-container)

# new versions of the mysql database (> v8) require an RSA certificate for authentication, but we will force using the old authentication by the user/password credentials
docker exec -it test-container mysql --user=root --password=$ROOT_PASSWORD --execute="CREATE DATABASE productsdb;"
docker exec -it test-container mysql --user=root --password=$ROOT_PASSWORD --execute="ALTER USER root IDENTIFIED WITH mysql_native_password BY '$ROOT_PASSWORD';"


#
# consul setup
#

# pull the consul image
docker pull consul

# run an instance of consul in a docker container
CONSUL_ID=$(docker run -d -e CONSUL_BIND_INTERFACE=eth0 consul)
CONSUL_HOST=$(docker inspect -f "{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}" $CONSUL_ID)

# wait for consul to start
while true
do
    leader_ip=$(curl -X GET http://$CONSUL_HOST:8500/v1/status/leader)
    if [[ ! -z $leader_ip ]]
    then
        break
    fi
done


#
# products-service setup
#

# build and run our service
cd products-service
docker build -t products-service .
cd ..

docker run -e DATABASE_HOST=$E_DATABASE_HOST \
           -e DATABASE_USERNAME=root \
           -e DATABASE_PASSWORD=$ROOT_PASSWORD \
           -e CONSUL_URL=http://$CONSUL_HOST:8500 \
           -e SERVICE_ID=1 \
           -d products-service

# to run other instances just increment PRODUCTS_SERVICE_ID each time
# docker run -e DATABASE_HOST=$E_DATABASE_HOST \
#            -e DATABASE_USERNAME=root \
#            -e DATABASE_PASSWORD=$ROOT_PASSWORD \
#            -e CONSUL_URL=http://$CONSUL_HOST:8500 \
#            -e SERVICE_ID=2 \
#            -d products-service


#
# receipts-service setup
#

docker exec -it test-container mysql --user=root --password=$ROOT_PASSWORD --execute="CREATE DATABASE receiptsdb;"

cd receipts-service
docker build -t receipts-service .
cd ..

docker run -e DATABASE_HOST=$E_DATABASE_HOST \
           -e DATABASE_USERNAME=root \
           -e DATABASE_PASSWORD=$ROOT_PASSWORD \
           -e CONSUL_URL=http://$CONSUL_HOST:8500 \
           -e SERVICE_ID=1 \
           -d receipts-service


#
# api-gateway setup
#

docker exec -it test-container mysql --user=root --password=$ROOT_PASSWORD --execute="CREATE DATABASE apigatewaydb;"

cd api-gateway
docker build -t api-gateway .
cd ..

docker run -e DATABASE_HOST=$E_DATABASE_HOST \
           -e DATABASE_USERNAME=root \
           -e DATABASE_PASSWORD=$ROOT_PASSWORD \
           -e CONSUL_URL=http://$CONSUL_HOST:8500 \
           -e SERVICE_ID=1 \
           -d api-gateway
