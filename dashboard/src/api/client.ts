import type { AnomalyResult, Device, Telemetry } from "../types";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL as string;

async function request<T>(path: string): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`);

  if (!response.ok) {
    if (response.status === 404) {
      throw new Error("Not found");
    }
    throw new Error(`Request failed with status ${response.status}`);
  }

  return response.json() as Promise<T>;
}

export function getDevices(): Promise<Device[]> {
  return request<Device[]>("/api/v1/devices");
}

export function getDevice(deviceId: string): Promise<Device> {
  return request<Device>(`/api/v1/devices/${deviceId}`);
}

export function getDeviceTelemetry(
  deviceId: string,
  limit = 20
): Promise<Telemetry[]> {
  return request<Telemetry[]>(
    `/api/v1/devices/${deviceId}/telemetry?limit=${limit}`
  );
}

export function getLatestTelemetry(): Promise<Telemetry[]> {
  return request<Telemetry[]>("/api/v1/telemetry/latest");
}


export function getDeviceAnomalies(deviceId: string): Promise<AnomalyResult[]> {
  return request<AnomalyResult[]>(`/api/v1/devices/${deviceId}/anomalies`);
}