# node-ingest

The ingestion service subscribes to MQTT topics, validates incoming
messages and stores them in PostgreSQL.

## Responsibilities

-   Subscribe to MQTT topics
-   Parse payloads
-   Register devices
-   Store telemetry

## Commands

``` bash
docker compose up -d --build node-ingest
docker logs -f node-ingest
docker exec -it node-ingest /bin/bash
```
