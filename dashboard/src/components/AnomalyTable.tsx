import type { EnrichedAnomalyResult } from "../utils/anomalyUtils";

interface AnomalyTableProps {
  results: EnrichedAnomalyResult[];
}

export function AnomalyTable({ results }: AnomalyTableProps) {
  if (results.length === 0) {
    return <p className="empty-state">No anomaly results yet.</p>;
  }

  return (
    <table className="anomaly-table">
      <thead>
        <tr>
          <th>Status</th>
          <th>Timestamp</th>
          <th>Score</th>
          <th>Temperature</th>
          <th>Humidity</th>
          <th>Pressure</th>
        </tr>
      </thead>
      <tbody>
        {results.map((result) => (
          <tr
            key={result.timestamp}
            className={result.is_anomaly ? "anomaly-table__row--anomalous" : ""}
          >
            <td>
              <span
                className={
                  result.is_anomaly
                    ? "anomaly-badge anomaly-badge--anomalous"
                    : "anomaly-badge anomaly-badge--normal"
                }
              >
                {result.is_anomaly ? "Anomalous" : "Normal"}
              </span>
            </td>
            <td>{new Date(result.timestamp).toLocaleString()}</td>
            <td>{result.anomaly_score.toFixed(4)}</td>
            <td>{result.temperature !== undefined ? `${result.temperature.toFixed(2)} °C` : "—"}</td>
            <td>{result.humidity !== undefined ? `${result.humidity.toFixed(2)} %` : "—"}</td>
            <td>{result.pressure !== undefined ? `${result.pressure.toFixed(2)} hPa` : "—"}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}