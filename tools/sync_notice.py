"""Render the maintainer's NOTICE consistently across documentation; no network access."""
import argparse
import html
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
START = '<!-- operator-notice:start -->'
END = '<!-- operator-notice:end -->'
SOURCE = 'https://phishdestroy.io/steam_dossier/taylor_wessing'


def statement(root):
    source = (root / 'NOTICE').read_text(encoding='utf-8')
    parts = source.split('=' * 64)
    if len(parts) != 4 or parts[1].strip() != 'NOTICE — Operator Incompatibility':
        raise ValueError('NOTICE must contain the named statement between its original separators')
    return parts[2].strip()


def quoted_html(text):
    """Preserve wording; use paragraphs and lists instead of a fixed-width text box."""
    blocks = []
    for paragraph in re.split(r'\n\s*\n', text):
        lines = paragraph.splitlines()
        if any(line.lstrip().startswith('—  ') for line in lines):
            title, entries = [], []
            for line in lines:
                if line.lstrip().startswith('—  '):
                    entries.append(line.lstrip()[3:].strip())
                elif entries:
                    entries[-1] += ' ' + line.strip()
                else:
                    title.append(line.strip())
            blocks.append('<p>' + html.escape(' '.join(title)) + '</p>')
            blocks.append('<ul>' + ''.join('<li>' + html.escape(item) + '</li>' for item in entries) + '</ul>')
        elif lines[0].strip() == 'Including, without limitation:':
            blocks.append('<p>Including, without limitation:</p>')
            blocks.append('<ul>' + ''.join('<li>' + html.escape(' '.join(line.split())) + '</li>' for line in lines[1:]) + '</ul>')
        else:
            blocks.append('<p>' + html.escape(' '.join(line.strip() for line in lines)) + '</p>')
    return '<blockquote lang="en" dir="ltr" translate="no">\n' + '\n'.join(blocks) + '\n</blockquote>'


def excerpt(full, notice, licence, raw, *, compact=False):
    if compact:
        return f'''## Licence and operator notice

[MIT License]({licence}) · [The maintainer's position on Taylor Wessing](docs/TAYLOR-WESSING-EXCLUSION.md)

> **NOTICE — Operator Incompatibility**
> PhishDestroy's statement concerning **Taylor Wessing PartG mbB — German core, Hamburg office.**
> [Full notice and context]({notice}) · [Original text]({raw}) · [Source record]({SOURCE})

<details>
<summary><strong>Read the complete notice</strong> — statement by PhishDestroy</summary>

<p>The following records the maintainer's statement and allegations, not an independent judicial or regulatory finding. It is the copyright holder's position, not a condition of the MIT License.</p>

{full}

</details>'''
    return f'''### NOTICE — Operator Incompatibility

> **Taylor Wessing PartG mbB — German core, Hamburg office.**
> PhishDestroy's operator notice is the copyright holder's position; TgWitness remains under the [MIT License]({licence}).
> [Full notice and context]({notice}) · [Original text]({raw}) · [Source record]({SOURCE})

The following records the maintainer's statement and allegations, not an
independent judicial or regulatory finding.

<details>
<summary><strong>Read the complete notice</strong> — statement by PhishDestroy</summary>

{full}

</details>'''


def document(full, *, wiki=False):
    prefix = '../' if wiki else ''
    root = '../../' if wiki else '../'
    return f'''# NOTICE — Operator Incompatibility

**Statement by PhishDestroy · TgWitness project notice**

This page records the maintainer's statement and allegations. It does not present
them as independent judicial or regulatory findings. It is the copyright holder's
position, not a licence condition: TgWitness is distributed under the
[MIT License]({root}LICENSE).

[Original NOTICE]({root}NOTICE) · [The maintainer's position]({prefix}TAYLOR-WESSING-EXCLUSION.md) · [Source record]({SOURCE})

## The statement

{full}

## Reading this notice

The quoted material is the maintainer's supplied rationale. The document numbers,
statistics, chronology, historical attribution and characterisations are its
claims; TgWitness does not establish them by producing a signature.

Verification requires an independently trusted public key. A valid signature
can establish integrity relative to that key, not the truth of an input, Telegram
origin, complete capture, or its legal significance in any jurisdiction. See the
[evidence model]({prefix}HOW-IT-WORKS.md) and [security and data handling]({root}.github/SECURITY.md).

The notice adds no runtime access control and no condition to the MIT License.
Third-party components keep their own licences; see the
[scope notes]({prefix}TAYLOR-WESSING-EXCLUSION.md#scope-and-reference-notes).

[Project]({root}README.md) · [Documentation]({prefix}README.md) · [Wiki]({'Home.md' if wiki else 'wiki/Home.md'})
'''


def outputs(root):
    full = quoted_html(statement(root))
    result = {
        'docs/OPERATOR-INCOMPATIBILITY.md': document(full),
        'docs/wiki/Operator-Incompatibility.md': document(full, wiki=True),
    }
    for name, notice, licence, raw in (
        ('README.md', 'docs/OPERATOR-INCOMPATIBILITY.md', 'LICENSE', 'NOTICE'),
        ('.github/SECURITY.md', '../docs/OPERATOR-INCOMPATIBILITY.md', '../LICENSE', '../NOTICE'),
    ):
        source = (root / name).read_text(encoding='utf-8')
        if source.count(START) != 1 or source.count(END) != 1:
            raise ValueError('Exactly one notice slot is required in ' + name)
        before, tail = source.split(START, 1)
        _, after = tail.split(END, 1)
        result[name] = before + START + '\n\n' + excerpt(full, notice, licence, raw, compact=name == 'README.md') + '\n\n' + END + after
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    stale = []
    for name, text in outputs(ROOT).items():
        path = ROOT / name
        if path.exists() and path.read_text(encoding='utf-8') == text:
            continue
        if args.check:
            stale.append(name)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding='utf-8')
    if stale:
        parser.exit(1, 'NOTICE copies need regeneration: ' + ', '.join(stale) + '\n')
    print('NOTICE copies are consistent.' if args.check else 'Updated NOTICE in README, SECURITY, documentation and Wiki.')


if __name__ == '__main__':
    main()
