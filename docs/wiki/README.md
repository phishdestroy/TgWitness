![Wiki source](../assets/presentation/folder-docs-wiki.svg)

# Wiki source

[Project](../../README.md) · [Documentation](../README.md) · [Wiki](Home.md) · [Support](../../SUPPORT.md)

Start with [Wiki home](Home.md). These Markdown files are the English source for the
separate GitHub Wiki; they also remain readable inside the main repository.

## Reading paths

| Goal | Guides |
| --- | --- |
| First capture | [Getting started](Getting-Started.md) → [Accounts](Accounts.md) → [Collection](Collection.md) |
| Investigation and handoff | [Investigations](Investigations.md) → [Exports and verification](Exports-and-Verification.md) |
| Reliable operation | [Proxies](Proxies.md), [Server and Docker](Server-and-Docker.md), [Backup and recovery](Backup-and-Recovery.md) |
| Independent checks | [Witness and Proof](Witness-and-Proof.md) |
| Find an answer | [Troubleshooting](Troubleshooting.md), [FAQ](FAQ.md), [Glossary](Glossary.md) |

## Maintain the wiki

`_Sidebar.md` and `_Footer.md` provide shared navigation. The explicit 13-page bundle
is built by [`tools/build_wiki.py`](../../tools/build_wiki.py); this directory README
is a repository index, not an additional published wiki page.

```sh
python tools/build_wiki.py
```

Run from the project root. The [maintenance guide](../internal/WIKI.md) covers
checks, link conversion and publication to the separate wiki repository.
