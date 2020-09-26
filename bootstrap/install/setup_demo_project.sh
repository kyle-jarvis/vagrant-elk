#!/bin/bash

echo "Running `basename $0`"

. /home/vagrant/variables.sh

PROJECT_DIR=/vagrant/examples

mkdir ${PROJECT_DIR}
cd ${PROJECT_DIR}

if [[ -f ./Pipfile ]]; then
    rm -f ./Pipfile
fi

if [[ -f ./Pipfile.lock ]]; then
    rm -f ./Pipfile.lock
fi

if [[ ! -z $(command -v pipenv) ]]; then
    echo "Creating venv in ${PROJECT_DIR}.."
    CMD="pipenv install $PYSPARK_TAR_PATH --skip-lock"
    echo $CMD
    eval $CMD
    CMD="pipenv install . --skip-lock"
    echo $CMD
    eval $CMD
    cat << EOF > requirements.txt
click
EOF
    pipenv install -r ./requirements.txt --skip-lock

fi
