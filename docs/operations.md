# Operations

This page contains the most common commands used to manage the SmartNodes platform during development and daily operation.

---

# node-hub (MQTT Broker)

## Start

```bash
docker compose up -d --build node-hub
```

## Stop

```bash
docker compose stop node-hub
```

## Restart

```bash
docker compose restart node-hub
```

## View logs

```bash
docker logs -f node-hub
```

## Open shell

```bash
docker exec -it node-hub /bin/sh
```

## Subscribe to device topics

```bash
docker exec -it node-hub \
mosquitto_sub -h node-hub \
-t 'devices/#' -v
```

## Subscribe to broker events

```bash
docker exec -it node-hub \
mosquitto_sub -h node-hub \
-t '$SYS/broker/log/#' -v
```

## List Dynamic Security clients

```bash
docker exec -it node-hub \
mosquitto_ctrl \
-h node-hub \
-u "$DYNSEC_ADMIN_USER" \
-P "$DYNSEC_ADMIN_PASS" \
dynsec listClients
```

---

# node-ingest (Message Ingestion)

## Start

```bash
docker compose up -d --build node-ingest
```

## Stop

```bash
docker compose stop node-ingest
```

## Restart

```bash
docker compose restart node-ingest
```

## View logs

```bash
docker logs -f node-ingest
```

## Open shell

```bash
docker exec -it node-ingest /bin/bash
```

---

# node-vault (PostgreSQL)

## Start

```bash
docker compose up -d --build node-vault
```

## Stop

```bash
docker compose stop node-vault
```

## Restart

```bash
docker compose restart node-vault
```

## View logs

```bash
docker logs -f node-vault
```

## Open PostgreSQL

```bash
docker exec -it node-vault \
psql -U vault_dbuser -d vault_db
```

## Open shell

```bash
docker exec -it node-vault /bin/bash
```

---

# node-gateway (REST API)

## Start

```bash
docker compose up -d --build node-gateway
```

## Stop

```bash
docker compose stop node-gateway
```

## Restart

```bash
docker compose restart node-gateway
```

## View logs

```bash
docker logs -f node-gateway
```

## Open shell

```bash
docker exec -it node-gateway /bin/sh
```

---

# Entire Platform

## Build everything

```bash
docker compose up -d --build
```

## Start existing containers

```bash
docker compose start
```

## Stop all containers

```bash
docker compose stop
```

## Restart all containers

```bash
docker compose restart
```

## Shut down the platform

```bash
docker compose down
```

## Remove containers and volumes

```bash
docker compose down --volumes
```

## View running containers

```bash
docker compose ps
```

## View all logs

```bash
docker compose logs
```

## Follow logs

```bash
docker compose logs -f
```

---

# Network Diagnostics

## Monitor MQTT traffic

```bash
sudo tcpdump -i any -nn port 1883
```

## List Docker containers

```bash
docker ps
```

## List Docker volumes

```bash
docker volume ls
```

## List Docker networks

```bash
docker network ls
```
