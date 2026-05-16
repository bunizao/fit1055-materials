# FIT1055 Quiz Revision Materials

Private working archive for FIT1055 IT Professional Practice and Ethics, S1 2026.

This repository collects the Week 11 quiz revision materials retrieved from Moodle and EdStem on 2026-05-16.

## Start Here

- `agent-readable/`: Markdown and JSON extracts generated for agent consumption.
- `materials/exam-info/edstem-quiz-threads/`: EdStem quiz posts and staff replies about scope, venue, timing, trial quiz, Safe Exam Browser, and question format.
- `materials/week-10-trial-quiz-and-revision/exam-prep/FIT1055 IT Professional Practice and Ethics Revision Notes S2 2025.pdf`: the key revision-notes PDF. Start here for a compact pass before drilling into weekly workshop slides.
- `materials/week-10-trial-quiz-and-revision/`: trial quiz page, revision notes, Week 10 workshop slides, and worksheet.
- `materials/week-02-communication/` through `materials/week-09-prototyping/`: main examinable weekly materials.
- `materials/week-12-gibbs-reflective-cycle/`: Week 12 Gibbs reflective cycle materials.
- `metadata/external-links.md`: external links that were not mirrored locally.
- `metadata/manifest.json`: full Moodle retrieval index.

## Agent-readable Slides

Slide decks have been extracted into `agent-readable/slides/` as Markdown and JSON. Each extracted deck preserves source path, slide order, slide titles, text blocks, and speaker notes where present.

The extraction script is `tools/extract_slides.py`. It handles `.pptx` directly via ZIP/XML parsing. The single legacy `.ppt` deck is recorded as metadata only because reliable slide-level extraction requires converting it to `.pptx` first.

## Confirmed Quiz Scope

Staff confirmed the quiz scope on EdStem as:

- Week 2-9
- Week 12
- Communication
- Research
- Meetings
- Teamwork and leadership
- Professional conduct
- ERF, all steps
- Gibbs reflective cycle

Week 10 is included because it contains the trial quiz and revision notes. The actual quiz is expected to be harder than the trial quiz, and the staff recommendation was to prioritise weekly workshop slides over relying only on revision notes.

The revision-notes PDF at `materials/week-10-trial-quiz-and-revision/exam-prep/FIT1055 IT Professional Practice and Ethics Revision Notes S2 2025.pdf` is the most compact exam-prep artifact in this archive. Treat it as the fast overview, then use the weekly workshop slides for depth.

## Directory Layout

Each week is organised by material type:

- `slides/`: workshop or seminar decks.
- `worksheets/`: applied session worksheets and related documents.
- `readings/`: PDFs, cases, articles, and reference readings.
- `handouts/`: short course handouts.
- `exam-prep/`: explicit quiz or revision material.
- `source-pages/`: saved Moodle wrapper pages for links, pages, quizzes, or folders.

## Tools Used

This archive was retrieved with:

- [`moodle-cli`](https://github.com/bunizao/moodle-cli), used for Moodle course, activity, resource, folder, page, quiz, and authenticated file retrieval.
- [`edstem-cli`](https://github.com/bunizao/edstem-cli), used for EdStem course discovery and quiz-thread exports.

Both tools made the archive reproducible without manually clicking through Moodle and EdStem. Nice little bit of terminal plumbing, honestly.

## Access And Copyright

Course materials from FIT1055, Moodle, and Monash learning systems remain copyright Monash University and/or the original named authors where applicable.
