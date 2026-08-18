export interface Device {
  device_id: string;
  created_at: string;
}

export interface Telemetry {
  id: number;
  device_id: string;
  timestamp: string;
  temperature: number;
  humidity: number;
  pressure: number;
}

export interface AnomalyResult {
  device_id: string;
  timestamp: string;
  is_anomaly: boolean;
  anomaly_score: number;
}