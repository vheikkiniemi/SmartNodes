import paho.mqtt.client as mqtt
import json
import psycopg2
import os

DB_CONFIG = {
    "host": os.environ.get("PGHOST"),
    "database": os.environ.get("PGDATABASE"),
    "user": os.environ.get("PGUSER"),
    "password": os.environ.get("PGPASSWORD")
}


BROKER = "node-hub"
PORT = int(os.environ.get("HUB_PORT"))

print("ENV DEBUG:")
print("PGHOST =", os.getenv("PGHOST"))
print("BROKER =", "node-hub")
print("PGDATABASE =", os.getenv("PGDATABASE"))
print("PGUSER =", os.getenv("PGUSER"))
print("PGPASSWORD =", os.getenv("PGPASSWORD"))
print("PGPORT =", os.getenv("PGPORT"))
print("HUB_PORT =", os.getenv("HUB_PORT"))

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

def get_or_create_device(conn, device_name):
    with conn.cursor() as cur:
        cur.execute("SELECT device_uid FROM devices WHERE device_name = %s", (device_name,))
        result = cur.fetchone()

        if result:
            return result[0]

        cur.execute("""
            INSERT INTO devices (device_name)
            VALUES (%s)
            RETURNING device_uid
        """, (device_name,))

        conn.commit()
        return cur.fetchone()[0]

def on_connect(client, userdata, flags, rc, properties=None):
    print("✅ Connected to MQTT broker, rc =", rc)
    client.subscribe("devices/#")

def on_message(client, userdata, msg):
    print("📥 RAW:", msg.topic, msg.payload)

    try:
        payload = json.loads(msg.payload.decode())
    except Exception as e:
        print("❌ JSON error:", e)
        return

    parts = msg.topic.split("/")
    if len(parts) < 3:
        print("❌ Invalid topic format")
        return

    device_name = parts[1]
    print("✅ Parsed message from device:", device_name, "payload:", payload)

    try:
        conn = get_db_connection()
        print("✅ DB connected")

        device_uid = get_or_create_device(conn, device_name)
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE devices
                SET last_seen = NOW()
                WHERE device_uid = %s
            """, (device_uid,))

        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO messages (device_uid, topic, payload, device_timestamp)
                VALUES (%s, %s, %s, %s)
            """, (
                device_uid,
                msg.topic,
                json.dumps(payload),
                payload.get("timestamp")
            ))

        conn.commit()
        print("✅ Inserted message")

    except Exception as e:
        print("❌ DB ERROR:", e)

    finally:
        if 'conn' in locals():
            conn.close()


client = mqtt.Client(
    protocol=mqtt.MQTTv5,
    callback_api_version=mqtt.CallbackAPIVersion.VERSION2
)

client.on_connect = on_connect
client.on_message = on_message

print("✅ Connecting to MQTT...")
client.connect(BROKER, PORT, 60)

client.loop_forever()