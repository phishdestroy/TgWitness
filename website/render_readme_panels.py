"""Render README cards and buttons in the PhishDestroy profile's visual style.

Uses the profile's charcoal cards, cyan/violet/red accents and compact split
buttons. Outlined Manrope captions need no installed or remotely loaded fonts.
"""
import argparse
from html import escape
from pathlib import Path
import xml.etree.ElementTree as ET

OUT = Path(__file__).resolve().parents[1] / "docs/assets/presentation"
FONT = "Segoe UI, Arial, sans-serif"
CYAN, VIOLET, RED = "#66d5e9", "#b1a0ff", "#ff697a"


def svg(width, height, title, body):
    title = escape(title, quote=True)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}" role="img" aria-label="{title}">'
            f'<title>{title}</title><g font-family="{FONT}">{body}</g></svg>\n')


def label(text, x, y, size, color="#a9b7c9", weight=400, spacing=0):
    return (f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" '
            f'font-weight="{weight}" letter-spacing="{spacing}">{escape(text)}</text>')


def card(width, height, kicker, title, lines, color, *, large=False, still=False, delay=0):
    result = (f'<rect x="1" y="1" width="{width-2}" height="{height-2}" rx="14" fill="#101720" stroke="#283341"/>'
              f'<path d="M27 1H{width-27}" stroke="{color}" stroke-opacity=".7" stroke-width="2"/>')
    result += label(kicker, 26, 42, 18 if large else 13, color, 600, 1.6)
    result += f'<circle cx="{width-30}" cy="37" r="4" fill="{color}">'
    if not still:
        result += f'<animate attributeName="opacity" values=".3;1;.3" dur="4s" begin="{delay}s" repeatCount="indefinite"/>'
    result += '</circle>'
    result += label(title, 26, 105 if large else 97, 40 if large else 27, "#f0f5fc", 650, -.6)
    for index, line in enumerate(lines):
        result += label(line, 26, (160 + index*39) if large else (145 + index*27), 27 if large else 17)
    return result


def services(still):
    entries = [
        ("apprise", "01 / APPRISE", "Notifications", ["Problem alerts, chat changes", "and daily summaries.", "Messengers, email or JSON webhooks."], CYAN),
        ("s3", "02 / S3 STORAGE", "Off-site copy", ["Journal, files and checkpoints.", "AES-256-GCM before upload.", "S3-compatible storage."], VIOLET),
    ]
    for name, kicker, title, lines, color in entries:
        body = card(600, 280, kicker, title, lines, color, large=True, still=still)
        text = title + ". " + " ".join(lines)
        (OUT / ("readme-card-" + name + ("-static" if still else "") + ".svg")).write_text(svg(600, 280, text, body), encoding="utf-8")


def handbook(mobile, still):
    entries = [
        ("01 / SET UP", "Connect & collect.", ["Accounts. Collection. Proxies.", "Start with a dedicated account."], CYAN),
        ("02 / WORK A CASE", "Follow the connections.", ["Investigations. Export & verify.", "Witness & Proof."], VIOLET),
        ("03 / MAINTAIN", "Keep it running.", ["Server, Docker and recovery.", "Troubleshooting."], RED),
    ]
    width, height = (640, 660) if mobile else (1200, 220)
    result = ""
    for index, (kicker, title, lines, color) in enumerate(entries):
        x, y = (0, index*230) if mobile else (index*408, 0)
        if mobile:
            # Keep the same reading order with larger type on a narrow screen.
            body = card(640, 200, kicker, title, lines, color, still=still, delay=index)
            body = body.replace('font-size="13"', 'font-size="18"').replace('font-size="27"', 'font-size="34"').replace('font-size="17"', 'font-size="25"')
            body = body.replace('y="145"', 'y="136"')
        else:
            body = card(384, 220, kicker, title, lines, color, still=still, delay=index)
        result += f'<g transform="translate({x} {y})">{body}</g>'
        if index < 2:
            route = f'M320 {y+201}V{y+229}' if mobile else f'M{x+385} 110H{x+407}'
            result += f'<path d="{route}" stroke="#39485b" stroke-width="2"/>'
    name = "readme-handbook" + ("-mobile" if mobile else "") + ("-static" if still else "")
    title = "Set up: accounts, collection and proxies. Work a case: investigations, exports and verification. Maintain: server, Docker, recovery and troubleshooting."
    (OUT / (name + ".svg")).write_text(svg(width, height, title, result), encoding="utf-8")


BUTTONS = (
    ("apprise", "APPRISE", "SETUP", "#167d95", 70, 58),
    ("s3", "S3", "SETUP & RECOVERY", "#7654b0", 36, 138),
    ("backup", "BACKUP", "GUIDE", "#245fa4", 67, 58),
    ("accounts", "SET UP", "ACCOUNTS", "#167d95", 64, 88),
    ("investigate", "INVESTIGATE", "GUIDE", "#7654b0", 105, 58),
    ("maintain", "MAINTAIN", "SERVER & DOCKER", "#a53b67", 86, 137),
    ("wiki", "WIKI", "OPEN", "#167d95", 47, 51),
    ("offline", "HANDBOOK", "OFFLINE", "#245fa4", 91, 75),
    ("docs", "DOCS", "REFERENCE", "#7654b0", 51, 97),
    ("explain", "EVIDENCE", "EXPLORE", "#167d95", 83, 80),
    ("model", "MODEL", "REFERENCE", "#7654b0", 63, 97),
    ("project", "BY", "PHISHDESTROY", "#a53b67", 31, 119),
    ("contribute", "CODE", "CONTRIBUTE", "#245fa4", 51, 105),
    ("support", "HELP", "SUPPORT", "#167d95", 48, 80),
    ("security", "SECURITY", "REPORT", "#7654b0", 82, 71),
)


def buttons():
    for name, left, right, color, a, b in BUTTONS:
        width = a+b
        body = (f'<clipPath id="edge"><rect width="{width}" height="34" rx="4"/></clipPath>'
                f'<g clip-path="url(#edge)"><rect width="{a}" height="34" fill="#26313e"/>'
                f'<rect x="{a}" width="{b}" height="34" fill="{color}"/>'
                f'<path d="M0 1H{width}" stroke="#fff" opacity=".12"/></g>'
                '<g fill="#fff" font-size="11" font-weight="600" letter-spacing=".7" text-anchor="middle">'
                f'<text x="{a/2}" y="21">{escape(left)}</text><text x="{a+b/2}" y="21">{escape(right)}</text></g>')
        (OUT / ("readme-button-" + name + ".svg")).write_text(svg(width, 34, left + ": " + right, body), encoding="utf-8")


def divider(still):
    body = '''<defs><linearGradient id="line" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="1200" y2="0"><stop stop-color="#ff506f" stop-opacity="0"/><stop offset=".35" stop-color="#ff506f" stop-opacity=".7"/><stop offset=".5" stop-color="#ff506f"/><stop offset=".65" stop-color="#58a6ff" stop-opacity=".7"/><stop offset="1" stop-color="#58a6ff" stop-opacity="0"/></linearGradient></defs>
<path d="M0 14H566M634 14H1200" stroke="url(#line)" stroke-width="1.5"/>
<path d="M580 14L588 6L596 14L588 22Z" fill="none" stroke="#ff506f" opacity=".55"/>
<path d="M597 14L605 6L613 14L605 22Z" fill="#ff506f">'''
    if not still:body += '<animate attributeName="opacity" values=".4;1;.4" dur="3s" repeatCount="indefinite"/>'
    body += '</path><path d="M614 14L622 6L630 14L622 22Z" fill="none" stroke="#58a6ff" opacity=".55"/>'
    for x, end, color in [(140, 460, "#ff6b81"), (1060, 740, "#58a6ff")]:
        body += f'<circle cx="{x}" cy="14" r="2" fill="{color}">'
        if not still:body += f'<animate attributeName="cx" values="{x};{end};{x}" dur="6s" repeatCount="indefinite"/>'
        body += '</circle>'
    (OUT / ("readme-divider" + ("-static" if still else "") + ".svg")).write_text(svg(1200, 28, "Section divider", body), encoding="utf-8")


def outline_captions(font_path):
    from fontTools.pens.svgPathPen import SVGPathPen
    from fontTools.ttLib import TTFont
    from fontTools.varLib.instancer import instantiateVariableFont

    ns = "http://www.w3.org/2000/svg"
    ET.register_namespace("", ns)
    faces = {w: instantiateVariableFont(TTFont(font_path), {"wght": w}, inplace=False) for w in (400, 600, 650)}
    cache = {}
    files = [*OUT.glob("readme-card-*.svg"), *OUT.glob("readme-handbook*.svg"), *OUT.glob("readme-button-*.svg")]
    for path in files:
        root = ET.fromstring(path.read_text(encoding="utf-8"))
        definitions = ET.Element("{" + ns + "}defs")
        glyph_ids = {}

        def visit(parent, inherited):
            inherited = {**inherited, **parent.attrib}
            for index, node in enumerate(list(parent)):
                attrs = {**inherited, **node.attrib}
                if node.tag != "{" + ns + "}text":
                    visit(node, inherited)
                    continue
                value = "".join(node.itertext())
                weight = int(attrs.get("font-weight", 400))
                face = faces[weight]
                size = float(attrs.get("font-size", 16))
                scale = size / face["head"].unitsPerEm
                spacing = float(attrs.get("letter-spacing", 0))
                glyph_set, cmap = face.getGlyphSet(), face.getBestCmap()
                chars = []
                for char in value:
                    key = weight, char
                    if key not in cache:
                        glyph = glyph_set[cmap[ord(char)]]
                        pen = SVGPathPen(glyph_set)
                        glyph.draw(pen)
                        cache[key] = pen.getCommands(), glyph.width
                    commands, width = cache[key]
                    if key not in glyph_ids and commands:
                        glyph_ids[key] = "caption-" + str(len(glyph_ids))
                        ET.SubElement(definitions, "{" + ns + "}path", {"id": glyph_ids[key], "d": commands})
                    chars.append((glyph_ids.get(key), width))
                length = sum(width * scale + spacing for _, width in chars) - spacing
                x, y = float(attrs.get("x", 0)), float(attrs.get("y", 0))
                if attrs.get("text-anchor") == "middle":x -= length / 2
                group = ET.Element("{" + ns + "}g", {"aria-label": value, "fill": attrs.get("fill", "#fff"), "transform": f"translate({x:g} {y:g}) scale({scale:g} {-scale:g})"})
                offset = 0
                for ident, width in chars:
                    if ident:
                        ET.SubElement(group, "{" + ns + "}use", {"href": "#" + ident, "transform": f"translate({offset:g} 0)"})
                    offset += width + spacing / scale
                parent.remove(node)
                parent.insert(index, group)

        visit(root, {})
        root.insert(1, definitions)
        path.write_text(ET.tostring(root, encoding="unicode"), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--font", required=True, help="Path to the OFL-licensed Manrope variable TTF")
    args = parser.parse_args()
    buttons()
    for still in (False, True):
        services(still)
        divider(still)
        for mobile in (False, True):handbook(mobile, still)
    outline_captions(args.font)
    print("Rendered service cards, handbook routes, compact buttons and matching PhishDestroy dividers.")


if __name__ == "__main__":
    main()
