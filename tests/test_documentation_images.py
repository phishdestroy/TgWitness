from pathlib import Path

from tools import site_wiki
from tools.check_publication import check_sources, documentation_links
from tools.build_source import FILES


def test_responsive_illustration_survives_site_rendering():
    source = '''<picture>
  <source media="(prefers-reduced-motion: reduce)" srcset="assets/still.svg">
  <source media="(max-width: 640px)" srcset="assets/mobile.svg">
  <img src="assets/animated.svg" alt="Captured message and its saved edit">
</picture>

Use <version> for the release number.
'''
    body, _, _ = site_wiki.to_html(source)
    assets = {}
    result = site_wiki.rewrite_links(
        body, "docs/README.md", "docs/reference/", {}, {},
        lambda page, asset: "../../" + asset,
        "https://github.com/example/project", "main", assets, Path("."),
    )
    assert "<picture>" in result and "</picture>" in result
    assert "&lt;version&gt;" in result
    for name in ("still", "mobile", "animated"):
        assert f'="../../assets/{name}.svg"' in result
        assert assets[f"assets/{name}.svg"] == f"docs/assets/{name}.svg"


def test_srcset_preserves_density_descriptors_and_external_urls():
    assets = {}
    result = site_wiki.rewrite_links(
        '<img srcset="images/small.png 1x, images/large.png 2x, https://example.org/huge.png 3x">',
        "docs/README.md", "docs/", {}, {}, lambda page, asset: "../" + asset,
        "https://github.com/example/project", "main", assets, Path("."),
    )
    assert 'srcset="../assets/small.png 1x, ../assets/large.png 2x, https://example.org/huge.png 3x"' in result
    assert len(assets) == 2


def test_publication_finds_missing_html_images_and_buttons(tmp_path):
    for name in FILES:
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("Synthetic source\n", encoding="utf-8")
    (tmp_path / "README.md").write_text(
        '<picture>\n<source srcset="docs/missing-still.svg">\n'
        '<img src="docs/missing-cover.svg">\n</picture>\n'
        '<a href="docs/missing-guide.md">Guide</a>\n', encoding="utf-8")
    _, links, findings = check_sources(tmp_path)
    assert links == 3
    assert len(findings) == 3
    assert findings[0].endswith("docs/missing-still.svg")
    assert findings[1].endswith("docs/missing-cover.svg")
    assert findings[2].endswith("docs/missing-guide.md")


def test_publication_ignores_code_examples_but_checks_real_picture_sources():
    content = '''```html
<img src="example.png">
```
`<a href="example.md">Example</a>`
~~~markdown
[Example](example.md)
~~~
<source srcset="small.png 1x, large.png 2x">
'''
    assert documentation_links(content) == [("small.png", 8), ("large.png", 8)]
