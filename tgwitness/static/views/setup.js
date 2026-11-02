// The goal's name and the two scales (levels.py). The goal itself is chosen in the step-by-step setup
// (views/wizard.js); the Extras card and the wizard's summary draw the scales from here.
export function goalName(tr, goal) {
  return {personal: () => tr("A personal record"), investigation: () => tr("An investigation"),
    evidence: () => tr("Evidence for a case")}[goal]?.() || tr("No goal chosen");
}

function itemName(tr, id) {
  return {journal: () => tr("Signed journal"), timestamps: () => tr("Independent timestamps"),
    drand: () => tr("Proof of live recording"), devices: () => tr("Telegram's device list"),
    code: () => tr("Code check"), witness: () => tr("Witness bot"), server: () => tr("Sealed server"),
    always_on: () => tr("Runs around the clock"), replica: () => tr("Off-site copy"),
    replica_lock: () => tr("Copy under Object Lock"), alerts: () => tr("Problem notifications"),
    gateway_log: () => tr("Cloudflare's log of the server's DNS")}[id]?.() || id;
}

function levelName(tr, level) {
  return {basic: () => tr("Basic"), moderate: () => tr("Moderate"), high: () => tr("High"),
    maximum: () => tr("Maximum")}[level]?.() || level;
}

export function levelOf(levels, percent) {
  return levels.find(([floor]) => percent >= floor)?.[1] || "basic";
}

function score(scale, levels) {
  const total = scale.items.reduce((sum, item) => sum + item.weight, 0);
  const got = scale.items.reduce((sum, item) => sum + (item.on ? item.weight : 0), 0);
  const percent = total ? Math.round(100 * got / total) : 0;
  return {percent, level: levelOf(levels, percent)};
}

// Both scales; with `after`, the part Apply would add is shown on top of the current state.
export function renderScales(box, data, {tr, node, after = null, compact = false}) {
  box.replaceChildren();
  const describe = {
    credibility: [tr("Credibility"), tr("What someone else can check: when the record existed, that it was written live and which program wrote it.")],
    reliability: [tr("Reliability"), tr("How likely collection keeps running and the record survives a lost or seized machine.")],
  };
  for (const key of ["credibility", "reliability"]) {
    const now = score(data.assessment[key], data.levels), next = after ? score(after[key], data.levels) : now;
    const wrap = node("div", "level-scale level-" + next.level);
    const head = node("div", "level-head");
    head.append(node("strong", "", describe[key][0]), node("span", "level-name", levelName(tr, next.level)));
    if (after && next.percent !== now.percent)
      head.append(node("span", "level-was", tr("now: {level}", {level: levelName(tr, now.level)})));
    const bar = node("div", "level-bar");
    bar.setAttribute("role", "meter"); bar.setAttribute("aria-valuemin", "0"); bar.setAttribute("aria-valuemax", "100");
    bar.setAttribute("aria-valuenow", String(next.percent)); bar.setAttribute("aria-label", describe[key][0]);
    bar.setAttribute("aria-valuetext", levelName(tr, next.level) + " · " + next.percent + "%");
    const solid = node("span", "level-now"), gain = node("span", "level-gain");
    solid.style.width = Math.min(now.percent, next.percent) + "%";
    gain.style.width = Math.max(0, next.percent - now.percent) + "%";
    bar.append(solid, gain);
    wrap.append(head, bar);
    if (!compact) {
      wrap.append(node("p", "hint", describe[key][1]));
      const list = node("ul", "level-items"), items = (after || data.assessment)[key].items;
      for (const item of items) {
        const row = node("li", item.on ? "on" : "off");
        row.append(node("span", "level-mark", item.on ? "✓" : "○"), node("span", "", itemName(tr, item.id)),
          node("span", "level-weight", "+" + item.weight));
        list.append(row);
      }
      wrap.append(list);
    }
    box.append(wrap);
  }
}
