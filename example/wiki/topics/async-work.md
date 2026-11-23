---
type: Topic
title: Async work
description: What I can show about moving slow work off the request path with a queue.
tags: [queues, reliability]
generated: { by: "claude-code/claude-opus-5-5", at: "2026-02-14T18:00:00+01:00" }
sources:
  - { id: queue, resource: ../../notes/2026-02-queue/NOTES.md, title: Queue for invoice e-mails }
---

# Async work

| Item | Status |
|---|---|
| Queue and worker with retries | done |
| Monitoring of queue depth and dead letters | done |

## What the topic covers

Taking a slow external call off the user's request and making sure no job is lost.[^queue]

## What I can show

- Checkout p95 from 1.9 s to 310 ms after moving invoice mail to a queue.[^queue] Evidence: [NOTES.md](../../notes/2026-02-queue/NOTES.md).
- 0 lost mails in a week, checked by queue depth and dead-letter count.[^queue]

## Gaps

- No load test of the worker yet: unknown how many mails per minute it can send.

[^queue]: [Queue for invoice e-mails](../../notes/2026-02-queue/NOTES.md)
