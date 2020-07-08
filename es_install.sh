#!/bin/bash

es=elasticsearch-7.7.0-linux-x86_64.tar.gz
cd /home/vagrant/
if [[ ! -f $es ]]; then
    wget --quiet https://artifacts.elastic.co/downloads/elasticsearch/$es
    wget --quiet "https://artifacts.elastic.co/downloads/elasticsearch/${es}.sha512"
    shasum -a 512 -c elasticsearch-7.7.0-linux-x86_64.tar.gz.sha512 
fi

if [[ ! -d $es ]]; then
    tar -xzf elasticsearch-7.7.0-linux-x86_64.tar.gz
    if [[ $? -eq 0 ]]; then
        cat >> /home/vagrant/.bashrc <<END
PATH=/home/vagrant/elasticsearch-7.7.0/bin:\$PATH
END
fi
fi
