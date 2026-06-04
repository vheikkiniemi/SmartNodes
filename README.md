

## Handling database (node-vault)

1. Creating node-vault container
```bash
docker compose up -d --build node-vault
```

2. Connecting to the Database
```bash
docker exec -it node-vault psql -U vault_dbuser -d vault_db
```

3. Checking if the tables exists
```bash
vault_db=# \dt
            List of relations
 Schema |   Name   | Type  |    Owner
--------+----------+-------+--------------
 public | devices  | table | vault_dbuser
 public | messages | table | vault_dbuser
(2 rows)

vault_db=#
```

4. Verifying the tables content
```bash
vault_db=# SELECT * FROM devices;
 id | created_at | device_id | device_name | api_key | role | ip_address | location | last_seen
----+------------+------------+-------------+---------+------+------------+----------+-----------
(0 rows)

vault_db=# SELECT * FROM messages;
 id | recorded_at | device_timestamp | device_id | topic | payload | qos | retain
----+-------------+------------------+-----------+-------+---------+-----+--------
(0 rows)

vault_db=#
```

5. Deleting Content (Optional)
```bash
vault_db=# DELETE FROM devices;
DELETE 0
vault_db=# DELETE FROM messages;
DELETE 0
vault_db=#
```

6. Closing the database connection
```bash
vault_db=# \q
```

7. Deleting the database (Optional)

```bash
docker compose down node-vault -v
```

Use `-v` only if you are OK with **losing all PostgreSQL data** for this project.