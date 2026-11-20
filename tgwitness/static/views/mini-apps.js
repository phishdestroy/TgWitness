const ASKS = {phone: "Phone number", write_access: "Permission to message this account", payment: "Payment",
  link: "Open a link", telegram_link: "Open a Telegram link", data: "Send data to the bot", message: "Send a prepared message",
  inline: "Inline query", download: "File download", clipboard: "Read the clipboard", location: "Location",
  emoji_status: "Emoji status", story: "Post a story", popup: "Pop-up", biometry: "Biometric access",
  home_screen: "Home-screen shortcut"};
const ENTRY = {button: "Button", link: "Link", menu: "Bot menu", main: "Main app"};

export function createMiniApps({node, icon, tr, json, busy, confirm, toast, fmtFull, isAdmin, may, preview, mask, openRecord,
  current}) {
  const shots = new Map();
  let shown = null;

  function text(tag, cls, value) { return node(tag, cls, value == null ? "" : String(value)); }

  function chip(label, value, tone = "") {
    const item = node("span", "mini-chip" + (tone ? " " + tone : ""));
    item.append(node("b", "", String(value)), node("span", "", label));
    return item;
  }

  function section(title, ...content) {
    const box = node("section", "mini-section");
    box.append(node("h3", "", title), ...content.filter(Boolean));
    return box;
  }

  function fold(title, count, build) {
    if (!count) return null;
    const box = node("details", "mini-fold"), summary = node("summary", "");
    summary.append(node("span", "", title), node("span", "mini-count", String(count)));
    box.append(summary);
    box.addEventListener("toggle", () => {if (box.open && box.childElementCount === 1) box.append(build());}, {once: false});
    return box;
  }

  function list(items, row) {
    const box = node("ul", "mini-list");
    for (const item of items) box.append(row(item));
    return box;
  }

  function code(value) { return text("code", "mini-code", mask(value || "")); }

  async function image(sha256, label) {
    const figure = node("figure", "mini-shot"), caption = text("figcaption", "", label || "");
    figure.append(node("div", "mini-shot-wait"), caption);
    let url = shots.get(sha256);
    if (url === undefined) {
      url = await preview("media/" + sha256 + "?inline=true").catch(() => null);
      if (shots.size > 48) {const [first, old] = shots.entries().next().value; if (old) URL.revokeObjectURL(old); shots.delete(first);}
      shots.set(sha256, url);
    }
    if (url) {
      const img = node("img", "");img.alt = label || tr("Screenshot");img.src = url;img.loading = "lazy";
      const link = node("a", "");link.href = url;link.target = "_blank";link.rel = "noopener";link.append(img);
      figure.firstElementChild.replaceWith(link);
    } else figure.firstElementChild.replaceWith(text("p", "hint", tr("The screenshot could not be loaded.")));
    return figure;
  }

  function confirmText(entry) {
    return tr("Open this mini application?") + "\n\n"
      + tr("Telegram tells the bot that this account opened it, and the bot sees the account's name and ID. TgWitness loads it once in an isolated browser through this workspace's route and records what it loads. The signed launch data, which works as a login to the application, is not recorded.")
      + (entry.type === "button" && entry.inline ? "\n\n" + tr("While it is open, the bot can post one message to this chat on this account's behalf.") : "");
  }

  async function open(chat, entry, host) {
    if (!(await confirm(confirmText(entry), {danger: true}))) return null;
    const {inline, ...body} = entry;
    toast(tr("Opening the mini application… this takes up to a minute."));
    const result = await json("webapp/open", {chat_id: chat, entry: body});
    if (!current(chat)) return result;
    toast(tr("Mini application recorded: journal record #{n}.", {n: result.seq}));
    if (host) {shown = result.seq; await render(host, chat, result);}
    return result;
  }

  function entryRow(chat, item, host, browser) {
    const row = node("li", "mini-entry"), main = node("div", "mini-entry-main");
    const label = tr(ENTRY[item.type] || item.type), title = item.text || item.url || label;
    main.append(text("strong", "", title));
    if (title !== label || item.message_id) main.append(text("small", "", label + (item.message_id ? " · #" + item.message_id : "")));
    if (item.url) main.append(code(item.url));
    row.append(main);
    if (isAdmin() && may("interact")) {
      const button = node("button", "secondary small", tr("Open"));button.type = "button";
      button.title = browser.browser ? tr("Opens it in the isolated browser and records it.") : tr(browser.reason || "");
      button.addEventListener("click", () => busy(button, () => open(chat, item.type === "link"
        ? {type: "link", url: item.url} : item.type === "button"
          ? {type: "button", seq: item.seq, row: item.row, column: item.column, inline: item.inline} : {type: item.type}, host)));
      row.append(button);
    }
    return row;
  }

  function captureCard(item, host, chat) {
    const card = node("button", "mini-capture");card.type = "button";
    const s = item.summary || {};
    const head = node("div", "mini-capture-head");
    head.append(text("strong", "", item.title || item.final_url || item.address || tr("Mini application")),
      text("small", "", [tr(ENTRY[item.entry] || item.entry || ""), fmtFull(item.at), "#" + item.seq,
        item.method === "static" ? tr("page and scripts only") : ""].filter(Boolean).join(" · ")));
    const chips = node("div", "mini-chips");
    chips.append(chip(tr("requests"), s.requests ?? 0), chip(tr("hosts"), s.hosts ?? 0),
      ...(item.third_party_hosts?.length ? [chip(tr("other hosts"), item.third_party_hosts.length, "warn")] : []),
      ...(s.sockets ? [chip(tr("WebSockets"), s.sockets)] : []), ...(s.asks ? [chip(tr("requests to Telegram"), s.asks, "warn")] : []),
      ...(s.wallets ? [chip(tr("wallets"), s.wallets, "danger")] : []));
    card.append(head, chips);
    card.addEventListener("click", () => busy(card, async () => {
      const full = await json("webapp/captures/" + item.seq + "?chat_id=" + encodeURIComponent(chat));
      if (!current(chat)) return;
      shown = item.seq; await render(host, chat, full);
    }));
    return card;
  }

  function add(box, ...parts) { box.append(...parts.filter(Boolean)); }

  function shown_(value) { return value && !['""', "null", "{}", "[]"].includes(String(value).trim()) ? value : ""; }

  function label(value) {
    const text_ = String(value || ""), moment = /^(\d+) s after loading$/.exec(text_);
    return moment ? tr("{n} s after loading", {n: moment[1]})
      : ["Whole page", "Page after loading"].includes(text_) ? tr(text_) : mask(text_);
  }

  function telegramRow(event) {
    const row = node("li", ASK_OF[event.type] ? "mini-ask" : "mini-call"), data = shown_(event.data);
    if (ASK_OF[event.type]) row.append(text("strong", "", tr(ASKS[ASK_OF[event.type]])), text("small", "", event.type));
    else row.append(code(event.type));
    if (data) row.append(code(data));
    return row;
  }

  const ASK_OF = {web_app_request_phone: "phone", web_app_request_write_access: "write_access", web_app_open_invoice: "payment",
    web_app_open_link: "link", web_app_open_tg_link: "telegram_link", web_app_data_send: "data",
    web_app_send_prepared_message: "message", web_app_switch_inline_query: "inline", web_app_request_file_download: "download",
    web_app_read_text_from_clipboard: "clipboard", web_app_request_location: "location",
    web_app_request_emoji_status_access: "emoji_status", web_app_set_emoji_status: "emoji_status",
    web_app_share_to_story: "story", web_app_open_popup: "popup", web_app_biometry_request_access: "biometry",
    web_app_add_to_home_screen: "home_screen"};

  async function detail(host, chat, item) {
    const box = node("div", "mini-detail"), back = node("button", "quiet small", "← " + tr("Mini apps"));back.type = "button";
    back.addEventListener("click", () => {shown = null; render(host, chat).catch(() => {});});
    const facts = node("dl", "mini-facts"), fact = (name, value) => {if (value) facts.append(text("dt", "", name), text("dd", "", value));};
    fact(tr("Opened"), mask(item.address));
    if (item.final_url && item.final_url !== item.address) fact(tr("Ended at"), mask(item.final_url));
    fact(tr("Page title"), item.title);
    fact(tr("Bot"), [item.bot?.name, item.bot?.username ? "@" + item.bot.username : "", item.bot?.id ? "ID " + item.bot.id : ""]
      .filter(Boolean).join(" · "));
    fact(tr("Recorded"), fmtFull(item.at));
    fact(tr("How"), item.method === "browser" ? (item.browser || "Chromium") + (item.sandbox === false ? " · " + tr("without sandbox") : "")
      : tr("Page and scripts fetched; no browser was available"));
    fact(tr("Route"), item.route);
    if (item.duration_ms) fact(tr("Time"), (item.duration_ms / 1000).toFixed(1) + " s");
    const record = node("button", "text-link", tr("Journal record #{n}", {n: item.seq}));record.type = "button";
    record.addEventListener("click", () => busy(record, () => openRecord(item.seq)));
    box.append(back, node("h3", "", item.title || tr("Mini application")), facts, record);
    if (item.browser_missing) box.append(text("p", "notice warning mini-note", tr(item.browser_missing)));
    const pictures = (item.files || []).filter(file => file.role === "screenshot");
    if (pictures.length) {
      const gallery = node("div", "mini-gallery");
      box.append(section(tr("Screenshots"), gallery));
      for (const file of pictures) gallery.append(await image(file.sha256, (file.labels || []).map(label).join(" · ")));
    }
    const asks = item.telegram_events || [];
    if (asks.length) {
      const flagged = (item.asks || []).map(ask => tr(ASKS[ask.kind] || ask.kind));
      box.append(section(tr("What it asked Telegram for"),
        flagged.length ? text("p", "mini-asks", flagged.join(" · ")) : null, list(asks, telegramRow)));
    }
    const wallets = (item.indicators || []).filter(found => found.kind === "wallet");
    if (wallets.length) box.append(section(tr("Wallets"), list(wallets, found => {
      const row = node("li", "");row.append(code(found.value), text("small", "", [found.chain, found.checksum === "valid" ? tr("checksum valid") : ""].filter(Boolean).join(" · ")));
      return row;
    })));
    if (item.third_party_hosts?.length) box.append(section(tr("Other hosts it contacted"),
      list(item.third_party_hosts, host_ => {const row = node("li", "");row.append(code(host_));return row;})));
    for (const [title, entries, row] of [
      [tr("Dialogs it showed"), item.dialogs, d => {const r = node("li", "");r.append(text("strong", "", d.type), code(d.message));return r;}],
      [tr("Windows it tried to open"), item.popups, p => {const r = node("li", "");r.append(code(p.url));return r;}],
      [tr("Downloads it started"), item.downloads, d => {const r = node("li", "");r.append(text("strong", "", d.file), code(d.url));return r;}],
      [tr("Forms"), item.forms, f => {const r = node("li", "");r.append(code(f));return r;}],
      [tr("Input fields"), item.inputs, f => {const r = node("li", "");r.append(code(f));return r;}]]) {
      if (entries?.length) box.append(section(title, list(entries, row)));
    }
    const sockets = item.sockets || [];
    add(box, fold(tr("WebSockets"), sockets.length, () => list(sockets, socket => {
      const row = node("li", "");row.append(code(socket.url), text("small", "", tr("{sent} sent · {received} received", {sent: socket.sent ?? 0, received: socket.received ?? 0})));
      if (socket.frames?.length) row.append(list(socket.frames, frame => {const f = node("li", "mini-frame " + frame.direction);
        f.append(text("small", "", frame.direction === "sent" ? "→" : "←"), code(frame.data));return f;}));
      return row;
    })));
    const requests = item.requests || [];
    add(box, fold(tr("All requests"), requests.length, () => list(requests, request => {
      const row = node("li", "mini-request" + (request.error ? " failed" : ""));
      row.append(text("small", "", [request.method, request.status ?? request.error ?? "…", request.type].filter(Boolean).join(" · ")), code(request.url));
      return row;
    })));
    const connections = item.connections || [];
    add(box, fold(tr("Connections"), connections.length, () => list(connections, c => {
      const row = node("li", "");row.append(code(c.host + (c.address ? " · " + c.address : "")),
        text("small", "", tr("{n} connections · {sent} B sent · {received} B received", {n: c.connections, sent: c.sent, received: c.received})));
      return row;
    })));
    const others = (item.indicators || []).filter(found => found.kind !== "wallet");
    add(box, fold(tr("Other indicators"), others.length, () => list(others, found => {
      const row = node("li", "");row.append(text("small", "", found.kind), code(found.value));return row;
    })));
    const files = item.files || [];
    add(box, fold(tr("Preserved files"), files.length, () => list(files, file => {
      const row = node("li", "");row.append(text("small", "", file.role + " · " + file.mime_type + " · " + file.size + " B"), code(file.sha256),
        ...(file.labels || []).slice(0, 2).map(value => text("small", "mini-label", label(value))));
      return row;
    })));
    if (item.blocked?.length) box.append(section(tr("Refused connections"), text("p", "hint", tr("Addresses inside the local network and addresses the route could not reach are refused.")),
      list(item.blocked, b => {const r = node("li", "");r.append(code(b.host + ":" + b.port), text("small", "", b.reason));return r;})));
    if (item.errors?.length) box.append(section(tr("Not captured"), list(item.errors, e => {const r = node("li", "");r.append(text("strong", "", e.component), text("small", "", e.error));return r;})));
    box.append(text("p", "hint mini-meaning", tr("Recorded once, at this time, through this workspace's route. Another visitor, time or address can be served differently.")));
    return box;
  }

  async function render(host, chat, opened = null) {
    if (opened || shown) {
      const item = opened || await json("webapp/captures/" + shown + "?chat_id=" + encodeURIComponent(chat));
      if (!current(chat)) return;
      host.replaceChildren(await detail(host, chat, item));
      return;
    }
    const data = await json("webapp?chat_id=" + encodeURIComponent(chat));
    if (!current(chat)) return;
    const box = node("div", "mini-apps");
    box.append(text("p", "hint", tr("Mini applications are web pages a bot opens inside Telegram. Opening one here asks Telegram for its address as this account, loads it once in an isolated browser and records every request, Telegram call and screenshot in the signed journal.")));
    if (!data.browser.browser) box.append(text("p", "notice warning mini-note", tr(data.browser.reason) + " " + tr("Without a browser, only the page and its own scripts are fetched and parsed.")));
    const entries = data.entries || [];
    if (data.bot) entries.push({type: "menu"}, {type: "main"});
    box.append(section(tr("Where this chat opens mini applications"), entries.length
      ? list(entries, item => entryRow(chat, item, host, data.browser))
      : text("p", "hint", tr("No mini application buttons or links in the saved messages of this chat."))));
    const captures = data.captures || [];
    box.append(section(tr("Recorded openings"), captures.length
      ? (() => {const wrap = node("div", "mini-captures");for (const item of captures) wrap.append(captureCard(item, host, chat));return wrap;})()
      : text("p", "hint", tr("Nothing opened yet."))));
    host.replaceChildren(box);
  }

  return {render, open, reset() {shown = null;}, focus(seq) {shown = seq;}};
}
