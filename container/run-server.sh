#!/bin/bash
#
#run the server as daemon use docker ps to see the status

CONFIG_PATH=$PWD
if [ -n "$1" ] 
then
    CONFIG_PATH="$(cd "$(dirname "$1")"; pwd)/$(basename "$1")"
fi

docker run -d --tty --rm -p 5000:5000 --volume "$CONFIG_PATH":/data  --volume "$HOME/.oci":/root/.oci oci-api-server  > /tmp/ociapiserver.pid
