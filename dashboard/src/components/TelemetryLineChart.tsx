import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import type { Telemetry } from "../types";

interface TelemetryLineChartProps {
  readings: Telemetry[];
  dataKey: "temperature" | "humidity" | "pressure";
  label: string;
  unit: string;
  color: string;
}

export function TelemetryLineChart({
  readings,
  dataKey,
  label,
  unit,
  color,
}: TelemetryLineChartProps) {
  if (readings.length === 0) {
    return <p className="empty-state">No data to chart yet.</p>;
  }

  const chartData = [...readings]
    .reverse()
    .map((r) => ({
      timestamp: new Date(r.timestamp).toLocaleTimeString(),
      value: r[dataKey],
    }));

  return (
    <div className="chart-block">
      <h4>
        {label} ({unit})
      </h4>
      <ResponsiveContainer width="100%" height={220}>
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" opacity={0.2} />
          <XAxis dataKey="timestamp" tick={{ fontSize: 12 }} />
          <YAxis tick={{ fontSize: 12 }} />
          <Tooltip formatter={(value: number) => [`${value} ${unit}`, label]} />
          <Line
            type="monotone"
            dataKey="value"
            stroke={color}
            dot={false}
            strokeWidth={2}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}