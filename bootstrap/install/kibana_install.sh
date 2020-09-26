#!/bin/bash

echo "Running `basename $0`"

kibana=kibana-7.7.0
kibanaf="${kibana}-linux-x86_64.tar.gz"

cd /home/vagrant/
if [[ ! -f $kibanaf ]]; then
    echo "Kibana not found, getting kibana.."
    wget --no-verbose "https://artifacts.elastic.co/downloads/kibana/${kibanaf}"
    wget --no-verbose "https://artifacts.elastic.co/downloads/kibana/${kibanaf}.sha512" 
    shasum -a 512 -c kibana-7.7.0-linux-x86_64.tar.gz.sha512
fi

if [[ ! -d $kibana ]]; then
    mkdir $kibana
    echo "Extracting kibana.."
    tar -xzf "${kibanaf}" -C "./${kibana}" --strip-components=1
    if [[ $? -eq 0 ]]; then
        cat >> /home/vagrant/.bashrc <<END
PATH=/home/vagrant/${kibana}/bin:\$PATH
END
    fi
fi