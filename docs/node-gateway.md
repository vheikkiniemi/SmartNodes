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
```
