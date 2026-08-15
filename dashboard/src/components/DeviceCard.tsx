import { Link } from "react-router-dom";
import type { Device } from "../types";

interface DeviceCardProps {
  device: Device;
}

export function DeviceCard({ device }: DeviceCardProps) {
  return (
    <Link to={`/devices/${device.device_id}`} className="device-card">
      <h3>{device.device_id}</h3>
      <p className="device-card__meta">
        Registered: {new Date(device.created_at).toLocaleString()}
      </p>
    </Link>
  );
}