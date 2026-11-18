<!-- workflow-docs -->
# Bass-tab

How to use: [How-to-use-Bass-tab](How-to-use-Bass-tab)

Milestone: https://github.com/jcl2018/skillset/milestone/1

Review: **Unreviewed**

## Problem
- I learn bass lines from many places: tab videos on YouTube and Bilibili, tab sites like Songsterr, other sites I find, screenshots and PDFs.
- Each shows only part of the song at a time, and they don't share a layout.
- I want one compact printout that shows the whole song at a glance (sections, chords, lyrics, tempo and key) in the same format for every song, so I don't miss a part while I play along.

## Requirements

### Functional
- BAS-1: **Reviewed 2026-11-11** One format, Songsterr-style <!-- reviewed ce865339 -->
  - Every song is written to the same song file and printed in one layout modeled on Songsterr's tab: one line per string, labeled at left; bar numbers above bars; time signatures where they change; rhythm marks under notes.
  - The layout is adjusted for print: several bars per line, repeats collapsed.
  - The fixture song's compact tab matches its recorded baseline exactly.
- BAS-2: **Unreviewed** The whole song at a glance
  - A bold label where each section starts.
  - A repeated figure is drawn once with its count (x4).
  - A section that repeats an earlier one is one line ("Chorus 2 = Chorus").
  - Chord names sit over their bars, and each lyric under its own bar.
  - A lyric prints in its own band under the lowest string and any rhythm marks, never on a string line or a fret digit, the estimate mark or a repeat count; one wider than its bar widens the bar, then wraps to a second line, then shrinks to the template's lyric minimum, and never runs into the next bar.
  - A section starts on a new line and, when the song has a tempo, its label carries its start time.
  - A repeat count sits above the closing repeat sign, clear of chord names and bar numbers.
  - A missing bar is drawn full width and marked "missing"; two or more plain missing bars in a row print as one line with their range, cut at each section start.
  - An estimated bar carries a "≈" sign and is never folded into a repeat or a section reference; repeats and references also stop at a change of chord.
- BAS-6: **Unreviewed** Only what the sources show
  - Sources are whatever I provide: any URL (such as a video, Songsterr or another tab site, or a lyrics or chord page), screenshots, PDFs, notes.
  - Each bar, chord and lyric comes only from a source I provided and can be traced to it, never from memory or a web search I didn't ask for.
  - A source it can't open or read is never guessed around.
  - A person reading the source report checks this; no test can: the row only checks the report's format (BAS-8).
- BAS-7: **Unreviewed** Song header
  - Every chart starts with the same header: title, artist, BPM, key, time signature, tuning, instrument (such as 5-string bass), and every source used.
  - A header field with no value follows BAS-10 (the old second bullet of this requirement was merged into BAS-10).
- BAS-8: **Unreviewed** Source report
  - A transcription's report has a fixed format listing missing bars, bars that are estimates, which source gave each section, and any source it couldn't open or read.
  - The chart prints it after the last stave line; a song with no report, or a report that names no bar, list or source, prints none, and an explicit empty list prints "none".
- BAS-9: **Reviewed 2026-11-11** Four- and five-string bass <!-- reviewed 399a7de6 -->
  - The tab draws as many string lines as the song's bass has (4 or 5, such as a low B), labeled to match its tuning.
- BAS-10: **Unreviewed** One format template
  - One template file defines the printed layout: header fields and order; how a section starts and how repeats and repeated sections show; the Songsterr-style staff; where chords and lyrics sit, including the smallest size a long lyric shrinks to; spacing and fonts.
  - Every song renders through it, so changing it changes every song the same way.
  - A header field with no value is left out, never a blank or a guess; a missing title still reads "not shown".

### Non-functional
- BAS-3: **Unreviewed** Fits a printout
  - Two US-Letter pages at most, tab digits at 9 pt or more.
  - Repeats collapse and spacing tightens before the font shrinks.
  - A song that still can't fit is refused with a line naming it.
  - A song that fits one page gets larger digits (over 10 pt).
- BAS-4: **Reviewed 2026-11-11** Same input, same printout <!-- reviewed 91020a70 -->
  - Rendering the same song file twice gives byte-identical PDFs.
- BAS-5: **Reviewed 2026-11-11** No silent question marks <!-- reviewed 4ebe8a8d -->
  - A Chinese or other non-Latin title or lyric is never printed as question marks.
  - It renders correctly, or it's refused with a fix line.

## Non-goals
- It doesn't hear audio or transcribe by ear: it reads what the sources show.
- It doesn't choose between two bass parts: it asks.
- It doesn't print every repeated bar.

## Success metrics
- Every chart is at most two pages, with the header filled in.
- Every transcription that has a source report prints it.

## Revisions

### BAS-1

| rev | date | text | why | approved |
|---|---|---|---|---|
| r1 | 2026-11-11 | One format, Songsterr-style <br> Every song is written to the same song file and printed in one layout modeled on Songsterr's tab: one line per string, labeled at left; bar numbers above bars; time signatures where they change; rhythm marks under notes. <br> The layout is adjusted for print: several bars per line, repeats collapsed. <br> The fixture song's compact tab matches its recorded baseline exactly. | migration r1; date from its stamp | o2: "Yes" |

### BAS-2

| rev | date | text | why | approved |
|---|---|---|---|---|
| r1 | 2026-11-18 | The whole song at a glance <br> A bold label where each section starts. <br> A repeated figure is drawn once with its count (x4). <br> A section that repeats an earlier one is one line ("Chorus 2 = Chorus"). <br> Chord names sit over their bars, and each lyric under its own bar. <br> A lyric prints in its own band under the lowest string and any rhythm marks, never on a string line or a fret digit, the estimate mark or a repeat count; one wider than its bar widens the bar, then wraps to a second line, then shrinks to the template's lyric minimum, and never runs into the next bar. <br> A section starts on a new line and, when the song has a tempo, its label carries its start time. <br> A repeat count sits above the closing repeat sign, clear of chord names and bar numbers. <br> A missing bar is drawn full width and marked "missing"; two or more plain missing bars in a row print as one line with their range, cut at each section start. <br> An estimated bar carries a "≈" sign and is never folded into a repeat or a section reference; repeats and references also stop at a change of chord. | migration r1; date from the run day | o2: "Yes" |

### BAS-3

| rev | date | text | why | approved |
|---|---|---|---|---|
| r1 | 2026-11-18 | Fits a printout <br> Two US-Letter pages at most, tab digits at 9 pt or more. <br> Repeats collapse and spacing tightens before the font shrinks. <br> A song that still can't fit is refused with a line naming it. <br> A song that fits one page gets larger digits (over 10 pt). | migration r1; date from the run day | o2: "Yes" |

### BAS-4

| rev | date | text | why | approved |
|---|---|---|---|---|
| r1 | 2026-11-11 | Same input, same printout <br> Rendering the same song file twice gives byte-identical PDFs. | migration r1; date from its stamp | o2: "Yes" |

### BAS-5

| rev | date | text | why | approved |
|---|---|---|---|---|
| r1 | 2026-11-11 | No silent question marks <br> A Chinese or other non-Latin title or lyric is never printed as question marks. <br> It renders correctly, or it's refused with a fix line. | migration r1; date from its stamp | o2: "Yes" |

### BAS-6

| rev | date | text | why | approved |
|---|---|---|---|---|
| r1 | 2026-11-18 | Only what the sources show <br> Sources are whatever I provide: any URL (such as a video, Songsterr or another tab site, or a lyrics or chord page), screenshots, PDFs, notes. <br> Each bar, chord and lyric comes only from a source I provided and can be traced to it, never from memory or a web search I didn't ask for. <br> A source it can't open or read is never guessed around. <br> A person reading the source report checks this; no test can: the row only checks the report's format (BAS-8). | migration r1; date from the run day | o2: "Yes" |

### BAS-7

| rev | date | text | why | approved |
|---|---|---|---|---|
| r1 | 2026-11-18 | Song header <br> Every chart starts with the same header: title, artist, BPM, key, time signature, tuning, instrument (such as 5-string bass), and every source used. <br> A header field with no value follows BAS-10 (the old second bullet of this requirement was merged into BAS-10). | migration r1; date from the run day | o2: "Yes" |

### BAS-8

| rev | date | text | why | approved |
|---|---|---|---|---|
| r1 | 2026-11-18 | Source report <br> A transcription's report has a fixed format listing missing bars, bars that are estimates, which source gave each section, and any source it couldn't open or read. <br> The chart prints it after the last stave line; a song with no report, or a report that names no bar, list or source, prints none, and an explicit empty list prints "none". | migration r1; date from the run day | o2: "Yes" |

### BAS-9

| rev | date | text | why | approved |
|---|---|---|---|---|
| r1 | 2026-11-11 | Four- and five-string bass <br> The tab draws as many string lines as the song's bass has (4 or 5, such as a low B), labeled to match its tuning. | migration r1; date from its stamp | o2: "Yes" |

### BAS-10

| rev | date | text | why | approved |
|---|---|---|---|---|
| r1 | 2026-11-18 | One format template <br> One template file defines the printed layout: header fields and order; how a section starts and how repeats and repeated sections show; the Songsterr-style staff; where chords and lyrics sit, including the smallest size a long lyric shrinks to; spacing and fonts. <br> Every song renders through it, so changing it changes every song the same way. <br> A header field with no value is left out, never a blank or a guess; a missing title still reads "not shown". | migration r1; date from the run day | o2: "Yes" |

## Tests

| Test | Kind | Guards | Checks | Last result |
|---|---|---|---|---|
| [bas-tab-baseline](Tests#t-bas-tab-baseline) | requirement | BAS-1 | Given the fixture song, when its compact text tab is generated, then it matches the recorded baseline byte for byte. | PASS 2026-11-13 |
| [bas-chart-layout](Tests#t-bas-chart-layout) | requirement | BAS-2 | Given an invented song with sections, repeats and lyrics, when its chart is rendered, then each section has a bold label, the repeated bars print once with a count, and each lyric sits under its own bar. | PASS 2026-11-13 |
| [bas-sources-only](Tests#t-bas-sources-only) | requirement | BAS-6 | Given sources for a song, when the agent writes the song file, then each bar, chord and lyric comes only from a cited source, which a person reading the source report checks; the nightly run checks the report's format (BAS-8). | not run |
| - | requirement | BAS-6 | no passing test | not enforced |
| [bas-header](Tests#t-bas-header) | requirement | BAS-7 | Given a song whose source shows only a title, when its chart is rendered, then the title prints, header fields with no value are left out, and a full song's fields print in template order. | PASS 2026-11-13 |
| [bas-source-report](Tests#t-bas-source-report) | requirement | BAS-8 | Given a song with a source report, when its chart is rendered, then missing bars, estimates and the source per section print after the last stave line, a missing part reads "not shown", and a bad report key is refused. | PASS 2026-11-13 |
| [bas-five-string](Tests#t-bas-five-string) | requirement | BAS-9 | Given a 5-string and a 4-string song, when each chart is rendered, then the first draws five stave lines labeled G D A E B and the second four labeled G D A E, and the text tab refuses the 5-string song. | PASS 2026-11-13 |
| [bas-template](Tests#t-bas-template) | requirement | BAS-10 | Given a changed copy of the format template, when two songs are rendered through it, then the header order, missing text, repeat format, section size and line gap all follow it, and a bad template is refused by name. | PASS 2026-11-13 |
| [bas-chart-fit](Tests#t-bas-chart-fit) | requirement | BAS-3 | Given a normal song and a 400-bar song, when each chart is rendered, then the first fits two pages with tab digits at 9 pt or more and the second is refused with a line naming it. | PASS 2026-11-13 |
| [bas-pdf-same](Tests#t-bas-pdf-same) | requirement | BAS-4 | Given one song file, when the tab PDF and the chart PDF are each rendered twice, then both copies are identical byte for byte. | PASS 2026-11-13 |
| [bas-nonlatin](Tests#t-bas-nonlatin) | requirement | BAS-5 | Given a tab with a Chinese title and no Pillow installed, when its PDF is rendered, then it is refused unless lossy output is asked for, and written when it is. | PASS 2026-11-13 |
| [bas-nonlatin-chart](Tests#t-bas-nonlatin-chart) | requirement | BAS-5 | Given a chart song with a Chinese lyric and no Pillow installed, when its PDF is rendered, then it is refused unless lossy output is asked for, and written when it is. | PASS 2026-11-13 |
