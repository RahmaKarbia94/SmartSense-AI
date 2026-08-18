import { describe, expect, it } from "vitest";
import { enrichAnomaliesWithTelemetry, summarizeAnomalies } from "./anomalyUtils";
import type { AnomalyResult, Telemetry } from "../types";

const reading: Telemetry = {
  id: 1,
  device_id: "simulator_001",
  timestamp: "2026-01-01T00:00:00Z",
  temperature: 25.0,
  humidity: 50.0,
  pressure: 1000.0,
};

describe("enrichAnomaliesWithTelemetry", () => {
  it("attaches telemetry values when a matching timestamp exists", () => {
    const anomalies: AnomalyResult[] = [
      { device_id: "simulator_001", timestamp: "2026-01-01T00:00:00Z", is_anomaly: false, anomaly_score: -0.05 },
    ];
    const [result] = enrichAnomaliesWithTelemetry(anomalies, [reading]);
    expect(result.temperature).toBe(25.0);
    expect(result.humidity).toBe(50.0);
    expect(result.pressure).toBe(1000.0);
  });

  it("still returns the anomaly result when no matching telemetry exists", () => {
    const anomalies: AnomalyResult[] = [
      { device_id: "simulator_001", timestamp: "2026-02-01T00:00:00Z", is_anomaly: true, anomaly_score: 0.5 },
    ];
    const [result] = enrichAnomaliesWithTelemetry(anomalies, [reading]);
    expect(result.is_anomaly).toBe(true);
    expect(result.temperature).toBeUndefined();
  });
});

describe("summarizeAnomalies", () => {
  it("counts total and anomalous readings correctly", () => {
    const anomalies = [
      { device_id: "simulator_001", timestamp: "2026-01-01T00:00:02Z", is_anomaly: false, anomaly_score: -0.05 },
      { device_id: "simulator_001", timestamp: "2026-01-01T00:00:01Z", is_anomaly: true, anomaly_score: 0.3 },
      { device_id: "simulator_001", timestamp: "2026-01-01T00:00:00Z", is_anomaly: true, anomaly_score: 0.5 },
    ];
    const summary = summarizeAnomalies(anomalies);
    expect(summary.totalAnalyzed).toBe(3);
    expect(summary.anomalyCount).toBe(2);
    expect(summary.latestAnomaly?.timestamp).toBe("2026-01-01T00:00:01Z");
  });

  it("returns null latestAnomaly when there are no anomalies", () => {
    const anomalies = [
      { device_id: "simulator_001", timestamp: "2026-01-01T00:00:00Z", is_anomaly: false, anomaly_score: -0.05 },
    ];
    const summary = summarizeAnomalies(anomalies);
    expect(summary.latestAnomaly).toBeNull();
  });

  it("handles an empty list", () => {
    const summary = summarizeAnomalies([]);
    expect(summary.totalAnalyzed).toBe(0);
    expect(summary.anomalyCount).toBe(0);
    expect(summary.latestAnomaly).toBeNull();
  });
});