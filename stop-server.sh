#!/bin/bash
#
docker stop `cat .apiserver.pid` 
rm .apiserver.pid
