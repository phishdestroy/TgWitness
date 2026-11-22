[TgWitness](../../README.md) / [Документация](../README.md) / [Папка](README.md) · [Доказательства и проверка](EVIDENCE.md)

![Доказательства и проверка](../assets/presentation/chapter-evidence.svg)

<a id="independent-verification"></a>
# Независимая проверка

[Политика безопасности](../../.github/SECURITY.md)

Сверьте полученный вами файл с его публичным рабочим процессом и исходным коммитом. Записи о происхождении предоставляются хостируемыми на GitHub бегунами, OIDC и Sigstore; ваша политика проверки определяет, каким рабочим процессом и каким версиям кода вы доверяете.

Для архива Telegram начните с [запечатанных доказательств](#sealed-evidence) или [руководства](../wiki/Exports-and-Verification.md) по [подписанному журналу](../wiki/Exports-and-Verification.md) для локальной рабочей области. Для выпуска TgWitness следуйте приведённым ниже инструкциям по работе с исходным архивом.

<a id="release-source-archive"></a>
## Архив исходного кода выпуска

Установите последнюю версию [GitHub CLI](https://cli.github.com/manual/gh_attestation_verify). Из релиза скачайте файлы `TgWitness-<ver>.zip`, `.zip.sha256`, `sbom.spdx.json`, `provenance.sigstore.json` и `sbom.sigstore.json`. ZIP-архив сформирован скриптом `tools/build_source.py` на Ubuntu, размещённом на GitHub (он отличается от более старого ресурса `*-source.zip`).

Выберите полный SHA-хэш коммита, который вы проверили, ознакомьтесь с файлом `.github/workflows/provenance.yml`, закреплёнными в нём действиями и скриптом `tools/build_source.py` для данного коммита. Не используйте SHA-хэш из ненадежного архива и не предполагайте, что теги никогда не перемещаются. Затем:

```sh
VERSION='<ver>'
COMMIT='<reviewed-release-commit>'
gh attestation verify "TgWitness-${VERSION}.zip" \
  --repo phishdestroy/TgWitness \
  --signer-workflow phishdestroy/TgWitness/.github/workflows/provenance.yml \
  --signer-digest "$COMMIT" --source-digest "$COMMIT" \
  --source-ref "refs/tags/v${VERSION}" --deny-self-hosted-runners
```

Эта проверка включает в себя проверку дайджеста файла, подписи происхождения SLSA, репозитория, ревизии рабочего процесса, исходного коммита/ссылки, а также подтверждение того, что сборка была выполнена хостируемым раннером. Сама по себе контрольная сумма ничего не говорит о том, кто создал файл. Запустите проверку ещё раз на файле `.zip.sha256`. Для сохраненных пакетов добавьте параметр `--bundle provenance.sigstore.json`; для автономных проверок заранее загрузите доверенные корневые сертификаты.

Коммиты были объединены 3 ноября 2026 года. Теперь теги указывают на коммиты с теми же файлами, однако в подтверждениях более ранних выпусков указаны исходные коммиты, которые по-прежнему доступны на GitHub. Используйте их в качестве `COMMIT`:

| Релиз | Заверенный коммит |
| --- | --- |
| 0.8.1 | `5ad1569e0b5bc8fce6920b5439eb3e35418a2193` |
| 0.8.0 | `204e31bd294534574a9ef9428f24a38c81b57e6b` |
| 0.7.1 | `99225f985701b0cdccb333d947c6bb9bad8673aa` |

<a id="rebuilding-the-source-zip"></a>
### Пересбор исходного ZIP-архива

Скрипт `python tools/build_source.py` сортирует записи и корректирует временные метки, права доступа и параметры сжатия, благодаря чему одинаковые входные байты и библиотеки Python/zlib дают одинаковый ZIP-файл. Временная метка 1980 года является лишь нейтральным значением. Для сравнения с размещённым ZIP-файлом выполните сборку на основе проверенного коммита в чистом репозитории с теми же настройками окончаний строк и набором инструментов, а затем сравните значения SHA-256. Окончания строк и версии компрессоров могут повлиять на результат.

<a id="sealed-evidence"></a>
## Запечатанные доказательства

После расшифровки передачи из [SEALED-ACTIONS](SEALED-ACTIONS.md) сверьте файл `evidence.zip` с вашим форком (`OWNER/TgWitness`):

```sh
gh attestation verify evidence.zip --bundle attestation.jsonl \
  --repo OWNER/TgWitness \
  --signer-workflow phishdestroy/TgWitness/.github/workflows/sealed-collector.yml \
  --signer-digest c292ca0af97e3a4a0a2edd7f7eb00b21876afb57 \
  --deny-self-hosted-runners
```

Ознакомьтесь с [закреплённым рабочим процессом сборщика](https://github.com/phishdestroy/TgWitness/blob/c292ca0af97e3a4a0a2edd7f7eb00b21876afb57/.github/workflows/sealed-collector.yml), который извлекает коммит сборщика `f5c131ec4c5aad1b603617aa259a689f641b30dc`. Проверенные пары рабочих процессов и сборщиков перечислены в файле [`tgwitness/sealed_policy.json`](../../tgwitness/sealed_policy.json); используйте ту пару, которую закрепляет вызывающий рабочий процесс вашего форка. Для проверки журнала, вложений, политики и охвата также запустите верификатор из установки, которой вы доверяете:

```sh
python -m tgwitness.sealed_verify evidence.zip --bundle attestation.jsonl --repo OWNER/TgWitness
```

<a id="public-records-and-sbom"></a>
## Публичные записи и SBOM

- **Журнал прозрачности.** Ссылка «Сводка действий» на этапе аттестации ведёт на Rekor; файл `verificationMaterial.tlogEntries` в пакете содержит запись журнала и доказательство включения. Просмотрите её с помощью [поиска в Sigstore](https://search.sigstore.dev/). Временная метка записи журнала фиксирует момент фиксации, а не сообщения Telegram ([Rekor](https://docs.sigstore.dev/logging/overview/)).
- **Отчёт Scorecard.** [Отчёт OpenSSF Scorecard](https://securityscorecards.dev/viewer/?uri=github.com/phishdestroy/TgWitness) генерируется каждый понедельник и при каждом пуше в ветку `main`. Обратите внимание на дату, коммит и выявленные проблемы наряду с оценкой.
- **Аудит рабочего процесса.** [Файл workflow-audit.yml](../../.github/workflows/workflow-audit.yml) запускает zizmor при изменениях в рабочем процессе и каждый понедельник, в результате чего создаётся артефакт `workflow-audit-sarif`.
- **Зависимости.** Файл `sbom.spdx.json` объединяет результаты анализа Syft с точными версиями Python из файлов `deploy/requirements.lock`, `deploy/build.lock` и `deploy/constraints-mcp.txt`. Рабочий процесс завершается с ошибкой в случае отсутствия, наличия лишних или несоответствующих пакетов.

Проверьте подпись SBOM с помощью приведённой выше команды release (указав в качестве файла `sbom.spdx.json`) и её привязку к исходному ZIP-файлу:

  ```sh
  gh attestation verify "TgWitness-${VERSION}.zip" \
    --bundle sbom.sigstore.json \
    --predicate-type https://spdx.dev/Document/v2.3 \
    --repo phishdestroy/TgWitness \
    --signer-workflow phishdestroy/TgWitness/.github/workflows/provenance.yml \
    --signer-digest "$COMMIT" --source-digest "$COMMIT" \
    --source-ref "refs/tags/v${VERSION}" --deny-self-hosted-runners
  ```

Затем выполните сканирование локально:

  ```sh
  grype sbom:sbom.spdx.json
  ```

<a id="verification-scope"></a>
## Объём проверки

Аттестация выпуска связывает указанный файл загрузки и его дайджест с зарегистрированным рабочим процессом сборки и ревизией исходного кода. Проверьте, соответствует ли предоставленная аттестация именно тому артефакту, который устанавливается; для других форматов пакетов предусмотрены собственные процедуры публикации и проверки.

SBOM описывает заявленные версии пакетов, тогда как при сканировании эти версии сравниваются с базой данных уязвимостей. Архивы доказательств проверяются отдельно в соответствии с [процедурой проверки, предусмотренной для их режима сбора](EVIDENCE.md#verification-scope).
