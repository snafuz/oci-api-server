# OCI API Server
## Introduction

Docker image to run API server to interact with OCI.

For the OCI API Server functions see [the server documentation](../readme.md)

## Installation

___Docker 1.8 is required___

```bash
    git clone https://github.com/snafuz/oci-api-server.git
    ./container/build.sh
```    
## Usage


#### Setup  OCI
Prepare the configuration file:

```bash
$ cp data/template_config.json data/config.json
```

Edit config.json according to your environment

#### Setup Terraform

Put you terraform file(s) in ./data

***NOTE: don't use config.json to setup terraform path if you're using Docker***

#### Run API Server
To run the server as daemon
```bash
    ./container/run-server.sh ./data
    #API Server running on http://localhost:5000/
    
```
To stop the server
```bash
    ./container/stop-server.sh
    
```

To run the server in interactive mode 

```bash
    ./container/run-server-interactive.sh ./data
    #API Server running on http://localhost:5000/
    
```
