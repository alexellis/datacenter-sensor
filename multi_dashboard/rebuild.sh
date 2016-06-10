#!/bin/bash
git pull
docker build -t multi .
docker run -e REDIS_HOST=192.168.0.38 --rm -ti --privileged multi
