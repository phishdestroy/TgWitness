# الأمن ومعالجة البيانات

Canonical page: https://phishdestroy.github.io/TgWitness/ar/docs/reference/security/

نموذج التهديدات، ونموذج الوصول، والأسرار المخزنة، والتعرض الشبكي، واستيراد الجلسات، وكيفية الإبلاغ عن الثغرات الأمنية.

This page describes access，storage and network protection in a local or server workspace． For collection on a GitHub runner or in an Intel TDX confidential VM，see the [verification modes](https://phishdestroy.github.io/TgWitness/ar/docs/reference/evidence/#verification-scope)，which add checks of the collection environment． Account connections，notifications，timestamps，off-site copies and witnesses have their own routing settings．

| المجال | باختصار |
| --- | --- |
| الوصول | مفتاح المسؤول بالإضافة إلى وصول محدود إلى الحسابات/الدردشات، وسبعة أذونات وجلسات قابلة للإلغاء؛ localhost بشكل افتراضي |
| الأسرار المخزنة | يتم تشفير الجلسة، وزوج واجهة برمجة التطبيقات (API)، ومفتاح التوقيع، وإعدادات الوكيل باستخدام Fernet |
| الرسائل والملفات الوسائطية | يتم التخزين دون تشفير: استخدم تشفير القرص وأذونات صارمة |
| النزاهة | سلسلة تجزئة SHA-256 وتوقيع Ed25519 على كل سجل |
| Local trust boundary | The host administrator controls the workspace and its signing key；independent checkpoints retain an earlier journal boundary |

للاطلاع على تقارير الثغرات الأمنية، انظر [سياسة الأمان](https://github.com/phishdestroy/TgWitness/blob/main/.github/SECURITY.md).

## نموذج الوصول

يمنح رمز اللوحة الرئيسية تحكمًا كاملاً. يمكن للأشخاص الآخرين الحصول على صلاحيات وصول [محددة النطاق](https://phishdestroy.github.io/TgWitness/ar/docs/reference/access/): مساحات العمل والدردشات المختارة، والأذونات، وتاريخ انتهاء الصلاحية، وقيود عناوين IP، وحدود تسجيل الدخول، والجلسات القابلة للإلغاء. لا يمكن للوصول المحدود بالدردشة تنفيذ عمليات على مستوى مساحة العمل بأكملها حتى لو تم تحديد أذونته. تشترك مساحات العمل في نفس العملية ولا تعزل البيانات عن المسؤول المضيف.

تستمع اللوحة إلى localhost بشكل افتراضي. يؤدي تسجيل الدخول عبر المتصفح إلى استبدال رمز الوصول ببيانات اعتماد الجلسة؛ ويقوم المتصفح بإرساله كرمز حامل. ويتم الاحتفاظ به في sessionStorage بدلاً من ملف تعريف ارتباط المصادقة. يؤدي القفل/تسجيل الخروج إلى مسح جلسة المتصفح. لا يؤدي إغلاق المتصفح أو إنهاء الجلسة إلى إيقاف عملية التجميع.

يتم الاحتفاظ بالرموز المميزة الصادرة وبيانات اعتماد الجلسة كرموز تجزئة في الخزينة المشفرة. يؤدي الإلغاء إلى إنهاء الجلسات المرتبطة؛ وتؤثر تغييرات الأذونات على الطلبات اللاحقة. لا يمكن استرداد الملفات التي تم تنزيلها. يمكن للمسؤول أيضًا تقييد جلسات المتصفح الخاصة به، لكن البرامج النصية التي تستخدم الرمز المميز للوحة الرئيسية تحتفظ مباشرةً بالوصول الكامل وتتجاوز حدود جلسات المتصفح تلك.

يتم تقييد معدل محاولات المصادقة الفاشلة حسب عنوان العميل. تستخدم قيود عناوين IP العنوان الذي يراه التطبيق؛ لذا يجب التحقق من سلوك الوكيل العكسي قبل الاعتماد عليه. تظل بيانات اعتماد Witness منفصلة عن بيانات اعتماد نقاط الفحص/التحقق من الحالة، وهي مخصصة للقراءة فقط.

### الوصول إلى النسخة التجريبية

`/api/demo-access` هو أداة تمهيدية غير مصدقة عن عمد من أجل عرض توضيحي اصطناعي معزول تم بدء تشغيله بشكل صريح. وهي تصدر إمكانية منفصلة تدوم طوال عمر العملية، وليس أبدًا رمز اللوحة الحقيقي أو تجاوز TGWITNESS_TOKEN. يتطلب الإصدار والاستخدام نظيرًا للارتداد (loopback) ومضيفًا، دون رؤوس معاد توجيهها، ودون طلب عبر الأصول. تؤدي مساحات العمل الإضافية أو الجلسة المصرح بها إلى تعطيل هذا المسار. لا تصدر مساحات العمل الحية هذه القدرة أبدًا. لا يمكن للعرض التوضيحي ربط الحسابات أو تغيير إعدادات التجميع.

## محتوى اللوحة وعمليات التصدير

لا تستخدم اللوحة أي خطوط خارجية أو أدوات تحليلية أو موارد شبكة توزيع المحتوى (CDN) أو وسائط بعيدة مدمجة. يتم إدراج النص المستمد من Telegram كنص عادي، وليس بتنسيق HTML. يتم تقديم المرفقات التي تم تنزيلها كمرفقات ثنائية. تحافظ عمليات التصدير بتنسيق JSONL على السلاسل النصية الأصلية؛ بينما يقوم HTML بتحويلها إلى رموز خاصة؛ وتُضاف علامة الفاصلة العليا كبادئة لخلايا CSV التي قد تتحول إلى صيغ حسابية.

تستبعد عمليات التصدير أسرار المصادقة والتوقيع، لكنها تحتوي عمدًا على البيانات الوصفية للمصدر التي تم جمعها، والمعرفات، وربما محتوى شخصي أو حساس. قد تظهر تجزئات الوصول إلى Telegram ومراجع الملفات في البيانات الوصفية الأولية للمصدر.

## الأسرار المخزنة

Telegram API credentials，the session and signing key are encrypted with Fernet． For local messages and media，encryption is provided by the host's disk or volume； the workspace stores ordinary files．Exports can use a password-protected AES-256 ZIP， and off-site copies use AES-256-GCM．

The vault key defaults to the protected data directory．Use an external master-key file below to store it separately．On Unix，new private-key files use mode 0600 and new data directories use 0700；on Windows，set the directory ACL for the service account and authorized administrators．Existing directory permissions are retained．

### مفتاح رئيسي خارجي

For a new data directory, TGWITNESS_VAULT_KEY_FILE can supply an external random master key. HKDF-SHA256 and a separate random salt derive a different Fernet key for each workspace. vault.external.json must be retained for recovery. Missing or wrong master keys fail closed. Existing local vaults are not silently migrated. The panel displays the selected key-storage mode．Disk encryption protects the local message and media files in either mode；see [connection and data protection](https://phishdestroy.github.io/TgWitness/ar/docs/reference/connection/) for setup details．

## الخوادم الوكيلة ومسارات الشبكة

يتم تشفير إعدادات الوكيل في الخزينة. ولا يتم إرجاع كلمات المرور وأسرار MTProxy عبر واجهة برمجة التطبيقات (API) أو تدوينها في سجلات الأدلة. تختار كل مساحة عمل مسار Telegram الخاص بها و[وضع IP](https://phishdestroy.github.io/TgWitness/ar/docs/reference/connection/#ip-modes).

**يؤدي إخفاء العنوان** إلى رفض الاستعانة المباشرة بـ Telegram كخيار بديل ويتطلب استخدام وكيل (بروكسي) لطلبات HTTP الخارجية. يسمح وضع الاستعانة البديلة المحدد صراحةً بالوصول المباشر إلى Telegram بعد فترة تأخير؛ بينما يسمح وضع النفق/VPN بالاتصال المباشر. لا يؤدي اختيار وضع النفق إلى تثبيت أو التحقق من VPN. لا تتحكم هذه الإعدادات في كل حركة مرور الجهاز أو المتصفحات أو مديري الحزم أو تحليل عناوين DNS لمضيف الوكيل المحلي.

تنقل MTProxy حركة مرور Telegram فقط. يمكن للطلبات الخارجية استخدام بروكسي SOCKS5/HTTP منفصل، أو مسار SOCKS5/HTTP الخاص بمساحة العمل، أو مسار مباشر مسموح به؛ كما يمكن تعطيلها. يمتلك الشاهد المستقل إعدادات النقل الخاصة به. لا يتم تشفير المصادقة العادية لـ SOCKS5/HTTP CONNECT بواسطة بروتوكولات الوكيل تلك نفسها. ولا تزال أسرار TLS المزيفة لـ MTProxy غير مدعومة.

## تسجيل الدخول واستيراد جلسات العمل

تحتوي ملفات .tgwitness-session المحولة على سر ترخيص بنص عادي حتى يتم تحميلها وتخزينها في الخزينة. تقبل واجهة سطر الأوامر (CLI) غير المتصلة بالإنترنت مخططات Telethon التي تمت مراجعتها. كما يقبل استيراد اللوحة Pyrogram SQLite، وملفات TData ZIP الحديثة ذات الحساب الواحد، ومدخلات JSON الموثقة. وهي مصادق عليها، ومحدودة بأربعة ملفات / 8 ميغابايت، وتعالج عمليات التحميل في الذاكرة دون استخراج الأرشيف أو حفظ الملفات الأصلية. يتم إرجاع بيانات الاعتماد المعيارية فقط إلى المتصفح المصادق عليه الطالب؛ ويتم حفظها في الخزينة المشفرة بعد نجاح عملية المصادقة عبر Telegram. قم بحماية الملفات الأصلية والمحولة، وتجنب قيام العملاء المتزامنين باستنساخ المصادقة.

تتحقق معالجة البيانات من مجموعات التحقق للحاويات، وتجزئات فك التشفير المحلية، وأطوال الهياكل. يتم استخدام رمز المرور المحلي المقدم لبرنامج سطح المكتب بشكل مؤقت ولا يتم تخزينه. لا يضمن هذا المحلل المحدود أن كل إصدار من إصدارات برنامج سطح المكتب متوافق. يتم إنشاء صور QR محليًّا، وتحتوي على رموز تسجيل دخول Telegram قصيرة الأمد، و لا يتم إرسالها أبدًا إلى خدمة عرض خارجية. يؤدي القفل، والتبديل بين مساحات العمل، وتسجيل الدخول الجديد، وتغييرات المسار إلى إلغاء محاولات QR المعلقة. قد تؤدي إعادة تحميل/إغلاق علامة تبويب إلى ترك محاولة معلقة حتى انتهاء صلاحيتها. لا يزال تسجيل الدخول الناجح عبر QR يفرض ربط الحساب. تظل أحجام نصوص واجهة برمجة التطبيقات (API) العادية محدودة بـ 16 كيلوبايت؛ بينما يقبل مسار الاستيراد المصادق عليه ما يصل إلى 12 ميغابايت من JSON المشفر، مع فرض حد أصغر للملفات المفككة التشفير بشكل منفصل.

لا يتم الاحتفاظ برموز تسجيل الدخول وكلمات مرور التحقق بخطوتين في Telegram. يتم الاحتفاظ بحالة رقم الهاتف/رمز التجزئة في الذاكرة أثناء عملية المصادقة. تمنح جلسات Telegram حق الوصول إلى الحساب؛ ولا يتم أبدًا تحميل دليل البيانات أو الجلسة أو الرمز المميز أو مفتاح الخزينة أو مفتاح التوقيع الخاص إلى GitHub.

## السجلات والنقل

تم استبدال استجابة التحقق الافتراضية لواجهة برمجة التطبيقات (API) بحيث لا تعكس قيم بيانات الاعتماد. تم تعطيل تسجيل وصول التطبيق. لا تقم بتكوين وكيل عكسي لتسجيل رؤوس التفويض أو نصوص الطلبات. ينقل بروتوكول HTTP الرموز وأسرار تسجيل الدخول بنص عادي: استخدم HTTPS أو نفق SSH عند مغادرة المضيف المحلي (localhost).

## حدود النزاهة

Local verification checks record signatures，the hash chain，attachments and the export manifest． The administrator holds the local signing key and can create another signed journal； an independently retained checkpoint detects replacement of the prefix it covers． Keep the key fingerprint and checkpoints with the recipient or an independent witness．

For independently checked collection，choose [GitHub Actions capture](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md) or [Intel TDX deployment](https://phishdestroy.github.io/TgWitness/ar/docs/reference/high-assurance/#confidential-vm-on-phala-cloud-intel-tdx)． Their verifiers check workflow provenance or hardware measurements in addition to archive integrity． Optional timestamps and encrypted off-site copies provide time anchors and recoverable copies； the [evidence format](https://phishdestroy.github.io/TgWitness/ar/docs/reference/evidence/#verification-scope) describes the checks for each mode．

## إذا كنت تشك في وجود مشكلة

Preserve the original data directory and use a separate copy for analysis． Report the affected version，operation and reproducible steps through the [security policy](https://github.com/phishdestroy/TgWitness/blob/main/.github/SECURITY.md)，keeping account data and credentials private．
