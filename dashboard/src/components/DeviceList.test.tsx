import { render, screen } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { describe, expect, it } from "vitest";
import { DeviceList } from "./DeviceList";
import type { Device } from "../types";

function renderWithRouter(ui: React.ReactElement) {
  return render(<MemoryRouter>{ui}</MemoryRouter>);
}

describe("DeviceList", () => {
  it("shows an empty state when there are no devices", () => {
    renderWithRouter(<DeviceList devices={[]} />);
    expect(screen.getByText(/no devices registered yet/i)).toBeInTheDocument();
  });

  it("renders a card for each device", () => {
    const devices: Device[] = [
      { device_id: "simulator_001", created_at: "2026-01-01T00:00:00Z" },
      { device_id: "esp32_001", created_at: "2026-01-02T00:00:00Z" },
    ];
    renderWithRouter(<DeviceList devices={devices} />);

    expect(screen.getByText("simulator_001")).toBeInTheDocument();
    expect(screen.getByText("esp32_001")).toBeInTheDocument();
  });
});