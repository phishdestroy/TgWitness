"""Count the Anlage 1 complaint table locally; emit aggregate data, never names/texts.

Requires PyMuPDF and lingua-language-detector. Table cells, rather than page-local
date anchors, keep complaint rows intact across page breaks. This parser is for
the pinned evidence file, not a general PDF table extractor.
"""
import argparse
from collections import Counter, defaultdict
import hashlib
import importlib.metadata
import json
from pathlib import Path
import re

import pymupdf
from lingua import LanguageDetectorBuilder


SOURCE_SHA256 = "2bb927e2c42fdc2e3ad089ae302dd887c343f6798aba00fcfac279224ff7d6af"


def intersects(word, box):
    return (min(word[2], box.x1) > max(word[0], box.x0)
            and min(word[3], box.y1) > max(word[1], box.y0))


def extract_rows(source):
    document = pymupdf.open(source)
    records = []
    fragments = 0
    for page_index in range(443, 620):
        page = document[page_index]
        drawings = page.get_drawings()
        boxes = [s["rect"] for s in drawings
                 if s.get("fill") == (0, 0, 0) and s.get("fill_opacity", 1) >= .99]
        # Right border of each Time of Report cell, including continuation cells.
        cells = sorted({(round(s["rect"].y0, 3), round(s["rect"].y1, 3))
                        for s in drawings if s["type"] == "s"
                        and abs(s["rect"].x0 - 380.027) < .05
                        and s["rect"].width < .05 and s["rect"].height > 1})
        words = page.get_text("words")
        for top, bottom in cells:
            band = sorted([w for w in words if top <= (w[1] + w[3]) / 2 < bottom],
                          key=lambda w: (round(w[1], 1), w[0]))
            dates = [w[4] for w in band if 323.03 <= w[0] < 380.4]
            if "Report" in dates or "Time" in dates:
                continue
            dates = [t for t in dates if re.fullmatch(r"20\d{2}-|\d{2}-\d{0,2}|\d{2}:\d{2}:\d{2}", t)]
            years = [t for t in dates if re.fullmatch(r"20\d{2}-", t)]
            if years:
                assert len(years) == 1
                records.append({"pages": [], "dates": [], "types": [], "texts": [], "name_parts": [],
                                "name_words": 0, "name_covered": 0,
                                "text_words": 0, "text_covered": 0})
            elif not records:
                continue
            else:
                fragments += 1
            row = records[-1]
            row["pages"].append(page_index + 1)
            row["dates"].extend(dates)
            row["types"].extend(w[4] for w in band if 380.4 <= w[0] < 453.5)
            for field, start, end in (("name", 20.9, 323.03), ("text", 453.5, 3260.9)):
                selected = [w for w in band if start <= w[0] < end]
                row[field + "_words"] += len(selected)
                row[field + "_covered"] += sum(any(intersects(w, b) for b in boxes) for w in selected)
                if field == "text":
                    row["texts"].extend(w[4] for w in selected)
                else:
                    row["name_parts"].extend(w[4] for w in selected)
    for row in records:
        years = [s for s in row["dates"] if re.fullmatch(r"20\d{2}-", s)]
        months = [s for s in row["dates"] if re.fullmatch(r"\d{2}-\d{0,2}", s)]
        times = [s for s in row["dates"] if ":" in s]
        assert len(years) == len(months) == 1 and len(times) <= 1
        row["date"] = years[0] + months[0]
        row["time"] = times[0] if times else None
        row["month"] = row["date"][:7]
        row["category"] = re.sub(r"\s*\(\d+\)", "", " ".join(row["types"])).strip()
        row["text"] = " ".join(row["texts"]).strip()
        row["name"] = "".join(row["name_parts"])
        count, covered = row["text_words"], row["text_covered"]
        row["visibility"] = ("empty" if not count else "visible" if not covered
                             else "boxed" if covered == count else "partly")
    return records, fragments


def classify_language(detector, text):
    # URLs and addresses are not useful evidence of the prose's language.
    clean = re.sub(r"https?://\S+|www\.\S+|[\w.+-]+@[\w.-]+", " ", text)
    words = re.findall(r"[^\W\d_]+", clean, flags=re.UNICODE)
    if len(words) < 3 or sum(map(len, words)) < 12:
        return "Uncertain / short / non-linguistic"
    values = detector.compute_language_confidence_values(clean)
    if len(values) < 2 or values[0].value < .70 or values[0].value - values[1].value < .20:
        return "Uncertain / short / non-linguistic"
    return values[0].language.name.title().replace("_", " ")


def audit(source):
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    if digest != SOURCE_SHA256:
        raise ValueError("This parser is pinned to the documented Anlage1.pdf SHA-256")
    rows, fragments = extract_rows(source)
    assert len(rows) == 1995, f"Unexpected row count: {len(rows)}"
    detector = LanguageDetectorBuilder.from_all_languages().build()
    for row in rows:
        row["language"] = classify_language(detector, row["text"])
    monthly = defaultdict(Counter)
    types = defaultdict(Counter)
    languages = defaultdict(Counter)
    for row in rows:
        for table, key in ((monthly, row["month"]), (types, row["category"]), (languages, row["language"])):
            table[key]["total"] += 1
            table[key][row["visibility"]] += 1
    visible_duplicates = Counter(row["text"] for row in rows if row["visibility"] == "visible")
    comparison = {}
    for visibility in ("visible", "boxed"):
        group = [r for r in rows if r["visibility"] == visibility]
        comparison[visibility] = {
            "records": len(group),
            "suspected_hijacker": sum(r["category"] == "Suspected Hijacker" for r in group),
            "descriptions_containing_cyrillic": sum(bool(re.search(r"[\u0400-\u052f]", r["text"])) for r in group),
            "login_latin_letters_then_3_to_5_digits": sum(bool(re.fullmatch(r"[A-Za-z]+[0-9]{3,5}", r["name"])) for r in group),
            "distinct_login_strings": len({r["name"] for r in group}),
        }
    with pymupdf.open(source) as document:
        logon = re.search(r"Last Client/Web Logon Time:\s*(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2}:\d{2})", document[0].get_text())
        assert logon
    result = {
        "source_sha256": digest, "source_pages": [444, 620], "records": len(rows),
        "method": "PDF table-cell borders; continuation cells joined across pages; word-box overlap with opaque black rectangles",
        "continuation_cells_joined": fragments,
        "visibility": dict(Counter(r["visibility"] for r in rows)),
        "visible_boxed_comparison": comparison,
        "comparison_method": {
            "cyrillic": "Description contains at least one character in U+0400–U+052F; script indicator, not language or nationality.",
            "login_pattern": "Full string matches [A-Za-z]+[0-9]{3,5}; formatting only, not proof of automation or common authorship.",
            "denominators": "50 visible and 1944 boxed non-empty descriptions; one empty description excluded.",
        },
        "latest_client_web_logon": {"value": " ".join(logon.groups()) + " UTC", "page": 1,
                                     "scope": "Value in the supplied export, not an independent audit of all sessions or message events."},
        "reporter_rows_with_text_under_boxes": sum(r["name_covered"] > 0 for r in rows),
        "complete_date_and_time": sum(bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", r["date"])) and bool(r["time"]) for r in rows),
        "incomplete_date_values": dict(Counter(r["date"] for r in rows if not r["time"])),
        "by_month": dict(sorted(monthly.items())),
        "report_types": dict(sorted(types.items(), key=lambda item: -item[1]["total"])),
        "language_estimates": dict(sorted(languages.items(), key=lambda item: -item[1]["total"])),
        "language_method": {"library": "lingua-language-detector", "version": importlib.metadata.version("lingua-language-detector"),
                            "languages": "all 75", "minimum_words": 3, "minimum_letters": 12,
                            "minimum_score": .70, "minimum_top_two_gap": .20,
                            "note": "Automatic predominant-language estimate, not a calibrated accuracy probability; short/ambiguous text is unassigned. No nationality inference. All processing local."},
        "visible_duplicate_groups": sum(count > 1 for count in visible_duplicates.values()),
        "visible_rows_in_duplicate_groups": sum(count for count in visible_duplicates.values() if count > 1),
        "empty_description_rows": [{"row": i + 1, "pages": r["pages"], "month": r["month"]}
                                   for i, r in enumerate(rows) if r["visibility"] == "empty"],
    }
    assert sum(v["total"] for v in result["by_month"].values()) == len(rows)
    assert sum(v["total"] for v in result["report_types"].values()) == len(rows)
    assert sum(v["total"] for v in result["language_estimates"].values()) == len(rows)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("source", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    result = audit(args.source)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
