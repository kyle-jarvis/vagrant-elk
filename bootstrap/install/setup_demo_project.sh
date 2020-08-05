#!/bin/bash

. /home/vagrant/variables.sh

PROJECT_DIR=/home/vagrant/demoProject

mkdir ${PROJECT_DIR}
cd ${PROJECT_DIR}

if [[ ! -z $(command -v pipenv) ]]; then
    echo "Creating venv in ${PROJECT_DIR}.."
    CMD="pipenv install $PYSPARK_TAR_PATH --skip-lock"
    echo $CMD
    eval $CMD
fi
