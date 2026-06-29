# node-hub

`node-hub` is the MQTT broker of SmartNodes.

## Responsibilities

-   Accept MQTT client connections
-   Route publish/subscribe messages
-   Manage MQTT topics
-   Provide broker logging

## Common commands

``` bash
docker compose up -d --build node-hub
docker logs -f node-hub
docker exec -it node-hub /bin/sh
```

## Useful troubleshooting

Subscribe to all device topics:

``` bash
docker exec -it node-hub mosquitto_sub -h node-hub -t 'devices/#' -v
```
