"use strict";
const $ = id => document.getElementById(id);
const panelLanguage = code => {
  const value = String(code || "").toLowerCase();
  return /^zh-(hant|tw|hk|mo)/.test(value) ? "zh-Hant" : value.split("-")[0];
};
let lang = (navigator.languages?.length ? navigator.languages : [navigator.language || ""])
  .map(panelLanguage)
  .find(code => code === "en" || window.TGW_SEALED_LOCALES?.[code]) || "en";
const RTL = ["ar", "fa", "he", "ur"];
$("language").replaceChildren(...Object.entries(window.TGW_SEALED_LANGUAGES || {en: "English", ru: "Русский"})
  .filter(([code]) => code === "en" || window.TGW_SEALED_LOCALES?.[code])
  .map(([code, name]) => Object.assign(document.createElement("option"), {value: code, textContent: name})));
let qrId = null, ended = false;
let lastState = null, connectionFailed = false, statusError = "", actionError = "";
// Chats left out of an account export from the plan table; changing other settings starts from all chats again.
let droppedChats = new Set();
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
// The live controls under the secret chats offer the same choices as the start screen.
for (const [from, to] of [["vis-read", "live-read"], ["vis-opened", "live-opened"], ["vis-typing", "live-typing"]])
  $(to).replaceChildren(...Array.from($(from).options, option => option.cloneNode(true)));
function translate() {
  document.documentElement.lang = lang;
  document.documentElement.dir = RTL.includes(lang) ? "rtl" : "ltr";
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
  if (!response.ok) throw Object.assign(new Error(tr(data.detail || "Request failed")), {status: response.status});
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
// "+62 878 80918834", "+7 (999) 123-45-67" and "0049 ..." are sent as "+<digits>"; the country code is required.
const phoneValue = value => {
  const text = String(value || "").trim();
  if (!/^\+?[0-9\s().-]{7,32}$/.test(text)) return text;
  const digits = text.replace(/[^0-9]/g, "");
  return "+" + (digits.startsWith("00") ? digits.slice(2) : digits);
};
bind("send-code", async () => {
  await api("phone", {...credentials(), phone: phoneValue($("phone").value)});
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
function secretButton(text, action, id, cls, item) {
  const button = document.createElement("button"); button.type = "button"; button.className = cls;
  button.textContent = text; button.dataset.secretAction = action; button.dataset.chat = String(id);
  if (item !== undefined) button.dataset.item = String(item);
  return button;
}
function renderSecret(secret) {
  $("secret-live").hidden = !secret;
  if (!secret) return;
  const vis = secret.visibility || {};
  for (const [id, key] of [["live-read", "read_receipts"], ["live-opened", "content_opened"], ["live-typing", "typing"]])
    if (document.activeElement !== $(id) && !visibilitySaving && vis[key]) $(id).value = vis[key];
  $("secret-note").textContent = secret.error ? tr("Secret chats reported an error: {error}", {error: secret.error}) :
    secret.notice ? tr("The secret chat could not be started: {reason}", {reason: secret.notice}) :
    secret.interaction_problem ? secret.interaction_problem : !secret.connected ? tr("Connecting secret chats…") :
    !(secret.chats || []).length ? tr("Waiting for a secret chat. Start one above, or ask the other side to start one with this account.") : "";
  const records = secret.records || [];
  const messages = records.filter(r => r.kind === "secret_chat.message");
  const shownKinds = ["secret_chat.message", "secret_chat.action", "secret_chat.file", "secret_chat.peer_read",
    "secret_chat.peer_typing"];
  $("capture-messages").textContent = String(secret.counts ? secret.counts.received + secret.counts.sent : messages.length);
  $("capture-files").textContent = String(secret.counts ? secret.counts.files : records.filter(r => r.kind === "secret_chat.file").length);
  $("capture-unavailable").textContent = String(secret.counts ? secret.counts.notices : records.filter(r => r.kind === "secret_chat.action").length);
  $("capture-unavailable-label").textContent = tr("Service notices");
  const signature = JSON.stringify([secret.chats, records.filter(r => shownKinds.includes(r.kind)).map(r => r.seq),
    secret.pending_files, lang]);
  if (signature === secretSignature) return;
  secretSignature = signature;
  for (const field of $("secret-chats").querySelectorAll("input[data-chat]")) secretDrafts[field.dataset.chat] = field.value;
  // A new message rebuilds the threads: keep each thread's scroll position (or stay at the newest message), open
  // previews and the caret in the message field, so reading or typing is not interrupted.
  const scroll = {}, active = document.activeElement;
  for (const thread of $("secret-chats").querySelectorAll(".secret-thread[data-chat]"))
    scroll[thread.dataset.chat] = {top: thread.scrollTop, end: thread.scrollHeight - thread.scrollTop - thread.clientHeight < 48};
  const typing = active?.matches?.("input[data-chat]") ? {chat: active.dataset.chat, start: active.selectionStart, end: active.selectionEnd} : null;
  const list = $("secret-chats"); list.replaceChildren();
  for (const chat of secret.chats || []) {
    const card = document.createElement("article"), head = document.createElement("header"), title = document.createElement("strong");
    card.className = "secret-card"; title.textContent = personLabel(secret.people, chat.peer_user_id);
    const state = document.createElement("span"); state.className = "secret-state " + chat.state;
    state.textContent = chat.state === "requested" && !chat.outbound ? tr("Waiting for you to accept")
      : tr(secretStates[chat.state] || chat.state);
    head.append(title, state);
    if ((chat.peer_typing || []).length) head.append(chip(tr("{name} is typing…", {name: personLabel(secret.people, chat.peer_user_id).split(" · ")[0]}), "typing"));
    if (chat.key_visualization) {
      const key = document.createElement("code"); key.className = "secret-key";
      key.textContent = (chat.key_visualization.match(/.{1,8}/g) || []).join(" "); head.append(key);
    }
    card.append(head);
    card.append(secretThread(records, chat.id, secret.pending_files, secret.visibility));
    if (chat.state === "ready") {
      const tools = document.createElement("div"), vis = secret.visibility || {};
      tools.className = "secret-tools";
      tools.append(chip(vis.read_receipts === "never" && vis.typing === "hidden" && vis.content_opened === "never"
        ? tr("Invisible: nothing is shown to the other side") : tr("Visible only as chosen; every notice is journaled"), "quiet"));
      if (vis.read_receipts === "on_open") tools.append(chip(tr("Marked as read 5 s after a message appears here"), "quiet"));
      if (vis.read_receipts === "manual") tools.append(secretButton(tr("Mark as read"), "read", chat.id, "chip-button"));
      if (vis.typing === "shown") tools.append(secretButton(tr("Show typing"), "typing", chat.id, "chip-button"));
      card.append(tools);
    }
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
  for (const digest of shownPreviews) {
    const button = list.querySelector(`button[data-secret-action="view"][data-item="${CSS.escape(digest)}"]`);
    if (button && viewed.has(digest)) showPreview(button, viewed.get(digest)); else shownPreviews.delete(digest);
  }
  for (const thread of list.querySelectorAll(".secret-thread[data-chat]")) {
    const was = scroll[thread.dataset.chat], newest = !was || was.end || stickTo === thread.dataset.chat;
    thread.scrollTop = newest ? thread.scrollHeight : was.top;
  }
  stickTo = null;
  autoRead(secret, records);
  const field = typing && list.querySelector(`input[data-chat="${CSS.escape(typing.chat)}"]`);
  if (field) {field.focus({preventScroll: true}); field.setSelectionRange(typing.start, typing.end);}
}
let stickTo = null, visibilitySaving = false;
// Read receipts "5 seconds after it appears here": only while this panel is in view, and once the newest received
// message has been shown for 5 seconds; a newer message restarts the wait. Files are never opened by this.
const AUTO_READ_MS = 5000, autoTimers = {}, autoDone = {};
let lastSecretForRead = null;
function autoRead(secret, records) {
  lastSecretForRead = secret;
  if (secret.visibility?.read_receipts !== "on_open" || document.visibilityState !== "visible") {
    for (const id of Object.keys(autoTimers)) {clearTimeout(autoTimers[id].timer); delete autoTimers[id];}
    return;
  }
  for (const chat of secret.chats || []) {
    if (chat.state !== "ready") continue;
    const newest = records.filter(r => r.kind === "secret_chat.message" && r.payload?.direction === "in" &&
      String(r.payload.secret_chat_id) === String(chat.id)).reduce((max, r) => Math.max(max, r.seq), 0);
    if (!newest || newest <= (autoDone[chat.id] || 0) || autoTimers[chat.id]?.seq === newest) continue;
    clearTimeout(autoTimers[chat.id]?.timer);
    autoTimers[chat.id] = {seq: newest, timer: setTimeout(async () => {
      delete autoTimers[chat.id];
      if (document.visibilityState !== "visible") return;
      try {
        const result = await api(`secret/${chat.id}/read`, {trigger: "on_open", shown_seconds: AUTO_READ_MS / 1000});
        autoDone[chat.id] = newest; secretSignature = ""; renderSecret(result.secret);
      } catch (error) {actionError = error.message; renderError();}
    }, AUTO_READ_MS)};
  }
}
document.addEventListener("visibilitychange", () => {
  if (lastSecretForRead) autoRead(lastSecretForRead, lastSecretForRead.records || []);
});
for (const id of ["live-read", "live-opened", "live-typing"]) $(id).addEventListener("change", async () => {
  visibilitySaving = true; actionError = "";
  try {
    const result = await api("secret/visibility", {read_receipts: $("live-read").value, content_opened: $("live-opened").value,
      typing: $("live-typing").value});
    secretSignature = ""; renderSecret(result.secret);
  } catch (error) {actionError = error.message;}
  finally {visibilitySaving = false; renderError();}
});
const shownPreviews = new Set();
const secretStates = {requested: "Waiting for the other side", ready: "Established", closed: "Ended"};
const secretMedia = {decryptedMessageMediaPhoto: "Photo", decryptedMessageMediaVideo: "Video",
  decryptedMessageMediaDocument: "File", decryptedMessageMediaAudio: "Audio", decryptedMessageMediaGeoPoint: "Location",
  decryptedMessageMediaVenue: "Venue", decryptedMessageMediaContact: "Contact", decryptedMessageMediaExternalDocument: "Sticker",
  decryptedMessageMediaWebPage: "Link preview"};
const stamp = record => String(record.observed_at || "").replace("T", " ").slice(0, 19) + " UTC · " + tr("Record #{n}", {n: record.seq});
function secretEvent(record) {
  const action = record.payload?.action, details = record.payload?.details || {};
  const ids = details.random_ids || record.payload?.random_ids || [];
  const text = action === "SetMessageTTL" ? (details.ttl_seconds ? tr("The other side set the self-destruct timer to {seconds} s", {seconds: details.ttl_seconds})
      : tr("The other side turned the self-destruct timer off"))
    : action === "ScreenshotMessages" ? tr("The other side took a screenshot")
    : action === "DeleteMessages" ? tr("The other side deleted messages ({count}); TgWitness keeps them", {count: ids.length})
    : action === "FlushHistory" ? tr("The other side cleared the history; TgWitness keeps every message")
    : action === "ReadMessages" ? tr("The other side opened self-destructing content")
    : tr("Service notice: {action}", {action: action || "?"});
  const line = document.createElement("p"); line.className = "secret-event" + (action === "ScreenshotMessages" || action === "DeleteMessages" ? " alert" : "");
  line.textContent = text;
  const meta = document.createElement("small"); meta.textContent = stamp(record); line.append(meta);
  return line;
}
const TYPING_ACTIONS = {Typing: "typing", RecordAudio: "recording a voice message", UploadAudio: "sending a voice message",
  RecordRound: "recording a video message", UploadRound: "sending a video message", UploadPhoto: "sending a photo",
  UploadVideo: "sending a video", RecordVideo: "recording a video", UploadDocument: "sending a file"};
function typingEvent(record) {
  const p = record.payload || {}, from = String(p.started_at || "").slice(11, 19), to = String(p.last_seen_at || "").slice(11, 19);
  const seconds = Math.max(1, Math.round((Date.parse(p.last_seen_at) - Date.parse(p.started_at)) / 1000) || 1);
  const what = (p.actions || ["Typing"]).map(name => tr(TYPING_ACTIONS[name] || "typing")).join(", ");
  const line = document.createElement("p"); line.className = "secret-event typing";
  line.textContent = tr("The other side was {what} · {from}–{to} UTC, {seconds} s", {what, from, to, seconds});
  const meta = document.createElement("small"); meta.textContent = stamp(record); line.append(meta);
  return line;
}
const chip = (text, cls) => Object.assign(document.createElement("span"), {className: "secret-chip " + (cls || ""), textContent: text});
const succeeded = (records, kind) => {
  const done = new Set(records.filter(r => r.kind === kind + "_result" && r.payload?.status === "succeeded").map(r => r.payload.request_event));
  return records.filter(r => r.kind === kind + "_requested" && done.has(r.seq));
};
function secretThread(records, chatId, pending, vis) {
  const mine = records.filter(r => String(r.payload?.secret_chat_id) === String(chatId));
  const files = new Map(mine.filter(r => r.kind === "secret_chat.file").map(r => [String(r.payload.random_id), r.payload]));
  const deleted = new Set(mine.filter(r => r.kind === "secret_chat.action" && r.payload?.action === "DeleteMessages")
    .flatMap(r => (r.payload.details?.random_ids || []).map(String)));
  // Notices this panel sent: read receipts cover messages up to a time; opened notices name messages.
  const readUpTo = succeeded(mine, "secret_chat.read").map(r => ({at: Date.parse(r.payload.max_date_at), when: r.observed_at}))
    .filter(item => Number.isFinite(item.at)).sort((a, b) => b.at - a.at)[0];
  const opened = new Map(succeeded(mine, "secret_chat.contents").flatMap(r => (r.payload.random_ids || []).map(id => [String(id), r.observed_at])));
  const time = value => String(value || "").slice(11, 19);
  const thread = document.createElement("div"); thread.className = "secret-thread"; thread.dataset.chat = String(chatId);
  // The other side's read receipts name the date of the newest message they read; Telegram dates a sent message
  // after this panel started sending it. Opened notices name the self-destructing messages they opened.
  const theirReads = mine.filter(r => r.kind === "secret_chat.peer_read").map(r => ({max: Date.parse(r.payload.max_date_at),
    when: r.payload.read_at || r.observed_at})).filter(item => Number.isFinite(item.max));
  const theirOpens = new Map(mine.filter(r => r.kind === "secret_chat.action" && r.payload?.action === "ReadMessages")
    .flatMap(r => (r.payload.random_ids || r.payload.details?.random_ids || []).map(id => [String(id), r.observed_at])));
  const shown = mine.filter(r => ["secret_chat.message", "secret_chat.action", "secret_chat.peer_typing"].includes(r.kind)).slice(-60);
  for (const record of shown) {
    if (record.kind === "secret_chat.action") {thread.append(secretEvent(record)); continue;}
    if (record.kind === "secret_chat.peer_typing") {thread.append(typingEvent(record)); continue;}
    const p = record.payload, id = String(p.random_id), incoming = p.direction !== "out";
    const bubble = document.createElement("div"), meta = document.createElement("small"), status = document.createElement("div");
    bubble.className = "secret-bubble " + (incoming ? "in" : "out") + (deleted.has(id) ? " deleted" : "");
    bubble.dataset.kind = p.media ? secretMedia[p.media._] || "" : "";
    const file = files.get(id);
    if (p.media) {
      const media = document.createElement("span"), parts = [tr(secretMedia[p.media._] || "Attachment")];
      if (p.media.duration) parts.push(tr("{seconds} s", {seconds: p.media.duration}));
      if (p.media.size) parts.push(humanBytes(p.media.size));
      media.className = "secret-media"; media.textContent = parts.join(" · "); bubble.append(media);
    }
    const body = p.text || p.media?.caption;
    if (body) bubble.append(Object.assign(document.createElement("span"), {className: "secret-text", textContent: body}));
    status.className = "secret-status";
    if (p.media) status.append(file ? chip(tr("Saved · SHA-256 {hash}", {hash: String(file.media_sha256 || "").slice(0, 12) + "…"}), "ok")
      : chip(pending ? tr("Downloading…") : tr("Not saved: see the journal"), pending ? "" : "bad"));
    else status.append(chip(tr("Saved"), "ok"));
    if (p.ttl) status.append(chip(tr("Timer {seconds} s · kept here", {seconds: p.ttl}), "warn"));
    if (deleted.has(id)) status.append(chip(tr("Deleted by the other side · kept here"), "bad"));
    if (!incoming) {
      const from = Math.floor(Date.parse(p.send_started_at || record.observed_at) / 1000) * 1000 - (p.send_started_at ? 0 : 1000);
      const read = theirReads.filter(item => item.max >= from).sort((a, b) => Date.parse(a.when) - Date.parse(b.when))[0];
      status.append(chip(read ? tr("Read by them · {time}", {time: time(read.when)}) : tr("Not read by them yet"), read ? "seen" : "quiet"));
      const openedAt = theirOpens.get(id);
      if (openedAt) status.append(chip(tr("Opened by them · {time}", {time: time(openedAt)}), "seen"));
    }
    if (incoming) {
      // Read receipts cover messages up to a whole second, as sent to Telegram.
      const read = readUpTo && Math.floor(Date.parse(record.observed_at) / 1000) * 1000 <= readUpTo.at;
      status.append(chip(read ? tr("Shown as read · {time}", {time: time(readUpTo.when)}) : tr("Not shown as read"), read ? "seen" : "quiet"));
      if (p.ttl || p.media) {
        const at = opened.get(id);
        if (at) status.append(chip(tr("Opened for them · {time}", {time: time(at)}), "seen"));
        else if (vis?.content_opened === "manual") status.append(secretButton(tr("Open for them"), "opened", chatId, "chip-button", id));
        else status.append(chip(tr("Not opened for them"), "quiet"));
      }
    }
    if (file && /Photo|Video|Audio/.test(secretMedia[p.media?._] || "")) status.append(secretButton(tr("View here"), "view", chatId, "chip-button", file.media_sha256));
    bubble.append(status);
    meta.textContent = (incoming ? tr("Received") : tr("Sent")) + " · " + stamp(record);
    bubble.append(meta); thread.append(bubble);
  }
  return thread;
}
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
// Saved copies are shown from this runner; nothing is sent to Telegram, so the other side is not notified.
const viewed = new Map();
function showPreview(button, url) {
  const bubble = button.closest(".secret-bubble"), kind = bubble.dataset.kind || "", thread = button.closest(".secret-thread");
  const preview = document.createElement(kind === "Video" ? "video" : kind === "Audio" ? "audio" : "img");
  preview.className = "secret-preview"; preview.src = url;
  if (preview.tagName !== "IMG") preview.controls = true; else preview.alt = "";
  // The preview grows the thread after it loads; a thread at its newest message stays there.
  const atEnd = thread && thread.scrollHeight - thread.scrollTop - thread.clientHeight < 48;
  preview.addEventListener(preview.tagName === "IMG" ? "load" : "loadedmetadata", () => {
    if (atEnd && thread) thread.scrollTop = thread.scrollHeight;
  }, {once: true});
  button.closest(".secret-status").after(preview); button.textContent = tr("Hide");
}
async function viewSecretFile(button) {
  const digest = button.dataset.item, bubble = button.closest(".secret-bubble");
  const shown = bubble.querySelector(".secret-preview");
  if (shown) {shown.remove(); shownPreviews.delete(digest); button.textContent = tr("View here"); return;}
  button.disabled = true; actionError = "";
  try {
    if (!viewed.has(digest)) {
      const response = await fetch("/api/secret/media/" + digest, {headers: {"Authorization": "Bearer " + token}, cache: "no-store", redirect: "error"});
      if (!response.ok) throw new Error(tr("The saved file could not be opened."));
      viewed.set(digest, URL.createObjectURL(await response.blob()));
    }
    // The thread may have been rebuilt while the file loaded; show it on the current button.
    const current = button.isConnected ? button : $("secret-chats").querySelector(`button[data-secret-action="view"][data-item="${CSS.escape(digest)}"]`);
    if (current && !current.closest(".secret-bubble").querySelector(".secret-preview")) showPreview(current, viewed.get(digest));
    shownPreviews.add(digest);
  } catch (error) {actionError = error.message; renderError();}
  finally {button.disabled = false;}
}
$("secret-chats").addEventListener("click", event => {
  const button = event.target.closest("button[data-secret-action]"); if (!button) return;
  const id = button.dataset.chat, action = button.dataset.secretAction;
  if (action === "view") {viewSecretFile(button); return;}
  if (action === "opened") {secretAction(`secret/${id}/opened`, {random_ids: [button.dataset.item]}); return;}
  if (action === "send") {
    const field = $("secret-chats").querySelector(`input[data-chat="${id}"]`), text = field.value.trim();
    if (!text) return;
    // Cleared before the request: the reply rebuilds the thread, and a failed send puts the text back.
    field.value = ""; secretDrafts[id] = ""; stickTo = id;
    secretAction(`secret/${id}/send`, {text}).then(() => {
      if (!actionError) return;
      const now = $("secret-chats").querySelector(`input[data-chat="${CSS.escape(id)}"]`);
      secretDrafts[id] = text; if (now && !now.value) now.value = text;
    });
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
function keptChats() {
  if (!droppedChats.size) return [];
  return (assessmentResult?.time_plan?.per_chat || []).map(chat => chat.chat_id).filter(id => !droppedChats.has(id));
}
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
    chat_ids: $("export-scope").value === "account" ? keptChats() : selected,
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
    include_session_metadata: $("account-sessions").checked, include_other_data: $("account-other").checked,
    // An investigator's own capture: charts name each sender with @username and ID instead of aliases.
    report_presentation: {participant_labels: "names"}};
  const accountMode = !journal;
  if (accountMode) {
    if (!$("total-budget").checkValidity() || !Number.isInteger(options.max_total_gib)) throw new Error(tr("Enter a whole media budget from 1 to 1024 GiB."));
    if (options.to_utc && options.from_utc && options.to_utc <= options.from_utc) throw new Error(tr("The end date must be on or after the start date."));
    if ($("include-avatars").checked) throw new Error("Participant avatar capture is available in single-chat regular capture. For account export use Account profile photos.");
    return {mode: "account", account_scope: options.chat_ids.length ? "selected" : "all", account_options: options};
  }
  const capture = {download_media: true, media_action: $("media-action").value,
    oversized_media: $("oversized-media").value, include_avatars: $("include-avatars").checked,
    messages_first: $("messages-first").checked, preserve_ephemeral_media: $("preserve-ephemeral-media").checked, types};
  if (investigation) return {mode: "chats", chat_ids: selected, capture};
  if (secret) return {mode: "secret", secret_peer: peerValue($("secret-peer").value) || null, accept_incoming: $("secret-accept").checked,
    secret_visibility: {read_receipts: $("vis-read").value, content_opened: $("vis-opened").value, typing: $("vis-typing").value}, capture};
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
  assessedSelection = null; assessmentResult = null; droppedChats = new Set(); $("save-selection").disabled = true;
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
  const planned = (assessmentResult?.time_plan?.per_chat || []).find(chat => chat.chat_id === id);
  return option ? option.textContent : planned?.title || tr("Chat {id}", {id});
}
// What a start now would hold, chat by chat: messages of all included chats in reading order first, then files.
function forecast(plan) {
  let budget = Math.max(0, (plan.collection_seconds || 0) - (plan.metadata_seconds || 0));
  const result = new Map(), rows = (plan.per_chat || []).filter(chat => !droppedChats.has(chat.chat_id));
  for (const chat of rows) {
    if (chat.unknown) {result.set(chat.chat_id, {messages: "unknown"}); continue;}
    const need = chat.history_seconds ?? chat.seconds ?? 0;
    const share = need <= budget ? 1 : budget > 0 ? budget / need : 0;
    budget = Math.max(0, budget - need);
    result.set(chat.chat_id, {messages: share >= 1 ? "all" : share > 0 ? "part" : "none", share, files: "none"});
  }
  for (const chat of rows) {
    const item = result.get(chat.chat_id);
    if (chat.unknown || item.messages !== "all") continue;
    const need = chat.file_seconds ?? 0;
    item.files = !need || need <= budget ? "all" : budget > 0 ? "part" : "none";
    budget = Math.max(0, budget - need);
  }
  return result;
}
function outcomeOf(chat, item) {
  if (!item) return "dropped";
  if (item.messages === "unknown") return "unknown";
  if (item.messages !== "all") return item.messages;
  return !chat.download_bytes || item.files === "all" ? "all" : "files";
}
function outcomeText(chat, item) {
  const state = outcomeOf(chat, item);
  return [{dropped: tr("Left out"), unknown: tr("not measured"), none: tr("Not reached"), all: tr("Complete"),
    part: item && tr("Newest ~{n} messages", {n: Math.max(1, Math.floor((chat.messages || 0) * (item.share || 0))).toLocaleString(lang)}),
    files: item?.files === "part" ? tr("Messages; files in part") : tr("Messages; no files")}[state], state];
}
function renderPlan(plan, format) {
  const rows = plan.per_chat || [], body = $("budget-table").tBodies[0], outcome = forecast(plan);
  const account = !["chats", "journal", "secret"].includes($("export-mode").value);
  body.replaceChildren();
  for (const chat of rows) {
    const row = document.createElement("tr"), pick = document.createElement("td"), box = document.createElement("input");
    box.type = "checkbox"; box.checked = !droppedChats.has(chat.chat_id); box.disabled = !account || rows.length < 2;
    box.dataset.chat = String(chat.chat_id); box.setAttribute("aria-label", tr("Include {name}", {name: chatName(chat.chat_id)}));
    pick.append(box); row.append(pick);
    const [text, state] = outcomeText(chat, outcome.get(chat.chat_id));
    for (const value of [chatName(chat.chat_id), chat.unknown ? "?" : (chat.messages || 0).toLocaleString(lang),
      chat.unknown ? "?" : format(chat.download_bytes) + (chat.unknown_size_files ? " +" : ""),
      chat.unknown ? tr("not measured") : tr("{n} min", {n: Math.ceil((chat.seconds || 0) / 60)})]) {
      const cell = document.createElement("td"); cell.textContent = value; row.append(cell);
    }
    const result = document.createElement("td"); result.className = "outcome " + state; result.textContent = text; row.append(result);
    if (droppedChats.has(chat.chat_id)) row.className = "dropped";
    body.append(row);
  }
  const kept = rows.filter(chat => !chat.unknown && !droppedChats.has(chat.chat_id));
  if (rows.length > 1) {
    const total = document.createElement("tr"); total.className = "total";
    for (const value of ["", tr("Total"), kept.reduce((sum, chat) => sum + (chat.messages || 0), 0).toLocaleString(lang),
        humanBytes(kept.reduce((sum, chat) => sum + (chat.download_bytes || 0), 0)),
        tr("{n} min", {n: Math.ceil(kept.reduce((sum, chat) => sum + (chat.seconds || 0), 0) / 60)}), ""]) {
      const cell = document.createElement("td"); cell.textContent = value; total.append(cell);
    }
    body.append(total);
  }
  const states = rows.filter(chat => outcome.has(chat.chat_id)).map(chat => outcomeOf(chat, outcome.get(chat.chat_id)));
  const complete = states.filter(state => state === "all").length, missed = states.filter(state => state === "none").length;
  const partial = states.filter(state => state === "part" || state === "files").length;
  const everything = complete === states.length && !droppedChats.size && plan.fit === "estimated_fit";
  $("budget-legend").hidden = true;
  const recommended = plan.recommended_session_minutes;
  $("budget-recommendation").textContent = everything ? tr("Everything selected fits this run.") :
    tr("If started now: {complete} of {total} chats complete, {partial} in part, {missed} not reached.",
      {complete, total: states.length, partial, missed}) + (recommended && !droppedChats.size ? " " + tr(
    "This selection needs a {minutes}-minute session. Finish or cancel this run and start a new one with {minutes} minutes, or keep only the chats that fit.",
    {minutes: recommended}) : (plan.split_runs || []).length && !droppedChats.size && complete < states.length ? " " + tr(
    "Even the longest session, {minutes} minutes, is not enough for everything selected.",
    {minutes: plan.split_runs[0].session_minutes}) : "");
  const list = $("budget-run-list"); list.replaceChildren();
  for (const run of plan.split_runs || []) {
    const item = document.createElement("li");
    item.textContent = run.chat_ids.map(chatName).join(", ") + " — " + (run.unmeasured ? tr("not measured") :
      tr("about {n} min of {total}", {n: Math.ceil(run.seconds / 60), total: run.session_minutes})) +
      (run.exceeds_one_run ? " — " + tr("too large for one run: limit the dates") : "");
    list.append(item);
  }
  $("budget-runs").hidden = !(plan.split_runs || []).length || droppedChats.size > 0 || everything;
  const finished = rows.filter(chat => outcomeOf(chat, outcome.get(chat.chat_id)) === "all").map(chat => chat.chat_id);
  $("budget-fit").hidden = !account || everything || !finished.length || finished.length === states.length;
  $("budget-fit").dataset.chats = JSON.stringify(finished);
  $("budget-order").hidden = !account;
  $("budget-plan").hidden = !rows.length;
}
// The include boxes sit inside the settings form; ticking them must not discard the assessment they belong to.
$("budget-table").addEventListener("input", event => event.stopPropagation());
$("budget-table").addEventListener("change", event => {
  const box = event.target.closest("input[data-chat]");
  if (!box || !assessmentResult?.time_plan) return;
  event.stopPropagation();
  const id = Number(box.dataset.chat), all = (assessmentResult.time_plan.per_chat || []).length;
  if (box.checked) droppedChats.delete(id); else droppedChats.add(id);
  if (droppedChats.size >= all) {droppedChats.delete(id); box.checked = true; return;}
  renderPlan(assessmentResult.time_plan, humanBytes);
});
$("budget-fit").onclick = () => {
  const keep = new Set(JSON.parse($("budget-fit").dataset.chats || "[]"));
  for (const chat of assessmentResult?.time_plan?.per_chat || []) if (!keep.has(chat.chat_id)) droppedChats.add(chat.chat_id);
  renderPlan(assessmentResult.time_plan, humanBytes);
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
let lastSecret = null;
function secretSummary(secret) {
  const counts = secret?.counts;
  if (!counts) return tr("Secret chat capture finished. The archive lists every recorded message, file and notice.");
  return tr("Secret chat capture finished: {messages} messages ({received} received, {sent} sent), {files} files and {notices} service notices are signed into the journal.",
    {messages: counts.received + counts.sent, received: counts.received, sent: counts.sent, files: counts.files, notices: counts.notices});
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
const STAGES = {inventory: "Reading the chat list", inventory_left: "Reading the channels and groups this account has left",
  checking: "Checking each chat before reading it", messages: "Reading messages", files: "Downloading files",
  waiting: "Waiting for Telegram", packaging: "Packaging the signed archive"};
const count = value => Number(value || 0).toLocaleString(lang);
function duration(seconds) {
  const total = Math.round((Number(seconds) || 0) / 60);
  return total < 1 ? tr("under a minute") : total < 60 ? tr("{n} min", {n: total}) :
    tr("{h} h {m} min", {h: Math.floor(total / 60), m: total % 60});
}
function meterPart(label, done, total, text) {
  const row = document.createElement("div"), name = document.createElement("span"), bar = document.createElement("span"),
    fill = document.createElement("span"), value = document.createElement("span");
  row.className = "meter-part"; name.className = "meter-name"; name.textContent = label;
  bar.className = "meter-mini"; value.className = "meter-value"; value.textContent = text;
  if (total) fill.style.width = (Math.min(1, (Number(done) || 0) / total) * 100).toFixed(1) + "%";
  else bar.classList.add("unknown");
  bar.append(fill); row.append(name, bar, value);
  return row;
}
function waitTime(value) {
  const at = typeof value === "number" ? value * 1000 : Date.parse(value);
  return Number.isFinite(at) && at > Date.now() ? new Date(at).toLocaleTimeString(lang, {hour: "2-digit", minute: "2-digit"}) : null;
}
let lastProgress = null;
function renderMeter(progress) {
  $("meter").hidden = !progress;
  if (!progress) return;
  lastProgress = progress;
  const known = progress.percent != null, waiting = progress.stage === "waiting" && waitTime(progress.wait_until);
  $("meter-stage").textContent = tr(STAGES[progress.stage] || "Reading messages");
  $("meter-current").textContent = progress.current ? tr("Now: {name}", {name: progress.current}) : "";
  $("meter-percent").textContent = known ? progress.percent + "%" : "";
  $("meter-bar").classList.toggle("indeterminate", !known);
  $("meter-fill").style.width = known ? progress.percent + "%" : "";
  if (known) $("meter-bar").setAttribute("aria-valuenow", String(progress.percent)); else $("meter-bar").removeAttribute("aria-valuenow");
  $("meter-elapsed").textContent = tr("Elapsed: {time}", {time: duration(progress.elapsed_seconds)});
  $("meter-eta").textContent = waiting ? tr("Telegram asked to wait until {time}", {time: waiting}) :
    progress.stage === "packaging" ? "" : progress.eta_seconds != null ?
    tr("About {time} left, archive included", {time: duration(progress.eta_seconds)}) : "";
  const parts = [], of = (done, total) => tr("{done} of {total}", {done: count(done), total: count(total)});
  const detail = progress.detail;
  if (detail) parts.push(meterPart(tr("Chats checked"), detail.done, detail.total, detail.total ? of(detail.done, detail.total) : count(detail.done)));
  const chats = progress.chats;
  if (chats?.total) parts.push(meterPart(tr("Chats finished"), chats.done, chats.total, of(chats.done, chats.total)));
  const messages = progress.messages || {};
  parts.push(meterPart(tr("Messages"), messages.done, messages.total, messages.total ?
    tr("{done} of about {total}", {done: count(messages.done), total: count(messages.total)}) : count(messages.done)));
  const chat = progress.chat;
  if (chat) parts.push(chat.stage === "files" && chat.files_total ?
    meterPart(tr("Files of this chat"), chat.files_done, chat.files_total, of(chat.files_done, chat.files_total)) :
    meterPart(tr("Messages of this chat"), chat.done, chat.total, chat.total ? of(chat.done, chat.total) : count(chat.done)));
  const files = progress.files;
  if (files && (files.done || files.total || files.bytes || files.bytes_total)) {
    const size = files.bytes ? " · " + (files.bytes_total ? tr("{size} of about {total}", {size: humanBytes(files.bytes), total: humanBytes(files.bytes_total)}) : humanBytes(files.bytes)) : "";
    parts.push(files.total ? meterPart(tr("Files"), files.finished ?? files.done, files.total,
      tr("{done} saved of {total}", {done: count(files.done), total: count(files.total)}) + size) :
      meterPart(tr("Files"), files.bytes, files.bytes_total, count(files.done) + size));
  }
  const transfer = progress.transfer;
  if (transfer) parts.push(meterPart(tr("Current file"), transfer.received_bytes, transfer.total_bytes, transfer.total_bytes ?
    tr("{size} of {total}", {size: humanBytes(transfer.received_bytes), total: humanBytes(transfer.total_bytes)}) : humanBytes(transfer.received_bytes)));
  $("meter-parts").replaceChildren(...parts);
  $("capture-transfer").hidden = true;
  $("capture-messages").textContent = count(messages.done);
  $("capture-files").textContent = count(files?.done);
  $("capture-unavailable").textContent = count(progress.problems);
}
function renderFacts(state) {
  const progress = lastProgress, box = $("complete-facts");
  box.hidden = !progress || state.phase !== "sealed";
  if (box.hidden) return;
  const facts = [[count(progress.messages?.done), tr("Messages")], [count(progress.files?.done), tr("Files saved")]];
  if (progress.chats?.total) facts.push([tr("{done} of {total}", {done: count(progress.chats.done), total: count(progress.chats.total)}), tr("Chats finished")]);
  facts.push([count(progress.problems), tr("Recorded problems")], [duration(progress.elapsed_seconds), tr("Collection time")]);
  box.replaceChildren(...facts.map(([value, label]) => {
    const item = document.createElement("div"), strong = document.createElement("strong"), span = document.createElement("span");
    strong.textContent = value; span.textContent = label; item.append(strong, span); return item;
  }));
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
    if (state.secret?.counts) lastSecret = state.secret;
    renderSteps(state);
    $("login").hidden = state.authorized || state.phase !== "login";
    $("selection").hidden = !state.authorized || state.phase !== "login";
    $("code-box").hidden = state.login !== "login_required";
    $("password-box").hidden = state.login !== "password_required";
    $("progress").hidden = !["collecting", "sealing"].includes(state.phase);
    $("finish").hidden = state.phase !== "collecting";
    $("complete").hidden = state.phase !== "sealed";
    const account = state.account_export;
    $("complete-summary").textContent = account ?
      (account.phase === "done" ? tr("Export completed within the selected scope.") : tr("Partial export: some selected data could not be acquired.")) + " " + tr(
        "{messages} messages preserved, {failures} recorded failures. See coverage details in the archive.",
        {messages: count(Math.max(account.counts?.messages || 0, account.acquisition?.messages_preserved || 0)), failures: count(account.coverage?.failures)}) :
      state.selection?.mode === "secret" ? secretSummary(state.secret?.counts ? state.secret : lastSecret) : chatSummary(state);
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
    if (state.progress && state.phase === "sealed") lastProgress = state.progress;
    renderMeter(["collecting", "sealing"].includes(state.phase) ? state.progress : null);
    renderFacts(state);
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
