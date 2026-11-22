[TgWitness](../../README.md) / [Документация](../README.md) / [Папка](README.md) · [Справочная документация по проекту](../README.md)

![Справочная документация по проекту](../assets/presentation/chapter-project.svg)

<picture>
  <source media="(max-width: 640px) and (prefers-reduced-motion: reduce)" srcset="../assets/presentation/tgwitness-investigation-mobile-static.svg">
  <source media="(prefers-reduced-motion: reduce)" srcset="../assets/presentation/tgwitness-investigation-static.svg">
  <source media="(max-width: 640px)" srcset="../assets/presentation/tgwitness-investigation-mobile-animated.svg">
  <img src="../assets/presentation/readme-investigation-animated.svg" width="1376" alt="TgWitness — Follow the trail. Preserve the evidence. Sources connect to a case file; captured records are preserved and a signed handoff is prepared. Illustrated workflow with fictional records.">
</picture>

<a id="the-illustrated-investigation"></a>
# Иллюстрированное расследование

Как формируется дело — в иллюстрациях. Примеры являются вымышленными; для просмотра реального интерфейса [откройте демо-версию](https://phishdestroy.github.io/TgWitness/demo/).

[Проект](../../README.md) · [Руководство по расследованию](../wiki/Home.md) · [Модель доказательств](HOW-IT-WORKS.md)

<a id="link-the-captured-events"></a>
### Свяжите сохраненные события

<picture>
  <source media="(max-width: 640px) and (prefers-reduced-motion: reduce)" srcset="../assets/presentation/case-chain-mobile-static.svg">
  <source media="(prefers-reduced-motion: reduce)" srcset="../assets/presentation/evidence-chain-static.svg">
  <source media="(max-width: 640px)" srcset="../assets/presentation/case-chain-mobile.svg">
  <img src="../assets/presentation/readme-evidence-chain-animated.svg" width="1200" alt="Observe, preserve, verify: captured events link to previous hashes, carry signatures and travel in a verifiable export.">
</picture>

[Модель доказательств](HOW-IT-WORKS.md)

<a id="detect-a-changed-record"></a>
### Обнаружение измененной записи

<picture>
  <source media="(prefers-reduced-motion: reduce)" srcset="../assets/presentation/evidence-tamper-static.svg">
  <img src="../assets/presentation/readme-evidence-tamper-animated.svg" width="1200" alt="Changing a captured record changes its hash and breaks verification of the linked record.">
</picture>

[Экспорт и проверка](../wiki/Exports-and-Verification.md)

<a id="retain-an-independent-checkpoint"></a>
### Сохранение независимой контрольной точки

<picture>
  <source media="(prefers-reduced-motion: reduce)" srcset="../assets/presentation/evidence-checkpoint-static.svg">
  <img src="../assets/presentation/readme-evidence-checkpoint-animated.svg" width="1200" alt="A separately retained witness checkpoint lets a recipient compare the exported journal with an earlier observation.">
</picture>

[Независимый свидетель](../wiki/Independent-Witness.md)

Подпись подтверждает, что запись не была изменена после подписания. Проверка источника сообщения и проверка на наличие пропусков — это отдельные процедуры: происхождение проверяется по аутентифицированному сеансу Telegram учетной записи, а полнота — по записям об охвате и пробелах.

[Вернуться к проекту](../../README.md) · [Документация](../README.md)
