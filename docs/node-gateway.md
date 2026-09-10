# node-gateway

REST API for accessing SmartNodes data.

## Example endpoints

``` text
GET /api/devices
GET /api/messages
GET /api/devices/{device_uid}
GET /api/messages/{device_uid}
```

## Commands

``` bash
docker compose up -d --build node-gateway
docker logs -f node-gateway
docker exec -it node-gateway /bin/sh
```

## Testing

The database should already contain devices and telemetry messages.

**Retrieve all devices**

```bash
curl http://localhost:8080/api/devices
```

**Retrieve all messages**

```bash
curl http://localhost:8080/api/messages
```

### Example Device Queries

**Retrieve device by UID**

```bash
curl http://localhost:8080/api/devices/d325e86d-040b-4608-9a6a-8413434e5966
```

**Retrieve messages by device UID**

```bash
curl http://localhost:8080/api/messages/d325e86d-040b-4608-9a6a-8413434e5966
```