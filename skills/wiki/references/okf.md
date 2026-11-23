# Open Knowledge Format (OKF) v0.3 — cheat sheet

Markdown plus YAML frontmatter that tells an agent what a note is, where it came from, how much to trust it and whether it is still current. Full spec: [SPEC.md](https://github.com/open-knowledge-format/open-knowledge-format/blob/main/SPEC.md) (v0.3; §13 lists the changes from v0.2). For OKF work beyond this wiki, the same repo has the `okf-generate` and `okf-consume` skills and a validator.

A bundle is a folder of `.md` files. Here the bundle root is `wiki/`. A concept is a `.md` file with a non-empty `type`; a `.md` file without frontmatter (such as a `README.md`) is not a concept. In OKF only `type` is required, and a missing field carries meaning (no `verified` = unverified). This skill also requires `title` and `description`.

## Frontmatter

```yaml
---
type: Topic                     # REQUIRED, free text (Topic, Concept, Answer, Reference…)
title: Display name
description: One sentence; used by index.md and search snippets
resource: https://…             # the asset this page describes, if any
tags: [a, b]                    # always a list: `tags: a, b` is ONE tag "a, b"
sources:                        # provenance; resource is required in an entry
  - { id: queue, resource: ../../notes/2026-02-queue/NOTES.md, title: Queue notes }
  - { id: traffic, resource: all checkout requests in production }   # a scope, not a path
generated: { by: "claude-code/claude-opus-5-5", at: "2026-01-28T09:00:00Z" }
verified:
  - { by: "human:<id>", at: "2026-01-28T10:00:00Z" }
status: deprecated              # draft | stable (default when absent) | deprecated
superseded_by: /topics/new.md   # only with status: deprecated
stale_after: "2026-02-28"       # only when a real review date is known
x-wiki-owner: team-a            # your own keys: prefix x-<producer>-
---
```

- **Syntax:** the file starts with a line that is exactly `---`, and the block ends at the next `---`. YAML 1.2, no duplicate keys. Quote timestamps, actors and values that look like numbers or booleans. When you change a file, keep keys you do not know and do not reformat values you did not change.
- **Timestamps:** a date-time with an offset (`"2026-06-30T14:00:00Z"`, `"2026-06-30T16:00:00+02:00"`) or a date only (`"2026-06-30"` = 00:00 UTC). A date-time without an offset is invalid. Use the date-time form for `generated.at` and `verified[].at`.
- **Per-claim attribution:** a footnote whose label is a `sources[].id` (`…text.[^queue]`), never a position such as `[^1]`. The footnote text is only a label for humans.
- **`generated.at`** is the last change in meaning. A fix of format, whitespace or links keeps the old value.
- **Trust tiers:** a `verified` event counts only when its `at` is not older than `generated.at`. No such event → unverified; only non-human actors → machine-confirmed; a `human:` actor → human-reviewed. A rewrite after a human review therefore drops the page to a lower tier until that person checks it again.
- **Actors:** `<tool>/<model>` for agents (`claude-code/claude-opus-5-5`, `codex/<model>`), `human:<id>`, `team:<id>`, `process:<id>`. Write `human:<id>` only for a person who confirmed the content and gave you that id; never take it from a login or the git config.
- **Retire or move:** keep the file, set `status: deprecated`, and add `superseded_by` when a replacement exists. A renamed page leaves a short deprecated page at the old path.
- **`stale_after`:** stale means "check again", not "false". A value that does not parse is never fresh.

## Reserved files

- Root `index.md` — frontmatter with `okf_version: "0.3"`, `title`, a one-sentence `description` of what the bundle is for, and `license` when known. Keep this frontmatter when you rewrite the index. The body has sections of `* [Title](path) - description`.
- `index.md` in a subfolder and every `log.md` — no frontmatter.
- `log.md` — `## YYYY-MM-DD` headings, newest first, `* **Creation**: …` / `**Update**` / `**Deprecation**`.

## Links and paths

- Links are `[text](target)`. `[[wikilinks]]` are not links in OKF, even when Obsidian shows them.
- A target that starts with `/` resolves from the bundle root, and any other target resolves from the file's own folder. Both forms are valid. This skill writes body links relative to the file, which works on GitHub and in Obsidian, and may write path fields (`resource`, `sources[].resource`, `superseded_by`) either way.
- A target outside the bundle root, such as `../../notes/…/NOTES.md` from inside `wiki/`, is external. OKF consumers do not read it from disk; it is a pointer. The lint of this skill still checks that it exists, because the wiki and its notes live in one repo.
- OKF consumers accept broken links (knowledge not yet written). The lint of this skill reports them, because every link here should point at a page or note that exists.
