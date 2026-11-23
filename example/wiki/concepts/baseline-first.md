---
type: Concept
title: Baseline first
description: Measure the number you want to move before you change anything, with the same tool you will measure after.
tags: [measurement]
status: stable
generated: { by: agent/model, at: 2026-02-14T18:00:00+01:00 }
sources:
  - { id: cache, resource: ../../notes/2026-01-cache/NOTES.md, title: Cache for the product API }
  - { id: queue, resource: ../../notes/2026-02-queue/NOTES.md, title: Queue for invoice e-mails }
---

# Baseline first

## Main point

A gain you did not measure before the change cannot be shown after it.[^cache]

## Where it showed up

| Where | How |
|---|---|
| [Cache](../../notes/2026-01-cache/NOTES.md) | same k6 script before and after[^cache] |
| [Queue](../../notes/2026-02-queue/NOTES.md) | checkout p95 taken before the change[^queue] |

## Checklist

- Name the number (p95, error rate, cost) before the work starts.
- Record it with the tool you will use afterwards.

[^cache]: [Cache for the product API](../../notes/2026-01-cache/NOTES.md)
[^queue]: [Queue for invoice e-mails](../../notes/2026-02-queue/NOTES.md)
