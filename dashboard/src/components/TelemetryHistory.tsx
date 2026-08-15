import type { Telemetry } from "../types";

interface TelemetryHistoryProps {
  readings: Telemetry[];
}

export function TelemetryHistory({ readings }: TelemetryHistoryProps) {
  if (readings.length === 0) {
    return <p className="empty-state">No telemetry recorded yet.</p>;
  }

  return (
    <table className="telemetry-table">
      <thead>
        <tr>
          <th>Timestamp</th>
          <th>Temperature (°C)</th>
          <th>Humidity (%)</th>
          <th>Pressure (hPa)</th>
        </tr>
      </thead>
      <tbody>
        {readings.map((reading) => (
          <tr key={reading.id}>
            <td>{new Date(reading.timestamp).toLocaleString()}</td>
            <td>{reading.temperature.toFixed(2)}</td>
            <td>{reading.humidity.toFixed(2)}</td>
            <td>{reading.pressure.toFixed(2)}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}