#!/bin/sh
set -e

PASSWORD_FILE="/mosquitto/config/mqtt.pass"

if [ -z "$INGESTORUSER" ]; then
  echo "ERROR: INGESTORUSER is missing"
  exit 1
fi

if [ -z "$INGESTORPASS" ]; then
  echo "ERROR: INGESTORPASS is missing"
  exit 1
fi

# Create password file from environment variables
mosquitto_passwd -b -c "$PASSWORD_FILE" "$INGESTORUSER" "$INGESTORPASS"

# Secure permissions
chmod 600 "$PASSWORD_FILE"
chown mosquitto:mosquitto "$PASSWORD_FILE"

exec mosquitto -c /mosquitto/config/mosquitto.conf