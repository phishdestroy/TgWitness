# Presentation assets

The repository and handbook share navy backgrounds, blue and gold accents,
outlined type and animated record diagrams. Application screenshots use
fictional demo data. Diagrams illustrate behavior; they are not screenshots.

[Documentation assets](../README.md) · [Illustrated reference](../../SHOWCASE.md)

## Current assets

| Files | Purpose |
| --- | --- |
| `casework-hero*`, `casework-handbook*` | Repository and handbook covers |
| `casework-nav-*`, `identity-action-*` | Demo, installation, account and deployment links |
| `readme-features*`, `readme-feature-*` | Chat export, investigation and saved-version diagrams |
| `readme-workspace-*.webp` | Demo recording in both themes, with desktop, phone and still variants |
| `casework-chain*`, `casework-tamper*`, `casework-checkpoint*` | Signatures, changed records and retained checkpoints |
| `readme-services*`, `readme-card-*` | Notifications and encrypted off-site storage |
| `readme-handbook*`, `wiki-*` | Handbook navigation and chapter covers |
| `readme-button-*`, `readme-divider*`, `identity-meta-*` | Links, section rules and project metadata |
| `preview-github.png`, `preview-social.png` | Repository and website sharing images |

## Rebuild

Run from the repository root with `fonttools` installed. Supply local
[Space Grotesk](OFL-SpaceGrotesk.txt) and [Manrope](OFL-Manrope.txt) font files:

```sh
python website/render_casework.py --display-font /path/to/SpaceGrotesk.ttf --text-font /path/to/Manrope.ttf
python website/render_readme_panels.py --font /path/to/Manrope.ttf
python website/render_wiki_headers.py --font /path/to/Manrope.ttf
python website/render_identity.py --font /path/to/Manrope.ttf
```

`render_identity.py` reads the version from `pyproject.toml`. Rebuild metadata
badges when the version changes. SVGs contain no scripts or remote fonts.

With Playwright Chromium installed, refresh the demo recording and sharing images:

```sh
python tools/build_site.py
python website/capture_readme.py
python website/render_presentation.py
```

The capture script opens the local demo and records its interface. It does not
connect a Telegram account. The preview renderer uses the static casework cover.
Upload `preview-github.png` under **Settings → Social preview**; the website
builder includes `preview-social.png` automatically.

## Embed and review

Use relative image paths. Each animated `<picture>` needs a separate still source
for `prefers-reduced-motion: reduce`. Where a phone composition exists, put the
combined narrow-screen/reduced-motion source first. Keep labels stable during
animation and include meaningful alt text.

Review the page at desktop and phone widths, in both themes, with motion enabled
and reduced. Check that navigation fits the README content column and that
essential instructions remain readable without images. Run
`python tools/check_publication.py` to check Markdown links, HTML links and image
sources. The wiki builder copies referenced images into its separate bundle.

## Retained artwork

Earlier `identity-*`, `technical-*`, `repository-*`, `case-*`, `entry-*`, `nav-*`
and `readme-cover*` compositions remain for existing references. Their renderers
are in `website/`. The [original launch kit](../launch-kit/README.md) documents
the Gemini-generated dossier artwork and its provenance.

The MP4/GIF concept films also remain as source assets. Current README and wiki
pages use inline illustrations with still alternatives.
