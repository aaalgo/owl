#!/bin/bash

mkdir -p trans
rm db.sqlite3
./manage.py migrate
find images/ -type f | ./manage.py import --run
