def content_type(path):
    with path.open("rb") as source:
        head = source.read(512)
    if head.startswith(b"\xff\xd8\xff"):
        return "image/jpeg"
    if head.startswith(b"\x89PNG\r\n\x1a\n"):
        return "image/png"
    if head[:6] in (b"GIF87a", b"GIF89a"):
        return "image/gif"
    if head.startswith(b"RIFF") and head[8:12] == b"WEBP":
        return "image/webp"
    if head.startswith(b"OggS"):
        return "audio/ogg"
    if head.startswith(b"RIFF") and head[8:12] == b"WAVE":
        return "audio/wav"
    if head.startswith(b"fLaC"):
        return "audio/flac"
    if head.startswith(b"\x1aE\xdf\xa3"):
        return "video/webm" if b"webm" in head[:64] else "video/x-matroska"
    if head.startswith(b"ID3") or head[:2] in (b"\xff\xfb", b"\xff\xf3", b"\xff\xf2"):
        return "audio/mpeg"
    if head[4:8] == b"ftyp" and head[8:12] in (b"avif", b"avis"):
        return "image/avif"
    if head[4:8] == b"ftyp" and head[8:12] in (b"heic", b"heix", b"mif1", b"msf1"):
        return "image/heic"
    if head[4:8] == b"ftyp" and head[8:12] in (
            b"isom", b"iso2", b"iso4", b"iso5", b"iso6", b"mp41", b"mp42", b"avc1", b"dash", b"mp4v", b"MSNV",
            b"3gp4", b"3gp5", b"3gp6", b"3g2a", b"f4v ", b"M4V ", b"M4A ", b"M4B ", b"qt  "):
        return "audio/mp4" if head[8:12] in (b"M4A ", b"M4B ") else "video/mp4"
    if head.startswith(b"%PDF-"):
        return "application/pdf"
    return "application/octet-stream"
