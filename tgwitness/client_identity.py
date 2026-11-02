"""Bounded Telegram client descriptions, retained with account authorization."""
import platform
import re
import unicodedata

from telethon import TelegramClient

from . import api_pool

FIELDS = {
    "device_model": ("device_model", "device"),
    "system_version": ("system_version", "sdk"),
    "app_version": ("app_version",),
    "lang_code": ("lang_code",),
    "system_lang_code": ("system_lang_code",),
    "lang_pack": ("lang_pack",),
}


def validate(profile):
    if profile is None:
        return {}
    if not isinstance(profile, dict) or set(profile) - FIELDS.keys():
        raise ValueError("Unsupported Telegram client profile fields.")
    result = {}
    for field, value in profile.items():
        limit = 32 if field in ("lang_code", "system_lang_code", "lang_pack") else 128
        if (not isinstance(value, str) or len(value) > limit
                or any(unicodedata.category(c).startswith("C") for c in value)):
            raise ValueError("Invalid Telegram client profile: " + field)
        value = value.strip()
        if not value and field != "lang_pack":
            raise ValueError("Empty Telegram client profile: " + field)
        if field in ("lang_code", "system_lang_code", "lang_pack") and value and not re.fullmatch(r"[A-Za-z0-9_-]+", value):
            raise ValueError("Invalid Telegram language identifier: " + field)
        result[field] = value
    return result


def from_account(raw):
    profile = {}
    for field, aliases in FIELDS.items():
        values = [raw[name] for name in aliases if raw.get(name) is not None]
        if values:
            if any(value != values[0] for value in values[1:]):
                raise ValueError("Conflicting Telegram client profile: " + field)
            profile[field] = values[0]
    return validate(profile)


def resolve(api_id, supplied=None):
    machine = platform.machine()
    model = "PC 64bit" if machine in ("x86_64", "AMD64") else "PC 32bit" if machine in ("i386", "i686", "x86") else machine
    profile = {"device_model": model or "Desktop", "system_version": re.sub(r"-.+", "", platform.release()) or "1.0",
               "app_version": TelegramClient.__version__, "lang_code": "en", "system_lang_code": "en", "lang_pack": ""}
    profile.update(api_pool.device_for(api_id))
    profile.update(validate(supplied))
    return validate(profile)
