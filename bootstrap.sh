#!/bin/bash
set -o errexit
set -o nounset

function echotask() {
    text=$1
    echo -e "\033[1;34m==>\033[0m \033[1m${text}\033[0m"
}

function promptupdate() {
    echo 'Already downloaded. Do you wish to download the latest data?'
    select yn in Yes No; do
        case $yn in
            Yes) return 0;;
            No) return 1;;
        esac
    done
}

#------------------------------------------------------------------------------
echotask 'Python'

if ! python3 --version 2>/dev/null; then
    echo "Python 3 is required. Please download the latest version"
    echo "from https://www.python.org"
    exit 1
fi

#------------------------------------------------------------------------------
mkdir -p data
cd data

#------------------------------------------------------------------------------
echotask 'Open Exoplanet Catalogue'

fn=oec-systems.xml
if [ ! -e $fn ] || promptupdate; then
    echo Downloading
    url=https://github.com/OpenExoplanetCatalogue/oec_gzip/raw/master/systems.xml.gz
    curl -L -\# "$url" > $fn.gz
    echo Unzipping
    [ -e $fn ] && mv $fn $fn.bak
    gunzip -v $fn.gz
fi

#------------------------------------------------------------------------------
echotask 'Corpora'

if [ ! -e corpora ]; then
    echo Downloading
    git clone --depth=1 https://github.com/dariusk/corpora.git
elif promptupdate; then
    echo 'Fetching changes'
    pushd corpora >/dev/null
    git checkout -f master
    git pull --depth=1 origin master
    popd >/dev/null
fi

#------------------------------------------------------------------------------
echotask 'Ready to go!'
