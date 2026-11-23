#!/usr/bin/env python3
"""Mechanical health check for an agent-compiled wiki: frontmatter, links, orphans, evidence.

Usage:
  python3 lint.py [wiki-dir] [--sections topics,concepts] [--evidence NOTES.md]

  --sections  subfolders whose pages must cite a source (default: topics,concepts)
  --evidence  file name a source link must point to (default: any file outside wiki-dir)

Exit code 1 if any problem is found. Python 3.8+, standard library only.
"""
import argparse
import re
import sys
from pathlib import Path

RESERVED = {"index.md", "log.md"}
REQUIRED = ("type", "title", "description")
LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
RESOURCE = re.compile(r"resource:\s*([^,}\s]+)")


def frontmatter(text):
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    return text[4:end] if end != -1 else None


def local_links(text):
    """Markdown link targets plus frontmatter `resource:` paths that are local files."""
    fm = frontmatter(text) or ""
    for target in LINK.findall(text) + RESOURCE.findall(fm):
        if re.match(r"[a-z]+:", target) or target.startswith("#"):
            continue
        yield target.split("#")[0]


def cites_source(page, text, wiki, evidence):
    for target in local_links(text):
        path = (page.parent / target).resolve()
        if evidence:
            if path.name == evidence:
                return True
        elif wiki not in path.parents:
            return True
    return False


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("wiki", nargs="?", default="wiki")
    ap.add_argument("--sections", default="topics,concepts")
    ap.add_argument("--evidence", default=None)
    args = ap.parse_args()

    wiki = Path(args.wiki).resolve()
    sections = {s.strip() for s in args.sections.split(",") if s.strip()}
    problems = []
    index_text = (wiki / "index.md").read_text(encoding="utf-8")
    indexed = {(wiki / t).resolve() for t in local_links(index_text)}

    for page in sorted(wiki.rglob("*.md")):
        rel = page.relative_to(wiki)
        text = page.read_text(encoding="utf-8")
        for target in local_links(text):
            if not (page.parent / target).resolve().exists():
                problems.append(f"{rel}: broken link {target}")
        if page.name in RESERVED and page.parent == wiki:
            continue
        fm = frontmatter(text)
        if fm is None:
            problems.append(f"{rel}: no frontmatter")
        else:
            for key in REQUIRED:
                if not re.search(rf"^{key}:", fm, re.M):
                    problems.append(f"{rel}: frontmatter has no {key}")
        if page.resolve() not in indexed:
            problems.append(f"{rel}: not listed in index.md")
        if rel.parts[0] in sections and not cites_source(page, text, wiki, args.evidence):
            what = args.evidence or "a source outside the wiki"
            problems.append(f"{rel}: no link to {what}")

    for p in problems:
        print(p)
    print(f"{'FAIL' if problems else 'OK'}: {len(problems)} problem(s) in {wiki}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
