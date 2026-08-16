import logging

from pipeline import detect_anomalies

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

if __name__ == "__main__":
    result = detect_anomalies("simulator_001", limit=500)

    print(f"\nAnalyzed {len(result)} readings for simulator_001\n")
    print(result.to_string(index=False))

    anomalies = result[result["is_anomaly"]]
    print(f"\n{len(anomalies)} reading(s) flagged as anomalous ({len(anomalies) / len(result):.1%})")
    if not anomalies.empty:
        print("\nFlagged readings:")
        print(anomalies.to_string(index=False))