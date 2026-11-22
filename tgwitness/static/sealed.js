"use strict";
const $ = id => document.getElementById(id);
let lang = (navigator.languages?.length ? navigator.languages : [navigator.language || ""])
  .map(code => String(code).toLowerCase().split("-")[0])
  .find(code => code === "en" || window.TGW_SEALED_LOCALES?.[code]) || "en";
let qrId = null, ended = false;
let lastState = null, connectionFailed = false, statusError = "", actionError = "";
const english = new WeakMap();
const tr = (text, values = {}) => {
  const translated = lang === "en" ? text : window.TGW_SEALED_LOCALES?.[lang]?.[text];
  return (typeof translated === "string" ? translated : text).replace(/\{(\w+)\}/g,
    (match, name) => Object.hasOwn(values, name) ? String(values[name]) : match);
};
const fragment = new URLSearchParams(location.hash.slice(1));
if (fragment.has("access")) {
  sessionStorage.setItem("sealed-access", fragment.get("access"));
  history.replaceState(null, "", location.pathname);
}
const token = sessionStorage.getItem("sealed-access") || "";
function translate() {
  document.documentElement.lang = lang;
  $("language").value = lang;
  document.querySelectorAll("[data-i18n]").forEach(el => {
    if (!english.has(el)) english.set(el, el.textContent);
    el.textContent = tr(english.get(el));
  });
  $("chat-search").placeholder = tr("Search chats"); $("chat-search").setAttribute("aria-label", tr("Search chats"));
  $("secret-people-search").placeholder = tr("Search people"); $("secret-people-search").setAttribute("aria-label", tr("Search people"));
}
$("language").onchange = () => {
  lang = $("language").value; translate(); describeMode();
  if (assessmentResult) renderAssessment(assessmentResult);
  if (lastState) renderState(lastState);
  else renderError();
};
translate();
async function api(path, body) {
  const response = await fetch("/api/" + path, {method: body === undefined ? "GET" : "POST",
    headers: {"Authorization": "Bearer " + token, "Content-Type": "application/json", "X-TgWitness-Language": lang,
      "X-TgWitness-System-Language": navigator.language},
    body: body === undefined ? undefined : JSON.stringify(body), cache: "no-store", redirect: "error"});
  const data = await response.json();
  if (!response.ok) throw Object.assign(new Error(data.detail || "Request failed"), {status: response.status});
  return data;
}
function bind(id, action) {
  $(id).onclick = async () => {
    $(id).disabled = true; actionError = ""; renderError();
    try {await action(); await poll().catch(() => {});}
    catch (error) {actionError = error.message; renderError();}
    finally {$(id).disabled = false;}
  };
}
function credentials() {
  const id = $("api-id").value.trim(), hash = $("api-hash").value.trim();
  if (!id && !hash) return {};
  if (!/^[0-9]+$/.test(id) || Number(id) < 1 || Number(id) > 2147483647 || !/^[a-fA-F0-9]{32}$/.test(hash)) {
    $("custom-api").open = true;
    throw new Error($("api-error").textContent);
  }
  return {api_id: Number(id), api_hash: hash};
}
bind("send-code", async () => {
  await api("phone", {...credentials(), phone: $("phone").value.trim()});
  qrId = null; $("qr-image").hidden = true;
});
bind("confirm-code", async () => {await api("code", {code: $("code").value}); $("code").value = "";});
bind("confirm-password", async () => {await api("password", {password: $("password").value}); $("password").value = "";});
bind("qr", async () => {
  const result = await api("qr", credentials()); qrId = result.id;
  $("qr-image").src = "data:image/svg+xml;charset=utf-8," + encodeURIComponent(result.svg);
  $("qr-image").hidden = false;
});
bind("refresh", async () => {
  const result = await api("dialogs"); $("chats").replaceChildren();
  result.dialogs.forEach(chat => {const option = document.createElement("option");
    option.value = String(chat.chat_id); option.textContent = `${chat.title} (${chat.chat_id})`;
    option.dataset.title = chat.title || ""; option.dataset.kind = chat.kind || "";
    $("chats").append(option);
  });
  renderChatList();
  $("collect").disabled = !result.dialogs.length;
  $("preflight").disabled = !result.dialogs.length;
  clearAssessment();
  $("dialog-note").textContent = result.may_be_truncated ? tr("The dialog list reached its limit; some chats may be missing.") : "";
});
const LIMIT_STEPS = [1, 2, 5, 8, 10, 20, 50, 100, 200, 500, 1000, 2000];
const commonLimit = () => LIMIT_STEPS[Number($("common-limit").value)] || 50;
let chatKind = "";
const kindGroup = kind => kind === "supergroup" ? "group" : kind;
function renderChatList() {
  const list = $("chat-list"); list.replaceChildren();
  const single = $("export-mode").value === "journal";
  for (const option of $("chats").options) {
    const row = document.createElement("label"), box = document.createElement("input"), name = document.createElement("span"), meta = document.createElement("span");
    row.className = "chat-row"; row.dataset.kind = kindGroup(option.dataset.kind || "");
    row.dataset.search = ((option.dataset.title || "") + " " + option.value).toLowerCase();
    box.type = single ? "radio" : "checkbox"; box.name = "chat-pick"; box.value = option.value; box.checked = option.selected;
    name.textContent = option.dataset.title || option.value; meta.className = "chat-meta";
    meta.textContent = (option.dataset.kind ? tr(kindLabels[kindGroup(option.dataset.kind)] || option.dataset.kind) + " · " : "") + option.value;
    row.append(box, name, meta); list.append(row);
  }
  const loaded = $("chats").options.length > 0;
  for (const id of ["chat-list", "chat-list-footer", "chat-search", "chat-kinds"]) $(id).hidden = !loaded;
  filterChatList();
}
const kindLabels = {private: "Personal", bot: "Bots", group: "Groups", channel: "Channels"};
function filterChatList() {
  const query = $("chat-search").value.trim().toLowerCase();
  for (const row of $("chat-list").children) row.hidden = (chatKind && row.dataset.kind !== chatKind) || (query && !row.dataset.search.includes(query));
  syncChatList();
}
function syncChatList() {
  if (!$("chat-list").children.length) return;
  const single = $("export-mode").value === "journal", selected = new Set(Array.from($("chats").selectedOptions, o => o.value));
  for (const box of $("chat-list").querySelectorAll("input")) {
    if ((box.type === "radio") !== single) {renderChatList(); return;}
    box.checked = selected.has(box.value);
  }
  $("chat-count").textContent = tr("{selected} of {total} chats selected", {selected: selected.size, total: $("chats").options.length});
  $("chat-all").hidden = single;
}
$("chat-list").addEventListener("input", event => {
  const box = event.target, single = $("export-mode").value === "journal";
  for (const option of $("chats").options) {
    if (option.value === box.value) option.selected = box.checked;
    else if (single && box.checked) option.selected = false;
  }
});
$("chat-search").addEventListener("input", event => {event.stopPropagation(); filterChatList();});
$("chat-kinds").addEventListener("click", event => {
  const chip = event.target.closest("button[data-kind]"); if (!chip) return;
  chatKind = chip.dataset.kind;
  for (const other of $("chat-kinds").children) other.classList.toggle("active", other === chip);
  filterChatList();
});
function pickShown(state) {
  const shown = new Set(Array.from($("chat-list").children).filter(row => !row.hidden).map(row => row.querySelector("input").value));
  for (const option of $("chats").options) {
    if (!state) option.selected = false;
    else if (shown.has(option.value)) option.selected = true;
  }
  clearAssessment();
}
$("chat-all").onclick = () => pickShown(true);
$("chat-none").onclick = () => pickShown(false);
for (const card of document.querySelectorAll('input[name="mode-card"]')) card.addEventListener("input", () => {
  if (!card.checked) return;
  $("export-mode").value = card.value === "account" ? $("export-method").value : card.value;
  renderChatList();
});
$("export-method").addEventListener("input", () => {
  if (document.querySelector('input[name="mode-card"]:checked')?.value === "account") $("export-mode").value = $("export-method").value;
});
const SECRET_PEER = /^@?[A-Za-z][A-Za-z0-9_]{3,31}$|^[0-9]{1,20}$|^\+[0-9]{7,15}$/;
const peerHint = () => tr("Enter a @username, a phone number with + and the country code, or choose a person from your chats.");
// "+7 (999) 123-45-67" becomes "+79991234567"; usernames and IDs stay as typed.
const peerValue = value => {
  const text = String(value || "").trim();
  return /^\+[0-9\s().-]+$/.test(text) ? "+" + text.replace(/[^0-9]/g, "") : text;
};
let secretPeople = [];
function renderPeople() {
  const list = $("secret-people"), query = $("secret-people-search").value.trim().toLowerCase(), current = peerValue($("secret-peer").value);
  const shown = secretPeople.filter(person => !query || ((person.title || "") + " " + person.chat_id).toLowerCase().includes(query)).slice(0, 300);
  list.replaceChildren();
  for (const person of shown) {
    const row = document.createElement("button"), name = document.createElement("span"), meta = document.createElement("span");
    row.type = "button"; row.className = "person-row"; row.dataset.peer = String(person.chat_id);
    row.classList.toggle("active", current === String(person.chat_id));
    name.textContent = person.title || tr("Deleted account"); meta.className = "chat-meta"; meta.textContent = "ID " + person.chat_id;
    row.append(name, meta); list.append(row);
  }
  if (!shown.length) list.append(Object.assign(document.createElement("p"), {className: "hint empty", textContent: tr("No personal chats match.")}));
  list.hidden = $("secret-people-search").hidden = false;
  const options = $("secret-people-options"); options.replaceChildren();
  for (const person of secretPeople.slice(0, 500)) {
    const option = document.createElement("option"); option.value = String(person.chat_id); option.label = person.title || ""; options.append(option);
  }
}
function pickedPerson() {
  const value = peerValue($("secret-peer").value), person = secretPeople.find(item => String(item.chat_id) === value);
  $("secret-peer-picked").textContent = person ? tr("Selected: {name}", {name: (person.title || tr("Deleted account")) + " · ID " + person.chat_id}) : "";
}
bind("secret-people-load", async () => {
  const result = await api("dialogs");
  secretPeople = result.dialogs.filter(dialog => dialog.kind === "private");
  renderPeople(); pickedPerson();
});
$("secret-people-search").addEventListener("input", event => {event.stopPropagation(); renderPeople();});
$("secret-people").addEventListener("click", event => {
  const row = event.target.closest("button[data-peer]"); if (!row) return;
  $("secret-peer").value = row.dataset.peer;
  $("secret-peer").dispatchEvent(new Event("input", {bubbles: true}));
});
$("secret-peer").addEventListener("input", () => {pickedPerson(); if (secretPeople.length) renderPeople();});
let secretSignature = "";
const secretDrafts = {};
function personLabel(people, id) {
  const person = people?.[String(id)] || {};
  return [person.name, person.username ? "@" + person.username : null, id != null ? "ID " + id : null].filter(Boolean).join(" · ");
}
function secretButton(text, action, id, cls) {
  const button = document.createElement("button"); button.type = "button"; button.className = cls;
  button.textContent = text; button.dataset.secretAction = action; button.dataset.chat = String(id); return button;
}
function renderSecret(secret) {
  $("secret-live").hidden = !secret;
  if (!secret) return;
  $("secret-note").textContent = secret.error ? tr("Secret chats reported an error: {error}", {error: secret.error}) :
    secret.notice ? tr("The secret chat could not be started: {reason}", {reason: secret.notice}) :
    secret.interaction_problem ? secret.interaction_problem : !secret.connected ? tr("Connecting secret chats…") :
    !(secret.chats || []).length ? tr("Waiting for a secret chat. Start one above, or ask the other side to start one with this account.") : "";
  const messages = (secret.records || []).filter(r => r.kind === "secret_chat.message");
  $("capture-messages").textContent = String(messages.length);
  $("capture-unavailable").textContent = String((secret.chats || []).filter(chat => chat.state === "closed").length);
  const signature = JSON.stringify([secret.chats, messages.map(r => r.seq), lang]);
  if (signature === secretSignature) return;
  secretSignature = signature;
  for (const field of $("secret-chats").querySelectorAll("input[data-chat]")) secretDrafts[field.dataset.chat] = field.value;
  const list = $("secret-chats"); list.replaceChildren();
  for (const chat of secret.chats || []) {
    const card = document.createElement("article"), head = document.createElement("header"), title = document.createElement("strong");
    card.className = "secret-card"; title.textContent = personLabel(secret.people, chat.peer_user_id);
    const state = document.createElement("span"); state.className = "secret-state " + chat.state;
    state.textContent = chat.state === "requested" && !chat.outbound ? tr("Waiting for you to accept")
      : tr(secretStates[chat.state] || chat.state);
    head.append(title, state);
    if (chat.key_visualization) {
      const key = document.createElement("code"); key.className = "secret-key";
      key.textContent = (chat.key_visualization.match(/.{1,8}/g) || []).join(" "); head.append(key);
    }
    card.append(head);
    const thread = document.createElement("div"); thread.className = "secret-thread";
    for (const record of messages.filter(r => String(r.payload?.secret_chat_id) === String(chat.id)).slice(-30)) {
      const bubble = document.createElement("p"), meta = document.createElement("small");
      bubble.className = "secret-bubble " + (record.payload.direction === "out" ? "out" : "in");
      bubble.textContent = record.payload.text || (record.payload.media ? tr("Attachment") : "");
      meta.textContent = (record.payload.direction === "out" ? tr("Sent") : tr("Received")) + " · " +
        String(record.observed_at || "").replace("T", " ").slice(0, 19) + " UTC · " + tr("Record #{n}", {n: record.seq});
      bubble.append(meta); thread.append(bubble);
    }
    card.append(thread);
    const actions = document.createElement("div"); actions.className = "secret-actions";
    if (chat.state === "requested" && !chat.outbound) actions.append(secretButton(tr("Accept"), "accept", chat.id, "primary"));
    if (chat.state === "ready") {
      const field = document.createElement("input"); field.type = "text"; field.maxLength = 4096; field.dataset.chat = String(chat.id);
      field.placeholder = tr("Message"); field.setAttribute("aria-label", tr("Message")); field.value = secretDrafts[chat.id] || "";
      actions.append(field, secretButton(tr("Send"), "send", chat.id, "primary"));
    }
    if (chat.state !== "closed") actions.append(secretButton(tr("End chat"), "close", chat.id, "quiet"));
    card.append(actions); list.append(card);
  }
}
const secretStates = {requested: "Waiting for the other side", ready: "Established", closed: "Ended"};
async function secretAction(path, body) {
  actionError = "";
  try {const result = await api(path, body); secretSignature = ""; renderSecret(result.secret);}
  catch (error) {actionError = error.message;}
  renderError();
}
$("secret-start").onclick = () => {
  const user = peerValue($("secret-new").value);
  if (!SECRET_PEER.test(user)) {actionError = peerHint(); renderError(); return;}
  secretAction("secret/create", {user}).then(() => {if (!actionError) $("secret-new").value = "";});
};
$("secret-chats").addEventListener("click", event => {
  const button = event.target.closest("button[data-secret-action]"); if (!button) return;
  const id = button.dataset.chat, action = button.dataset.secretAction;
  if (action === "send") {
    const field = $("secret-chats").querySelector(`input[data-chat="${id}"]`), text = field.value.trim();
    if (!text) return;
    secretAction(`secret/${id}/send`, {text}).then(() => {if (!actionError) {secretDrafts[id] = ""; field.value = "";}});
  } else secretAction(`secret/${id}/${action}`, {});
});
$("secret-chats").addEventListener("keydown", event => {
  if (event.key === "Enter" && event.target.matches("input[data-chat]")) {
    event.preventDefault(); event.target.parentElement.querySelector('button[data-secret-action="send"]')?.click();
  }
});
const chatCategories = ["personal", "bots", "private_groups", "public_groups", "private_channels", "public_channels"];
const mediaTypes = {photo: 20, video: 100, animation: 20, video_note: 50, voice: 20, audio: 50, sticker: 5, document: 50};
const mediaNames = {photo: "Photos", video: "Videos", animation: "Animations", video_note: "Video messages",
  voice: "Voice messages", audio: "Audio", sticker: "Stickers", document: "Documents"};
function translatedText(text, tag = "span") {
  const element = document.createElement(tag); element.dataset.i18n = ""; element.textContent = text; return element;
}
for (const [kind, limit] of Object.entries(mediaTypes)) {
  const row = document.createElement("div"), label = document.createElement("label"), check = document.createElement("input");
  check.type = "checkbox"; check.id = "type-" + kind; check.checked = true;
  label.append(check, " ", translatedText(mediaNames[kind])); row.append(label);
  const sizeLabel = document.createElement("label"), size = document.createElement("input");
  size.type = "number"; size.id = "limit-" + kind; size.min = "1"; size.max = "2000"; size.value = String(limit);
  sizeLabel.append(translatedText("Download limit (MiB)"), " ", size); row.append(sizeLabel);
  const action = document.createElement("select"); action.id = "action-" + kind; action.setAttribute("aria-label", kind + " action");
  for (const [value, text] of [["", "Use selected attachment action"], ["download", "Download"], ["hashes_only", "Hashes only"], ["exclude", "Skip"]]) {
    const option = translatedText(text, "option"); option.value = value; action.append(option);
  }
  row.append(action); $("media-rules").append(row);
}
// Presets never drop a file type: types that are not downloaded keep Telegram server hashes.
const mediaPresets = {
  all: Object.keys(mediaTypes),
  light: ["photo", "voice", "video_note", "document"],
  photos: ["photo"],
  messages: []};
let applyingPreset = false;
function applyPreset() {
  const download = mediaPresets[$("media-preset").value];
  if (!download) return;
  applyingPreset = true;
  $("media-action").value = download.length ? "download" : "hashes_only";
  $("oversized-media").value = "hashes_only";
  for (const kind of Object.keys(mediaTypes)) {
    $("type-" + kind).checked = true;
    $("limit-" + kind).value = String(commonLimit());
    $("action-" + kind).value = download.length && !download.includes(kind) ? "hashes_only" : "";
  }
  applyingPreset = false;
}
$("common-limit").addEventListener("input", () => {
  $("common-limit-value").textContent = commonLimit() + " MB";
  if ($("media-preset").value === "custom") for (const kind of Object.keys(mediaTypes)) $("limit-" + kind).value = String(commonLimit());
  else applyPreset();
});
$("media-preset").addEventListener("change", applyPreset);
$("media-rules").addEventListener("change", () => { if (!applyingPreset) $("media-preset").value = "custom"; });
$("media-action").addEventListener("change", () => { if (!applyingPreset) $("media-preset").value = "custom"; });
applyPreset();
function selection() {
  const investigation = $("export-mode").value === "chats", secret = $("export-mode").value === "secret";
  const journal = $("export-mode").value === "journal" || investigation || secret;
  const selected = Array.from($("chats").selectedOptions, option => Number(option.value));
  if (investigation && selected.length > 50) throw new Error(tr("Select at most 50 chats for one run."));
  if (secret) {
    const peer = peerValue($("secret-peer").value);
    if (peer && !SECRET_PEER.test(peer)) throw new Error(peerHint());
    if (!peer && !$("secret-accept").checked) throw new Error(tr("Name a user to start a secret chat with, or accept secret chats started by others."));
  }
  if (!secret && (journal || $("export-scope").value === "chat") && !selected.length) {
    throw new Error(tr("Load chats and select at least one."));
  }
  const types = {};
  for (const kind of Object.keys(mediaTypes)) {
    const field = $("limit-" + kind);
    if (!field.checkValidity() || !Number.isInteger(Number(field.value))) throw new Error(tr("Download limits must be whole numbers from 1 to 2000 MiB."));
    types[kind] = {enabled: $("type-" + kind).checked, max_mb: Number(field.value), action: $("action-" + kind).value || null};
  }
  const options = {transport: $("export-mode").value, export_format: $("export-format").value,
    chat_ids: $("export-scope").value === "account" ? [] : selected,
    chat_kinds: chatCategories.some(name => $("cat-" + name).checked) ? ["private", "bot", "group", "supergroup", "channel"] : [],
    chat_categories: chatCategories.filter(name => $("cat-" + name).checked),
    own_only_categories: ["private_groups", "public_groups"].filter(name => $("cat-" + name).checked && $("own-" + name).checked),
    include_archived: $("account-archived").checked, own_messages_only: false,
    messages_first: true, media_action: $("media-action").value, oversized_media: $("oversized-media").value,
    max_media_file_mib: 2000, max_total_gib: Number($("total-budget").value), budget_exhausted: "hashes_only",
    media_types: Object.keys(types).filter(k => types[k].enabled).map(k => k === "video_note" ? "video_message" : k),
    media_rules: Object.fromEntries(Object.entries(types).map(([k, rule]) => [k === "video_note" ? "video_message" : k, rule])),
    from_utc: $("from-date").value ? $("from-date").value + "T00:00:00Z" : null,
    to_utc: $("through-date").value ? new Date(Date.parse($("through-date").value + "T00:00:00Z") + 86400000).toISOString() : null,
    include_profile: $("account-profile").checked, include_contacts: $("account-contacts").checked,
    include_profile_photos: $("account-photos").checked, include_stories: $("account-stories").checked,
    include_session_metadata: $("account-sessions").checked, include_other_data: $("account-other").checked};
  const accountMode = !journal;
  if (accountMode) {
    if (!$("total-budget").checkValidity() || !Number.isInteger(options.max_total_gib)) throw new Error(tr("Enter a whole media budget from 1 to 1024 GiB."));
    if (options.to_utc && options.from_utc && options.to_utc <= options.from_utc) throw new Error(tr("The end date must be on or after the start date."));
    if ($("include-avatars").checked) throw new Error("Participant avatar capture is available in single-chat regular capture. For account export use Account profile photos.");
    return {mode: "account", account_scope: $("export-scope").value === "account" ? "all" : "selected", account_options: options};
  }
  const capture = {download_media: true, media_action: $("media-action").value,
    oversized_media: $("oversized-media").value, include_avatars: $("include-avatars").checked,
    messages_first: $("messages-first").checked, preserve_ephemeral_media: $("preserve-ephemeral-media").checked, types};
  if (investigation) return {mode: "chats", chat_ids: selected, capture};
  if (secret) return {mode: "secret", secret_peer: peerValue($("secret-peer").value) || null, accept_incoming: $("secret-accept").checked, capture};
  return {chat_id: Number($("chats").value), capture};
}
let assessedSelection = null, assessmentResult = null;
function describeMode() {
  const mode = $("export-mode").value;
  $("mode-description").textContent = mode === "secret" ? tr(
    "A secret chat lives only on the two devices. This runner becomes one of them: it starts or accepts the chat, keeps every message and file as they arrive, and signs them into the journal. Nothing from before the run can be recovered.") : mode === "auto" ? tr(
    "Uses Takeout when Telegram allows it and the regular API otherwise. This runner signs in fresh, and Telegram usually refuses Takeout for sessions younger than 24 hours, so expect the regular API. The archive records which method was used.") : mode === "takeout" ? tr(
    "Takeout only. Telegram usually refuses it for a session signed in less than 24 hours ago, and this runner always signs in fresh, so the capture may stop waiting for approval. Prefer Automatic.") : mode === "regular" ? tr(
    "Regular API cannot enumerate groups and channels you left, and contacts include Telegram users rather than the full saved phone contact list. Rate limits still apply.") : mode === "chats" ? tr(
    "Each selected chat becomes its own signed chat archive: full visible history, files by your rules, everyone who wrote with message counts and first and last message, the chat card, the admin log when this account can read it, and missing message-ID ranges rechecked one by one. Works for chats with content protection.") : tr(
    "One chat, its history and changes observed while this runner is active.");
  $("chat-help").textContent = mode === "journal" ? tr("Choose one chat.") : mode === "chats" ? tr(
    "Select up to 50 chats. They are exported one after another, in this list's order.") : tr(
    "Select one or more chats, use Ctrl or Cmd with a click to add another, or Shift with arrow keys. An empty selection cannot start an account export.");
}
function clearAssessment() {
  assessedSelection = null; assessmentResult = null; $("save-selection").disabled = true;
  $("preflight-result").textContent = ""; $("preflight-details").hidden = true;
  $("preflight-budget").textContent = ""; $("budget-actions").hidden = true;
  $("budget-plan").hidden = true; $("budget-fit").hidden = true; $("plan-summary").hidden = true;
  for (const name of ["private_groups", "public_groups"]) {
    $("own-" + name).disabled = !$("cat-" + name).checked;
    if ($("own-" + name).disabled) $("own-" + name).checked = false;
  }
  const investigation = $("export-mode").value === "chats", secret = $("export-mode").value === "secret";
  const journal = $("export-mode").value === "journal" || investigation || secret;
  $("secret-options").hidden = !secret;
  $("chat-picker").closest("section").hidden = secret;
  $("preflight").hidden = secret;
  document.querySelectorAll("#capture-settings .account-only").forEach(element => {element.hidden = journal;});
  $("export-scope").disabled = journal;
  $("export-format").disabled = journal;
  const card = document.querySelector(`input[name="mode-card"][value="${journal ? (investigation ? "chats" : secret ? "secret" : "journal") : "account"}"]`);
  if (card && !card.checked) card.checked = true;
  if (!journal) $("export-method").value = $("export-mode").value;
  $("account-other").disabled = $("export-mode").value !== "takeout";
  if ($("account-other").disabled) $("account-other").checked = false;
  $("takeout-notice").hidden = $("export-mode").value !== "takeout";
  $("account-note").hidden = journal;
  $("include-avatars").disabled = !journal;
  $("include-avatars").parentElement.hidden = !journal;
  if (!journal) $("include-avatars").checked = false;
  $("messages-first").disabled = !journal;
  $("preserve-ephemeral-media").disabled = !journal;
  $("preserve-ephemeral-media").parentElement.hidden = !journal;
  if (!journal) $("messages-first").checked = true;
  $("chat-picker").hidden = secret || (!journal && $("export-scope").value === "account");
  $("chats").multiple = !journal || investigation; $("chats").size = journal && !investigation ? 1 : 8;
  if (journal && !investigation) {
    const chosen = Array.from($("chats").selectedOptions);
    chosen.slice(1).forEach(option => {option.selected = false;});
  }
  syncChatList();
  $("collect").disabled = secret ? !(SECRET_PEER.test(peerValue($("secret-peer").value)) || $("secret-accept").checked)
    : !$("chat-picker").hidden && !$("chats").selectedOptions.length;
  $("preflight").disabled = $("collect").disabled;
  describeMode();
}
$("capture-settings").addEventListener("input", clearAssessment);
$("capture-settings").addEventListener("change", clearAssessment);
clearAssessment();
translate();
bind("preflight", async () => {
  const options = selection(), stamp = JSON.stringify(options);
  $("preflight-result").textContent = tr("Checking disk and up to 25 recent messages per sampled chat…");
  const result = await api("preflight", options);
  if (JSON.stringify(selection()) !== stamp || $("selection").hidden) return;
  assessmentResult = result; renderAssessment(result);
  $("preflight-json").textContent = JSON.stringify(result, null, 2); $("preflight-details").hidden = false;
  assessedSelection = result.selection; $("save-selection").disabled = !assessedSelection;
  $("collect").disabled = !result.can_start;
});
function renderAssessment(result) {
  const format = humanBytes;
  $("preflight-result").textContent = (result.can_start ? tr("Settings accepted.") : tr("Cannot start with these resources.")) +
    ((result.issues || []).length ? " " + result.issues.map(issue => tr(issue.message)).join(" ") : "");
  const plan = result.time_plan;
  if (!plan) return;
  const minutes = seconds => Math.ceil(seconds / 60), states = {
    estimated_fit: tr("Fits the time estimate."),
    over_budget: tr("The selected volume exceeds the available time."),
    no_collection_time: tr("Only archive preparation time remains."),
    unknown: tr("Not all selected data could be measured.")};
  renderSummary(plan, states[plan.fit] || "");
  $("preflight-budget").textContent = tr("Download assumption: 1 MiB/s with a 2× time margin.") +
    (plan.approval === "not_requested" ? " " + tr("Takeout approval time will be added when Telegram reports it.") : "") +
    (plan.files_exceed_budget ? " " + tr("Estimated files also exceed the selected download budget.") : "");
  $("budget-actions").hidden = !plan.suggestions.length;
  $("budget-messages").hidden = !plan.suggestions.includes("messages_only");
  $("budget-chats").hidden = !plan.suggestions.includes("fewer_chats") || $("export-mode").value === "journal";
  renderPlan(plan, format);
}
function humanBytes(bytes) {
  const value = Number(bytes) || 0, units = ["B", "KiB", "MiB", "GiB", "TiB"];
  let size = value, unit = 0;
  const digitsFor = value => unit === 0 || value >= 10 ? 0 : 1;
  const rounded = value => Math.round(value * 10 ** digitsFor(value)) / 10 ** digitsFor(value);
  while (rounded(size) >= 1024 && unit < units.length - 1) {size /= 1024; unit++;}
  const digits = digitsFor(size);
  return size.toLocaleString(lang, {maximumFractionDigits: digits}) + " " + units[unit];
}
function renderSummary(plan, verdict) {
  const box = $("plan-summary"), needed = Math.ceil((plan.acquisition_seconds + plan.sealing_reserve_seconds) / 60);
  const available = Math.ceil(plan.remaining_seconds / 60);
  box.replaceChildren();
  const status = document.createElement("p"); status.className = "plan-verdict " + plan.fit; status.textContent = verdict;
  const tiles = document.createElement("div"); tiles.className = "plan-tiles";
  for (const [value, label] of [[tr("{n} min", {n: needed}), tr("Needed, including archive preparation")],
      [tr("{n} min", {n: available}), tr("Left in this session")],
      [Number(plan.messages_to_read || 0).toLocaleString(lang), tr("Messages to read")],
      [humanBytes(plan.download_bytes), tr("Files to download")]]) {
    const tile = document.createElement("div"), strong = document.createElement("strong"), span = document.createElement("span");
    strong.textContent = value; span.textContent = label; tile.append(strong, span); tiles.append(tile);
  }
  box.append(status, tiles); box.hidden = false;
}
function chatName(id) {
  const option = Array.from($("chats").options).find(item => Number(item.value) === id);
  return option ? option.textContent : tr("Chat {id}", {id});
}
function renderPlan(plan, format) {
  const rows = plan.per_chat || [], body = $("budget-table").tBodies[0];
  body.replaceChildren();
  for (const chat of rows) {
    const row = document.createElement("tr");
    for (const value of [chatName(chat.chat_id), chat.unknown ? "?" : (chat.messages || 0).toLocaleString(),
      chat.unknown ? "?" : format(chat.download_bytes) + (chat.unknown_size_files ? " +" : ""),
      chat.unknown ? tr("not measured") : tr("{n} min", {n: Math.ceil((chat.seconds || 0) / 60)})]) {
      const cell = document.createElement("td"); cell.textContent = value; row.append(cell);
    }
    if (plan.fit !== "estimated_fit" && (plan.fits_now || []).includes(chat.chat_id)) row.className = "fits";
    body.append(row);
  }
  const measured = rows.filter(chat => !chat.unknown);
  if (rows.length > 1) {
    const total = document.createElement("tr"); total.className = "total";
    for (const value of [tr("Total"), measured.reduce((sum, chat) => sum + (chat.messages || 0), 0).toLocaleString(lang),
        humanBytes(measured.reduce((sum, chat) => sum + (chat.download_bytes || 0), 0)),
        tr("{n} min", {n: Math.ceil(measured.reduce((sum, chat) => sum + (chat.seconds || 0), 0) / 60)})]) {
      const cell = document.createElement("td"); cell.textContent = value; total.append(cell);
    }
    body.append(total);
  }
  $("budget-legend").hidden = !body.querySelector("tr.fits");
  const recommended = plan.recommended_session_minutes;
  $("budget-recommendation").textContent = plan.fit === "estimated_fit" ? tr(
    "Everything selected fits this run.") : recommended ? tr(
    "This selection needs a {minutes}-minute session. Finish or cancel this run and start a new one with {minutes} minutes, or keep only the chats that fit.",
    {minutes: recommended}) : (plan.split_runs || []).length ? tr(
    "Even the longest session, {minutes} minutes, is not enough for everything selected.",
    {minutes: plan.split_runs[0].session_minutes}) : tr(
    "Not all selected data could be measured, so no session length can be recommended.");
  const list = $("budget-run-list"); list.replaceChildren();
  for (const run of plan.split_runs || []) {
    const item = document.createElement("li");
    item.textContent = run.chat_ids.map(chatName).join(", ") + " — " + (run.unmeasured ? tr("not measured") :
      tr("about {n} min of {total}", {n: Math.ceil(run.seconds / 60), total: run.session_minutes})) +
      (run.exceeds_one_run ? " — " + tr("too large for one run: limit the dates") : "");
    list.append(item);
  }
  $("budget-runs").hidden = !(plan.split_runs || []).length;
  const fits = plan.fits_now || [];
  $("budget-fit").hidden = plan.fit === "estimated_fit" || !fits.length || fits.length === rows.length || $("export-mode").value === "journal";
  $("budget-fit").dataset.chats = JSON.stringify(fits);
  $("budget-plan").hidden = !rows.length;
}
$("budget-fit").onclick = () => {
  const keep = new Set(JSON.parse($("budget-fit").dataset.chats || "[]"));
  $("export-scope").value = "chat"; clearAssessment();
  const options = Array.from($("chats").options);
  if (!options.length) { $("dialog-note").textContent = tr("Load my chats first, then press this button again."); $("refresh").focus(); return; }
  for (const option of options) option.selected = keep.has(Number(option.value));
  clearAssessment(); $("preflight").click();
};
$("budget-messages").onclick = () => {
  $("media-preset").value = "messages"; applyPreset();
  for (const id of ["include-avatars", "preserve-ephemeral-media", "account-photos", "account-stories", "account-other"]) $(id).checked = false;
  clearAssessment(); $("preflight").click();
};
$("budget-chats").onclick = () => {$("export-scope").value = "chat"; clearAssessment(); ($("chat-search").hidden ? $("refresh") : $("chat-search")).focus();};
$("save-selection").onclick = () => {
  if (!assessedSelection) return;
  const url = URL.createObjectURL(new Blob([JSON.stringify(assessedSelection, null, 2) + "\n"], {type: "application/json"}));
  const link = document.createElement("a"); link.href = url; link.download = "sealed-export-settings.json";
  document.body.append(link); link.click(); link.remove(); setTimeout(() => URL.revokeObjectURL(url), 1000);
};
bind("collect", () => api("collect", selection()));
bind("resume", () => api("resume", {}));
bind("finish", () => api("finish", {}));
bind("cancel", () => api("cancel", {}));
let polling = false;
function renderError() {
  $("error").textContent = lastState?.revocation === "not_confirmed" ? tr(
    "Session revocation was not confirmed. End this session in Telegram Settings > Devices.") : connectionFailed ? statusError || tr(
    "Connection unavailable. The runner may be finishing, check GitHub Artifacts.") : !token ? tr(
    "Open the connection file with your private key in the setup helper first.") :
    actionError || (lastState?.phase === "collecting" ? lastState.account_export?.error || "" : "");
}
function chatSummary(state) {
  const history = state.history, media = state.media || {};
  const pending = ["queued", "retry", "running", "cancelled"].reduce((sum, key) => sum + (media[key] || 0), 0);
  const complete = history.phase === "complete" && !history.unavailable && !media.failed && !pending;
  return (complete ? tr("History reading completed within the selected scope.") : tr(
    "Partial capture, check the gaps recorded in the archive.")) + " " + tr(
    "Messages preserved: {captured}, unavailable: {unavailable}. Attachments saved: {done}, hashes only: {hashed}, skipped: {skipped}, failed: {failed}, unfinished: {pending}.",
    {captured: history.captured || 0, unavailable: history.unavailable || 0, done: media.done || 0, hashed: media.hashed || 0,
      skipped: media.skipped || 0, failed: media.failed || 0, pending});
}
const STEPS = ["login", "choose", "capture", "seal"];
function renderSteps(state) {
  const step = state.phase === "login" ? (state.authorized ? "choose" : "login") : state.phase === "collecting" ? "capture" : "seal";
  const index = STEPS.indexOf(step), stopped = ["cancelled", "failed"].includes(state.phase);
  for (const item of $("steps").children) {
    const at = STEPS.indexOf(item.dataset.step);
    item.classList.toggle("done", at < index || state.phase === "sealed" && at === index);
    item.classList.toggle("current", at === index && state.phase !== "sealed" && !stopped);
    item.classList.toggle("stopped", at === index && stopped);
    if (at === index) item.setAttribute("aria-current", "step"); else item.removeAttribute("aria-current");
  }
}
function renderState(state) {
    const terminal = ["sealed", "cancelled", "failed"].includes(state.phase);
    renderSteps(state);
    $("login").hidden = state.authorized || state.phase !== "login";
    $("selection").hidden = !state.authorized || state.phase !== "login";
    $("code-box").hidden = state.login !== "login_required";
    $("password-box").hidden = state.login !== "password_required";
    $("progress").hidden = state.phase !== "collecting";
    $("complete").hidden = state.phase !== "sealed";
    const account = state.account_export;
    $("complete-summary").textContent = account ?
      (account.phase === "done" ? tr("Export completed within the selected scope.") : tr("Partial export: some selected data could not be acquired.")) + " " + tr(
        "{messages} messages preserved, {failures} recorded failures. See coverage details in the archive.",
        {messages: account.counts?.messages || 0, failures: account.coverage?.failures || 0}) : chatSummary(state);
    if (state.revocation === "revoked") $("complete-summary").textContent += " " + tr(
      "Telegram session revocation confirmed.");
    $("capture-messages").textContent = String(account ? Math.max(account.counts?.messages || 0, account.acquisition?.messages_preserved || 0) : state.history.captured || 0);
    $("capture-unavailable").textContent = String(account ? account.coverage?.failures || 0 : state.history.unavailable || 0);
    $("capture-remaining").textContent = String(Math.ceil(state.remaining_seconds / 60));
    const budget = state.time_budget;
    $("capture-budget").textContent = budget ? tr(
      "Collection time left: {collection} min, reserved for the archive: {sealing} min.",
      {collection: Math.ceil(budget.collection_seconds / 60), sealing: Math.ceil(budget.sealing_reserve_seconds / 60)}) +
      (budget.estimated_remaining_seconds == null ? "" : " " + tr("Current completion estimate: {minutes} min.",
        {minutes: Math.ceil(budget.estimated_remaining_seconds / 60)})) +
      (budget.fit === "wait_exceeds_window" ? " " + tr("Telegram's reported wait exceeds this session. Approve Takeout from an established session, or finish with the data already saved.") :
       budget.fit === "over_budget" ? " " + tr("At the current rate, the full selection will not fit; collection stops before packaging time.") : "") : "";
    const transfer = account?.active && account.transfer;
    $("capture-transfer").hidden = !transfer;
    const mib = bytes => (bytes / 1024**2).toFixed(2);
    $("capture-transfer").textContent = !transfer ? "" : transfer.total_bytes == null ? tr(
      "Current file: {received} MiB received. The file is preserved after the download completes.", {received: mib(transfer.received_bytes)}) : tr(
      "Current file: {received} MiB received of {total} MiB. The file is preserved after the download completes.",
      {received: mib(transfer.received_bytes), total: mib(transfer.total_bytes)});
    $("resume").hidden = account ? !["paused", "waiting", "failed"].includes(account.phase) || account.active : state.history.phase !== "paused";
    $("resume").textContent = account?.wait_reason === "takeout_approval" ? tr("Check export approval") : tr("Resume paused capture");
    $("cancel").hidden = terminal || state.phase === "sealing";
    $("counts").textContent = JSON.stringify({history: state.history.phase, messages: state.history.captured || 0,
      unavailable: state.history.unavailable || 0, media: state.media, account_export: account, remaining_seconds: state.remaining_seconds}, null, 2);
    $("context").textContent = JSON.stringify({recipient_sha256: state.recipient_sha256, ...state.context,
      selection: state.selection, selection_sha256: state.selection_sha256}, null, 2);
    $("status").textContent = state.phase === "sealed" ? tr("Capture finished. Wait for the encrypted result in GitHub Artifacts.") :
      state.phase === "cancelled" ? tr("Cancelled. No archive will be published.") :
      state.phase === "failed" ? tr("Capture failed. Check this run in GitHub.") :
      state.phase === "sealing" ? tr("Preparing the archive…") :
      state.phase === "collecting" ? tr("Capturing available messages and files…") :
      state.authorized ? tr("Connected. Choose what to export.") :
      tr("Sign in to Telegram to continue.");
    if (account?.wait_reason === "takeout_approval" && state.phase === "collecting") $("status").textContent =
      tr("Telegram requires export approval from another device that was already signed in before this request. The requesting session and a fresh login cannot approve it. After allowing the export there, click Check export approval. Telegram reported {delay} seconds of waiting, this runner has {remaining} seconds left. A new runner may require approval again.",
        {delay: account.delay_seconds, remaining: state.remaining_seconds});
    const chats = state.chat_exports;
    if (chats) {
      const kept = chats.kept || [], saved = kept.reduce((sum, item) => sum + (item.captured || 0), 0) + (chats.current?.captured || 0);
      $("capture-messages").textContent = String(saved);
      $("capture-unavailable").textContent = String(kept.filter(item => !item.complete).length);
      $("complete-summary").textContent = tr("{done} of {total} chats exported completely, {messages} messages saved.",
        {done: kept.filter(item => item.complete).length, total: chats.total, messages: saved}) +
        (state.revocation === "revoked" ? " " + tr("Telegram session revocation confirmed.") : "");
      $("capture-transfer").hidden = chats.current_chat == null;
      $("capture-transfer").textContent = chats.current_chat == null ? "" : tr("Chat {number} of {total}: {captured} messages read.",
        {number: kept.length + 1, total: chats.total, captured: chats.current?.captured || 0});
      $("resume").hidden = true;
    }
    renderSecret(state.phase === "collecting" ? state.secret : null);
    if (state.authorized) {$("api-hash").value = ""; $("phone").value = ""; qrId = null;}
    renderError();
    if (terminal) {ended = true; sessionStorage.removeItem("sealed-access");}
}
async function poll() {
  if (polling || ended) return;
  polling = true;
  try {
    const state = await api("status");
    lastState = state; connectionFailed = false; statusError = ""; renderState(state);
    if (qrId) {const qr = await api("qr/" + encodeURIComponent(qrId));
      if (["expired", "failed", "cancelled"].includes(qr.step)) {qrId = null; $("qr-image").hidden = true;
        actionError = tr("QR expired or failed. Generate another code."); renderError();}}
  } catch (error) {connectionFailed = true; statusError = error.status ? error.message : ""; renderError(); throw error;
  } finally {polling = false;}
}
if (!token) renderError();
else {poll().catch(() => {});
  setInterval(() => {if (!ended) poll().catch(() => {});}, 1500);}
