#!/bin/bash
set -e

psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" <<EOF
INSERT INTO devices (
    device_name,
    mqtt_password_hash,
    role
)
VALUES (
    '${INGESTORUSER}',
    crypt('${INGESTORPASS}', gen_salt('bf')),
    'ingestor'
)
ON CONFLICT (device_name)
DO UPDATE SET
    mqtt_password_hash = EXCLUDED.mqtt_password_hash,
    role = EXCLUDED.role;
EOF