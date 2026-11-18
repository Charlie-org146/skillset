# Design: docs-v2-migration

Status: APPROVED (unattended, recommended answers taken)

## Problem
Skillset's docs predate the template's v2.0 format. The README holds install steps, usage tables and a settings block; Bass-tab.md has no Revisions section; there is no How-to-use page; Home has links outside the repo and no system diagram.

## Premises
1. The goal is format-only: no requirement wording changes, no content is lost (it moves).
2. The only PRD page is Bass-tab; its requirements are BAS-1..BAS-10 (Reviewed lines stay Reviewed, seals untouched).
3. The README may hold only its title, principles with the enforcing requirement IDs, and one link to Home.

## Approaches
- A (minimal): shrink README, add Revisions, patch findings one by one.
- B (recommended, template pattern): README = title + template line + one Home link + a few principles, each with a one-line statement and "Enforced by: BAS-n" lines; Home takes the install, check, license and use text plus a system diagram; new `How-to-use-Bass-tab.md` takes the "You say / What happens" table, usage commands and the check command; Bass-tab.md migrated with `criteria.py migrate` (owner record needed); regenerate Settings/Automation blocks and START.md with the tools.
- C (lateral): add a Principles.md page like the template. Rejected: the README must hold the principles, a second page is a copy.

## Design (approach B)
Principles (statements drawn from the existing requirements, none new):
1. One format for every song: BAS-1, BAS-10, BAS-4
2. The whole song at a glance, fitting a printout: BAS-2, BAS-3, BAS-7
3. Only what the sources show: BAS-6, BAS-8, BAS-5
4. Works for the player's bass: BAS-9
(mapping checked against each requirement's text at build time.)

Content moves (nothing dropped): the skills table, Install, Use bass-tab, Check and License move to Home and How-to-use-Bass-tab. The README keeps the template and the Home link. README settings/automation blocks move out (they are Home's generated blocks). Home: remove the outside-repo links by saying them in words (the Runbook links in the automation text come from `.loop/config.json` and are generated; the config's automation text is changed to words or the links go under public_origins only if they are skillset's own site, which they are not), add a system diagram, point How to use at the How-to page.
How-to-use-Bass-tab: What it's for, How to reach or run it, URLs and deployments, Automations and schedules, Runbooks, Links; with a system diagram.
Revisions: `criteria.py migrate --owner-record <id> --page Bass-tab`. If no owner record covers it, the step waits (PENDING).
Raw URLs to skillset's own site: add the origin to `public_origins` in `.loop/config.json` only if a page needs a raw URL.
START.md: render at the committed floor (4) and set a local 2.0 only for lanes.

## Risks
- The installed docs check may still demand the old README front door (DOC-5 How to use tables) until the template's v1.0.69 checks are installed; the build runs `docs.py check` and `wiki.py prepare` and reports any finding that conflicts with the frozen done line instead of changing the line.
- Migrate needs an owner record (owner-words.tsv).

## Success
README matches the template pattern; every PRD page has Revisions; `wiki.py prepare` prints no finding for a changed page.
