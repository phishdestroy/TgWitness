import hashlib
import json
import zipfile

import pytest

from tools.build_source import FILES as SOURCE_FILES
from tools.build_wiki import FILES, PAGES, build_wiki


@pytest.fixture
def wiki_tree(tmp_path):
    for name in SOURCE_FILES:
        (tmp_path / name).write_text("Public fixture\n", encoding="utf-8")
    (tmp_path / "pyproject.toml").write_text('[project]\nversion = "1.2.3"\n', encoding="utf-8")
    wiki = tmp_path / "docs/wiki"
    wiki.mkdir(parents=True)
    for name in FILES:
        (wiki / name).write_text("# " + name.removesuffix(".md") + "\n\n[Home](Home.md)\n", encoding="utf-8")
    return tmp_path


def test_wiki_bundle_has_only_reviewed_pages_and_matching_hashes(wiki_tree):
    extra = wiki_tree / "docs/wiki/unreviewed.md"
    extra.write_text("Do not publish this page", encoding="utf-8")
    result = build_wiki(wiki_tree)
    assert result["pages"] == len(PAGES) == 13
    assert result["language"] == "en"
    output = wiki_tree / "dist"
    archive_path = output / result["archive"]
    assert hashlib.sha256(archive_path.read_bytes()).hexdigest() == result["sha256"]
    assert json.loads((output / "wiki-manifest.json").read_text()) == result
    assert archive_path.with_suffix(".zip.sha256").read_text().split()[0] == result["sha256"]
    with zipfile.ZipFile(archive_path) as archive:
        assert set(archive.namelist()) == set(FILES)
        assert {p.name for p in (output / "wiki").iterdir()} == set(FILES)
        for name, digest in result["files"].items():
            data = archive.read(name)
            assert data == (output / "wiki" / name).read_bytes()
            assert hashlib.sha256(data).hexdigest() == digest
    assert extra.read_text() == "Do not publish this page"


def test_wiki_rewrites_page_document_and_image_links_for_forks(wiki_tree):
    (wiki_tree / "docs/reference.md").write_text("# Reference\n", encoding="utf-8")
    assets = wiki_tree / "docs/assets"
    assets.mkdir()
    (assets / "demo.png").write_bytes(b"synthetic image")
    (wiki_tree / "docs/wiki/Home.md").write_text(
        '[Start](Getting-Started.md#install)\n[Reference](../reference.md)\n'
        '![Demo](../assets/demo.png "Fictional data")\n[External](https://example.org/docs)\n'
        '[Section](#section)\n~~~md\n[Example](missing.md)\n~~~\n',
        encoding="utf-8")
    build_wiki(wiki_tree, repository="example/Project", branch="release")
    page = (wiki_tree / "dist/wiki/Home.md").read_text(encoding="utf-8")
    assert "[Start](https://github.com/example/Project/wiki/Getting-Started#install)" in page
    assert "[Reference](https://github.com/example/Project/blob/release/docs/reference.md)" in page
    assert '![Demo](https://raw.githubusercontent.com/example/Project/release/docs/assets/demo.png "Fictional data")' in page
    assert "[External](https://example.org/docs)" in page
    assert "[Section](#section)" in page
    assert "~~~md\n[Example](missing.md)\n~~~" in page


@pytest.mark.parametrize("target", ["missing.md", "../../data/private.md", "../../../outside.md"])
def test_wiki_refuses_missing_or_private_link_targets(wiki_tree, target):
    data = wiki_tree / "docs/data"
    data.mkdir()
    (data / "private.md").write_text("Not public", encoding="utf-8")
    private = wiki_tree / "data"
    private.mkdir()
    (private / "private.md").write_text("Not public", encoding="utf-8")
    (wiki_tree / "docs/wiki/Home.md").write_text("[Bad](" + target + ")\n", encoding="utf-8")
    with pytest.raises(ValueError, match="not a public source file"):
        build_wiki(wiki_tree)
    assert not (wiki_tree / "dist").exists()


def test_wiki_refuses_unrelated_output_without_overwriting_it(wiki_tree):
    output = wiki_tree / "dist/wiki"
    output.mkdir(parents=True)
    (output / "private.txt").write_text("Keep this file", encoding="utf-8")
    (output / "Home.md").write_text("Old reviewed page", encoding="utf-8")
    with pytest.raises(ValueError, match="Unexpected or linked"):
        build_wiki(wiki_tree)
    assert (output / "private.txt").read_text() == "Keep this file"
    assert (output / "Home.md").read_text() == "Old reviewed page"


def test_wiki_requires_every_navigation_page(wiki_tree):
    (wiki_tree / "docs/wiki/FAQ.md").unlink()
    with pytest.raises(ValueError, match="Missing or linked wiki input: FAQ.md"):
        build_wiki(wiki_tree)


@pytest.mark.parametrize("settings", [
    {"repository": "../private"},
    {"repository": "https://github.com/example/project"},
    {"branch": "../../private"},
])
def test_wiki_rejects_invalid_destination_parameters(wiki_tree, settings):
    with pytest.raises(ValueError):
        build_wiki(wiki_tree, **settings)
