# SmartSense AI — Backend

FastAPI backend foundation for SmartSense AI. This sprint establishes
the application skeleton only — no MQTT ingestion, database, or
business logic yet.

## Requirements

- Python 3.12+

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

| Variable       | Default       | Description                              |
|----------------|---------------|-------------------------------------------|
| `APP_ENV`      | `development` | Application environment                   |
| `DATABASE_URL` | (empty)       | Reserved for future PostgreSQL connection |
| `MQTT_HOST`    | `localhost`   | Reserved for future MQTT ingestion        |
| `MQTT_PORT`    | `1883`        | Reserved for future MQTT ingestion        |

`DATABASE_URL` and `MQTT_HOST`/`MQTT_PORT` are not used yet — the
backend does not connect to PostgreSQL or MQTT in this version.

## Running the Server

```bash
uvicorn app.main:app --reload
```

Server starts at `http://127.0.0.1:8000`.

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