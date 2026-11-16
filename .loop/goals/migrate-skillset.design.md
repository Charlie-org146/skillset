# Design: migrate-skillset

## Problem
skillset's `.loop/config.json` is at template_version 0.27.58; the template is at v1.0.0 and the installed skills (symlinks into the template checkout) are now v1.0.0. `setup.py migration-check --offline` shows 7 PR-closable gaps: stale START.md (MIG_FILES), ten missing settings (MIG_SETTINGS), a Usage section in Bass-tab.md (MIG_USAGE, MIG_FORMAT), missing `.loop/health-rules.json` (MIG_RULES), and stale Settings blocks in Home.md and README.md (MIG_BLOCKS). `health.py check` is not green: 75 pass, 15 warn, 1 fail.

## Approaches
1. Run `update.py --apply --repo .` in the goal worktree, then the generators the gaps name (`render.py blocks`, `entry.py write`, setup for `health-rules.json`), delete the Usage section, rerun the check. Cost: small, mostly generated files. Risk: the update could touch reviewed PRD text or write ~/.workflow-loop.
2. Hand-edit each file. Cost: larger, drifts from generators. Rejected.

## Chosen
Approach 1, run with the repo's own tooling only. update.py reads ~/.workflow-loop but writes nothing there (checked in its source); I will confirm with a before/after hash and never run a command that writes private settings (no `setup.py` default run). Reviewed requirement text stays untouched: only the Usage section (not a requirement) goes, as MIG_USAGE demands. Owner steps the check lists (Backlog milestones, hooks in the operation repo) are reported, not done.

## Done lines
- v1.0 skills installed, template_version 1.0.0, no reviewed PRD text changed, nothing written to ~/.workflow-loop: update.py --apply plus a home-folder hash and a diff of requirement lines.
- migration-check no gaps: rerun with --repo . --pr (the PR-closable codes).
- health.py check clean or each finding listed with its cause: rerun; list the rest in the PR body.
- regression rows run: `regression.py run` per row without `--live` (GitHub issue read still 504s).

## Open questions
None for the owner; the three OWNER STEP lines are reported in the PR.
