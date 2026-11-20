#!/usr/bin/env python3
"""Check that every cited source ID resolves to the evidence base.

Reads settings from team/config.json ("provenance"):
  paths          globs of deliverable files to scan for citations
  exclude        globs to skip
  id_pattern     regex for source IDs (default SRC-[A-Za-z0-9_-]+)
  evidence_dir   where evidence files define IDs (default team/evidence)
  require_citations_in  globs of files that must each cite at least one ID

An ID is "defined" if it appears in the Sources section of an evidence file,
i.e. at the start of a line ("SRC-x: ...", "- SRC-x ...", "| SRC-x |").

If evidence.require_review is true in config, IDs count as defined only in
evidence files whose header says "Status: reviewed".

Usage: python3 check_provenance.py [--config team/config.json] [--require-citations] [--verbose]
Exit 1 if any cited ID is undefined, or (with --require-citations) a required file cites nothing.
"""
import fnmatch
import json
import re
import sys
from pathlib import Path


def arg(name, default):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default


full_cfg = json.load(open(arg("--config", "team/config.json")))
cfg = full_cfg.get("provenance", {})
require_review = (full_cfg.get("evidence") or {}).get("require_review", False)
pattern = re.compile(cfg.get("id_pattern", r"SRC-[A-Za-z0-9_-]+"))
ev_dir = Path(cfg.get("evidence_dir", "team/evidence"))
paths = cfg.get("paths", ["**/*.md"])
exclude = cfg.get("exclude", [])
required = cfg.get("require_citations_in", [])
root = Path(".")

defined, unreviewed = set(), set()
def_line = re.compile(r"^\s*(?:[-*|]\s*)?(" + pattern.pattern + r")\b")
status_line = re.compile(r"^\s*Status:\s*(\w+)", re.I | re.M)
for f in ev_dir.rglob("*"):
    if f.is_file() and f.suffix in (".md", ".txt", ".csv", ".json", ".yml", ".yaml", ".bib"):
        text = f.read_text(errors="ignore")
        m = status_line.search("\n".join(text.splitlines()[:10]))
        reviewed = bool(m and m.group(1).lower() == "reviewed")
        for line in text.splitlines():
            d = def_line.match(line)
            if d:
                (defined if reviewed or not require_review else unreviewed).add(d.group(1))


def match_any(p, globs):
    s = p.as_posix()
    return any(fnmatch.fnmatch(s, g) for g in globs)


files = set()
for g in paths:
    files.update(p for p in root.glob(g) if p.is_file())
files = sorted(p for p in files if not match_any(p, exclude) and ev_dir not in p.parents)

undefined, cited, no_cites = {}, set(), []
pending = {}
for f in files:
    ids = set(pattern.findall(f.read_text(errors="ignore")))
    cited |= ids
    for i in ids - defined:
        (pending if i in unreviewed else undefined).setdefault(i, []).append(f.as_posix())
    if "--require-citations" in sys.argv and required and match_any(f, required) and not ids:
        no_cites.append(f.as_posix())

print(f"Provenance: {len(files)} files scanned, {len(cited)} IDs cited, {len(defined)} defined in {ev_dir}")
if "--verbose" in sys.argv:
    unused = sorted(defined - cited)
    if unused:
        print(f"  info: {len(unused)} defined but never cited: {', '.join(unused[:15])}")
problems = False
if undefined:
    problems = True
    print("Undefined source IDs (cited but not in the evidence base):")
    for i, fs in sorted(undefined.items()):
        print(f"  {i}: {', '.join(fs[:5])}")
if pending:
    problems = True
    print("Cited IDs from evidence files not yet reviewed (Status: reviewed):")
    for i, fs in sorted(pending.items()):
        print(f"  {i}: {', '.join(fs[:5])}")
if no_cites:
    problems = True
    print("Files that must cite sources but cite none:")
    for f in no_cites:
        print(f"  {f}")
sys.exit(1 if problems else 0)

