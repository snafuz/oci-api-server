# OCI API SERVER
## Introduction

API server to interact with OCI via Terraform and OCI SDK

The server is providing rest API leveraging the following pyhton modules
* Flask --> microframework
* Flask-RESTPlus --> Flask extension to build REST API
* python-terraform (0.9.1) --> providea a wrapper of `terraform` command line tool
* oci (1.3.14)

This project is currently in Beta. You will use at your own risk

## Installation

The preferred way to run the server is emebded in a Container (see [here](../readme.md))


If you want to run it on your machine.

```bash
    $ git clone ...
    $ cd oci-api-server

    $ pip install virtualenv
    $ virtualenv venv-oci-api-server
    $ . venvoci-api-server/bin/activate

    (venv-oci-api-server) $ pip install -r pip_packages.txt

```
## Usage
#### Run API Server
* Setup OCI SDK environment ([OCI SDK and Tool Configuration](https://docs.us-phoenix-1.oraclecloud.com/Content/API/Concepts/sdkconfig.htm))
* Edit config.json
* Run the server
    ```bash
    $ . venvoci-api-server/bin/activate

    (venv-oci-api-server) $ python oci-api-server.py config.json
    #API Server running on http://localhost:5000/

    ```

    The server will run ***terraform init*** on the provided directory at startup

### Available APIs

#### _Terraform_

##### _plan_
shows an execution plan summary

example:

```bash
$ curl http://localhost:5000/plan
{
    "plan": [
        "add oci_core_internet_gateway.internetgateway1",
        "add oci_core_virtual_network.vcn1"
    ]
}
```
##### _apply_
builds or changes infrastructure according to Terraform configuration in the working directory

***NOTE: this will apply the configuration without asking for confirmation***

example:
```bash
$ curl http://localhost:5000/apply
{
    "apply": "Apply complete! Resources: 2 added, 0 changed, 0 destroyed."
}
```
#####_destroy_

destroy Terraform-managed infrastructure.

***NOTE: this will destroy all without asking for confirmation***

example:
```bash
$ curl http://localhost:5000/destroy
{
    "destroy": "Destroy complete! Resources: 2 destroyed."
}
```

####_OCI_
####_scale instance_

Scale up/down an existing instance.
Currently the instance is identified by compartment name + instance name. If multiple instances with the same name exist the action will fail

```
API: action/scale/compartment_name/instance_name/new_shape
```
example:
```bash
$ curl http://localhost:5001/action/scale/am-lab/instance20180214072455/VM.Standard1.1

{
    "instance_ocid": "ocid1.instance.oc1.eu-frankfurt-1.abtheljraljk5mq7lf3fpsff4k7zcjgtyuvrlkch7ozzqf4b7fx2vafjaueq"

}
```










