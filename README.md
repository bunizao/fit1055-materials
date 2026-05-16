# FIT1055 Quiz Revision Materials

Archive for FIT1055 IT Professional Practice and Ethics, S1 2026.

Collected from Moodle and EdStem on 2026-05-16 for the Week 11 quiz.

## Start Here

- [Revision Notes PDF](<materials/week-10-trial-quiz-and-revision/exam-prep/FIT1055 IT Professional Practice and Ethics Revision Notes S2 2025.pdf>) is the compact exam-prep artifact. Start there, then use the weekly workshop slides for depth.
- [EdStem Quiz Threads](materials/exam-info/edstem-quiz-threads/) contains staff posts and replies about scope, marking, venue, timing, trial quiz, Safe Exam Browser, and question format.
- [Agent-readable slide extracts](agent-readable/slides/index.md) provides Markdown and JSON versions of the slide decks.
- [External Links](metadata/external-links.md) lists Moodle URL activities that point to external systems such as YouTube, Panopto, Wayground, or Google Drive.

## Confirmed Quiz Scope

Staff confirmed the quiz covers:

- Week 2-9
- Week 12
- Communication
- Research
- Meetings
- Teamwork and leadership
- Professional conduct
- ERF, all steps
- Gibbs reflective cycle

Week 10 is included in this archive because it contains the trial quiz, revision notes, workshop slides, and worksheet. The actual quiz is expected to be harder than the trial quiz, and staff recommended prioritising weekly workshop slides over relying only on revision notes.

## Key Exam Info

- [Marks clarification and scope](materials/exam-info/edstem-quiz-threads/497_marks_clarification_and_scope.json): marking rules, topics, 20-question count, 60-minute duration, attendance timing, and Week 12 Gibbs reference.
- [Quiz preparation advice](materials/exam-info/edstem-quiz-threads/513_quiz_preparation.json): staff recommendation to study weekly workshop slides.
- [EOS quiz format](materials/exam-info/edstem-quiz-threads/504_eos_quiz_format.json): actual quiz uses a similar MCQ style to the trial quiz, but with harder situation-based questions.
- [Test venue](materials/exam-info/edstem-quiz-threads/506_test_venue.json): venue and workshop allocation confirmation.
- [Safe Exam Browser note](materials/exam-info/edstem-quiz-threads/475_trial_quiz_and_seb.json): trial quiz and Safe Exam Browser context.

## Weekly Materials

| Week | Topic | Materials |
| --- | --- | --- |
| Week 2 | Communication | [folder](materials/week-02-communication/) |
| Week 3 | Research | [folder](materials/week-03-research/) |
| Week 4 | Meetings | [folder](materials/week-04-meetings/) |
| Week 5 | Teamwork and leadership | [folder](materials/week-05-teamwork-leadership/) |
| Week 6 | Professional conduct and ethics | [folder](materials/week-06-professional-conduct-ethics/) |
| Week 7 | ERF and ethical reasoning | [folder](materials/week-07-erf-and-ethical-reasoning/) |
| Week 8 | Ideation and deontology | [folder](materials/week-08-ideation-and-deontology/) |
| Week 9 | Prototyping | [folder](materials/week-09-prototyping/) |
| Week 10 | Trial quiz and revision | [folder](materials/week-10-trial-quiz-and-revision/) |
| Week 12 | Gibbs reflective cycle | [folder](materials/week-12-gibbs-reflective-cycle/) |

Each week is organised by material type:

- `slides/`: workshop or seminar decks.
- `worksheets/`: applied session worksheets and related documents.
- `readings/`: PDFs, cases, articles, and reference readings.
- `handouts/`: short course handouts.
- `exam-prep/`: explicit quiz or revision material.
- `source-pages/`: saved text-only Moodle wrapper pages for links, pages, quizzes, or folders.

## Agent-readable Extracts

Slide decks have been extracted into [agent-readable/slides](agent-readable/slides/) as Markdown and JSON. Each extracted deck preserves source path, slide order, slide titles, text blocks, and speaker notes where present.

The extraction script is [tools/extract_slides.py](tools/extract_slides.py). It handles `.pptx` directly via ZIP/XML parsing. The single legacy `.ppt` deck is recorded as metadata only because reliable slide-level extraction requires converting it to `.pptx` first.

## Metadata

- [Moodle retrieval manifest](metadata/manifest.json)
- [Course JSON snapshot](metadata/fit1055_course.json)
- [Local inventory](metadata/local-inventory.txt)
- [External links](metadata/external-links.md)

## Tools Used

This archive was retrieved with:

- [moodle-cli](https://github.com/bunizao/moodle-cli), used for Moodle course, activity, resource, folder, page, quiz, and authenticated file retrieval.
- [edstem-cli](https://github.com/bunizao/edstem-cli), used for EdStem course discovery and quiz-thread exports.

Both tools made the archive reproducible without manually clicking through Moodle and EdStem.

## Copyright

Course materials from FIT1055, Moodle, and Monash learning systems remain copyright Monash University and/or the original named authors where applicable.
