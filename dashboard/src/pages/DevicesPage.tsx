import { useEffect, useState } from "react";
import { getDevices } from "../api/client";
import { DeviceList } from "../components/DeviceList";
import type { Device } from "../types";

export function DevicesPage() {
  const [devices, setDevices] = useState<Device[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;

    getDevices()
      .then((data) => {
        if (!cancelled) {
          setDevices(data);
          setLoading(false);
        }
      })
      .catch((err: Error) => {
        if (!cancelled) {
          setError(err.message);
          setLoading(false);
        }
      });

    return () => {
      cancelled = true;
    };
  }, []);

  if (loading) {
    return <p className="loading-state">Loading devices...</p>;
  }

  if (error) {
    return <p className="error-state">Failed to load devices: {error}</p>;
  }

  return (
    <div>
      <h2>Devices</h2>
      <DeviceList devices={devices} />
    </div>
  );
}