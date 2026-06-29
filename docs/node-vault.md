# node-vault

PostgreSQL database used by SmartNodes.

## Tables

-   devices
-   messages

## Connect

``` bash
docker exec -it node-vault psql -U vault_dbuser -d vault_db
```

## Useful queries

``` sql
SELECT * FROM devices;

SELECT recorded_at, topic, payload
FROM messages
ORDER BY recorded_at DESC
LIMIT 10;
```
