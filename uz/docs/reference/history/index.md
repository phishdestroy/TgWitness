# Manba tarixini yuklash

Canonical page: https://phishdestroy.github.io/TgWitness/uz/docs/reference/history/

Yoqilgan manbalardan avvalgi xabarlarni yuklang, to'xtating va davom ettiring, shuningdek imzolangan progress hisobotini tasdiqlang.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Hujjatlash](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Yig'ma](https://github.com/phishdestroy/TgWitness/blob/main/docs/COLLECTION-MODES.md)

![Collection](https://phishdestroy.github.io/TgWitness/assets/chapter-collect.svg)

In **Sources**, review the enabled chats, pause observation, choose Standard API or Takeout export, then choose **Load full history**. The run fixes that list of sources and reads their available past messages into Chats and the signed observation journal. Media uses the existing attachment settings and durable download queue. This is separate from the per-chat signed JSON/HTML export.

For account-wide collection, select **Whole account**, start observation to load its source list, and review that list before starting history. The dialog-list limit still applies (1,000 by default, adjustable in Parameters). A successful run does not prove that every account dialog was listed. Chats discovered or enabled later need another run. Pause observation before starting history; one acquisition owns an account at a time.

Choose one to five attachment workers and whether to preserve available Recent Actions and compare previously saved versions. Takeout may require approval in Telegram and a server-specified wait. These options remain fixed on resume. See [Backfill behavior and evidence contract](https://github.com/phishdestroy/TgWitness/blob/main/docs/BACKFILL.md) for transport, retry and trust details.

## Tanaffus, qayta boshlash va qisman natijalar

- **Pause history** stops reading. **Continue history** resumes from the last committed message in each source; restarting the app also leaves the run paused until resumed. Resuming requires the same idle Telegram account.
- Xabarni kuzatish, ilova ishini bajarish va kursorni commit qilish bitta tranzaktsiyada amalga oshiriladi. Qayta boshlangan ijro allaqachon commit qilingan kuzatuvlarni takrorlamaydi. Jonli yozib olish yoki alohida, aniq boshlangan ijro mustaqil ravishda bir xil xabarni kuzatishi mumkin.
- Each source (each Telegram split range in Takeout) fixes an upper message ID on its first read. Newer messages belong to live observation, not to that source's remaining historical pages.
- Kirib bo'lmaydigan manbalar va olish jarayonida o'chirib qo'yilgan manbalar muvaffaqiyatsiz yoki o'tkazib yuborilgan holda ko'rinadi. Boshqa manbalar davom etadi; umumiy natija to'liq emas.
- FloodWait delays respect the saved account backoff. Transient failures retry up to five times; exhaustion and low disk space pause with the cursor intact.
- **End this history run** preserves saved observations. It does not remove them or cancel standard-API attachment jobs. Ending Takeout marks its remaining Takeout files as skipped; pausing keeps them resumable. A new run reads enabled sources anew.

Tarixni to'ldirish faqat o'qish rejimida tarixni ko'rsatadi. Ilovalar kutib turishi, muvaffaqiyatsiz bo'lishi yoki sozlangan siyosat tomonidan istisno qilinishi mumkin. Jurnal va ilovalar navbatidagi media kvitansiyalarini tekshiring; saqlangan ilova faqat saqlangan baytlarga ega bo'lgan yakuniy kvitansiya hisoblanadi. Tarix operatsiyasi aniq snapshot so'rovi bo'lib, kelajakdagi jonli voqealar toifalarini tanlaydigan kalitlardan alohida.

## Ko'chirish va tekshirish

**Imzolangan ijro hisobot**ini saqlang, so'ng **dalillarni eksport qilish** funksiyasidan foydalanib jurnal va saqlangan ilovalarni yuklab oling. Keyingi dalillar eksporti qo'shimcha yozuvlarni o'z ichiga olishi mumkin; hisobot o'z hisoblagichlarini yaratilgan paytdagi jurnal prefiksiga bog'laydi. Verifikatorni ushbu versiyaning ishonchli chiqishidan ishga tushiring:

```
python tgwitness/verify.py tgwitness-history-report.json --evidence evidence.zip --fingerprint TRUSTED_FINGERPRINT
```

Keep the expected signing-key fingerprint independently. The verifier checks the report signature, the evidence archive, the report checkpoint, source plan, account and counts of saved/unavailable messages. New runs also bind source progress and options to signed cursor events. Without `--evidence`, it checks only the signed report and its internal consistency. Legacy progress fields and attachment summaries remain signed collector statements. The evidence verifier checks archived media bytes.

Neither signing nor finishing the available history proves Telegram origin, an atomic snapshot, or historical completeness. Messages can change while reading; deleted messages and intermediate edits outside available Recent Actions, and Secret Chats, are not recovered. An operator controlling the signing key can fabricate a journal before outside commitments exist. Use separately retained checkpoints or an independent witness for the documented tamper-detection properties.

Yozib olish kursori mahalliy ish maydonining holatini bildiradi. Faqat dalillar ZIP-faylini tiklash kutib turgan yozib olish ishini yoki Telegram sessiyasini tiklamaydi. Agar asl ishni davom ettirish zarur bo'lsa, ish maydonining zaxira nusxasini saqlang.
