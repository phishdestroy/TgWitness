"""Compose TgWitness's investigation artwork into its repository identity.

Pass --font /path/to/Manrope.ttf. Uses the existing, reviewed illustration and
outlined type. No network, new image generation, account data or SVG scripts.
"""
import argparse
from copy import deepcopy
from pathlib import Path
import re
import xml.etree.ElementTree as ET

from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

from render_readme import Drawing
from render_case_assets import save

ROOT = Path(__file__).resolve().parents[1]
NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)


def scene():
    source = ET.fromstring((ROOT / "docs/assets/presentation/readme-investigation-animated.svg").read_text(encoding="utf-8"))
    result = []
    for element in source:
        tag = element.tag.rsplit("}", 1)[-1]
        cls = element.get("class", "")
        keep = tag in {"defs", "style"} or (tag == "use" and bool(element.get("mask")))
        keep |= cls.startswith(("source-", "packet ")) or bool(element.get("clip-path"))
        if not keep:
            continue
        item = deepcopy(element)
        if cls.startswith("source-"):
            # The illustrated tiles tell the story; remove their tiny old labels.
            for child in list(item):
                if child.tag.rsplit("}", 1)[-1] == "g":
                    item.remove(child)
        result.append(ET.tostring(item, encoding="unicode"))
    svg = "".join(result)
    svg = re.sub(r'id="([^"]+)"', r'id="scene-\1"', svg)
    svg = re.sub(r'href="#([^"]+)"', r'href="#scene-\1"', svg)
    svg = re.sub(r'url\(#([^)]+)\)', r'url(#scene-\1)', svg)
    return svg


def background(d):
    d.add('''<defs>
<linearGradient id="identity-bg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#080f1a"/><stop offset=".55" stop-color="#0c1829"/><stop offset="1" stop-color="#10243a"/></linearGradient>
<radialGradient id="identity-light"><stop stop-color="#4084b7" stop-opacity=".26"/><stop offset="1" stop-color="#1e507e" stop-opacity="0"/></radialGradient>
<linearGradient id="identity-line"><stop stop-color="#69b9f8" stop-opacity="0"/><stop offset=".5" stop-color="#c7ebff"/><stop offset="1" stop-color="#d9b97f" stop-opacity="0"/></linearGradient>
<radialGradient id="identity-fade" cx="52%" cy="52%" r="64%"><stop offset=".55" stop-color="white"/><stop offset="1" stop-color="black"/></radialGradient>
<mask id="identity-feather"><rect width="820" height="690" fill="url(#identity-fade)"/></mask>
<linearGradient id="identity-fade-y" x1="0" y1="0" x2="0" y2="1"><stop stop-color="black"/><stop offset=".1" stop-color="white"/><stop offset=".83" stop-color="white"/><stop offset="1" stop-color="black"/></linearGradient>
<mask id="identity-vertical"><rect width="820" height="690" fill="url(#identity-fade-y)"/></mask>
<pattern id="identity-dots" width="28" height="28" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r=".8" fill="#88b2d3" opacity=".14"/></pattern>
</defs>''')
    d.add(f'<rect width="{d.width}" height="{d.height}" rx="22" fill="url(#identity-bg)"/>')
    d.add(f'<rect width="{d.width}" height="{d.height}" rx="22" fill="url(#identity-dots)"/>')
    d.add(f'<ellipse cx="{d.width*.72}" cy="{d.height*.48}" rx="500" ry="430" fill="url(#identity-light)"/>')
    d.add('''<style>
.identity-orbit{transform-box:fill-box;transform-origin:center;animation:identity-orbit 48s linear infinite}
.identity-float{animation:identity-float 12s ease-in-out infinite}
.identity-trace{stroke-dasharray:100 1300;animation:identity-trace 12s linear infinite}
.identity-sign{stroke-dasharray:1;animation:identity-sign 12s ease-in-out infinite}
@keyframes identity-orbit{to{transform:rotate(360deg)}}
@keyframes identity-float{0%,100%{transform:translateY(0)}50%{transform:translateY(-11px)}}
@keyframes identity-trace{from{stroke-dashoffset:1400}to{stroke-dashoffset:0}}
@keyframes identity-sign{0%,35%{stroke-dashoffset:1;opacity:.3}65%,90%{stroke-dashoffset:0;opacity:1}100%{stroke-dashoffset:0;opacity:.3}}
</style>''')


def artwork(d, x, y, width, height, original):
    d.add(f'<svg x="{x}" y="{y}" width="{width}" height="{height}" viewBox="0 0 820 690">'
          '<g mask="url(#identity-vertical)"><g mask="url(#identity-feather)"><g class="identity-float">'
          '<svg width="820" height="690" viewBox="535 30 820 690">'
          + original + '</svg></g></g></g></svg>')


def hero(font, original, mobile=False, still=False, wiki=False):
    width, height = (720, 920) if mobile else (1440, 690)
    if wiki and not mobile:
        height = 510
    d = Drawing(font, width, height, "TgWitness — Follow the trail. Preserve the evidence.")
    background(d)
    if mobile:
        artwork(d, -40, 241, 800, 665, original)
    else:
        d.add('<circle class="identity-orbit" cx="1070" cy="335" r="291" fill="none" '
              'stroke="#8abfdf" stroke-opacity=".17" stroke-dasharray="95 370 20 180" stroke-width="1.5"/>')
        artwork(d, 624 if not wiki else 790, -9 if not wiki else -30, 840 if not wiki else 650, 705 if not wiki else 547, original)
    mark = (ROOT / "tgwitness/static/mark.svg").read_text(encoding="utf-8")
    mark = mark.replace('viewBox="0 0 48 48"', 'x="44" y="37" width="34" height="34" viewBox="0 0 48 48"')
    d.add(mark)
    d.text("TgWitness / PHISHDESTROY" if wiki else "PHISHDESTROY", 91, 60, 13, "#b9cde1", 600, 2.4)
    if mobile:
        d.text("TgWitness", 41, 175, 98, "#edf6ff", 800, -3.5)
        d.text("Follow the trail.", 45, 233, 36, "#e3effd", 600, -.8)
        d.text("Preserve the evidence.", 45, 281, 36, "#9fc7ef", 600, -.8)
        d.add('<path d="M0 840H720V898a22 22 0 0 1-22 22H22a22 22 0 0 1-22-22Z" fill="#0b1828" fill-opacity=".9"/>'
              '<path d="M46 840H674" stroke="#365472"/>')
        d.text("CAPTURE", 46, 881, 15, "#a9c8e4", 600, 1.6)
        d.text("CONNECT", 280, 881, 15, "#a9c8e4", 600, 1.6)
        d.text("VERIFY", 537, 881, 15, "#d8c29a", 600, 1.6)
        d.add('<path class="identity-trace" d="M46 840H674" fill="none" stroke="url(#identity-line)" stroke-width="2"/>')
    elif wiki:
        d.text("THE INVESTIGATION HANDBOOK", 46, 117, 13, "#9fc7ef", 600, 2)
        d.text("Work the case.", 43, 218, 76, "#edf6ff", 800, -2.5)
        d.text("Keep the record.", 43, 303, 76, "#a5cff7", 800, -2.5)
        d.text("Your first capture. Your next lead. Your signed handoff.", 47, 365, 21, "#b3c7dd")
        d.add('<path d="M46 451H1394" stroke="#29455f"/>')
        d.add('<path class="identity-trace" d="M46 451H1394" fill="none" stroke="url(#identity-line)" stroke-width="2"/>')
    else:
        d.text("YOUR TELEGRAM INVESTIGATION WORKSPACE", 47, 127, 13, "#92b9d9", 600, 1.2)
        d.text("TgWitness", 40, 247, 116, "#edf6ff", 800, -4)
        d.text("Follow the trail.", 47, 320, 43, "#e3effd", 600, -1.2)
        d.text("Preserve the evidence.", 47, 377, 43, "#9fc7ef", 600, -1.2)
        d.text("Conversations. Connections. A record you can verify.", 49, 432, 20, "#adc2d9")
        d.add('<path class="identity-sign" pathLength="1" d="M53 520c27-61 41-54 25-5s38-60 47-39-42 69-13 61 47-49 46-27-17 32 4 21 18-36 31-19-8 30 9 22l68-20" '
              'fill="none" stroke="#b9dfd5" stroke-width="2.2" stroke-linecap="round"/>')
        d.text("FOLLOW THE SOURCES. KEEP THE CONTEXT.", 49, 578, 13, "#799ab7", 600, 1.1)
        d.add('<path d="M0 630H1440V668a22 22 0 0 1-22 22H22a22 22 0 0 1-22-22Z" fill="#0b1828" fill-opacity=".9"/>'
              '<path d="M46 631H1394" stroke="#29455f"/>')
        d.add('<path class="identity-trace" d="M46 631H1394" fill="none" stroke="url(#identity-line)" stroke-width="2"/>')
        for x, num, word in [(47,"01","CAPTURE"),(360,"02","CONNECT"),(719,"03","PRESERVE"),(1091,"04","VERIFY")]:
            d.text(num, x, 665, 12, "#d4b884", 600)
            d.text(word, x+34, 665, 12, "#a3bfd9", 600, 1.6)
    if still:
        d.add('<style>*{animation:none!important}.packet,.scan,.seal-ring{display:none}.flow{opacity:.45}.identity-sign{stroke-dasharray:none;stroke-dashoffset:0}</style>')
    else:
        # Keep the composition complete at every point in the loop. Records and
        # connection traces provide the narrative movement; tiles gently float.
        d.add('''<style>
.source-private,.source-group,.source-channel,.source-bot,.source-record{opacity:1;animation:identity-source 8s ease-in-out infinite}
.source-group{animation-delay:-2s}.source-channel{animation-delay:-4s}.source-bot{animation-delay:-6s}
@keyframes identity-source{0%,100%{transform:translateY(0)}50%{transform:translateY(-4px)}}
</style>''')
    name = "identity-wiki" if wiki else "identity-hero"
    name += "-mobile" if mobile else ""
    name += "-static" if still else ""
    save(d, name + ".svg", "An illustrated investigation: sources connect, observed records move into a dossier, "
         "and a signature is drawn. Fictional records, not a screenshot of the application.")


def navigation(font):
    for name, title, primary in (("demo","Explore the workspace",True),("start","Start your first case",False),("wiki","Open the handbook",False)):
        d = Drawing(font, 248, 56, title)
        fill, stroke, ink = ("#c3e2ff","#c3e2ff","#112941") if primary else ("#102033","#355473","#d7e9fc")
        d.add(f'<rect x=".5" y=".5" width="247" height="55" rx="8" fill="{fill}" stroke="{stroke}"/>')
        d.text(title, 18, 34, 15, ink, 600, -.2)
        d.add(f'<path d="M218 28h12m-5-5 5 5-5 5" fill="none" stroke="{ink}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>')
        save(d, "identity-nav-"+name+".svg", title)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--font", required=True)
    args = parser.parse_args()
    font = {weight: instantiateVariableFont(TTFont(args.font), {"wght":weight}, inplace=False) for weight in (500,600,800)}
    original = scene()
    for still in (False, True):
        hero(font, original, still=still)
        hero(font, original, mobile=True, still=still)
        hero(font, original, wiki=True, still=still)
    navigation(font)
    print("Rendered six investigation identity covers and three navigation assets.")


if __name__ == "__main__":
    main()
