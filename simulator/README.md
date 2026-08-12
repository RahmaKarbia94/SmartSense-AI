Example: `smartsense/devices/simulator_001/telemetry`

## Telemetry Payload

```json
{
  "device_id": "simulator_001",
  "timestamp": "2026-08-12T22:59:42.201634+00:00",
  "temperature": 25.34,
  "humidity": 52.18,
  "pressure": 1014.27
}
```

- `temperature`: 18–35 °C
- `humidity`: 30–80 %
- `pressure`: 950–1050 hPa
- `timestamp`: UTC, ISO 8601

Published at QoS 1 (at-least-once delivery).

## Reconnection Behavior

If the MQTT broker becomes unreachable, the simulator keeps running,
logs each failed publish attempt, and automatically reconnects once the
broker is available again (backing off between retries, up to 30s).
No manual restart is required.

## Troubleshooting

**`Failed to connect to MQTT broker: [WinError 10061]` (or similar) on startup**
The broker isn't running or isn't reachable at `MQTT_HOST:MQTT_PORT`.
Confirm Mosquitto is running and listening on `localhost:1883`.

**`[ERROR] Failed to publish telemetry (rc=4)` repeating**
The client has lost its connection to the broker. This is expected
during a broker outage — publishing will resume automatically once the
broker is reachable again.

**No messages appear in MQTT Explorer**
Confirm MQTT Explorer is connected to the same host/port as `MQTT_HOST`/
`MQTT_PORT`, and check the topic path matches `MQTT_TOPIC` exactly.