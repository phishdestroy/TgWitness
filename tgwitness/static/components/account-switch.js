import {accountState} from "./account-state.js";
import {describeWorkspace} from "./workspaces.js?v=2";

const TONES = {demo: "info", collecting: "ok", reconnecting: "warn", paused: "off", sign_in: "bad", failed: "bad", empty: "off", unavailable: "off"};
const WORDS = {demo: "Demo", collecting: "Observing", reconnecting: "Reconnecting", paused: "Observation off", sign_in: "Sign-in required",
  failed: "Needs attention", empty: "Account not connected", unavailable: "Unavailable"};

export function createAccountSwitch({node, icon, tr, avatar, profiles, current, status, choose, add, canAdd, manage, canManage}) {
  const host = document.querySelector(".profile-switch"), select = document.getElementById("profile-select");
  const button = node("button", "account-switch"), face = node("span", "account-switch-face");
  const text = node("span", "account-switch-text"), name = node("span", "account-switch-name"), line = node("span", "account-switch-line");
  const chevron = icon("chevron"); chevron.classList.add("account-switch-chevron");
  const menu = node("div", "account-menu"), list = node("div", "account-menu-list"), foot = node("div", "account-menu-foot");
  button.type = "button"; button.id = "account-switch"; menu.id = "account-menu"; menu.hidden = true;
  button.setAttribute("aria-haspopup", "menu"); button.setAttribute("aria-expanded", "false"); button.setAttribute("aria-controls", menu.id);
  menu.setAttribute("role", "menu"); menu.setAttribute("aria-label", tr("Accounts"));
  text.append(name, line); button.append(face, text, chevron); menu.append(list, foot);
  host.prepend(button); host.append(menu); host.classList.add("has-account-switch");
  select.tabIndex = -1; select.setAttribute("aria-hidden", "true");
  let faceKey = "", rendered = "";

  function entry(profile) {
    const live = profile.id === current() && status() ? {...profile, ...status()} : profile;
    const account = live.collector?.account || null, info = accountState(live);
    const kind = live.demo ? "demo" : profile.error_type ? "unavailable" : info.kind;
    const handle = account?.username ? "@" + account.username : "";
    const title = account?.name || handle || profile.label || profile.id;
    const problems = describeWorkspace(live, tr).problems;
    return {id: profile.id, account, kind, handle, title, label: profile.label || profile.id, problems,
      disabled: Boolean(profile.error_type), word: tr(WORDS[kind] || "Unavailable"), tone: TONES[kind] || "off"};
  }
  function chip(item) {
    const mark = node("span", "account-chip");
    mark.dataset.tone = item.tone; mark.append(node("span", "account-chip-dot"), node("span", "", item.word));
    return mark;
  }
  function picture(item, size) {
    const wrap = node("span", "account-face " + size);
    wrap.append(avatar(item.account?.id, item.account?.name || item.account?.username || item.label, size, item.id));
    if (item.problems) {const count = node("b", "account-face-alert", String(item.problems)); count.setAttribute("aria-hidden", "true"); wrap.append(count);}
    return wrap;
  }
  function describe(item) {
    return [item.title, item.handle && item.handle !== item.title ? item.handle : "", item.label !== item.title ? item.label : "", item.word,
      item.problems ? tr("Health checks needing attention: {n}", {n: item.problems}) : ""].filter(Boolean).join(" · ");
  }
  function update() {
    const all = profiles() || [], selected = all.find(profile => profile.id === current());
    button.hidden = !selected && !status();
    const item = entry(selected || {id: current(), label: tr("Main workspace")});
    const key = item.id + ":" + (item.account?.id || "") + ":" + item.problems;
    if (key !== faceKey) {faceKey = key; face.replaceChildren(picture(item, "sm"));}
    name.textContent = item.title;
    line.replaceChildren(chip(item));
    if (item.handle && item.handle !== item.title) line.append(node("span", "account-switch-handle", item.handle));
    button.setAttribute("aria-label", tr("Accounts") + ": " + describe(item));
    if (!menu.hidden) renderMenu();
  }
  function renderMenu() {
    const items = (profiles() || []).map(entry), stamp = JSON.stringify([items, current(), canAdd(), canManage()]);
    if (stamp === rendered) return;
    const focused = menu.contains(document.activeElement) ? document.activeElement.dataset.account : null;
    rendered = stamp; list.replaceChildren(); foot.replaceChildren();
    for (const item of items) {
      const row = node("button", "account-menu-item"), body = node("span", "account-menu-body"), sub = node("span", "account-menu-sub");
      row.type = "button"; row.dataset.account = item.id; row.setAttribute("role", "menuitemradio");
      row.setAttribute("aria-checked", String(item.id === current())); row.disabled = item.disabled; row.setAttribute("aria-label", describe(item));
      sub.append(chip(item));
      const extra = [item.handle && item.handle !== item.title ? item.handle : "", item.label !== item.title ? item.label : ""].filter(Boolean).join(" · ");
      if (extra) sub.append(node("span", "account-menu-extra", extra));
      body.append(node("span", "account-menu-name", item.title), sub);
      row.append(picture(item, ""), body);
      if (item.id === current()) {const mark = icon("check"); mark.classList.add("account-menu-check"); row.append(mark);}
      row.addEventListener("click", () => {close(true); if (item.id !== current()) choose(item.id);});
      list.append(row);
    }
    if (canAdd()) foot.append(action("plus", tr("Add account"), add));
    if (canManage()) foot.append(action("users", tr("All accounts"), manage));
    foot.hidden = !foot.children.length;
    if (focused) menu.querySelector(`[data-account="${CSS.escape(focused)}"]`)?.focus();
  }
  function action(symbol, label, run) {
    const item = node("button", "account-menu-action"); item.type = "button"; item.setAttribute("role", "menuitem");
    item.append(icon(symbol), node("span", "", label));
    item.addEventListener("click", () => {close(false); run();});
    return item;
  }
  const items = () => [...menu.querySelectorAll("button:not([disabled])")];
  function open(focus = "current") {
    rendered = ""; renderMenu(); menu.hidden = false; button.setAttribute("aria-expanded", "true");
    const all = items(), target = focus === "last" ? all.at(-1) : menu.querySelector('[aria-checked="true"]:not([disabled])') || all[0];
    target?.focus();
  }
  function close(restore) {
    if (menu.hidden) return;
    menu.hidden = true; button.setAttribute("aria-expanded", "false");
    if (restore) button.focus({preventScroll: true});
  }
  button.addEventListener("click", () => menu.hidden ? open() : close(false));
  button.addEventListener("keydown", event => {
    if (event.key === "ArrowDown" || event.key === "ArrowUp") {event.preventDefault(); open(event.key === "ArrowUp" ? "last" : "current");}
  });
  menu.addEventListener("keydown", event => {
    const all = items(), index = all.indexOf(document.activeElement);
    const next = {ArrowDown: index + 1, ArrowUp: index - 1, Home: 0, End: all.length - 1}[event.key];
    if (event.key === "Escape") {event.preventDefault(); event.stopPropagation(); close(true);}
    else if (event.key === "Tab") close(false);
    else if (next !== undefined) {event.preventDefault(); all[(next + all.length) % all.length]?.focus();}
  });
  document.addEventListener("pointerdown", event => {if (!menu.hidden && !host.contains(event.target)) close(false);});
  window.addEventListener("tgwitness:lock", () => close(false));
  select.addEventListener("change", () => queueMicrotask(update));
  return {update, close};
}
