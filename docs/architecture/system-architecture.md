# SmartSense AI — System Architecture

## 1. Overview

SmartSense AI is an IoT monitoring and anomaly-detection platform.
A virtual sensor (with a real ESP32 sensor as a future, drop-in
replacement) publishes environmental telemetry over MQTT; a FastAPI
backend validates and persists it to PostgreSQL, runs anomaly
detection in the background, and exposes everything through a REST
API consumed by a React dashboard.

Each component is independently developed, tested, and documented.
This document describes how they fit together; see each component's
own README for setup, configuration, and implementation detail.

## 2. Components

| Component | Tech | Docs |
|---|---|---|
| Simulator | Python, Paho MQTT | `simulator/README.md` |
| MQTT Broker | Mosquitto | — |
| Backend | FastAPI, SQLAlchemy, Alembic | `backend/README.md` |
| Database | PostgreSQL | `backend/README.md` |
| AI Module | scikit-learn (Isolation Forest) | `ai/README.md` |
| Dashboard | React, TypeScript, Vite, Recharts | `dashboard/README.md` |

## 3. Data Flow

Python Simulator
|
| MQTT publish (QoS 1)
v
Mosquitto (localhost:1883)
|
| MQTT subscribe (wildcard topic: smartsense/devices/+/telemetry)
v
FastAPI MQTT Consumer
|
| decode UTF-8, parse JSON, validate
| (required fields, numeric types, sensor ranges, UTC timestamp)
v
Telemetry Service --- get-or-create device, insert reading
|
v
PostgreSQL (devices, telemetry, anomaly_results tables)
|
|---------------------------------------------+
| |
| (background thread, per reading) |
v |
AI Module (ai/ package, reused as an editable |
local dependency) --- preprocess, fit + predict |
Isolation Forest, persist anomaly_results |
| |
+----------------------------------------------+
|
| REST API (/api/v1/*)
v
React Dashboard --- device list, telemetry charts,
anomaly detection view


## 4. Key Architectural Decisions

- **Device-agnostic contract.** The MQTT topic and telemetry JSON
  schema are the platform's stable contract. Any device that
  publishes valid telemetry to `smartsense/devices/{device_id}/telemetry`
  works with the backend unchanged — the simulator today, an ESP32
  later.
- **Independent components, independent environments.** The
  simulator, backend, and AI module each have their own virtual
  environment and dependencies. The backend reuses the AI module's
  code via an editable local install (`pip install -e ../ai`) rather
  than duplicating it.
- **Two-tier error handling throughout.** Malformed data (invalid
  JSON, missing fields, out-of-range values) is logged and dropped.
  Infrastructure failures (database down, MQTT disconnect) are
  logged and recovered from automatically once the dependency is
  available again. The system does not crash on either category.
- **Anomaly detection is asynchronous and best-effort.** Analysis
  runs in a background thread after each telemetry write, so it
  never blocks MQTT ingestion. It is not a guaranteed or
  production-grade task queue — see `ai/README.md` and
  `backend/README.md` for its documented limitations.

## 5. What This Document Does Not Cover

Environment variables, exact validation rules, API endpoints, test
commands, and troubleshooting steps live in each component's own
README, not here, to avoid this document going stale as those details
change. This document only covers how the components relate to each
other.