#!/bin/bash

spark=spark-2.4.6-bin-hadoop2.7
sparkfile=${spark}.tgz
spark_url=https://apache.mirrors.nublue.co.uk/spark/spark-2.4.6

cd /home/vagrant/

if [[ ! -f ${sparkfile} ]]; then
    if [[ -f /vagrant/${spark}.tgz ]]; then
        echo "Found ${spark}.tgz at /vagrant/${spark}.tgz"
        cp /vagrant/${spark}.tgz /home/vagrant/${spark}.tgz
    else
        echo "WGetting ${sparkfile} from ${spark_url}"
        wget --quiet ${spark_url}/${sparkfile}
    fi
else
    echo "${sparkfile} already exists."
fi

if [[ ! -d $spark ]]; then
    tar -xzf ${sparkfile}
    if [[ $? -eq 0 ]]; then
        cat >> /home/vagrant/.bashrc <<END
export SPARK_HOME=/home/vagrant/${spark}
PATH=/home/vagrant/${spark}/bin:\$PATH
END
fi
fi

es_hdp=elasticsearch-hadoop-7.8.0
es_hdp_file=${es_hdp}.zip
es_hdp_url=https://artifacts.elastic.co/downloads/elasticsearch-hadoop/${es_hdp_file}

if [[ ! -f ${es_hdp_file} ]]; then
    echo "WGetting ${es_hdp_file} from ${es_hdp_url}"
    wget --quiet ${es_hdp_url}
fi

if [[ ! -d ${es_hdp} ]]; then
    unzip ${es_hdp_file}
    if [[ $? -eq 0 ]]; then
        cat >> /home/vagrant/.bashrc <<END
export ES_HDP_JAR=/home/vagrant/${es_hdp}/dist/elasticsearch-hadoop-7.8.0.jar
END
fi
fi

PYTHON_DIR="/home/vagrant/${spark}/python"
PYTHON_DIST_DIR="${PYTHON_DIR}/dist"

if [[ -d ${PYTHON_DIR} ]]; then
    cd ${PYTHON_DIR}
    if [[ ! -z $(command -v python3) ]]; then
        echo "Building pyspark..."
        python3 setup.py sdist
        if [[ $? -eq 0 ]]; then 
            DIST_BUILT=true
        fi
    else
        echo "python3 not found."
    fi
else
    echo "${PYTHON_DIR} not found"
fi

if [[ ! -z ${DIST_BUILT} ]]; then
    cd ${PYTHON_DIST_DIR}
    PYSPARK_TAR_FILE="$(ls | grep -o '.*.tar.gz')"
    PYSPARK_TAR_PATH="$(realpath ${PYSPARK_TAR_FILE})"
    cat >> /home/vagrant/.bashrc <<END
export PYSPARK_TAR_PATH=${PYSPARK_TAR_PATH}
END
    cat >> /home/vagrant/variables.sh <<END
PYSPARK_TAR_PATH=${PYSPARK_TAR_PATH}
END
fi



