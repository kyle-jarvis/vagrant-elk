# vagrant-elk ![version1.0.0](https://img.shields.io/badge/version-1.0.0-brightgreen)
## A VM configured with Vagrant for exploring Spark, ElasticSearch and Kibana.
### 1. Vagrant-up and running.
[Vagrant getting started](https://www.vagrantup.com/intro/getting-started).

With vagrant installed, clone this repository and initialise and provision a VM by running: `vagrant up`

### 2. Provisioning.

__ElasticSearch__

Running on port `9200`. Query the status of the ElasticCluster by e.g. 

`curl -XGET 127.0.0.1:9200/_cat/health?v`

from the guest machine.

__Kibana__

Running on port `5601`, forwarded to `5602` on the host machine. Find Kibana UI at `127.0.0.1:5602` through host machine's browser.

__Spark__

Spark `2.4.6` is installed during the provisioning process. During installation the synced folder (this projects root, guest machines' `/vagrant/`) is first checked for `spark-2.4.6-bin-hadoop.2.7.tgz`, downloadable from [here](https://spark.apache.org/downloads.html). If the file is not found a default mirror is used to `wget` get the file, sometimes this is slow, so it's recommended to manually download and include this file.

An additional jar file is downloaded as part of the provisioning to facilitate ES integration with hadoop (Spark, for the purposes of this repository). 

### 3. Demo scripts

Included in this repository are a number of scripts demonstrating some of the functionality of the VM. As part of the provisioning process, these scripts are installed into a virtual environment, and made accessible through a common entry point accessed as shown below:

`cd /vagrant/examples`

`pipenv shell`

Run the command:

`spark-es-demo --help`

You'll see there are a few options that you can try:

(1) `spark-es-demo make-spark-dataframe`

(2) `spark-es-demo spark-to-es`

(3) `spark-es-demo search-es-index`

The above commands will illustrate how to create a Spark DataFrame using the pyspark API, index the contents of a Spark DataFrame directly into an ES cluster, and finally, how to query an ES cluster using the requests lib.