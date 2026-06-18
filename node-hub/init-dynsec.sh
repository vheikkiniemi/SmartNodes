#!/bin/sh
set -e

ADMIN_USER="${DYNSEC_ADMIN_USER:-admin}"
ADMIN_PASS="${DYNSEC_ADMIN_PASS:?DYNSEC_ADMIN_PASS is missing}"

: "${INGESTORUSER:?INGESTORUSER is missing}"
: "${INGESTORPASS:?INGESTORPASS is missing}"

echo "Creating ingestor role..."
mosquitto_ctrl -h localhost -u "$ADMIN_USER" -P "$ADMIN_PASS" dynsec createRole ingestor-role || true

echo "Adding ingestor ACLs..."
mosquitto_ctrl -h localhost -u "$ADMIN_USER" -P "$ADMIN_PASS" dynsec addRoleACL ingestor-role subscribePattern "devices/#" allow 10 || true
mosquitto_ctrl -h localhost -u "$ADMIN_USER" -P "$ADMIN_PASS" dynsec addRoleACL ingestor-role publishClientReceive "devices/#" allow 10 || true 
mosquitto_ctrl -h localhost -u "$ADMIN_USER" -P "$ADMIN_PASS" dynsec addRoleACL ingestor-role subscribePattern '$SYS/#' allow 10 || true
mosquitto_ctrl -h localhost -u "$ADMIN_USER" -P "$ADMIN_PASS" dynsec addRoleACL ingestor-role publishClientReceive '$SYS/#' allow 10 || true

echo "Creating ingestor client..."
if ! mosquitto_ctrl -h localhost -u "$ADMIN_USER" -P "$ADMIN_PASS" dynsec listClients | grep -qx "$INGESTORUSER"; then
    printf '\n' | mosquitto_ctrl -h localhost -u "$ADMIN_USER" -P "$ADMIN_PASS" dynsec createClient "$INGESTORUSER"
else
    echo "Client $INGESTORUSER already exists."
fi

mosquitto_ctrl -h localhost -u "$ADMIN_USER" -P "$ADMIN_PASS" dynsec setClientPassword "$INGESTORUSER" "$INGESTORPASS"
mosquitto_ctrl -h localhost -u "$ADMIN_USER" -P "$ADMIN_PASS" dynsec setClientId "$INGESTORUSER" "$INGESTORUSER"
mosquitto_ctrl -h localhost -u "$ADMIN_USER" -P "$ADMIN_PASS" dynsec addClientRole "$INGESTORUSER" ingestor-role 10 || true

#echo "Creating anonymous device role..."
#mosquitto_ctrl -h localhost -u "$ADMIN_USER" -P "$ADMIN_PASS" dynsec createRole anonymous-device-role || true

#echo "Adding anonymous device ACLs..."
echo "Configure the Anonymous Group"
mosquitto_ctrl -h localhost -u "$ADMIN_USER" -P "$ADMIN_PASS" dynsec createRole device_anonymous_role
echo "Allow anonymous users to publish to device topics"
mosquitto_ctrl -h localhost -u "$ADMIN_USER" -P "$ADMIN_PASS" dynsec addRoleACL device_anonymous_role publishClientSend "devices/#" allow 10
echo "Allow anonymous users to subscribe to device topics"
mosquitto_ctrl -h localhost -u "$ADMIN_USER" -P "$ADMIN_PASS" dynsec addRoleACL device_anonymous_role subscribePattern "devices/#" allow 10
echo "Attach the Role to the Anonymous Group"
mosquitto_ctrl -h localhost -u "$ADMIN_USER" -P "$ADMIN_PASS" dynsec addGroupRole anonymous device_anonymous_role
echo "Explicitly Set the Anonymous Group"
mosquitto_ctrl -h localhost -u "$ADMIN_USER" -P "$ADMIN_PASS" dynsec setAnonymousGroup anonymous

#mosquitto_ctrl -h localhost -u "$ADMIN_USER" -P "$ADMIN_PASS" dynsec addRoleACL anonymous-device-role publishClientSend "devices/#" allow 10 || true
#mosquitto_ctrl -h localhost -u "$ADMIN_USER" -P "$ADMIN_PASS" dynsec addRoleACL anonymous-device-role subscribePattern "devices/#" allow 10 || true
#mosquitto_ctrl -h localhost -u "$ADMIN_USER" -P "$ADMIN_PASS" dynsec addRoleACL anonymous-device-role publishClientReceive "devices/#" allow 10 || true

#echo "Creating unauthenticated group..."
#mosquitto_ctrl -h localhost -u "$ADMIN_USER" -P "$ADMIN_PASS" dynsec createGroup unauthenticated || true

#echo "Adding anonymous device role to unauthenticated group..."
#mosquitto_ctrl -h localhost -u "$ADMIN_USER" -P "$ADMIN_PASS" dynsec addGroupRole unauthenticated anonymous-device-role 10 || true

echo "Done."