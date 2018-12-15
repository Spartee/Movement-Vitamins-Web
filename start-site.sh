#!/bin/bash

docker-compose build
docker-compose up -d
docker-compose run --rm web python ./instance/db_create.py


