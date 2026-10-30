# Publish the project and website

Publish TgWitness **0.6.1** with the project website and release packages. See
[readiness](READINESS.md) for tested environments and known limitations.

The [investigation presentation kit](../assets/presentation/README.md) contains the
current repository and wiki covers, diagrams and sharing images. Rebuild the
GitHub and website PNGs with `python website/render_presentation.py`. The earlier
[launch kit](../assets/launch-kit/README.md) is retained as legacy artwork.

The [project wiki](../wiki/Home.md) has its own GitHub repository and a separate
[build and publishing procedure](WIKI.md). Run `python tools/build_wiki.py` to prepare
its pages, navigation, ZIP and checksums. The Wiki bundle workflow produces artifacts;
publishing Pages or the main repository does not publish the wiki.

## Preview the website locally

The builder uses Python 3.11+ and the project's Markdown dependency. It does not import the
application, open a journal, connect to Telegram, or require account credentials.

```sh
python tools/build_site.py --repository phishdestroy/TgWitness
python -m http.server 8790 --bind 127.0.0.1 --directory dist/site
```

Open <http://127.0.0.1:8790>. Use the HTTP preview for navigation between pages;
opening a homepage directly from disk can display it, but directory links need a
web server. Copying commands depends on the browser's clipboard permissions.
Stop the preview server with Ctrl+C.

Open `/docs/` for the English guides, `/docs/concepts/` for interactive explanations,
or `/docs/cases/` for practical workflows. The multilingual site includes a screenshot
tour, platform-specific setup, local search, reference documents, diagrams, formulas
and interactive examples. It has no account
form, telemetry, external scripts, fonts or runtime API calls. Content and
navigation remain available without JavaScript. [Metadata and SEO](SEO.md).

## Publish to GitHub

1. Authenticate with `gh auth login` or your Git client, using your own account.
   Never put a GitHub token into a repository file or chat.
2. Create an empty repository with the intended name, for example `phishdestroy/TgWitness`.
   This local project initially had no commits and no configured remote.
3. Review the selected files before the first commit. Runtime data, `.env`, session
   files, keys, logs, builds, and test output must stay ignored. The source packager
   has an allowlist, but Git uses `.gitignore`; those are separate controls.
4. Commit the reviewed source and push `main` to the new remote.
5. In **Settings → Pages → Build and deployment**, choose **GitHub Actions**.
6. Run **Actions → Project website → Run workflow** if the initial push ran before
   Pages was enabled. The workflow checks the site before uploading `dist/site`.

For `phishdestroy/TgWitness`, the default address is
`https://phishdestroy.github.io/TgWitness/`. In Actions, the build derives the owner
and repository from `GITHUB_REPOSITORY`, so forks get their own URLs automatically.
It uses `main` for source links. A different default branch requires updating the
workflow branch filter and passing `--branch NAME` to the builder.

Use the published wiki URL in **About → Website** while Pages is unavailable. After
a successful Pages deployment, the documentation website can replace it there.
Suggested About description:

> A self-hosted Telegram investigation workspace. Capture conversations, preserve
> observed changes, trace connections, and share independently verifiable records.

Suggested topics: `telegram`, `telethon`, `self-hosted`, `python`, `fastapi`,
`digital-forensics`, `osint`, `investigation-tools`, `evidence`, `cryptography`.

Pull requests build and test the site, but cannot deploy it. Only the deploy job has
`pages: write` and `id-token: write`; no personal token is needed for Pages.
A workflow definition is not evidence of a successful hosted run.

## What gets published to Pages

The builder copies only these assets into `dist/site`:

- The homepage, guide index, explicitly listed guides and reference documents in
  the languages declared by the website builder.
- The presentation styles and scripts from `website/`.
- The application logo and explicitly listed synthetic workspace screenshots and diagrams.
- The social-preview image from `docs/assets/presentation/preview-social.png`.
- `.nojekyll`, `robots.txt`, and `sitemap.xml`.

It rejects linked inputs and unexpected files already present in the output.
`data/`, account files, the Python backend, and tests never enter the site artifact.
Do not change the Pages upload path to the repository root.

An optional Actions variable `TGWITNESS_SITE_URL` sets the canonical URL for a custom
domain. Configure the domain and DNS in GitHub Pages separately; the variable alone
does not configure hosting or DNS.

## Check before publication

From the project environment:

```sh
python -m pytest -q
python tools/check_publication.py --git-index
python tools/build_site.py
python tools/check_site.py
python tools/check_docs_site.py
python tools/check_browser.py
python tools/check_account_browser.py
python tools/check_interactions_browser.py
python tools/check_workspace_browser.py
python tools/check_quick_browser.py
python tools/build_source.py
```

Browser checks require Playwright Chromium (`python -m playwright install chromium`).
The publication check scans the public source allowlist for recognizable secret formats
and checks that local Markdown link targets are included. With `--git-index`, it also
scans the staged text, rejects non-public paths and unresolved merges, and requires every
public file to be staged with the reviewed contents. Normal Git line-ending conversion
is allowed. New files and edits made after staging cause a failure until the index is
updated. The check does not stage files or change Git configuration.

Run it without `--git-index` while editing; run it with that flag after staging the
reviewed publication set. It reports filenames and line numbers without printing matching
secrets. This is a bounded format check, not a scan of historical commits. Review the
staged diff before committing, including newly added files. Local account-inspection
scripts such as `_inspect_live.py` are outside the public allowlist and must stay local.

CI also runs [pip-audit](https://github.com/pypa/pip-audit) against all runtime pins in
`constraints.txt`, with strict dependency collection. Audit results are attached to the run;
known vulnerabilities or incomplete collection fail the job and block the release checks.

The site check uses a temporary loopback server, blocks external requests, and checks
project-subpath assets, keyboard navigation, clipboard refusal, narrow layouts, and
the no-JavaScript fallback. The guide check covers search, all guide layouts from
320 to 1440 pixels, playback/pause, reduced motion, hash calculations independently
checked with Python, witness decisions, chart/table agreement and the investigation
map's account/link/file references. Screenshots go into
ignored `test-results/site/` and `test-results/docs-site/`.

If a workspace drive cannot maintain Playwright's download lock on Windows, set
`PLAYWRIGHT_BROWSERS_PATH` to a directory on a local disk before installing and
running browser checks. Use the same value for both commands.

## Releases

Publish the first release tagged `v0.6.1` after repository
checks succeed. The existing release workflow verifies the version, runs checks,
and builds source, wheel, Windows portable, and GHCR artifacts.
Release downloads do not exist until those jobs complete. The website provides
source-install instructions and links to the release listing instead of assuming
that a `latest` release or a portable binary already exists.

Publishing the site does not deploy a collector, expose the local panel, or start
observation on any account.
