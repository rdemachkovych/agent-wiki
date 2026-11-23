# Cache for the product API

- **Goal:** p95 of `GET /products` under 200 ms.
- **Built:** read-through Redis cache, 60 s TTL, key per query string.
- **Result:** p95 went from 840 ms to 120 ms in a one-hour load test (k6, 50 VUs).
- **Learned:** measured p95 before and after with the same k6 script; without the baseline the gain could not be shown.
- **Open:** cache invalidation on product edits is not done.
