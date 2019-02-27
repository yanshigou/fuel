#!/bin/sh

./restart.sh
sudo service nginx restart
uwsgi --ini fuel_uwsgi.ini &