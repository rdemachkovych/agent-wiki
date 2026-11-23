---
name: wiki
description: Use when the owner wants to update, ask or check their notes wiki ("update the wiki", "compile the wiki after <folder>", "what can I show for <topic>", "file this answer", "lint the wiki") and after finishing a piece of work that has its own notes folder — keeps wiki/ (topics, concepts, answers) compiled from the source notes, every claim footnoted to a source.
---

# wiki

`wiki/` answers three questions: what the owner can already show for each topic, which ideas repeat across pieces of work, and which answers were worth keeping. Agents write it; the owner reads it (in Obsidian, on GitHub, in any Markdown viewer) and does not edit it by hand.

Start every task by reading `wiki/index.md`. It is the map. If `wiki/` does not exist yet, create it from the Layout below with an empty `index.md` and `log.md`.

## Settings

Read these from the repo's `AGENTS.md` or `CLAUDE.md` if it names them; otherwise use the defaults.

| Setting | Default | Meaning |
|---|---|---|
| source folders | folders with a notes file | one folder per piece of work (a lesson, project, incident, sprint) |
| notes file | `NOTES.md` | the file in each source folder that holds its facts |
| topics folder | `wiki/topics/` | one page per topic; rename (e.g. `skill-cards/`) to fit the owner's goal |

## Layout

| Path | What | One page per |
|---|---|---|
| `wiki/index.md` | map: sections of `* [Title](path) - one line in the words the owner would ask with` | — |
| `wiki/log.md` | `## YYYY-MM-DD`, newest first, `* **Creation** / **Update** / **Deprecation**: …` | — |
| `wiki/topics/<slug>.md` | Status table, What the topic covers, What I can show, Gaps | topic |
| `wiki/concepts/<slug>.md` | Main point, Where it showed up, Rules or Checklist | idea seen in 2+ source folders |
| `wiki/answers/YYYY-MM-DD-<slug>.md` | a question and its answer, with sources | answer worth keeping |

Every page except `index.md` and `log.md` has OKF v0.2 frontmatter: `type`, `title`, `description` (required here), `tags`, `status`, `generated`, `sources` with ids used as footnotes (`[^id]`). Format: [references/okf.md](references/okf.md). Page shapes: the `example/wiki/` folder of this skill's repo.

## Rules

1. **One home per fact.** Details stay in the source folder's notes file; the wiki points to them. Every topic and concept page links at least one notes file.
2. **Relative links** (`../../projects/…/NOTES.md`), so they work on GitHub and in Obsidian. Not the OKF `/bundle-root` style.
3. **Structure is earned.** A new concept page only when an idea appears in a second source folder; until then it is a line on the topic page.
4. **Nothing is orphaned.** Every page is in `index.md`.
5. **Facts only from sources.** No claim without a footnote to a notes file, document or link. Unknown → write it under Gaps.
6. Show a plan before renaming, merging or deleting pages. Deprecate (`status: deprecated`, a `log.md` line) instead of delete.

## Compile (after a piece of work)

1. Read the source folder's notes file (and the headings of any longer material it links, for "What the topic covers").
2. Create or update its topic page; add or update its line in `index.md`.
3. For each learned point that matches an existing concept, add a row to its "Where it showed up". A point that now appears in two source folders → new concept page.
4. Update `index.md` lines and add a `log.md` entry.
5. Run the check below.

## Ask

Answer from `wiki/` first, following its links to the notes files for evidence; say which files you used. If the answer is worth keeping (an explanation, comparison or interview answer), offer to file it in `wiki/answers/` and add it to `index.md`.

## Check

```sh
python3 scripts/lint.py wiki                       # OK: 0 problem(s)
python3 scripts/lint.py wiki --sections skill-cards,concepts --evidence NOTES.md
```

Paths are relative to this skill's folder for the script and to the repo root for `wiki`. The script finds broken links, missing frontmatter fields, pages not in `index.md`, and topic or concept pages with no link to a source outside `wiki/` (or, with `--evidence`, to a file of that name). After it, read the changed pages for meaning problems: contradictions with the notes files, duplicates, stale statuses (a page says "pending" but the notes say done).
