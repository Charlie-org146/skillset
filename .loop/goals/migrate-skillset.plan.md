# Plan: migrate-skillset

Checked: `update.py` (reads ~/.workflow-loop/repos, writes only the repo half and the skills stamp), `setup.py migration-check`, `render.py blocks`, `entry.py write`, `health.py check` all exist under `~/.claude/skills/workflow-*/scripts` (symlinks into the template, now v1.0.0).

## Build steps
1. Record a hash of ~/.workflow-loop and a copy of the requirement lines of `docs/wiki/*.md`.
2. `update.py --apply --repo .` in this worktree; read its output for UPDATE_* refusals.
3. Fill what migration-check still names: `render.py blocks` (Home.md, README.md), `entry.py write` (START.md), the missing settings and `.loop/health-rules.json` through the repo-half generators only, never a default `setup.py` run (it writes private settings).
4. Delete the Usage section of `docs/wiki/Bass-tab.md`, then `docs.py audit`.
5. Rerun `migration-check --repo . --pr`, `health.py check`, and each regression row without `--live`.
6. Compare the hash and the requirement lines to step 1.

## Test per done line
- v1.0 installed, template_version 1.0.0: `config.json` shows it; hash unchanged; requirement-line diff empty.
- migration-check: exit 0, `MIGRATION OK`.
- health: green, or each remaining WARN/FAIL listed in the PR body with its cause.
- Regression rows: every row passes, or each failure is listed with its cause.

## What could break
`update.py` rewriting reviewed requirement text (step 6 catches it); CRLF noise in generated files; health FAIL that predates the migration (list it, do not fix it).

## Out of scope
Owner steps (Backlog milestones, hooks in the operation repo), skillset feature work, GitHub issue changes.

VERDICT: self: plan covers every done line
