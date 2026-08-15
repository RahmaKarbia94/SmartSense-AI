import { render, screen, waitFor } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { describe, expect, it, vi } from "vitest";
import { DevicesPage } from "./DevicesPage";
import * as apiClient from "../api/client";

describe("DevicesPage", () => {
  it("shows a loading state initially", () => {
    vi.spyOn(apiClient, "getDevices").mockReturnValue(new Promise(() => {}));

    render(
      <MemoryRouter>
        <DevicesPage />
      </MemoryRouter>
    );

    expect(screen.getByText(/loading devices/i)).toBeInTheDocument();
  });

  it("shows devices once loaded", async () => {
    vi.spyOn(apiClient, "getDevices").mockResolvedValue([
      { device_id: "simulator_001", created_at: "2026-01-01T00:00:00Z" },
    ]);

    render(
      <MemoryRouter>
        <DevicesPage />
      </MemoryRouter>
    );

    await waitFor(() => {
      expect(screen.getByText("simulator_001")).toBeInTheDocument();
    });
  });

  it("shows an error state when the API call fails", async () => {
    vi.spyOn(apiClient, "getDevices").mockRejectedValue(
      new Error("Failed to fetch")
    );

    render(
      <MemoryRouter>
        <DevicesPage />
      </MemoryRouter>
    );

    await waitFor(() => {
      expect(screen.getByText(/failed to load devices/i)).toBeInTheDocument();
    });
  });
});