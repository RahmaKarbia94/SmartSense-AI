# SmartSense AI — Backend

FastAPI backend for SmartSense AI. Connects to the MQTT broker,
subscribes to device telemetry, validates incoming payloads, and
persists valid readings to PostgreSQL.

## Requirements

- Python 3.12+
- A running MQTT broker (developed and tested against Mosquitto 2.1.2
  at `localhost:1883`)
- PostgreSQL (developed and tested against PostgreSQL 18)

## Setup

From the `backend/` directory:

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

`requirements.txt` includes `-e ../ai`, which installs the `ai/`
package (see `ai/README.md`) as an editable local dependency — the
backend reuses its preprocessing and model code directly rather than
duplicating it.

### Database

Create a local development database:

```bash
psql -U postgres -c "CREATE DATABASE smartsense_dev;"
```

Copy `.env.example` to `.env` and set your real `DATABASE_URL`
(never commit `.env`):
DATABASE_URL=postgresql://postgres:<your_password>@localhost:5432/smartsense_dev
Apply migrations to create the schema:

```bash
alembic upgrade head
```

## Configuration

Configuration is read from environment variables (see `app/config.py`,
loaded automatically from `.env` via `python-dotenv`):

| Variable         | Default                              | Description                                   |
|------------------|---------------------------------------|------------------------------------------------|
| `APP_ENV`        | `development`                        | Application environment                         |
| `DATABASE_URL`   | (empty)                              | PostgreSQL connection string                    |
| `MQTT_HOST`      | `localhost`                          | MQTT broker hostname                            |
| `MQTT_PORT`      | `1883`                               | MQTT broker port                                |
| `MQTT_TOPIC`     | `smartsense/devices/+/telemetry`     | Wildcard subscription — matches any device_id   |
| `MQTT_CLIENT_ID` | `smartsense_backend_subscriber`      | MQTT client ID     |
| `CORS_ALLOWED_ORIGINS` | `http://localhost:5173`        | Comma-separated list of origins allowed to call the API from a browser |

The `+` wildcard in `MQTT_TOPIC` matches any single topic level, so the
backend receives telemetry from any device (e.g. `simulator_001`,
`esp32_001`) without code changes.

## Database Migrations

Migrations are managed with Alembic (`backend/alembic/`).

```bash
# Apply all pending migrations
alembic upgrade head

# Create a new migration after changing models
alembic revision --autogenerate -m "description of change"

# Roll back the last migration
alembic downgrade -1
```

## Running the Server

```bash
uvicorn app.main:app --reload
```

Server starts at `http://127.0.0.1:8000`. On startup, the backend
connects to the MQTT broker and subscribes to the telemetry topic. On
shutdown, it disconnects cleanly.

## MQTT Ingestion & Persistence

Incoming messages go through:
MQTT message -> decode UTF-8 -> parse JSON -> validate schema -> telemetry service -> PostgreSQL
Each stage fails safely — invalid payloads and database failures are
logged and the message is dropped; the application never crashes.

When telemetry arrives for a device not yet seen, a `devices` row is
created automatically (`device_id` is unique — no duplicates are
created for repeated readings from the same device).

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
All fields are required. Validation rules (`app/schemas/telemetry.py`):

- `device_id` — non-empty string, maximum 100 characters.
- `timestamp` — valid ISO 8601 datetime, **must be UTC** (a naive
  datetime or a non-UTC offset like `+02:00` is rejected).
- `temperature` — numeric, must be between -50.0 and 60.0 °C.
- `humidity` — numeric, must be between 0.0 and 100.0 %.
- `pressure` — numeric, must be between 800.0 and 1100.0 hPa.

These ranges are intentionally wider than the simulator's own
generation range (18-35 °C / 30-80 % / 950-1050 hPa) — they exist to
catch clearly bad or faulty sensor data (e.g. a stuck or
disconnected sensor), not to constrain what any real device could
legitimately report.

### Database Schema

- `devices`: `id` (PK), `device_id` (unique), `created_at`
- `telemetry`: `id` (PK), `device_pk` (FK -> `devices.id`), `timestamp`
  (when the reading was generated), `temperature`, `humidity`,
  `pressure`, `created_at` (when the row was inserted)

## Available Endpoints

| Method | Path                                   | Description                          |
|--------|-----------------------------------------|----------------------------------------|
| GET    | `/`                                     | Service status                         |
| GET    | `/health`                               | Health check — reports app and database connectivity status |
| GET    | `/docs`                                 | Interactive API docs (Swagger)         |
| GET    | `/openapi.json`                         | OpenAPI schema                         |
| GET    | `/api/v1/devices`                       | List registered devices                |
| GET    | `/api/v1/devices/{device_id}`           | Get one device (404 if not found)      |
| GET    | `/api/v1/devices/{device_id}/telemetry` | Telemetry history, newest first, paginated (`limit`, `offset`) |
| GET    | `/api/v1/telemetry/latest`              | Latest reading for each device         |
| GET    | `/api/v1/devices/{device_id}/anomalies` | Anomaly results for a device (404 if not found) |
Telemetry history pagination: `limit` (1-500, default 50), `offset`
(>= 0, default 0). Invalid values return `422`.


## Complete Data Flow

Python Simulator
|
| MQTT publish
v
Mosquitto (localhost:1883)
|
| MQTT subscribe (wildcard topic)
v
FastAPI MQTT Consumer --- decode UTF-8, parse JSON
|
| validate (required fields, types, sensor ranges, UTC timestamp)
v
Telemetry Service --- get-or-create device, insert reading
|
v
PostgreSQL
|
| REST API (/api/v1/*)
v
React Dashboard


Every stage fails safely and independently:

- **Malformed MQTT payloads** (invalid JSON, missing fields, wrong
  types, out-of-range values, non-UTC timestamps) are logged and
  dropped by the MQTT consumer — the backend keeps running and keeps
  processing subsequent messages.
- **Database failures** (PostgreSQL down, connection dropped) are
  caught in the telemetry service, logged, and the backend resumes
  storing telemetry automatically once PostgreSQL is reachable again
  — no manual restart needed.
- **`GET /health`** reports live status: `{"status": "ok",
  "database": "connected"}` when everything is healthy, or
  `{"status": "degraded", "database": "unreachable"}` if PostgreSQL
  can't be reached — the endpoint itself never crashes even when the
  database is down.

## Anomaly Detection

After each telemetry reading is stored, the backend re-analyzes that
device's most recent readings (a sliding window, default 100) for
anomalies in a background thread, using the `ai/` package's
Isolation Forest model (`ai/README.md` covers why Isolation Forest,
input features, and its documented limitations — read that first).
Telemetry stored
|
v
Background thread: fetch recent window -> preprocess -> fit + predict
|
v
Skip readings already analyzed (unique per telemetry row)
|
v
Persist new results -> anomaly_results table


This does not block MQTT ingestion — the next telemetry message is
processed immediately regardless of how long analysis takes.

### Anomaly Schema

```json
{
  "device_id": "simulator_001",
  "timestamp": "2026-08-18T01:10:35.439344+00:00",
  "is_anomaly": false,
  "anomaly_score": -0.0369
}
```

`anomaly_score`: higher = more anomalous. `is_anomaly`: whether the
model's threshold flagged this reading.

### Database Schema (Anomaly Results)

- `anomaly_results`: `id` (PK), `telemetry_pk` (FK -> `telemetry.id`,
  unique — one result per reading), `is_anomaly`, `anomaly_score`,
  `created_at`

### Known Limitations of This Integration

These are current, real limitations, not hedging:

- **Once a reading is scored, its result is permanent.** Later calls
  train on a different, shifted window and could in principle score
  the same reading differently — the first score is kept, not
  updated. There is no re-scoring or versioning yet.
- **Background threads are fire-and-forget**, not a real task queue.
  If the backend restarts mid-analysis, that analysis is simply lost
  (not retried) — acceptable at this stage, but not production-grade
  background processing.
- All limitations documented in `ai/README.md` (no labeled ground
  truth, guessed contamination rate, no persisted/versioned model)
  apply here too, since this integration reuses that same model
  unchanged.

## Running Tests

```bash
python -m pytest tests/ -v
```

Database-layer tests use an in-memory SQLite database — they never
touch your local PostgreSQL data.

## Verifying Stored Telemetry

1. Ensure PostgreSQL and Mosquitto are both running, and migrations
   are applied (`alembic upgrade head`).
2. Start the backend: `uvicorn app.main:app`
3. Start the simulator (`simulator/main.py`) in a separate terminal.
4. Watch the backend logs for lines like:
   `Stored telemetry: device=simulator_001 temp=25.34 ...`
5. Inspect the database directly:
```bash
   psql -U postgres -d smartsense_dev -c "SELECT * FROM devices;"
   psql -U postgres -d smartsense_dev -c "SELECT * FROM telemetry ORDER BY id DESC LIMIT 5;"
```
6. To test failure handling, stop PostgreSQL while the backend is
   running — it logs database errors and resumes storing telemetry
   automatically once PostgreSQL is available again.