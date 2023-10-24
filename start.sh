#!bin/sh

sudo apt update
sudo apt install docker-compose

docker-compose build
docker-compose up

