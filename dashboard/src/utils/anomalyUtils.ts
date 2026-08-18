import type { AnomalyResult, Telemetry } from "../types";

export interface EnrichedAnomalyResult extends AnomalyResult {
  temperature?: number;
  humidity?: number;
  pressure?: number;
}

export interface AnomalySummary {
  totalAnalyzed: number;
  anomalyCount: number;
  latestAnomaly: EnrichedAnomalyResult | null;
}

/**
 * Attaches temperature/humidity/pressure to each anomaly result when a
 * telemetry reading with a matching timestamp is available. Anomaly
 * results always render even without a match — the telemetry values
 * are supplementary, not required.
 */
export function enrichAnomaliesWithTelemetry(
  anomalies: AnomalyResult[],
  readings: Telemetry[]
): EnrichedAnomalyResult[] {
  const byTimestamp = new Map(readings.map((r) => [r.timestamp, r]));

  return anomalies.map((anomaly) => {
    const match = byTimestamp.get(anomaly.timestamp);
    return match
      ? {
          ...anomaly,
          temperature: match.temperature,
          humidity: match.humidity,
          pressure: match.pressure,
        }
      : anomaly;
  });
}

/**
 * Anomaly results are assumed sorted newest-first (matches the
 * backend's ordering), so the first flagged result is the latest one.
 */
export function summarizeAnomalies(
  anomalies: EnrichedAnomalyResult[]
): AnomalySummary {
  const anomalyResults = anomalies.filter((a) => a.is_anomaly);

  return {
    totalAnalyzed: anomalies.length,
    anomalyCount: anomalyResults.length,
    latestAnomaly: anomalyResults[0] ?? null,
  };
}