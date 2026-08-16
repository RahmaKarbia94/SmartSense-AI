Each layer is independently testable and has a single responsibility.
`pipeline.py` is the only place that wires them together.

## Why Isolation Forest

- **Unsupervised.** There is no labeled anomaly data for this project
  — nobody has manually marked any reading as "faulty sensor" versus
  "real spike." Isolation Forest requires no labels: it isolates
  points by randomly partitioning the feature space, and points that
  are isolated in fewer splits are considered more anomalous.
- **Multivariate.** It scores temperature, humidity, and pressure
  together, not as three independent thresholds.
- **No feature scaling required**, unlike distance-based methods.
- **Cheap to retrain** on a small batch, appropriate for this
  project's current scale (hundreds of readings, not millions).
- Matches the project's stated principle: start simple and
  explainable before considering anything heavier.

## Input Features

`temperature`, `humidity`, `pressure` — the same three fields
persisted by the backend. `device_id` and `timestamp` pass through
untouched for identifying results, but are not fed to the model.

## Expected Output

`pipeline.detect_anomalies(device_id)` returns a DataFrame with:

| Column          | Type      | Description                                  |
|-----------------|-----------|-----------------------------------------------|
| `device_id`     | str       | Which device the reading belongs to           |
| `timestamp`     | datetime  | When the reading was generated                |
| `is_anomaly`    | bool      | Whether the model flagged this reading         |
| `anomaly_score` | float     | Higher = more anomalous (inverted from scikit-learn's raw score, where higher normally means more *normal* — inverted here for an intuitive direction) |

## Limitations of This First Model

These are real, current limitations — not hedging:

1. **No labeled ground truth.** There is no way to verify precision
   or recall, because no human has ever confirmed which readings, if
   any, are genuinely anomalous. "Anomaly" here means
   "statistically unusual relative to the batch it was trained on,"
   not "verified as scientifically wrong."

2. **`contamination=0.05` is a guess, not a measured rate.** It tells
   the model to expect ~5% of the batch to be unusual. Changing it
   changes how many readings get flagged, independent of the data
   itself.

3. **Trains on whatever batch it's given, and treats the majority of
   that batch as "normal" by construction.** If a batch contains a
   sustained fault (e.g. a sensor stuck at one value for hours), the
   model may not flag it, because that becomes the new "normal" for
   the window it was trained on.

4. **No persisted model.** `detect_anomalies()` trains a fresh model
   from scratch on every call. There is no model versioning, no drift
   monitoring, and no way to compare today's model against
   yesterday's.

5. **Observed on real data (see below): with the current simulator,
   flagged readings are not dramatically different from the rest —
   just the statistical tail of independently-random values.** The
   simulator generates temperature, humidity, and pressure
   independently at random each reading, with no real physical
   relationship between them and no simulated sensor faults. This
   means what gets flagged today is mostly noise, not a demonstration
   of catching a real problem. This will become more meaningful once
   real (or more realistically correlated) sensor data is available.

6. **Preprocessing's missing/invalid-value handling is a second line
   of defense**, not the primary one — the backend's Sprint 9 schema
   validation already rejects non-numeric values and out-of-range
   readings before they reach PostgreSQL. This layer exists in case
   the AI package is ever pointed at a different or less-validated
   data source.

## Real-Data Experiment

Run against your own database:

```bash
python experiment.py
```

Example result against 395 real `simulator_001` readings: 20 flagged
(5.1%, close to the configured `contamination=0.05`), with anomaly
scores only marginally above the threshold — consistent with
limitation #5 above.

## Running Tests

```bash
python -m pytest tests/ -v
```

Model and pipeline tests use synthetic, seeded data (not real
telemetry) so results are deterministic and specific cases (a known
outlier, insufficient data) can be reliably tested. The real-data
experiment (`experiment.py`) is the actual verification against real
telemetry, run separately.