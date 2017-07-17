#!/bin/bash

set -eux

echo "DB startup..."
until mysql -u root -h 127.0.0.1 -P 3306 -e 'show databases;'; do
  >&2 echo "MySQL is unavailable - sleeping"
  sleep 5
done

>&2 echo "MySQL now accepts connections, creating database..."

echo "EMG Run tests..."

python setup.py test