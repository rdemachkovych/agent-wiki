# Open Knowledge Format (OKF) v0.2 — cheat sheet

Markdown plus YAML frontmatter that tells an agent what a note is, where it came from, how much to trust it and whether it is still current. Full spec: [OKF SPEC v0.2](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md).

A bundle is a folder of `.md` files. In OKF only `type` is required, and a missing field carries meaning (no `verified` = unverified). This skill also requires `title` and `description`.

## Frontmatter

```yaml
---
type: Playbook                 # REQUIRED, free text (Topic, Concept, Answer, Reference…)
title: Display name
description: One sentence; used by index.md and search snippets
resource: https://…            # the asset this page describes, if any
tags: [a, b]
sources:                        # provenance
  - { id: src1, resource: ../../notes/x/NOTES.md, title: X notes }
generated: { by: agent/model, at: 2026-01-28T09:00:00Z }
verified: { by: human:owner, at: 2026-01-28T10:00:00Z }
status: draft                   # draft | stable (default) | deprecated
stale_after: 2026-02-28T00:00:00Z
---
```

- Per-claim attribution: a footnote whose label is a `sources[].id` (`…text.[^src1]`).
- Trust tiers: no `verified` → unverified; non-human only → machine-confirmed; `human:` → human-reviewed.
- Actors: `<producer>/<version>`, `human:<id>`, `process:<id>`.
- Timestamps: ISO 8601 with offset.

## Reserved files

- `index.md` — no frontmatter (the root one may hold `okf_version`); sections of `* [Title](path) - description`.
- `log.md` — `## YYYY-MM-DD` headings, newest first, `* **Creation**: …` / `**Update**` / `**Deprecation**`.

## Links

OKF prefers bundle-relative `/path/note.md` and allows broken links (knowledge not yet written). This skill differs on both: links are file-relative so they work on GitHub and in Obsidian, and the lint reports broken ones.
