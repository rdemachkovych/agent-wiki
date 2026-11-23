#!/usr/bin/env python3
"""Mechanical health check for an agent-compiled wiki (an OKF v0.3 bundle).

Usage:
  python3 lint.py [wiki-dir] [--sections topics,concepts] [--evidence NOTES.md]

Settings come from the root index.md frontmatter (OKF extension keys), and a
flag overrides them:
  x-wiki-sections: [topics, concepts]   subfolders whose pages must cite a source
  x-wiki-evidence: NOTES.md             file name a source must point to
                                        (unset: any file outside the wiki)

Checks: root index.md has okf_version; log.md and sub-indexes have no
frontmatter; pages have type, title, description; status is draft, stable or
deprecated; superseded_by only on deprecated pages; tags is a list; timestamps
in generated / verified / stale_after are a date or a date-time with an offset;
Markdown links and path fields (resource, sources[].resource, superseded_by)
resolve; [[wikilinks]] are not used; every page is in index.md; pages in the
evidence sections cite a source.

Exit code 1 if any problem is found. Python 3.8+, standard library only.
"""
import argparse
import re
import sys
import urllib.parse
from pathlib import Path

RESERVED = {"index.md", "log.md"}
REQUIRED = ("type", "title", "description")
STATUSES = {"draft", "stable", "deprecated"}
LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)\)")
WIKILINK = re.compile(r"\[\[[^\]]+\]\]")
PATH_FIELD = re.compile(r"\b(resource|superseded_by):\s*(\"[^\"]*\"|'[^']*'|[^,}\n]+)")
TIME_FIELD = re.compile(r"\b(at|stale_after):\s*(\"[^\"]*\"|'[^']*'|[^,}\s]+)")
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
DATETIME = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:\d{2})$")
FENCE = re.compile(r"^(```|~~~).*?^\1", re.M | re.S)
CODE = re.compile(r"`[^`\n]*`")


def split(text):
    """Return (frontmatter or None, body). The block ends at the next line that is exactly ---."""
    lines = text.split("\n")
    if not lines or lines[0].rstrip("\r") != "---":
        return None, text
    for i, line in enumerate(lines[1:], 1):
        if line.rstrip("\r") == "---":
            return "\n".join(lines[1:i]), "\n".join(lines[i + 1:])
    return None, text


def scalar(fm, key):
    m = re.search(rf"^{re.escape(key)}:[ \t]*(.*)$", fm or "", re.M)
    return m.group(1).strip().strip("\"'") if m else None


def as_list(value):
    if value is None:
        return None
    if value.startswith("[") and value.endswith("]"):
        return [v.strip().strip("\"'") for v in value[1:-1].split(",") if v.strip()]
    return [value]


def unquote(value):
    value = value.strip()
    if len(value) > 1 and value[0] == value[-1] and value[0] in "\"'":
        value = value[1:-1]
    return value


def body_links(body):
    body = CODE.sub("", FENCE.sub("", body))
    return LINK.findall(body)


def path_fields(fm):
    """Path-field values that are local paths: not URLs, not scope descriptors (they contain spaces)."""
    out = []
    for key, raw in PATH_FIELD.findall(fm or ""):
        value = unquote(raw)
        if not value or " " in value or re.match(r"[a-z][a-z0-9+.-]*:", value, re.I):
            continue
        out.append((key, value))
    return out


def resolve(target, page, wiki):
    clean = urllib.parse.unquote(target.split("#", 1)[0].split("?", 1)[0])
    if not clean:
        return None
    if clean.startswith("/"):
        return (wiki / clean.lstrip("/")).resolve()
    return (page.parent / clean).resolve()


def local(target):
    return not (re.match(r"[a-z][a-z0-9+.-]*:", target, re.I) or target.startswith("#"))


def main():
    ap = argparse.ArgumentParser(description="Health check for an agent-compiled OKF wiki.")
    ap.add_argument("wiki", nargs="?", default="wiki")
    ap.add_argument("--sections", default=None)
    ap.add_argument("--evidence", default=None)
    args = ap.parse_args()

    wiki = Path(args.wiki).resolve()
    problems = []
    root_index = wiki / "index.md"
    if not root_index.exists():
        print(f"FAIL: no index.md in {wiki}")
        return 1
    root_fm, root_body = split(root_index.read_text(encoding="utf-8"))
    if root_fm is None or not scalar(root_fm, "okf_version"):
        problems.append('index.md: frontmatter has no okf_version (write okf_version: "0.3")')
    for key in ("title", "description"):
        if root_fm is not None and not scalar(root_fm, key):
            problems.append(f"index.md: frontmatter has no {key}")

    sections = args.sections.split(",") if args.sections else as_list(scalar(root_fm, "x-wiki-sections")) or ["topics", "concepts"]
    sections = {s.strip() for s in sections if s.strip()}
    evidence = args.evidence or scalar(root_fm, "x-wiki-evidence") or None
    indexed = {resolve(t, root_index, wiki) for t in body_links(root_body) if local(t)}

    for page in sorted(wiki.rglob("*.md")):
        rel = page.relative_to(wiki)
        if any(part.startswith(".") for part in rel.parts):
            continue
        fm, body = split(page.read_text(encoding="utf-8"))
        targets = [t for t in body_links(body) if local(t)]
        fields = path_fields(fm) if page != root_index else []

        for target in targets + [v for _, v in fields]:
            path = resolve(target, page, wiki)
            if path is not None and not path.exists():
                problems.append(f"{rel}: broken link {target}")
        if WIKILINK.search(CODE.sub("", FENCE.sub("", body))):
            problems.append(f"{rel}: [[wikilink]] is not a link in OKF; write [text](path)")

        if page.name in RESERVED:
            if fm is not None and page != root_index:
                problems.append(f"{rel}: {page.name} must have no frontmatter")
            continue

        if fm is None:
            problems.append(f"{rel}: no frontmatter")
            continue
        for key in REQUIRED:
            if not scalar(fm, key):
                problems.append(f"{rel}: frontmatter has no {key}")
        status = scalar(fm, "status")
        if status and status not in STATUSES:
            problems.append(f"{rel}: status {status!r} is not draft, stable or deprecated")
        if scalar(fm, "superseded_by") and status != "deprecated":
            problems.append(f"{rel}: superseded_by without status: deprecated")
        tags = scalar(fm, "tags")
        if tags and not tags.startswith("["):
            problems.append(f"{rel}: tags must be a YAML list, e.g. tags: [a, b]")
        for key, raw in TIME_FIELD.findall(fm):
            value = unquote(raw)
            if not (DATE.match(value) or DATETIME.match(value)):
                problems.append(f"{rel}: {key} {value!r} is not a date or a date-time with an offset")
        if page.resolve() not in indexed:
            problems.append(f"{rel}: not listed in index.md")

        if rel.parts[0] in sections:
            cited = [resolve(t, page, wiki) for t in targets + [v for k, v in fields if k == "resource"]]
            cited = [p for p in cited if p is not None]
            ok = any(p.name == evidence for p in cited) if evidence else any(wiki not in p.parents for p in cited)
            if not ok:
                problems.append(f"{rel}: no link to {evidence or 'a source outside the wiki'}")

    for p in problems:
        print(p)
    print(f"{'FAIL' if problems else 'OK'}: {len(problems)} problem(s) in {wiki}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
