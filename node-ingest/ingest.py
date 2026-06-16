import paho.mqtt.client as mqtt
import json
import psycopg2
import os
import re
from datetime import datetime

DB_CONFIG = {
    "host": os.environ.get("PGHOST"),
    "database": os.environ.get("PGDATABASE"),
    "user": os.environ.get("PGUSER"),
    "password": os.environ.get("PGPASSWORD"),
}


BROKER = "node-hub"
PORT = int(os.environ.get("HUB_PORT"))

""" Debugging environment variables - make sure they are loaded correctly
print("ENV DEBUG:")
print("PGHOST =", os.getenv("PGHOST"))
print("BROKER =", "node-hub")
print("PGDATABASE =", os.getenv("PGDATABASE"))
print("PGUSER =", os.getenv("PGUSER"))
print("PGPASSWORD =", os.getenv("PGPASSWORD"))
print("PGPORT =", os.getenv("PGPORT"))
print("HUB_PORT =", os.getenv("HUB_PORT"))
 """

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)


def get_or_create_device(conn, device_name, ip_address=None):
    with conn.cursor() as cur:

        cur.execute(
            """
            SELECT device_uid
            FROM devices
            WHERE device_name = %s
            """,
            (device_name,)
        )

        row = cur.fetchone()

        if row:
            cur.execute(
                """
                UPDATE devices
                SET last_seen = NOW()
                WHERE device_name = %s
                """,
                (device_name,)
            )

            conn.commit()
            return row[0]

        cur.execute(
            """
            INSERT INTO devices (
                device_name,
                ip_address,
                last_seen
            )
            VALUES (%s, %s, NOW())
            RETURNING device_uid
            """,
            (device_name, ip_address)
        )

        device_uid = cur.fetchone()[0]
        conn.commit()

        return device_uid

def get_device_uid(conn, device_name):
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT device_uid
            FROM devices
            WHERE device_name = %s
            """,
            (device_name,)
        )

        row = cur.fetchone()
        return row[0] if row else None

def on_connect(client, userdata, flags, rc, properties=None):
    print("✅ Connected to MQTT broker, rc =", rc)
    client.subscribe("devices/#")
    client.subscribe("$SYS/#")


def on_message(client, userdata, msg):
    # Decode payload as UTF-8, but ignore errors to prevent crashes on binary data.
    raw_payload = msg.payload.decode(errors="ignore")

    try:
        payload = json.loads(raw_payload)
    except Exception:
        payload = raw_payload

    topic = msg.topic
    parts = topic.split("/")
    ip = None
    client_id = None

    if topic.startswith("$SYS/broker/log/"):
        m = re.search(
            r"New client connected from ([0-9.]+):([0-9]+) as ([^ ]+)",
            raw_payload
        )

        if not m:
            return
        
        ip = m.group(1)
        client_id = m.group(3)

        conn = get_db_connection()
        get_or_create_device(conn, client_id, ip)
        conn.close()
        return

    if topic.startswith("devices/"):
        if len(parts) < 3:
            print("❌ Invalid device topic")
            return
        
        device_name = parts[1]
        
        try:
            conn = get_db_connection()
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), " ✅ DB connected")

            device_uid = get_or_create_device(conn, device_name)
            if not device_uid:
                print("❌ Unknown device, message ignored:", device_name)
                conn.close()
                return

            if isinstance(payload, dict):
                device_timestamp = payload.get("timestamp")
            else:
                payload = {"value": payload}
                device_timestamp = None

            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO messages (device_uid, topic, payload, device_timestamp)
                    VALUES (%s, %s, %s, %s)
                """,
                    (device_uid, msg.topic, json.dumps(payload), device_timestamp),
                )

            conn.commit()
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), " ✅ Inserted message:", payload, "from device:", device_name)

        except Exception as e:
            print("❌ DB ERROR:", e)

        finally:
            if "conn" in locals():
                conn.close()


client = mqtt.Client(
    protocol=mqtt.MQTTv5, callback_api_version=mqtt.CallbackAPIVersion.VERSION2
)

client.on_connect = on_connect
client.on_message = on_message

print("✅ Connecting to MQTT...")
client.connect(BROKER, PORT, 60)

client.loop_forever()
