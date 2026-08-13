# SmartSense AI — Backend

FastAPI backend for SmartSense AI. Connects to the MQTT broker,
subscribes to device telemetry, validates incoming payloads, and
passes valid readings to a service layer. Database persistence is
not implemented yet.

## Requirements

- Python 3.12+
- A running MQTT broker (developed and tested against Mosquitto 2.1.2
  at `localhost:1883`)

## Setup

From the `backend/` directory:

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

## Configuration

Configuration is read from environment variables (see `app/config.py`),
with local defaults if unset:

| Variable         | Default                              | Description                                |
|------------------|----------------------------------------|----------------------------------------------|
| `APP_ENV`        | `development`                          | Application environment                       |
| `DATABASE_URL`   | (empty)                                | Reserved for future PostgreSQL connection     |
| `MQTT_HOST`      | `localhost`                            | MQTT broker hostname                          |
| `MQTT_PORT`      | `1883`                                 | MQTT broker port                              |
| `MQTT_TOPIC`     | `smartsense/devices/+/telemetry`       | Wildcard subscription — matches any device_id |
| `MQTT_CLIENT_ID` | `smartsense_backend_subscriber`        | MQTT client ID                                |

`DATABASE_URL` is not used yet — the backend does not connect to
PostgreSQL in this version.

The `+` wildcard in `MQTT_TOPIC` matches any single topic level, so the
backend receives telemetry from any device (e.g. `simulator_001`,
`esp32_001`) without code changes.

## Running the Server

```bash
uvicorn app.main:app --reload
```

Server starts at `http://127.0.0.1:8000`. On startup, the backend
connects to the MQTT broker and subscribes to the telemetry topic. On
shutdown, it disconnects cleanly.

## MQTT Ingestion

Incoming messages go through:

Each stage fails safely — invalid payloads are logged and dropped, the
application never crashes on malformed data.

### Telemetry Schema

```json
{
  "device_id": "simulator_001",
  "timestamp": "2026-08-12T23:00:00+00:00",
  "temperature": 25.34,
  "humidity": 52.18,
  "pressure": 1014.27
}
```

All fields are required. `timestamp` must be a valid ISO 8601
datetime; `temperature`, `humidity`, `pressure` must be numeric.

Currently, valid telemetry is logged by the service layer only
(`app/services/telemetry_service.py`) — no persistence yet.

## Available Endpoints

| Method | Path            | Description                     |
|--------|-----------------|----------------------------------|
| GET    | `/`             | Service status                   |
| GET    | `/health`       | Health check                     |
| GET    | `/docs`         | Interactive API docs (Swagger)   |
| GET    | `/openapi.json` | OpenAPI schema                   |

## Running Tests

```bash
python -m pytest tests/ -v
```

## Verifying Telemetry Reception

1. Ensure Mosquitto is running on `localhost:1883`.
2. Start the backend: `uvicorn app.main:app --reload`
3. Start the simulator (`simulator/main.py`) in a separate terminal.
4. Watch the backend logs for lines like:
   `Telemetry received: device=simulator_001 temp=25.34 ...`
5. To test invalid-payload handling, publish a malformed message (e.g.
   invalid JSON, or JSON missing a required field) to
   `smartsense/devices/<any_id>/telemetry` via MQTT Explorer's Publish
   panel — the backend logs an error and keeps running.