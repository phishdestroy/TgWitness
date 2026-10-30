"""Render the product's own UI and artwork into shareable PNG files. No network."""
import argparse
import os
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]


def main():
    formats = {"cover": (1600, 640), "cover-ru": (1600, 640),
               "social": (1200, 630), "github": (1280, 640),
               "square": (1080, 1080), "workflow": (1600, 500)}
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--format", action="append", choices=formats,
                        help="Render selected formats; repeat to select more than one")
    args = parser.parse_args()
    output = ROOT / "docs/assets/launch-kit"
    output.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True, channel=os.environ.get("TGWITNESS_BROWSER_CHANNEL") or None)
        page = browser.new_page(reduced_motion="reduce", device_scale_factor=1)
        errors = []
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.route("http://**/*", lambda route: route.abort())
        page.route("https://**/*", lambda route: route.abort())
        for name in args.format or ("cover", "social", "github", "square", "workflow"):
            width, height = formats[name]
            page.set_viewport_size({"width": width, "height": height})
            query = "cover&lang=ru" if name == "cover-ru" else "social" if name == "github" else name
            page.goto((ROOT / "website/artwork.html").as_uri() + "?format=" + query)
            page.wait_for_function("[...document.images].every(image => image.complete && image.naturalWidth > 0)")
            page.evaluate("document.fonts.ready")
            target = output / ("tgwitness-" + name + ".png")
            page.screenshot(path=str(target))
            print(target)
        assert not errors, errors
        browser.close()


if __name__ == "__main__":
    main()
