import { SummaryCard } from "./SummaryCard";
import type { AnomalySummary as AnomalySummaryData } from "../utils/anomalyUtils";

interface AnomalySummaryProps {
  summary: AnomalySummaryData;
}

export function AnomalySummary({ summary }: AnomalySummaryProps) {
  return (
    <div className="summary-cards">
      <SummaryCard label="Analyzed Readings" value={String(summary.totalAnalyzed)} />
      <SummaryCard label="Anomalies Detected" value={String(summary.anomalyCount)} />
      <SummaryCard
        label="Latest Anomaly"
        value={
          summary.latestAnomaly
            ? new Date(summary.latestAnomaly.timestamp).toLocaleString()
            : "None"
        }
      />
    </div>
  );
}