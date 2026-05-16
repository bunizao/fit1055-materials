from __future__ import annotations

import json
import re
from email.message import Message
from pathlib import Path
from urllib.parse import unquote, urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from moodle_cli.auth import get_session
from moodle_cli.config import load_config


ROOT = Path(__file__).resolve().parent
COURSE_JSON = ROOT / "fit1055_course.json"
OUT = ROOT / "fit1055_revision_materials"
WEEKS = {"Week 2", "Week 3", "Week 4", "Week 5", "Week 6", "Week 7", "Week 8", "Week 9", "Week 10", "Week 12"}
INCLUDE_MODS = {"resource", "folder", "page", "quiz", "url", "label"}
SKIP_NAME_RE = re.compile(
    r"(?i)(upload|SETU|student evaluation|group registration|studiosity|assignment 1|assignment 2|assignment 3)"
)


def slug(value: str, max_len: int = 90) -> str:
    value = re.sub(r"[^\w.\-()]+", "_", value.strip(), flags=re.ASCII).strip("._")
    return (value or "item")[:max_len]


def filename_from_response(response: requests.Response, fallback: str) -> str:
    content_disposition = response.headers.get("content-disposition", "")
    msg = Message()
    msg["content-disposition"] = content_disposition
    filename = msg.get_filename()
    if not filename:
        parsed = urlparse(response.url)
        filename = Path(unquote(parsed.path)).name
    if not filename:
        filename = fallback
    return slug(filename, max_len=140)


def write_bytes(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_bytes() == content:
        return
    path.write_bytes(content)


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_text(encoding="utf-8") == content:
        return
    path.write_text(content, encoding="utf-8")


def download_response(response: requests.Response, dest_dir: Path, fallback: str) -> dict:
    filename = filename_from_response(response, fallback)
    path = dest_dir / filename
    write_bytes(path, response.content)
    return {
        "path": str(path.relative_to(ROOT)),
        "content_type": response.headers.get("content-type", ""),
        "bytes": len(response.content),
    }


def extract_links(html: str, base_url: str) -> list[tuple[str, str]]:
    soup = BeautifulSoup(html, "html.parser")
    links: list[tuple[str, str]] = []
    selectors = [
        ".foldertree a[href]",
        ".fp-filename-icon a[href]",
        ".resourceworkaround a[href]",
        ".resourcecontent a[href]",
        "a.resourceworkaround[href]",
    ]
    seen: set[str] = set()
    for selector in selectors:
        for link in soup.select(selector):
            href = link.get("href")
            if not href:
                continue
            absolute = urljoin(base_url, href)
            if absolute in seen:
                continue
            seen.add(absolute)
            label = " ".join(link.get_text(" ", strip=True).split())
            links.append((label, absolute))
    return links


def request_moodle(session: requests.Session, base_url: str, url: str) -> requests.Response:
    absolute = url if url.startswith("http") else urljoin(base_url, url)
    response = session.get(absolute, allow_redirects=True, timeout=60)
    response.raise_for_status()
    return response


def retrieve() -> list[dict]:
    config = load_config()
    base_url = config["base_url"].rstrip("/")
    session = requests.Session()
    session.cookies.set("MoodleSession", get_session(base_url))

    course = json.loads(COURSE_JSON.read_text(encoding="utf-8"))
    manifest: list[dict] = []
    for section in course:
        week = section.get("name")
        if week not in WEEKS:
            continue
        week_dir = OUT / slug(week)
        for activity in section.get("activities") or []:
            mod = activity.get("modname")
            name = activity.get("name") or f"activity_{activity.get('id')}"
            url = activity.get("url") or ""
            if mod not in INCLUDE_MODS:
                continue
            if mod in {"url", "label"} and SKIP_NAME_RE.search(name):
                continue

            record = {
                "week": week,
                "id": activity.get("id"),
                "modname": mod,
                "name": name,
                "source_url": url,
                "downloads": [],
                "notes": [],
            }
            item_dir = week_dir / f"{activity.get('id')}_{slug(name)}"

            if mod == "resource" and url:
                response = request_moodle(session, base_url, url)
                content_type = response.headers.get("content-type", "")
                if "text/html" in content_type:
                    links = extract_links(response.text, base_url)
                    write_text(item_dir / "page.html", response.text)
                    record["downloads"].append({"path": str((item_dir / "page.html").relative_to(ROOT)), "content_type": content_type, "bytes": len(response.content)})
                    for index, (label, href) in enumerate(links, start=1):
                        file_response = request_moodle(session, base_url, href)
                        record["downloads"].append(download_response(file_response, item_dir, f"{index}_{label or activity['id']}"))
                else:
                    record["downloads"].append(download_response(response, item_dir, f"{activity['id']}_{name}"))

            elif mod == "folder" and url:
                response = request_moodle(session, base_url, url)
                write_text(item_dir / "folder.html", response.text)
                record["downloads"].append({"path": str((item_dir / "folder.html").relative_to(ROOT)), "content_type": response.headers.get("content-type", ""), "bytes": len(response.content)})
                for index, (label, href) in enumerate(extract_links(response.text, base_url), start=1):
                    file_response = request_moodle(session, base_url, href)
                    record["downloads"].append(download_response(file_response, item_dir, f"{index}_{label or activity['id']}"))

            elif mod == "page" and url:
                response = request_moodle(session, base_url, url)
                soup = BeautifulSoup(response.text, "html.parser")
                main = soup.select_one("#region-main") or soup.body or soup
                text = main.get_text("\n", strip=True)
                write_text(item_dir / "page.txt", text + "\n")
                write_text(item_dir / "page.html", response.text)
                record["downloads"].append({"path": str((item_dir / "page.txt").relative_to(ROOT)), "content_type": "text/plain", "bytes": len(text.encode("utf-8"))})
                record["downloads"].append({"path": str((item_dir / "page.html").relative_to(ROOT)), "content_type": response.headers.get("content-type", ""), "bytes": len(response.content)})

            elif mod in {"url", "quiz"} and url:
                response = request_moodle(session, base_url, url)
                soup = BeautifulSoup(response.text, "html.parser")
                main = soup.select_one("#region-main") or soup.body or soup
                text = main.get_text("\n", strip=True)
                html_name = "quiz.html" if mod == "quiz" else "url.html"
                text_name = "quiz.txt" if mod == "quiz" else "url.txt"
                write_text(item_dir / html_name, response.text)
                write_text(item_dir / text_name, text + "\n")
                record["downloads"].append({"path": str((item_dir / text_name).relative_to(ROOT)), "content_type": "text/plain", "bytes": len(text.encode("utf-8"))})
                record["downloads"].append({"path": str((item_dir / html_name).relative_to(ROOT)), "content_type": response.headers.get("content-type", ""), "bytes": len(response.content)})
                targets = []
                for label, href in extract_links(response.text, base_url):
                    if href != url:
                        targets.append({"label": label, "url": href})
                if targets:
                    record["notes"].append({"target_urls": targets})

            elif url:
                record["notes"].append({"external_or_activity_url": url})

            manifest.append(record)

    OUT.mkdir(parents=True, exist_ok=True)
    write_text(OUT / "manifest.json", json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    return manifest


if __name__ == "__main__":
    retrieved = retrieve()
    file_count = sum(len(item["downloads"]) for item in retrieved)
    print(f"retrieved_items={len(retrieved)}")
    print(f"downloaded_files={file_count}")
    print(f"output={OUT}")
