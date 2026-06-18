#!/bin/sh
set -e

ADMIN_USER="${DYNSEC_ADMIN_USER:-admin}"

: "${INGESTORUSER:?INGESTORUSER is missing}"
: "${INGESTORPASS:?INGESTORPASS is missing}"

echo "Creating ingestor role..."
mosquitto_ctrl -h localhost -u "$ADMIN_USER" dynsec createRole ingestor-role || true

echo "Adding ACLs..."
mosquitto_ctrl -h localhost -u "$ADMIN_USER" dynsec addRoleACL ingestor-role subscribePattern "devices/#" allow 10 || true
mosquitto_ctrl -h localhost -u "$ADMIN_USER" dynsec addRoleACL ingestor-role publishClientReceive "devices/#" allow 10 || true

echo "Creating ingestor client..."
mosquitto_ctrl -h localhost -u "$ADMIN_USER" dynsec createClient "$INGESTORUSER" -i "$INGESTORUSER" || true
mosquitto_ctrl -h localhost -u "$ADMIN_USER" dynsec setClientPassword "$INGESTORUSER" "$INGESTORPASS"
mosquitto_ctrl -h localhost -u "$ADMIN_USER" dynsec addClientRole "$INGESTORUSER" ingestor-role 10 || true

echo "Done."