#!/usr/bin/env bash

set -e

# Note: This script should be executed manually before running mirror.yml role since ansible does not have good support
#  for different sudo passwords per host (e.g. for localhost).

if ! command -v yq &> /dev/null
then
    echo 'Error: yq could not be found. Please install it with pip or the OS package manager.'
    echo ''
    echo -e '\tGithub repository: https://github.com/kislyuk/yq'
    echo -e '\tPyPI: https://pypi.org/project/yq/'
    echo -e '\tArch linux package: https://www.archlinux.org/packages/community/any/yq/'
    echo ''
    echo 'NB: yq relies on jq - https://stedolan.github.io/jq/download/'
    exit 1
fi

yq --help | grep 'https://github.com/kislyuk/yq' &> /dev/null || (echo "Error: Not using correct yq" && exit 1)

echo "Turning off the site"
docker-compose down

echo "Detecting media dir"
media_dir=`docker-compose config | yq -r '.services.django.volumes[]' | grep '/files/media' | cut -d: -f1`
data_dir=`dirname ${media_dir}`

if [[ "$data_dir" != *".data" ]]; then
    echo "Data directory does not end with .data"
    exit 1
fi

echo "Media dir is ${media_dir}"

echo "Changing .data dir ownership to ${USER}"
sudo chown -R ${USER}: ${data_dir}

echo "Changing media dir ownership to ${USER}"
sudo chown -R ${USER}: ${media_dir}

echo "Detecting postgres data dir"
postgres_dir=`docker-compose config | yq -r '.services.postgres.volumes[]' | grep '/var/lib/postgresql/data' | cut -d: -f1`
echo echo "Postgres dir is ${postgres_dir}"

echo "Changing postgres dir ownership to ${USER}"
sudo chown -R ${USER}: ${postgres_dir}

echo "Detecting postgres mirror dir"
postgres_dir=`docker-compose config | yq -r '.services.postgres.volumes[]' | grep 'db-mirror' | cut -d: -f1`
echo "Postgres mirror dir is ${postgres_dir}"

sudo mkdir -p ${postgres_dir}
sudo chown -R ${USER}: ${postgres_dir}

echo "DONE"
