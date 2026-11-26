const KINDS = "coverage.gap,connection.restored,process.started,process.stopped,observation.started,observation.stopped";
const INTERRUPTIONS = {transport_disconnected: "Connection to Telegram lost", authorization_required: "Telegram signed this account out", resume_failed: ""};
const CAUSE = "cause:";
const STOPS = {shutdown: "TgWitness was shut down", operator: "Observation paused"};
const MOMENTS = {"updates delivered while observation was paused": "Updates arrived while observation was paused",
  "startup buffer full": "Too many updates arrived during startup", source_access_lost: "The account lost access to a source",
  scope_undetermined: "Updates from an unidentified chat were not recorded",
  updates_diverted: "Updates are going to another session",
  session_revoked_externally: "The session was ended from another device or by Telegram.",
  "Telegram reported that updates for this interval are too old to deliver": "Telegram could not deliver older updates"};
const LISTED = 3;

export function intervals(events, chat) {
  const found = [];
  // A stop before observation ever ran interrupts nothing: a new workspace starts the program several times
  // during setup. The first start of a journal has no earlier record; without it, assume observation had run.
  let open = null, observed = true;
  const start = (at, reason, unexpected) => {
    if (!open) open = {from: at, reasons: new Set(), unexpected};
    if (reason) open.reasons.add(reason);
  };
  for (const event of [...events].sort((a, b) => a.seq - b.seq)) {
    const account = event.chat_id === null || event.chat_id === undefined;
    if (!account && event.chat_id !== chat) continue;
    const at = Date.parse(event.observed_at), payload = event.payload || {};
    if (!Number.isFinite(at)) continue;
    if (event.kind === "coverage.gap") {
      if (account && Object.hasOwn(INTERRUPTIONS, payload.reason)) start(at, payload.reason === "authorization_required"
        && typeof payload.cause === "string" && payload.cause ? CAUSE + payload.cause : INTERRUPTIONS[payload.reason], true);
      else found.push({from: at, to: at, reasons: MOMENTS[payload.reason] ? [MOMENTS[payload.reason]] : []});
    } else if (event.kind === "observation.stopped") {
      observed = true;
      start(at, STOPS[payload.reason] || STOPS.operator, !Object.hasOwn(STOPS, payload.reason));
    } else if (event.kind === "process.stopped") {
      if (observed) start(at, STOPS.shutdown, false);
    } else if (event.kind === "process.started") {
      const before = Date.parse(payload.previous_observation?.observed_at);
      if (!payload.previous_observation) observed = false;
      else if (observed) start(Number.isFinite(before) ? Math.min(before, at) : at, STOPS.shutdown, false);
    } else {
      observed = true;
      if (open) {
        found.push({from: open.from, to: at, reasons: [...open.reasons]});
        open = null;
      }
    }
  }
  if (open?.unexpected) found.push({from: open.from, to: null, reasons: [...open.reasons]});
  const merged = [];
  for (const item of found.sort((a, b) => a.from - b.from)) {
    const last = merged.at(-1);
    if (last && (last.to === null || item.from <= last.to + 1000)) {
      last.to = last.to === null || item.to === null ? null : Math.max(last.to, item.to);
      last.reasons = [...new Set([...last.reasons, ...item.reasons])];
    } else merged.push({...item});
  }
  return merged;
}

export function createChatGaps({node, tr, icon, json, fmtTime, openJournal, allowJournal, fmtDay = null, dayKey = null, lossText = null}) {
  const reasonText = reason => !reason.startsWith(CAUSE) ? tr(reason)
    : lossText ? lossText(reason.slice(CAUSE.length)) : tr(INTERRUPTIONS.authorization_required);
  let numbers = new Map(), offlineWindows = new Map(), periods = [], loadedKey = "", pendingKey = "", compact = true;
  const cache = new Map(), answers = new Map();

  function coverage(chatKey, chat, range, dataKey) {
    const query = new URLSearchParams();
    for (const name of ["since", "until"]) if (range[name]) query.set(name, range[name]);
    const id = chatKey + "|" + chat + "|" + query + "|" + dataKey;
    if (answers.has(id)) return Promise.resolve(answers.get(id));
    const legacy = () => json("events?kind=" + KINDS + "&limit=500" + (query.size ? "&" + query : ""));
    const request = compact ? json("chats/" + encodeURIComponent(chat) + "/coverage" + (query.size ? "?" + query : ""))
      .catch(error => {if (error?.status !== 404) throw error; compact = false; return legacy();}) : legacy();
    return request.then(result => {
      answers.set(id, result);
      if (answers.size > 24) answers.delete(answers.keys().next().value);
      return result;
    });
  }

  function marker(kind, key, build) {
    const id = kind + ":" + key;
    let box = cache.get(id);
    if (!box) {
      box = node("div", "chat-gap");
      box.dataset.kind = kind; box.setAttribute("role", "note");
      build(box);
      if (cache.size > 400) cache.clear();
      cache.set(id, box);
    }
    return box;
  }

  function numberMarker(list) {
    const total = list.reduce((sum, gap) => sum + gap.missing, 0);
    return marker("numbers", list.map(gap => gap.low + "-" + gap.high).join(","), box => {
      const ranges = list.slice(0, LISTED).map(gap => gap.low === gap.high ? "#" + gap.low : "#" + gap.low + "–#" + gap.high);
      if (list.length > LISTED) ranges.push("…");
      box.append(icon("question"), node("b", "", total.toLocaleString(document.documentElement.lang||undefined)),
        node("span", "", tr("Message numbers not observed") + ": " + ranges.join(", ")));
    });
  }

  function length(seconds) {
    const n = Math.max(0, Math.round(seconds));
    if (n < 60) return tr("{n} s", {n});
    if (n < 3600) return tr("{n} min", {n: Math.round(n / 60)});
    return tr("{n} h", {n: Math.floor(n / 3600)}) + " " + tr("{n} min", {n: Math.round(n % 3600 / 60)});
  }
  function span(from, to) {
    const clock = value => fmtTime(new Date(value).toISOString(), {mode: "clock"});
    if (!fmtDay || !dayKey) return fmtTime(new Date(from).toISOString()) + (to === null ? " – …" : to === from ? "" : " – " + fmtTime(new Date(to).toISOString()));
    const start = fmtDay(new Date(from).toISOString()) + ", " + clock(from);
    if (to === null) return start + " – …";
    if (to === from || clock(to) === clock(from) && dayKey(new Date(to).toISOString()) === dayKey(new Date(from).toISOString())) return start;
    return start + "–" + (dayKey(new Date(to).toISOString()) === dayKey(new Date(from).toISOString()) ? "" : fmtDay(new Date(to).toISOString()) + ", ") + clock(to);
  }
  function stopped(list) {
    const low = Math.min(...list.map(item => item.from)) - 1000;
    const high = list.some(item => item.to === null) ? Infinity : Math.max(...list.map(item => item.to)) + 1000;
    return [...offlineWindows.values()].filter(stop => stop.from >= low && stop.from <= high);
  }
  function periodMarker(list) {
    const windows = stopped(list), unattributed = windows.reduce((sum, stop) => sum + stop.deletions, 0);
    return marker("coverage", list.map(item => item.from + "-" + item.to).join(",") + "|" + windows.length + ":" + unattributed, box => {
      const ongoing = list.some(item => item.to === null);
      const seconds = list.reduce((sum, item) => sum + (item.to === null ? 0 : (item.to - item.from) / 1000), 0);
      const reasons = [...new Set(list.flatMap(item => item.reasons))].map(reasonText);
      const summary = [list.length > 1 ? tr("Pauses: {n}", {n: list.length.toLocaleString(document.documentElement.lang || undefined)}) : "",
        span(list[0].from, ongoing ? null : Math.max(...list.map(item => item.to))), seconds >= 1 ? length(seconds) : "",
        list.length === 1 ? reasons.join(" · ") : ""].filter(Boolean).join(" · ");
      const lines = node("span", "chat-gap-lines"), head = node("span", "chat-gap-summary");
      head.append(node("strong", "", tr("Coverage gap")), node("span", "", summary));
      lines.append(head);
      if (windows.length) lines.append(node("span", "chat-gap-offline", [tr("TgWitness was not running: messages sent and deleted in this time could not be recorded."),
        unattributed ? tr("Deletions reported afterwards without a chat: {n}. Messages of this chat may be among them.",
          {n: unattributed.toLocaleString(document.documentElement.lang || undefined)}) : ""].filter(Boolean).join(" ")));
      const details = node("details", "chat-gap-details"), all = node("span", "chat-gap-all");
      details.append(node("summary", "", tr("Details")), all);
      for (const item of list) {
        const why = item.reasons.map(reasonText).join(" · ");
        const from = fmtTime(new Date(item.from).toISOString()), to = item.to === null ? "…" : fmtTime(new Date(item.to).toISOString());
        all.append(node("span", "", (from === to ? from : from + " – " + to) + (why ? " · " + why : "")));
      }
      if (list.length > 1 || reasons.length) lines.append(details);
      box.append(icon("alert"), lines);
      if (allowJournal()) {
        const open = node("button", "text-link", tr("Show in the journal"));
        open.type = "button";
        open.addEventListener("click", () => openJournal("coverage.gap"));
        box.append(open);
      }
    });
  }

  function between(previous, message, when) {
    if (!previous) return [];
    const marks = [], holes = [];
    for (const gap of numbers.values()) if (gap.low > previous.id && gap.high < message.message_id) holes.push(gap);
    if (holes.length) marks.push(numberMarker(holes.sort((a, b) => a.low - b.low)));
    const from = Date.parse(previous.when), to = Date.parse(when);
    if (Number.isFinite(from) && Number.isFinite(to) && to > from) {
      const hit = periods.filter(item => item.from >= from && item.from < to);
      if (hit.length) marks.push(periodMarker(hit));
    }
    return marks;
  }

  function after(previous) {
    const from = Date.parse(previous?.when);
    if (!Number.isFinite(from)) return [];
    const hit = periods.filter(item => item.from >= from);
    return hit.length ? [periodMarker(hit)] : [];
  }

  function load(chatKey, dataKey, chat, done, range = {}) {
    const key = chatKey + "|" + dataKey;
    if (key === loadedKey || key === pendingKey) return;
    if (!loadedKey.startsWith(chatKey + "|")) periods = [];
    pendingKey = key;
    coverage(chatKey, chat, range, dataKey).then(result => {
      if (pendingKey !== key) return;
      const next = intervals(result.events || [], chat), changed = JSON.stringify(next) !== JSON.stringify(periods);
      periods = next; loadedKey = key; pendingKey = "";
      if (changed) done();
    }).catch(() => {if (pendingKey === key) {loadedKey = key; pendingKey = "";}});
  }

  function offline(list) {
    for (const stop of list || []) {
      const from = Date.parse(stop.from), to = Date.parse(stop.to);
      if (Number.isFinite(from) && Number.isFinite(to))
        offlineWindows.set(from, {from, to, deletions: Number.isSafeInteger(stop.unattributed_deletions) ? stop.unattributed_deletions : 0});
    }
  }

  return {reset: () => {numbers = new Map(); offlineWindows = new Map();}, add: list => {for (const gap of list || []) numbers.set(gap.low, gap);},
    offline, between, after, load};
}
