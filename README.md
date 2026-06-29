# 🚀 SmartNodes

**A lightweight, containerized MQTT platform for intelligent IoT devices.**

SmartNodes is an open-source platform for collecting, processing, storing, and exposing telemetry from IoT devices. It combines an MQTT broker, data ingestion service, PostgreSQL database, and REST API into a modular Docker Compose deployment.

Whether you're building an industrial IoT solution, an educational laboratory, or a prototype, SmartNodes provides a clean foundation that is easy to understand and extend.

---

## ✨ Features

- MQTT-based device communication
- Automatic device registration
- Telemetry collection and storage
- PostgreSQL persistence
- REST API for applications
- Docker Compose deployment
- Modular microservice architecture
- Easy to extend

---

## 🏗 Architecture

![SmartNodes Architecture](images/SmartNodeStack.png)

```text
                  MQTT
+------------+  Publish/Subscribe  +-----------+
|  Devices   | ───────────────────► | node-hub |
+------------+                      +-----------+
                                          │
                                          ▼
                                  +---------------+
                                  | node-ingest   |
                                  +---------------+
                                          │
                                          ▼
                                  +---------------+
                                  | node-vault    |
                                  | PostgreSQL    |
                                  +---------------+
                                          │
                                          ▼
                                  +---------------+
                                  | node-gateway  |
                                  | REST API      |
                                  +---------------+
                                          │
                                          ▼
                                Web Apps • Dashboards • Integrations
```

---

## 📦 Services

| Service | Description |
|---------|-------------|
| 📡 **node-hub** | Mosquitto MQTT broker |
| 📥 **node-ingest** | Processes MQTT messages |
| 🗄️ **node-vault** | PostgreSQL database |
| 🔌 **node-gateway** | REST API |

---

## 🚀 Quick Start

Clone the repository.

```bash
git clone https://github.com/vheikkiniemi/SmartNodes.git
cd SmartNodes
```

Create your configuration.

```bash
cp .env.example .env
```

Start the platform.

```bash
docker compose up -d --build
```

Verify that all services are running.

```bash
docker compose ps
```

---

## 📡 Example Data Flow

```text
Sensor
   │
   ▼
MQTT Publish
   │
   ▼
node-hub
   │
   ▼
node-ingest
   │
   ▼
PostgreSQL
   │
   ▼
REST API
   │
   ▼
Dashboard
```

---

## 📁 Project Structure

```text
SmartNodes/
│
├── node-hub/
├── node-ingest/
├── node-vault/
├── node-gateway/
├── docs/
├── examples/
├── images/
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## 📚 Documentation

Detailed documentation is available in the **docs/** directory.

| Topic | Description |
|------|-------------|
| [Installation](./docs/installation.md) | Installing SmartNodes |
| [Node-hub](./docs/node-hub.md) | MQTT broker |
| [Node-ingest](./docs/node-ingest.md) | Message ingestion |
| [Node-vault](./docs/node-vault.md )| PostgreSQL database |
| [Node-gateway](./docs/node-gateway.md) | REST API |
| [API](./docs/api.md) | REST API reference |
| [Troubleshootin](./docs/troubleshooting.md) | Common problems |

---

## 🛠 Technologies

- Docker Compose
- Eclipse Mosquitto
- PostgreSQL
- Python
- Node.js / Express
- MQTT v5

---

## 🎯 Use Cases

SmartNodes is suitable for:

- Industrial IoT
- Environmental monitoring
- Smart buildings
- Edge computing
- Embedded systems
- Educational laboratories
- MQTT demonstrations

---

## 🗺 Roadmap

Future development includes:

- Device authentication
- MQTT authorization
- HTTPS support
- Web dashboard
- Device provisioning
- Monitoring and metrics
- AI-assisted analytics
- High availability

---

## 🤝 Contributing

Contributions, ideas and pull requests are welcome.

Please open an issue before implementing major changes.

---

## 📄 License

This project is licensed under the MIT License.