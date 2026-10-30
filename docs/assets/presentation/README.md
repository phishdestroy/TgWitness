![TgWitness investigation presentation](brand.svg)

# Investigation presentation kit

The shared visual system for the repository and wiki: midnight blue, ice-blue
headings, warm connection lines and the original TgWitness application mark.
The approved investigation artwork was generated with Gemini; captions, typography
and animation are SVG elements. The artwork illustrates a workflow, not an app screen.

| Asset | Purpose |
| --- | --- |
| `readme-product-{light,dark}.png` | README opening: project identity and a crop of the actual fictional Chats workspace |
| `readme-product-mobile-{light,dark}.png` | Mobile composition with a closer view of the conversation |
| [Repository cover](readme-cover.svg), [static cover](readme-cover-static.svg), [mobile cover](readme-cover-mobile.svg) | Compact TgWitness masthead with the original animated investigation scene and reduced-motion alternative |
| [Workspace preview, light](workspace-preview-light.png), [dark](workspace-preview-dark.png) | Framed, unmodified Chats screenshots with fictional demo data |
| `nav-*.svg` | Four equal-width navigation buttons; two per row on narrow screens |
| [README hero](readme-hero.svg) | Compact animated repository cover |
| [Shared brand cover](brand.svg) | Reduced-motion README alternative and translated introductions |
| [Investigation artwork](tgwitness-investigation-static.svg) | Full-size static composition |
| [Animated investigation](tgwitness-investigation-animated.svg) | Extended investigation sequence |
| [Investigation overview film](investigation-overview.mp4) | The illustrated SVG sequence as a 12-second, 1280 × 720 MP4 |
| [Mobile cover](mobile.svg) | Legible narrow-screen composition |
| [Capability cards](capabilities.svg), [mobile cards](capabilities-mobile.svg) | Collection, captured versions, investigation and verification |
| [Film navigation](button-films.svg) | Direct access to the films and animation gallery |
| [Investigation film](investigation.mp4), [GIF](investigation.gif) | 12-second concept film, 1280 × 672 MP4 |
| [Message history film](message-history.mp4), [GIF](message-history.gif), [still](message-history-static.png) | 12-second concept film, 1280 × 576 MP4 |
| [GitHub preview](preview-github.png) | 1280 × 640 repository sharing image |
| [Website preview](preview-social.png) | 1200 × 630 Open Graph image |
| [Workflow](workflow.svg) | Observe → Preserve → Verify |
| `evidence-*-animated.svg` | Record chain, changed content and retained checkpoint explanations |
| `evidence-*-static.svg` | Static alternatives to the three explanations |
| `wiki-*.svg` | Individual wiki covers |
| `folder-*.svg` | Directory introductions |
| [Divider](divider.svg), `button-*.svg` | Shared section and navigation elements |

## Use and maintenance

The main README combines its title and actual workspace in one opening image.
Its `picture` selects a matching light/dark and desktop/mobile composition. Both
native video players follow the introduction; playback is user-controlled.
Additional screenshots and the source map expand on demand. The earlier animated
covers remain available for other project pages, with separate static alternatives.

Rebuild the current README images with `python website/render_readme.py`.
For the committed Manrope typography, pass `--font /path/to/Manrope.ttf`; the font
licence is retained below. Without a font file, the renderer uses Arial. It uses
only the existing fictional-data screenshots and the application mark; it blocks
network requests. The mobile image crops the desktop capture without changing its
content. The full captures remain linked from the README.

Use relative links inside the repository. The wiki builder copies referenced images
into the separate Wiki repository and rewrites their links. Keep captions in image
alt text too; never replace essential instructions with an image.

The SVGs are self-contained and contain no JavaScript. Headings and captions are
outlined from Manrope for consistent rendering. The font licence is retained in
[OFL-Manrope.txt](OFL-Manrope.txt). Review animation as an ordinary image, both
themes and a narrow viewport before replacing an asset.

The original artwork and renderer remain documented in [launch-kit](../launch-kit/README.md).

## Films and animations

[Watch the gallery](../../SHOWCASE.md). All three films are silent H.264 MP4s using
fictional records. The investigation overview renders the illustrated SVG sequence
at 24 frames per second. The two earlier concept films retain their original exports
and GIF alternatives. These films illustrate the workflow; they are not recordings
of a live account.

README, gallery and wiki use GitHub's video players with playback controls and no
autoplay. Each has a download link to its versioned MP4. To replace a film, upload
the new MP4 as a repository attachment and update both the player URL and the
versioned file. The publication builder allows only these three MP4s and the two
named GIFs. SVG animations keep their static reduced-motion alternatives; the
message-history still is [`message-history-static.png`](message-history-static.png).

## Preview images

Both PNGs are rendered from the static investigation artwork, with the same
illustration and outlined typography as the repository. From the development
environment with Playwright Chromium installed:

```sh
python website/render_presentation.py
```

Use `--format github` or `--format social` to render one image. The renderer blocks
network requests and does not open the application or account data.

The website builder includes `preview-social.png` automatically. GitHub's repository
sharing image is a separate setting: upload `preview-github.png` under
**Settings → Social preview → Edit → Upload an image**. It follows
[GitHub's recommended dimensions and file limit](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/customizing-your-repositorys-social-media-preview).
