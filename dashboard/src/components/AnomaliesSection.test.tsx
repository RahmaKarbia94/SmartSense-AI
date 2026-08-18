import { render, screen, waitFor } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { AnomaliesSection } from "./AnomaliesSection";
import * as apiClient from "../api/client";
import type { AnomalyResult, Telemetry } from "../types";

const reading: Telemetry = {
  id: 1,
  device_id: "simulator_001",
  timestamp: "2026-01-01T00:00:00Z",
  temperature: 25.0,
  humidity: 50.0,
  pressure: 1000.0,
};

describe("AnomaliesSection", () => {
  it("shows a loading state initially", () => {
    vi.spyOn(apiClient, "getDeviceAnomalies").mockReturnValue(new Promise(() => {}));

    render(<AnomaliesSection deviceId="simulator_001" readings={[reading]} />);

    expect(screen.getByText(/loading anomaly results/i)).toBeInTheDocument();
  });

  it("renders a normal result correctly", async () => {
    const normalResult: AnomalyResult = {
      device_id: "simulator_001",
      timestamp: "2026-01-01T00:00:00Z",
      is_anomaly: false,
      anomaly_score: -0.05,
    };
    vi.spyOn(apiClient, "getDeviceAnomalies").mockResolvedValue([normalResult]);

    render(<AnomaliesSection deviceId="simulator_001" readings={[reading]} />);

    await waitFor(() => {
      expect(screen.getByText("Normal")).toBeInTheDocument();
    });
    expect(screen.getByText(/25.00.*C/)).toBeInTheDocument();
  });

  it("renders an anomalous result correctly", async () => {
    const anomalousResult: AnomalyResult = {
      device_id: "simulator_001",
      timestamp: "2026-01-01T00:00:00Z",
      is_anomaly: true,
      anomaly_score: 0.42,
    };
    vi.spyOn(apiClient, "getDeviceAnomalies").mockResolvedValue([anomalousResult]);

    render(<AnomaliesSection deviceId="simulator_001" readings={[reading]} />);

    await waitFor(() => {
      expect(screen.getByText("Anomalous")).toBeInTheDocument();
    });
  });

  it("shows an empty state when there are no results", async () => {
    vi.spyOn(apiClient, "getDeviceAnomalies").mockResolvedValue([]);

    render(<AnomaliesSection deviceId="simulator_001" readings={[]} />);

    await waitFor(() => {
      expect(screen.getByText(/no anomaly results yet/i)).toBeInTheDocument();
    });
  });

  it("shows an error state when the API call fails", async () => {
    vi.spyOn(apiClient, "getDeviceAnomalies").mockRejectedValue(
      new Error("Failed to fetch")
    );

    render(<AnomaliesSection deviceId="simulator_001" readings={[]} />);

    await waitFor(() => {
      expect(screen.getByText(/failed to load anomaly results/i)).toBeInTheDocument();
    });
  });
});