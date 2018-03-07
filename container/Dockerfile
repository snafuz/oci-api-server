#################################################################
# oci-api-server
#
# run OCI API server 
#
# Reequires: Docker 1.9 or above
#################################################################

FROM oraclelinux:7-slim 

ARG PYTHON_VERSION=3.6.4
ARG TERRAFORM_VERSION=0.11.2-1.el7
ARG OCI_PROVIDER_VERSION=2.0.6-1.el7

RUN yum install -y unzip tar gzip gcc python-devel make libffi-devel openssl-devel python-setuptools
RUN curl -SL https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tgz | tar xvz
WORKDIR Python-${PYTHON_VERSION}
RUN ./configure &&\
 make &&\
 make install
RUN easy_install pip

RUN yum-config-manager --enable ol7_developer
RUN yum install -y terraform-${TERRAFORM_VERSION} terraform-provider-oci-${OCI_PROVIDER_VERSION}
RUN rm -rf /var/cache/yum/* &&\
    rm -rf Python-${PYTHON_VERSION}

RUN mkdir /python_scripts
COPY pip_packages.txt /python_scripts/
WORKDIR /python_scripts
RUN pip3 install -r pip_packages.txt

COPY src/ /python_scripts/

VOLUME ["/data"]
WORKDIR /data

#EXPOSE 5000

CMD  python3 /python_scripts/api-server.py config.json