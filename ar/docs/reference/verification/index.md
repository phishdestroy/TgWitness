# ما تم اختباره

Canonical page: https://phishdestroy.github.io/TgWitness/ar/docs/reference/verification/

اختبار Telegram المباشر، والفحوصات الآلية، وفحوصات المتصفح، وما لم يتم التحقق منه بعد.

## Live server journal inventory · 1 November 2026

At approximately 19:15 UTC, sequential read-only SQLite `query_only` queries counted events in ten workspace databases on a running server. Collection continued during the queries, so this is not an atomic snapshot across workspaces.

| Observed across the ten workspace databases | العدد |
| --- | --- |
| Workspaces with at least one `message.new` event | 8 |
| Journal records, including operational events | 1,610,818 |
| `message.new` events | 900,232 |
| `message.edited` events | 80,683 |
| `message.deleted` events | 400,536 |
| `message.recovered` events | 53,403 |
| `message.snapshot` events | 2,183 |
| `media.saved` events | 50,418 |
| `media.failed` events | 5,575 |
| `coverage.gap` events | 11 |
| Database bytes, excluding WAL files and media | 7,909,003,264 |

These are **event counts**, not unique messages, people or media files. The same message can appear in more than one workspace, and an edit or deletion can produce another journal event. `media.failed` counts historical failure events, not the current media queue. The queries did **not** newly verify signatures and the full hash chain of all 1,610,818 records, measure delivery or throughput, or establish that every Telegram event was captured. No message content, account or chat IDs, workspace labels, credentials or private files are published here.

At this review, the separately configured public monitor covered three sources: one capture response was OK and two reported `no_response`. That monitor is not a ten-workspace health summary. `no_response` means the observer could not obtain a response at that check; it does not establish message loss. The smaller 29 October test below has its own explicit signature and hash-chain verification.

## Recent offline and fault-injection checks · 1 November 2026

These checks use fictional data and local files; they add regression evidence for the current source, not another live Telegram delivery measurement:

| تحقق | What it exercised |
| --- | --- |
| [Source archive](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_source_archive.py) | Two builds with identical source bytes but changed file times produced the same ZIP and checksum. Exact archived bytes and file hashes matched; private test files stayed out. A simulated write failure left the previous archive and checksum intact. |
| [Account export recovery](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_account_export_recovery.py) | A simulated disk error on the second ZIP member left no published or partial ZIP. Resume kept every signed receipt byte-identical, produced an independently verifiable archive using the expected signing fingerprint, and retained the synthetic coverage gap as a partial result. Scale assertions guard against repeated task and receipt scans as histories grow. |
| [Minimized disclosure privacy](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_disclosure_privacy.py) | Synthetic Unicode names and aliases, nested metadata, unknown senders and media fields were checked in all three identity modes and with text omission. A masking-limit failure did not silently weaken redaction; the original signed account export stayed unchanged. |
| [Linux media decoder and OCR](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_media_worker.py) | A [Linux Docker CI check](https://github.com/phishdestroy/TgWitness/actions/runs/41341200341/job/124951395192) at commit `5a9e0814` passed generated Ogg/Opus, MP3, M4A, MP4 with video, WAV and FLAC inputs; forged-duration and secondary-file-reference controls; and 48 mutated parser fixtures (34 rejected, 14 decoded within bounds). Real Tesseract OCR ran with original bytes unchanged. The decoder and OCR ran in network-isolated containers without a Whisper model. |

The checks run in the [pull-request](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/pr-check.yml) and [full Checks](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/checks.yml) workflows. They test these failure boundaries, not every possible storage failure or whether a disclosure is automatically safe to publish. The media check does not measure speech recognition accuracy or Telegram delivery. Review each derivative before sharing.

## اختبار Telegram مباشر، الحساب بالكامل · 29 أكتوبر 2026

استمر الحساب نفسه في العمل بعد الاختبار المذكور أدناه. في 29 أكتوبر الساعة 12:10 بالتوقيت العالمي المنسق (UTC)، تم تغيير نطاقه ليشمل الحساب بأكمله (القنوات، والمجموعات، والمحادثات الخاصة، والروبوتات)؛ وطلبت لوحة التحكم التأكيد، وسجلت السجلات الموقعة ذلك. بحلول الساعة 17:59 بالتوقيت العالمي المنسق (UTC)، كان السجل يحتوي على:

| تم التسجيل في الفترة من 27 أكتوبر الساعة 21:36 إلى 29 أكتوبر الساعة 17:59 بالتوقيت العالمي المنسق (UTC) | العدد |
| --- | --- |
| سجلات السجل | 9,968 |
| رسائل جديدة | 5,308 |
| منها بعد الانتقال إلى الحساب الكامل | 3,878 |
| عمليات الحذف | 784 |
| تم حذفها بعد أن قام TgWitness بحفظ الرسالة | 596 |
| التعديلات | 41 |
| الرسائل المضافة بعد إعادة التحقق | 2,273 |
| الرسائل التي لم يعد بالإمكان العثور عليها عند إعادة الفحص | 18 |
| الرسائل المحفوظة عبر لقطات السجل | 242 |
| المرفقات المحفوظة | 247 |
| يبدأ برنامج التجميع | 19 |
| Telegram FloodWait في وضع الإيقاف المؤقت | 26 |

- أكدت عملية التحقق **«Verify»** التي أجرتها اللجنة صحة التوقيعات وسلسلة التجزئة لجميع السجلات البالغ عددها 9,968 سجلاً.
- جاءت الرسائل من مجموعتين أو قناتين و3 محادثات خاصة وبوتات. تم الضغط على زر رسالة واحد من **قسم «المحادثات**»؛ ويرد الطلب ورد Telegram في السجل.
- تمت إضافة محادثات جديدة عندما أعاد المجمع مسح الحساب عند إعادة التشغيل. كان خيار حفظ الرسائل السابقة للمحادثات الجديدة معطلاً (`history = 0`)، لذا لم يتم تناوله هنا.

لا يشمل الموقع: ردود الفعل، وتغييرات العضوية، وملفات تعريف الأشخاص، وإرسال الرسائل، والانضمام عن طريق الدعوة، والوكلاء، والإشعارات، وروبوت Witness، وعدة حسابات في آن واحد. الملفات العامة تحتوي على الأعداد فقط.

## ملف تصدير محمي بكلمة مرور يُفتح باستخدام libarchive · 29 أكتوبر 2026

تم فتح أرشيف تم إنشاؤه بواسطة كود تشفير التصدير (WinZip AES-256، وهو التنسيق الذي يقرأه كل من 7-Zip وWinRAR ) باستخدام Windows `tar` (bsdtar 3.6.2، libarchive). باستخدام كلمة المرور الصحيحة، تطابق الملف المستخرج مع قيمة SHA-256 الأصلية؛ أما كلمة المرور الخاطئة فقد تم رفضها بعبارة «عبارة مرور غير صحيحة ». ولم يتم تشغيل برامج 7-Zip وWinRAR نفسها.

## اختبار Telegram المباشر · من 27 إلى 29 أكتوبر 2026

قام حساب Telegram حقيقي واحد، تم تسجيل الدخول إليه عبر مجموعة أزواج واجهة برمجة التطبيقات (API) المدمجة، بتسجيل مجموعة كبيرة واحدة من **27 أكتوبر الساعة 21:36 بالتوقيت العالمي المنسق (UTC) إلى 29 أكتوبر الساعة 05:15 بالتوقيت العالمي المنسق (UTC)**. تم تشغيل أداة التجميع 12 مرة خلال تلك الفترة.

| مسجلة | العدد |
| --- | --- |
| سجلات السجل، بما في ذلك نبضات القلب وسجلات الخدمة | 2,385 |
| رسائل جديدة | 1,291 |
| عمليات الحذف | 472 |
| تم حذفها بعد أن قام TgWitness بحفظ النص | 347 |
| التعديلات | 12 |
| الرسائل التي فاتت أثناء التوقف، تمت إضافتها عند إعادة الفحص | 12 |
| المرفقات المحفوظة | 17 |
| المرفقات لم يتم تنزيلها (التنزيل معطل، أو لا يوجد ملف للتنزيل) | 14 |
| يقوم Telegram FloodWait بالتوقف مؤقتًا لمدة 3 ثوانٍ في كل مرة أثناء إعادة الفحص | 8 |

- يتم التحقق من التوقيعات وسلسلة التجزئة لجميع السجلات البالغ عددها 2,385 سجلًا مقابل المفتاح العام للسجل.
- بعد إعادة التشغيل، يستأنف المجمع العمل من حالة التحديث المحفوظة (`pts`) ويقوم Telethon بملء الفجوات؛ ثم تضيف عملية إعادة الفحص الرسائل التي لا تزال مفقودة.
- في كل مرة يواجه فيها المجمع حالة «FloodWait»، ينتظر المجمع المدة المطلوبة ثم يواصل العمل.
- ظل الحساب مسجلاً للدخول، وأعيد الاتصال بنفس الجلسة في 29 أكتوبر.

لا يشمل هذا الاختبار: التعامل مع عدة حسابات في آن واحد، وأدوار المسؤولين، والبروكسيات، وانقطاعات الخدمة التي تزيد مدتها عن بضع ساعات، وإ[جراءات القبول المباشرة](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md) الكاملة. تحتوي الملفات العامة على هذه العناصر فقط: لا توجد معرّفات للحسابات أو الدردشات، ولا رسائل، ولا بيانات اعتماد.

## قياس القدرات المحلية الاصطناعية

الأمر: `python tools/check_capacity.py --events 10000 --chats 100`

| المقاييس | تمت الملاحظة |
| --- | --- |
| المدخلات | 10,000 حدث رسالة اصطناعية عبر 100 مصدر اصطناعي مختار |
| نص الرسالة | 400 حرف؛ بدون وسائط أو شبكة |
| الاستيعاب | 53.273 ثانية؛ 187.7 حدثًا في الثانية |
| زمن استجابة المعالج | p50 4.162 مللي ثانية؛ p95 7.784 مللي ثانية؛ الحد الأقصى 129.118 مللي ثانية |
| تصدير ملف ZIP | 19.868 ثانية مع تمكين tracemalloc |
| ذروة تخصيصات تصدير Python التي تم تتبعها | 0.51 ميغابايت؛ لا يدعم RSS |
| حجم ملف ZIP | 4,610,962 بايت |
| التحقق المستقل | تم التحقق من صحة جميع الأحداث البالغ عددها 10,000 حدث |

يقيس هذا مسار التسجيل/التصدير التسلسلي المحلي على مضيف Windows هذا. ولا يقيس تسليم MTProto، أو الحسابات المتزامنة، أو تقييد سرعة Telegram، أو الوسائط، أو أعباء العمل طويلة الأمد، أو عددًا مضمونًا من المحادثات الحقيقية. ويأتي هذا القياس قبل أدوات الطابع الزمني النهائية في وضع عدم الاتصال، والتي لا تغير مسار الرسائل المقاسة.

## المؤهلات المتبقية

تثبت السجلات الحية المحفوظة عمليات التجميع الفعلية، وإشعارات التعديل والحذف، والمرفقات، عمليات إعادة التحقق، ومعالجة حدود معدل الاستخدام. ولا يثبت التسليم الشامل أو وجود مصفوفة خاضعة للرقابة لرؤية الأدوار، والجهات الفاعلة في الاستجابة، وFloodWait المطول، وحظر الحسابات، و استعادة الشبكة/العملية بعد الانقطاع. ويظل إصدار رمز QR منفصلاً عن التأكيد النهائي لرمز QR عبر الهاتف المحمول.

يظل كل من بناء/تشغيل Docker، والتثبيت على Linux/macOS، وتحمل الأحمال العالية المستمرة، والمراجعة الأمنية المستقلة، والاستجابة الحقيقية والمستقلة لـ TSA، والتحقق من إبطال الشهادات/أرشفتها، والشهادة الجنائية خارج نطاق المؤهلات المسجلة. تم تنفيذ حفظ حالة MTProto واللحاق بالرسائل؛ ولا يزال إعادة التشغيل المتين الذري غير مؤكد. يظل جمع سجلات الإدارة، وقوائم المفاعلات الإضافية، والاستطلاع القصير ذو الأولوية ميزات منفصلة. انظر [القبول المباشر](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md) لمصفوفة المؤهلات الخاضعة للرقابة.

توجد الإيصالات المحلية التفصيلية ولقطات الشاشة في المجلد test-results/ (مهملة في Git). تحتوي لقطات الشاشة العامة الموجودة في المجلد docs/assets/ على بيانات توضيحية خيالية فقط.
