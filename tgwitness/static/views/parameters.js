const equal = (a, b) => JSON.stringify(a) === JSON.stringify(b);
const groupNames = {collection: "Collection", recheck: "Recheck", attachments: "Media", people: "People",
  notifications: "Notifications", exports: "Exports", connection: "Telegram", proxies: "MTProxy"};

export function createParameters(context) {
  const {root, tr, getState, getSession, json, may, toast, refreshStatus} = context;
  const find = id => root.querySelector("#" + id), form = find("parameters-form");
  const listeners = new AbortController(), fields = new Map(), groups = new Map();
  let session = getSession(), catalog = null, request = 0, saving = false, schema = "", selected = "collection";
  const on = (node, event, fn) => node.addEventListener(event, fn, {signal: listeners.signal});
  const active = () => getState().view === "parameters";
  const allowed = () => may("settings") && !getState().status?.demo;
  const make = (tag, className = "", text = "") => {
    const node = root.ownerDocument.createElement(tag); node.className = className; node.textContent = text; return node;
  };
  const items = () => (catalog?.groups || []).flatMap(group => group.items);
  const raw = entry => entry.item.kind === "bool" ? entry.field.checked : entry.field.value;
  const value = entry => entry.item.kind === "bool" ? entry.field.checked : entry.item.kind === "lines"
    ? entry.field.value.split("\n").map(line => line.trim()).filter(Boolean) : Number(entry.field.value);
  const write = (entry, next) => {
    if (entry.item.kind === "bool") entry.field.checked = next;
    else entry.field.value = entry.item.kind === "lines" ? next.join("\n") : String(next);
  };
  const formatted = value => Array.isArray(value) ? tr("{n} lines", {n: value.length})
    : typeof value === "boolean" ? tr(value ? "On" : "Off") : Number(value).toLocaleString();
  const draft = () => Object.fromEntries([...fields].filter(([, entry]) => !equal(value(entry), entry.item.value))
    .map(([key, entry]) => [key, value(entry)]));

  function offset() {
    root.style.setProperty("--parameters-top", Math.max(0, context.headerOffset?.() || 0) + "px");
    root.style.setProperty("--parameters-group-top", ((context.headerOffset?.() || 0)
      + find("parameters-toolbar").getBoundingClientRect().height + 16) + "px");
  }

  function filter() {
    const query = find("parameters-search").value.trim().toLocaleLowerCase(), changed = find("parameters-changed").checked;
    let total = 0;
    for (const [id, group] of groups) {
      let count = 0;
      for (const entry of group.entries) {
        entry.row.hidden = !!(query && !entry.search.includes(query) || changed && !entry.row.classList.contains("changed"));
        if (!entry.row.hidden) count++;
      }
      total += count; group.card.hidden = group.link.hidden = !count;
      group.link.setAttribute("aria-current", id === selected ? "location" : "false");
    }
    find("parameters-count").textContent = tr("{shown} of {total} parameters", {shown: total, total: fields.size});
    find("parameters-empty").hidden = !!total || !catalog;
    offset();
  }

  function renderDraft() {
    if (!catalog || !active()) return;
    let count = 0;
    for (const entry of fields.values()) {
      const changed = !equal(value(entry), entry.item.default);
      entry.row.classList.toggle("changed", changed);
      entry.reset.hidden = !changed; entry.reset.disabled = !allowed() || saving;
      entry.field.disabled = !allowed();
      if (!equal(value(entry), entry.item.value)) count++;
    }
    context.setDirty(!!count);
    find("parameters-unsaved").textContent = count ? tr("Unsaved changes — press Save parameters to apply.") : "";
    form.querySelector('[type="submit"]').disabled = !allowed() || saving || !count;
    find("parameters-reset").disabled = !allowed() || saving;
    for (const group of groups.values()) {
      const changed = group.entries.filter(entry => !equal(value(entry), entry.item.default)).length;
      group.count.hidden = !changed; group.count.textContent = String(changed);
    }
    filter();
  }

  function build(data) {
    fields.clear(); groups.clear(); find("parameters-groups").replaceChildren(); find("parameters-nav").replaceChildren();
    for (const group of data.groups) {
      const card = make("section", "card padded parameters-group"), grid = make("div", "parameters-grid");
      card.id = "parameters-group-" + group.id;
      card.append(make("h2", "", tr(groupNames[group.id] || group.title)), make("p", "muted", tr(group.description)), grid);
      const link = make("a", "", tr(groupNames[group.id] || group.title)), count = make("span", "parameters-nav-count");
      link.href = context.sectionHref?.(group.id) || "#" + card.id; link.dataset.parameterGroup = group.id;
      count.hidden = true; link.append(count); find("parameters-nav").append(link);
      const entryGroup = {card, link, count, entries: []}; groups.set(group.id, entryGroup);
      for (const item of group.items) {
        const row = make("div", "parameter-row"), id = "parameter-" + item.key;
        const label = make("label", item.kind === "bool" ? "check-label" : "", tr(item.label)); label.htmlFor = id;
        const field = make(item.kind === "lines" ? "textarea" : "input");
        field.id = id; field.dataset.parameter = item.key;
        if (item.kind === "bool") {field.type = "checkbox"; label.prepend(field); row.append(label);}
        else {
          const line = make("div", "parameter-field");
          if (item.kind === "lines") {field.rows = 3; field.spellcheck = false;}
          else Object.assign(field, {type: "number", min: item.low, max: item.high, step: 1, required: true});
          line.append(field); if (item.unit) line.append(make("span", "unit", tr(item.unit))); row.append(label, line);
        }
        if (item.help) row.append(make("p", "hint", tr(item.help)));
        const meta = make("p", "hint parameter-meta", [item.kind === "int"
          ? tr("{low} to {high}", {low: item.low.toLocaleString(), high: item.high.toLocaleString()}) : "",
          tr("Default: {value}", {value: formatted(item.default)})].filter(Boolean).join(" · "));
        const reset = make("button", "text-link", tr("Restore default")); reset.type = "button"; reset.dataset.parameterReset = item.key;
        meta.append(" · ", reset); row.append(meta); grid.append(row);
        const entry = {item, field, row, reset, search: [item.key, item.label, item.help, tr(item.label), tr(item.help || ""),
          group.id, tr(groupNames[group.id] || group.title)].join(" ").toLocaleLowerCase()};
        fields.set(item.key, entry); entryGroup.entries.push(entry); write(entry, item.value);
      }
      find("parameters-groups").append(card);
    }
  }

  function accept(data, submitted = null) {
    const nextSchema = JSON.stringify(data.groups.map(group => ({id: group.id, items: group.items.map(({value, ...item}) => item)})));
    if (nextSchema !== schema) {build(data); schema = nextSchema;}
    else for (const group of data.groups) for (const item of group.items) {
      const entry = fields.get(item.key);
      if (submitted ? equal(raw(entry), submitted[item.key]) : equal(value(entry), entry.item.value)) write(entry, item.value);
      entry.item = item;
    }
    catalog = data; context.saved(data); renderDraft();
  }

  async function load({signal, current = active} = {}) {
    if (!active()) return;
    if (session !== getSession()) resetSession();
    const mine = ++request, now = getSession(), profile = getState().profile;
    find("parameters-result").textContent = catalog ? "" : tr("Loading parameters…");
    try {
      const result = await json("parameters", undefined, {profile, signal});
      if (mine !== request || now !== getSession() || !current()) return;
      accept(result); find("parameters-result").textContent = "";
    } catch (error) {
      if (mine !== request || now !== getSession() || !current() || error.name === "AbortError" || error.name === "StaleView") return;
      find("parameters-result").textContent = error.message; throw error;
    }
  }

  on(find("parameters-search"), "input", filter); on(find("parameters-changed"), "change", filter);
  on(find("parameters-clear-search"), "click", () => {
    find("parameters-search").value = ""; find("parameters-changed").checked = false; filter(); find("parameters-search").focus();
  });
  on(find("parameters-nav"), "click", event => {
    const link = event.target.closest("a[data-parameter-group]"); if (!link) return;
    event.preventDefault(); selected = link.dataset.parameterGroup; context.sectionChanged?.(selected); filter();
    groups.get(selected).card.scrollIntoView({block: "start", behavior: "instant"});
  });
  on(form, "input", renderDraft);
  on(form, "click", event => {
    const button = event.target.closest("button[data-parameter-reset]"); if (!button || !allowed() || saving) return;
    const entry = fields.get(button.dataset.parameterReset); write(entry, entry.item.default); renderDraft(); entry.field.focus();
  });
  on(form, "submit", async event => {
    event.preventDefault(); if (!catalog || !allowed() || saving) return;
    for (const entry of fields.values()) if (entry.item.kind === "int"
      && (entry.field.value.trim() === "" || !entry.field.checkValidity())) {
      find("parameters-result").textContent = tr("{name}: enter a whole number from {low} to {high}.", {
        name: tr(entry.item.label), low: entry.item.low, high: entry.item.high}); entry.field.focus(); return;
    }
    const values = draft(); if (!Object.keys(values).length) return;
    const submitted = Object.fromEntries([...fields].map(([key, entry]) => [key, raw(entry)]));
    const now = getSession(), profile = getState().profile; request++; saving = true; renderDraft();
    try {
      const result = await json("parameters", {values}, {profile});
      if (now !== getSession()) return;
      accept(result, submitted); await refreshStatus();
      if (now !== getSession()) return;
      if (active()) find("parameters-result").textContent = tr("Parameters saved and recorded in the signed journal.");
      toast(tr("Parameters saved and recorded in the signed journal."));
    } catch (error) {
      if (now !== getSession() || error.name === "StaleView") return;
      if (active()) find("parameters-result").textContent = error.message;
      toast(error.message, true);
    } finally {if (now === getSession()) {saving = false; renderDraft();}}
  });
  on(find("parameters-reset"), "click", () => {
    if (!allowed() || saving || !catalog || !context.confirm(tr("Restore every parameter of this workspace to its default?"))) return;
    for (const entry of fields.values()) write(entry, entry.item.default);
    renderDraft(); form.requestSubmit();
  });
  on(root.ownerDocument.defaultView, "resize", () => {if (active()) offset();});

  function resetSession() {
    request++; session = getSession(); saving = false; catalog = null; schema = ""; selected = "collection";
    fields.clear(); groups.clear(); find("parameters-groups").replaceChildren(); find("parameters-nav").replaceChildren();
    find("parameters-search").value = ""; find("parameters-changed").checked = false;
    for (const id of ["parameters-count", "parameters-result", "parameters-unsaved"]) find(id).textContent = "";
    context.setDirty(false); context.saved(null);
  }
  return {load, enter: load, updateStatus() {if (active()) renderDraft();}, leave() {request++;}, resetSession,
    destroy() {request++; listeners.abort();}};
}
