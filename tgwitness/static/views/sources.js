const monitoring = ["messages", "edits", "deletions", "reactions", "membership"];
const media = [
  ["photo", "Photos"], ["video", "Videos"], ["animation", "GIFs & animations"],
  ["video_note", "Round video messages"], ["voice", "Voice messages"],
  ["audio", "Music & audio"], ["sticker", "Stickers"], ["document", "Files & documents"],
];
const same = (a, b) => JSON.stringify(a) === JSON.stringify(b);
const copy = value => JSON.parse(JSON.stringify(value));

function changes(before, after) {
  if (before && after && typeof before === "object" && typeof after === "object")
    return [...new Set([...Object.keys(before), ...Object.keys(after)])]
      .reduce((total, key) => total + changes(before[key], after[key]), 0);
  return before === after ? 0 : 1;
}

/** Sources owns its tabs and recording drafts. All state and actions come from the host. */
export function createSources(context) {
  const {root, tr, getState, getSession, may, json, refreshStatus, toast} = context;
  const find = id => root.querySelector("#" + id);
  const form = find("recording-form"), listeners = new AbortController();
  const tabs = [...root.querySelectorAll("[data-source-tab]")];
  let tab = "scope", baseline = null, session = getSession(), saving = false, generation = 0;
  let dirty = {monitoring: false, capture: false, recheck: false};
  const on = (element, event, handler) => element.addEventListener(event, handler, {signal: listeners.signal});
  const allowed = group => !getState().status?.demo && may(group === "recheck" ? "sources" : "settings");
  const permission = group => may(group === "recheck" ? "sources" : "settings");

  function showTab(name, focus = false) {
    if (!tabs.some(button => button.dataset.sourceTab === name)) name = "scope";
    tab = name;
    for (const button of tabs) {
      const selected = button.dataset.sourceTab === tab;
      button.setAttribute("aria-selected", String(selected));
      button.tabIndex = selected ? 0 : -1;
      find("sources-panel-" + button.dataset.sourceTab).hidden = !selected;
      if (selected && focus) button.focus();
    }
    if (name === "recording") updateStatus(getState().status);
  }
  for (const button of tabs) {
    on(button, "click", () => showTab(button.dataset.sourceTab));
    on(button, "keydown", event => {
      const index = tabs.indexOf(button);
      const next = {ArrowRight: (index + 1) % tabs.length, ArrowLeft: (index + tabs.length - 1) % tabs.length,
        Home: 0, End: tabs.length - 1}[event.key];
      if (next === undefined) return;
      event.preventDefault();
      showTab(tabs[next].dataset.sourceTab, true);
    });
  }

  function buildMedia() {
    const box = find("media-rules");
    for (const [key, label] of media) {
      const row = root.ownerDocument.createElement("div");
      row.className = "media-rule";
      const checkbox = root.ownerDocument.createElement("input");
      checkbox.type = "checkbox"; checkbox.id = "media-on-" + key;
      const title = root.ownerDocument.createElement("label");
      title.htmlFor = checkbox.id; title.textContent = tr(label);
      const size = root.ownerDocument.createElement("input");
      Object.assign(size, {id: "media-max-" + key, type: "number", min: "1", max: "2000", step: "1", required: true});
      size.setAttribute("aria-label", tr("Maximum size for {type}", {type: tr(label)}));
      const field = root.ownerDocument.createElement("span");
      field.className = "field-unit";
      const unit = root.ownerDocument.createElement("span");
      unit.className = "unit"; unit.textContent = "MiB";
      field.append(size, unit); row.append(checkbox, title, field); box.append(row);
    }
  }
  buildMedia();

  function read() {
    return {
      monitoring: Object.fromEntries(monitoring.map(key => [key, find("monitor-" + key).checked])),
      capture: {
        ...baseline?.capture,
        download_media: find("download-media").checked, max_media_mb: Number(find("max-media").value),
        types: Object.fromEntries(media.map(([key]) => [key, {
          enabled: find("media-on-" + key).checked, max_mb: Number(find("media-max-" + key).value),
        }])),
      },
      recheck: {recheck_minutes: Number(find("recheck-priority").value),
        recheck_other_minutes: Number(find("recheck-other").value)},
    };
  }

  function write(group, value) {
    if (group === "monitoring") {
      for (const key of monitoring) find("monitor-" + key).checked = value[key] ?? true;
    } else if (group === "capture") {
      find("download-media").checked = value.download_media;
      find("max-media").value = String(value.max_media_mb);
      for (const [key] of media) {
        const rule = value.types[key] || {enabled: true, max_mb: value.max_media_mb};
        find("media-on-" + key).checked = rule.enabled;
        find("media-max-" + key).value = String(rule.max_mb);
      }
    } else {
      find("recheck-priority").value = String(value.recheck_minutes);
      find("recheck-other").value = String(value.recheck_other_minutes);
    }
  }

  function clearValidation() {
    for (const input of form.querySelectorAll("[aria-invalid]")) {
      const error = input.id + "-field-error";
      find(error)?.remove();
      input.removeAttribute("aria-invalid");
      const ids = (input.getAttribute("aria-describedby") || "").split(/\s+/).filter(id => id && id !== error);
      if (ids.length) input.setAttribute("aria-describedby", ids.join(" "));
      else input.removeAttribute("aria-describedby");
    }
  }

  function renderDraft() {
    if (!baseline) return;
    const draft = read();
    let count = 0;
    for (const group of Object.keys(dirty)) {
      dirty[group] = allowed(group) && !same(draft[group], baseline[group]);
      if (dirty[group]) count += changes(baseline[group], draft[group]);
    }
    context.setDirty({...dirty});
    find("recording-change-count").textContent = count
      ? tr(count === 1 ? "1 unsaved change" : "{n} unsaved changes", {n: count}) : tr("No unsaved changes");
    const badge = find("recording-tab-dirty");
    badge.hidden = !count; badge.textContent = String(count);
    find("recording-save").disabled = saving || !count;
    find("recording-discard").disabled = saving || !count;
    find("recording-save").textContent = tr(saving ? "Saving…" : "Save recording settings");
    find("recording-savebar").classList.toggle("is-dirty", !!count);
    find("monitoring-unsaved").textContent = dirty.monitoring ? tr("Unsaved changes") : "";
    find("capture-unsaved").textContent = dirty.capture ? tr("Unsaved changes") : "";
    const enabled = monitoring.filter(key => draft.monitoring[key]);
    find("monitoring-note").textContent = tr(!enabled.length
      ? "No live event types selected. Only operational and other group service records will continue."
      : !draft.monitoring.messages
        ? "New message capture is off. Edits and deletion notices may have no earlier content to compare."
        : "Original messages provide context for later edits and deletion notices. Already saved records remain available.");
  }

  function updateStatus(status) {
    if (!status) return;
    if (session !== getSession()) resetSession();
    const latest = {
      monitoring: Object.fromEntries(monitoring.map(key => [key, status.monitoring?.[key] ?? true])),
      capture: copy(status.capture),
      recheck: copy(status.recheck),
    };
    for (const group of Object.keys(dirty)) {
      if (!baseline || !dirty[group] || !allowed(group)) write(group, latest[group]);
      find(group === "monitoring" ? "monitoring-form" : group === "capture" ? "capture-form" : "recheck-form")
        .querySelectorAll("input,select,button").forEach(element => element.disabled = !allowed(group));
    }
    baseline = latest;
    const enabled = monitoring.filter(key => latest.monitoring[key]);
    find("monitoring-current").textContent = tr("Saved for this account: {list}.", {
      list: enabled.length ? enabled.map(key => context.termText(key)).join(", ") : tr("no live event categories"),
    });
    find("sources-scope-summary").textContent = context.scopeName(status.scope?.mode || "selected");
    find("sources-count-summary").textContent = tr("{n} enabled sources", {n: status.targets.filter(item => item.enabled).length});
    find("sources-recording-summary").textContent = tr(status.collector.running ? "Observation enabled" : "Observation paused");
    find("sources-tab-count").textContent = String(status.targets.length);
    const note = find("recording-result");
    if (status.demo) note.textContent = tr("This demo is read-only. Recording settings can be changed in your own workspace.");
    else if (!permission("monitoring") && !permission("recheck")) note.textContent = tr("This access cannot change recording settings.");
    renderDraft();
  }

  on(form, "input", event => {
    if (event.target.id === "max-media")
      for (const [key] of media) find("media-max-" + key).value = event.target.value;
    find("recording-result").textContent = "";
    renderDraft();
  });
  on(form, "change", renderDraft);
  for (const button of root.querySelectorAll("[data-monitor-preset]")) {
    on(button, "click", () => {
      if (!allowed("monitoring")) return;
      for (const key of monitoring)
        find("monitor-" + key).checked = button.dataset.monitorPreset === "all" || ["messages", "edits", "deletions"].includes(key);
      renderDraft();
    });
  }
  on(find("recording-discard"), "click", () => {
    if (saving || !baseline) return;
    for (const group of Object.keys(dirty)) write(group, baseline[group]);
    clearValidation();
    find("recording-result").textContent = tr("Changes discarded.");
    renderDraft();
  });

  on(form, "submit", async event => {
    event.preventDefault();
    if (saving || !baseline || !form.reportValidity()) return;
    renderDraft();
    const draft = read(), payload = Object.fromEntries(Object.keys(dirty).filter(group => dirty[group])
      .map(group => [group, draft[group]]));
    if (!Object.keys(payload).length) return;
    const current = getSession(), attempt = ++generation, profile = getState().profile;
    saving = true; renderDraft();
    try {
      const result = await json("recording", payload, {profile});
      if (current !== getSession() || attempt !== generation) return;
      baseline = {monitoring: result.monitoring, capture: result.capture, recheck: result.recheck};
      context.saved(result);
      renderDraft();
      await refreshStatus();
      if (current !== getSession() || attempt !== generation) return;
      const message = Object.values(dirty).some(Boolean)
        ? tr("Settings saved. Newer edits are still unsaved.")
        : tr("Recording settings saved.");
      find("recording-result").textContent = message;
      toast(message);
    } catch (error) {
      if (current !== getSession() || attempt !== generation || error.name === "StaleView") return;
      find("recording-result").textContent = error.message;
      toast(error.message, true);
    } finally {
      if (current === getSession() && attempt === generation) {saving = false; renderDraft();}
    }
  });

  function resetSession() {
    generation++; session = getSession(); baseline = null; saving = false;
    dirty = {monitoring: false, capture: false, recheck: false};
    context.setDirty({...dirty}); form.reset(); clearValidation(); find("recording-result").textContent = "";
    find("recording-save").disabled = find("recording-discard").disabled = true;
    find("recording-tab-dirty").hidden = true;
    for (const id of ["target-list", "dialog-list", "scope-exclude", "snapshot-source", "chat-export-source"])
      find(id)?.replaceChildren();
    for (const id of ["sources-scope-summary", "sources-count-summary", "sources-recording-summary"])
      find(id).textContent = "";
    find("sources-tab-count").textContent = "0";
    showTab("scope");
  }
  return {
    enter({params} = {}) {showTab(params?.tab || tab); updateStatus(getState().status);},
    updateStatus, showTab,
    leave() {},
    resetSession,
    destroy() {generation++; listeners.abort();},
  };
}
