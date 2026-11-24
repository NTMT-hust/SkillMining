"""Turn the archived ITviec and TopDev HTML pages into reviewable CSV files.

Uses only the Python standard library. Run from any working directory:

    python src/data_preprocessing/extract_meaningfull.py

By default this reads ``data/raw/{itviec,topdev}`` and writes:
    data/processed/postings.csv
    data/processed/extraction_audit.csv

The extractor deliberately keeps source identifiers and raw page text so that
every extracted record can be checked against its HTML. It does not infer
missing values or extract normalized skills; those should be separate steps.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Iterable


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_RAW_ROOTS = [PROJECT_ROOT / "data" / "raw"]
# Some downloaded datasets are split into folders such as
# data/raw-<archive-id>-001/raw and ...-002/raw. Use all parts by default.
if not DEFAULT_RAW_ROOTS[0].exists():
    DEFAULT_RAW_ROOTS = sorted(PROJECT_ROOT.glob("data/raw-*/raw"))
OUTPUT_ROOT = PROJECT_ROOT / "data" / "processed"

VOID_TAGS = {
    "area", "base", "br", "col", "embed", "hr", "img", "input", "link",
    "meta", "param", "source", "track", "wbr",
}
IGNORED_TAGS = {"script", "style", "noscript", "svg", "iframe", "nav", "footer"}
JOB_CONTAINER_HINTS = (
    "job", "detail", "description", "content", "requirement", "benefit",
    "responsibilit", "vacancy", "position",
)
WHITESPACE_RE = re.compile(r"\s+")


@dataclass
class Node:
    tag: str
    attrs: dict[str, str] = field(default_factory=dict)
    children: list[Node | str] = field(default_factory=list)


class PageParser(HTMLParser):
    """Small tolerant HTML tree builder that avoids an external dependency."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.root = Node("document")
        self.stack = [self.root]
        self.meta: dict[str, str] = {}
        self.scripts: list[tuple[dict[str, str], str]] = []
        self._script_attrs: dict[str, str] | None = None
        self._script_chunks: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_map = {k.lower(): (v or "") for k, v in attrs}
        if tag.lower() == "meta":
            key = (attr_map.get("property") or attr_map.get("name") or "").lower()
            if key and attr_map.get("content"):
                self.meta.setdefault(key, attr_map["content"].strip())
        node = Node(tag.lower(), attr_map)
        self.stack[-1].children.append(node)
        if tag.lower() == "script":
            self._script_attrs = attr_map
            self._script_chunks = []
        if tag.lower() not in VOID_TAGS:
            self.stack.append(node)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)
        if tag.lower() not in VOID_TAGS:
            self.handle_endtag(tag)

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag == "script" and self._script_attrs is not None:
            self.scripts.append((self._script_attrs, "".join(self._script_chunks)))
            self._script_attrs = None
            self._script_chunks = []
        # HTML pages often omit closing tags. Pop to the nearest matching node.
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                del self.stack[i:]
                break

    def handle_data(self, data: str) -> None:
        if self._script_attrs is not None:
            self._script_chunks.append(data)
        else:
            self.stack[-1].children.append(data)


def node_text(node: Node, *, skip_ignored: bool = True) -> str:
    if skip_ignored and node.tag in IGNORED_TAGS:
        return ""
    parts: list[str] = []
    for child in node.children:
        if isinstance(child, str):
            parts.append(child)
        else:
            parts.append(node_text(child, skip_ignored=skip_ignored))
    return clean_text(" ".join(parts))


def clean_text(value: str) -> str:
    value = value.replace("\u00a0", " ").replace("\u200b", "")
    return WHITESPACE_RE.sub(" ", value).strip()


def walk(node: Node) -> Iterable[Node]:
    yield node
    for child in node.children:
        if isinstance(child, Node):
            yield from walk(child)


def container_score(node: Node, text: str) -> int:
    if node.tag in IGNORED_TAGS:
        return -1
    if len(text) < 160:
        return -1
    hints = " ".join((node.attrs.get("class", ""), node.attrs.get("id", ""))).lower()
    score = min(len(text), 6000) // 20
    score += 250 * sum(1 for hint in JOB_CONTAINER_HINTS if hint in hints)
    if node.tag in {"main", "article"}:
        score += 500
    # Penalize a document-wide container so header/footer material is less likely
    # to win over a narrower job detail block.
    if node.tag in {"html", "body"}:
        score -= 700
    return score


def best_job_text(root: Node) -> str:
    candidates = [n for n in walk(root) if n.tag in {"main", "article", "section", "div"}]
    if not candidates:
        return node_text(root)
    # Build visible text for each node once. Recomputing descendant text for
    # every nested div made large pages needlessly quadratic to process.
    text_by_node: dict[int, str] = {}

    def collect(node: Node) -> str:
        if node.tag in IGNORED_TAGS:
            text_by_node[id(node)] = ""
            return ""
        parts: list[str] = []
        for child in node.children:
            parts.append(clean_text(child) if isinstance(child, str) else collect(child))
        value = clean_text(" ".join(part for part in parts if part))
        text_by_node[id(node)] = value
        return value

    collect(root)
    winner = max(candidates, key=lambda n: container_score(n, text_by_node.get(id(n), "")))
    text = text_by_node.get(id(winner), "")
    # On some static pages a generic main element wins but contains only a
    # short shell. Fall back to all visible body text in that case.
    return text if len(text) >= 250 else node_text(root)


def find_jobposting(value: Any) -> dict[str, Any] | None:
    """Find a Schema.org JobPosting object inside JSON-LD structures."""
    if isinstance(value, list):
        for item in value:
            found = find_jobposting(item)
            if found:
                return found
    elif isinstance(value, dict):
        kind = value.get("@type", "")
        kinds = kind if isinstance(kind, list) else [kind]
        if any(str(k).lower() == "jobposting" for k in kinds):
            return value
        for child in value.values():
            found = find_jobposting(child)
            if found:
                return found
    return None


def jsonld_job(parser: PageParser) -> dict[str, Any]:
    for attrs, body in parser.scripts:
        if "ld+json" not in attrs.get("type", "").lower():
            continue
        try:
            job = find_jobposting(json.loads(body.strip()))
        except (json.JSONDecodeError, TypeError):
            continue
        if job:
            return job
    return {}


def text_value(value: Any) -> str:
    if isinstance(value, str):
        return clean_text(value)
    if isinstance(value, list):
        return "; ".join(filter(None, (text_value(v) for v in value)))
    if isinstance(value, dict):
        # Schema.org address, organization, and salary values.
        for key in ("name", "streetAddress", "addressLocality", "addressRegion", "value"):
            if key in value:
                result = text_value(value[key])
                if result:
                    return result
        return "; ".join(filter(None, (text_value(v) for v in value.values())))
    return ""


def parse_page(path: Path) -> dict[str, str]:
    # utf-8-sig also handles a BOM; replacement keeps one malformed byte from
    # aborting the whole batch. Original HTML is never modified.
    html = path.read_text(encoding="utf-8-sig", errors="replace")
    parser = PageParser()
    try:
        parser.feed(html)
        parser.close()
    except Exception as exc:  # keep the batch moving; audit records the error
        return {"page_title": "", "meta_description": "", "job_text": "",
                "jobposting_jsonld": "", "extraction_status": f"parse_error: {exc}"}

    job = jsonld_job(parser)
    title_node = next((n for n in walk(parser.root) if n.tag == "title"), None)
    page_title = node_text(title_node, skip_ignored=False) if title_node else ""
    title = text_value(job.get("title")) or parser.meta.get("og:title", "") or page_title
    description = text_value(job.get("description"))
    meta_description = (parser.meta.get("description", "")
                        or parser.meta.get("og:description", ""))
    location = text_value(job.get("jobLocation")) or text_value(job.get("jobLocationType"))
    company = text_value(job.get("hiringOrganization"))
    salary = text_value(job.get("baseSalary"))
    text = best_job_text(parser.root)

    # Titles often carry a useful expired/closed marker. Keep the raw page text
    # too; this status is only a transparent keyword hint, not a legal status.
    status = ""
    status_match = re.search(r"\b(expired|closed|filled|đã hết hạn|hết hạn)\b", title + " " + text, re.I)
    if status_match:
        status = status_match.group(1)

    return {
        "title": title,
        "company": company,
        "location": location,
        "posted_date": text_value(job.get("datePosted")),
        "valid_through": text_value(job.get("validThrough")),
        "employment_type": text_value(job.get("employmentType")),
        "salary": salary,
        "status_hint": status,
        "description": description,
        "meta_description": meta_description,
        "job_text": text,
        "jobposting_jsonld": json.dumps(job, ensure_ascii=False) if job else "",
        "extraction_status": "ok" if text or title else "empty_page_text",
    }


def read_indexes(batch_dir: Path) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    index_path = batch_dir / "_index.csv"
    if not index_path.exists():
        return result
    with index_path.open("r", encoding="utf-8-sig", newline="") as stream:
        for row in csv.DictReader(stream):
            job_id = (row.get("job_id") or "").strip()
            if job_id:
                result[job_id] = row
    return result


def read_fetch_logs(batch_dir: Path) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    log_path = batch_dir / "_fetch_log.jsonl"
    if not log_path.exists():
        return result
    with log_path.open("r", encoding="utf-8-sig") as stream:
        for line in stream:
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            filename = row.get("file")
            if filename:
                result[Path(filename).stem] = row
    return result


def source_for(path: Path, raw_root: Path) -> str:
    # Expected layout: data/raw/<source>/archive/census/<batch>/<page>.html
    relative = path.relative_to(raw_root)
    return relative.parts[0] if relative.parts else "unknown"


def make_record(
    path: Path,
    index: dict[str, str],
    log: dict[str, str],
    raw_root: Path,
) -> dict[str, str]:
    job_id = path.stem
    fields = parse_page(path)
    source = source_for(path, raw_root)
    url = index.get("url", "") or log.get("url", "")
    if not url:
        if source == "itviec":
            url = f"https://itviec.com/it-jobs/{job_id}"
        elif source == "topdev":
            url = f"https://topdev.vn/detail-jobs/{job_id}"
    return {
        "posting_id": f"{source}:{job_id}",
        "source": source,
        "batch": path.parent.name,
        "job_id": job_id,
        "html_file": str(path.relative_to(PROJECT_ROOT)),
        "url": url,
        "captured_at": index.get("captured", "") or log.get("archived_at", ""),
        "wanted": index.get("wanted", ""),
        "fetch_status": log.get("status", ""),
        **fields,
    }


POSTING_FIELDS = [
    "posting_id", "source", "batch", "job_id", "html_file", "url",
    "captured_at", "wanted", "fetch_status", "title", "company", "location",
    "posted_date", "valid_through", "employment_type", "salary", "status_hint",
    "description", "meta_description", "job_text", "jobposting_jsonld", "extraction_status",
]
AUDIT_FIELDS = ["posting_id", "source", "html_file", "extraction_status", "fetch_status"]


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def extract(raw_roots: list[Path], output_root: Path, sources: list[str]) -> tuple[int, int]:
    postings: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for raw_root in raw_roots:
        for source in sources:
            source_root = raw_root / source
            if not source_root.exists():
                print(f"Skip missing source folder: {source_root}")
                continue
            # Read each batch's metadata once instead of reopening a large index
            # file for every individual HTML page.
            for batch_dir in sorted(p for p in source_root.rglob("*") if p.is_dir()):
                html_files = sorted(batch_dir.glob("*.html"))
                if not html_files:
                    continue
                indexes = read_indexes(batch_dir)
                logs = read_fetch_logs(batch_dir)
                for html_path in html_files:
                    identity = (source, html_path.stem)
                    if identity in seen:
                        continue
                    seen.add(identity)
                    postings.append(make_record(
                        html_path,
                        indexes.get(html_path.stem, {}),
                        logs.get(html_path.stem, {}),
                        raw_root,
                    ))

    postings_path = output_root / "postings.csv"
    audit_path = output_root / "extraction_audit.csv"
    write_csv(postings_path, postings, POSTING_FIELDS)
    write_csv(audit_path, postings, AUDIT_FIELDS)
    failed = sum(row["extraction_status"] != "ok" for row in postings)
    print(f"Extracted {len(postings):,} pages; {failed:,} need review.")
    print(f"Postings: {postings_path}")
    print(f"Audit:    {audit_path}")
    return len(postings), failed


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raw", type=Path, nargs="+", default=DEFAULT_RAW_ROOTS,
                        help="one or more raw folders; defaults to data/raw or all data/raw-*/raw folders")
    parser.add_argument("--output", type=Path, default=OUTPUT_ROOT,
                        help=f"output folder (default: {OUTPUT_ROOT})")
    parser.add_argument("--sources", nargs="+", default=["itviec", "topdev"],
                        help="source folder names to process")
    args = parser.parse_args()
    extract([p.resolve() for p in args.raw], args.output.resolve(), args.sources)


if __name__ == "__main__":
    main()
