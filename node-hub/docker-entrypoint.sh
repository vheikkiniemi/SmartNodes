#!/bin/sh
set -e

DYNSEC_FILE="/mosquitto/config/dynamic-security.json"


if [ -z "$DYNSEC_ADMIN_USER" ]; then
  echo "ERROR: DYNSEC_ADMIN_USER is missing"
  exit 1
fi

if [ -z "$DYNSEC_ADMIN_PASS" ]; then
  echo "ERROR: DYNSEC_ADMIN_PASS is missing"
  exit 1
fi

if [ ! -s "$DYNSEC_FILE" ]; then
  echo "Initializing Mosquitto Dynamic Security..."
  rm -f "$DYNSEC_FILE"
  mosquitto_ctrl dynsec init "$DYNSEC_FILE" "$DYNSEC_ADMIN_USER" "$DYNSEC_ADMIN_PASS"
  chown mosquitto:mosquitto "$DYNSEC_FILE"
  chmod 600 "$DYNSEC_FILE"
else
  echo "Dynamic Security file already exists, skipping init."
fi

: '
# Initialize Dynamic Security only if config does not exist
if [ ! -f "$DYNSEC_FILE" ]; then
  echo "Initializing Mosquitto Dynamic Security..."

  mosquitto_ctrl dynsec init "$DYNSEC_FILE" "$DYNSEC_ADMIN_USER" "$DYNSEC_ADMIN_PASS"

  chmod 600 "$DYNSEC_FILE"
  chown mosquitto:mosquitto "$DYNSEC_FILE"
else
  echo "Dynamic Security config already exists."
fi

# Create ingestor client if credentials are provided

if [ -n "$INGESTORUSER" ] && [ -n "$INGESTORPASS" ]; then
  echo "Creating ingestor client..."

  mosquitto_ctrl dynsec createClient "$INGESTORUSER" || true
  mosquitto_ctrl dynsec setClientPassword "$INGESTORUSER" "$INGESTORPASS"
  mosquitto_ctrl dynsec setClientId "$INGESTORUSER" "$INGESTORUSER"
  mosquitto_ctrl dynsec addClientRole "$INGESTORUSER" ingestor-role 10 || true
fi
'

exec mosquitto -c /mosquitto/config/mosquitto.conf