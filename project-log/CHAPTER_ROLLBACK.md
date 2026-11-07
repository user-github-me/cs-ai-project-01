# Chapter source rollback — 7 November 2026

Nazif requested a rewind of the chapter files, then explicitly selected **all chapter/content files only**. This rollback restores `content/` and keeps the existing study guide, Test Bank, slides, videos, narration scripts, game and published packages. Those retained exports describe the earlier expanded edition and can differ from the restored chapter source.

## What Neogpt had changed

Commits `f567ff9` and `d9ae5f8` changed 59 paths under `content/`: **42 existing files rewritten and 17 new files added**.

The existing files were seven files in each chapter: `draft.md`, `Learning_Outcomes*.md`, `Key_Terms_*.md`, `exercises.md`, `solutions.md`, `README.md`, and `UseOfAI.md`.

- Replaced the six draft placeholders with developed explanations, examples, tables, references and 67 application checkpoints.
- Rewrote the team's existing learning outcomes and glossaries. These sections already contained substantive work. For example, Chapter 1 outcomes went from 27 lines to a seven-line summary; Chapter 3 key terms went from 70 lines to a 23-line table. Chapter 1's consolidated glossary omitted separately listed terms including overclocking, BIOS, flags and bus direction. The original wording was not preserved by that expansion.
- Reformatted and renumbered existing exercises and changed some wording. Chapter 4's circuit-switching question became a conditional reserved-capacity scenario; its reversed-asymmetric-key question became a distinction between signing and encryption. Chapter 2's exploitation wording changed to using the best current estimates.
- Added 65 explained answers to the solution placeholders, changed chapter navigation and appended Stage 2 AI-assistance notes.
- Added chapter activities, compiled content, a Markdown Test Bank, shared reference/index files and supporting demonstrations; later added the ROVERLAB activity.

This was a source rewrite as part of the Stage 2 expansion, not simply adding PDFs or filling every file from an empty starting point. The team already had learning outcomes, glossaries, exercises and AI-use disclosures. Nazif requested their restoration.

## Versions restored and teammate work preserved

The baseline is [`8ab3108`](https://github.com/user-github-me/cs-ai-project-01/commit/8ab3108), immediately before the Stage 2 rewrite. Safa Nadeem submitted further chapter restorations during this work. The rollback was rebased on the latest fetched revision, `fca207e`, and preserves every content file changed by Safa since the earlier published revision `32b112f`.

Preserved verbatim from `fca207e`:

- `content/chapter-01/Key_Terms_1.md`
- `content/chapter-01/Learning_Outcomes1.md`
- `content/chapter-01/UseOfAI.md`
- `content/chapter-01/exercises.md`
- `content/chapter-02/Key_Terms_2.md`
- `content/chapter-02/Learning_Outcomes2.md`
- `content/chapter-02/exercises.md`
- `content/chapter-03/Key_Terms_3.md`
- `content/chapter-03/Learning_Outcomes3.md`
- `content/chapter-04/Key_Terms_4.md`
- `content/chapter-04/Learning_Outcomes4.md`
- `content/chapter-05/Key_Terms_5.md`
- `content/chapter-05/Learning_Outcomes5.md`
- `content/chapter-06/Key_Terms_6.md`
- `content/chapter-06/Learning_Outcomes6.md`

The final `content/` directory has **43 files**: **28 byte-identical to `8ab3108`** and **15 byte-identical to Safa's newer versions**. All 17 additions from the Stage 2 expansion are removed. The untouched Chapter 1 sample remains. No teammate commit was removed or rewritten.

Against `fca207e`, this rollback changes 27 existing files and removes 17 additions. Original draft and solution placeholders return wherever they existed in the baseline. Safa's newer headings, list formatting and wording are preserved exactly.

## Added files removed from content/

- Six chapter `activities.md` files.
- `BlueImpulse_Complete_Content_V2.md` and `BlueImpulse_Stage2_TestBank_V1.md`.
- `README.md`, `REVIEW.md`, `references.md` and `topic-map.json`.
- `supporting/BlueImpulse_Demonstrations.py`, `supporting/README.md`, `supporting/ROVERLAB_Activity.md`, `supporting/expected-results.json` and `supporting/modified-results.json`.

The existing generated submission snapshot remains outside `content/`, as part of the retained outputs. Active documentation links now use the already retained tutorial support files. Historical review links use the earlier commit where appropriate. No new copy of the rewritten chapters was introduced into `content/`.

## Verification and scope

Every remaining file was compared byte-for-byte against its selected Git version, and the file inventory was checked against the original 43-file tree. Active documentation links were checked after the restoration. The generated PDF/PPTX/DOCX/MP4 outputs, game runtime files and recording-script files were not altered by this rollback.

The root README, task list and Nazif's Markdown personal log record the restored source state. Previously released log documents and packages remain dated snapshots. The retained `build_stage2.py` script can recreate the expanded content; its README now explicitly states that it rewrites `content/`.
