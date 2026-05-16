from __future__ import annotations

import json
import re
import subprocess
import zipfile
from dataclasses import dataclass
from pathlib import Path
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
SLIDES_ROOT = ROOT / "materials"
OUT_ROOT = ROOT / "agent-readable" / "slides"

NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "rel": "http://schemas.openxmlformats.org/package/2006/relationships",
}


@dataclass
class SlideText:
    number: int
    title: str
    text: list[str]
    notes: list[str]


def slug(value: str, max_len: int = 96) -> str:
    value = re.sub(r"[^\w.-]+", "-", value.lower(), flags=re.ASCII).strip("-")
    value = re.sub(r"-+", "-", value)
    return (value or "deck")[:max_len]


def clean_lines(lines: list[str]) -> list[str]:
    cleaned: list[str] = []
    previous = ""
    for line in lines:
        line = " ".join(line.split())
        if not line or line == previous:
            continue
        cleaned.append(line)
        previous = line
    return cleaned


def text_from_xml(xml: bytes) -> list[str]:
    root = ET.fromstring(xml)
    lines: list[str] = []
    for paragraph in root.findall(".//a:p", NS):
        parts = [node.text or "" for node in paragraph.findall(".//a:t", NS)]
        line = "".join(parts).strip()
        if line:
            lines.append(line)
    return clean_lines(lines)


def slide_paths(zip_file: zipfile.ZipFile) -> list[str]:
    names = zip_file.namelist()
    if "ppt/presentation.xml" not in names or "ppt/_rels/presentation.xml.rels" not in names:
        return sorted(
            [name for name in names if re.fullmatch(r"ppt/slides/slide\d+\.xml", name)],
            key=lambda name: int(re.search(r"slide(\d+)\.xml", name).group(1)),
        )

    presentation = ET.fromstring(zip_file.read("ppt/presentation.xml"))
    rels = ET.fromstring(zip_file.read("ppt/_rels/presentation.xml.rels"))
    targets = {
        rel.attrib["Id"]: rel.attrib["Target"]
        for rel in rels.findall("rel:Relationship", NS)
        if rel.attrib.get("Type", "").endswith("/slide")
    }
    ordered: list[str] = []
    for slide_id in presentation.findall(".//p:sldIdLst/p:sldId", NS):
        rel_id = slide_id.attrib.get(f"{{{NS['r']}}}id")
        target = targets.get(rel_id or "")
        if target:
            ordered.append("ppt/" + target.lstrip("/"))
    return ordered


def notes_for_slide(zip_file: zipfile.ZipFile, slide_path: str) -> list[str]:
    rel_path = slide_path.replace("ppt/slides/", "ppt/slides/_rels/") + ".rels"
    if rel_path not in zip_file.namelist():
        return []
    rels = ET.fromstring(zip_file.read(rel_path))
    for rel in rels.findall("rel:Relationship", NS):
        if rel.attrib.get("Type", "").endswith("/notesSlide"):
            target = rel.attrib.get("Target", "")
            note_path = str((Path(slide_path).parent / target).as_posix())
            note_path = re.sub(r"ppt/slides/\.\./", "ppt/", note_path)
            if note_path in zip_file.namelist():
                return text_from_xml(zip_file.read(note_path))
    return []


def extract_pptx(path: Path) -> list[SlideText]:
    slides: list[SlideText] = []
    with zipfile.ZipFile(path) as zip_file:
        for index, slide_path in enumerate(slide_paths(zip_file), start=1):
            lines = text_from_xml(zip_file.read(slide_path))
            notes = notes_for_slide(zip_file, slide_path)
            title = lines[0] if lines else f"Slide {index}"
            slides.append(SlideText(index, title, lines, notes))
    return slides


def extract_legacy_ppt(path: Path) -> tuple[list[str], str]:
    try:
        result = subprocess.run(
            ["/usr/bin/mdls", "-name", "kMDItemTitle", "-name", "kMDItemAuthors", str(path)],
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError as exc:
        return [], f"Legacy .ppt extraction unavailable: {exc}"
    metadata = clean_lines(result.stdout.splitlines())
    return metadata, "Legacy .ppt binary format. Install LibreOffice and convert to .pptx for slide-level extraction."


def deck_output_path(deck: Path) -> Path:
    week = deck.relative_to(SLIDES_ROOT).parts[0]
    return OUT_ROOT / week / f"{slug(deck.stem)}.md"


def write_deck_markdown(deck: Path, slides: list[SlideText], warning: str | None = None) -> Path:
    out = deck_output_path(deck)
    out.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        f"# {deck.stem}",
        "",
        f"- Source: `{deck.relative_to(ROOT)}`",
        f"- Format: `{deck.suffix.lower().lstrip('.')}`",
    ]
    if warning:
        lines.extend(["", f"> {warning}"])
    lines.append("")

    for slide in slides:
        lines.extend([f"## Slide {slide.number}: {slide.title}", ""])
        if slide.text:
            lines.extend(f"- {line}" for line in slide.text)
        else:
            lines.append("- [No extractable text]")
        if slide.notes:
            lines.extend(["", "Speaker notes:"])
            lines.extend(f"- {line}" for line in slide.notes)
        lines.append("")

    out.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return out


def write_deck_json(deck: Path, slides: list[SlideText], warning: str | None = None) -> Path:
    out = deck_output_path(deck).with_suffix(".json")
    payload = {
        "source": str(deck.relative_to(ROOT)),
        "format": deck.suffix.lower().lstrip("."),
        "warning": warning,
        "slides": [
            {"number": slide.number, "title": slide.title, "text": slide.text, "notes": slide.notes}
            for slide in slides
        ],
    }
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return out


def main() -> None:
    if OUT_ROOT.exists():
        for old in OUT_ROOT.rglob("*"):
            if old.is_file():
                old.unlink()
    decks = sorted(SLIDES_ROOT.glob("week-*/slides/*.[pP][pP][tT]*"))
    index: list[dict] = []
    for deck in decks:
        warning = None
        if deck.suffix.lower() == ".pptx":
            slides = extract_pptx(deck)
        else:
            metadata, warning = extract_legacy_ppt(deck)
            slides = [SlideText(1, deck.stem, metadata, [])]
        md_path = write_deck_markdown(deck, slides, warning)
        json_path = write_deck_json(deck, slides, warning)
        index.append(
            {
                "source": str(deck.relative_to(ROOT)),
                "markdown": str(md_path.relative_to(ROOT)),
                "json": str(json_path.relative_to(ROOT)),
                "slide_count": len(slides),
                "warning": warning,
            }
        )

    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    (OUT_ROOT / "index.json").write_text(json.dumps(index, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = ["# Agent-readable slide extracts", ""]
    for item in index:
        warning = " (legacy warning)" if item.get("warning") else ""
        markdown_path = Path(item["markdown"]).relative_to(OUT_ROOT.relative_to(ROOT))
        lines.append(f"- [{markdown_path.stem}]({markdown_path}): {item['slide_count']} slides{warning}")
    (OUT_ROOT / "index.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"decks={len(index)}")
    print(f"output={OUT_ROOT}")


if __name__ == "__main__":
    main()
