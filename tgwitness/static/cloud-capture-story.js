/* An illustrative, local-only explanation. Never reads capture keys or files. */
(() => {
  "use strict";
  const motion = matchMedia("(prefers-reduced-motion: reduce)");
  let host, lang = "en", frame = 0, playing = !motion.matches, visible = false, timer, observer;
  let scenario = "original";
  const t = (en, ru) => lang === "ru" ? ru : en;
  const icon = name => `<svg viewBox="0 0 24 24" class="icon" aria-hidden="true">${{
    key: '<circle cx="8" cy="9" r="4"/><path d="m11 12 9 9m-4-4 3-3m-6 0 3-3"/>',
    chat: '<path d="M21 11a8 8 0 0 1-8 8H8l-5 3V7a4 4 0 0 1 4-4h6a8 8 0 0 1 8 8Z"/><path d="M7 8h9M7 12h6"/>',
    server: '<rect x="3" y="3" width="18" height="7" rx="2"/><rect x="3" y="14" width="18" height="7" rx="2"/><path d="M7 6.5h.01M7 17.5h.01M12 7h5M12 18h5"/>',
    file: '<path d="M14 3H6v18h13V8ZM14 3v5h5M9 13h7M9 17h5"/>',
    lock: '<rect x="5" y="10" width="14" height="11" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3M12 14v3"/>',
    check: '<path d="m5 12 4 4L19 6"/>',
    shield: '<path d="m12 3 8 3v6c0 5-8 9-8 9s-8-4-8-9V6Z"/><path d="m8 12 3 3 5-6"/>',
    arrow: '<path d="M4 12h16m-6-6 6 6-6 6"/>',
    play: '<path d="m8 4 12 8-12 8Z"/>',
    pause: '<path d="M8 4v16M16 4v16"/>',
    cross: '<path d="m6 6 12 12M18 6 6 18"/>'
  }[name]}</svg>`;
  const steps = () => [t("Your key", "Ваш ключ"), t("Capture", "Сбор"), t("Attestation", "Фиксация"), t("Encryption", "Шифрование"), t("Verification", "Проверка")];
  const scenes = () => [
    [t("The key starts with you.", "Всё начинается с вашего ключа."), t("The browser creates a pair of keys. Save the private key on your device. Give GitHub only the public part: it can lock the archive, but cannot open it.", "Браузер создаёт пару ключей. Закрытый ключ сохраняете у себя. GitHub передаёте только открытую часть: ей можно закрыть архив, но нельзя открыть."), t("You do: save sealed-key.json", "Ваше действие: сохранить sealed-key.json")],
    [t("GitHub runs the collector.", "GitHub запускает сборщик."), t("Start the workflow in your fork, open the temporary panel and sign in to Telegram. Choose one chat. The pinned collector reads its available messages and media.", "Запускаете задачу в своём форке, открываете временную панель и входите в Telegram. Выбираете один чат. Закреплённый сборщик читает доступные сообщения и медиа."), t("You do: sign in and select a chat", "Ваше действие: войти и выбрать чат")],
    [t("The archive gets a fingerprint.", "У архива появляется отпечаток."), t("GitHub attests the archive’s hash and the workflow identity. This connects the exact file to the process that produced it. The chat contents are not published in the attestation.", "GitHub фиксирует хеш архива и сведения о workflow. Так конкретный файл связывается с процессом его создания. Содержимое чата в аттестацию не публикуется."), t("The result: evidence.zip + attestation.jsonl", "Результат: evidence.zip + attestation.jsonl")],
    [t("Only encrypted delivery is uploaded.", "На скачивание — зашифрованный пакет."), t("The archive and attestation are encrypted with your public key. Download the result from GitHub and open it here with your saved private key. The temporary machine is removed after the job.", "Архив и аттестация шифруются вашим открытым ключом. Скачиваете результат из GitHub и открываете здесь сохранённым закрытым ключом. После задачи временная машина удаляется."), t("You do: download and decrypt", "Ваше действие: скачать и расшифровать")],
    [t("Someone else can check the result.", "Результат может проверить другой человек."), t("Give the reviewer the archive and attestation. The verifier checks the file hash and the approved workflow and collector version. Your private decryption key is not needed for that check.", "Передаёте проверяющему архив и аттестацию. Проверка сверяет хеш файла, разрешённый workflow и версию сборщика. Ваш закрытый ключ для этой проверки не нужен."), t("Try changing the example below ↓", "Попробуйте изменить пример ниже ↓")]
  ];
  const item = (symbol, name, detail, cls = "") => `<div class="story-object ${cls}"><span class="story-object-icon">${icon(symbol)}</span><strong>${name}</strong><small>${detail}</small></div>`;
  const wire = () => `<div class="story-wire" aria-hidden="true"><span></span>${icon("arrow")}</div>`;
  const windowCard = (title, body) => `<div class="story-window"><div class="story-window-bar"><span class="story-window-dots" aria-hidden="true">● ● ●</span><span>${title}</span></div>${body}</div>`;
  function illustration() {
    if (frame === 0) return `<div class="story-flow">${item("key", t("Your device", "Ваше устройство"), "sealed-key.json", "story-origin")}${wire()}<div class="story-key-pair">${item("server", t("Public key → GitHub", "Открытый ключ → GitHub"), t("Encrypt the delivery", "Зашифровать результат"))}${item("lock", t("Private key → stays with you", "Закрытый ключ → у вас"), t("Open the delivery", "Открыть результат"), "story-private")}</div></div>`;
    if (frame === 1) return windowCard(t("GitHub · temporary runner", "GitHub · временная машина"), `<div class="story-flow story-in-runner"><div class="story-chat"><span class="story-mini-label">${icon("chat")} ${t("Selected Telegram chat", "Выбранный чат Telegram")}</span><div class="story-bubble">${t("Meeting at 18:00", "Встречаемся в 18:00")}<small>18:02</small></div><div class="story-bubble story-bubble-reply">${t("The files are attached", "Материалы во вложении")}<small>18:03</small></div><div class="story-attachment">${icon("file")} document.pdf</div></div>${wire()}${item("file", "evidence.zip", t("Messages + media", "Сообщения + медиа"))}</div>`);
    if (frame === 2) return `<div class="story-flow">${item("file", "evidence.zip", t("The original archive", "Исходный архив"))}${wire()}<div class="story-certificate"><span class="story-certificate-seal">${icon("shield")}</span><span class="story-mini-label">GITHUB ATTESTATION</span><strong>attestation.jsonl</strong><div class="story-fingerprint">SHA-256 <span>8f24 · a19c · 7d03 · …</span></div><p>${icon("check")}${t("Archive hash", "Хеш архива")}</p><p>${icon("check")}${t("Workflow identity", "Сведения о workflow")}</p></div></div>`;
    if (frame === 3) return `<div class="story-flow"><div class="story-file-stack">${item("file", "evidence.zip", t("Chat and media", "Чат и медиа"))}${item("shield", "attestation.jsonl", t("GitHub provenance", "Аттестация GitHub"))}</div>${wire()}<div class="story-envelope">${icon("lock")}<span class="story-cipher" aria-hidden="true">7b 4e a2 91 f0 6c<br>c8 03 5d ab 72 e9<br>1f b6 04 d8 3a 60</span><strong>delivery.tgwsealed</strong><small>${t("Opened with your private key", "Открывается вашим закрытым ключом")}</small></div></div>`;
    return `<div class="story-flow">${item("file", t("Archive + attestation", "Архив + аттестация"), t("Send to a reviewer", "Передайте проверяющему"))}${wire()}<div class="story-verifier"><span class="story-mini-label">${icon("shield")}${t("Independent verification", "Независимая проверка")}</span>${[t("File hash matches", "Хеш файла совпадает"), t("Workflow approved", "Workflow разрешён"), t("Collector version approved", "Версия сборщика разрешена")].map(x => `<p>${icon("check")}${x}</p>`).join("")}<strong>${t("All three checks matter", "Важны все три проверки")}</strong></div></div>`;
  }
  function template() {
    return `<section class="capture-story" aria-labelledby="capture-story-title"><div class="story-title-row"><div><span class="eyebrow">${t("UNDERSTAND BEFORE YOU START", "СНАЧАЛА РАЗБЕРЁМСЯ")}</span><h2 id="capture-story-title">${t("From a chat to a verifiable archive.", "От чата до проверяемого архива.")}</h2></div><button type="button" class="secondary story-start" data-story-start>${t("Start my capture", "Перейти к выгрузке")}${icon("arrow")}</button></div>
      <div class="story-player"><div class="story-tabs" role="group" aria-label="${t("Explanation steps", "Этапы объяснения")}">${steps().map((name, i) => `<button type="button" data-story-frame="${i}" aria-pressed="false"><span>0${i+1}</span>${name}<i aria-hidden="true"></i></button>`).join("")}</div>
      <div class="story-scene"></div><div class="story-player-footer"><span class="story-example-label">${t("Illustration · no account connected", "Схема · аккаунт не подключён")}</span><button type="button" class="quiet" data-story-play></button></div></div>
      <div class="story-benefits">${[["server",t("No local installation", "Без установки"),t("A temporary machine runs the collector for you.", "Сборщик работает на временной машине GitHub.")],["lock",t("Private delivery", "Приватный результат"),t("The downloadable package is encrypted with your key.", "Пакет для скачивания зашифрован вашим ключом.")],["shield",t("Checkable origin", "Проверяемое происхождение"),t("A reviewer can check the file and its collector.", "Можно проверить файл и версию его сборщика.")]].map(([i,h,p])=>`<div>${icon(i)}<strong>${h}</strong><p>${p}</p></div>`).join("")}</div>
      <section class="story-lab" aria-labelledby="story-lab-title"><div class="story-lab-heading"><div><span class="eyebrow">${t("TRY A CHANGE", "ПОПРОБУЙТЕ ПОДМЕНУ")}</span><h3 id="story-lab-title">${t("What if someone edits the result?", "А если кто-то изменит результат?")}</h3><p>${t("Choose a scenario. See what the verifier checks.", "Выберите сценарий. Посмотрите, что заметит проверка.")}</p></div><span class="story-demo-tag">${t("DEMO", "ПРИМЕР")}</span></div>
      <div class="story-scenarios" role="group" aria-label="${t("Verification example", "Пример проверки")}">${[["original",t("Unchanged", "Без изменений")],["message",t("Edit a message", "Изменить сообщение")],["collector",t("Replace the collector", "Подменить сборщик")]].map(([id,label])=>`<button type="button" data-story-scenario="${id}" aria-pressed="false">${label}</button>`).join("")}</div><div class="story-lab-result" aria-live="polite" aria-atomic="true"></div>
      <p class="story-lab-note">${t("An illustrative example, not a check of your archive. Real verification checks the cryptographic attestation and the approved collector policy.", "Это учебный пример, а не проверка вашего архива. Настоящая проверка сверяет криптографическую аттестацию и разрешённые версии сборщика.")}</p></section>
      <details class="story-details"><summary>${t("What is private, and who do I trust?", "Что остаётся приватным и кому мы доверяем?")}</summary><p>${t("Your private key stays on your device. The temporary GitHub machine processes the chat and Telegram session during collection; the HTTPS tunnel provides access to its panel. These are trusted parts of the process. Public attestation metadata includes a hash and workflow information. The check establishes file integrity and provenance, not whether a statement in a message is true or whether the history is complete.", "Закрытый ключ остаётся на вашем устройстве. Временная машина GitHub обрабатывает чат и Telegram-сессию во время сбора; HTTPS-туннель даёт доступ к панели. Это доверенные части процесса. Публичная аттестация содержит хеш и сведения о workflow. Проверяется целостность и происхождение файла, а не правдивость высказываний в сообщениях или полнота истории.")}</p></details></section>`;
  }
  function schedule() {
    clearTimeout(timer);
    const running = playing && visible && !document.hidden;
    if (host) host.dataset.running = String(running);
    if (running) timer = setTimeout(() => {
      if (frame < 4) {frame++; drawScene();} else {playing = false; drawControls(); schedule();}
    }, 7500);
  }
  function drawControls() {
    host.querySelectorAll("[data-story-frame]").forEach((b,i) => {
      b.setAttribute("aria-pressed", String(i === frame)); b.dataset.complete = String(i < frame);
    });
    host.querySelector("[data-story-play]").innerHTML = icon(playing ? "pause" : "play") + (playing ? t("Pause", "Пауза") : frame === 4 ? t("Replay", "Повторить") : t("Play explanation", "Смотреть процесс"));
  }
  function drawScene() {
    const [title, body, action] = scenes()[frame];
    host.querySelector(".story-scene").innerHTML = `<div class="story-narrative"><span class="story-scene-number">0${frame+1}<span> / 05</span></span><h3>${title}</h3><p>${body}</p><span class="story-your-action">${action}</span></div><div class="story-visual" data-scene="${frame}">${illustration()}</div>`;
    drawControls(); schedule();
  }
  function drawLab() {
    const changed = scenario !== "original", message = scenario === "message", collector = scenario === "collector";
    host.querySelectorAll("[data-story-scenario]").forEach(b => b.setAttribute("aria-pressed",String(b.dataset.storyScenario === scenario)));
    const row = (name, ok) => `<div class="story-check-row" data-ok="${ok}"><span>${name}</span><strong>${icon(ok ? "check" : "cross")}${ok ? t("Matches", "Совпадает") : t("Mismatch", "Не совпадает")}</strong></div>`;
    host.querySelector(".story-lab-result").innerHTML = `<div class="story-sample"><span class="story-mini-label">${t("Example message", "Пример сообщения")}</span><p>${t("Meeting at", "Встречаемся в")} <strong class="${message ? "story-edited" : ""}">${message ? "21:00" : "18:00"}</strong></p><div class="story-sample-code">${icon("server")}<span>${collector ? t("Modified collector", "Изменённый сборщик") : t("Approved collector", "Разрешённый сборщик")}</span>${collector ? icon("cross") : icon("check")}</div></div><div class="story-checks">${row(t("Archive hash", "Хеш архива"),!message)}${row(t("Workflow / collector", "Workflow / сборщик"),!collector)}<div class="story-verdict" data-valid="${!changed}">${icon(changed ? "cross" : "shield")}<div><strong>${changed ? t("Example: rejected", "Пример: проверка отклонена") : t("Example: checks pass", "Пример: проверка пройдена")}</strong><p>${message ? t("The changed bytes no longer match the attested hash.", "После изменения байтов хеш не совпадает с зафиксированным.") : collector ? t("A GitHub signature alone is not enough: the collector must also be approved.", "Подписи GitHub недостаточно: версия сборщика тоже должна быть разрешена.") : t("The file and collector match the attestation and policy.", "Файл и сборщик соответствуют аттестации и правилам проверки.")}</p></div></div></div>`;
  }
  function mount(target, language) {
    observer?.disconnect(); clearTimeout(timer); host = target; lang = language;
    if (!host) return;
    host.innerHTML = template(); visible = false; drawScene(); drawLab();
    host.addEventListener("click", event => {
      const step = event.target.closest("[data-story-frame]");
      const sample = event.target.closest("[data-story-scenario]");
      if (step) {frame = Number(step.dataset.storyFrame); playing = false; drawScene();}
      if (sample) {scenario = sample.dataset.storyScenario; playing = false; drawControls(); schedule(); drawLab();}
      if (event.target.closest("[data-story-play]")) {if (!playing && frame === 4) frame = 0; playing = !playing; drawScene();}
      if (event.target.closest("[data-story-start]")) {
        playing = false; drawControls(); schedule();
        const setup = document.getElementById("capture-setup");
        setup?.scrollIntoView({behavior: motion.matches ? "instant" : "smooth", block: "start"});
        setup?.focus({preventScroll:true});
      }
    });
    observer = new IntersectionObserver(entries => {visible = entries[0].isIntersecting; schedule();});
    observer.observe(host.querySelector(".story-player"));
  }
  document.addEventListener("visibilitychange", schedule);
  motion.addEventListener("change", () => {if (motion.matches) {playing = false; if (host) {drawControls(); schedule();}}});
  window.TgWitnessCaptureStory = {mount, reset() {playing = false; frame = 0; scenario = "original"; clearTimeout(timer);}};
})();
