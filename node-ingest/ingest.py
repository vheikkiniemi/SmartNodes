import paho.mqtt.client as mqtt
import json
import psycopg2
import os
import re

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
            INSERT INTO devices (device_name, ip_address, last_seen)
            VALUES (%s, %s, NOW())
            ON CONFLICT (device_name)
            DO UPDATE SET
                ip_address = COALESCE(EXCLUDED.ip_address, devices.ip_address),
                last_seen = NOW()
            RETURNING device_uid;
            """,
            (device_name, ip_address)
        )

        device_uid = cur.fetchone()[0]
        conn.commit()
        return device_uid


def on_connect(client, userdata, flags, rc, properties=None):
    print("✅ Connected to MQTT broker, rc =", rc)
    client.subscribe("devices/#")
    client.subscribe("$SYS/#")


def describe_sys(topic, value):
    if "uptime" in topic:
        return f"⏱ Uptime: {value}"

    if "clients/connected" in topic:
        return f"👥 Connected clients: {value}"

    if "messages/sent" in topic:
        return f"📤 Messages sent: {value}"

    if "messages/received" in topic:
        return f"📥 Messages received rate: {value} msg/s"

    return f"ℹ️ {topic} = {value}"


def on_message(client, userdata, msg):
    # Decode payload as UTF-8, but ignore errors to prevent crashes on binary data.
    raw_payload = msg.payload.decode(errors="ignore")
    topic = msg.topic
    parts = topic.split("/")

    #print("📥 TOPIC:", msg.topic)
    #print("📥 PAYLOAD:", raw_payload)

    if topic.startswith("$SYS/broker/log/"):
        m = re.search(
            r"New client connected from ([0-9.]+):([0-9]+) as ([^ ]+)",
            raw_payload
        )

        if m:
            ip = m.group(1)
            source_port = m.group(2)
            client_id = m.group(3)

            #print("🔌 MQTT client connected")
            #print("IP:", ip)
            #print("Source port:", source_port)
            #print("Client ID:", client_id)

        # ✅ Try JSON, but don't require it

    try:
        payload = json.loads(raw_payload)
        print("✅ JSON parsed:", payload)
    except Exception:
        payload = raw_payload
        print("ℹ️ Non-JSON payload")

    # ✅ Stop here for first testing phase
    #return

    # Adding stops here

    if client_id:
        device_name = client_id
    else:
        device_name = parts[1]

    print("✅ Parsed message from device:", device_name, "payload:", payload)

    try:
        conn = get_db_connection()
        print("✅ DB connected")

        device_uid = get_or_create_device(conn, device_name, ip)
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE devices
                SET last_seen = NOW()
                WHERE device_uid = %s
            """,
                (device_uid,),
            )

        # Updated: We want to store the raw payload as well, so we insert it as a JSON string.
        # with conn.cursor() as cur:
        #    cur.execute("""
        #        INSERT INTO messages (device_uid, topic, payload, device_timestamp)
        #        VALUES (%s, %s, %s, %s)
        #    """, (
        #        device_uid,
        #        msg.topic,
        #        json.dumps(payload),
        #        payload.get("timestamp")
        #    ))

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
        print("✅ Inserted message")

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
