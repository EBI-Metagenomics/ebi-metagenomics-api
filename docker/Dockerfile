FROM centos:centos7
MAINTAINER EBI Metagenomics Team <olat@ebi.ac.uk>


RUN yum -y update; yum clean all

RUN yum -y install epel-release gcc bzip2 git wget; yum clean all

RUN yum -y install python34 python34-devel python34-setuptools
RUN easy_install-3.4 pip
RUN pip3 install -U pip virtualenv setuptools

# Install mysql tools
RUN yum -y install mysql mysql-devel

# Add user
RUN useradd emg

ADD run.sh /tmp/docker/run.sh
RUN chmod a+x /tmp/docker/run.sh
RUN chown emg:emg /tmp/docker/run.sh

USER emg

ENV HOME /home/emg
WORKDIR /home/emg

RUN mkdir -p $HOME/emg

ENTRYPOINT ["/tmp/docker/run.sh"]
