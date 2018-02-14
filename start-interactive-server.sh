#!/bin/bash
#
#run the server in interactive mode
CONFIG_PATH=$PWD
if [ -n "$1" ] 
then
    CONFIG_PATH="$(cd "$(dirname "$1")"; pwd)/$(basename "$1")"
fi
 
docker run --interactive --tty --rm -p 5000:5000 --volume "$CONFIG_PATH":/data  --volume "$HOME/.oci":/root/.oci oci-api-server 
