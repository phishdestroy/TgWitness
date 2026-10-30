"""Compose README artwork from the real, fictional-data workspace captures.

Uses Playwright Chromium and an optional local Manrope font. No network requests,
application imports or account data. The output is a still in both colour themes.
"""
import argparse
import base64
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'docs/assets/presentation'


def data(path, mime):
    return f'data:{mime};base64,' + base64.b64encode(path.read_bytes()).decode('ascii')


def artwork(theme, mobile, font=None):
    dark = theme == 'dark'
    screenshot = ROOT / 'docs/assets' / ('chats-dark.png' if dark else 'chats.png')
    font_face = (f'@font-face{{font-family:Manrope;src:url("{data(font, "font/ttf")}");font-weight:200 800}}' if font else '')
    palette = ('#0d1422', '#132135', '#e8f0ff', '#9bafc9', '#74a8ff', '#29394f') if dark else ('#f2f5fa', '#e5edf8', '#14243c', '#52647d', '#225bca', '#ccd8e8')
    bg, soft, ink, muted, accent, line = palette
    return f'''<!doctype html><html lang="en"><meta charset="utf-8"><style>
{font_face}
*{{box-sizing:border-box}}html,body{{margin:0;width:100%;height:100%;overflow:hidden}}
body{{font-family:Manrope,Arial,sans-serif;background:{bg};color:{ink}}}
.poster{{position:relative;width:1440px;height:920px;padding:46px 52px 0;overflow:hidden}}
.wash{{position:absolute;z-index:0;width:1000px;height:650px;right:-250px;top:-310px;border-radius:50%;background:radial-gradient(ellipse,{soft},transparent 70%);pointer-events:none}}
.brand,h1,.description{{position:relative;z-index:1}}
.brand{{display:flex;align-items:center;gap:13px;font-size:31px;font-weight:800;letter-spacing:-1.2px}}
.brand img{{width:40px;height:40px}}.brand small{{font-size:12px;font-weight:600;letter-spacing:1.6px;color:{muted};margin-left:auto}}
h1{{font-size:64px;line-height:1.12;letter-spacing:-3.3px;font-weight:750;margin:30px 0 14px}}
h1 span{{color:{accent}}}.description{{font-size:20px;color:{muted};margin:0;letter-spacing:-.25px}}
.app{{position:relative;margin-top:34px;border:1px solid {line};border-radius:15px 15px 0 0;overflow:hidden;box-shadow:0 16px 50px #07152a24;background:{bg};height:625px}}
.bar{{height:40px;display:flex;align-items:center;padding:0 17px;gap:7px;border-bottom:1px solid {line};background:{soft};font-size:10px;color:{muted};font-weight:600}}
.dot{{width:7px;height:7px;border-radius:50%;background:{muted};opacity:.35}}.bar b{{margin-left:12px;letter-spacing:.4px;font-weight:600}}.bar span:last-child{{margin-left:auto;letter-spacing:1px;font-size:9px}}
.viewport{{overflow:hidden}}.screen{{display:block;width:100%;height:auto}}.edge{{position:absolute;bottom:0;left:0;right:0;height:48px;background:linear-gradient(transparent,{bg})}}
.mobile{{width:720px;height:770px;padding:37px 32px 0}}
.mobile .brand{{font-size:37px;letter-spacing:-1.3px;gap:13px}}.mobile .brand img{{width:43px;height:43px}}.mobile .brand small{{font-size:10px;letter-spacing:1px;max-width:130px;text-align:right;line-height:1.6}}
.mobile h1{{font-size:56px;letter-spacing:-2.5px;line-height:1.13;margin:31px 0 16px;max-width:620px}}
.mobile h1 span{{display:block}}.mobile .description{{font-size:22px;line-height:1.5;max-width:550px}}
.mobile .app{{margin-top:28px;height:400px}}.mobile .bar{{height:35px}}.mobile .screen{{width:1230px;max-width:none;transform:translate(-535px,-138px)}}
.mobile .bar span:last-child{{font-size:8px}}.mobile .edge{{height:35px}}
</style><body><div class="poster{' mobile' if mobile else ''}"><div class="wash"></div>
<div class="brand"><img src="{data(ROOT / 'tgwitness/static/mark.svg', 'image/svg+xml')}" alt="">TgWitness<small>TELEGRAM<br>INVESTIGATION WORKSPACE</small></div>
<h1>Follow the trail. <span>Keep the record.</span></h1>
<p class="description">Captured conversations. Preserved changes. Verifiable exports.</p>
<div class="app"><div class="bar"><i class="dot"></i><i class="dot"></i><i class="dot"></i><b>WORKSPACE / CHAT HISTORY</b><span>FICTIONAL DEMO</span></div>
<div class="viewport"><img class="screen" src="{data(screenshot, 'image/png')}" alt="Actual TgWitness chat workspace with fictional records"></div></div><div class="edge"></div></div></body></html>'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--font', type=Path, help='Optional local Manrope variable TTF (see OFL-Manrope.txt)')
    args = parser.parse_args()
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(device_scale_factor=1, reduced_motion='reduce')
        page.route('http://**/*', lambda route: route.abort())
        page.route('https://**/*', lambda route: route.abort())
        for mobile in (False, True):
            for theme in ('light', 'dark'):
                page.set_viewport_size({'width': 720 if mobile else 1440, 'height': 770 if mobile else 920})
                page.set_content(artwork(theme, mobile, args.font))
                page.evaluate('document.fonts.ready')
                page.wait_for_function('[...document.images].every(i=>i.complete&&i.naturalWidth>0)')
                target = OUTPUT / f'readme-product-{"mobile-" if mobile else ""}{theme}.png'
                page.screenshot(path=str(target))
                print(target)
        browser.close()


if __name__ == '__main__':
    main()
