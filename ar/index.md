# الرسائل تتغير． احتفظ بما رأيته．

Canonical page: https://phishdestroy.github.io/TgWitness/ar/

[مفتوح المصدر ／ v0.9.0](https://phishdestroy.github.io/TgWitness/ar/docs/reference/changelog/)

احفظ محادثات Telegram مع كل تعديل وحذف، ثم سلّم سجلاً يمكن لأي شخص التحقق منه．

[تجربة العرض التوضيحي](https://phishdestroy.github.io/TgWitness/demo/?lang=ar)[دليل الإعداد](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=ar)

بيانات وهمية، بدون تسجيل دخول إلى Telegram．

 [التقاط عبر GitHub Actions （نسخة تجريبية）](https://phishdestroy.github.io/TgWitness/ar/docs/capture/) [نسخة خارجية على S3： الإعداد والاستعادة](https://phishdestroy.github.io/TgWitness/ar/#s3)

رسالة عبر الزمن ＃0042

Northstar · الأبحاثمصدر／رسالة خيالية رقم 42

1. **الرسالة التي تم رصدها：**09：41：02

   يبدأ الملخص عند 14：00．
2. **تم الحفاظ على التعديل**09：43：18

   يبدأ الملخص عند 15：00．

   تم الاحتفاظ بالإصدار السابق
3. **إشعار الحذف**10：06：45

   يُحتفظ بالمحتوى المسجل في دفتر الأدلة الخاص بك．

ثلاث ملاحظات． تاريخ واحد． مثال

تختفي الرسالة． لكن السجل المسجل يبقى．

## كل تغيير يتم تسجيله． في المكان الذي تحتاجه بالضبط．

الواجهة الحقيقية، ببيانات مختلقة．

TgWitness ／ المحادثات المحفوظةمساحة عمل المراقبة الخاصة بك

![محادثات Telegram المحفوظة باللون الداكن، مع الاحتفاظ بالتعديلات والرسائل المحذوفة في سياقها الأصلي](https://phishdestroy.github.io/TgWitness/assets/chats-dark.png)

01 ／ المحادثات المحفوظة تبدو كمحادثة عادية، مع التعديلات والحذف بجوار الرسائل مباشرة．

TgWitness ／ السجلمساحة العمل المحلية

![سجل يحتوي على الرسائل الملاحظة، والتعديلات، وإشعارات الحذف، والأحداث التي تمت تغطيتها](https://phishdestroy.github.io/TgWitness/assets/workspace.png)

02 ／ السجل كل ما رآه حسابك، قابل للبحث، بما في ذلك الفجوات．

TgWitness ／ سجل التعديلاتمساحة العمل المحلية

![نافذة تفصيلية تقارن بين النسخة السابقة المسجلة والنسخة المعدلة من الرسالة](https://phishdestroy.github.io/TgWitness/assets/detail.png)

03 ／ سجل التعديلات النسخ القديمة والجديدة جنبًا إلى جنب، دون الكتابة فوق أي شيء．

TgWitness ／ الصادرات الموقعةمساحة العمل المحلية

![مساحة عمل للتصدير توفر ملفات ZIP وJSONL وCSV موقعة، بالإضافة إلى تقرير HTML يمكن استخدامه دون اتصال بالإنترنت](https://phishdestroy.github.io/TgWitness/assets/exports.png)

04 ／ صادرات موقّعة خذ السجل معك، موقّعًا، مع أداة التحقق الخاصة به．

تتبع السجل المحفوظ عبر [«لوحة القضية](https://phishdestroy.github.io/TgWitness/ar/docs/case-board/)» （[Case Board](https://phishdestroy.github.io/TgWitness/ar/docs/case-board/)） [وتصميم التقرير](https://phishdestroy.github.io/TgWitness/ar/docs/reports/) و[نسخة](https://phishdestroy.github.io/TgWitness/ar/docs/handover/) [المشاركة](https://phishdestroy.github.io/TgWitness/ar/docs/handover/)． [راجع مجموعات الحسابات](https://phishdestroy.github.io/TgWitness/ar/docs/groups/) معًا．

01 ／ التسجيل

### أنت تختار نطاق العمل．

بضع محادثات أو مجلد أو الحساب بأكمله． لكل حساب مساحة عمل خاصة به．

[قارن بين أوضاع التجميع](https://phishdestroy.github.io/TgWitness/ar/guides/modes.html#scope)

02 ／ الحفظ

### التغييرات تضيف إلى القصة．

النسخ والحذف والفجوات تبقى كلها في السجل．

[انظر مصفوفة الأحداث](https://phishdestroy.github.io/TgWitness/ar/guides/modes.html#events)

03 ／ التسليم

### سجل متنقل．

ملف ZIP موقّع وملفات وتقرير يعمل دون اتصال． كلمة المرور اختيارية．

[تصدير وتحقق من](https://phishdestroy.github.io/TgWitness/ar/docs/exports/)

## إذا تم تغيير بايت واحد،
فسيُعلمك نظام التحقق بذلك．

يرتبط كل حدث بالتجزئة السابقة ويحمل توقيع Ed25519．

![ترتبط الأحداث المسجلة برموز التجزئة السابقة، وتحمل توقيعات، وتُنقل في ملف تصدير قابل للتحقق．](https://phishdestroy.github.io/TgWitness/assets/evidence-chain-animated.svg)

![يؤدي تغيير أي سجل تم التقاطه إلى تغيير هاشه وإبطال إمكانية التحقق من السجل المرتبط به．](https://phishdestroy.github.io/TgWitness/assets/evidence-tamper-animated.svg)

![تتيح نقطة تحقق يتم الاحتفاظ بها بشكل منفصل للمستلم مقارنة السجل المُصدَّر مع ملاحظة سابقة．](https://phishdestroy.github.io/TgWitness/assets/evidence-checkpoint-animated.svg)

اتبع عمليات التحقق بدءًا من تجزئة الملف وصولًا إلى نقطة التحقق المحفوظة بشكل منفصل．

[استكشف ثمانية مستويات من الأدلة](https://phishdestroy.github.io/TgWitness/ar/guides/modes.html#levels)

## مستعد لمراجعة من شخص آخر．

الرسائل والملفات وتقرير دون اتصال في حزمة واحدة موقّعة．

[اقرأ نموذج الأدلة](https://phishdestroy.github.io/TgWitness/ar/docs/reference/evidence/)

tgwitness-evidence.zipحزمة موقعة

- 01

  ملاحظات أصليةسجلات JSONL ＋ جدول CSV
- 02

  سياق سهل القراءةتقرير HTML يمكن قراءته دون اتصال بالإنترنت ＋ الوسائط المحفوظة
- 03

  التحقق المستقلقائمة موثقة ＋ أداة تحقق مستقلة

يتحقق المستلم من كل شيء مقابل مفتاحك، وتُظهر نقطة تحقق محفوظة في مكان آخر أن شيئًا لم يُعَد كتابته منذ ذلك الحين． [كيف تعمل عمليات التحقق．](https://phishdestroy.github.io/TgWitness/ar/docs/concepts/#layers)

## نسخ على S3． عمليات تدقيق خارجية．

احتفظ بنسخ مشفرة وأضف عمليات تحقق مستقلة．

معطلة افتراضيًا

### نسخ كل شيء إلى مساحة تخزين متوافقة مع S3

السجل والملفات ونقاط التحقق وصادرات المحادثات، مشفّرة قبل إرسالها إلى S3．

**إعدادات التخزين والاستعادة**

التشفير من جانب العميل

`AES-256-GCM` على جهازك． لا يرى المزوّد سوى النص المشفّر．

نسخ مجدولة أو يدوية

انسخ الآن أو كل 1 إلى 1，440 دقيقة، والتقدم يظهر في اللوحة．

Object Lock

اختر أيام الاحتفاظ ووضعه، وتتحقق اللوحة من أنه طُبِّق فعلاً．

استعادة مُثبتة

احفظ المفتاح بشكل منفصل． استعد في أي مكان، ولا تخرج الملفات إلا بعد التحقق．

![لوحة نسخ كاملة خارج الموقع： نقطة النهاية، والمنطقة، والمخزن، ومفاتيح الوصول، والجدول الزمني، وأدوات التحكم في قفل الكائنات ومفاتيح الاستعادة](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)

اللوحة الكاملة مع الخيارات المتقدمة مفتوحة． لا تظهر أي بيانات اعتماد للتخزين．

السجلات ووسائل الإعلام`AES-256-GCM`تخزين متوافق مع S3

[تكوين S3 واستعادة نسخة](https://phishdestroy.github.io/TgWitness/ar/docs/exports/#s3)[اقرأ تفاصيل التحقق](https://phishdestroy.github.io/TgWitness/ar/docs/reference/evidence/#off-site-copy-and-restore-s3)

**مفتاح الاسترداد** احفظه بشكل منفصل، فبدونه لا يمكن قراءة النسخة．

### الإشعارات · Apprise

المشكلات وتغييرات المحادثات وملخص يومي إلى تطبيقات المراسلة أو البريد الإلكتروني أو webhook الخاص بك．

**اختر ما تشاركه** لا يُرسل نص الرسائل إلا إذا فعّلته．

 [تكوين وجهات الإشعارات](https://phishdestroy.github.io/TgWitness/ar/docs/reference/operations/#notifications)

### طوابع زمنية خارجية

تجزئة نقاط التحقق ذات الطابع الزمني باستخدام RFC 3161 و OpenTimestamps．

**تابع النتيجة** تحقق من رد TSA أو رقِّ إيصال OpenTimestamps إلى إثبات Bitcoin．

 [تحقق من أدلة الطوابع الزمنية](https://phishdestroy.github.io/TgWitness/ar/docs/reference/timestamp/)

### شاهد مستقل

يحتفظ مضيف منفصل بالملاحظات الموقعة ويمكنه نشر `TGW1` نقاط التحقق．

**افصل المرجع** شغّله على مضيف آخر، بمفتاح وسجل خاصين به．

 [إعداد شاهد](https://phishdestroy.github.io/TgWitness/ar/docs/witness/)

### الاستعادة والثغرات الظاهرة

استئناف العمل بعد إعادة التشغيل． إعادة الفحص و `coverage.json` عرض الرسائل المستردة والفجوات．

**راجع الفترة** الرسائل المستردة والفجوات المسجلة جنبًا إلى جنب．

 [فحص الاستمرارية والثغرات](https://phishdestroy.github.io/TgWitness/ar/guides/modes.html#continuity)

## مساحة العمل الأولى الخاصة بك تبدأ من هنا．

جرّب العرض التوضيحي أولاً، ثم اربط حسابًا احتياطيًا حين تكون جاهزًا．
Windows أو Linux أو macOS أو Docker．

[اقرأ دليل الإعداد](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=ar)

**جلسة مستوردة واحدة، وعميل واحد قيد التشغيل．**

لا تشغّل TData أو جلسة مستوردة في Telegram Desktop وTgWitness في الوقت نفسه، فقد يُبطل Telegram كليهما （AUTH_KEY_DUPLICATED）． تحتاج كليهما؟ سجّل الدخول إلى TgWitness بشكل منفصل عبر الهاتف أو رمز QR．

[اقرأ تحذير استيراد الجلسة](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=ar#session-warning)

**ألقِ نظرة قبل الاتصال．**

جرب مساحة العمل الافتراضية دون الحاجة إلى حساب Telegram．

[افتح العرض التوضيحي عبر الإنترنت →](https://phishdestroy.github.io/TgWitness/demo/?lang=ar)

Windows `scripts\Demo.cmd`Linux ／ macOS `sh start.sh --demo`

**أوامر التثبيت المحلي**

الخطوة 01

### احصل على المصدر．

[قم بتنزيل ملف ZIP المصدر](https://github.com/phishdestroy/TgWitness/archive/refs/heads/main.zip) واستخراجه، أو انسخ المستودع：

```
git clone https://github.com/phishdestroy/TgWitness.git
cd TgWitness
```

يتطلب Python 3.11 أو أحدث． على Windows يعرض المشغّل تثبيته．

[تصفح الإصدارات](https://github.com/phishdestroy/TgWitness/releases)

الخطوة 02

### اختر طريقة التشغيل．

انقر نقرًا مزدوجًا على `Start.cmd`، أو قم بتشغيله في PowerShell：

```
.\Start.cmd
```

هل تريد الاستكشاف فقط؟ انقر نقرًا مزدوجًا على `scripts\Demo.cmd` للحصول على نسخة تجريبية منفصلة． لا حاجة لتسجيل الدخول إلى Telegram．

مع توفر Python 3.11+ و`venv`：

```
sh start.sh
```

لفتح السجل الوهمي بدلاً من ذلك، قم بتشغيل `sh start.sh --demo`．

مع تشغيل Docker وتثبيت Compose 2.20+：

```
docker compose up -d --build --wait
docker compose exec tgwitness cat /data/panel-token.txt
```

يُظهر الأمر الثاني رمز لوحة التحكم الخاصة بك． احتفظ به على جهازك．

افتح [127.0.0.1:8787](http://127.0.0.1:8787) بعد التشغيل．

في التثبيت من المصدر يكون الرمز في `data/live/panel-token.txt`． زوج API الخاص بك من [my.telegram.org](https://my.telegram.org) اختياري． [دليل الإعداد الكامل ↗](https://phishdestroy.github.io/TgWitness/ar/docs/reference/quickstart/)

**TgWitness 0.9.0** [ما الجديد →](https://phishdestroy.github.io/TgWitness/ar/docs/reference/changelog/) · [الميزات والقيود المعروفة →](https://phishdestroy.github.io/TgWitness/ar/docs/reference/features/)

## تعليمات واضحة． خطوة تالية مفيدة．

[استكشف الأدلة ↗](https://phishdestroy.github.io/TgWitness/ar/docs/)

[### الأوضاع والسيناريوهات ومستويات الأدلة أربعة أوضاع للتجميع． ثمانية مستويات للتحقق． اعثر على مسار العمل المناسب لحالتك．](https://phishdestroy.github.io/TgWitness/ar/guides/modes.html)

[01 ### ربط حساب دعم استيراد البيانات عبر الهاتف ورموز QR والجلسات المدعومة．](https://phishdestroy.github.io/TgWitness/ar/docs/accounts/)[02 ### اختر وكيلًا قوائم MTProxy العامة أو مسارك الخاص．](https://phishdestroy.github.io/TgWitness/ar/docs/proxies/)[03 ### إعداد روبوت «Witness» نقاط تفتيش موقعة في قناتك على Telegram．](https://phishdestroy.github.io/TgWitness/ar/docs/witness/)[04 ### التصدير والتحقق مشاركة السجل المسجل والتحقق من سلامته．](https://phishdestroy.github.io/TgWitness/ar/docs/exports/)

## العمل على الأرشيف．

السجل التاريخي، والذكاء الاصطناعي مع المصادر، وMCP، وOCR، وwebhooks موقّعة．

[استكشف سير العمل](https://phishdestroy.github.io/TgWitness/ar/docs/archive/)

## قبل أن تبدأ．

**هل ترتبط هذه الصفحة بـ Telegram؟**

لا． هذه صفحة ثابتة بأمثلة وهمية． يعمل التطبيق على جهازك وتسجّل الدخول هناك．

**هل يمكنها استعادة الرسائل التي تم حذفها قبل تسجيلها؟**

لا． يحتفظ بما رآه حسابك أثناء تشغيله． لا يمكن للقطة لاحقة إعادة بناء التعديلات الفائتة أو الرسائل المحذوفة．

**هل السجل بأكمله مشفر؟**

الجلسات والمفاتيح نعم． الرسائل والملفات لا، فاستخدم تشفير القرص． يمكن حماية الصادرات بكلمة مرور AES－256．

**هل هذا الموقع تابع لـ Telegram؟**

لا． إنه مشروع مستقل مرخّص بـ MIT ومبني على Telethon． تسجّل الدخول بحساباتك الخاصة．

PROJECT NOTICE ／ LICENCE

## Operator incompatibility．

**Taylor Wessing PartG mbB， German core， Hamburg office．**

This statement from the authors of TgWitness adds no condition to the MIT License， and the complete notice includes its source record．

[Read the complete notice](https://phishdestroy.github.io/TgWitness/docs/reference/notice/) [Original text](https://phishdestroy.github.io/TgWitness/NOTICE)

## استكشف الموقع أولاً． قم بالإعداد عندما تكون مستعدًا．

[تجربة العرض التوضيحي](https://phishdestroy.github.io/TgWitness/demo/?lang=ar)[دليل الإعداد](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=ar)
