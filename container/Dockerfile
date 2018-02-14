#################################################################
# oci-api-server
#
# run API server interacting with terraform to provision 
# the demo environment
#################################################################

FROM oraclelinux:7-slim

ARG TERRAFORM_VERSION=0.11.2-1.el7
ARG OCI_PROVIDER_VERSION=2.0.6-1.el7

RUN yum-config-manager --enable ol7_developer
RUN yum -y install terraform-${TERRAFORM_VERSION} terraform-provider-oci-${OCI_PROVIDER_VERSION} 
    

RUN yum -y install python-setuptools
RUN rm -rf /var/cache/yum/*

RUN curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"
RUN python get-pip.py

RUN mkdir /python_scripts
ADD api-server/pip_packages.txt /python_scripts
WORKDIR /python_scripts
RUN pip install -r pip_packages.txt

COPY api-server/src/ /python_scripts/
#ADD api-server.py /python_scripts


VOLUME ["/data"]
WORKDIR /data

#EXPOSE 5000

CMD  python /python_scripts/api-server.py config.json