import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { getDevice, getDeviceTelemetry } from "../api/client";
import { TelemetryHistory } from "../components/TelemetryHistory";
import type { Device, Telemetry } from "../types";

export function DeviceDetailsPage() {
  const { deviceId } = useParams<{ deviceId: string }>();
  const [device, setDevice] = useState<Device | null>(null);
  const [readings, setReadings] = useState<Telemetry[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!deviceId) return;
    let cancelled = false;

    Promise.all([getDevice(deviceId), getDeviceTelemetry(deviceId)])
      .then(([deviceData, telemetryData]) => {
        if (!cancelled) {
          setDevice(deviceData);
          setReadings(telemetryData);
          setLoading(false);
        }
      })
      .catch((err: Error) => {
        if (!cancelled) {
          setError(err.message);
          setLoading(false);
        }
      });

    return () => {
      cancelled = true;
    };
  }, [deviceId]);

  if (loading) {
    return <p className="loading-state">Loading device...</p>;
  }

  if (error) {
    return (
      <div>
        <p className="error-state">Failed to load device: {error}</p>
        <Link to="/">Back to devices</Link>
      </div>
    );
  }

  if (!device) {
    return null;
  }

  const latest = readings[0];

  return (
    <div>
      <Link to="/">&larr; Back to devices</Link>
      <h2>{device.device_id}</h2>

      {latest ? (
        <div className="latest-reading">
          <div>
            <strong>Temperature</strong>
            <p>{latest.temperature.toFixed(2)} °C</p>
          </div>
          <div>
            <strong>Humidity</strong>
            <p>{latest.humidity.toFixed(2)} %</p>
          </div>
          <div>
            <strong>Pressure</strong>
            <p>{latest.pressure.toFixed(2)} hPa</p>
          </div>
        </div>
      ) : (
        <p className="empty-state">No telemetry recorded yet.</p>
      )}

      <h3>History</h3>
      <TelemetryHistory readings={readings} />
    </div>
  );
}