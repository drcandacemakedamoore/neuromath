#!/usr/bin/env bash

set -xe

PROJECT_DIR=$(echo $PWD | sed 's#/[^/]\+$##')

docker rm -f imarker-test ||:

docker run --rm --name imarker-test \
       -v "$PROJECT_DIR:/opt/image-marker" \
       -p 8080:8080 imarker-test sleep infinity &

while :
do
    found=$(docker ps -a | grep imarker-test ||:)
    if [ "$found" != "" ]; then
        break
    fi
    echo waiting for container to start
    sleep 1
done

docker exec imarker-test sh -c 'cd /opt/image-marker && python setup.py install'

docker exec imarker-test imarker
