#!/bin/bash

es=elasticsearch-7.7.0-linux-x86_64.tar.gz
cd /home/vagrant/
if [[ ! -f $es ]]; then
    wget --quiet https://artifacts.elastic.co/downloads/elasticsearch/$es
    wget --quiet "https://artifacts.elastic.co/downloads/elasticsearch/${es}.sha512"
    shasum -a 512 -c elasticsearch-7.7.0-linux-x86_64.tar.gz.sha512 
fi

tar -xzf elasticsearch-7.7.0-linux-x86_64.tar.gz

cat >> /home/vagrant/.bashrc <<END
# add for anaconda install
PATH=/home/vagrant/elasticsearch-7.7.0/bin:\$PATH
JAVA_HOME="/usr/lib/jvm/java-8-openjdk-amd64/"
END

#cd elasticsearch-7.7.0/ 