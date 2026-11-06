# تحميل سجل المصدر

Canonical page: https://phishdestroy.github.io/TgWitness/ar/docs/reference/history/

تحميل الرسائل السابقة من المصادر الممكّنة، وإيقاف التشغيل مؤقتًا واستئنافه، والتحقق من تقرير التقدم الموقّع.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [التوثيق](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [المجموعة](https://github.com/phishdestroy/TgWitness/blob/main/docs/COLLECTION-MODES.md)

![Collection](https://phishdestroy.github.io/TgWitness/assets/chapter-collect.svg)

In **Sources**, review the enabled chats, pause observation, choose Standard API or Takeout export, then choose **Load full history**. The run fixes that list of sources and reads their available past messages into Chats and the signed observation journal. Media uses the existing attachment settings and durable download queue. This is separate from the per-chat signed JSON/HTML export.

For account-wide collection, select **Whole account**, start observation to load its source list, and review that list before starting history. The dialog-list limit still applies (1,000 by default, adjustable in Parameters). A successful run does not prove that every account dialog was listed. Chats discovered or enabled later need another run. Pause observation before starting history; one acquisition owns an account at a time.

Choose one to five attachment workers and whether to preserve available Recent Actions and compare previously saved versions. Takeout may require approval in Telegram and a server-specified wait. These options remain fixed on resume. See [Backfill behavior and evidence contract](https://github.com/phishdestroy/TgWitness/blob/main/docs/BACKFILL.md) for transport, retry and trust details.

## الإيقاف المؤقت، وإعادة التشغيل، والنتائج الجزئية

- **Pause history** stops reading. **Continue history** resumes from the last committed message in each source; restarting the app also leaves the run paused until resumed. Resuming requires the same idle Telegram account.
- يتم تسجيل ملاحظة الرسالة، ومهمة المرفقات، وتسجيل حركة المؤشر في معاملة واحدة. لا يكرر التشغيل المستأنف الملاحظات التي تم تسجيلها بالفعل. قد يقوم التسجيل المباشر أو تشغيل منفصل تم بدءه صراحةً بمراقبة نفس الرسالة بشكل مستقل.
- Each source (each Telegram split range in Takeout) fixes an upper message ID on its first read. Newer messages belong to live observation, not to that source's remaining historical pages.
- تظل المصادر التي يتعذر الوصول إليها والمصادر التي تم تعطيلها أثناء عملية الاستخراج مرئية على أنها «فشلت» أو «تم تخطيها». تستمر المصادر الأخرى؛ وتكون النتيجة الإجمالية غير مكتملة.
- FloodWait delays respect the saved account backoff. Transient failures retry up to five times; exhaustion and low disk space pause with the cursor intact.
- **End this history run** preserves saved observations. It does not remove them or cancel standard-API attachment jobs. Ending Takeout marks its remaining Takeout files as skipped; pausing keeps them resumable. A new run reads enabled sources anew.

يصف إكمال السجل قراءة السجل فقط. قد تظل المرفقات معلقة، أو تفشل، أو يتم استبعادها بموجب السياسة المُعدة مسبقًا. تحقق من إيصالات الوسائط في السجل وقائمة انتظار المرفقات؛ ولا يُعتبر مرفقًا محفوظًا إلا الإيصال المكتمل الذي تم الحفاظ على بايتاته. تعد عملية السجل طلبًا صريحًا لالتقاط لقطة، وهي منفصلة عن المفاتيح التي تحدد فئات الأحداث الحية المستقبلية.

## نقل والتحقق

احفظ **تقرير التقدم الموقّع**، ثم استخدم **خيار «تصدير الأدلة»** لتنزيل السجل والمرفقات المحفوظة. قد يتضمن تصدير الأدلة في وقت لاحق سجلات إضافية؛ حيث يربط التقرير عداداته ببادئة السجل في وقت إنشائه. قم بتشغيل أداة التحقق من نسخة موثوقة من هذا الإصدار:

```
python tgwitness/verify.py tgwitness-history-report.json --evidence evidence.zip --fingerprint TRUSTED_FINGERPRINT
```

Keep the expected signing-key fingerprint independently. The verifier checks the report signature, the evidence archive, the report checkpoint, source plan, account and counts of saved/unavailable messages. New runs also bind source progress and options to signed cursor events. Without `--evidence`, it checks only the signed report and its internal consistency. Legacy progress fields and attachment summaries remain signed collector statements. The evidence verifier checks archived media bytes.

Neither signing nor finishing the available history proves Telegram origin, an atomic snapshot, or historical completeness. Messages can change while reading; deleted messages and intermediate edits outside available Recent Actions, and Secret Chats, are not recovered. An operator controlling the signing key can fabricate a journal before outside commitments exist. Use separately retained checkpoints or an independent witness for the documented tamper-detection properties.

مؤشر الاستحواذ هو حالة مساحة العمل المحلية. لا تؤدي استعادة ملف ZIP الخاص بالأدلة وحده إلى استعادة مهمة الاستحواذ المعلقة أو جلسة Telegram. احتفظ بنسخة احتياطية من مساحة العمل إذا كان من الضروري متابعة المهمة الأصلية.
