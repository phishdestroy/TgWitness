![TgWitness investigation presentation](brand.svg)

# Investigation presentation kit

The shared visual system for the repository and wiki: midnight blue, ice-blue
headings, warm connection lines and the original TgWitness application mark.
The approved investigation artwork was generated with Gemini; captions, typography
and animation are SVG elements. The artwork illustrates a workflow, not an app screen.

| Asset | Purpose |
| --- | --- |
| [README hero](readme-hero.svg) | Compact animated repository cover |
| [Shared brand cover](brand.svg) | Reduced-motion README alternative and translated introductions |
| [Investigation artwork](tgwitness-investigation-static.svg) | Full-size static composition |
| [Animated investigation](tgwitness-investigation-animated.svg) | Extended investigation sequence |
| [Mobile cover](mobile.svg) | Legible narrow-screen composition |
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

Use relative links inside the repository. The wiki builder copies referenced images
into the separate Wiki repository and rewrites their links. Keep captions in image
alt text too; never replace essential instructions with an image.

The SVGs are self-contained and contain no JavaScript. Headings and captions are
outlined from Manrope for consistent rendering. The font licence is retained in
[OFL-Manrope.txt](OFL-Manrope.txt). Review animation as an ordinary image, both
themes and a narrow viewport before replacing an asset.

The original artwork and renderer remain documented in [launch-kit](../launch-kit/README.md).

## Films and animations

[Watch the gallery](../../SHOWCASE.md). Both films are silent H.264 MP4s, with GIF
alternatives, using fictional records. These are the original presentation exports,
copied without recompression. They illustrate concepts rather than record a live account.

README, gallery and wiki show GIF previews and provide the MP4 originals alongside
them. Both formats are stored in the repository. With reduced motion, the README
and gallery show a still instead: the static investigation artwork and
[`message-history-static.png`](message-history-static.png), a frame of the finished
sequence. Only the four named films are allowed by the publication builder; replacing
one means replacing its MP4, GIF and still together.

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
