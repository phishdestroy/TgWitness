const RAIL = [["chats", "message"], ["secret-chats", "lock"], ["evidence", "export"], ["accounts", "users"], ["settings", "settings"]];

export function createResponsiveShell({node, icon, tr}) {
  const workspace = document.getElementById("workspace"), sidebar = workspace.querySelector(".sidebar");
  const main = workspace.querySelector("main"), header = main.querySelector(".topbar");
  const mobile = matchMedia("(max-width: 767px)");
  const toggle = node("button", "quiet mobile-nav-toggle");
  toggle.type = "button"; toggle.id = "navigation-toggle";
  toggle.title = tr("Main navigation"); toggle.setAttribute("aria-label", tr("Main navigation"));
  sidebar.id = "panel-sidebar"; toggle.setAttribute("aria-controls", sidebar.id);
  toggle.setAttribute("aria-expanded", "false"); toggle.append(icon("menu"));
  header.prepend(toggle);
  const close = node("button", "quiet mobile-nav-close");
  close.type = "button"; close.title = tr("Close navigation"); close.setAttribute("aria-label", tr("Close navigation"));
  close.append(icon("x")); sidebar.prepend(close);
  const scrim = node("div", "sidebar-scrim"); scrim.hidden = true;
  workspace.append(scrim);
  const rail = node("nav", "rail"), railMenu = node("button", "rail-item rail-menu");
  rail.setAttribute("aria-label", tr("Main navigation"));
  railMenu.type = "button"; railMenu.title = tr("Main navigation"); railMenu.setAttribute("aria-label", tr("Main navigation"));
  railMenu.setAttribute("aria-controls", sidebar.id); railMenu.setAttribute("aria-expanded", "false"); railMenu.append(icon("menu"));
  rail.append(railMenu);
  const railItems = RAIL.map(([view, glyph]) => {
    const item = node("button", "rail-item");
    item.type = "button"; item.dataset.railView = view;
    item.append(icon(glyph), node("span", "rail-label"));
    item.addEventListener("click", () => sidebar.querySelector('.nav[data-view="' + view + '"]')?.click());
    rail.append(item);
    return item;
  });
  workspace.prepend(rail);
  const measure = document.createElement("canvas").getContext("2d");
  function fitRail() {
    const shown = railItems.filter(item => !item.hidden && item.lastElementChild.textContent);
    if (!measure || !shown.length) return;
    const style = getComputedStyle(shown[0]), room = 112 - 18;
    measure.font = style.fontWeight + " " + style.fontSize + " " + style.fontFamily;
    const widest = Math.max(...shown.flatMap(item => item.lastElementChild.textContent.split(/\s+|(?<=-)/)).map(word => measure.measureText(word).width));
    rail.style.setProperty("--nav-rail", Math.min(112, Math.max(82, Math.ceil(widest) + 18)) + "px");
    const size = widest > room ? Math.max(8.5, parseFloat(style.fontSize) * room / widest).toFixed(1) + "px" : "";
    for (const item of railItems) item.lastElementChild.style.fontSize = size;
  }
  function syncRail(current = null) {
    for (const item of railItems) {
      const source = sidebar.querySelector('.nav[data-view="' + item.dataset.railView + '"]');
      item.hidden = !source || source.hidden;
      if (!source) continue;
      const label = [...source.childNodes].filter(child => child.nodeType === Node.TEXT_NODE).map(child => child.textContent).join("").trim();
      item.lastElementChild.textContent = label; item.title = label;
      const active = current ? current === item.dataset.railView : source.classList.contains("active");
      if (active) item.setAttribute("aria-current", "page"); else item.removeAttribute("aria-current");
    }
    fitRail();
  }
  new MutationObserver(() => syncRail()).observe(sidebar.querySelector("nav"), {attributes: true, subtree: true, childList: true, characterData: true, attributeFilter: ["class", "hidden"]});
  syncRail();
  document.fonts?.ready.then(fitRail);
  let opened = false, previousFocus = null, openMenu = null;
  const closeMenus = (except = null) => {
    if (openMenu && openMenu !== except) {openMenu.open = false; openMenu = null;}
    for (const menu of workspace.querySelectorAll('.action-menu[open]')) if (menu !== except) menu.open = false;
  };
  workspace.addEventListener('toggle', event => {
    if (event.target.matches('.action-menu') && event.target.open) {closeMenus(event.target); openMenu = event.target;}
  }, true);
  document.addEventListener('pointerdown', event => {
    for (const menu of workspace.querySelectorAll('.action-menu[open]')) if (!menu.contains(event.target)) menu.open = false;
  });
  document.addEventListener('keydown', event => {
    if (event.key !== 'Escape' || document.querySelector('dialog[open]')) return;
    const menu = workspace.querySelector('.action-menu[open]');
    if (menu) { event.preventDefault(); menu.open = false; menu.querySelector('summary').focus(); }
  });

  function setOpen(value, restore = true) {
    opened = Boolean(value);
    if (opened) previousFocus = document.activeElement;
    workspace.classList.toggle("navigation-open", opened);
    toggle.setAttribute("aria-expanded", String(opened)); railMenu.setAttribute("aria-expanded", String(opened)); scrim.hidden = !opened;
    main.inert = opened; rail.inert = opened; sidebar.inert = !opened;
    if (opened) {
      sidebar.setAttribute("role", "dialog"); sidebar.setAttribute("aria-modal", "true");
      sidebar.setAttribute("aria-label", tr("Main navigation")); close.focus();
    } else {
      sidebar.removeAttribute("role"); sidebar.removeAttribute("aria-modal");
      if (restore && previousFocus?.isConnected && !previousFocus.closest("[inert]")) previousFocus.focus();
      else if (sidebar.contains(document.activeElement)) (mobile.matches ? toggle : railMenu).focus({preventScroll: true});
      previousFocus = null;
    }
  }
  function resize() {
    setOpen(false, false);
    closeMenus();
  }
  toggle.addEventListener("click", () => setOpen(!opened));
  railMenu.addEventListener("click", () => setOpen(!opened));
  close.addEventListener("click", () => setOpen(false)); scrim.addEventListener("click", () => setOpen(false));
  sidebar.addEventListener("click", event => {
    if (event.target.closest("[data-view], #lock-panel, #mode-switch, .doc-toggle")) setOpen(false, false);
  });
  window.addEventListener("tgwitness:route", event => {
    syncRail(event.detail?.view || null);
    closeMenus();
    if (event.detail?.reason !== "initial") setOpen(false, false);
  });
  window.addEventListener("tgwitness:lock", () => {closeMenus();setOpen(false, false);});
  document.addEventListener("keydown", event => {
    if (!opened) return;
    if (event.key === "Escape") { event.preventDefault(); setOpen(false); return; }
    if (event.key !== "Tab") return;
    const controls = [...sidebar.querySelectorAll("a[href],button,input,select,summary,[tabindex='0']")]
      .filter(control => !control.disabled && control.checkVisibility());
    const first = controls[0], last = controls.at(-1);
    if (event.shiftKey && (document.activeElement === first || !sidebar.contains(document.activeElement))) {
      event.preventDefault(); last?.focus();
    } else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first?.focus(); }
  });
  mobile.addEventListener("change", resize); resize();
  return {close: () => setOpen(false, false)};
}
