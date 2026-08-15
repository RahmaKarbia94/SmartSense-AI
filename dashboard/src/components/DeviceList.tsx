import type { Device } from "../types";
import { DeviceCard } from "./DeviceCard";

interface DeviceListProps {
  devices: Device[];
}

export function DeviceList({ devices }: DeviceListProps) {
  if (devices.length === 0) {
    return <p className="empty-state">No devices registered yet.</p>;
  }

  return (
    <div className="device-list">
      {devices.map((device) => (
        <DeviceCard key={device.device_id} device={device} />
      ))}
    </div>
  );
}