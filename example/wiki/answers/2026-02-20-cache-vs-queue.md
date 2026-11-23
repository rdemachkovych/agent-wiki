---
type: Answer
title: Cache vs queue
description: When I would pick a cache and when a queue, from my own two cases.
tags: [interview, performance]
status: stable
generated: { by: agent/model, at: 2026-02-20T18:00:00+01:00 }
sources:
  - { id: cache, resource: ../../notes/2026-01-cache/NOTES.md, title: Cache for the product API }
  - { id: queue, resource: ../../notes/2026-02-queue/NOTES.md, title: Queue for invoice e-mails }
---

# Cache vs queue

**Q:** When would you use a cache, and when a queue?

**A:** A cache when the user needs the answer now and it can be a little stale: product reads, 60 s TTL, p95 840 → 120 ms.[^cache] A queue when the user does not need the result to continue: invoice mail, checkout p95 1.9 s → 310 ms.[^queue] See [Caching](../topics/caching.md) and [Async work](../topics/async-work.md).

[^cache]: [Cache for the product API](../../notes/2026-01-cache/NOTES.md)
[^queue]: [Queue for invoice e-mails](../../notes/2026-02-queue/NOTES.md)
