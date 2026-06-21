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
INGESTORUSER = os.environ.get("INGESTORUSER")
INGESTORPASS = os.environ.get("INGESTORPASS")

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


def create_device(conn, device_name, ip_address=None, connected=True):
    """
    Creates a device on first contact.

    :param conn: DB connection
    :param device_name: unique device name
    :param ip_address: optional IP address
    :param connected: True (default) = device is connecting
    """
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO devices (
                device_name,
                ip_address,
                last_seen,
                is_connected,
                disconnected_at
            )
            VALUES (
                %s,
                %s,
                NOW(),
                %s,
                CASE WHEN %s THEN NULL ELSE NOW() END
            )
            RETURNING device_uid
            """,
            (device_name, ip_address, connected, connected)
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
    
def update_device(conn, device_uid, ip_address=None, connected=None):
    """
    Updates device state.

    :param conn: DB connection
    :param device_uid: device UUID
    :param ip_address: optional IP address
    :param connected: 
        True  -> device connected
        False -> device disconnected
        None  -> just update last_seen (heartbeat)
    """
    with conn.cursor() as cur:
        if connected is True:
            # CONNECT
            cur.execute(
                """
                UPDATE devices
                SET 
                    last_seen = NOW(),
                    ip_address = COALESCE(%s, ip_address),
                    is_connected = TRUE,
                    disconnected_at = NULL
                WHERE device_uid = %s
                """,
                (ip_address, device_uid)
            )

        elif connected is False:
            # DISCONNECT
            cur.execute(
                """
                UPDATE devices
                SET 
                    is_connected = FALSE,
                    disconnected_at = NOW()
                WHERE device_uid = %s
                """,
                (device_uid,)
            )

        else:
            # HEARTBEAT (no state change)
            cur.execute(
                """
                UPDATE devices
                SET 
                    last_seen = NOW(),
                    ip_address = COALESCE(%s, ip_address)
                WHERE device_uid = %s
                """,
                (ip_address, device_uid)
            )

        conn.commit()

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print(f"✅ Connected as {INGESTORUSER}")
    else:
        print(f"❌ Connection failed: {rc}")
        
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
        open_connection = re.search(
            r"New client connected from ([0-9.]+):([0-9]+) as ([^ ]+)",
            raw_payload
        )

        close_connection = re.search(
            r"Client ([^ ]+) \[[0-9.]+:[0-9]+\] disconnected",
            raw_payload
        )

        if not open_connection and not close_connection:
            return
        
        conn = get_db_connection()

        if open_connection:
            ip = open_connection.group(1)
            client_id = open_connection.group(3)
            if get_device_uid(conn, client_id):
                update_device(conn, get_device_uid(conn, client_id), ip_address=ip, connected=True)
                conn.close()
                return
            else:
                create_device(conn, client_id, ip)
                conn.close()
                return
        else:
            client_id = close_connection.group(1)
            update_device(conn, get_device_uid(conn, client_id), ip_address=ip, connected=False)
            conn.close()
            return

        

        #create_device(conn, client_id, ip)
        #conn.close()
        #return

    if topic.startswith("devices/"):
        if len(parts) < 3:
            print("❌ Invalid device topic")
            return
        
        device_name = parts[1]
        
        try:
            conn = get_db_connection()
            #print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), " ✅ DB connected")

            device_uid = get_device_uid(conn, device_name)
            if not device_uid:
                print("❌ Unknown device, message ignored:", device_name)
                conn.close()
                return
            
            update_device(conn, device_uid)

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
    client_id=INGESTORUSER,
    protocol=mqtt.MQTTv5,
    callback_api_version=mqtt.CallbackAPIVersion.VERSION2
)

client.username_pw_set(
    username=INGESTORUSER,
    password=INGESTORPASS
)

client.on_connect = on_connect
client.on_message = on_message

print("✅ Connecting to MQTT...")
client.connect(BROKER, PORT, 60)

client.loop_forever()
