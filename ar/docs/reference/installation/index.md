# التثبيت والتحقق والتحديث

Canonical page: https://phishdestroy.github.io/TgWitness/ar/docs/reference/installation/

يمكن التثبيت بأمر واحد، والتحقق من التوقيعات والتجزئات، والتحديث، وإزالة التثبيت.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [التوثيق](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [البدء](https://phishdestroy.github.io/TgWitness/ar/docs/reference/quickstart/)

![البدء](https://phishdestroy.github.io/TgWitness/assets/chapter-start.svg)

[المشروع](https://github.com/phishdestroy/TgWitness/blob/main/README.md) · [البداية السريعة](https://phishdestroy.github.io/TgWitness/ar/docs/reference/quickstart/) · [النشر](https://phishdestroy.github.io/TgWitness/ar/docs/reference/deployment/)

**في هذه الصفحة**

- [التثبيت بأمر واحد](https://phishdestroy.github.io/TgWitness/ar/docs/reference/installation/#install-with-one-command)
- [حيث يعمل كل شيء](https://phishdestroy.github.io/TgWitness/ar/docs/reference/installation/#where-everything-runs)
- [إعدادات البحث عن النص الكامل](https://phishdestroy.github.io/TgWitness/ar/docs/reference/installation/#full-text-search-settings)
- [الوصول عبر سطر الأوامر](https://phishdestroy.github.io/TgWitness/ar/docs/reference/installation/#command-line-access)
- [التحقق قبل التشغيل](https://phishdestroy.github.io/TgWitness/ar/docs/reference/installation/#verify-before-running)
- [تحديث تثبيت موجود](https://phishdestroy.github.io/TgWitness/ar/docs/reference/installation/#update-an-existing-installation)
- [الأوامر اليومية في نظام Ubuntu](https://phishdestroy.github.io/TgWitness/ar/docs/reference/installation/#everyday-commands-on-ubuntu)
- [إزالة TgWitness](https://phishdestroy.github.io/TgWitness/ar/docs/reference/installation/#remove-tgwitness)

## التثبيت بأمر واحد

يتضمن المثبت الموجه بيئة تشغيل خاصة لـ Python. استخدم العنوان نفسه للتثبيتات المستقبلية: فكل إصدار يقوم بتحديث المثبت، والتجزئات، والتوقيعات، ومعلومات البناء معًا.

**Linux / macOS (Bash):**

```
curl -fsSL https://get.destroy.tools/install.sh | bash
```

على خادم Ubuntu، قم بتشغيل البرنامج كجذر (root) لتثبيت خدمة تعمل في الخلفية. على جهاز سطح المكتب، قم بتشغيله كمستخدم عادي.

**Windows (PowerShell أو موجه الأوامر):**

```
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "irm https://get.destroy.tools/install.ps1 | iex"
```

لا حاجة إلى مسؤول في نظام Windows. تترك العملية الفرعية لـ PowerShell المحطة الطرفية مفتوحة مع عرض النتيجة. ويبقى لغة Python والتبعيات ضمن التثبيت.

في نظام Ubuntu، اختر **«هذا الكمبيوتر**» أو **«رابط HTTPS مؤقت**» أو **«نطاق خاص**». يقوم المثبت بعرض عنوان اللوحة ومفتاح الوصول. للحصول على رابط مؤقت، افتح عنوان HTTPS هذا في متصفحك وأدخل المفتاح. في حالة الوصول المحلي إلى خادم بعيد، استخدم إعادة توجيه SSH من جهاز الكمبيوتر الخاص بك (`ssh -L 8787:127.0.0.1:8787 user@server`) وافتح `http://127.0.0.1:8787`. في نظامي macOS وWindows، تفتح اللوحة المحلية في متصفحك؛ حافظ على تشغيل محطة العمل الخاصة بها.

سجّل الدخول إلى Telegram في اللوحة واختر ما تريد جمعه. التثبيت وحده لا يبدأ عملية جمع البيانات من Telegram.

## المكان الذي يعمل فيه كل شيء

`get.destroy.tools` هي أداة **Cloudflare Worker تقدم التنزيلات الثابتة**. ولا تحتوي على لوحة TgWitness، ولا جلسة Telegram، ولا قاعدة بيانات أدلة المستخدمين. ولا يتم توجيهها إلى خادم VPS خاص بالمشروع. يعمل التطبيق على الجهاز الذي تنفذ عليه الأمر.

| التثبيت | البرنامج | البيانات |
| --- | --- | --- |
| Ubuntu كجذر | `/opt/tgwitness` | خدمة النظام: `/var/lib/tgwitness-<installation ID>`؛ استخدم `tgwitness paths` للحصول على المسار الدقيق. |
| مستخدمو Linux / macOS | `~/.local/share/tgwitness` | `data/live` في إطار ذلك التثبيت. |
| مستخدم Windows | `%LOCALAPPDATA%\TgWitness` | `data\live` في إطار ذلك التثبيت. |

اضبط `TGWITNESS_INSTALL_DIR` لاختيار مجلد آخر. الإصدارات المثبتة والبيانات منفصلتان. لا يقوم المثبت بتحميل حساباتك أو رسائلك أو مفاتيحك إلى موقع التنزيل. يؤدي اختيار نفق Cloudflare إلى توجيه حركة مرور اللوحة عبر Cloudflare؛ بينما يؤدي استخدام نطاقك الخاص إلى توجيهها إلى خادمك الخاص.

يتضمن كل تثبيت **START-HERE.html** و**START-HERE.txt**، مع المسارات المحلية والأوامر والروابط إلى المستودع. قم بتشغيل `tgwitness guide` لفتح الدليل. في نظام Windows، استخدم `& "$env:LOCALAPPDATA\TgWitness\bin\tgwitness.cmd" guide` في PowerShell.

## إعدادات البحث عن النص الكامل

لا يحتاج [البحث عن النص الكامل](https://phishdestroy.github.io/TgWitness/ar/docs/reference/search/) (معاينة) إلى أي إعداد. يتم إنشاء فهرسه في الخلفية بعد التحديث.

| متغير أو أمر | التأثير |
| --- | --- |
| `TGWITNESS_FULLTEXT=disk` | الافتراضي: يتم الاحتفاظ بالفهرس في `search/fulltext.sqlite3` كل مساحة عمل |
| `TGWITNESS_FULLTEXT=memory` | لا يوجد ملف فهرس؛ يتم إعادة إنشاء الفهرس عند كل بدء تشغيل |
| `TGWITNESS_FULLTEXT=off` | لا يوجد فهرس؛ البحث عن النص الدقيق فقط |
| `tgwitness index status` | حالة فهرس كل مساحة عمل |
| `tgwitness stop`, `tgwitness index rebuild`, `tgwitness start` | أعد بناء كل فهرس من السجل الموقّع |

يُفضل اختيار المسؤول في **«Journal» → «Filters» → «Search index»** على المتغير الخاص بمساحة العمل تلك. تبحث الأوامر عن دليل البيانات الخاص بالتثبيت الذي يتم تشغيلها عليه؛ وفي الأماكن الأخرى، أضف `--data-dir` المسار من `tgwitness paths`. للحصول على قاموس أوكراني كامل (بيانات GPL-3.0)، قم بتثبيت `pymorphy3-dicts-uk` في بيئة Python الخاصة بالتثبيت.

## الوصول عبر سطر الأوامر

يقرأ [سطر](https://phishdestroy.github.io/TgWitness/ar/docs/reference/cli/) [الأوامر](https://phishdestroy.github.io/TgWitness/ar/docs/reference/cli/) (نسخة تجريبية) الأرشيف بحثًا عن البرامج النصية والوكلاء.

| متغير | التأثير |
| --- | --- |
| `TGWITNESS_URL` | عنوان اللوحة الخاصة بـ `tgwitness search`, `context`, `messages`, `stats` و `export`؛ القيمة الافتراضية `http://127.0.0.1:8787` عند تعيين رمز مميز |
| `TGWITNESS_MCP_TOKEN` | أرشفة رمز الاتصال من **«التكاملات» → «MCP**»، الذي يتم مشاركته مع عملاء MCP؛ `--token-file` قراءته من ملف بدلاً من ذلك |
| `TGWITNESS_DATA` | يتم قراءة دليل البيانات مباشرةً في حالة عدم `--data-dir`أو لم يتم تقديم عنوان URL أو رمز مميز |

## التحقق قبل التشغيل

يعتمد الأمر المكون من سطر واحد على بروتوكول HTTPS في البرنامج النصي الأولي. يتحقق هذا البرنامج النصي من SHA-256 وتوقيع RSA الخاص بالمشروع على التطبيق والقيود قبل التثبيت. يمكنك أيضًا تنزيل البرنامج النصي الأولي والتحقق منه أولاً.

مفتاح الإصدار العام هو [release-signing.pub](https://github.com/phishdestroy/TgWitness/blob/main/deploy/installer/release-signing.pub). SHA-256 الخاص به هو:

```
039d98a658ccda14253e45a00335b4a68d840976d8ec18b8d4355cc7c458447d
```

احتفظ بهذه البصمة من إصدار مستودع تثق به. ويقوم مجموع اختباري من نفس خادم التنزيل باكتشاف أي عدم تطابق؛ والمفتاح العام الموثوق به بشكل مستقل هو ما يوثق توقيع الإصدار.

استخدم مجلدًا جديدًا فارغًا لتنزيلات التحقق أدناه.

**Linux / macOS — يتم تشغيلها في دليل تنزيل جديد وفارغ** (يتطلب وجود curl و OpenSSL):

```
curl -fSLO https://get.destroy.tools/install.sh &&
curl -fSLO https://get.destroy.tools/install.sh.sig &&
curl -fSLO https://get.destroy.tools/release-signing.pub &&
test "$(openssl dgst -sha256 release-signing.pub | awk '{print $NF}')" = \
  '039d98a658ccda14253e45a00335b4a68d840976d8ec18b8d4355cc7c458447d' &&
openssl dgst -sha256 -verify release-signing.pub -signature install.sh.sig install.sh &&
bash install.sh
```

تتوقف `&&` السلسلة قبل التنفيذ إذا فشل التنزيل أو فحص بصمة المفتاح أو فحص التوقيع . إذا تم النشر بين تنزيل البرنامج النصي وتوقيعه ، فقم بتنزيل كليهما مرة أخرى. تحتفظ برامج التثبيت القديمة بعناوين URL الثابتة لحزمها.

**نظام Windows — افحص العنصر SHA-256 قبل التشغيل:**

```
Invoke-WebRequest https://get.destroy.tools/install.ps1 -OutFile install.ps1 -UseBasicParsing
Get-FileHash .\install.ps1 -Algorithm SHA256
Invoke-RestMethod https://get.destroy.tools/SHA256SUMS.txt
```

قارن التجزئة مع `install.ps1` السطر. لإجراء فحص مستقل للتوقيع، استخدم OpenSSL (على سبيل المثال، من Git Bash) وبصمة المفتاح العام نفسها المذكورة أعلاه:

```
curl -fSLO https://get.destroy.tools/install.ps1 &&
curl -fSLO https://get.destroy.tools/install.ps1.sig &&
curl -fSLO https://get.destroy.tools/release-signing.pub &&
test "$(openssl dgst -sha256 release-signing.pub | awk '{print $NF}')" = \
  '039d98a658ccda14253e45a00335b4a68d840976d8ec18b8d4355cc7c458447d' &&
openssl dgst -sha256 -verify release-signing.pub -signature install.ps1.sig install.ps1 &&
powershell.exe -NoProfile -ExecutionPolicy Bypass -File install.ps1
```

يقوم نظام Windows نفسه بالتحقق من توقيعات الحزم باستخدام .NET ولا يتطلب OpenSSL. هذه توقيعات منفصلة من نوع RSA-3072 / SHA-256، وليست توقيعات Authenticode. يسجل [البيان](https://get.destroy.tools/manifest.json) إصدار البرنامج، والالتزام الدقيق في Git، ومعرّف الإصدار الثابت، وSHA-256 لكل عنصر. ترتبط الصفحة بالمصدر المقابل. كما يحتوي البيان وقائمة المجموع الاختباري على توقيعات منفصلة (`manifest.json.sig` و `SHA256SUMS.txt.sig`).

## تحديث تثبيت موجود

**يؤدي إصدار جديد إلى تحديث موقع التنزيل؛ وتتم تحديث البرامج المثبتة عند تشغيل المثبت مرة أخرى.** لا يوجد محدث يعمل تلقائيًا أو إعادة تشغيل تلقائية لـ مجموعة قيد التشغيل. قناة المثبت الحالية هي قناة **«معاينة**»؛ وهي تتبع الإصدارات المنشورة والمُراجعة من `main`، والتي قد يكون التزامها أحدث من آخر إصدار مرقّم على GitHub. يأتي إصدار الصفحة من `pyproject.toml`؛ حيث يميز التزامها ومعرف البنية التحديثات داخل نفس الإصدار التجريبي.

يتم النشر تلقائيًا بعد اجتياز ذلك الالتزام المحدد لفحوصات التطبيق و الأمان، واجتياز الحزمة الموقعة لاختبارات خدمة Ubuntu و تثبيت Windows PowerShell. أثناء إجراء الفحوصات، أو في حالة فشلها، تستمر الأوامر نفسها في تثبيت الإصدار الذي تم فحصه سابقًا. يُظهر بيان الإصدار الالتزام المتاح حاليًا؛ وقد يظل رقم الإصدار وحده كما هو بين تحديثات المعاينة.

استخدم مجلد التثبيت نفسه ومستخدم نظام التشغيل نفسه كما في السابق. قم بعمل نسخة احتياطية من دليل البيانات بالكامل مع إيقاف عملية التجميع؛ `tgwitness paths` يحددها. التصدير الموقّع ليس نسخة احتياطية كاملة للتثبيت.

**تثبيت Ubuntu كجذر في `/opt/tgwitness`:**

```
curl -fsSL https://get.destroy.tools/install.sh | TGWITNESS_INSTALL_DIR=/opt/tgwitness bash -s -- --no-start
```

بعد التثبيت بنجاح:

```
/opt/tgwitness/bin/tgwitness restart
/opt/tgwitness/bin/tgwitness status
/opt/tgwitness/bin/tgwitness open
```

لتثبيت المستخدم على نظامي Linux/macOS، استخدم الإعداد الأصلي `TGWITNESS_INSTALL_DIR` أو الإعدادات الافتراضية وقم بتشغيل أمر التثبيت الأول مرة أخرى. أغلق اللوحة الأمامية قبل التحديث وأعد تشغيلها بعد ذلك. بالنسبة لخدمة مستخدم Linux التي تم تكوينها، قم بتشغيل `tgwitness restart` الأمر الخاص بها.

**نظام Windows:** أغلق اللوحة قيد التشغيل، وقم بتشغيل أمر التثبيت الخاص بنظام Windows مرة أخرى، ثم افتح `bin\tgwitness.cmd` في نفس التثبيت. يحتفظ المثبت بالبيانات، وجلسات العمل، وإعدادات الوصول، ومفاتيح التوقيع. ولا يقوم بتبديل المشغل إلا بعد اجتياز البيئة الجديدة لفحوصاتها؛ أما في حالة فشل التثبيت، فيبقى المشغل السابق في مكانه. احتفظ بنسخة احتياطية ما قبل الترقية تحسبًا لتغييرات تنسيق التخزين.

## الأوامر اليومية في Ubuntu

| الأوامر | النتيجة |
| --- | --- |
| `tgwitness open` | عنوان URL الحالي للوحة ومفتاح الوصول. |
| `tgwitness paths` | المسارات الدقيقة للبرامج والبيانات والأدلة. |
| `tgwitness guide --print` | تعليمات التشغيل في وضع عدم الاتصال بالإنترنت. |
| `tgwitness status` / `tgwitness logs` | سجلات التوافر / الخدمة. |
| `tgwitness stop` / `tgwitness start` | إيقاف الخدمة أو استئنافها؛ الاحتفاظ بالبيانات. |
| `tgwitness token rotate` | استبدال مفتاح المسؤول وإنهاء جلسات المتصفح. |
| `tgwitness tunnel off` | قم بتعطيل النفق السريع العام؛ واحتفظ باللوحة المحلية. |
| `tgwitness tunnel on` / `tgwitness tunnel restart` | إنشاء رابط نفق سريع / استبدال عنوانه. |

انظر [قسم «الوصول»](https://phishdestroy.github.io/TgWitness/ar/docs/reference/access/) للاطلاع على رموز الزملاء والجلسات وقيود عناوين IP، و [نشر المثبت](https://github.com/phishdestroy/TgWitness/blob/main/deploy/installer/README.md#automatic-publication-from-github) لمعرفة سير عمل الإصدار من GitHub إلى Cloudflare.

## إزالة TgWitness

لا يوجد برنامج لإلغاء التثبيت: ما عليك سوى إيقاف تشغيل اللوحة وحذف مجلداتها. يؤدي حذف مجلد البيانات إلى إتلاف السجلات ومفاتيح التوقيع وجلسات Telegram والملفات المحفوظة نهائيًا. قبل ذلك:

1. قم بتصدير ما تحتاجه (**التصدير → تنزيل ZIP الموقّع**) واحتفظ ببصمة مفتاح التوقيع ونقاط التحقق خارج هذا الجهاز. للاحتفاظ بمساحة العمل نفسها، انسخ مجلد البيانات بالكامل بعد إيقاف عملية التجميع.
2. احذف الخوادم التي تم إنشاؤها ضمن **«Extras» → «Server 24/7»** من **«Your servers»** أو باستخدام `python -m tgwitness.cloud destroy`؛ حيث يقوم المزود بفوترة هذه الخوادم حتى يتم حذفها.
3. قم بإنهاء جلسة كل حساب في Telegram من خلال **«الإعدادات» → «الأجهزة**». لا يؤدي حذف الملفات إلى تسجيل الخروج من الجلسة من جانب Telegram.

**تثبيت Ubuntu كجذر.** لاحظ مجلد البيانات، وأوقف الخدمة، ثم قم بإزالة الخدمة والمجلدات والاختصار:

```
/opt/tgwitness/bin/tgwitness paths
/opt/tgwitness/bin/tgwitness stop
systemctl list-unit-files 'tgwitness-*'
systemctl disable tgwitness-<ID>
rm /etc/systemd/system/tgwitness-<ID>.service
systemctl daemon-reload
rm -rf /opt/tgwitness /var/lib/tgwitness-<ID> /usr/local/bin/tgwitness
```

**تثبيت مستخدمي Linux أو macOS.** أغلق اللوحة. يتم إيقاف خدمة مستخدم Linux المُهيأة باستخدام `systemctl --user disable --now tgwitness-<ID>`؛ وتوجد وحدتها في `~/.config/systemd/user/`. ثم احذف `~/.local/share/tgwitness` (أو `TGWITNESS_INSTALL_DIR`) و `~/.local/bin/tgwitness` الاختصار.

**نظام ويندوز.** أغلق اللوحة واحذفها `%LOCALAPPDATA%\TgWitness` (أو `TGWITNESS_INSTALL_DIR`). لا يضيف المثبت أي خدمة أو مهمة مجدولة أو اختصار.
