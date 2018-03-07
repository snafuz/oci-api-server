#OCI Scripts

###_oci_wrapper package_

####Installation

* Setup a virtualenv and install the dependencies.

```bash
    $ git clone https://github.com/snafuz/oci-api-server.git
    $ cd oci-api-server/src/wrappers/oci_scripts

    $ pip install virtualenv
    $ virtualenv venv-oci-scripts
    $ . venv-oci-scripts/bin/activate

    (venv-oci-scripts) $ pip install -r pip_oci_scripts_packages.txt

```

* Setup OCI SDK environment ([OCI SDK and Tool Configuration](https://docs.us-phoenix-1.oraclecloud.com/Content/API/Concepts/sdkconfig.htm))



####Instance Scale up/down

####*Usage*

Prepare the configuration file:
```bash
$ cp data/template_config.json oci-api-server/src/wrappers/oci_scripts/config.json
```

Insert:
  * new shape
  * compartment OCID
  * instance OCID

```
"oci":{
    "profile" : "(OPTIONAL) select a specific configuration in  ~/.oci/config",

    "actions":{
      "scale":{
        "new_shape":"new shape name",
        "compartment_ocid" :"compartment OCID cointaining the instance to be scaled ",
        "instance_ocid":"instance OCID"
      }
    }
  }
´´´

Run the scale up/down script

 ´´´bash
 python oci_wrapper.py config.json
 ´´´