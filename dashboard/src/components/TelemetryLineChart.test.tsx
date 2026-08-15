import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { TelemetryLineChart } from "./TelemetryLineChart";
import type { Telemetry } from "../types";

describe("TelemetryLineChart", () => {
  it("shows an empty state when there are no readings", () => {
    render(
      <TelemetryLineChart
        readings={[]}
        dataKey="temperature"
        label="Temperature"
        unit="°C"
        color="#ef5350"
      />
    );
    expect(screen.getByText(/no data to chart yet/i)).toBeInTheDocument();
  });

  it("renders a chart title with label and unit when data is present", () => {
    const readings: Telemetry[] = [
      {
        id: 1,
        device_id: "simulator_001",
        timestamp: "2026-01-01T00:00:00Z",
        temperature: 25.34,
        humidity: 52.18,
        pressure: 1014.27,
      },
    ];
    render(
      <TelemetryLineChart
        readings={readings}
        dataKey="temperature"
        label="Temperature"
        unit="°C"
        color="#ef5350"
      />
    );
    expect(screen.getByText(/temperature \(°c\)/i)).toBeInTheDocument();
  });
});
