# SmartSense AI — Dashboard

React dashboard for SmartSense AI. Displays registered devices, their
telemetry history, and interactive charts by reading from the FastAPI
REST API. Built with React, TypeScript, and Vite.

## Requirements

- Node.js 18+
- The SmartSense AI backend running (see `backend/README.md`)

## Setup

From the `dashboard/` directory:

```bash
npm install
```

## Configuration

Copy `.env.example` to `.env` and set the backend API URL:
VITE_API_BASE_URL=http://127.0.0.1:8000


Environment variables must be prefixed `VITE_` to be readable by the
frontend (a Vite requirement). No production URL is hard-coded.

## Development

```bash
npm run dev
```

Starts the dev server at `http://localhost:5173`.

The backend must be running and have CORS configured to allow
`http://localhost:5173` (already set up in `backend/app/main.py`).

## Pages

- **Devices** (`/`) — lists registered devices, links to each device's
  details page. Shows loading, error, and empty states.
- **Device Details** (`/devices/:deviceId`) — shows summary cards
  (latest temperature, humidity, pressure, and reading timestamp),
  line charts for temperature/humidity/pressure over time, a
  time-range selector, and a telemetry history table. Shows loading
  and error states (including device-not-found).

## Charts & Time Range

Charts are built with [Recharts](https://recharts.org/). The
time-range selector (Last 10 / 25 / 50 / 100) re-fetches telemetry
from the API with the corresponding `limit` — it does not slice
already-loaded data client-side, so the chart always reflects real
backend data for the selected range.

## Architecture

src/
├── api/client.ts # single API client, all HTTP calls go through here
├── components/ # reusable, presentation-only components
│ ├── SummaryCard.tsx
│ ├── TelemetryLineChart.tsx # generic chart, parameterized by dataKey/label/unit/color
│ ├── TimeRangeSelector.tsx
│ ├── DeviceList.tsx / DeviceCard.tsx
│ └── TelemetryHistory.tsx
├── pages/ # route-level components that fetch data
└── types.ts # TypeScript interfaces matching backend schemas


Components never call `fetch` directly — all requests go through
`api/client.ts`, which reads `VITE_API_BASE_URL` and wraps the
backend's `/api/v1/*` endpoints. Chart and summary components are
presentation-only: they receive data via props and contain no
fetching logic.

## Testing

```bash
npm run test
```

Tests use Vitest and React Testing Library, with the API client mocked
- no live backend is required to run the test suite.

Note: `recharts` relies on the browser's `ResizeObserver` API, which
`jsdom` does not implement. A mock is provided in `src/test/setup.ts`
so chart components can be tested.