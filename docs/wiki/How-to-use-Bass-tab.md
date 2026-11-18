<!-- workflow-docs -->
# How to use Bass tab

## What it's for

Turns my sources for a song into one compact bass tab and a one-or-two-page play-along chart PDF, in the same format for every song. Each skill in this repo is a small, standalone folder under `skills/` with a `SKILL.md` and whatever scripts and templates it needs. Sources are anything I provide: a screenshot or PDF of a tab, notes, links. The skill never invents bars or lyrics; links to recordings contribute a title, tempo and section names at most.

### What's delivered

| Component | Kind | What it is | How a user uses it |
|---|---|---|---|
| `/bass-tab` | Skill | The folder `skills/bass-tab` with its `SKILL.md`, scripts and templates, portable across Claude Code, Codex and other agents that read `SKILL.md`. | Copy the folder into the agent's skills folder, then ask for a bass tab and give sources. |
| `tabgen.py` | Command | Renders a song file to the compact text tab. | `python3 scripts/tabgen.py song/song.py song/song.tab --bars 3 --cut compact`, run from `skills/bass-tab`. |
| `chart2pdf.py` | Command | Renders a song file to the 1-2 page chart PDF. | `python3 scripts/chart2pdf.py song/song.py -o song/song.pdf`, run from `skills/bass-tab`. |
| `sh tests/bass-tab/run.sh` | Command | Renders the fixture song, compares the text tab with its recorded baseline, builds the PDF and checks script sizes and that no personal strings are present. | `sh tests/bass-tab/run.sh`. |

### System diagram

```text
[Skill: /bass-tab | the agent session] --reads my sources--> (song file written from what they show)
[Command: tabgen.py | the repo checkout] --renders the song file--> (compact text tab)
[Command: chart2pdf.py | the repo checkout] --renders the song file--> (chart PDF, one or two pages)
[Command: sh tests/bass-tab/run.sh | the repo checkout] --renders the fixture and compares--> (baseline match, script sizes, no personal strings)

Legend: a box is Kind, Component and where it runs; --text--> a flow of data or control; (text) a part outside the table.
```

## How to reach or run it

Say these to your agent. Each part below has the exact commands.

**Install a skill**

Copy the skill's folder into your agent's skills directory.

```sh
# Claude Code (all projects)
cp -R skills/bass-tab ~/.claude/skills/bass-tab
# or one project
cp -R skills/bass-tab <project>/.claude/skills/bass-tab
```

For Codex or another agent that reads `SKILL.md`, put the folder wherever that agent looks for skills (for example `~/.codex/skills/` or `.agents/skills/`). Skills use `python3` and the standard library; bass-tab also uses Pillow for a non-Latin title, artist or lyrics, and without it refuses rather than print `?` unless told `--allow-lossy`.

**Use bass-tab**

Ask your agent for a bass tab and give it sources. It writes a song file from what the sources show, then renders it:

```sh
cd skills/bass-tab
python3 scripts/tabgen.py song/song.py song/song.tab --bars 3 --cut compact
python3 scripts/chart2pdf.py song/song.py -o song/song.pdf   # 1-2 page chart
```

Start a song file from `skills/bass-tab/templates/song-template.py`. Links to recordings contribute a title, tempo and section names at most; the skill never invents bars or lyrics (lyrics come from the owner or from what a source visibly shows).

**Check**

```sh
sh tests/bass-tab/run.sh
```

Renders the fixture song, compares the text tab with a recorded baseline, builds the PDF, and checks script sizes (each under 20 KB) and that no personal strings are present.

| You say | What happens |
|---|---|
| "Make a bass tab of this song from these sources" | A song file is written from what the sources show, then the compact tab and a one-or-two-page chart PDF are made. |
| "Fix bar 12 in this tab and print it again" | The song file is corrected once, so every copy of a repeated figure changes, and the chart is printed again. |
| "Make the chart for this 5-string song with a low B" | The tab draws five string lines, labeled to match the tuning. |
| "What's in the header and where did each part come from?" | You get the header (title, artist, BPM, key, time signature, tuning, instrument and sources; a field no source shows is left out, and a missing title reads "not shown") and the source report. |
| "Which bars are missing or guessed?" | The source report lists missing bars, estimated bars and which source gave each section; on the chart, two or more empty missing bars in a row (no notes, chord or lyric) print as one line with their range, cut at each section start. |

- BAS-1: One format, Songsterr-style. Example, from the bas-tab-baseline test: given the fixture song, when its compact text tab is generated, then it matches the recorded baseline byte for byte.
- BAS-2: The whole song at a glance. Example, from the bas-chart-layout test: given an invented song with sections, repeats and lyrics, when its chart is rendered, then each section has a bold label, the repeated bars print once with a count, and each lyric sits under its own bar.
- BAS-6: Only what the sources show. Example: a person reading the source report checks that each bar, chord and lyric traces to a source I provided; the nightly run checks the report's format (BAS-8).
- BAS-7: Song header. Example, from the bas-header test: given a song whose source shows only a title, when its chart is rendered, then the title prints and header fields with no value are left out.
- BAS-8: Source report. Example, from the bas-source-report test: given a song with a source report, when its chart is rendered, then missing bars, estimates and the source per section print after the last stave line.
- BAS-9: Four- and five-string bass. Example, from the bas-five-string test: given a 5-string and a 4-string song, when each chart is rendered, then the first draws five stave lines and the second four.
- BAS-10: One format template. Example, from the bas-template test: given a changed copy of the format template, when two songs are rendered through it, then both follow it.

### Skill: /bass-tab
- **Say:** "Make a bass tab of this song from these sources"
- **Command:** `/bass-tab`

### Command: tabgen.py
- **Command:** `python3 scripts/tabgen.py song/song.py song/song.tab --bars 3 --cut compact`
- **Dry run:** none needed: it only renders a file.
- **Reads:** the song file.
- **Writes:** the text tab named on the command line.
- **Exit codes:** 0 on success; a refusal prints a line naming the fix.

### Command: chart2pdf.py
- **Command:** `python3 scripts/chart2pdf.py song/song.py -o song/song.pdf`
- **Dry run:** none needed: it only renders a file.
- **Reads:** the song file and the format template.
- **Writes:** the PDF named after `-o`.
- **Exit codes:** 0 on success; a song that cannot fit two pages, or a non-Latin text with no Pillow and no `--allow-lossy`, is refused with a line naming it.

### Command: sh tests/bass-tab/run.sh
- **Command:** `sh tests/bass-tab/run.sh`
- **Dry run:** none needed.
- **Reads:** the fixture song and its recorded baseline.
- **Writes:** temporary files only.
- **Exit codes:** 0 when every check passes.

## URLs and deployments

- Wiki: [Bass-tab](https://github.com/jcl2018/skillset/wiki/Bass-tab)
- Milestone: [Bass-tab](https://github.com/jcl2018/skillset/milestone/1)
- Releases: https://github.com/jcl2018/skillset/releases

Skills are meant to be listed on Agensi later; there is no deployment yet.

## Automations and schedules

None for this feature: the repo's health and regression rounds run on its Mac as listed on Home.

## Runbooks

None: a failed chart prints the line that names its fix.

## Links

- PRD page: [Bass-tab](Bass-tab)
- License: MIT, see the LICENSE file in the repo root.
- Backlog: [Backlog: Bass-tab](https://github.com/jcl2018/skillset/milestones)
