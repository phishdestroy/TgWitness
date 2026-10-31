# الرسائل تتغير. احتفظ بما رأيته.

Canonical page: https://phishdestroy.github.io/TgWitness/ar/

[مفتوح المصدر / v0.7.0](https://phishdestroy.github.io/TgWitness/ar/docs/reference/changelog/)

التقاط رسائل Telegram، والحفاظ على التغييرات التي تطرأ عليها، وتصدير سجل موقّع.

[تجربة العرض التوضيحي](https://phishdestroy.github.io/TgWitness/demo/?lang=ar)[دليل الإعداد](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=ar)

يستخدم العرض التوضيحي بيانات خيالية. لا يلزم تسجيل الدخول إلى Telegram.

 [التقاط عبر GitHub Actions (نسخة تجريبية)](https://phishdestroy.github.io/TgWitness/ar/docs/capture/) [نسخة خارجية على S3: الإعداد والاستعادة](https://phishdestroy.github.io/TgWitness/ar/#s3)

رسالة عبر الزمن #0042

Northstar · الأبحاثمصدر/رسالة خيالية رقم 42

1. **الرسالة التي تم رصدها:**09:41:02

   يبدأ الملخص عند 14:00.
2. **تم الحفاظ على التعديل**09:43:18

   يبدأ الملخص عند 15:00.

   تم الاحتفاظ بالإصدار السابق
3. **إشعار الحذف**10:06:45

   يُحتفظ بالمحتوى المسجل في دفتر الأدلة الخاص بك.

ثلاث ملاحظات. تاريخ واحد. مثال

تختفي الرسالة. لكن السجل المسجل يبقى.

## كل تغيير يتم تسجيله. في المكان الذي تحتاجه بالضبط.

تصفح الواجهة باستخدام بيانات توضيحية خيالية.

TgWitness / المحادثات المحفوظةمساحة عمل المراقبة الخاصة بك

![محادثات Telegram المحفوظة باللون الداكن، مع الاحتفاظ بالتعديلات والرسائل المحذوفة في سياقها الأصلي](https://phishdestroy.github.io/TgWitness/assets/chats-dark.png)

01 / المحادثات المحفوظة: عرض مألوف للمحادثات، مع تسجيل عمليات التعديل وإشعارات الحذف بجانب الرسائل.

TgWitness / السجلمساحة العمل المحلية

![سجل يحتوي على الرسائل الملاحظة، والتعديلات، وإشعارات الحذف، والأحداث التي تمت تغطيتها](https://phishdestroy.github.io/TgWitness/assets/workspace.png)

02 / السجل: خط زمني قابل للبحث لما رصده حسابك، بما في ذلك الانقطاعات.

TgWitness / سجل التعديلاتمساحة العمل المحلية

![نافذة تفصيلية تقارن بين النسخة السابقة المسجلة والنسخة المعدلة من الرسالة](https://phishdestroy.github.io/TgWitness/assets/detail.png)

03 / سجل التعديلات: قارن بين الإصدارات المسجلة دون الكتابة فوق الملاحظة السابقة.

TgWitness / الصادرات الموقعةمساحة العمل المحلية

![مساحة عمل للتصدير توفر ملفات ZIP وJSONL وCSV موقعة، بالإضافة إلى تقرير HTML يمكن استخدامه دون اتصال بالإنترنت](https://phishdestroy.github.io/TgWitness/assets/exports.png)

04 / الصادرات الموقعة اصطحب السجل معك، مع قائمة محتويات ومدقق مستقل.

01 / التسجيل

### أنت تختار نطاق العمل.

المحادثات المختارة، أو مجلد Telegram، أو الحساب بأكمله. مساحة عمل منفصلة لكل حساب.

[قارن بين أوضاع التجميع](https://phishdestroy.github.io/TgWitness/ar/guides/modes.html#scope)

02 / الحفظ

### التغييرات تضيف إلى القصة.

تُحتفظ في السجل بالإصدارات التي تم التقاطها وإشعارات الحذف وفجوات المراقبة.

[انظر مصفوفة الأحداث](https://phishdestroy.github.io/TgWitness/ar/guides/modes.html#events)

03 / التسليم

### سجل متنقل.

ملف ZIP موقّع، وملفات محفوظة، وتقرير يمكن الاطلاع عليه دون اتصال بالإنترنت. حماية اختيارية بكلمة مرور.

[تصدير وتحقق من](https://phishdestroy.github.io/TgWitness/ar/docs/exports/)

## غيّر بايتًا واحدًا. وستخبرك السلسلة بذلك.

يرتبط كل حدث بالتجزئة السابقة ويحمل توقيع Ed25519.

![ترتبط الأحداث المسجلة برموز التجزئة السابقة، وتحمل توقيعات، وتُنقل في ملف تصدير قابل للتحقق.](https://phishdestroy.github.io/TgWitness/assets/evidence-chain-animated.svg)

![يؤدي تغيير أي سجل تم التقاطه إلى تغيير هاشه وإبطال إمكانية التحقق من السجل المرتبط به.](https://phishdestroy.github.io/TgWitness/assets/evidence-tamper-animated.svg)

![تتيح نقطة تحقق يتم الاحتفاظ بها بشكل منفصل للمستلم مقارنة السجل المُصدَّر مع ملاحظة سابقة.](https://phishdestroy.github.io/TgWitness/assets/evidence-checkpoint-animated.svg)

اطلع على ما تحدده كل آلية تحقق، وأين تكمن حدودها.

[استكشف ثمانية مستويات من الأدلة](https://phishdestroy.github.io/TgWitness/ar/guides/modes.html#levels)

## مستعد لمراجعة من شخص آخر.

قم بتسليم الملاحظات والملفات وتقرير HTML غير متصل بالإنترنت في حزمة واحدة موقعة.

[اقرأ نموذج الأدلة](https://phishdestroy.github.io/TgWitness/ar/docs/reference/evidence/)

tgwitness-evidence.zipحزمة موقعة

- 01

  ملاحظات أصليةسجلات JSONL + جدول CSV
- 02

  سياق سهل القراءةتقرير HTML يمكن قراءته دون اتصال بالإنترنت + الوسائط المحفوظة
- 03

  التحقق المستقلقائمة موثقة + أداة تحقق مستقلة

تكتشف التوقيعات أي تلاعب مقارنةً بمفتاح موثوق به. وهي لا تثبت أن الرسائل صادرة عن Telegram ولا تضمن التقاطها بالكامل. يحتاج محتوى السجل والملفات الوسائطية إلى تخزين مشفر توفره أنت.

## نسخ على S3. عمليات تدقيق خارجية.

احتفظ بنسخ مشفرة وأضف عمليات تحقق مستقلة.

معطلة افتراضيًا

### نسخ كل شيء إلى مساحة تخزين متوافقة مع S3

المذكرات والملفات ونقاط التحقق المختومة بختم زمني وصادرات الدردشات — يتم تشفيرها قبل تحميلها إلى AWS S3 أو أي وسيلة تخزين متوافقة.

**إعدادات التخزين والاستعادة**

التشفير من جانب العميل

يقوم `AES-256-GCM` بتشفير الكائنات الموجودة على هذا الجهاز. ويتلقى المزود الكائنات المشفرة.

نسخ مجدولة أو يدوية

انسخ الآن، أو اختر فترة زمنية تتراوح بين 1 و1,440 دقيقة. تحقق من التقدم في اللوحة.

Object Lock

اختر عدد أيام الاحتفاظ ووضع الاحتفاظ إذا كان الحاوية تدعم ذلك. تُظهر اللوحة ما إذا تم تأكيد الاحتفاظ بالنسبة للعنصر الذي تم تحميله أم لا.

استعادة مُثبتة

قم بتنزيل مفتاح التشفير واحتفظ به في مكان منفصل. قم باستعادة البيانات على جهاز آخر؛ ولا يتم نشر الملفات إلا بعد التحقق منها.

![لوحة نسخ كاملة خارج الموقع: نقطة النهاية، والمنطقة، والمخزن، ومفاتيح الوصول، والجدول الزمني، وأدوات التحكم في قفل الكائنات ومفاتيح الاستعادة](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)

اللوحة الكاملة مع الخيارات المتقدمة مفتوحة. لا تظهر أي بيانات اعتماد للتخزين.

السجلات ووسائل الإعلام`AES-256-GCM`تخزين متوافق مع S3

[تكوين S3 واستعادة نسخة](https://phishdestroy.github.io/TgWitness/ar/docs/exports/#s3)[اقرأ تفاصيل التحقق](https://phishdestroy.github.io/TgWitness/ar/docs/reference/evidence/#off-site-copy-and-restore-s3)

**ما لا يفعله** لا تقوم الأداة باستعادة البيانات دون مفتاح فك التشفير الذي تم تصديره، ولا تحل محل الشاهد المستقل.

### الإشعارات · Apprise

تنبيهات بالمشكلات وتغييرات الدردشة والملخصات اليومية عبر Apprise: تطبيقات المراسلة أو البريد الإلكتروني أو webhook JSON الخاص بك.

**لا يقوم** بذلك: لا يرسل نص الرسالة ما لم تقم بتمكين المقتطفات.

 [تكوين وجهات الإشعارات](https://phishdestroy.github.io/TgWitness/ar/docs/reference/operations/#notifications)

### طوابع زمنية خارجية

تجزئة نقاط التحقق ذات الطابع الزمني باستخدام RFC 3161 و OpenTimestamps.

**ما لا يفعله** ولا تعتبر الإيصال المعلق في التقويم بمثابة طابع زمني مؤكد لبيتكوين.

 [تحقق من أدلة الطوابع الزمنية](https://phishdestroy.github.io/TgWitness/ar/docs/reference/timestamp/)

### شاهد مستقل

يحتفظ مضيف منفصل بالملاحظات الموقعة ويمكنه نشر `TGW1` نقاط التحقق.

**ما لا يفعله** ولا يُعتبر إنشاء مساحتين للعمل على مضيف تجميع واحد بمثابة شاهدين مستقلين.

 [إعداد شاهد](https://phishdestroy.github.io/TgWitness/ar/docs/witness/)

### الاستعادة والثغرات الظاهرة

استئناف العمل بعد إعادة التشغيل. إعادة الفحص و `coverage.json` عرض الرسائل المستردة والفجوات.

**ما لا يفعله** ولا تعيد الأداة بناء كل تعديل فات أو رسالة اختفت.

 [فحص الاستمرارية والثغرات](https://phishdestroy.github.io/TgWitness/ar/guides/modes.html#continuity)

## مساحة العمل الأولى الخاصة بك تبدأ من هنا.

جرب النسخة التجريبية أولاً. قم بربط حساب مخصص عندما تكون جاهزًا. Windows، Linux، macOS، أو Docker.

[اقرأ دليل الإعداد](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=ar)

**جلسة مستوردة واحدة، وعميل واحد قيد التشغيل.**

لا تقم بتشغيل مفتاح TData/مفتاح الجلسة المستورد في Telegram Desktop وTgWitness في نفس الوقت. قد يقوم Telegram بإبطال صلاحية التفويض المشترك (AUTH_KEY_DUPLICATED). للاستخدام المتوازي، قم بإنشاء تسجيل دخول منفصل إلى TgWitness عبر الهاتف أو رمز الاستجابة السريعة (QR).

[اقرأ تحذير استيراد الجلسة](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=ar#session-warning)

**ألقِ نظرة قبل الاتصال.**

جرب مساحة العمل الافتراضية دون الحاجة إلى حساب Telegram.

[افتح العرض التوضيحي عبر الإنترنت →](https://phishdestroy.github.io/TgWitness/demo/?lang=ar)

Windows `scripts\Demo.cmd`Linux / macOS `sh start.sh --demo`

**أوامر التثبيت المحلي**

الخطوة 01

### احصل على المصدر.

[قم بتنزيل ملف ZIP المصدر](https://github.com/phishdestroy/TgWitness/archive/refs/heads/main.zip) واستخراجه، أو انسخ المستودع:

```
git clone https://github.com/phishdestroy/TgWitness.git
cd TgWitness
```

يتطلب تشغيل البرنامج وجود Python 3.11 أو أحدث. يوفر مشغل Windows خيار التثبيت في حالة عدم وجود Python.

[تصفح الإصدارات](https://github.com/phishdestroy/TgWitness/releases)

لا يتوفر لغة Python على نظام Windows؟ [قم بتنزيل الحزمة المحمولة](https://github.com/phishdestroy/TgWitness/releases/download/v0.7.0/TgWitness-0.7.0-windows-amd64-portable.zip)، وقم بفك ضغطها، ثم انقر نقرًا مزدوجًا على ملف `TgWitness.cmd`.

الخطوة 02

### اختر طريقة التشغيل.

انقر نقرًا مزدوجًا على `Start.cmd`، أو قم بتشغيله في PowerShell:

```
.\Start.cmd
```

هل تريد الاستكشاف فقط؟ انقر نقرًا مزدوجًا على `scripts\Demo.cmd` للحصول على نسخة تجريبية منفصلة. لا حاجة لتسجيل الدخول إلى Telegram.

مع توفر Python 3.11+ و`venv`:

```
sh start.sh
```

لفتح السجل الوهمي بدلاً من ذلك، قم بتشغيل `sh start.sh --demo`.

مع تشغيل Docker وتثبيت Compose 2.20+:

```
docker compose up -d --build --wait
docker compose exec tgwitness cat /data/panel-token.txt
```

يُظهر الأمر الثاني رمز لوحة التحكم الخاصة بك. احتفظ به على جهازك.

افتح [127.0.0.1:8787](http://127.0.0.1:8787) بعد التشغيل.

بالنسبة للتثبيت من المصدر، الرمز هو `data/live/panel-token.txt`. يمكن تسجيل الدخول إلى Telegram باستخدام إعدادات واجهة برمجة التطبيقات (API) المدمجة أو الزوج الخاص بك من [my.telegram.org](https://my.telegram.org). [دليل الإعداد الكامل ↗](https://phishdestroy.github.io/TgWitness/ar/docs/reference/quickstart/)

**TgWitness 0.7.0** [ما الجديد →](https://phishdestroy.github.io/TgWitness/ar/docs/reference/changelog/) · [الميزات والقيود المعروفة →](https://phishdestroy.github.io/TgWitness/ar/docs/reference/features/)

## تعليمات واضحة. خطوة تالية مفيدة.

[استكشف الأدلة ↗](https://phishdestroy.github.io/TgWitness/ar/docs/)

[### الأوضاع والسيناريوهات ومستويات الأدلة أربعة أوضاع للتجميع. ثمانية مستويات للتحقق. اعثر على مسار العمل المناسب لحالتك.](https://phishdestroy.github.io/TgWitness/ar/guides/modes.html)

[01 ### ربط حساب دعم استيراد البيانات عبر الهاتف ورموز QR والجلسات المدعومة.](https://phishdestroy.github.io/TgWitness/ar/docs/accounts/)[02 ### اختر وكيلًا قوائم MTProxy العامة أو مسارك الخاص.](https://phishdestroy.github.io/TgWitness/ar/docs/proxies/)[03 ### إعداد روبوت «Witness» نقاط تفتيش موقعة في قناتك على Telegram.](https://phishdestroy.github.io/TgWitness/ar/docs/witness/)[04 ### التصدير والتحقق مشاركة السجل المسجل والتحقق من سلامته.](https://phishdestroy.github.io/TgWitness/ar/docs/exports/)

## العمل على الأرشيف.

تحميل السجل، ومراجعة مصادر الذكاء الاصطناعي، وتوصيل عميل MCP، والتعرف على الوسائط المحفوظة، وإرسال webhooks موقعة.

متاح من المصدر الحالي. الإصدار التجريبي المحمول 0.7.0 أقدم من هذه الأدوات.

[استكشف سير العمل](https://phishdestroy.github.io/TgWitness/ar/docs/archive/)

## قبل أن تبدأ.

**هل ترتبط هذه الصفحة بـ Telegram؟**

لا. هذه صفحة مشروع ثابتة تحتوي على أمثلة خيالية ولقطات شاشة. يعمل التطبيق الفعلي على جهاز الكمبيوتر الخاص بك أو على الخادم الخاص بك؛ ويتم تسجيل الدخول من هناك.

**هل يمكنها استعادة الرسائل التي تم حذفها قبل تسجيلها؟**

لا. تحتفظ TgWitness بالمحتوى الذي رصده حسابك أثناء عملية التجميع. ولا يمكن لأي لقطة لاحقة من السجل إعادة بناء التعديلات التي فاتت أو الرسائل المحذوفة.

**هل السجل بأكمله مشفر؟**

يتم تخزين بيانات اعتماد الحساب وأسرار التوقيع في خزينة مشفرة. تتطلب الرسائل والمرفقات المحلية قرصًا أو وحدة تخزين مشفرة. يمكن للتصدير، بشكل اختياري، استخدام ملف ZIP مشفر بتقنية AES-256 ومحمي بكلمة مرور.

**هل هذا الموقع تابع لـ Telegram؟**

لا. TgWitness هو مشروع مستقل يستخدم Telethon، ويتم توزيعه بموجب ترخيص MIT. أنت تقوم بتفويض حساباتك الخاصة، باستخدام إعدادات واجهة برمجة التطبيقات (API) المدمجة أو زوج واجهة برمجة التطبيقات (API) الخاص بك.

PROJECT NOTICE / LICENCE

## Operator incompatibility.

**Taylor Wessing PartG mbB — German core, Hamburg office.**

Our statement as the authors of TgWitness. It adds no condition to the MIT License. Read the complete notice and its source record.

[Read the complete notice](https://phishdestroy.github.io/TgWitness/docs/reference/notice/) [Original text](https://phishdestroy.github.io/TgWitness/NOTICE)

## استكشف الموقع أولاً. قم بالإعداد عندما تكون مستعدًا.

[تجربة العرض التوضيحي](https://phishdestroy.github.io/TgWitness/demo/?lang=ar)[دليل الإعداد](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=ar)
