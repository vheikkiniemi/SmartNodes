#!/bin/sh
set -e

BROKER_HOST="localhost"
ADMIN_USER="${DYNSEC_ADMIN_USER:-admin}"

if [ -z "$INGESTORUSER" ]; then
  echo "ERROR: INGESTORUSER is missing"
  exit 1
fi

if [ -z "$INGESTORPASS" ]; then
  echo "ERROR: INGESTORPASS is missing"
  exit 1
fi

echo "Creating ingestor role..."
mosquitto_ctrl -h "$BROKER_HOST" -u "$ADMIN_USER" dynsec createRole ingestor-role || true

echo "Adding ACLs..."
mosquitto_ctrl -h "$BROKER_HOST" -u "$ADMIN_USER" dynsec addRoleACL ingestor-role subscribePattern allow "devices/#" 10 || true
mosquitto_ctrl -h "$BROKER_HOST" -u "$ADMIN_USER" dynsec addRoleACL ingestor-role publishClientReceive allow "devices/#" 10 || true

echo "Creating ingestor client..."
mosquitto_ctrl -h "$BROKER_HOST" -u "$ADMIN_USER" dynsec createClient "$INGESTORUSER" || true
mosquitto_ctrl -h "$BROKER_HOST" -u "$ADMIN_USER" dynsec setClientPassword "$INGESTORUSER" "$INGESTORPASS"
mosquitto_ctrl -h "$BROKER_HOST" -u "$ADMIN_USER" dynsec setClientId "$INGESTORUSER" "$INGESTORUSER"
mosquitto_ctrl -h "$BROKER_HOST" -u "$ADMIN_USER" dynsec addClientRole "$INGESTORUSER" ingestor-role 10 || true

echo "Done."