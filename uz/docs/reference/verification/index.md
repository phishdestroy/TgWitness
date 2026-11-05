# Nima sinovdan o'tkazilgan

Canonical page: https://phishdestroy.github.io/TgWitness/uz/docs/reference/verification/

Jonli Telegram sinovi, avtomatlashtirilgan tekshiruvlar, brauzer tekshiruvlari va hali tasdiqlanmagan narsalar.

## Live Phala Cloud joylashtirish · 2026-yil 4-noyabr

`--provider phala --quick-tunnel` haqiqiy **Phala Cloud** (`tdx.small`, US-WEST-1 mintaqasi) bo'sh ish maydoni uchun Phala Cloud API kaliti, haqiqiy ntfy.sh, GitHub va Intel PCS bilan ishladi. CVM `df7d860c` (v0.8.1) commitini o'rnatdi; deploy, verify va destroy buyruq satridan quyidagi tuzatishlar bilan ishga tushirildi. Yetti CVM jami taxminan 1,9 AQSh sentiga tushdi.

Birinchi ikkita joylashtirish simulyatsiya qilingan Phala Cloud'dan beshta farqni aniqladi. [`tools/check_phala.py`](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_phala.py) endi har birini qayta hosil qiladi va tuzatishsiz xato beradi:

| Phala Cloudda | Tuzatishdan oldin | Tuzatish |
| --- | --- | --- |
| `compose_file.name` talab etiladi | HTTP 422, hech narsa yaratilmadi | Docker Compose konfiguratsiyasi CVM nomini o'z ichiga oladi |
| Bo'sh qiymat ko'rsatilmagan taqdirda, Phala o'lchangan app-comple ga o'zining ishga tushirishdan oldingi skriptini qo'shadi (v0.0.20: Docker login, `docker compose pull`, root paroli, `user_config` dan SSH kalitlari) | `tdx_compose` xato beradi: nashr etilgan Docker Compose konfiguratsiyasidan tashqaridagi kod | app-compose `pre_launch_script` ni `""` ga o'rnatadi; Phala esa uni hisobga olmaydi |
| `image` bo'lmasa, Phala `dstack-dev-0.5.12`, rivojlantirish versiyasini, SSH-kirish yoqilgan holda tanlaydi | `server_state` muvaffaqiyatsiz bo'ladi. Faqat uskunani tasdiqlash yozuvi ushbu tasvirdan o'tdi; faqat provayder yozuvi va `tdx_os` uni ko'rsatadi. | Joylashtirish Phala'ning joriy chiqarilishining, `dstack-0.5.12`, ishlab chiqarish versiyasini so'raydi |
| dstack gateway o'chirilganda, CVM tafsilotlari hech qachon `instance_id` kodini olmadi | Joylashtirish 30 daqiqa kutadi va muvaffaqiyatsiz tugaydi | Instance ID CVM holatidan o'qiladi |
| Qayta ishga tushirish, to'xtatish va ishga tushirish — bu CVM operatsiyalari, ilova reviziyalari emas. | `provider_actions` qayta ishga tushirishlarni ro'yxatga olmadi | Operatsiyalar ham o'qiladi |

Uchinchi joylashtirish:

- CVM `dstack-0.5.12` ni SSH kirish o'chirilgan holda ishga tushirdi. Kollektor yaratilganidan taxminan 1,5 daqiqa o'tib o'z imzolangan manzilini joyladi. Keyin Deploy `tdx_binding` va `tdx_quote` (Intel TCB UpToDate, apparat guvohnoma yozuvi v4, FMSPC `20a06f000000`, xatolik tuzatish rejimida emas, ko'chirilmaydigan, Intel'dan olingan kriptografik tasdiqlash ma'lumotlarini qo'llab-quvvatlaydi), `tdx_compose_hash`, `tdx_compose` (byte for byte) va `tdx_identity` (KMS kalitlari).
- trycloudflare.com manzildagi panel tokenisiz yoki noto'g'ri token bilan 401 kodini, panel tokeni bilan esa 200 kodini qaytardi.
- `verify` bilan `--source` commit arxivini GitHubga o'rnatish va barmoq izi alohida uzatilgan: server, `server_state`, firewall (yo'lchiqarsiz, ommaviy nuqtasi yo'q), provayder logi, bayonot, barmoq izi, manba xesh, yuklash va beshta `tdx_*` tekshiruvlari o'tkazildi. Cloudflare va `tdx_os` mavjud emas edi, shuning uchun natija TO'LAKAMAS bo'ldi.
- Phala API orqali ikki marta qayta ishga tushirish: har safar CVM ikki daqiqadan kam vaqt ichida bir xil yig'uvchi kalit, yangi imzolangan manzil va eski manzil 530-kod bilan javob bergan holda qayta ishga tushdi. `verify` yangi yuklashni va ikkala qayta ishga tushirishni REVIEW (ko'rib chiqish) deb xabar qildi. `--evidence` jurnal imzolarini va uchta ishga tushirishni tasdiqladi, har biri bir xil CVMdan olingan o'z Intel TDX apparat guvohnoma yozuviga ega edi.
- `destroy` faqat o'sha CVMni o'chirib tashladi. Shundan so'ng ish maydoni bo'shab qoldi va panel manzili javob berishni to'xtatdi.
- Panel ustasi narx tekshiruvi `tdx.small` soatiga $0.058 ni ko'rsatdi. Noto'g'ri kalit oddiy "API kalitini qabul qilmadi" xabarini berdi.

Keyinchalik tuzatilgan yana ikki topilma:

- Agar manzil kaliti bo'lmasa, `verify` manzil mavzusidagi eng yangi to'g'ri tuzilgan postni kuzatdi, u nashr etilgan Docker Compose konfiguratsiyasida chop etilgan. Bir soxta post uni mavjud bo'lmagan hostga yubordi, va `statement` muvaffaqiyatsiz bo'ldi: soxtalashtiruvchi yig'uvchi sifatida o'tolmaydi, lekin blok qilishi mumkin uchinchi tomon tasdiqlashni soxta kelajak vaqt belgisi bilan 12 soatgacha amalga oshiradi. Endi yig'uvchi o'z manzilini o'z kaliti bilan imzolab post qiladi, `verify` faqat yig'uvchi tomonidan qilingan bunday postlarni qabul qiladi va postlar ntfy.sh tomonidan qabul qilingan vaqt bo'yicha tartiblanadi. [`tools/check_cloud_wizard.py`](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_cloud_wizard.py) soxta postlarni qayta ijro etadi. CVM buni faqat uni o'z ichiga olgan commitdan ishga tushiradi, shuning uchun ushbu ijro etuvchi collector hali o'z manzilini imzolamagan va `verify` shuni bildirgan.
- `tdx_os` `dstack-mr`siz ishga tushmaydi, uning joriy versiyasida hujjatlarda ko'rsatilgan `measure --json` o'rniga `measure-os` mavjud. Verifikator endi nashr etilgan image va VM shakli, jumladan ACPI jadvallari asosida MRTD va RTMR0-2 ni o'zi hisoblaydi.

To'rtinchi joylashtirish, quyidagilar bilan:

- Deploy bir marta e'lon qilingan `dstack-0.5.12` ni yuklab olib, uni CVM xabar qilgan OS tasviri hashiga moslashtirdi va `tdx_os` o'tdi: MRTD, RTMR0, RTMR1 va RTMR2 QEMU uchun hisoblangan qiymatlarga teng. 8.2.2, 1 vCPU va 2 GiB. Xuddi shu hisob-kitob da'vo qilingan 4 GiB, 2 vCPU, QEMU 9.2.1 yoki ikkinchi tarmoq kartasi uchun boshqa RTMR0 berdi va o'zgartirilgan yadro, firmware yoki buyruq qatori hamda rivojlantirish tasviri uchun muvaffaqiyatsiz bo'ldi.
- `verify` o'zining 16 ta tekshiruvining barchasidan, jumladan Quick Tunnel konnektori tekshiruvidan ham muvaffaqiyatli o'tdi, shuning uchun natija PASS bo'ldi. U Belgiya hukumati vaqt belgilash bo'limi TSU 202301 (Belgiyaning ishonchli ro'yxatiga kiritilgan) tomonidan berilgan malakali eIDAS vaqt belgilashi, FreeTSA vaqt belgilashi va verifikator imzosi bilan raqamli muhrlangan HTML va PDF sertifikatini yaratdi; `check-report` ularning barchasini va PDF imzosi tasdiqladi.
- Qayta ishga tushirgandan so'ng, `verify --evidence` ikkita ishga tushirishni tasdiqladi, har biri CVM ichida yaratilgan apparat guvohnomasi bilan birga bo'lib, har biri e'lon qilingan `dstack-0.5.12` dan yuklangan; qayta ishga tushirish va yangi yuklash REVIEW bo'ldi.
- `destroy` ish maydonini bo'sh qoldirdi.

Beshinchi joylashtirish `53a0f7e9` commitidan collector-ni ishga tushirdi, unda yuqoridagilarning barchasi mavjud:

- Yig'uvchi o'z kaliti bilan imzolangan manzilini operatorning HMAC posti yoniga joylashtirdi. Keyin mavzuga ikkita soxta post qo'shildi: biri HMAC qiymati nolga teng qilingan, ikkinchisi boshqa Ed25519 kaliti bilan imzolangan; ikkalasi ham 2096 yildagi vaqtni da'vo qilgan. `verify` kollektor kaliti bilan imzolangan manzilni oldi va barcha 16 tekshiruvdan o'tkazdi; muhr yana malakali Belgiya vaqti shtampi, FreeTSA vaqti shtampi va verifikator imzosi bilan edi, va `check-report` ularni tasdiqladi.
- Qayta ishga tushgach, yig‘uvchi yangi manzilni imzolab e’lon qildi: `verify` uni darhol, operatorning **Joriy manzilni topish** funksiyasi esa HMAC xabaridan 27 soniya keyin topdi. Ikkalasi ham soxta xabarlarni e’tiborsiz qoldirdi. `verify --evidence` ikki ishga tushirish `dstack-0.5.12` dan yuklanganini tasdiqladi.
- Deploy chop etdi: Phala CVMga diskni ham qo'shib qancha to'lov solishini: soatiga $0.06078.

Panel ustasi Phala Cloud'da ikki marta ishga tushirildi: bir marta uning ish API'si orqali va bir marta haqiqiy Chromium brauzeri orqali: narxni tekshirish, **Advanced** ostidagi commit bilan yaratish, barcha oltita tasdiqlash tekshiruvlarining muvaffaqiyatli o'tishi, serverlar ro'yxatida to'langan narx (oyiga 44,37 USD) ko'rsatilishi, **Joriy manzilni topish**, o'lchangan Docker Compose konfiguratsiyasini yuklab olish va o'chirish. Brauzer hech qanday sahifa xatolarini ko'rmadi. Har safar undan keyin ish maydoni bo'sh bo'ldi.

Qamrab olinmagan: Phala'dagi Cloudflare domeni, CVM'dagi Telegram hisobi va `dstack-0.6.1` image. Yaratishdan oldingi ustaning narxi faqat Phala'ning hisoblash narxi bo'lib, chunki uning API mavjud CVM uchun faqat disk narxini ko'rsatadi; serverlar ro'yxati esa yaratilgandan keyingi to'lanadigan narxni ko'rsatadi.

## Live server journal inventory · 1 November 2026

At approximately 19:15 UTC, sequential read-only SQLite `query_only` queries counted events in ten workspace databases on a running server. Collection continued during the queries, so this is not an atomic snapshot across workspaces.

| Observed across the ten workspace databases | Hisob |
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

| Tekshirish | What it exercised |
| --- | --- |
| [Source archive](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_source_archive.py) | Two builds with identical source bytes but changed file times produced the same ZIP and checksum. Exact archived bytes and file hashes matched; private test files stayed out. A simulated write failure left the previous archive and checksum intact. |
| [Account export recovery](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_account_export_recovery.py) | A simulated disk error on the second ZIP member left no published or partial ZIP. Resume kept every signed receipt byte-identical, produced an independently verifiable archive using the expected signing fingerprint, and retained the synthetic coverage gap as a partial result. Scale assertions guard against repeated task and receipt scans as histories grow. |
| [Minimized disclosure privacy](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_disclosure_privacy.py) | Synthetic Unicode names and aliases, nested metadata, unknown senders and media fields were checked in all three identity modes and with text omission. A masking-limit failure did not silently weaken redaction; the original signed account export stayed unchanged. |
| [Linux media decoder and OCR](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_media_worker.py) | A [Linux Docker CI check](https://github.com/phishdestroy/TgWitness/actions/runs/41341200341/job/124951395192) at commit `5a9e0814` passed generated Ogg/Opus, MP3, M4A, MP4 with video, WAV and FLAC inputs; forged-duration and secondary-file-reference controls; and 48 mutated parser fixtures (34 rejected, 14 decoded within bounds). Real Tesseract OCR ran with original bytes unchanged. The decoder and OCR ran in network-isolated containers without a Whisper model. |

The checks run in the [pull-request](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/pr-check.yml) and [full Checks](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/checks.yml) workflows. They test these failure boundaries, not every possible storage failure or whether a disclosure is automatically safe to publish. The media check does not measure speech recognition accuracy or Telegram delivery. Review each derivative before sharing.

## Jonli Telegram sinovi, to'liq hisob · 29 oktyabr 2026

Quyidagi testdan so'ng shu akkaunt ishlashda davom etdi. 29 oktyabr kuni soat 12:10 UTCda uning doirasi butun akkauntga (kanallar, guruhlar, shaxsiy suhbatlar va botlar) o'zgartirildi; panel tasdiq so'radi va imzolangan jurnal buni qayd etdi. 17:59 UTCga kelib jurnalda quyidagilar qayd etilgan edi:

| Yozib olindi, 27 oktyabr 21:36 dan 29 oktyabr 17:59 UTC gacha | Hisob |
| --- | --- |
| Jurnal yozuvlari | 9,968 |
| Yangi xabarlar | 5,308 |
| ular butun akkauntga o'tkazilgach | 3,878 |
| O'chirishlar | 784 |
| ular TgWitness xabarni saqlaganidan keyin o'chirildi | 596 |
| Tahrirlar | 41 |
| Qayta tekshirishlar orqali qo'shilgan xabarlar | 2,273 |
| Qayta tekshirishda topib bo'lmaydigan xabarlar | 18 |
| Xabarlar tarix snopshotlari orqali saqlangan | 242 |
| Saqlangan ilovalar | 247 |
| Yig'uvchi ishga tushadi | 19 |
| Telegram FloodWait tanaffuslari | 26 |

- Panelning **Verify** tekshiruvi barcha 9 968 ta yozuvning imzolari va xesh zanjirini tasdiqladi.
- Xabarlar 2 ta guruh yoki kanal va 3 ta shaxsiy suhbat hamda botlardan kelgan. **Suhbatlardan** bir xabar tugmasi bosilgan; so'rov va Telegramning javobi jurnalda keltirilgan.
- Yangi suhbatlar hisobni qayta ishga tushirganda kollektor hisobni qayta skanerlaganida qo'shildi. Yangi suhbatlarning avvalgi xabarlarini saqlash o'chirilgan edi (`history = 0`), shuning uchun bu yerda qamrab olinmagan.

Qamrab olinmagan: munosabatlar, a'zolik o'zgarishlari, foydalanuvchi profillari, xabar yuborish, taklif orqali qo'shilish, proksi-serverlar, bildirishnomalar, Witness bot va bir nechta hisoblarni bir vaqtda boshqarish. Ochiq fayllarda faqat hisob-kitoblar mavjud.

## Parol bilan himoyalangan eksport libarchive yordamida ochildi · 2026-yil 29-oktabr

Eksport shifrlash kodi (WinZip AES-256, 7-Zip va WinRAR o'qiydigan format) bilan yaratilgan arxiv Windows `tar` (bsdtar 3.6.2, libarchive) yordamida ochildi. To'g'ri parol bilan chiqarilgan fayl original SHA-256 bilan mos keldi; noto'g'ri parol esa "Incorrect passphrase" xabari bilan rad etildi. 7-Zip va WinRAR o'zi ishga tushirilmadi.

## Telegram jonli sinovi · 2026 yil 27–29 oktyabr

Ichki API juftlik havzasi orqali tizimga kirgan bitta haqiqiy Telegram akkaunti **27 oktyabr 21:36 UTC**dan**29 oktyabr 05:15 UTC gacha** bo'lgan davrda bitta superguruhni yozib oldi. Ushbu davrda kollektor 12 marta ishga tushirildi.

| Yozib olindi | Hisob |
| --- | --- |
| Jurnal yozuvlari, jumladan yurak urishlari va xizmat yozuvlari | 2,385 |
| Yangi xabarlar | 1,291 |
| O'chirishlar | 472 |
| ularning matni TgWitness tomonidan saqlanganidan keyin o'chirildi | 347 |
| Tahrirlar | 12 |
| To'xtatilgan paytda o'tkazib yuborilgan xabarlar qayta tekshiruv orqali qo'shildi | 12 |
| Saqlangan ilovalar | 17 |
| Ilovalar yuklab olinmagan (yuklab olish o'chirilgan yoki yuklab olinadigan fayl yo'q) | 14 |
| Telegram FloodWait qayta tekshirishlar paytida har biri 3 soniyaga to'xtaydi | 8 |

- Jurnalning ommaviy kaliti bilan tekshirilganda, barcha 2 385 ta yozuvning imzolari va xesh zanjiri tasdiqlanadi.
- Qayta ishga tushirilgandan so'ng, yig'uvchi saqlangan yangilanish holatidan (`pts`) davom ettiradi va Telethon qoldirilgan xabarlarni to'ldiradi; keyingi qayta tekshiruv esa hanuzgacha yetishmayotgan xabarlarni qo'shadi.
- Har bir FloodWaitda kollektor so'ralgan vaqtni kutib, keyin davom ettirdi.
- Hisob imzolangan holda qoldi va 29 oktyabrda xuddi shu sessiya qayta ulandi.

Ushbu test quyidagilarni qamrab olmaydi: bir nechta akkauntni bir vaqtda ishlatish, administrator rollari, proksi-serverlar, bir necha soatdan ortiq davom etadigan uzilishlar va to'liq [jonli qabul qilish protsedurasi](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md). Ochiq fayllarda faqat quyidagi sanalar mavjud: hech qanday akkaunt yoki suhbat identifikatorlari, xabarlar yoki kirish ma'lumotlari yo'q.

## Sun'iy mahalliy quvvatni o'lchash

Komanda: `python tools/check_capacity.py --events 10000 --chats 100`

| Metric | Kuzatildi |
| --- | --- |
| Kirish | 100 ta sun'iy tanlangan manba bo'ylab 10 000 ta sintetik xabar hodisasi |
| Xabar matni | 400 belgilar; media yoki tarmoqsiz |
| Ma'lumotni qabul qilish | 53,273 soniya; soniyada 187,7 voqea |
| Qo'riqchi kechikishi | p50 4.162 ms; p95 7.784 ms; maksimal 129.118 ms |
| ZIP eksporti | tracemalloc yoqilganda 19.868 soniya |
| Python eksporti bo'yicha izlangan maksimal ajratmalar | 0.51 MiB; RSS jarayonini bajarilmaydi |
| ZIP hajmi | 4,610,962 bayt |
| Mustaqil tasdiqlash | Barcha 10 000 voqea tasdiqlandi |

Bu Windows mezbonidagi mahalliy ketma-ket yozib olish/eksport yo'lini o'lchaydi. U MTProto yetkazib berishni, bir vaqtda bir nechta hisoblarni, Telegramning cheklovlarini, media fayllarni, uzoq muddatli ish yukini yoki haqiqiy suhbatlarning kafolatlangan sonini o'lchamaydi. Ushbu o'lchov yakuniy oflayn vaqt tamg'alari vositalaridan oldin amalga oshirilgan bo'lib, u o'lchangan xabar yo'lini o'zgartirmaydi.

## Qolgan malaka

Saqlangan jonli jurnal haqiqiy yig'ish, tahrirlar, o'chirish bildirishnomalari, ilovalar, qayta tekshirishlar va tezlik chegaralashni boshqarishni qayd etadi. U to'liq yetkazib berilishni yoki rollarning ko'rinishi, reaksiya qiluvchi aktyorlar, uzoq muddatli FloodWait, hisob taqiqlanishi va tarmoq/jarayon uzilishidan tiklanish bo'yicha nazorat matritsasini aniqlamaydi. QR-token chiqarilishi yakunlangan mobil QR tasdig'idan alohida bo'lib qoladi.

Docker build/run, Linux/macOS o'rnatilishi, barqaror yuqori yuk, mustaqil xavfsizlik ko'rib chiqilishi, haqiqiy mustaqil TSA javobi, sertifikatni bekor qilish/arxivni tasdiqlash va sud-tibbiyot sertifikatlash yozib olingan malaka doirasidan tashqarida qoladi. Saqlangan MTProto holati va orqaga yetish amalga oshirilgan; atomik barqaror qayta ijro etish hali joriy etilmagan. Ma'muriy-log yig'ish, qo'shimcha reaktorlar ro'yxatlari va ustuvor qisqa so'rovlar alohida xususiyatlar bo'lib qoladi. Boshqariladigan malaka matritsasi uchun [jonli qabulni](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md) ko'ring.

Mahalliy batafsil kvitansiyalar va skrinshotlar test-results/ (Git tomonidan e'tiborsiz qoldirilgan) yo'lida joylashgan. docs/assets/ dagi ommaviy skrinshot faqat badiiy namoyish ma'lumotlarini o'z ichiga oladi.
