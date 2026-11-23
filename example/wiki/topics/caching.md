---
type: Topic
title: Caching
description: What I can show about caching an API, and what is still missing.
tags: [performance, redis]
status: stable
generated: { by: agent/model, at: 2026-01-30T18:00:00+01:00 }
sources:
  - { id: cache, resource: ../../notes/2026-01-cache/NOTES.md, title: Cache for the product API }
---

# Caching

| Item | Status |
|---|---|
| Read-through cache in front of an API | done |
| Invalidation on writes | open |

## What the topic covers

Putting a cache in front of a slow read path and proving the gain.[^cache]

## What I can show

- p95 of `GET /products` from 840 ms to 120 ms with a Redis read-through cache, 60 s TTL.[^cache] Evidence: [NOTES.md](../../notes/2026-01-cache/NOTES.md).
- Measured with the same k6 script before and after; see [Baseline first](../concepts/baseline-first.md).[^cache]

## Gaps

- Cache invalidation on product edits.[^cache]

[^cache]: [Cache for the product API](../../notes/2026-01-cache/NOTES.md)
