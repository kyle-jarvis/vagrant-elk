#!/bin/bash

kibana=kibana-7.7.0-linux-x86_64.tar.gz
cd /home/vagrant/
if [[ ! -f $kibana ]]; then
    wget --quiet https://artifacts.elastic.co/downloads/kibana/$kibana
    wget --quiet "https://artifacts.elastic.co/downloads/kibana/${kibana}.sha512" 
    shasum -a 512 -c kibana-7.7.0-linux-x86_64.tar.gz.sha512
fi

if [[ ! -d $es ]]; then
    tar -xzf kibana-7.7.0-linux-x86_64.tar.gz
    if [[ $? -eq 0 ]]; then
        cat >> /home/vagrant/.bashrc <<END
PATH=/home/vagrant/kibana-7.7.0/bin:\$PATH
END
fi
fi