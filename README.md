# agent-wiki

An agent skill that keeps a small wiki compiled from your own work notes. The agent writes it, you read it. Every claim carries a footnote back to the notes it came from.

It answers three questions:

- **What can I show for topic X?** Topic pages list what is done, the evidence, and the gaps.
- **Which ideas keep coming back?** A concept page appears only once an idea shows up in a second piece of work.
- **What answers were worth keeping?** Explanations and interview answers get filed with their sources.

The idea comes from Andrej Karpathy's "LLM Knowledge Bases" post: an LLM compiles raw notes into a linked Markdown wiki, keeps it up to date, and runs health checks on it. The wiki is an [Open Knowledge Format v0.3](https://github.com/open-knowledge-format/open-knowledge-format/blob/main/SPEC.md) bundle, so an agent can tell what a page is, where it came from, how far to trust it and whether it is current.

## What is in the repo

```
skills/wiki/
  SKILL.md            the skill: layout, rules, compile / ask / check
  scripts/lint.py     mechanical check, Python 3.8+, stdlib only
  references/okf.md   OKF v0.3 cheat sheet
example/
  notes/              two pieces of work, one NOTES.md each
  wiki/               the wiki compiled from them: 2 topics, 1 concept, 1 answer
```

## Install

Copy or link `skills/wiki/` into the skills folder your agent reads:

```sh
# Claude Code
cp -r skills/wiki ~/.claude/skills/wiki          # or <repo>/.claude/skills/wiki
# Codex and other AGENTS.md harnesses
cp -r skills/wiki <repo>/.agents/skills/wiki
```

The repo you use it in needs one folder per piece of work (a lesson, project, incident, sprint), each with a `NOTES.md`. Settings live in the frontmatter of `wiki/index.md`, next to `okf_version`, so the agent and the lint read the same values:

```yaml
---
okf_version: "0.3"
title: My work wiki
description: What I can show per topic, with evidence from my project notes.
x-wiki-sections: [topics, concepts]   # pages that must cite a notes file
x-wiki-evidence: NOTES.md
---
```

## Use

- "update the wiki after `projects/2026-02-queue`" — compiles that folder into a topic page, updates concepts, `index.md` and `log.md`, then runs the check.
- "what can I show for caching?" — answers from the wiki, names the files it used, and offers to file the answer.
- "lint the wiki" — runs the script, then reads the changed pages for contradictions, duplicates and stale statuses.

## Check

```sh
python3 skills/wiki/scripts/lint.py example/wiki
# OK: 0 problem(s) in …/example/wiki

python3 skills/wiki/scripts/lint.py wiki   # your own wiki; settings from its index.md
```

The script checks the OKF v0.3 rules the skill relies on: root `index.md` metadata, no frontmatter in `log.md`, required fields, `status` and `superseded_by`, list `tags`, timestamps with an offset, broken links and path fields (`/` and relative), no `[[wikilinks]]`, pages missing from `index.md`, and pages that cite no notes file. It exits with 1 on any problem, so you can run it in CI or a pre-commit hook. For full OKF conformance, use the validator in the OKF repo's `okf-generate` skill.

Read the wiki in [Obsidian](https://obsidian.md) (open the repo as a vault) or on GitHub. Links are file-relative, so they work in both.

## Origin

Built for a 4-week agentic engineering course, where it kept one page per course skill card and linked each one to the lesson notes as evidence. The version here has the course-specific parts taken out.

## License

[Apache-2.0](LICENSE)
