#!/bin/bash
#
docker stop `cat /tmp/ociapiserver.pid` 
rm /tmp/ociapiserver.pid
