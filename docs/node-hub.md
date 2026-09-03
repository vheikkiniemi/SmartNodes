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

## Connecting (using example script)

```bash
cd examples
python .\subscriber.py
```

The subscriber listens for MQTT messages published to configured topics.

## Publishing (using example script)

```bash
cd examples
python .\publisher.py
```

The publisher sends example telemetry data to the broker.

## Useful troubleshooting

Subscribe to all device topics:

``` bash
docker exec -it node-hub mosquitto_sub -h node-hub -t 'devices/#' -v
```