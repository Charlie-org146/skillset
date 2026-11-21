#!/usr/bin/env python3
"""features-v1 run: every requirement on the wiki pages becomes a feature in place.

Each entry keeps its ID, page and words; its Reviewed mark and seal are cleared (all
Unreviewed) and a marker block of `  - ` bullets follows its sub-bullets. Marks and
generated blocks change only. A re-run strips the block and rebuilds it: same bytes.

  python3 docs/feature-migration/features-v1.py run [--base SHA] [--skip IDS] [--expect N] [--tools DIR]

Run from the repo root. Never prompts, never commits. The docs tool's parsers are found
at --tools, else $WORKFLOW_DOCS_SCRIPTS, else the installed workflow-docs skill.
Failure prints `REFUSED <CODE> <what>; fix: <fix>` on stderr, nothing is written,
exit 2 usage, 3 refusal, 4 setup. Last line on success: `RUN OK`.
Codes: E_USAGE bad argument. E_TOOLS parser files not found. E_COUNT count differs from
base or --expect. E_MARK a Reviewed line not on the base. E_HASH a requirement hash
changed. E_PARTIAL a write failed midway. E_DIRTY a target has uncommitted changes.
E_SETUP git or file error. Report: docs/feature-migration/features-v1-report.md
(a historical record of the migration at its base SHA; this script is archival).
"""
import argparse, hashlib, os, re, subprocess, sys

DIR = "docs/feature-migration"
REPORT = DIR + "/features-v1-report.md"
MARK = "  - Feature markers v1"
OLD = re.compile(r"^  - (Reference: |Line \d+: .*; test )")
FILES = ("criteria.py", "pageformat.py", "prdcopy.py", "entry.py", "docs.py")


def die(code, what, fix, rc=3):
    sys.stderr.write("REFUSED %s %s; fix: %s\n" % (code, what, fix))
    sys.exit(rc)


def git(*a):
    r = subprocess.run(["git"] + list(a), capture_output=True, text=True)
    if r.returncode:
        die("E_SETUP", "git %s failed" % a[0], "run from the repo root with the base fetched", 4)
    return r.stdout


def tools(given):
    found = given or os.environ.get("WORKFLOW_DOCS_SCRIPTS") or os.path.join(
        os.path.expanduser("~"), ".claude", "skills", "workflow-docs", "scripts")
    if not all(os.path.isfile(os.path.join(found, f)) for f in FILES):
        die("E_TOOLS", "parser files not found", "pass --tools DIR or set WORKFLOW_DOCS_SCRIPTS to the workflow-docs scripts folder", 4)
    sys.path.insert(0, found)
    sys.dont_write_bytecode = True
    mods = [__import__(n[:-3]) for n in FILES[:4]]
    hashes = " ".join(hashlib.sha256(open(os.path.join(found, f), "rb").read()).hexdigest()[:12] for f in FILES[:4])
    print("tools: %s %s" % ("/".join(found.rstrip("/").split("/")[-2:]), hashes))
    return mods


def strip(lines):
    out, i = [], 0
    while i < len(lines):
        if lines[i] == MARK:
            if out and out[-1] == "":
                out.pop()
            i += 1
            while i < len(lines) and OLD.match(lines[i]):
                i += 1
            continue
        out.append(lines[i])
        i += 1
    return out


def entries(lines, C):
    found = []
    for i, line in enumerate(lines):
        m = C.LINE.match(line)
        if m:
            found.append((i, m, C.subs(lines, i)))
    return found


def readme_map(text):
    sec, seen = 0, {}
    for line in text.split("\n"):
        h = re.match(r"^### (\d+)\. ", line)
        if h:
            sec = int(h.group(1))
        elif line.startswith("## "):
            sec = 0
        elif sec and line.startswith("|"):
            cells = line.split("|")
            ids = re.findall(r"^\[?([A-Z]{2,5}-\d+)\b", cells[1].strip())
            if len(cells) > 2:
                for grp in re.findall(r"absorbs ([A-Z0-9, -]+)", cells[2]):
                    ids += re.findall(r"[A-Z]{2,5}-\d+", grp)
            for x in ids:
                seen.setdefault(x, set()).add(sec)
    return seen


def metric_of(text, ident):
    m = re.search(r"(?ms)^## Success metrics\n(.*?)(?=^## |\Z)", text)
    n = 0
    for line in (m.group(1).split("\n") if m else []):
        if re.match(r"^(- |\d+\. )", line):
            n += 1
            if re.search(r"(?<![A-Za-z0-9-])%s(?![A-Za-z0-9-])" % re.escape(ident), line):
                return "Success metric %d of this page" % n
    return "metric missing"


def sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", choices=["run"])
    ap.add_argument("--base", default="")
    ap.add_argument("--skip", default="")
    ap.add_argument("--expect", type=int, default=0)
    ap.add_argument("--tools", default="")
    try:
        a = ap.parse_args()
    except SystemExit as e:
        sys.exit(2 if e.code else 0)
    if a.base and not re.fullmatch(r"[0-9a-f]{7,40}", a.base):
        die("E_USAGE", "--base must be a commit SHA", "pass a hex SHA", 2)
    skip = set(x for x in a.skip.split(",") if x)
    if not all(re.fullmatch(r"[A-Z]{2,5}-\d+", x) for x in skip):
        die("E_USAGE", "--skip must be IDs like AB-1", "pass IDs separated by commas", 2)
    C, F, P, E = tools(a.tools)
    root = git("rev-parse", "--show-toplevel").strip()
    os.chdir(root)
    base = a.base or git("merge-base", "HEAD", "origin/main").strip()
    wiki = "docs/wiki"
    linked, _loose = C.test_rows(root)
    readme = readme_map(open("README.md", encoding="utf-8").read())
    names = []
    for p in C.pages(root):
        n = os.path.basename(p)[:-3]
        if not n.startswith("How-to") and entries(open(p, encoding="utf-8").read().split("\n"), C):
            names.append(n)
    out, rows, marks, split, skipped, files = {}, [], [], [], [], {}
    bt = lambda path: git("show", "%s:%s" % (base, path))
    for n in names:
        page = "%s/%s.md" % (wiki, n)
        cp = ".loop/prd/%s.md" % n
        has_copy = P.copy_of(root, n) is not None
        btxt = bt(page)
        bl = btxt.split("\n")
        be = entries(bl, C)
        for _i, m, subs in be:
            if m.group(3):
                ok = C.seal_of(m.group(4), subs) == m.group(5)
                marks.append((m.group(1), n, m.group(3), m.group(5), "seal match" if ok else "seal stale", "page+copy" if has_copy else "page"))
        files[n] = (page, cp, has_copy, btxt, be)

    def make(lines, n, ptext):
        lines = strip(lines)
        added = []
        for i, m, subs in reversed(entries(lines, C)):
            ident = m.group(1)
            if ident in skip:
                skipped.append(ident)
                continue
            n_lines = max(1, len(subs))
            refs = readme.get(ident, set())
            ref = "Principle %d" % next(iter(refs)) if len(refs) == 1 else "reference missing"
            test = "%d linked rows, see Tests" % len(linked[ident]) if linked.get(ident) else "test missing"
            met = metric_of(ptext, ident)
            block = ["", MARK, "  - Reference: " + ref] + ["  - Line %d: %s; test %s" % (k, met, test) for k in range(1, n_lines + 1)]
            if m.group(3):
                lines[i] = "- %s: **Unreviewed** %s" % (ident, m.group(4))
            at = i + 1 + len(subs)
            lines[at:at] = block
            added.append((ident, n_lines, ref, met, test))
        return "\n".join(lines), added

    total = 0
    for n, (page, cp, has_copy, btxt, be) in files.items():
        cur = open(page, encoding="utf-8").read()
        for txt, path in [(cur, page)] + ([(open(cp, encoding="utf-8").read(), cp)] if has_copy else []):
            seen = set(bt(path).split("\n"))
            for _i, m, _s in entries(txt.split("\n"), C):
                if m.group(3) and m.group(0) not in seen:
                    die("E_MARK", "Reviewed line of %s in %s is not on the base" % (m.group(1), path), "a review was made after the base; re-freeze")
        if has_copy:
            ctxt = open(cp, encoding="utf-8").read()
            if P.with_block(cur, ctxt) != cur:
                die("E_HASH", "%s page and its copy disagree" % n, "run docs.py check and fix the page or copy first")
            new_copy, added = make(ctxt.split("\n"), n, cur)
            new_page = P.with_block(cur, new_copy)
            out[cp] = new_copy
        else:
            new_page, added = make(cur.split("\n"), n, cur)
        out[page] = new_page
        after = {m.group(1): (m, s) for _i, m, s in entries(new_page.split("\n"), C)}
        if len(after) != len(be):
            die("E_COUNT", "%s has %d entries after, %d on base" % (n, len(after), len(be)), "do not run on a page that changed since the base")
        for _i, m, subs in be:
            m2, s2 = after[m.group(1)]
            if F.unit(m.group(4), subs) != F.unit(m2.group(4), s2):
                die("E_HASH", "requirement %s text changed" % m.group(1), "report this; nothing was written")
            if E.requirements(btxt).get(m.group(1)) != E.requirements(new_page).get(m.group(1)):
                die("E_HASH", ".base hash of %s would change" % m.group(1), "report this; nothing was written")
        for ident, nl, ref, met, test in reversed(added):
            hb = sha(F.unit(after[ident][0].group(4), after[ident][1]))
            rows.append((ident, n, hb, nl, met, test, ref))
            if nl > 5:
                split.append((ident, nl))
        total += len(added)
    base_total = sum(len(v[4]) for v in files.values())
    if total + len(set(skipped)) != base_total or (a.expect and base_total != a.expect):
        die("E_COUNT", "%d on base, %d migrated, expected %s" % (base_total, total, a.expect or "any"), "re-measure and tell the owner before running")
    rows.sort(key=lambda r: (r[1], r[0]))
    rep = ["# Feature migration report (features-v1)", "",
           "Historical record of the migration at base `%s`; the two scripts beside it are archival." % base,
           "Per-line metric and test results are ID-level values repeated on each line (clause coverage is unknown;",
           "a linked test row may be a documentation check, not a behaviour check).",
           "Codes: E_USAGE E_TOOLS E_COUNT E_MARK E_HASH E_PARTIAL E_DIRTY E_SETUP (see `--help`).", "",
           "## Totals", "", "- features migrated %d (skipped %d: %s)" % (total, len(set(skipped)), ", ".join(sorted(set(skipped))) or "none"),
           "- marks cleared %d (seal stale %d)" % (len(marks), sum(1 for m in marks if m[4] == "seal stale")),
           "- features to split %d, lines %d" % (len(split), sum(r[3] for r in rows)),
           "- metric missing %d of %d" % (sum(1 for r in rows if r[4] == "metric missing"), len(rows)),
           "- test missing %d of %d" % (sum(1 for r in rows if r[5] == "test missing"), len(rows)),
           "- reference missing %d of %d" % (sum(1 for r in rows if r[6] == "reference missing"), len(rows)), "",
           "## Features", "", "| ID | page | hash before | hash after | lines | metric | test | reference |", "|---|---|---|---|---|---|---|---|"]
    rep += ["| %s | %s | %s | %s | %d | %s | %s | %s |" % (r[0], r[1], r[2], r[2], r[3], r[4], r[5], r[6]) for r in rows]
    rep += ["", "## Cleared marks", "", "| ID | page | date | seal | seal check | where | record |", "|---|---|---|---|---|---|---|"]
    rep += ["| %s | %s | %s | %s | %s | %s | record not available |" % m for m in sorted(marks)]
    rep += ["", "## To split (more than five lines)", ""] + ["- %s: %d lines" % s for s in sorted(split)]
    listed = [l for l in open("README.md", encoding="utf-8").read().split("\n") if "**Reviewed " in l]
    rep += ["", "## Listed, not edited", "", "- README lines with a Reviewed mark: %d" % len(listed)]
    out[REPORT] = "\n".join(rep) + "\n"
    targets = [p for p in out if p != REPORT]
    dirty = git("status", "--porcelain", "--", *targets).strip()
    if dirty:
        die("E_DIRTY", "targets have uncommitted changes: %s" % dirty.split("\n")[0][3:], "commit or discard them first")
    wrote, done = 0, []
    try:
        for path in targets + [REPORT]:
            old = open(path, encoding="utf-8").read() if os.path.exists(path) else None
            if old != out[path]:
                os.makedirs(os.path.dirname(path), exist_ok=True)
                tmp = path + ".tmp"
                open(tmp, "w", encoding="utf-8", newline="").write(out[path])
                os.replace(tmp, path)
                done.append(path)
                wrote += 1
    except OSError as e:
        die("E_PARTIAL", "write failed after %d files (%s)" % (len(done), e.strerror), "git checkout -- %s" % " ".join(done))
    print("features %d, marks cleared %d, to split %d" % (total, len(marks), len(split)))
    print("wrote %d files" % wrote)
    print("RUN OK")


if __name__ == "__main__":
    main()
