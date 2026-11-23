# Quick start

The wiki invents nothing: it compiles what is already written down. So you need sources first, and the wiki comes after them.

## 1. Install the skill (once per project)

```sh
git clone https://github.com/rdemachkovych/agent-wiki /tmp/agent-wiki
mkdir -p <project>/.agents/skills <project>/.claude/skills
cp -r /tmp/agent-wiki/skills/wiki <project>/.agents/skills/wiki
ln -s ../../.agents/skills/wiki <project>/.claude/skills/wiki   # Claude Code reads it through this link
```

If you only use Claude Code, copying it to `.claude/skills/wiki` is enough.

## 2. New project: keep notes from day one

Give each piece of work (a feature, sprint, incident, migration) its own folder with a `NOTES.md`. Five lines are enough:

```markdown
- **Goal:** what it should achieve (with a number if you can)
- **Built:** what was done
- **Result:** what was measured or checked
- **Learned:** what to take away
- **Open:** what is not done
```

When the first folder is finished, tell the agent "update the wiki after `<folder>`". The skill creates `wiki/index.md` with its settings, `log.md` and the first topic page, then runs the lint.

The first wiki is small, and that is expected: a concept page appears only when an idea shows up in a second folder.

## 3. Existing project without notes

Two ways:

- **Recover the notes.** The agent writes a `NOTES.md` for each major stage from git history, pull requests, issues and docs. Each fact links its commit or pull request as the source. Whatever the sources do not show goes under "Open" or "Gaps". Then compile the wiki from those notes. Worth it for a portfolio, because the evidence is there.
- **Build on what is already there.** If the project has `docs/`, ADRs or runbooks, remove `x-wiki-evidence: NOTES.md` from the `wiki/index.md` frontmatter. The lint then accepts any source outside the wiki, and pages can cite those documents directly.

Do not write wiki pages without sources: that breaks the skill's main rule. Start with notes instead.

## 4. Make it stick

- Add one line to `AGENTS.md` or `CLAUDE.md`: "When a piece of work is finished, run the `wiki` skill's Compile for its folder."
- Run the lint in a pre-commit hook or CI:

  ```sh
  python3 .agents/skills/wiki/scripts/lint.py wiki
  ```

  It exits with 1 on any problem.
