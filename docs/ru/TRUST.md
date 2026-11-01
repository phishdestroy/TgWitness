# Независимая проверка

[English](../TRUST.md) · [Политика безопасности](../../.github/SECURITY.md)

Вы можете проверить соответствие байтов артефакта опубликованному workflow и
коммиту без доступа к нашей инфраструктуре и без доверия к нашему self-hosted
раннеру. При этом остаётся доверие к одобренному вами коду, раннерам и OIDC
GitHub, Sigstore и вашим инструментам проверки. Attestation — подписанное
утверждение, а не доказательство безвредности кода.

## Релизный архив исходников

Нужен актуальный [GitHub CLI](https://cli.github.com/manual/gh_attestation_verify).
Из релиза, выпущенного после добавления `provenance.yml`, скачайте
`TgWitness-<ver>.zip`, его файл `.zip.sha256`, `sbom.spdx.json` и
`provenance.sigstore.json`. Этот ZIP собирается через `tools/build_source.py`
на GitHub-hosted Ubuntu. Отдельное имя исключает конфликт с `*-source.zip`,
который загружает существующий релизный workflow. Ручные запуски сохраняют
файлы в Actions-артефакте `attested-source`, без загрузки в релиз.

Выберите версию релиза и полный SHA коммита, который вы независимо проверили.
Просмотрите `.github/workflows/provenance.yml`, закреплённые actions и
`tools/build_source.py` именно в этом коммите. Не берите ожидаемый SHA из
недоверенного архива и не считайте тег неизменяемым. Затем выполните:

```sh
VERSION='<ver>'
COMMIT='<reviewed-release-commit>'
gh attestation verify "TgWitness-${VERSION}.zip" \
  --repo phishdestroy/TgWitness \
  --signer-workflow phishdestroy/TgWitness/.github/workflows/provenance.yml \
  --signer-digest "$COMMIT" --source-digest "$COMMIT" \
  --source-ref "refs/tags/v${VERSION}" --deny-self-hosted-runners
```

Успешная проверка подтверждает хеш файла, подпись SLSA provenance, репозиторий,
ревизию workflow, ревизию/ref исходников и использование hosted-раннера. Один
путь workflow **не** закрепляет его ревизию. Одна контрольная сумма не
устанавливает, кто собрал файл. Если проверка отсутствует или завершилась
ошибкой, этой гарантии нет. Повторите команду для файла `.zip.sha256`, чтобы
подтвердить и его подлинность. Для сохранённого bundle добавьте
`--bundle provenance.sigstore.json`; для полностью автономной проверки
заранее получите доверенные корни.

## Sealed evidence

Расшифровав передачу по [SEALED-ACTIONS](SEALED-ACTIONS.md), проверьте
`evidence.zip`, указав фактический форк, запустивший сбор (`OWNER/TgWitness`):

```sh
gh attestation verify evidence.zip --bundle attestation.jsonl \
  --repo OWNER/TgWitness \
  --signer-workflow phishdestroy/TgWitness/.github/workflows/sealed-collector.yml \
  --signer-digest eab5169e400ff3010d8853f42c8e430fe23ffe6b \
  --deny-self-hosted-runners
```

Просмотрите [закреплённый workflow коллектора](https://github.com/phishdestroy/TgWitness/blob/eab5169e400ff3010d8853f42c8e430fe23ffe6b/.github/workflows/sealed-collector.yml):
он загружает коммит коллектора `68fc80c3f4ca6764ffb178ce1a21f74dbd5dd6bf`.
Для проверки журнала, вложений, политики коллектора и полноты захвата также
запустите верификатор из независимо доверенной установки:

```sh
python -m tgwitness.sealed_verify evidence.zip --bundle attestation.jsonl --repo OWNER/TgWitness
```

## Публичные записи и SBOM

- **Прозрачность:** откройте ссылку Rekor в публичном отчёте шага attestation
  в Actions. Поле `verificationMaterial.tlogEntries` скачанного bundle содержит
  идентификатор журнала, индекс и доказательство включения;
  `gh attestation verify` проверяет подписанный bundle и данные журнала.
  Для просмотра связанной записи используйте [поиск Sigstore](https://search.sigstore.dev/).
  Запись фиксирует время обязательства по хешу, а не время сообщений Telegram.
  Подробнее — [роль Rekor](https://docs.sigstore.dev/logging/overview/).
- **Проверки репозитория:** откройте [отчёт OpenSSF Scorecard](https://securityscorecards.dev/viewer/?uri=github.com/phishdestroy/TgWitness).
  Смотрите дату, коммит и отдельные замечания, а не только оценку. Workflow
  запрашивает проверку по понедельникам в 04:32 UTC и при push в `main`;
  публикация делает результаты доступными в публичном датасете OpenSSF и
  подписанных записях Rekor. Это автоматический анализ, а не независимый
  человеческий аудит. Отсутствующий или устаревший отчёт не подтверждает успех.
- **Проверки workflow:** [workflow-audit.yml](../../.github/workflows/workflow-audit.yml)
  запускает zizmor при изменениях workflow и по понедельникам в 07:00 UTC.
  Артефакт `workflow-audit-sarif` содержит замечания об инъекциях, правах и
  закреплении actions. Результаты также загружаются в code scanning; доступ
  к его панели может быть ограничен.
- **Зависимости:** `sbom.spdx.json` — перечень компонентов репозитория,
  подписанный как результат сборки и связанный с ZIP через SPDX attestation.
  Подтвердите его командой проверки релиза выше, заменив имя файла на
  `sbom.spdx.json` и сохранив ограничения коммита/ref, затем проверьте локально:

  ```sh
  grype sbom:sbom.spdx.json
  ```

## Чего это не гарантирует

- Отсутствие ошибок, вредоносного поведения, уязвимых зависимостей или
  компрометации GitHub, Sigstore, одобренных actions и ваших инструментов проверки.
- Подлинность, правдивость и полноту содержимого Telegram; восстановление
  ненаблюдавшихся удалений; время сообщений; секретность от хоста сбора.
- Покрытие portable ZIP, wheel, контейнеров, автоматических архивов GitHub,
  прежних `*-source.zip` или релизов без этой attestation.
- Побайтовую воспроизводимость повторной сборки: текущий сборщик ZIP записывает
  время. Гарантия относится к конкретным опубликованным и подписанным байтам.
- Исчерпывающий SBOM установленной среды или отсутствие уязвимостей. SBOM
  описывает компоненты, обнаруженные сканером в репозитории исходников.
