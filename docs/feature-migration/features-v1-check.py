#!/usr/bin/env python3
"""features-v1 check: proves the migration against the base. Writes nothing to the repo.

  python3 docs/feature-migration/features-v1-check.py check [--base SHA] [--tools DIR]

Run from the repo root on the committed HEAD. Proves, from the report and `git show`:
1 every requirement's text hash is equal at base and HEAD, and migrated + skipped equals
the base count; 2 each page and copy, with its blocks stripped and its marks restored from
the report, equals the base byte for byte, every changed path is allowed (printed), and the
docs gates print the same STALE lines in a base clone and a HEAD clone; 3 test-link counts
equal and every line carries a metric, test and reference result; 4 no Reviewed mark is left
and the report's marks equal the base's; 5 a second `run` in a clone leaves an empty diff.
Never prompts. Prints PASS or FAIL per proof, then `CHECK OK` or `CHECK FAILED <n>`.
Failure: `REFUSED <CODE> ...` on stderr, exit 3 (refusal), 4 (setup), 2 (usage).
Codes: E_USAGE E_TOOLS E_SETUP E_GATE (a proof failed).
"""
import argparse, hashlib, os, re, shutil, subprocess, sys, tempfile

DIR = "docs/feature-migration"
REPORT = DIR + "/features-v1-report.md"
MARK = "  - Feature markers v1"
OLD = re.compile(r"^  - (Reference: |Line \d+: .*; test )")
FILES = ("criteria.py", "pageformat.py", "prdcopy.py", "entry.py", "docs.py")
TOLERATED = (".loop/goals/", ".loop/regression-", ".loop/queue.md", ".loop/findings.md", ".loop/milestones", "docs/wiki/Tests.md")
bad = []


def die(code, what, fix, rc=3):
    sys.stderr.write("REFUSED %s %s; fix: %s\n" % (code, what, fix))
    sys.exit(rc)


def run(args, cwd=None, env=None):
    return subprocess.run(args, capture_output=True, text=True, cwd=cwd, env=env)


def git(*a, cwd=None):
    r = run(["git"] + list(a), cwd)
    if r.returncode:
        die("E_SETUP", "git %s failed" % a[0], "run from the repo root with the base fetched", 4)
    return r.stdout


def say(ok, text):
    print("%s %s" % ("PASS" if ok else "FAIL", text))
    if not ok:
        bad.append(text)


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


def stale(tools, cwd):
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    got = []
    for cmd in (["docs.py", "check"], ["criteria.py", "render", "--check"]):
        r = run(["python3", os.path.join(tools, cmd[0])] + cmd[1:], cwd, env)
        got += sorted(l[:60] for l in (r.stdout + r.stderr).split("\n") if l.startswith("STALE") and "commits since" not in l)
    return got


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", choices=["check"])
    ap.add_argument("--base", default="")
    ap.add_argument("--tools", default="")
    try:
        a = ap.parse_args()
    except SystemExit as e:
        sys.exit(2 if e.code else 0)
    found = a.tools or os.environ.get("WORKFLOW_DOCS_SCRIPTS") or os.path.join(
        os.path.expanduser("~"), ".claude", "skills", "workflow-docs", "scripts")
    if not all(os.path.isfile(os.path.join(found, f)) for f in FILES):
        die("E_TOOLS", "parser files not found", "pass --tools DIR or set WORKFLOW_DOCS_SCRIPTS", 4)
    sys.path.insert(0, found)
    sys.dont_write_bytecode = True
    C, F = __import__("criteria"), __import__("pageformat")
    print("tools: %s %s" % ("/".join(found.rstrip("/").split("/")[-2:]), " ".join(
        hashlib.sha256(open(os.path.join(found, f), "rb").read()).hexdigest()[:12] for f in FILES[:4])))
    root = git("rev-parse", "--show-toplevel").strip()
    os.chdir(root)
    head = git("rev-parse", "HEAD").strip()
    base = a.base or git("merge-base", "HEAD", "origin/main").strip()
    show = lambda ref, path: git("show", "%s:%s" % (ref, path))
    rep = show(head, REPORT).split("\n")
    feats = [[c.strip() for c in l.strip("|").split("|")] for l in rep if re.match(r"^\| [A-Z]{2,5}-\d+ \|", l) and l.count("|") == 9]
    marks = [[c.strip() for c in l.strip("|").split("|")] for l in rep if re.match(r"^\| [A-Z]{2,5}-\d+ \|", l) and l.count("|") == 8]
    tot = re.search(r"features migrated (\d+) \(skipped (\d+)", "\n".join(rep))
    pages = sorted(set(f[1] for f in feats))
    copy = lambda n: ".loop/prd/%s.md" % n
    has_copy = {n: run(["git", "cat-file", "-e", "%s:%s" % (base, copy(n))]).returncode == 0 for n in pages}
    paths = ["docs/wiki/%s.md" % n for n in pages] + [copy(n) for n in pages if has_copy[n]]
    print("head %s base %s" % (head[:8], base[:8]))
    # 1 text hashes
    n_base, same = 0, True
    for n in pages:
        for p in ("docs/wiki/%s.md" % n,):
            bl, hl = show(base, p).split("\n"), show(head, p).split("\n")
            be = {m.group(1): F.unit(m.group(4), s) for i, l in enumerate(bl) for m in [C.LINE.match(l)] if m for s in [C.subs(bl, i)]}
            he = {m.group(1): F.unit(m.group(4), s) for i, l in enumerate(hl) for m in [C.LINE.match(l)] if m for s in [C.subs(hl, i)]}
            n_base += len(be)
            same &= be == he
    say(same, "1 requirement text hash equal per ID at base and HEAD")
    say(bool(tot) and n_base == int(tot.group(1)) + int(tot.group(2)) == len(feats) + int(tot.group(2)), "1 base %d = migrated + skipped, %d report rows" % (n_base, len(feats)))
    # 2 byte proof, allowed paths, gates
    for p in paths:
        n = os.path.basename(p)[:-3]
        lines = strip(show(head, p).split("\n"))
        by = {m[0]: m for m in marks if m[1] == n}
        for i, l in enumerate(lines):
            m = re.match(r"^- ([A-Z]{2,5}-\d+): \*\*Unreviewed\*\* (\S.*)$", l)
            if m and m.group(1) in by:
                lines[i] = "- %s: **Reviewed %s** %s <!-- reviewed %s -->" % (m.group(1), by[m.group(1)][2], m.group(2), by[m.group(1)][3])
        say("\n".join(lines) == show(base, p), "2 byte proof %s" % p)
    changed = git("diff", "--name-only", base, head).split()
    allowed = set(paths) | {REPORT, DIR + "/features-v1.py", DIR + "/features-v1-check.py"}
    extra = [c for c in changed if c not in allowed]
    say(all(c.startswith(TOLERATED) for c in extra), "2 changed paths allowed; also changed (named): %s" % (", ".join(extra) or "none"))
    tmp = tempfile.mkdtemp(prefix="f1check")
    try:
        cl = {}
        for tag, ref in (("base", base), ("head", head)):
            cl[tag] = os.path.join(tmp, tag)
            run(["git", "clone", "-q", "--local", "--no-checkout", root, cl[tag]])
            run(["git", "checkout", "-q", "--detach", ref], cl[tag])
        sb, sh = stale(found, cl["base"]), stale(found, cl["head"])
        say(sb == sh, "2 docs gates print the same STALE lines in a base clone (%d) and a HEAD clone (%d)" % (len(sb), len(sh)))
        real = stale(found, root)
        print("INFO real tree prints %d STALE lines; clones print %d (clone-only: %s)" % (len(real), len(sh), ", ".join(sorted(set(sh) - set(real))) or "none"))
        # 5 idempotence in a clone
        r = run(["python3", DIR + "/features-v1.py", "run", "--base", base, "--tools", found], cl["head"])
        st = run(["git", "status", "--porcelain"], cl["head"]).stdout.strip()
        say("wrote 0 files" in r.stdout and not st and r.returncode == 0, "5 second run leaves an empty diff (%s)" % (r.stdout.strip().split("\n")[-2:-1] or r.stderr.strip()[:80]))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    # 3 tests and results
    linked, _l = C.test_rows(root)
    okt = all((f[6] == "test missing") == (not linked.get(f[0])) and (f[6] == "test missing" or f[6].startswith("%d linked rows" % len(linked[f[0]]))) for f in feats)
    say(okt, "3 test-link counts equal per ID")
    res = True
    for n in pages:
        for l in show(head, "docs/wiki/%s.md" % n).split("\n"):
            res &= not (l.startswith("  - Line ") and "; test " not in l)
    say(res and all(f[5] and f[6] and f[7] for f in feats), "3 every line carries a metric and test result, every feature a reference result")
    # 4 marks
    left = sum(1 for p in paths for l in show(head, p).split("\n") if (m := C.LINE.match(l)) and m.group(3))
    say(left == 0, "4 no Reviewed mark is left on any page or copy")
    bm = set()
    for n in pages:
        bl = show(base, "docs/wiki/%s.md" % n).split("\n")
        for i, l in enumerate(bl):
            m = C.LINE.match(l)
            if m and m.group(3):
                bm.add((m.group(1), n, m.group(3), m.group(5)))
    say(bm == set((m[0], m[1], m[2], m[3]) for m in marks), "4 the report's %d cleared marks equal the base's %d" % (len(marks), len(bm)))
    if bad:
        print("CHECK FAILED %d" % len(bad))
        sys.exit(3)
    print("CHECK OK head %s base %s" % (head[:8], base[:8]))


if __name__ == "__main__":
    main()
