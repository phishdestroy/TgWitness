import re


def initials(name):
    text = re.sub(r"^@", "", str(name or "").strip())
    words = [word for word in text.split() if word[:1].isalpha() and word != "ID"]
    if words:
        return (words[0][0] + (words[1][0] if len(words) > 1 else "")).upper()
    return "#" if re.search(r"\d", text) else "?"
