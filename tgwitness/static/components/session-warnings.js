const HIDDEN_KEY = "tgwitness-takeover-hidden-v1:";

export function createSessionWarnings({host, node, icon, tr, fmtFull, riskNames, may, askConfirm, json, refreshStatus, toast,
  openJournal, canJournal, openSessions, canSessions}) {
  const takeover = node("section", "session-warning"), rollback = node("section", "session-warning");
  takeover.dataset.tone = "warning"; rollback.dataset.tone = "danger";
  takeover.hidden = rollback.hidden = true;
  takeover.setAttribute("role", "status"); rollback.setAttribute("role", "alert");
  host.append(rollback, takeover);
  let scope = "", takeoverKey = "", rollbackKey = "", full = true;
  const expanded = new Set();

  const button = (label, className, action) => {
    const b = node("button", className, label);
    b.type = "button";
    b.addEventListener("click", event => action(event.currentTarget));
    return b;
  };
  const compact = () => {
    for (const card of [takeover, rollback]) card.dataset.compact = String(!full && !expanded.has(card));
  };
  const head = (card, symbol, title, meta) => {
    const box = node("div", "session-warning-head"), text = node("div", "session-warning-title");
    text.append(node("strong", "", title));
    if (meta) text.append(node("span", "session-warning-meta", meta));
    box.append(icon(symbol), text, button(tr("Details"), "text-link session-warning-more", () => { expanded.add(card); compact(); }));
    return box;
  };
  const signature = risk => [risk.kind, risk.pattern || "", risk.unconfirmed_pattern || "", risk.session_app_id || ""].join(":");
  const hiddenFor = () => { try { return localStorage.getItem(HIDDEN_KEY + scope) || ""; } catch { return ""; } };
  const hide = value => { try { localStorage.setItem(HIDDEN_KEY + scope, value); } catch { } };

  function riskItem(risk) {
    const item = node("li", "session-risk"), name = riskNames[risk.kind] || risk.kind;
    let title = name, why = "", fix = "";
    if (risk.kind === "login_email") {
      title = name + (risk.pattern ? " · " + risk.pattern : "");
      why = tr("Telegram sends sign-in codes to this mailbox. Whoever reads it can sign in without the phone and end this session.");
      fix = tr("Official Telegram app → Settings → Privacy and Security → Login email: change it to an address you control.");
    } else if (risk.kind === "recovery_email") {
      title = name + (risk.unconfirmed_pattern ? " · " + risk.unconfirmed_pattern : "");
      why = tr("Whoever reads this mailbox can reset the two-step password.");
      fix = tr("Official Telegram app → Settings → Privacy and Security → Two-Step Verification → Change recovery email.");
    } else if (risk.kind === "two_step_password") {
      why = tr("If you did not set it yourself or through TgWitness, the previous owner knows it.");
      fix = tr("Official Telegram app → Settings → Privacy and Security → Two-Step Verification → Change password.");
    } else if (risk.kind === "app_id_mismatch") {
      why = tr("This session key was created by {app} (api_id {created}); TgWitness connects as api_id {sent}. Whoever made the key may still hold a copy of it.",
        {app: risk.session_app || "?", created: risk.session_app_id ?? "?", sent: risk.client_app_id ?? "?"});
      fix = tr("Sign in to TgWitness with a new code or QR, then end the other sessions of this account.");
    }
    item.append(node("strong", "", title));
    if (why) item.append(node("span", "", why));
    if (fix) item.append(node("span", "session-risk-fix", fix));
    return item;
  }

  function renderTakeover(record, demo) {
    const risks = Array.isArray(record?.risks) ? record.risks : [];
    const key = risks.map(signature).sort().join("|");
    if (demo || !risks.length || hiddenFor() === key) { takeover.hidden = true; takeoverKey = ""; return; }
    if (key + "@" + record.at === takeoverKey) { takeover.hidden = false; return; }
    takeoverKey = key + "@" + record.at;
    const list = node("ul", "session-risks"), actions = node("div", "session-warning-actions");
    risks.forEach(risk => list.append(riskItem(risk)));
    if (canSessions()) actions.append(button(tr("Sessions of this account"), "secondary", () => openSessions()));
    actions.append(button(tr("Hide until something changes"), "quiet", () => { hide(key); takeover.hidden = true; takeoverKey = ""; }));
    const notes = [tr("TgWitness checks this each time observation starts. After fixing, pause and resume observation to check again.")];
    if (record.password_check_error) notes.unshift(tr("Email and password settings could not be read: {error}.", {error: record.password_check_error}));
    takeover.replaceChildren(
      head(takeover, "shield", tr("Someone else may still be able to sign in to this account"), record.at ? tr("Checked {time}", {time: fmtFull(record.at)}) : ""),
      node("p", "", tr("Whoever controls the items below can sign in without this session and end it. Observation would stop.")),
      list, ...notes.map(text => node("p", "session-warning-note", text)), actions);
    takeover.hidden = false;
  }

  function renderRollback(record, demo) {
    if (demo || !record?.remembered) { rollback.hidden = true; rollbackKey = ""; return; }
    const seen = record.remembered.seq, last = record.journal_head?.seq ?? 0, key = [record.detected_at, seen, last].join(":");
    if (key === rollbackKey) { rollback.hidden = false; return; }
    rollbackKey = key;
    const shorter = record.reason === "shorter", seenAt = record.remembered.at ? fmtFull(record.remembered.at) : tr("unknown");
    const text = shorter
      ? tr("This computer had seen record #{seen} ({time}). The journal now ends at record #{head}. Records missing from this copy: {n}.",
        {seen, head: last, n: Math.max(0, seen - last), time: seenAt})
      : tr("Record #{seen} in this journal differs from the one this computer saw ({time}). From that point on, the records come from another copy.",
        {seen, time: seenAt});
    const actions = node("div", "session-warning-actions");
    if (canJournal()) actions.append(button(tr("Show in the journal"), "secondary", () => openJournal("journal.rolled_back")));
    if (may("settings")) actions.append(button(tr("I restored it myself"), "quiet", async target => {
      if (!(await askConfirm(tr("Confirm that you restored this copy on purpose? The warning is cleared for everyone with access, and your confirmation is added to the signed journal."),
        {confirmText: tr("I restored it myself")}))) return;
      target.disabled = true;
      try {
        await json("journal/rollback/acknowledge", {});
        toast(tr("Confirmation added to the journal."));
        await refreshStatus();
      } catch (error) { toast(error.message, true); }
      finally { target.disabled = false; }
    }));
    rollback.replaceChildren(
      head(rollback, "alert", tr(shorter ? "This journal was restored from an older copy" : "This journal was replaced by a different copy"),
        record.detected_at ? tr("Detected {time}", {time: fmtFull(record.detected_at)}) : ""),
      node("p", "", text),
      node("p", "session-warning-note", tr("The event is recorded in the signed journal and observation continues. If you did not restore a backup yourself, someone replaced the data folder: find the newer copy before you export evidence.")),
      actions);
    rollback.hidden = false;
  }

  return {
    update(status, workspace, home = true) {
      if (workspace !== scope) { scope = workspace; takeoverKey = rollbackKey = ""; expanded.clear(); }
      if (home !== full) { full = home; expanded.clear(); }
      const collector = status?.collector || {};
      renderRollback(collector.journal_rollback, !!status?.demo);
      renderTakeover(collector.takeover_risk, !!status?.demo);
      compact();
      host.hidden = takeover.hidden && rollback.hidden;
    },
  };
}
