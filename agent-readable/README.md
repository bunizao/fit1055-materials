# Agent-readable extracts

This folder contains text-first extracts generated from binary course materials.

## Slides

- `slides/index.md`: human-readable index of extracted decks.
- `slides/index.json`: machine-readable index with source paths and slide counts.
- `slides/<week>/*.md`: slide-by-slide Markdown.
- `slides/<week>/*.json`: structured slide text for agents.

The extractor is `tools/extract_slides.py`. It uses only Python standard-library ZIP/XML parsing for `.pptx` files, so it is reproducible without LibreOffice or PowerPoint.

One legacy `.ppt` file is included as metadata only. That format is an old binary Office container; convert it to `.pptx` with LibreOffice or PowerPoint if slide-level extraction is needed.
