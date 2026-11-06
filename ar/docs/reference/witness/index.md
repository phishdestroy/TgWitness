# شاهد مستقل

Canonical page: https://phishdestroy.github.io/TgWitness/ar/docs/reference/witness/

قم بتشغيل «شاهد» باستخدام مفتاحه الخاص وروبوته، وانشر نقاط التحقق الموقعة على قناة، وقارن الصادرات بها.

[التصدير والتحقق](https://phishdestroy.github.io/TgWitness/ar/docs/reference/evidence/) · [ضمان عالي](https://phishdestroy.github.io/TgWitness/ar/docs/reference/high-assurance/) · [دليل اللوحة](https://phishdestroy.github.io/TgWitness/ar/docs/reference/panel/#extras)

A witness retains signed checkpoints separately from the collector. It checks the collector's signature and journal continuity, signs the result with its own key, and publishes it to a Telegram channel. Run it on a separate server with read-only access to the collector's witness endpoint.

مخطط تدفق · أداة التجميع → Witness (نقطة التحقق الموقعة: عدد السجلات + هاش الرأس); Witness → سجل الشهود، مفتاح خاص; Witness → قناة Telegram (منشور موقّع عبر الروبوت الخاص بها); ملف ZIP للأدلة → verify.py; سجل الشهود، مفتاح خاص → verify.py; قناة Telegram → verify.py (صفحة التصدير من Telegram Desktop أو صفحة t.me/s) · أداة التجميع · Witness · سجل الشهود، مفتاح خاص · قناة Telegram · ملف ZIP للأدلة · verify.py · نقطة التحقق الموقعة: عدد · السجلات + هاش الرأس · منشور موقّع عبر الروبوت · الخاص بها · صفحة التصدير من Telegram · Desktop أو صفحة t.me/s

**الرسم التخطيطي كنص**

1. أداة التجميع → Witness (نقطة التحقق الموقعة: عدد السجلات + هاش الرأس)
2. Witness → سجل الشهود، مفتاح خاص
3. Witness → قناة Telegram (منشور موقّع عبر الروبوت الخاص بها)
4. ملف ZIP للأدلة → verify.py
5. سجل الشهود، مفتاح خاص → verify.py
6. قناة Telegram → verify.py (صفحة التصدير من Telegram Desktop أو صفحة t.me/s)

## ما يحصل عليه الشاهد، وما لا يحصل عليه

| الشاهد لديه | الشاهد لم يسبق له أبدًا |
| --- | --- |
| **رمز شاهد** للقراءة فقط لمساحة عمل واحدة | بيانات اعتماد جلسة Telegram الخاصة بالمجمع أو بيانات اعتماد واجهة برمجة التطبيقات (API) |
| مفتاح Ed25519 خاص بها وسجلها الخاص | خزينة المجمع، أو مفتاح التوقيع، أو رمز لوحة التحكم |
| رمز بوت Telegram الخاص به | محتوى الرسالة: يتكون العنوان من عدد السجلات وقيمة التجزئة |

يتم إنشاء الرمز المميز في **«Extras» → «Independent witness**»، ويظهر مرة واحدة ويتم تخزينه فقط على شكل SHA-256. يفتح نقطة نهاية واحدة فقط، `GET /api/witness/head`، والتي تُرجع نقطة تحقق موقعة حديثًا بالإضافة إلى عدادات المجموعات الخالية من المحتوى الموقعة وحالة التشغيل. لا يمكنها فتح اللوحة، أو قراءة محتوى الرسائل، أو تغيير الإعدادات، كما أن رمز اللوحة غير مقبول هناك. يمكن إلغاء الرمز في نفس الصفحة. يقوم المجمع بالتسجيل عندما يبدأ مفتاح شاهد جديد في الفحص (`witness.seen`) ويعرض آخر فحص لكل رمز؛ ويتم وضع علامة «متأخر» على الشاهد الذي لم يقم بالفحص خلال 2.5 فترة.

يرسل الشهود الجدد تحديًا عشوائيًا في كل استطلاع؛ وتكرره عبارة التسجيل تحت توقيع المجمع. وترتبط العدادات بنقطة التحقق المحددة وتُدرج في منشورات الشهود الموقعة. وتظل الرؤوس القديمة مقبولة من قبل الشاهد المستقل. ولا يُحسب نمو السجل وحده أبدًا كرسالة جديدة.

## ما الذي تتحقق منه وتسجله

في كل فترة زمنية (10 دقائق بشكل افتراضي)، تقوم الأداة بما يلي:

1. يسترد الرأس نفسه (لا يمكن للمجمع دفعه أو تخطيه)؛
2. verifies the collector's signature, the pinned collector key (`--collector-fingerprint`, or the first key seen), a nondecreasing count and an unchanged head at an unchanged count. Merkle inclusion and consistency proofs verify that a growing journal extends the retained checkpoint. Once continuity proofs have been used, removing them is rejected;
3. يُلحق سجلًا موقّعًا بسجله الخاص: `witness.anchor` مع الحالة `ok`، `key_changed`، `rollback` (عدد سجلات أقل من ذي قبل)، `fork` (نفس الطول، رأس مختلف ) أو `invalid` (فشل التحقق من الإجابة)، أو `witness.no_response` عندما لم يرد المُجمِّع؛
4. ينشر النتيجة على القناة، موقعة، بما في ذلك «لا يوجد رد» أثناء تشغيل TgWitness وإمكانية وصوله إلى واجهة برمجة تطبيقات الروبوت (Bot API). يتم تسجيل معرّف المنشور (`witness.posted`)، وكذلك المنشور الفاشل (`witness.post_failed`).

تبدو إحدى المنشورات كما يلي؛ ويحتوي السطر الأخير على البيان الموقّع:

```
TgWitness witness #42 · journal head
Collector 3fa9c2d1e0b4a7f6: 18234 records
Head 9b1f…c07e
2026-10-28T19:40:00.123+00:00
TGW1.eyJhdCI6…<statement>.<signature>
```

## تشغيل «Witness»

تحتاج إلى روبوت Telegram (يمكنك إنشاء واحد باستخدام @BotFather)، وقناة يكون هذا الروبوت مسؤولًا فيها، وعنوان أداة التجميع الذي يمكن الوصول إليه من قبل الشاهد — عبر HTTPS خارج شبكة خاصة (انظر ملف تعريف HTTPS في [قسم النشر](https://phishdestroy.github.io/TgWitness/ar/docs/reference/deployment/)).

افتح **«Extras» → «Independent witness» → «Configure»** في اللوحة. تتضمن الخطوات الثلاث الوصول للقراءة فقط، وقناتك، والفاصل الزمني، ثم تشغيل الشاهد. توجد سياسة النشر، ووكيل HTTP/SOCKS5 الاختياري، وعنوان واجهة برمجة تطبيقات الروبوت المخصص ضمن **«الإعدادات المتقدمة**». يقوم النموذج بتنزيل `witness.json` مع تثبيت مفتاح المجمع الخاص بمساحة العمل هذه. قم بتنزيل الرمز الذي تم إنشاؤه حديثًا للقراءة فقط باستخدام **«حفظ ملف الوصول** باسم» `witness-token.txt`؛ ضعه مع `bot-token.txt`تم إنشاؤه على مضيف الشاهد بجانب ملف JSON هذا. لا يتلقى المجمع أبدًا رمز البوت. لا يؤدي التنزيل إلى بدء تشغيل خدمة أو نشر رسالة. لا يتم تسجيل أي شاهد مشروع مستضاف ضمنيًا.

```
python -m tgwitness.witness run --config witness.json --check-config
python -m tgwitness.witness run --config witness.json
python -m tgwitness.witness fingerprint --config witness.json
```

يقوم الأمر الأول بالتحقق من ملفات التكوين والملفات السرية دون طلبات شبكة أو إنشاء مفتاح . المسارات في JSON نسبية بالنسبة لذلك الملف؛ أما مسارات CLI/البيئة فهي نسبية بالنسبة لدليل العمل. احتفظ ببصمة الشاهد خارج مضيفها. مؤشر «آخر استقصاء» الخاص بالمجمع يؤكد الطلب فقط؛ أما النشر فيتم الإبلاغ عنه بواسطة Proof أو التحقق منه في سجل الشاهد والقناة.

إذا كانت اللوحة تعمل خلف نفق SSH، فلا تكشف سوى نقطة النهاية المحددة لـ «Witness» على اسم مضيف HTTPS منفصل باستخدام [هذا المثال من Caddy](https://github.com/phishdestroy/TgWitness/blob/main/deploy/Caddyfile.witness.example). تستخدم مساحة العمل الافتراضية عندئذٍ `https://witness.example.org`، بينما تستخدم مساحات العمل الأخرى `https://witness.example.org/profiles/ID`. لا تزال الرموز مطلوبة؛ ولا يتم توجيه اللوحة و مسارات واجهة برمجة التطبيقات (API) الأخرى الخاصة بها عبر ذلك المضيف الافتراضي.

اختر `all` للحصول على نقاط فحص تُنشر بانتظام. الفاصل الزمني البالغ خمس دقائق يعني حوالي 288 منشورًا لكل مساحة عمل يوميًا. أما `changes` و`problems` فيتركان بعض عمليات الفحص غير منشورة عن قصد. MTProxy مخصص لعميل Telegram الخاص بالمجمع. يستخدم استطلاع Witness عبر HTTP وواجهة برمجة تطبيقات Telegram HTTPS Bot مسارها الخاص المباشر/HTTP/SOCKS5 ([Bot API](https://core.telegram.org/bots/api)).

**بجانب أداة التجميع، باستخدام Docker** (نفس المضيف — عملية ومفتاح مستقلان، لكن نفس المشغل): أدخل القيم في `.env` وابدأ تشغيل الملف الشخصي.

```
TGWITNESS_WITNESS_TOKEN=tgww_...
TGWITNESS_WITNESS_BOT_TOKEN=123456:ABC...
TGWITNESS_WITNESS_CHANNEL=@your_witness_channel
# another workspace: TGWITNESS_WITNESS_COLLECTOR=http://tgwitness:8787/profiles/<workspace ID>

docker compose --profile witness up -d
docker compose logs witness     # prints the witness key fingerprint
```

عند استخدام الصورة المنشورة، يرجى استخدام الرمز `docker compose --project-directory . -f deploy/compose/compose.image.yaml --profile witness up -d`.

**على خادم شخص آخر** (شاهد مستقل حقيقي): انسخ المستودع إلى هناك، واضبط `TGWITNESS_WITNESS_COLLECTOR=https://your-collector.example.org` بالإضافة إلى القيم الثلاث المذكورة أعلاه في `.env`، ثم

```
docker compose --project-directory . -f deploy/compose/compose.witness.yaml up -d
```

أو بدون Docker:

```
python -m tgwitness.witness run --collector https://your-collector.example.org \
    --token-file witness-token.txt --bot-token-file bot-token.txt --channel @your_witness_channel
```

### النشر على Discord

يمكن للشاهد النشر على قناة Discord بدلاً من Telegram. في Discord، افتح **«تحرير القناة» → «التكاملات» → «Webhooks»،** وأنشئ webhook وانسخ عنوان URL الخاص به. في اللوحة، اختر **«Discord webhook · قناتك»** في الخطوة 2. على مضيف الشاهد، احفظ عنوان URL باسم `discord-webhook.txt` بجوار `witness.json`؛ فهو لا يصل أبدًا إلى المجمع.

```
python -m tgwitness.witness run --collector https://your-collector.example.org \
    --token-file witness-token.txt --discord-webhook-file discord-webhook.txt
```

يكون لكل شاهد ناشر واحد: إما قناة Telegram أو webhook على Discord، وليس كلاهما. تحتوي المنشورات على نفس البيان الموقّع ولا يمكنها إرسال إشعار إلى أي شخص. يتم استبدال أي منشور يزيد طوله عن الحد الأقصى المسموح به في Discord وهو 2,000 حرف بسطر قصير مع إرفاق الفحص الكامل على النحو التالي `witness-check.txt`. يتم تسجيل معرّف كل منشور على أنه `witness.posted`. `verify.py --channel`يقرأ الصادرات من قناة Telegram فقط، لذا بالنسبة لـ Discord احتفظ بدفتر الشاهد: فهو يحتوي على كل فحص.

### خيارات

| خيار | البيئة | الافتراضي | المعنى |
| --- | --- | --- | --- |
| `--interval` | `TGWITNESS_WITNESS_INTERVAL` | 10 | الفترة الزمنية بين عمليات الفحص: 1–1440 |
| `--timeout` | `_TIMEOUT` | 30 | ثوانٍ للانتظار حتى يبدأ المجمع وواجهة برمجة تطبيقات الروبوت (Bot API) في العمل، 5–600 |
| `--post` | `_POST` | `all` | `all`: كل شيء على ما يرام؛ `changes`: بداية جديدة أو مشكلة؛ `problems`: مشاكل فقط وإجابات مفقودة |
| `--title` | `_TITLE` | `TgWitness witness` | الكلمات الأولى من كل منشور في القناة |
| `--collector-fingerprint` | `_COLLECTOR_FINGERPRINT` | – | قم بتثبيت مفتاح المجمع بدلاً من الوثوق بالإجابة الأولى |
| `--proxy` | `_PROXY` | مباشر | `socks5://host:port` أو `http://host:port` |
| `--bot-api` | `_BOT_API` | `https://api.telegram.org` | عنوان واجهة برمجة تطبيقات (API) الروبوت، على سبيل المثال خادم محلي لواجهة برمجة تطبيقات الروبوت |
| `--data-dir` | `_DATA` | `witness-data` | مفتاح الشاهد والسجل |
| `--config` | `_CONFIG` | – | ملف JSON مع أي من الخيارات المذكورة أعلاه |

يأتي عنوان المجمع والرموز والقناة من `--collector`, `--token` أو `--token-file`, `--bot-token` أو `--bot-token-file`, `--discord-webhook-file` و `--channel`، أو `_COLLECTOR`, `_TOKEN`, `_TOKEN_FILE`, `_BOT_TOKEN`, `_BOT_TOKEN_FILE`, `_DISCORD_WEBHOOK_FILE` و `_CHANNEL`، مما يحافظ على سرية العناصر من قائمة العمليات.

يستخدم ملف التكوين أسماء الخيارات مع علامات التسطير السفلية، بالإضافة إلى `texts`، الذي يحل محل الكلمات الموجودة في منشورات القناة:

```
{"collector": "https://your-collector.example.org", "token_file": "witness-token.txt",
 "bot_token_file": "bot-token.txt", "channel": "@your_witness_channel",
 "interval": 5, "timeout": 30, "post": "changes", "title": "Partner witness",
 "texts": {"ok": "journal head", "no_response": "no answer from the collector", "records": "records"}}
```

مفاتيح `texts`: `ok`، `key_changed`، `rollback`، `fork`، `invalid`، `no_response`، `collector`، `records`، `head`. خط الأوامر له الأسبقية على البيئة، والبيئة لها الأسبقية على الملف. تؤدي الخيارات غير المعروفة أو مفاتيح النص إلى إيقاف الشاهد برسالة بدلاً من تجاهلها. لا تؤثر الصياغة أبدًا على التحقق: يقوم verify.py بالتحقق من الرمز المميز الموقّع في نهاية كل منشور. مع `--post changes` أو `problems`، تظل عمليات التحقق التي لم يتم نشرها موجودة في سجل الشاهد، بينما يسردها `verify.py` على أنها لم تُنشر أبدًا؛ ويحدد سجل البداية السياسة. لا تزال كل عملية تحقق تظهر في السجل، لذا فإن عدد المنشورات الأقل يعني عددًا أقل من أوقات Telegram المستقلة، وليس عددًا أقل من عمليات التحقق.

حتى في حالة عدم وجود قناة، تظل أداة TgWitness تحتفظ بسجلها. احفظ بصمة مفتاح TgWitness (`python -m tgwitness.witness fingerprint`) في مكان آخر.

## صفحة إثبات عامة لعدة مساحات عمل

`python -m tgwitness.proof` تدعم TgWitness ما يصل إلى 32 مساحة عمل في آن واحد وتقدم صفحة للقراءة فقط تحتوي على أحدث فحص موقّع لكل منها. تحصل كل مساحة عمل على مفتاح witness خاص بها و سجل تحت مجلد البيانات ومفتاح جامع مثبت؛ ويُعد النشر على قناة Telegram اختياريًا لكل مساحة عمل. ابدأ من [ملف proof.config.example](https://github.com/phishdestroy/TgWitness/blob/main/deploy/proof.config.example):

| المجال | المعنى |
| --- | --- |
| `title` | عنوان الصفحة، 1–100 حرفًا |
| `data_dir` | مفاتيح و«المذكرات» الخاصة بـ«Witness»، المتعلقة بالملف؛ الإعدادات الافتراضية `proof-data` |
| `interval`, `timeout` | عدد الدقائق بين عمليات الفحص (1–1440، القيمة الافتراضية 5)؛ عدد الثواني للانتظار (5–600، القيمة الافتراضية 20) |
| `workspaces[].id`, `label` | اسم مستعار قصير بأحرف صغيرة والاسم المعروض |
| `workspaces[].collector` | عنوان Collector؛ أما مساحات العمل الأخرى فتنتهي بـ `/profiles/<workspace ID>` |
| `workspaces[].collector_fingerprint` | مطلوب، ويختلف من مساحة عمل إلى أخرى |
| `workspaces[].token_file` | ملف يحتوي على رمز الشاهد للقراءة فقط الخاص بمساحة العمل تلك |
| `workspaces[].channel`, `bot_token_file` | اختياري، معًا: انشر كل فحص على قناة |
| `workspaces[].proxy`, `bot_api` | مسار اختياري وعنوان واجهة برمجة تطبيقات الروبوت (Bot API) |

```
python -m tgwitness.proof --config proof.json --check-config
python -m tgwitness.proof --config proof.json --host 127.0.0.1 --port 8790
```

يقوم الأمر الأول بالتحقق من صحة الملف وملفات الرموز المميزة دون فتح اتصال. تستجيب الصفحة لطلبات GET و HEAD فقط:

- `/` يُظهر كل مساحة عمل؛ وتُصنف مساحة العمل التي لم يتم التحقق منها لمدة 2.5 فترة على أنها قديمة.
- `/api/proof` تُرجع نفس النتيجة التي تُرجعها JSON.
- `/api/proof/<id>` تنزيل أحدث بيان موقّع (`tgwitness-public-proof-v1`): رقم سجل الشاهد والتجزئة، والحالة، ومفتاح المجمع المثبت، ونقطة التحقق، وعدادات التجميع وما إذا كان نشر القناة قد نجح أم لا، موقّعًا بمفتاح الشاهد الخاص بمساحة العمل تلك.
- `/healthz` تُرجع الرمز 503 عندما يتوقف جهاز مراقبة مساحة العمل عن العمل.

أعطِ الصفحة اسم مضيف خاص بها، كما في [Caddyfile.proof.example](https://github.com/phishdestroy/TgWitness/blob/main/deploy/Caddyfile.proof.example). للتحقق، قم بتصدير سجل الشاهد الخاص بمساحة العمل باستخدام `python -m tgwitness.witness export --data-dir proof-data/<id> --out witness.zip` واستخدمها كما هو موضح أدناه.

## التحقق

من جانب الشاهد، قم بتصدير السجل الخاص به:

```
python -m tgwitness.witness export --out witness.zip
# Docker (add -f deploy/compose/compose.witness.yaml on a witness server):
docker compose exec witness python -m tgwitness.witness export --out /witness/witness.zip
docker compose cp witness:/witness/witness.zip .
```

بعد ذلك، في أي مكان، باستخدام ملف ZIP الموقّع من أداة التجميع والقناة التي تم تصديرها من Telegram Desktop (*تصدير سجل الدردشة* → JSON يعطي `result.json` ) أو صفحتها العامة `https://t.me/s/…` :

```
python verify.py tgwitness-evidence.zip --fingerprint COLLECTOR_SHA256 \
    --witness witness.zip --witness-fingerprint WITNESS_SHA256 --channel result.json
```

يقوم `verify.py` بالتحقق من سجل الشاهد (السلسلة والتوقيعات)، ثم التأكد من أن **كل رأس شاهده الشاهد هو جزء من السجل المصدَّر**: يجب أن يكون للسجل عند ذلك العدد بالضبط تلك القيمة التجزئية. أي رأس لا يتطابق يفشل في التحقق — مما يعني أن السجل قد تم تغييره بعد أن شاهده الشاهد. كما يبلغ عن الرؤوس التي شوهدت بعد التصدير، والانحرافات التي سجلها الشاهد ، والإجابات التي فشلت، والفترات التي توجد نقاط تفتيش مطابقة لها في هذا التصدير («تمت مشاهدتها من X إلى Y») والفجوات. لا تمدد نقاط التفتيش اللاحقة تلك الفترات. تتضمن النتيجة رقم السجل الأخير المطابق وعدد السجلات اللاحقة التي لا تحتوي على نقطة تفتيش مطابقة. لا تُحتسب سوى الإجابات الموقعة بمفتاح التصدير نفسه: يُبلغ عن التصدير الموقع بمفتاح لم يره الشاهد قط على أنه غير مشهود، وبدون `--fingerprint` يظل الموقع غير مثبت. مع `--channel`، يجب أن يتطابق كل منشور موقّع مع دفتر الشاهد سجلًا بسجل: تفشل المنشورات التي تم تغييرها في التحقق، ويتم إدراج المنشورات المفقودة في القائمة. يُعد التاريخ الموجود في ملف تصدير JSON المقدم من Telegram بيانات وصفية قابلة للتعديل، خارج نطاق رمز الشاهد الموقّع. لا تؤدي مطابقة الرمز إلى مصادقة تاريخ النشر؛ حيث تُشير النتيجة صراحةً إلى أنه لم يتم إجراء التحقق من وقت النشر.

### يلزم وجود حدود تصدير مشهود عليها

لإجراء عملية تسليم يجب أن تتضمن سجلاً نهائياً مشهوداً عليه، أضف `--require-witness`:

```
python verify.py tgwitness-evidence.zip --fingerprint COLLECTOR_SHA256 \
    --witness witness.zip --witness-fingerprint WITNESS_SHA256 --require-witness
```

وهذا يتطلب الاحتفاظ بشكل مستقل ببصمة الشاهد ونقطة تفتيش مطابقة في النهاية الدقيقة لعملية التصدير هذه. إن نقطة التفتيش التي تغطي فقط البادئة السابقة غير كافية. أوقف عملية التجميع مؤقتًا، ودع الشاهد يراقب الحالة النهائية، ثم قم بالتصدير قبل إجراء أي عمليات كتابة أخرى في السجل؛ إذا تغير السجل، فاحتفظ بنقطة تفتيش أخرى و قم بتصدير تلك الحالة. لا يمكن لنقطة فحص لاحقة بمفردها التحقق من التجزئة النهائية لعملية تصدير أقصر. عندما يتم توفير `--channel` أيضًا، فإن المنشورات المزعومة المفقودة أو مجموعة المطابقة الفارغة تفشل في اجتياز هذا الفحص الصارم. بدون العلامة، لا تزال فحوصات السلامة العادية تبلغ عن السجلات غير المشهودة دون رفض أرشيف سليم بخلاف ذلك.

Keep the witness journal and its pinned key separately. Online checks verify continuity between checkpoints; offline verification compares every retained checkpoint with the export. Legacy heads without continuity proofs retain the offline comparison and are reported without online continuity verification. The report lists witness downtime and failed publications by interval.

### Daily seals and unavailable timestamp calendars

The witness seals the previous UTC day's journal boundary and submits the hash of that signed seal to OpenTimestamps. A calendar submission is pending evidence; only independently checked Bitcoin commitments receive confirmation in the verifier.

If all calendars fail, the signed seal and unsuccessful attempt remain in the journal. The hourly maintenance pass retries that original record, including after a restart or a change of date. It scans at most 32 seals, submits at most two missing submissions and spends at most 60 seconds on retries per pass. A persistent cursor rotates through older seals. Retained submissions follow the existing proof-upgrade path.

A retry does not rewrite the seal, change its original date or claim that the calendar received it earlier. A later Bitcoin commitment remains a later external confirmation. Missing proofs remain `none`; pending proofs remain `pending` until the verifier checks them independently.
