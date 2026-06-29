# Troubleshooting

## Check running containers

``` bash
docker compose ps
```

## View logs

``` bash
docker logs -f node-hub
docker logs -f node-ingest
docker logs -f node-vault
docker logs -f node-gateway
```

## Check MQTT traffic

``` bash
sudo tcpdump -i any -nn port 1883
```

## Check database

``` bash
docker exec -it node-vault psql -U vault_dbuser -d vault_db
```
