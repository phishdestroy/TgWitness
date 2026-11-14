import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).parent / 'examination'
FORMAT = 'tgwitness-examination-v1'
PROCEDURES = ('criminal', 'civil')
ALIASES = {'US': 'US-federal', 'GB-EW': 'UK'}


def codes():
    return {path.stem for path in ROOT.glob('*.json')}


def load(code):
    code = ALIASES.get(code, code)
    if code is None or code not in codes():
        return None
    raw = (ROOT / (code + '.json')).read_bytes()
    record = json.loads(raw)
    if record.get('format') != FORMAT or record.get('code') != code:
        raise ValueError('Invalid examination catalog entry: ' + code)
    record['catalog_sha256'] = hashlib.sha256(raw).hexdigest()
    return record


def available_routes(record):
    return [part for part in record.get('procedures', [])
            if any((part.get(key) or {}).get('source') and (part[key].get('basis') or part[key].get('items_en'))
                   for key in ('appointment', 'questions', 'report_contents', 'rights_duties'))]


def route(record, procedure, scope=None):
    matches = [item for item in available_routes(record) if item.get('route') == procedure]
    if scope is not None:
        matches = [item for item in matches if item.get('id') == scope]
        if not matches:
            raise ValueError('Unknown procedure scope for ' + record['code'] + ': ' + scope)
    if len(matches) > 1:
        choices = ', '.join(item.get('id') or item.get('scope') or procedure for item in matches)
        raise ValueError('Choose a procedure_scope for ' + record['code'] + ': ' + choices)
    return matches[0] if matches else {}


def liability(record, procedure, scope=None):
    return [row for row in record.get('liability', []) if row.get('route') in (procedure, 'all')
            and (not row.get('procedure_ids') or scope in row['procedure_ids'])]


def declaration(record, procedure, scope=None):
    found = record.get('declaration_criminal') if procedure == 'criminal' else None
    found = found or record.get('declaration')
    if (found and found.get('route') in ('all', procedure)
            and (not found.get('procedure_ids') or scope in found['procedure_ids'])):
        return found
    return None
