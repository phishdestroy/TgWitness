"""Build an English GitHub Wiki bundle from reviewed Markdown pages.

No Git operations, publication, application imports or network access.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import tomllib
from urllib.parse import quote, unquote, urlsplit
import zipfile

if __package__:
    from .build_source import public_sources
else:
    from build_source import public_sources

ROOT = Path(__file__).resolve().parents[1]
PAGES = (
    "Home", "Getting-Started", "Accounts", "Collection", "Investigations",
    "Exports-and-Verification", "Proxies", "Witness-and-Proof", "Server-and-Docker",
    "Backup-and-Recovery", "Troubleshooting", "FAQ", "Glossary",
)
FILES = tuple(name + ".md" for name in (*PAGES, "_Sidebar", "_Footer"))
LINK = re.compile(r'(!?\[[^\]\n]*\]\()(<[^>\n]+>|[^)\s]+)((?:\s+"[^"\n]*")?\))')
FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")


def render_links(content, source, root, public, repository, branch):
    """Resolve local documentation links for GitHub's separate wiki repository."""
    repo_url = "https://github.com/" + repository
    wiki = root / "docs/wiki"

    def replace(match):
        href = urlsplit(match[2].strip("<>"))
        if href.scheme or href.netloc or not href.path:
            return match[0]
        target = (source.parent / unquote(href.path)).resolve()
        if not target.is_relative_to(root) or target not in public:
            raise ValueError("Wiki link is not a public source file in " + source.name + ": " + href.path)
        if target.parent == wiki and target.name in FILES:
            url = repo_url + "/wiki/" + quote(target.stem, safe="")
        else:
            name = quote(target.relative_to(root).as_posix(), safe="/")
            if match[1].startswith("!"):
                url = "https://raw.githubusercontent.com/" + repository + "/" + branch + "/" + name
            else:
                url = repo_url + "/blob/" + branch + "/" + name
        if href.query:
            url += "?" + href.query
        if href.fragment:
            url += "#" + quote(unquote(href.fragment), safe="-_.~")
        return match[1] + url + match[3]

    lines, fence = [], None
    for line in content.splitlines(keepends=True):
        marker = FENCE.match(line)
        if marker and fence is None:
            fence = marker[1]
        elif marker and fence and marker[1][0] == fence[0] and len(marker[1]) >= len(fence) and not marker[2].strip():
            fence = None
        elif fence is None:
            line = LINK.sub(replace, line)
        lines.append(line)
    return "".join(lines)


def build_wiki(root=ROOT, *, repository="phishdestroy/TgWitness", branch="main"):
    root = Path(root).resolve()
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9-]*/[A-Za-z0-9][A-Za-z0-9_.-]*", repository):
        raise ValueError("Repository must be OWNER/REPOSITORY")
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", branch):
        raise ValueError("Branch must be a simple branch name")
    version = tomllib.loads((root / "pyproject.toml").read_text(encoding="utf-8"))["project"]["version"]
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9.+-]*", version):
        raise ValueError("Invalid package version")
    public = set(public_sources(root))
    rendered = {}
    for name in FILES:
        source = root / "docs/wiki" / name
        if source not in public or source.resolve() != source:
            raise ValueError("Missing or linked wiki input: " + name)
        rendered[name] = render_links(source.read_text(encoding="utf-8"), source, root, public, repository, branch)

    output = root / "dist/wiki"
    archive_path = root / "dist" / ("TgWitness-" + version + "-wiki.zip")
    checksum_path = archive_path.with_suffix(".zip.sha256")
    manifest_path = root / "dist/wiki-manifest.json"
    # Fail before writing if the output contains unrelated data or filesystem links.
    if output.resolve() != output or (output.exists() and not output.is_dir()):
        raise ValueError("Wiki output must be an ordinary directory")
    if output.exists():
        for path in output.iterdir():
            if path.resolve() != path or not path.is_file() or path.name not in FILES:
                raise ValueError("Unexpected or linked wiki output: " + path.name)
    for path in (archive_path, checksum_path, manifest_path):
        if path.resolve() != path or (path.exists() and not path.is_file()):
            raise ValueError("Wiki artifact must be an ordinary file: " + path.name)
    output.mkdir(parents=True, exist_ok=True)
    hashes = {}
    with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, content in rendered.items():
            data = content.encode("utf-8")
            (output / name).write_bytes(data)
            archive.writestr(name, data)
            hashes[name] = hashlib.sha256(data).hexdigest()
    digest = hashlib.sha256(archive_path.read_bytes()).hexdigest()
    checksum_path.write_text(digest + "  " + archive_path.name + "\n", encoding="utf-8")
    manifest = {
        "format": "tgwitness-wiki-bundle-v1", "repository": repository,
        "source_branch": branch, "version": version, "language": "en",
        "pages": len(PAGES), "files": hashes, "archive": archive_path.name, "sha256": digest,
    }
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", default=os.environ.get("GITHUB_REPOSITORY") or "phishdestroy/TgWitness")
    parser.add_argument("--branch", default="main")
    args = parser.parse_args()
    try:
        result = build_wiki(repository=args.repository, branch=args.branch)
    except (ValueError, OSError) as exc:
        parser.exit(1, "Wiki build failed: " + str(exc) + "\n")
    print(f"Built {result['pages']} English pages plus sidebar/footer in {ROOT / 'dist/wiki'}")
    print("Wiki archive:", ROOT / "dist" / result["archive"])
    print("SHA-256:", result["sha256"])


if __name__ == "__main__":
    main()
