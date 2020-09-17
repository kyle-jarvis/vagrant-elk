#!/bin/bash

echo "Running `basename $0`"

es=elasticsearch-7.7.0
esf="${es}-linux-x86_64.tar.gz"

cd /home/vagrant/

# If the file does not exist in the synced folder, try to download it.
if [[ ! -f $esf ]]; then
    echo "ES not found, getting ES.."
    wget --no-verbose https://artifacts.elastic.co/downloads/elasticsearch/$esf
    wget --no-verbose "https://artifacts.elastic.co/downloads/elasticsearch/${esf}.sha512"
    shasum -a 512 -c "${esf}.sha512" 
fi

# If there is no directory, unzip the contents of the archive.
if [[ ! -d $es ]]; then
    mkdir $es
    tar -xzf ${esf} -C "./${es}" --strip-components=1
    if [[ $? -eq 0 ]]; then
        cat >> /home/vagrant/.bashrc <<END
PATH=/home/vagrant/${es}/bin:\$PATH
END
    fi
fi
