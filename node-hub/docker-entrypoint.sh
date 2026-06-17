#!/bin/sh
set -e

cp /mosquitto/config/mosquitto.conf.template /mosquitto/config/mosquitto.conf

sed -i "s|\${PGHOST}|${PGHOST}|g" /mosquitto/config/mosquitto.conf
sed -i "s|\${PGPORT}|${PGPORT}|g" /mosquitto/config/mosquitto.conf
sed -i "s|\${PGDATABASE}|${PGDATABASE}|g" /mosquitto/config/mosquitto.conf
sed -i "s|\${PGUSER}|${PGUSER}|g" /mosquitto/config/mosquitto.conf
sed -i "s|\${PGPASSWORD}|${PGPASSWORD}|g" /mosquitto/config/mosquitto.conf

exec mosquitto -c /mosquitto/config/mosquitto.conf