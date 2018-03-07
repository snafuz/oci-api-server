#!/bin/bash

cd "$(dirname "$0")"
docker build  -f Dockerfile -t oci-api-server:latest ../