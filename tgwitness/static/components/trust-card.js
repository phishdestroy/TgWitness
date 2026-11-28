export function createTrustCard({tr, node, json, busy, toast, formatTime, openJournal}) {
  let serial = 0;
  const COURT_MISSING = {
    disabled: () => tr('independent timestamps are turned off'),
    no_authority: () => tr('no timestamp authority is set'),
    none: () => tr('a validated timestamp from a third party'),
    stale: () => tr('a recent answer from the timestamp authority'),
    empty: () => tr('saved records'),
  };
  return function trustCard(live, refresh) {
    const c = live?.court_readiness, trust = live?.trust;
    if (!c || !trust) return null;
    const number = value => Number(value || 0).toLocaleString(document.documentElement.lang || undefined);
    const box = node('section', 'home-trust');
    
    const head = node('div', 'home-trust-head'), title = node('h2', '', tr('What this journal proves'));
    title.id = 'trust-title-' + (++serial);
    const check = node('button', 'secondary', tr('Check now'));
    check.type = 'button';
    check.addEventListener('click', () => busy(check, async () => {
      try { await json('verify', {}); } catch (error) { toast(error.message, true); }
      await refresh();
    }));
    box.setAttribute('aria-labelledby', title.id);
    head.append(title, check);
    const rows = node('dl', 'home-trust-rows');
    const marks = {ok: '✓', warn: '!', fail: '✕', none: '—'};
    const row = (state, label, ...content) => {
      const term = node('dt'), mark = node('span', 'home-trust-mark', marks[state]);
      mark.setAttribute('aria-hidden', 'true');
      term.dataset.state = state;
      term.append(mark, node('span', '', label));
      const detail = node('dd');
      detail.append(...content.filter(Boolean));
      rows.append(term, detail);
    };
    const integrity = trust.integrity;
    if (integrity?.state === 'failed')
      row('fail', tr('Integrity'), node('span', '', tr('Journal failed its integrity check') + ' · ' + tr('Detected {time}', {time: formatTime(integrity.detected_at)})));
    else if (integrity?.state === 'ok')
      row('ok', tr('Integrity'), node('span', '', tr('All {n} records match their hashes and signatures.', {n: number(integrity.events)}) + ' '
        + tr('Full check {time}', {time: formatTime(integrity.checked_at)})),
        integrity.previous_failure ? node('small', 'home-note', tr('Failed on {time}; the record stays in the signed journal.', {time: formatTime(integrity.previous_failure)})) : null);
    else row('none', tr('Integrity'), node('span', '', tr('Not checked yet.')));
    const copy = node('button', 'text-link', tr('Copy'));
    copy.type = 'button';
    copy.addEventListener('click', async () => {
      try { await navigator.clipboard.writeText(trust.fingerprint); toast(tr('Copied.')); }
      catch { toast(trust.fingerprint); }
    });
    row('warn', tr('Signing key'), node('span', '', tr('Fingerprint {fingerprint}. The recipient compares it through a separate channel; without that the signature shows only which key signed.',
      {fingerprint: (trust.fingerprint || '').match(/.{1,4}/g)?.join(' ') || '—'})), copy);
    const items = (c.missing || []).map(key => (COURT_MISSING[key] || (() => key))(c)).join('; ');
    if (c.ready)
      row('ok', tr('External time'), node('span', '', tr('RFC 3161 covers {through} of {total} records · answer {time}',
        {through: number(c.stamped_through), total: number(c.records), time: formatTime(c.stamped_at)})));
    else
      row(c.missing?.includes('empty') ? 'none' : 'warn', tr('External time'), node('span', '', tr('Missing: {items}', {items})),
        c.stamped_through ? node('small', 'home-note', tr('A validated timestamp covers {through} of {total} records.', {through: number(c.stamped_through), total: number(c.records)})) : null);
    if (!trust.gaps_24h)
      row('ok', tr('Completeness'), node('span', '', tr('No observation gaps in the last 24 hours.')));
    else {
      const show = trust.last_gap && openJournal ? node('button', 'text-link', tr('Show in the journal')) : null;
      if (show) { show.type = 'button'; show.addEventListener('click', () => openJournal(trust.last_gap.kind)); }
      row('warn', tr('Completeness'), node('span', '', tr('Observation gaps in the last 24 hours: {n}. Last one {time}.',
        {n: number(trust.gaps_24h), time: trust.last_gap ? formatTime(trust.last_gap.at) : '—'})), show);
    }
    box.append(head, rows, node('small', 'home-note', tr('The recipient must also confirm the signing key fingerprint received separately and run verify.py with --tsa-ca and the timestamp authority’s root certificate.')));
    return box;
  };
}
