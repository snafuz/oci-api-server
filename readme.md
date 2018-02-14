# OCI API Server
## Introduction

Docker image to run API server to interact with OCI.

For the OCI API Server functions see [the server documentation](api-server/readme.md)

## Installation


```bash
    git clone ...
    ./build.sh
```    
## Usage
#### Configuration for OCI
```bash
$ cp ./api-server/data/template_config.json ./data/config.json
```
Edit config.json according to your environment 
#### Configuration for Terraform

Put you terraform file(s) in ./data  

***NOTE: don't use config.json to setup terraform path if you're using Docker image***

#### Run API Server
To run the server as daemon
```bash
    ./run-server.sh ./data
    #API Server running on http://localhost:5000/
    
```
To stop the server
```bash
    ./stop-server.sh
    
```

To run the server in interactive mode 

```bash
    ./run-server-interactive.sh ./data
    #API Server running on http://localhost:5000/
    
```
