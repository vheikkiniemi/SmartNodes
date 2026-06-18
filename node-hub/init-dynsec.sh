#!/bin/sh
set -e

ADMIN_USER="${DYNSEC_ADMIN_USER:-admin}"
ADMIN_PASS="${DYNSEC_ADMIN_PASS:?DYNSEC_ADMIN_PASS is missing}"

: "${INGESTORUSER:?INGESTORUSER is missing}"
: "${INGESTORPASS:?INGESTORPASS is missing}"

echo "Creating ingestor role..."
mosquitto_ctrl -h localhost -u "$ADMIN_USER" -P "$ADMIN_PASS" dynsec createRole ingestor-role || true  >/dev/null 2>&1;

echo "Adding ACLs..."
mosquitto_ctrl -h localhost -u "$ADMIN_USER" -P "$ADMIN_PASS" dynsec addRoleACL ingestor-role subscribePattern "devices/#" allow 10 || true  >/dev/null 2>&1;
mosquitto_ctrl -h localhost -u "$ADMIN_USER" -P "$ADMIN_PASS" dynsec addRoleACL ingestor-role publishClientReceive "devices/#" allow 10 || true  >/dev/null 2>&1;

echo "Creating ingestor client..."
if ! mosquitto_ctrl -h localhost -u "$ADMIN_USER" -P "$ADMIN_PASS" dynsec getClient "$INGESTORUSER" >/dev/null 2>&1; then
    printf '\n' | mosquitto_ctrl -h localhost -u "$ADMIN_USER" -P "$ADMIN_PASS" dynsec createClient "$INGESTORUSER"
fi

mosquitto_ctrl -h localhost -u "$ADMIN_USER" -P "$ADMIN_PASS" dynsec setClientPassword "$INGESTORUSER" "$INGESTORPASS"
mosquitto_ctrl -h localhost -u "$ADMIN_USER" -P "$ADMIN_PASS" dynsec setClientId "$INGESTORUSER" "$INGESTORUSER"
mosquitto_ctrl -h localhost -u "$ADMIN_USER" -P "$ADMIN_PASS" dynsec addClientRole "$INGESTORUSER" ingestor-role 10 || true

echo "Done."