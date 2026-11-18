# Plan: docs-v2-migration (condensed review)

1. Migrate Bass-tab.md: `criteria.py migrate --owner-record o2 --goal docs-v2-migration --page Bass-tab`; diff must show only a Revisions section added (and review stamps unchanged); no requirement line edited.
2. Write docs/wiki/How-to-use-Bass-tab.md (sections: What it's for, How to reach or run it, URLs and deployments, Automations and schedules, Runbooks, Links; system diagram; the README's "You say / What happens" table, install, usage and check commands move here). Map it in .loop/docs.tsv.
3. Rewrite README.md: title, template block, one link to wiki Home, then principles (statement, system diagram not required, "Enforced by: BAS-n" lines) built from the existing requirements; keep license line only if the template pattern keeps it, else move it to Home.
4. Update Home.md: features table row How-to-use link to the new page, system diagram block, Install / Check / License text moved from README, outside-repo links said in words (edit the automation entries in .loop/config.json), keep generated blocks.
5. Re-render generated blocks (docs.py audit / render), regenerate START.md at the committed floor (4), set a local 2.0 floor only for lanes.
6. Verify: docs.py check, wiki.py prepare docs-v2-migration (no finding for changed pages), diff of Bass-tab shows format-only change, grep that every dropped README line exists elsewhere.

Review (one round): scope is docs only, wording of requirements untouched, no new tests needed (regression rows already cover BAS-*); risk is the installed check enforcing the old README shape: if so report and keep the done line.
