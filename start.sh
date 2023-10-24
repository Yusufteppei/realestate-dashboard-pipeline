#!bin/sh

sudo apt update
sudo apt install docker-compose -y

docker-compose build
docker-compose up

