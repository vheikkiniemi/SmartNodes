# node-vault

`node-vault` is the persistent PostgreSQL database of SmartNodes. It stores:

-   Registered devices
-   Telemetry messages
-   Device metadata
-   Historical MQTT data

## Common commands

``` bash
docker compose up -d --build node-vault
docker logs -f node-vault
```

## Connect

``` bash
docker exec -it node-vault psql -U vault_dbuser -d vault_db
```
**Alternative (Recommended)** ─► Expanded output and disabled pager improve readability:

```bash
docker exec -it node-vault psql -U vault_dbuser -d vault_db -P pager=off -P expanded=on
```

## Tables

```bash
vault_db=# \dt
```

Expected output:

```text
            List of relations
 Schema |   Name   | Type  |    Owner
--------+----------+-------+--------------
 public | devices  | table | vault_dbuser
 public | messages | table | vault_dbuser
(2 rows)
```

## Useful queries

```sql
SELECT * FROM devices;
```

```sql
SELECT * FROM messages;
```

```sql
SELECT device_name, last_seen, is_connected, disconnected_at, ip_address FROM devices;
```

```sql
SELECT recorded_at, topic, payload
FROM messages
ORDER BY recorded_at DESC
LIMIT 10;
```

### Remove all stored devices and messages

```sql
DELETE FROM devices;
DELETE FROM messages;
```