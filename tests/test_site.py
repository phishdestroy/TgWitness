"""Publication boundary checks: the Pages artifact must never include live data."""
import shutil
import json
from html.parser import HTMLParser
from urllib.parse import unquote, urljoin, urlsplit
import xml.etree.ElementTree as ET

import pytest

from tools.build_site import INPUTS, LANGS, LOCAL_PAGES, PAGES, ROOT, SEARCH_FILES, STATIC, TRANSLATIONS, build_site
from tools.site_i18n import LANGUAGES


@pytest.fixture
def site_root(tmp_path):
    for name in ("pyproject.toml", *INPUTS, *TRANSLATIONS):
        if name in TRANSLATIONS and not (ROOT / name).exists():
            continue  # a language not translated yet falls back to English
        target = tmp_path / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / name, target)
    return tmp_path


def test_pages_uses_only_presentation_files_and_project_relative_assets(site_root):
    for name in ("data/live/panel-token.txt", "website/credentials.enc", "docs/assets/account.session"):
        path = site_root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("synthetic-private-data", encoding="utf-8")
    output = build_site(site_root, repository="example/Journal")
    assert {p.relative_to(output).as_posix() for p in output.rglob("*") if p.is_file()} == {
        *(page + "index.html" for page in PAGES), *SEARCH_FILES, *STATIC, ".nojekyll", "sitemap.xml", "robots.txt",
    }
    content = (output / "index.html").read_text(encoding="utf-8")
    assert "https://example.github.io/Journal/" in content
    assert 'src="assets/workspace.png"' in content
    assert 'src="../assets/workspace.png"' in (output / "ru/index.html").read_text(encoding="utf-8")
    assert "https://github.com/example/Journal.git" in content
    assert "@@" not in content
    assert all(b"synthetic-private-data" not in p.read_bytes() for p in output.rglob("*") if p.is_file())


def test_existing_unexpected_output_blocks_publication(site_root):
    output = build_site(site_root)
    (output / "account.session").write_text("synthetic", encoding="utf-8")
    with pytest.raises(ValueError, match="Unexpected file"):
        build_site(site_root)


def test_site_rejects_linked_source(site_root, tmp_path):
    asset = site_root / "docs/assets/workspace.png"
    secret = tmp_path / "private.txt"
    secret.write_text("synthetic", encoding="utf-8")
    asset.unlink()
    try:
        asset.symlink_to(secret)
    except OSError:
        pytest.skip("Filesystem cannot create symlinks")
    with pytest.raises(ValueError, match="ordinary repository file"):
        build_site(site_root)


@pytest.mark.parametrize("repository", ["../private", "owner/repo/extra", 'owner/repo\"', "owner/repo?x"])
def test_invalid_repository_cannot_generate_links(site_root, repository):
    with pytest.raises(ValueError, match="OWNER/REPOSITORY"):
        build_site(site_root, repository=repository)


def test_custom_domain_and_user_pages_have_correct_canonical(site_root):
    output = build_site(site_root, repository="example/example.github.io")
    assert '<loc>https://example.github.io/</loc>' in (output / "sitemap.xml").read_text()
    output = build_site(site_root, base_url="https://watch.example.org")
    assert 'href="https://watch.example.org/"' in (output / "index.html").read_text(encoding="utf-8")


@pytest.mark.parametrize("base_url", ["javascript:alert(1)", "https://user:pass@example.org", "https://example.org/?token=private"])
def test_invalid_site_url_is_rejected(site_root, base_url):
    with pytest.raises(ValueError, match="HTTPS site URL"):
        build_site(site_root, base_url=base_url)


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.tags = []
        self.scripts = []
        self.ids = []
        self.title = ""
        self.h1 = ""
        self.active = None
        self.script = ""
        self.feed(path.read_text(encoding="utf-8"))

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append((tag, attrs))
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if tag in ("title", "h1"):
            self.active = tag
        if tag == "script" and attrs.get("type") in ("application/ld+json", "application/json"):
            self.active, self.script = "json", ""

    def handle_data(self, data):
        if self.active == "json":
            self.script += data
        elif self.active:
            setattr(self, self.active, getattr(self, self.active) + data)

    def handle_endtag(self, tag):
        if tag == "script" and self.active == "json":
            self.scripts.append(json.loads(self.script))
            self.active = None
        elif tag == self.active:
            self.active = None

    def find(self, tag, **attrs):
        return [data for name, data in self.tags if tag == name and all(data.get(k) == v for k, v in attrs.items())]


@pytest.mark.parametrize("base_url", ["https://example.github.io/Journal", "https://watch.example.org"])
def test_every_page_has_distinct_metadata_and_valid_links(site_root, base_url):
    output = build_site(site_root, repository="example/Journal", base_url=base_url)
    pages = {base_url + "/" + path: Page(output / path / "index.html") for path in PAGES}
    assert len(pages) == len(PAGES) == len(LANGS) * len(LOCAL_PAGES) == 13 * 31
    for lang in LANGS:
        prefix = "" if lang == "en" else lang + "/"
        local = [pages[base_url + "/" + prefix + path] for path in LOCAL_PAGES]
        assert len({page.title for page in local}) == len(local), lang
        assert len({page.find("meta", name="description")[0]["content"] for page in local}) == len(local), lang
    for url, page in pages.items():
        path = url.removeprefix(base_url + "/")
        lang = path.split("/")[0] if path.split("/")[0] in LANGUAGES and "/" in path else "en"
        local = path.removeprefix(lang + "/") if lang != "en" else path
        assert page.h1, url
        assert len(page.find("h1")) == 1, url
        assert len(page.ids) == len(set(page.ids)), url
        assert page.find("link", rel="canonical") == [{"rel": "canonical", "href": url}]
        assert page.find("meta", property="og:url")[0]["content"] == url
        html_tag = page.find("html")[0]
        assert html_tag["lang"] == LANGUAGES[lang][1] and html_tag["dir"] == LANGUAGES[lang][2], url
        # Every page names all of its language versions, and each of them exists.
        alternates = {a["hreflang"]: a["href"] for a in page.find("link", rel="alternate")}
        assert set(alternates) == {LANGUAGES[other][1] for other in LANGS} | {"x-default"}, url
        assert alternates["x-default"] == base_url + "/" + local
        assert all(href in pages for href in alternates.values()), url
        graphs = [script["@graph"] for script in page.scripts if "@graph" in script]
        assert len(graphs) == 1
        assert graphs[0][0]["@id"] == url
        for item in graphs[0]:
            assert "aggregateRating" not in item and "review" not in item
            for crumb in item.get("itemListElement", []):
                assert crumb["item"] in pages
        for tag, attrs in page.tags:
            for attr in ("href", "src"):
                href = attrs.get(attr)
                if not href:
                    continue
                resolved = urlsplit(urljoin(url, href))
                if resolved.netloc != urlsplit(base_url).netloc:
                    # Passive assets must stay local, even if navigation is external.
                    assert tag not in ("script", "img", "iframe")
                    continue
                target_url = resolved._replace(fragment="", query="").geturl()
                if target_url in pages:
                    if resolved.fragment:
                        assert unquote(resolved.fragment) in pages[target_url].ids, (url, href)
                else:
                    relative = resolved.path.removeprefix(urlsplit(base_url).path + "/")
                    assert (output / relative).is_file(), (url, href)
    for name in SEARCH_FILES:
        index = json.loads((output / name).read_text(encoding="utf-8"))
        hub = base_url + "/" + name.removesuffix("search.json")
        assert len(index["pages"]) == 28
        for entry in index["pages"]:
            assert urljoin(hub, entry["url"]) in pages
            assert len(entry["text"]) > 300
    sitemap = ET.parse(output / "sitemap.xml")
    assert {node.text for node in sitemap.findall(".//{*}loc")} == set(pages)


def test_unlisted_guide_is_not_published(site_root):
    private = site_root / "website/guides/en/private.html"
    private.write_text("synthetic-private-guide", encoding="utf-8")
    output = build_site(site_root)
    assert all(b"synthetic-private-guide" not in p.read_bytes() for p in output.rglob("*") if p.is_file())


def test_reference_source_links_open_the_document_on_github(site_root):
    """Audit A10: the footer must lead to GitHub, never back to the same rendered page."""
    from tools.build_site import REFERENCE, WIKI_HUB
    output = build_site(site_root, repository="example/Journal")
    checked = 0
    for lang in LANGS:
        prefix = "" if lang == "en" else lang + "/"
        for slug, (_, _, _, source) in REFERENCE.items():
            page = Page(output / (prefix + WIKI_HUB + slug + "/") / "index.html")
            links = [a["href"] for a in page.find("a", **{"class": "reference"})]
            assert links == ["https://github.com/example/Journal/edit/main/" + source], (lang, slug, links)
            checked += 1
    assert checked == len(LANGS) * len(REFERENCE)
