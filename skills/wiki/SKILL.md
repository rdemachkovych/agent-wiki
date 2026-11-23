---
name: wiki
description: Use when the owner wants to update, ask or check their notes wiki ("update the wiki", "compile the wiki after <folder>", "what can I show for <topic>", "file this answer", "lint the wiki") and after finishing a piece of work that has its own notes folder — keeps wiki/ (topics, concepts, answers) compiled from the source notes as an OKF v0.3 bundle, every claim footnoted to a source.
---

# wiki

`wiki/` answers three questions: what the owner can already show for each topic, which ideas repeat across pieces of work, and which answers were worth keeping. Agents write it; the owner reads it (in Obsidian, on GitHub, in any Markdown viewer) and does not edit it by hand. It is an [Open Knowledge Format](references/okf.md) v0.3 bundle whose root is `wiki/`.

Start every task by reading `wiki/index.md`. It is the map, and its frontmatter holds the settings. If `wiki/` does not exist yet, create it from the Layout below: a root `index.md` with the frontmatter shown there and an empty `log.md`.

## Settings

The root `index.md` frontmatter holds them, so the agent and the lint read the same values:

```yaml
---
okf_version: "0.3"
title: <name of the wiki>
description: <one sentence: what it covers and when to use it>
x-wiki-sections: [topics, concepts]   # folders whose pages must cite a notes file
x-wiki-evidence: NOTES.md             # the notes file in each source folder
---
```

A source folder is one folder per piece of work (a lesson, project, incident, sprint) with that notes file in it. Rename `topics/` to fit the owner's goal (e.g. `skill-cards/`) and list the new name in `x-wiki-sections`.

## Layout

| Path | What | One page per |
|---|---|---|
| `wiki/index.md` | frontmatter above; then sections of `* [Title](path) - description` | — |
| `wiki/log.md` | `## YYYY-MM-DD`, newest first, `* **Creation** / **Update** / **Deprecation**: …`; no frontmatter | — |
| `wiki/topics/<slug>.md` | Status table, What the topic covers, What I can show, Gaps | topic |
| `wiki/concepts/<slug>.md` | Main point, Where it showed up, Rules or Checklist | idea seen in 2+ source folders |
| `wiki/answers/YYYY-MM-DD-<slug>.md` | a question and its answer, with sources | answer worth keeping |

Every page except `index.md` and `log.md` has OKF frontmatter: `type`, `title`, `description` (all three required here), `tags` (a list), `status` only when `draft` or `deprecated`, `generated`, and `sources` whose ids label the footnotes (`[^id]`). Field rules: [references/okf.md](references/okf.md). Page shapes: the `example/wiki/` folder of this skill's repo.

## Rules

1. **One home per fact.** Details stay in the source folder's notes file; the wiki points to them. Every page in `x-wiki-sections` cites at least one notes file in `sources` or a link.
2. **Relative links** in the body (`../../projects/…/NOTES.md`), so they work on GitHub and in Obsidian. Never `[[wikilinks]]`: they are not links in OKF.
3. **Structure is earned.** A new concept page only when an idea appears in a second source folder; until then it is a line on the topic page.
4. **Nothing is orphaned.** Every page is in `index.md`.
5. **Facts only from sources.** No claim without a footnote to a notes file, document or link. Unknown → write it under Gaps.
6. **Honest trust.** `generated: { by: "<tool>/<model>", at: "<now, with offset>" }` on each page you create or change in meaning; a fix of format or links keeps the old `generated`. Add `verified` only for a person who confirmed the page and gave their id (`human:<id>`); never take the id from a login or git config. After a change in meaning, tell the owner which pages lost their review.
7. **Keep what you do not own.** Keep unknown keys, `verified` history and the root `index.md` frontmatter when you rewrite a file.
8. Show a plan before renaming, merging or deleting pages. Deprecate instead of delete: `status: deprecated`, `superseded_by: <new path>` when there is one, and a `log.md` line. A renamed page leaves a short deprecated page at the old path.

## Compile (after a piece of work)

1. Read the source folder's notes file (and the headings of any longer material it links, for "What the topic covers").
2. Create or update its topic page; add or update its line in `index.md`.
3. For each learned point that matches an existing concept, add a row to its "Where it showed up". A point that now appears in two source folders → new concept page.
4. Update `index.md` lines (description copied from each page's frontmatter) and add a `log.md` entry.
5. Run the check below.

## Ask

Answer from `wiki/` first, following its links to the notes files for evidence; say which files you used. Skip `deprecated` pages unless asked for history; follow `superseded_by` instead. If the answer is worth keeping (an explanation, comparison or interview answer), offer to file it in `wiki/answers/` and add it to `index.md`.

## Check

```sh
python3 scripts/lint.py wiki        # OK: 0 problem(s)
```

The script path is relative to this skill's folder; `wiki` is relative to the repo root. Settings come from the root `index.md`; `--sections` and `--evidence` override them. The script reports: a missing `okf_version`, `title` or `description` on the root index; frontmatter in `log.md` or a sub-index; pages without `type`, `title` or `description`; a `status` other than draft, stable or deprecated; `superseded_by` on a page that is not deprecated; `tags` that is not a list; timestamps without an offset; broken links and path fields; `[[wikilinks]]`; pages missing from `index.md`; pages in `x-wiki-sections` with no notes file cited.

After it, read the changed pages for meaning problems: contradictions with the notes files, duplicates, stale statuses (a page says "pending" but the notes say done). For a full OKF conformance check, the OKF repo's `okf-generate` skill has a validator.
