import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { getDevice, getDeviceTelemetry } from "../api/client";
import { TelemetryHistory } from "../components/TelemetryHistory";
import { TelemetryLineChart } from "../components/TelemetryLineChart";
import { TimeRangeSelector } from "../components/TimeRangeSelector";
import { SummaryCard } from "../components/SummaryCard";
import { AnomaliesSection } from "../components/AnomaliesSection";
import type { Device, Telemetry } from "../types";

export function DeviceDetailsPage() {
  const { deviceId } = useParams<{ deviceId: string }>();
  const [device, setDevice] = useState<Device | null>(null);
  const [readings, setReadings] = useState<Telemetry[]>([]);
  const [limit, setLimit] = useState(25);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!deviceId) return;
    let cancelled = false;
    setLoading(true);

    Promise.all([getDevice(deviceId), getDeviceTelemetry(deviceId, limit)])
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
  }, [deviceId, limit]);

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
        <div className="summary-cards">
          <SummaryCard label="Temperature" value={`${latest.temperature.toFixed(2)} °C`} />
          <SummaryCard label="Humidity" value={`${latest.humidity.toFixed(2)} %`} />
          <SummaryCard label="Pressure" value={`${latest.pressure.toFixed(2)} hPa`} />
          <SummaryCard
            label="Last Reading"
            value={new Date(latest.timestamp).toLocaleString()}
          />
        </div>
      ) : (
        <p className="empty-state">No telemetry recorded yet.</p>
      )}

      <div className="time-range-row">
        <h3>Charts</h3>
        <TimeRangeSelector value={limit} onChange={setLimit} />
      </div>

      <TelemetryLineChart
        readings={readings}
        dataKey="temperature"
        label="Temperature"
        unit="°C"
        color="#ef5350"
      />
      <TelemetryLineChart
        readings={readings}
        dataKey="humidity"
        label="Humidity"
        unit="%"
        color="#42a5f5"
      />
      <TelemetryLineChart
        readings={readings}
        dataKey="pressure"
        label="Pressure"
        unit="hPa"
        color="#66bb6a"
      />

      <h3>History</h3>
      <TelemetryHistory readings={readings} />

      <h3>Anomaly Detection</h3>
      <AnomaliesSection deviceId={device.device_id} readings={readings} />
    </div>
  );
}