"""Interface languages: the panel loads /locale.js and receives the dictionary of one language."""
import json
from functools import lru_cache
from pathlib import Path

LANGUAGES = ("en", "ru", "uk", "es", "pt", "tr", "ar", "fa", "ur", "hi", "id", "vi", "zh")
COOKIE = "tgwitness-lang"
LOCALES = Path(__file__).parent / "locales"
ENGLISH_FALLBACKS = Path(__file__).parent / "english_fallbacks.json"


def pick(cookie, accept):
    """The language chosen in the panel, else the browser's preferred supported one, else English."""
    if cookie in LANGUAGES:
        return cookie
    choices = []
    for order, part in enumerate((accept or "").split(",")):
        tag, *params = part.strip().split(";")
        weight = 1.0
        for param in params:
            name, _, value = param.strip().partition("=")
            if name == "q":
                try:
                    weight = float(value)
                except ValueError:
                    weight = 0.0
        if weight > 0:
            choices.append((-weight, order, tag.strip().lower().split("-")[0]))
    return next((lang for _, _, lang in sorted(choices) if lang in LANGUAGES), "en")


def words(lang):
    if lang == "en":
        return {}
    # Explicitly catalogued English text for sections awaiting translation.
    # Coverage tests still reject new strings absent from both catalogs.
    fallback = {text: text for text in json.loads(ENGLISH_FALLBACKS.read_text(encoding="utf-8"))}
    return {**fallback, **json.loads((LOCALES / (lang + ".json")).read_text(encoding="utf-8"))}


@lru_cache(maxsize=None)
def script(lang):
    return ("window.TGW_LANG=" + json.dumps(lang) + ";window.TGW_DICT="
            + json.dumps(words(lang), ensure_ascii=False, separators=(",", ":")) + ";\n").encode("utf-8")
