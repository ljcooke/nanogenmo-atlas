#!/bin/bash
set -o errexit
set -o nounset

function echotask() {
    text=$1
    echo -e "\033[1;34m==>\033[0m \033[1m${text}\033[0m"
}

basedir=$PWD

#------------------------------------------------------------------------------
echotask 'Open Exoplanet Catalogue'
cd corpus/OpenExoplanetCatalogue
if [ -e systems.xml ]; then
    echo Downloaded
else
    ./download.py
fi
cd "$basedir"

#------------------------------------------------------------------------------
echotask 'Done'
