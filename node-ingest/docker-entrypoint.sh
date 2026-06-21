#!/bin/sh
set -e

ADMIN_USER="${DYNSEC_ADMIN_USER:-admin}"
ADMIN_PASS="${DYNSEC_ADMIN_PASS:?DYNSEC_ADMIN_PASS is missing}"

: "${INGESTORUSER:?INGESTORUSER is missing}"
: "${INGESTORPASS:?INGESTORPASS is missing}"

echo "Creating ingestor role..."
mosquitto_ctrl -h node-hub -u "$ADMIN_USER" -P "$ADMIN_PASS" dynsec createRole ingestor-role || true

echo "Adding ingestor ACLs..."
mosquitto_ctrl -h node-hub -u "$ADMIN_USER" -P "$ADMIN_PASS" dynsec addRoleACL ingestor-role subscribePattern "devices/#" allow 10 || true
mosquitto_ctrl -h node-hub -u "$ADMIN_USER" -P "$ADMIN_PASS" dynsec addRoleACL ingestor-role publishClientReceive "devices/#" allow 10 || true 
mosquitto_ctrl -h node-hub -u "$ADMIN_USER" -P "$ADMIN_PASS" dynsec addRoleACL ingestor-role subscribePattern '$SYS/#' allow 10 || true
mosquitto_ctrl -h node-hub -u "$ADMIN_USER" -P "$ADMIN_PASS" dynsec addRoleACL ingestor-role publishClientReceive '$SYS/#' allow 10 || true

echo "Creating ingestor client..."
if ! mosquitto_ctrl -h node-hub -u "$ADMIN_USER" -P "$ADMIN_PASS" dynsec listClients | grep -qx "$INGESTORUSER"; then
    printf '\n' | mosquitto_ctrl -h node-hub -u "$ADMIN_USER" -P "$ADMIN_PASS" dynsec createClient "$INGESTORUSER"
else
    echo "Client $INGESTORUSER already exists."
fi

mosquitto_ctrl -h node-hub -u "$ADMIN_USER" -P "$ADMIN_PASS" dynsec setClientPassword "$INGESTORUSER" "$INGESTORPASS"
mosquitto_ctrl -h node-hub -u "$ADMIN_USER" -P "$ADMIN_PASS" dynsec setClientId "$INGESTORUSER" "$INGESTORUSER"
mosquitto_ctrl -h node-hub -u "$ADMIN_USER" -P "$ADMIN_PASS" dynsec addClientRole "$INGESTORUSER" ingestor-role 10 || true

echo "Configure the Anonymous access..."
mosquitto_ctrl -h node-hub -u "$ADMIN_USER" -P "$ADMIN_PASS" dynsec createRole device_anonymous_role
mosquitto_ctrl -h node-hub -u "$ADMIN_USER" -P "$ADMIN_PASS" dynsec addRoleACL device_anonymous_role publishClientSend "devices/#" allow 10
mosquitto_ctrl -h node-hub -u "$ADMIN_USER" -P "$ADMIN_PASS" dynsec addRoleACL device_anonymous_role subscribePattern "devices/#" allow 10
mosquitto_ctrl -h node-hub -u "$ADMIN_USER" -P "$ADMIN_PASS" dynsec createGroup anonymous
mosquitto_ctrl -h node-hub -u "$ADMIN_USER" -P "$ADMIN_PASS" dynsec addGroupRole anonymous device_anonymous_role
mosquitto_ctrl -h node-hub -u "$ADMIN_USER" -P "$ADMIN_PASS" dynsec setAnonymousGroup anonymous

echo "Done."

exec python -u ingest.py