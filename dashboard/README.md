Components never call `fetch` directly — all requests go through
`api/client.ts`, which reads `VITE_API_BASE_URL` and wraps the
backend's `/api/v1/*` endpoints.

## Testing

```bash
npm run test
```

Tests use Vitest and React Testing Library, with the API client mocked
— no live backend is required to run the test suite.