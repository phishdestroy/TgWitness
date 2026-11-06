# Arxitektura

Canonical page: https://phishdestroy.github.io/TgWitness/uz/docs/reference/architecture/

Yig'uvchi, panel, jurnal, ishchilar va guvoh komponentlari hamda ma'lumotlar ularning o'rtasida qanday harakatlanadi.

Bir Python jarayoni FastAPI panelini va istalgan sonli izolyatsiyalangan ish maydonlarini, har biri Telethon foydalanuvchi-akunenti bilan, mezbonlik qiladi. SQLite faqat qo'shimcha kiritishga mo'ljallangan imzolangan voqealar jurnalini va o'zgartiriladigan operatsion sozlamalarni saqlaydi. Shifrlangan ombor API ma'lumotlari, StringSession va imzolash kalitini saqlaydi. Frontend oddiy paketlangan HTML/CSS/JavaScript: Node build, CDN yoki frontend ish vaqti yuklamalari kerak emas.

Optional browser and AyuGram recorders run in **separate processes or containers**. The `tgwitness_capture` package owns their event format, keys, artifacts, checkpoint API, independent witness and standalone verifier. It is bundled in the main wheel and can also be installed alone from `addons/capture`, without importing the collector. The main panel's `capture_api.py` and `capture_connections.py` provide administrator-only, workspace-scoped controls under `/api/capture`; connection tokens live in the encrypted vault. No recorder or outbound request starts with the main process. Each explicit command verifies a fresh challenge against the pinned recorder key. Exports are verified before download and keep their original signature; they do not become Telegram message events. Collection sessions and proxy routes stay with each client. See the English [Independent capture guide](https://github.com/phishdestroy/TgWitness/blob/main/docs/OPTIONAL-CAPTURE.md) for deployment and trust boundaries.

| Modul | Mas'uliyat |
| --- | --- |
| collector.py | Avtorizatsiya, dialog tanlovi, yangilanishlar, snapshotlar, media navbati, ulanishni monitoring qilish |
| interactions.py / telegram_client.py | Panelning aniq harakatlari, imzolangan kvitansiyalar, doimiy so'rov identifikatorlari va vazifa-mahalliy callback/qo'shilishni qayta urinish siyosati |
| message_content.py | Kuzatiladigan xabarlarni solishtirish, transportga kirish metama'lumotlarini istisno qilgan holda |
| workers.py | Bekor qilishni tozalashdan oldin eksport fayllari ishchilarini kuting |
| distributed_export.py / distributed_pages.py | Concurrent chat jobs, per-account reservations, signed checkpoints and cleanup after archive verification |
| distributed_takeout.py / export_timing.py | Resumable Takeout sessions and timings for each start or resume |
| store.py | WAL tranzaktsiyalari, tartibga solingan voqealar zanjiri, so'rov filtrlari, operatsion sozlamalar |
| fulltext.py | To'liq matn indeksi (so'z shakllari, BM25) imzolangan jurnal boshiga bog'langan; hech qachon eksport qilinmaydi |
| security.py | Shaxsiy fayl yaratish, shifrlangan ombor, Ed25519 imzolash, yagona jarayon qulfi |
| evidence.py | Butun jurnalni eksport qilish, derivativlar, tekshiruv nuqtalari, ilovalarni tasdiqlash |
| verify.py | Mustaqil, faqat o'qish uchun mo'ljallangan tasdiqlovchi (stdlib + kriptografiya): arxivlar, qamrov, guvoh jurnallari va kanal postlari, profil fayllari |
| app.py | Avtorizatsiyalangan API, hayotiy tsikl, so'rovni tasdiqlash, statik panel |
| profiles.py | Bir nechta akkaunt yig'uvchilar, ulashilgan kirish nazorati, har bir ish maydoni bo'yicha hayotiy tsikl |
| access.py | Grantlar doirasini belgilash, ruxsatlarni tekshirish, IP-manzillarni cheklash, sessiya limitlari va administrator konsoli |
| proxy_catalog.py | Ommaviy kanallar yozuvlari, transport tekshiruvlari, ulashilgan proksi havzasi va holatga asoslangan tanlov |
| provenance.py | Imzolangan olish-ijro etish jarayonida shaxsiyat, kod va bog'liqlik o'lchovlari |
| network.py | Har bir ish maydoni bo'yicha tasdiqlangan yo'nalishlar; o'chirilgan holat va dalillar; Telethon transport variantlari |
| sessions.py | Ko'rib chiqilgan Telethon SQLite sxemalarini oflayn faqat o'qish uchun konvertatsiya qilish |
| account_import.py | Qo'llab-quvvatlanadigan akkaunt fayllari va JSON-larni xotirada aniqlash va normalizatsiya qilish |
| tdata.py | Cheklangan zamonaviy TData ZIP o'qirgichi, tekshirish summasi/dekripsiya tasdiqlovi, chiqarib olish yo'q |
| doctor.py | Mahalliy tayyorgarlik tekshiruvlari ma'lumot yig'ish, tizimga kirish yoki paket o'rnatilishini talab qilmaydi |
| download.py | Avtorizatsiyalangan jonli eksport yuklab olish, chegaralangan o'qishlar va ustma-ust yozishsiz |
| monitoring.py | Har bir ish maydoni bo'yicha voqealar siyosati va har bir turdagi ilovalar qoidalari tasdiqlangan, handlerlar, holat va imzolangan kvitansiyalar bilan baham ko'riladi |
| scope.py | Kuzatuv doirasi (tanlangan suhbatlar, Telegram papkasi, butun hisob), manba turlari, istisnolar, qayta tekshirish darajalari |
| dossier.py | Saklanib qolgan yozuvlar asosida chatdagi odam profillari: yozuv raqamlari bilan faktlar, avatar SHA-256/pHash, tilga olishlarni ajratib olish |
| witness_api.py | Faqat o'qish uchun mo'ljallangan guvoh tokenlari va ular olishi mumkin bo'lgan imzolangan jurnal sarlavhasi |
| witness.py | Mustaqil guvoh jarayoni: o'z kaliti va jurnal, bosh tekshiruvlari, imzolangan kanal postlari, eksport |
| alerts.py | Bildirishnomalar va panelning bildirishnomalar ro'yxati |
| logging_config.py | Penceresiz ishga tushirishlar uchun konsol yozuvlari va aylanib turuvchi server diagnostikasi |
| static/ | Moslashuvchan interfeys, mahalliy kirish darvozasi, filtrlar, tafsilotlar, eksportlar, hisob sozlamalari |
| demo.py | Aniq yorliq bilan belgilangan sintetik jurnal, haqiqiy to'plamdan ajratilgan |

Kuzatuv ishlovchilari ulanishdan oldin ro'yxatdan o'tkaziladi. Jonli yig'ish faol mijoz identifikatori, aniq bajarilish holati, yoqilgan manbalar yoki kuzatuv doirasi (papka yoki butun hisob rejimlari yangi suhbatni birinchi yangilanishida manba sifatida qo'shadi) va voqea siyosati bilan nazorat qilinadi. Rad etilgan va almashtirilgan mijozlar jonli yangilanishlarni taqdim eta olmaydi. Xom munosabatlar va a'zolik yangilanishlari ko'rinish chegaralarini saqlaydi. Kiruvchi xabar mazmuni va uning doimiy media vazifasi birgalikda yozib qo'yiladi. Vazifalar asl TL tavsiflagichni saqlaydi va uning xeshini imzolangan xabar kuzatuviga bog'laydi. Jo'natuvchi/tahrirlovchi/o'chiruvchi semantikalari ajratilgan.

Har bir ish maydoni bitta hisobni qabul qiladi va o'zining katalogi hamda imzolash identifikatori bilan ta'minlangan. Asosiy ish maydoni moslik uchun ildizda qoladi; qo'shimcha ish maydonlari profiles/<id>/ yo'lida joylashadi. Bitta egasi token butun o'rnatishni nazorat qiladi; ish maydonlari alohida ruxsatnomaga ega bo'lgan ijara bo'linmalari emas. Jarayon qulflari kataloglarni himoya qiladi; ma'lumotlar bazasi qulflari voqealarni kiritishni ketma-ket amalga oshiradi. Har bir qo'shimcha yozuv FULL sinxron rejimda SQLite WALga sinxron tarzda yoziladi. Voqea yangilanishi/o'chirish to'siqlari oddiy ilova tahrirlariga yo'l qo'ymaydi; fayl tizimi ma'murlari ishonch chegarasi ichida qoladi.

API authorization is a bearer token. Login operations are serialized and time-bounded. Account uploads use a dedicated 12 MiB encoded-body limit and an 8 MiB decoded-file limit; normal API requests retain the 16 KiB limit. Conversion runs in a worker thread, keeps uploads in memory, and returns normalized input to the authenticated browser. QR login has a per-workspace candidate, short-lived identifier, waiter task, and explicit cancellation. Only accepted authorization becomes the active client. Telegram FloodWait is returned with a Retry-After value; credentials and raw RPC error messages are not exposed in API errors. Journal exports run outside the async event loop and are serialized per workspace. They stream a stable read snapshot alongside continuing WAL writes. Chat acquisition jobs can run concurrently on separate accounts; each account remains reserved until its job stops. A paused or failed job retains its checkpoints. Successful archive verification permits cleanup of its working files, leaving the ZIP, signed plan and status. Workspace collectors share the process/event loop.

Joriy tarix snopshotlari va jonli yangilanishlar bir-birini kesib o'tishi mumkin. Ikkalasi ham alohida kuzatuvlar bo'lib, manba bo'yicha belgilangan; takrorlar jimjit birlashtirilmaydi. Yo'qolgan IDlar, soxta o'chirilgan matn, majburiy a'zolarni sanab o'tish yoki guruhga avtomatik qo'shilish asosida hech qanday xulosa chiqarilmaydi.

Operatorlar uchun tushuntirishni [to'plash qanday ishlashi](https://phishdestroy.github.io/TgWitness/uz/docs/reference/collection/) va [hisoblar hamda sessiya formatlari](https://phishdestroy.github.io/TgWitness/uz/docs/reference/accounts/) bo'limlarida ko'ring.

Tarmoq sozlamalari shifrlangan omborda saqlanadi. Yo'nalishni qo'llash eski klientlarni yopadi va yakunlanmagan kirishni bekor qiladi; keyingi ulanishlar o'sha yo'nalishdan foydalanadi va to'g'ridan-to'g'ri qaytish yo'q. Yangi tashqi kalit o'rnatilganda, har bir ish maydonining Fernet kaliti HKDF-SHA256 yordamida bosh kalit fayli va saqlangan tasodifiy tuzdan hosil qilinadi. Bu maxfiy ma'lumotlarni oddiy matndagi jurnal/media mazmunidan alohida himoya qiladi.

Mahalliy demo kirish alohida yaratilgan jarayon imkoniyatidan foydalanadi, hech qachon sozlangan panel tokenidan emas. Chiqarish va qabul qilish aniq demo rejimini, qo'shimcha ish maydonchalarsiz yoki ruxsat etilgan sessiyasiz sintetik ildizni, loopback peer/Host, proxy yo'naltirish sarlavhalarisiz va cross-origin brauzer so'rovisiz talab qiladi. Jonli APIlar bearer autentifikatsiyasini saqlab qoladi va demo rejimida yig'ish o'zgarishlarini rad etadi.
