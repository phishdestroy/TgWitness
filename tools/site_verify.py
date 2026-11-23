"""The independent browser verifier at verify/: one self-contained folder per language (page, script, stylesheet),
so a saved copy keeps working offline. The page's own policy forbids network connections."""
import html
import json
import re

try:
    from . import site_i18n
except ImportError:
    import site_i18n

PATH = "verify/"
SOURCE = "website/verify/index.html"
SCRIPT = "website/verify/verify.js"
ASSETS = {"verify.js": SCRIPT, "verify.css": "website/verify/verify.css"}
TITLE = "Check a TgWitness archive"
DESCRIPTION = ("Check a TgWitness evidence archive in your browser: the manifest signature, every file and the signed "
               "event chain. Nothing is uploaded.")
MAIN = re.compile(r'(<main class="vf">)(.*?)(</main>)', re.S)


def outputs(prefixes):
    return [prefix + PATH + name for prefix in prefixes for name in ("index.html", *ASSETS)]


def fragment(template):
    return MAIN.search(template).group(2)


def strings(template, script):
    return [TITLE, DESCRIPTION, "Language", *site_i18n.attribute_values(fragment(template)), *site_i18n.script_strings(script)]


def page(template, script, lang, data, languages):
    """languages: (code, native name, href) for the language menu, in site order."""
    code, direction = site_i18n.LANGUAGES[lang][1], site_i18n.LANGUAGES[lang][2]
    text = lambda value: site_i18n.text(data, value)
    body, missing = site_i18n.localize(fragment(template), data)
    dictionary = {} if data is None else {key: data["strings"][key] for key in site_i18n.script_strings(script)
                                          if data["strings"].get(key, "").strip()}
    menu = f'<nav class="vf-langs" aria-label="{html.escape(text("Language"), quote=True)}">' + "".join(
        f'<a href="{html.escape(href, quote=True)}" lang="{site_i18n.LANGUAGES[other][1]}"'
        + (' aria-current="page"' if other == lang else "") + f'>{html.escape(name)}</a>' for other, name, href in languages) + "</nav>"
    result = MAIN.sub(lambda match: match.group(1) + body + match.group(3), template, count=1)
    result = result.replace('<html lang="en" dir="ltr">', f'<html lang="{code}" dir="{direction}">', 1)
    result = result.replace(f"<title>{TITLE}</title>", f"<title>{html.escape(text(TITLE))}</title>", 1)
    result = result.replace(f'content="{DESCRIPTION}"', f'content="{html.escape(text(DESCRIPTION), quote=True)}"', 1)
    result = result.replace('<script type="application/json" id="site-dict">{}</script>',
                            '<script type="application/json" id="site-dict">'
                            + json.dumps(dictionary, ensure_ascii=False).replace("</", "<\\/") + "</script>", 1)
    return result.replace("<!--LANGUAGES-->", menu, 1), missing
