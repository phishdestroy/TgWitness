import argparse
import hashlib
import json
from pathlib import Path
import shutil
import tempfile

from ..verify import (assurance, bounded_lines, cross_check_witness, open_archive, parse_time, safe_text,
                      verify_bundle, verify_witness)
from ..store import canonical
from .model import build, Limit
from dataclasses import asdict
from .render import write
from .text import LANGUAGES


def generate(package, out, lang='en', jurisdiction=None, fingerprint=None, witness=None,
             witness_fingerprint=None, check_drand=False, check_bitcoin=False, tsa_ca=None):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    if out.is_symlink() or any(out.iterdir()):
        raise ValueError('Narrative output must be an ordinary empty directory')
    with tempfile.TemporaryDirectory(prefix='.narrative-', dir=out) as scratch:
        scratch = Path(scratch)
        source = scratch / 'source.zip'
        shutil.copyfile(package, source)
        result = verify_bundle(source, fingerprint, tsa_ca=tsa_ca, check_drand=check_drand, check_bitcoin=check_bitcoin)
        if witness:
            other = scratch / 'witness.zip'
            shutil.copyfile(witness, other)
            checked = verify_witness(other, witness_fingerprint, check_drand, check_bitcoin)
            result['witness'] = cross_check_witness(checked, source, result)
        result['assurance'] = assurance(result)
        if any(row['status'] == 'fail' for row in result['assurance']['ladder']):
            raise ValueError('Contradictory evidence cannot produce a successful narrative')
        with open_archive(source) as archive, archive.open('events.jsonl') as stream:
            events = []
            for line in bounded_lines(stream):
                if len(events) >= 100000:
                    raise ValueError('Narrative is limited to 100000 records; select a smaller signed package')
                events.append(json.loads(line))
        model = build(events, result)
        if not fingerprint:
            model['limits'].append(asdict(Limit('assurance.state', {'tier': 'signer_pinned', 'status': 'absent'})))
        if witness:
            with open_archive(other) as archive, archive.open('events.jsonl') as stream:
                witness_events = []
                for line in bounded_lines(stream):
                    if len(witness_events) >= 100000:
                        raise ValueError('Witness narrative exceeds the 100000-record limit')
                    witness_events.append(json.loads(line))
            witness_model = build(witness_events, checked, journal='witness')
            model['scenes'] += witness_model['scenes']
            model['scenes'].sort(key=lambda s: (parse_time(s['at_from']), s['journal'], s['from_seq']))
            model['witness_source'] = witness_model['source']
            with other.open('rb') as stream:
                model['witness_source']['package_sha256'] = hashlib.file_digest(stream, 'sha256').hexdigest()
        model['model_sha256'] = hashlib.sha256(canonical(model['scenes'])).hexdigest()
        with source.open('rb') as stream:
            model['package_sha256'] = hashlib.file_digest(stream, 'sha256').hexdigest()
        rendered = scratch / 'rendered'
        write(model, rendered, lang, jurisdiction)
        for file in rendered.iterdir():
            file.rename(out / file.name)
    return model


def main():
    parser = argparse.ArgumentParser(description='Build a source-linked narrative from a verified evidence journal')
    parser.add_argument('package', type=Path)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--lang', choices=LANGUAGES, default='en')
    parser.add_argument('--jurisdiction')
    parser.add_argument('--fingerprint')
    parser.add_argument('--witness', type=Path)
    parser.add_argument('--witness-fingerprint')
    parser.add_argument('--check-drand', action='store_true')
    parser.add_argument('--check-bitcoin', action='store_true')
    parser.add_argument('--tsa-ca', type=Path)
    args = parser.parse_args()
    try:
        generate(**vars(args))
    except Exception as exc:
        parser.exit(1, safe_text(type(exc).__name__ + ': ' + str(exc)) + '\n')
    print(str(args.out))


if __name__ == '__main__':
    main()
