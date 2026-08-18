import { useEffect, useState } from "react";
import { getDeviceAnomalies } from "../api/client";
import { enrichAnomaliesWithTelemetry, summarizeAnomalies } from "../utils/anomalyUtils";
import { AnomalySummary } from "./AnomalySummary";
import { AnomalyTable } from "./AnomalyTable";
import type { Telemetry } from "../types";

interface AnomaliesSectionProps {
  deviceId: string;
  readings: Telemetry[];
}

export function AnomaliesSection({ deviceId, readings }: AnomaliesSectionProps) {
  const [anomalies, setAnomalies] = useState<ReturnType<typeof enrichAnomaliesWithTelemetry>>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setError(null);

    getDeviceAnomalies(deviceId)
      .then((data) => {
        if (!cancelled) {
          setAnomalies(enrichAnomaliesWithTelemetry(data, readings));
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
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [deviceId]);

  if (loading) {
    return <p className="loading-state">Loading anomaly results...</p>;
  }

  if (error) {
    return <p className="error-state">Failed to load anomaly results: {error}</p>;
  }

  const summary = summarizeAnomalies(anomalies);

  return (
    <div>
      <AnomalySummary summary={summary} />
      <AnomalyTable results={anomalies} />
    </div>
  );
}