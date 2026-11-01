# Nima sinovdan o'tkazilgan

Canonical page: https://phishdestroy.github.io/TgWitness/uz/docs/reference/verification/

Jonli Telegram sinovi, avtomatlashtirilgan tekshiruvlar, brauzer tekshiruvlari va hali tasdiqlanmagan narsalar.

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

Quyidagi eski yozuvlar o'z ish jarayonlarini tasvirlaydi; ularning aksariyati sintetik test mijozlaridan foydalangan. Eng so'nggi avtomatlashtirilgan natijalar quyida keltirilgan.

## O'rnatilgan ommaviy MTProxy ro'yxatlari · 29 oktyabr 2026

Bu asl qo'lda tanlangan build-ning tarixiy test yozuvi. Joriy avtomatik pool va IP rejimlari uchun [ulanish sozlamalariga](https://phishdestroy.github.io/TgWitness/uz/docs/reference/connection/#ip-modes) qarang. Quyidagi hisob-kitoblar va qo'llab-quvvatlanmagan xususiyatlar shu sinovdan o'tkazilgan versiyaga tegishli.

Qo'shimcha ravishda SoliSpirit/mtproto va zakky8/mtproto-proxy-pro dan ochiq snapshot hamda aniq HTTPS yangilanishi kiritildi. Ushbu mezbanda ilova yuklovchisi 2026-yil 29-oktabr kuni soat 12:58 UTCda ikkala oqimni muvaffaqiyatli olgan: filtrlash, takrorlarni yo'qotish va har bir manba bo'yicha 64 yozuv chegarasi qo'llanilgach, **118 ta noyob mos keluvchi manzil** qolgan. Bu faqat ro'yxatni olishni tasdiqlaydi, ushbu proxy-lar orqali ulanish yoki xabar yetkazib berishni emas. Ushbu ish davomida hech qanday haqiqiy hisob ro'yxatga kiritilgan proxy-ga ulanmagan. [Operator va foydalanuvchi qo'llanmasi](https://github.com/phishdestroy/TgWitness/blob/main/docs/ru/PROXIES.md).

Muvaffaqiyatsiz/bo'sh/mos kelmaydigan manba javoblari avvalgi yozuvlar va sanalarni saqlab qoladi. Yangilanishlar tanlangan yo'nalishni o'zgartirmaydi. Jamoat manzillari tasdiqlanadi va tanlovda IP-lar mahkamlanadi; operator/qo'lda yo'nalishlar alohida qoladi. Ulashuv testi endi hisobga kirishdan oldin paneldagi mavjud. Soxta TLS ee va avtomatik proksi tanlovi qo'llab-quvvatlanmaydi. Operatorning katalogi obunalarni to'liq bekor qiladi.

- To'liq to'plam: **366 o'tdi, 3 o'tkazib yuborildi**, 287,94 soniya. Mavjud bog'liqlik ogohlantirishlari va platforma o'tkazib yuborishlari saqlanib qoladi. Oxirgi public-list/mahalliylashtirish regressiyasi: **36 o'tdi**, jumladan nohaq yuklab olish-proxy portlari rad etildi; bu to'liq to'plam bilan to'g'ri keladi.
- Brauzer mosligi ingliz/rus tillarida, yorug'/qorong'i rejimda 390/1440 pikselda o'tdi: biriktirilgan tanlovlar, sozlamalarni ochishda tashqi yuklab olish yo'q, aniq yangilash, nosozliklar paytida yo'llar va keş saqlanadi, oldindan kirish tekshiruvi, kechikgan javobli ish maydoni izolyatsiyasi, manba ma'lumotlari va tartib/kontrast. JavaScript xatolari yoki tashqi brauzer so'rovlari yo'q.
- Oxirgi statik tarjima qamrovi barcha 13 ta lokalizatsiya bo'yicha muvaffaqiyatli yakunlandi; yangi matn boshqa joylarda aniq inglizcha zaxira matn bilan birga rus tiliga tarjima qilindi. Yangilangan o'rnatilgan qo'llanma ikkala mavzu bo'yicha ham maket va kontrast tekshiruvlaridan muvaffaqiyatli o'tdi.
- Qarorq va nashriyot tekshiruvlari muvaffaqiyatli o'tdi (259 ta ommaviy fayl, 1 354 ta mahalliy havola); yangilandi Yozish va CI YAML fayllari tahlil qilindi. Docker va masofaviy CI bu yerda ishga tushirilmadi.
- Qayta qurilgan g'ildirak izolyatsiyalangan o'rnatish, paketlar ro'yxatini yuklash va imzolangan eksportni tekshirishdan o'tdi. Barcha 69 ta paket resursi ish maydoni bilan mos keldi; manba hashlar tekshirildi.

Cheklar: `test-results/public-proxy-research/download-receipt.json`, `test-results/public-proxy-research/copy-receipt.json`, `test-results/public-proxies-full-suite.log`, `test-results/public-proxies-final-focused.log`, `test-results/public-proxies-browser/receipt.json` va `test-results/public-proxies-package.log`. Brauzer/hisob/transport sozlamalari sun'iy; yuqoridagi ikkita feed yuklab olishlar esa haqiqiy HTTPS so'rovlari.

## Ixtiyobiy qo'shimchalar taqdimoti · 2026-yil 29-oktabr

Avvalgi Proof bot manzili endi **Extras** bo'limida: qisqa sharh va undan keyin tanlangan variant uchun alohida sozlash sahifasi. Witness formasida uch bosqich mavjud bo'lib, ulanishni boshqarish, tarmoq sozlamalari va joylashtirish tafsilotlari yashirilgan. GitHub aniq rejalashtirilgan va unga kirish uchun parol formasiga ega emas. [Rus tilidagi umumiy ko'rinish](https://github.com/phishdestroy/TgWitness/blob/main/docs/ru/EXTRAS.md).

- Mahalliylashtirish, guvoh sozlash va nashriyot tekshiruvlari uchun 30 ta maqsadli test muvaffaqiyatli o'tkazildi.
- Chromium sozlamalari qabul qilindi: ingliz va rus tillarida, yorug'lik/qorong'i rejimlarda, 390/1440 pikselda: klaviatura fokuslanishi va qaytish tugmasi, qo'shimchalarni tanlashda yashirin bog'lanishlar yo'qligi, loyiha saqlash, mahkamlangan konfiguratsiya/token yuklamalari, qulflanganda tokenlarni tozalash va mahalliy qo'llanma havolalarining ishlashi. Joylashuv va qattiq fonli matn kontrasti tekshiruvlari muvaffaqiyatli o'tdi.
- Ish maydoni almashtirishni qabul qilish o'tdi, shu jumladan almashtirishdan keyin kechikib keladigan token javobi. Tezkor navigatsiya bot, proof va GitHub shartlari orqali qo'shimchalarni topadi; mavjud 320/390/1440-piksel va ruscha/RTL tekshiruvlari ham o'tdi.
- Sozlash jarayonida JavaScript xatolari yoki brauzerdan tashqi so'rovlar qayd etilmadi. Bu sun'iy foydalanuvchi interfeysi tekshiruvlari bo'lib, yangi jonli Telegram yoki bot nashr dalillari emas.
- Oxirgi til yuklash va lug'at qamrovi barcha 13 ta lokalada muvaffaqiyatli yakunlandi, rus tilidan tashqari aniq inglizcha zaxira matnlar saqlab qolindi. Kengaytirilgan Proof qo'llanmasi ham har ikkala mavzuda 320/768/1440 piksel o'lchamlarda tartib/kontrast tekshiruvlaridan muvaffaqiyatli o'tdi.
- Qayta qurilgan g'ildirak izolyatsiyalangan o'rnatish va imzolangan eksportni tekshirishdan muvaffaqiyatli o'tdi. Barcha 67 ta paketlangan resurs ish maydoni bilan mos keldi; manba arxivida 253 ta ommaviy fayl mavjud. Manba/havola tekshiruvi 1 346 ta mahalliy hujjat havolalari bo'yicha muvaffaqiyatli o'tdi.

Cheklar: `test-results/setup-browser/receipt.json`, `test-results/quick-navigation/receipt.json`, `test-results/extras-final.json`, `test-results/extras-package.log` va `test-results/extras-artifacts.json`. Skrinshot aktivlari sun'iy ish maydonlaridan foydalanadi.

## Witness bot va proxy sozlamalarini audit qilish · 29 oktyabr 2026

Witness sozlamalari (hozirda **Extras → A bot in your channel**) mustaqil ravishda joylashtirilgan guvohni tayyorlaydi: pinlangan yig'uvchi kaliti, doiraviy token yuklab olish, o'z kanali, nashr siyosati, HTTP/SOCKS5 marshruti va maxsus Bot API. Bot tokeni guvoh hostida qoladi. Uning yangi `--check-config` tarmoq ulanishini ochmasdan yoki kalit yaratmasdan konfiguratsiya va fayllarni tasdiqlaydi. JSON fayl yo'llari konfiguratsiya yonida aniqlanadi. Barcha Compose guvoh variantlari endi HTTP proksi va Bot API sozlamalarini uzatadi.

Hisob sozlamalari operator boshqaradigan ommaviy MTProxy katalogini, Telegram proxy-ulovish havolalarining moslashtirilgan ko'rinishini va mavjud qo'lda to'ldiriladigan maydonlarni qo'llab-quvvatlaydi. Katalog javoblari maxfiy ma'lumotlarni o'z ichiga olmaydi; tanlov yo'nalishni ish maydoni xazinachasida saqlaydi. Katalog yetishmayotgan yoki noto'g'ri bo'lsa, qo'lda yo'nalishlar mavjud bo'lib qoladi. Loyiha proxy manzillari yoki joylashtirilgan guvoh xizmati avtomatik ravishda yaratilmaydi yoki yoqilmaydi. Tashqi guvoh panelini maxfiy saqlaydigan yig'uvchiga yetib borganda, Caddy misoli faqat belgilangan head endpointni ko'rsatadi.

Tasdiqlash:

- To'liq to'plam: **348 ta o'tkazildi, 3 ta o'tkazib yuborildi**, 195,81 soniya. Windows cheklovlari o'tkazib yuborilishlarga sabab bo'ladi; mavjud ikkita eski bog'liqlikni bekor qilish ogohlantirishlari saqlanib qoladi.
- Oxirgi guvoh/sozlama/chiqarish regressiya testi: **11 o'tdi, 1 o'tkazib yuborildi**. Bu to'liq test to'plamini qamrab oladi. Testlarga yo'l hal qilish, oflayn oldindan tekshirish, haqiqiy loopback HTTP Bot API moslamasi orqali imzolash/nashr qilish, yozib olingan yetkazib berish muvaffaqiyatsizligi, kanal-tokenni tasdiqlash va proxy-maxfiy ma'lumotni istisno qilish kiradi.
- Chromium sozlamalari 390/1440 pikselda (ingliz/rus tillarida) qabul qilindi: pinlangan konfiguratsiya va token yuklamalari, qulflanganda tokenlarni tozalash, katalog tanlovi, maxsus havola ko'rinishi, so'ngra aniq saqlash, tartib/kontrast va JavaScript xatolari yoki tashqi brauzer so'rovlari bo'lmasligi. Tor ruscha hisob-kitob sarlavhasi va kirish yorlig'ining ortiqcha chiqishini tuzatildi.
- Ruff, manba/havola tekshiruvlari va Compose/ish jarayoni YAML parse qilish muvaffaqiyatli o'tdi.
- Qayta qurilgan g'ildirak izolyatsiyalangan o'rnatish, panel/statik resurs va API-avtorizatsiya tekshiruvlaridan, shuningdek, to'g'ridan-to'g'ri va oqim orqali uzatilgan 32-hodisali sintetik eksportlarning mustaqil tasdiqidan o'tdi.

Cheklar: `test-results/setup-full-suite.log`, `setup-final-focused.log`, `setup-browser/receipt.json`, `setup-browser-final.log` va `setup-package.log`. Ushbu tekshiruvlar sun'iy akkauntlar/proxy-lar va mahalliy Bot API moslamasidan foydalanadi. Ular haqiqiy bot nashrini, ishlayotgan ommaviy MTProxy serverini, masofaviy CI ijrosini yoki Docker joylashtirishini da'vo qilmaydi. Yuqoridagi saqlangan haqiqiy Telegram kuzatuv tarixi alohida dalil bo'lib qoladi. [Sozlash bo'yicha ko'rsatmalar](https://github.com/phishdestroy/TgWitness/blob/main/docs/ru/WITNESS.md).

## Taqdimot va hujjatlarni ko'rib chiqish · 2026-yil 29-oktabr

Mahsulot sahifasi, kirish ekrani, Inglizcha/Ruscha README hujjatlari va taqdimot tasvirlari endi bitta vizual uslubga ega. Ochiq skrinshotlarda badiiy demo ma'lumotlari ishlatiladi. Sharh shuningdek yuqoridagi eskirgan jonli-validatsiya va tiklash tavsiflarini ham tuzatdi.

- Mahalliylashtirishga yo'naltirilgan sayt va nashr sinovlari: **33 ta o'tdi, 1 ta o'tkazib yuborildi**. O'tkazib yuborilgan sinov ushbu mezbanda mavjud bo'lmagan simvolik havola (symlink) yaratishni talab qiladi.
- Umumiy Chromium paneli qabul qilindi, jumladan barcha til kataloglari, RTL tartibi, yorug'/qorong'i mavzular, matnning yuqori kontrasti va ish maydoni almashtirish. Profil yaratish tekshiruvi endi tanlangan ish maydonini tekshirishdan oldin uning haqiqiy HTTP javobini kutadi.
- Inglizcha/ruscha kirish ekranlari har ikkala mavzuda 320, 390, 768, 850 va 1440 pikselda joylashuv va kontrast tekshiruvlaridan o'tdi; yuborish tugmasi dastlabki ko'rinish oynasida qoladi.
- Jamoat saytida qabul qilish 320, 390, 768, 1024 va 1440 pikselda, xabarni ham o'z ichiga olgan holda o'tkazildi tarix nazoratlari, skrinshotni kattalashtirish/Escape/diqqatni qaytarish, klaviatura yorliqlari, clipboard rad etish, loyiha ostki yo'llari, harakatni kamaytirish va JavaScript bo'lmagan zaxira rejimi. Hech qanday muvaffaqiyatsiz aktiv so'rovlari, tashqi so'rovlar yoki JavaScript xatolari kuzatilmadi.
- Qayta qurilgan g'ildirak izolyatsiyalangan o'rnatish tekshiruvidan muvaffaqiyatli o'tdi: panel resurslari va lokal fayllar yuklanishi, APIga kirish uchun autentifikatsiya talab qilinishi hamda to'g'ridan-to'g'ri/oqimli eksportlar mustaqil ravishda barcha 32 ta sintetik voqeani tasdiqladi. Ruff va public-source/link tekshiruvlari ham muvaffaqiyatli o'tdi.

Mahalliy kvitansiyalar: `test-results/design-tests.log`, `design-panel-final.log`, `design-review-final.log`, `design-site.log` va `design-package/install-receipt.json`. Ushbu taqdimot/hujjatlardagi o'zgarish uchun to'liq orqa ofis to'plami qayta ishga tushirilmagan; uning avvalgi natijasi nashrdan oldingi auditda saqlanib qoladi.

## 0.6.1-versiya

0.6.1 versiyasi panel taqdimotini, ishga tushiruvchi vositalarni, paketlash va hujjatlashtirishni o'zgartiradi; yig'ish, saqlash, imzolash va eksport kodlari o'zgarmagan. Windows 11 / Python 3.12.10 da tegishli ijro muhiti biriktirilgan holda:

- To'liq to'plam **137 ta testdan** o'tdi, 2**tasini o'tkazib yubordi** va mavjud Starlette ogohlantirishi bilan. Yangi testlar ishga tushiruvchining Ctrl+C bosishini (server tartibli to'xtash uchun 30 soniya vaqt oladi) va sozlash bosqichidagi bartaraf etilishi mumkin bo'lgan xatoliklarni qamrab oladi.
- Chromium (headless shell 156) barcha **45 ta umumiy ssenariy** va **35 hisob-import/QR/Auth kalit ssenariylarini**, jumladan matn kontrasti tekshiruvi, 320–1440 px oralig'ida gorizontal to'lib-toshmaganligi va 320/390 px'da birinchi kirish maydonlarining ko'rinishini muvaffaqiyatli o'tkazdi. Sahifada JavaScript xatolari yoki tashqi so'rovlar qayd etilmadi.
- `python start.py --setup-only` paketni 0.6.1 versiyasiga qayta o'rnatdi va `python start.py --check` tayyorligini xabar qildi. Haqiqiy `python -m tgwitness --demo` serveri panel, uslub varaqasi, skript, logo, qo'llanma va `/api/status` 0.6.1 versiyasini qaytarib berdi; o'chirib tashlangan `workspace.css` esa 404 kodini qaytarib berdi.
- `Start.cmd` PATH tashqarisida Python o'rnatilganini aniqladi. Python mavjud bo'lmaganda u o'rnatish taklifini ko'rsatdi; bosqichma-bosqich bosma qo'llanma ko'rsatmalarini rad etib, 1 chiqib ketdi. python.org dan yuklab olish bosqichi 3.12.10 installyerini olib, Python Software Foundation Authenticode tekshiruvidan o'tdi; installyer o'zi ushbu hostda ishga tushirilmadi.
- `start.sh`, Python'siz o'rnatish bo'yicha ko'rsatmani chop etdi va chiqdi 1. `scripts\Docker.cmd` va `scripts/docker-start.sh` soxta `docker` ijro etiladigan fayllariga nisbatan sinovdan o'tkazildi: chaqiruv ketma-ketligi, panel manzili va token chiqishi to'g'ri bo'ldi, xato bo'lgandan keyin esa muvaffaqiyat xabari chiqmadi.
- `python tools/build_portable.py` Windows uchun 18,8 MiB hajmli paketni embeddable-runtime tekshiruv summasini tasdiqlaganidan so'ng yaratdi. Faqat bo'shliqli yo'lga chiqarilgan va PATHda faqat `C:\Windows` papkalarini o'rnatgan holda ishga tushirilganda, uning ichidagi Python `TgWitness-Check.cmd` ni o'tkazdi, demo (32 ta voqea) va jonli ish maydonini taqdim etdi, va Chromium jurnal va tafsilotlar oynasini JavaScript xatolarisiz render qildi. Ma'lumotlar paketning `data` papkasiga yozildi.
- `python tools/build_preview.py` 110 ta fayldan iborat manba arxivini yaratdi. `git add` ning quruq sinovi sessiya, kalit, ma'lumotlar bazasi, token, log yoki eksport fayllarisiz, mahalliy mutlaq yo'llarsiz va sir shaklida bo'lgan satrlarsiz shu 110 ta faylni ro'yxatlab chiqdi.

Ushbu 27 oktyabrdagi paketlash urinishida bajarilmagan: avtomatik Python o'rnatilishi, Docker build/Compose tekshiruvlari, Linux/macOS ishga tushirishlari yoki yangi jonli-akunt mashqi. Haqiqiy Telegram dalillari yuqorida va quyidagi oldingi akunt tekshiruvlarida qayd etilgan. CI ta'riflari o'z-o'zidan platforma ijrosini tasdiqlamaydi.

## 0.6.0-versiya

Windows 11 / Python 3.12.10 uchun so'nggi to'liq pinlangan ijro muhitlari to'plami 135 ta testdan o'tdi, 1 tasi o'tkazib yuborildi va buning uchun 26,53 soniya vaqt ketdi, mavjud Starlette ogohlantirishi bilan. O'tkazish POSIX ruxsatnomalarini talab qiladi. QR rendererini tayyorgarlik tekshiruvlari va jarayon o'lchovlariga qo'shgandan so'ng, 8 ta ta'sirlangan tayyorgarlik/ish maydoni tekshiruvlari ham muvaffaqiyatli bo'ldi.

Yangi qamrovga Telethon sxemalari 7/8, Pyrogram sxemalari 2/3, to'liq JSON kiradi kalitlar va faqat metama'lumotli JSON, mos keluvchi/qarama-qarshi hisob fayllari, TData parollari, cheksumni o'zgartirish va xavfsiz bo'lmagan yo'llar, oflayn/avtorizatsiyalangan xotira ichidagi konvertatsiya, onlayn hisob-ID tekshiruvlari, QR muvaffaqiyati/2FA/muddati tugashi, eskirgan bekor qilish va hisob izolyatsiyasi. TData fixtures shifrlash uchun alohida AES-IGE implementatsiyasidan foydalanadi.

Chromium **45 ta umumiy ssenariy** va **35 ta hisob-import/QR/Avtorizatsiya kaliti ssenariylarini** muvaffaqiyatli o'tkazdi, hech qanday sahifa JavaScript xatolari yoki tashqi so'rovlar qayd etilmadi. Yangi brauzer tekshiruvlari barcha to'rtta kirish formatini birgalikda, himoyalangan TData, API metadata, QR tasvirlash, muddat tugashi/qayta urinish, 2FA, noto'g'ri hisobni rad etish, qulflash/ish maydoni bekor qilish, moslashuvchan maket va yangi fayl tanlangandan keyin kech konversiya javoblarini qamrab oladi.

Hisob ma'lumotlarini kiritish bo'yicha o'zgarishlardan so'ng ikkala brauzer ham yana muvaffaqiyatli ishga tushdi. Jonli sozlash hisob formasini ochadi; demo rejim esa o'z namunaviy jurnalini ochadi. Demo hisob sahifasi jonli ishga tushirish bo'yicha ko'rsatmalarni ko'rsatadi va kirish ma'lumotlarini yashiradi. 320, 390 va 1440 pikselda o'tkazilgan diqqatli tekshiruvlar raqam maydoni va asosiy tugma aylantirmasdan sig'ishini, API maydonchalari dastlab yopiq bo'lishini va matn kontrasti o'qilishi mumkinligini tasdiqladi. Yozib olish va tekshirish boshqaruvlari ularning yangi kengaytiriladigan bo'limlari ochilgandan keyin ham yopiq bo'lib qoladi.

To'g'ridan-to'g'ri Auth Key oqimi sintetik ma'lumotlar yordamida haqiqiy import va ruxsat berish endpointlari orqali sinovdan o'tkazildi. Tekshiruvlar to'liq bo'lmagan kalitlar, DC yo'qligi, noaniq foydalanuvchi identifikatorlari, hisob identifikatori nomuvofiqligi, saqlangan API ma'lumotlari, so'rovning ko'rinadigan bajarilish jarayoni, maxfiy tozalash hamda tahrirlar yoki usul o'zgarishlaridan keyingi kechikgan javoblarni o'z ichiga oladi. Kirishning to'rtta usuli 320, 390 va 1440 pikselda tekshirildi. Fayl tanlovchisi format bo'yicha ko'rsatmalardan oldin joylashgan va Ulanish tugmasi dastlabki 844 pikselli oynaga API sozlamalari siqib qo'yilganda sig'adi. Ushbu UI qabul qilish sinovida haqiqiy Auth Key avtorizatsiyasi amalga oshirilmadi.

Paneli yangilash ikkala brauzer to'plami bilan yana tekshirildi: sahifada JavaScript xatolari yoki tashqi so'rovlar aniqlanmadi. Hisob ma'lumotlari to'plami endi bitta API ID/hash juftligini joylashtirishni, maydonlarni almashtirmasdan noto'g'ri yoki bir nechta juftliklarni rad etishni, faqat metadata bo'yicha ko'rsatmalar berishni va kirish usuli o'zgartirilgandan yoki foydalanuvchi ma'lumotlari qo'lda tahrirlangandan so'ng eskirgan import javoblarini e'tiborsiz qoldirishni o'z ichiga oladi. Sozlash bo'yicha qo'llanma, aniq boshlash/tanaffus, bo'sh qidiruvdan tiklash, hamda yakuniy ulanish/mahalliy-qo'llanma tartibi va matnning yuqori kontrasti bo'yicha oltita qo'shimcha diqqat bilan tekshiruv 320, 390 va 1440 pikselda muvaffaqiyatli o'tkazildi. To'g'ridan-to'g'ri kirish yangilanishi bitta telefon/kod-so'rov operatsiyasini qo'shadi va telefon, QR hamda sessiya kirish uchun joriy ish maydonining saqlangan API juftligidan qayta foydalanadi. Yuqoridagi to'liq Python to'plami yangi saqlash, qisman parolni rad etish va ish maydonini izolyatsiya qilish testlarini o'z ichiga oladi. Brauzer tekshiruvlari to'g'ridan-to'g'ri telefon kiritishni, saqlangan parolni qayta ishlatishni, faqat metadata bo'yicha yo'naltirishni, bitta tugma bilan faylga ruxsat berishni va takroriy hisoblarni rad etishni qamrab oladi. Yengillashtirilgan panel-token va telefon shakllari ham 320, 390 va 1440 pikselda dastlabki aylantirishsiz tekshirildi. Moslik tekshiruvi to'g'ridan-to'g'ri telefon shakli eski konfiguratsiya/kod endpointlaridan foydalanishi mumkinligini, eski jarayon hali ham ishlayotgan paytda ham tasdiqladi.

Foydalanuvchi taqdim etgan bitta hisob alohida, ommaviy test sharoitlaridan tashqarida tekshirildi. Uning Telethon, Pyrogram va TData kirishlari bir xil ruxsatga mos keldi; hamroh JSON API ma'lumotlarini taqdim etdi. Barcha to'rtta fayl 0.6.0 paneli orqali yuklandi va Telegram kutilgan sonli hisob IDni tasdiqladi. Manba fayllari o'zgarmagan holda qoldi. Hech qanday manba tanlanmagan va kuzatuv o'chirilgan holda qoldirilgan. Bu jonli yig'ish, tiklash yoki quvvatni emas, balki import/kirish bo'yicha bitta misolni tashkil etadi.

Telegram shuningdek haqiqiy QR tokenini ham chiqardi, u skanerlashsiz bekor qilindi. To'liq QR tasdiqlash va 2FA jarayonlari sintetik mijozlar bilan sinab ko'rildi; haqiqiy Telegram ilovasi orqali mobil tasdiq alohida qabul qilish bosqichi bo'lib qoladi. Ommaviy fayllarga haqiqiy akkaunt identifikatorlari, sirlar yoki skrinshotlar kiritilmagan.

Ishga tushiruvchi yangilanishi yakunlandi; manba, o'rnatilgan metadata va tayyorlik belgisi 0.6.0 versiyasini, qrcode 8.2 va o'tkazilgan `pip check` ni xabar qiladi. O'rnatilgan g'ildirak panel va qo'llanmaga xizmat qildi, tasdiqlanmagan API so'rovlarini rad etdi va mustaqil ravishda to'g'ridan-to'g'ri hamda jonli uzatilgan 32-hodisali sintetik eksportlarni tekshirdi. Yangilangan oflayn qo'llanma 320, 390 va 1440 pikselda tekshirildi. Ommaviy skrinshotlar sun'iy bo'lib qolmoqda.

Manba kodining chiqarilishi 107 ta ruxsat berilgan faylni o'z ichiga oladi. Mahalliy hujjat havolalari to'g'ri ishlaydi. Docker/Caddy ijrosi, masofaviy CI/paket nashri, ARM64 ijro muhiti, uzluksiz yig'ish va to'liq jonli Telegram qabul qilish matritsasi bu yerda aniq belgilab o'tilmagan.

## 0.5.1-versiya

Windows 11 / Python 3.12.10 da to'liq loyiha muhit to'plami 31,21 soniyada **94 ta o'tkazildi, 2 ta o'tkazib yuborildi** va mavjud Starlette ogohlantirishi bilan yakunlandi. O'tkazib yuborilganlar POSIX ruxsatnomalari va simvolik havolalar (symlink) yaratishni talab qiladi, bu mezbanda mavjud emas. HTTP yuklab olish fiksturasi so'rov-thread diagnostikani chop etdi; barcha da'volar o'tdi. Ushbu ish mezban transport muammolarining yo'qligini aniqlamaydi.

Yangi regressiya qamrov mashqlari StringSession, kod va 2FA hisob ma'lumotlaridagi o'zgarishlarni, bekor qilingan identifikator qidiruvini, kutilayotgan kirishni bekor qilishni hamda faol, rad etilgan, yangilangan va probe mijozlardagi ro'yxatdan o'tgan handlerlar orqali yangilanishlarni inkor etdi. Faqat faol yig'uvchi voqealarni taqdim etadi; saqlangan ma'lumotlar va imzolangan tarix o'z holicha saqlanadi. Boshqa yangi tekshiruvlar ma'lumotlar bazasini qayta ochgandan keyin Unicode qidiruvini, Coverage'ga monitoring-siyosati chegaralarini kiritishni va ochiq manba paketlashdan istisno qilishlarni qamrab oladi.

`pythonw.exe` loyihasi izolyatsiyalangan sintetik panelni ishga tushirdi, HTTP 200 javobini qaytardi va `logs/server.log` da ishga tushirish diagnostikalarini saqlab qoldi. Logda yaratilgan panel tokeni yoki HTTP kirish yozuvlari mavjud emas edi. Test faqat o'zining sintetik jarayonini yakunladi. Hech qanday Task Scheduler vazifasi ro'yxatdan o'tmagan; tizimga kirish/chiqish, uxlab turish va xizmatni tiklash alohida holatlar bo'lib qoladi.

Chromium ma'qullash jarayoni **45 ssenariyni** muvaffaqiyatli yakunladi, hech qanday sahifa JavaScript xatolari aniqlanmadi va hech qanday tashqi so'rovlar kuzatilmadi. Yangi tekshiruvlar 601/768/850 pikselli timeline sanalari va vaqtlarini, status yangilanishi davomida ilova loyihalarini, saqlash paytida qilingan yangi tahrirlarni, hisobni almashtirganda tozalangan tasdiqlash natijalarini, boshqa ilovaga o'tib qaytgandan keyingi kechikgan tasdiqlash javoblarini hamda yangi voqealar kelganda aniq tasdiqlash chegaralarini qamrab oladi. Qidiruv ikonkasi va matn oralig'i ham tuzatildi hamda brauzer to'plami qayta ishga tushirildi.

Brauzerni ishga tushirishda `.venv`dagi belgilangan ijro muhiti va mavjud tizim tomonidan taqdim etilgan Playwright 1.62.0/Chromium import yo'lidagi loyiha muhitidan keyin qo'shimcha o'rnatildi. Majburiy bo'lmagan rivojlantirishga oid bog'liqlikni o'rnatish sekin Playwright yuklanishi paytida to'xtatildi; yangi brauzer-asbob versiyasi tasdiqlanmadi. Oddiy `python start.py --setup-only` ilova yangilanishini yakunladi. Manba, o'rnatilgan metama'lumotlar va ishga tushiruvchining marker hisobot 0.5.1; `pip check` o'tdi. Tayyorlik tekshiruvlari toza, ishlatilmagan yo'lda o'tdi, kutilgan mahalliy-seif-kalit ogohlantirishini saqlab qoldi.

0.5.1 g'ildiragi alohida o'rnatilib, smoke-testdan o'tkazildi: barcha panel/qo'llanma aktivlari yetkazib berildi, autentifikatsiyasiz API-ga kirish rad etildi va to'g'ridan-to'g'ri hamda oqim asosidagi 32-hodisali dalil ZIP-fayllari mustaqil tekshiruvdan muvaffaqiyatli o'tdi. O'rnatilgan paketdagi ilova fayllari manba kodi bilan solishtirildi. Ochiq manba arxivi aniq fayl turlari ro'yxatini (allowlist) ishlatadi va bog'langan manba fayllarni rad etadi; ijro vaqti materiallari manba papkalariga joylashtirilganda regressiya testlari tomonidan chiqarib tashlanadi.

Kodni tuzatish jarayonida ochiq manba tanlovi va Git nomzodlar to'plami 86 ta faylni o'z ichiga olgan, ijro etish vaqti ma'lumotlari kataloglari kiritilmagan. Tan olinadigan xususiy kalit, GitHub tokeni, Telegram bot-tokeni va StringSession naqshlari bo'yicha tekshiruv hech qanday moslik topmadi. Bu cheklangan naqsh tekshiruvi bo'lib, to'liq maxfiylik auditi emas. Ignore-rule tekshiruvlari o'n ikkita keng tarqalgan akkaunt/ma'lumot/eksport artefaktlarini qamrab oladi. Workflow/issue/Compose YAML va Windows vazifa skripti muvaffaqiyatli tahlil qilindi. Mahalliy hujjat havolalari to'g'ri ishga tushdi.

27 oktabrdagi ko'rib chiqishning barcha yetti xulosasi ko'rib chiqildi. GitHub ish jarayonini ijro etish, Linux/macOS/Docker ijro muhiti, haqiqiy Telegram, tashqi proxy/TSA o'zaro moslik va uzluksiz yuklamaga bardosh berish sinovi ushbu mahalliy ish jarayonidan tashqarida qoladi. Hech qanday ombor nashri, xizmatni ro'yxatdan o'tkazish yoki haqiqiy hisoblarni to'plash amalga oshirilmagan.

### Ingliz tilidagi hujjat yangilandi

README hujjati, hisob/sessiya ma'lumotnomasi, yig'ish ish jarayoni va biriktirilgan qo'llanma endi qo'llab-quvvatlanadigan kirishlar, ish maydoni xatti-harakatlari, voqea siyosatlari va eksport formatlarini ingliz tilida tasvirlaydi. Uchta ommaviy skrinshot sintetik ma'lumotlar yordamida yangilandi. O'sha paytda ochiq manba tanlovi, ikkita yangi qo'llanma hamda boshqa 88 ta fayldan iborat edi. 23 ta Markdown hujjat bo'ylab joylashgan barcha 131 ta mahalliy havola to'g'ri ochiladi.

Interfeys va qo'llanma tahrirlari kiritilgach, Chromium qabul qiluvchanligi yana barcha 45 stsenariyni muvaffaqiyatli o'tkazdi, hech qanday sahifa JavaScript xatosi yoki tashqi so'rovlar qayd etilmadi. Ushbu hujjat va taqdimot yangilanishi uchun to'liq Python to'plami qayta ishga tushirilmadi; yuqoridagi 94 o'tkazilgan natija oldingi kodni tuzatish yurishi natijasiga tegishli.

Qayta qurilgan g'ildirak yangi izolyatsiyalangan maqsadga o'rnatildi. Uning paneli va yo'riqnoma aktivlari muvaffaqiyatli xizmat qildi, autentifikatsiyalanmagan API-ga kirish rad etildi va to'g'ridan-to'g'ri hamda oqimli eksportlar 32 ta sintetik hodisa bo'yicha mustaqil tekshiruvdan o'tdi.

### O'rnatish va ishga tushirish bo'yicha yangilanish

Diqqatga sazovor o'rnatgich, paketlash va tayyorgarlik tekshiruvlari **14 ta testdan** muvaffaqiyatli o'tdi, mavjud bo'lmagan simlink yaratishni o'tkazib yuborish bilan. Mahalliy o'ram tekshiruvlari bo'shliqli yo'llar, argument uzatish, setup/demo rejimlari va nolga teng bo'lmagan chiqish natijasini tarqatishni qamrab oladi. Git Bash tekshiruvlari Docker shell yordamchisini simulyatsiya qilingan daemon bilan ishga tushiradi, jumladan Docker yo'qligi, Compose yo'qligi, sog'liqni tekshirish kutishining muvaffaqiyatsizligi va muqobil port orqali muvaffaqiyatli ishga tushirish. Ushbu simulyatsiya qilingan tekshiruvlar Docker ijro muhitining mosligini aniqlamaydi.

To'liq ochiq manbali nusxa bo'shliqlarga ega bo'lgan yangi Windows papkasiga o'rnatildi. `scripts\Setup.cmd` yangi muhit yaratdi va belgilangan ijro muhitini o'rnatdi; `Start.cmd --check --json` maqsadli ma'lumotlar papkasini yaratmasdan tayyorligini xabar qildi. `pip check` muvaffaqiyatli o'tdi. Qayta tuzilgan g'ildirak ham o'rnatilgan paket tekshiruvidan, jumladan to'g'ridan-to'g'ri va oqimli 32-hodisali eksportlarni ham o'z ichiga olgan holda muvaffaqiyatli o'tdi.

Shell sintaksisi va beshta ish jarayoni/Compose YAML fayllari tahlil qilindi. Manba va image Compose konfiguratsiyalari saqlash va ijro etish vaqtidagi sozlamalar bo'yicha kelishib olindi. Shu bosqichda 23 ta Markdown hujjat bo'ylab jami 139 ta mahalliy havola hal qilindi. Ochiq manba tanlovi 99 ta fayldan iborat.

CI ta'riflari endi Windows/Linux/macOSda yangi mahalliy sozlamalarni, konteyner qayta yaratilganda Compose holati/kirish nazorati/barqarorlikni va Caddy konfiguratsiyasini qo'llaydi. Reliz jarayoni ushbu tekshiruvlarga asoslangan holda nashr etishni boshqaradi va emulyatsiya qilingan ARM64 smoke-checkni qo'shadi. Docker ushbu mezbanda mavjud emas: haqiqiy Compose/Caddy ijrosi, sertifikat berish, ARM64 ijrosi va masofaviy ish jarayoni/paket nashriyoti mahalliy darajada hali to'liq qo'llab-quvvatlanmaydi. Ilova/UI kodi ushbu yangilanish bilan o'zgarmadi; oldingi to'liq Python va brauzer natijalari qayta ishga tushirilmagan.

## 0.5.0-versiya

To'liq pinlangan ijro muhitlari to'plami o'tdi: **81 o'tdi, 1 o'tkazib yuborildi**, 22,00 soniyada, mavjud Starlette ogohlantirishi bilan. Windowsda POSIX ruxsatnomalarini tekshirish o'tkazib yuboriladi. Yangi handler xabarlar, tahrirlar, doirali/doirasiz o'chirishlar, munosabatlar, ishtirokchilarni yangilash va a'zolik xizmat xabarlarini turli siyosatlar orqali yuboradi. O'chirib qo'yilgan kategoriyalar mos keladigan jonli kuzatuvlarni hosil qilmaydi; qamrov diagnostikasi va aniq snapshotlar mavjud bo'lib qoladi. Testlar saqlangan siyosatni, ish maydoni ajratilishini, imzolangan oldingi/keyingi audit yozuvlarini, o'zgarmagan siyosat xatti-harakatlarini, qat'iy tasdiqlashni va keyingi jarayon kvitansiyasiga kiritilishni tekshiradi.

Demo kirish testlari uning imkoniyatlari sozlangan panel tokenidan farq qilishini, jonli ish maydonini avtorizatsiya qila olmasligini, yig'ish sozlamalarini o'zgartira olmasligini va u masofaviy, yo'naltirilgan, turli kelib chiqishli yoki nomaqbul-Host so'rovlari uchun berilmaydi yoki qabul qilinmaydi. Saqlangan demo-ni aniq demo bayrog'isiz ochish avtomatik kirishni yoqmaydi.

Chromium qabul qiluvchanligi **39 ta ssenariyni** muvaffaqiyatli bajardi, jumladan token kiritilmasdan mahalliy demo kirish, monitoring oldindan sozlamalari, manba tanlashdan siyosatga o'tish, har bir hisob mustaqilligi hamda stol/320/390-pikselli tartib va matn kontrasti tekshiruvlari. Sahifadagi JavaScript xatolari aniqlanmadi. Mezbonning AdGuard orqali kiritilgan so'rovlari kvitansiyada saqlanib qoladi. Yuklab olish HTTP fiksturasi mijoz ulanishni yopgandan so'ng ulanishni qayta tiklashni qayd etdi; assertsiyalar hanuzgacha o'tdi. Bu jonli xizmat natijasi emas.

Oddiy ishga tushiruvchi izolyatsiyalangan muhitni 0.5.0 ga yangiladi; manba va o'rnatilgan versiyalar mos keldi va pip tekshiruvi muvaffaqiyatli o'tdi. Mavjud maxfiy ombor shifrlash, noto'g'ri/yetishmayotgan kalit rad etish hamda imzo/media manipulyatsiya tekshiruvlari to'liq to'plamda muvaffaqiyatli o'tdi. Xabar mazmuni yoki ilovalar uchun yangi ilova shifrlash da'vo qilinmaydi.

Yangilangan foydalanuvchi interfeysini mavjud qilish uchun mahalliy demo qayta ishga tushiriladi. Mavjud sun'iy yozuvlar saqlanadi; eski fon demo jarayonini to'xtatish keyingi ishga tushirishda oflayn chegarani yaratadi. Ushbu tekshiruvlar uchun haqiqiy Telegram sessiyasi ishlatilmaydi.

Mahalliy host:8787 panelida versiya 0.5.0, avtomatik demo kirish, beshta monitoring boshqaruvi va 33 ta saqlangan sintetik jurnal hodisalari ko'rsatildi. Alohida o'rnatilgan 0.5.0 g'ildiragi barcha panel/qo'llanma aktivlarini taqdim etdi, autentifikatsiyalanmagan API-ga kirishni rad etdi va tekshirilgan 32-hodisali ZIP-faylni bevosita hamda oqimli yuklab olish yordamchisi orqali yaratdi. Ijro etish paketlari versiyalari 0.4 uchun qayd etilganidek bloklangan holda qoladi.

## Versiya 0.4.0

To'liq pinlangan ijro muhitlari to'plami 19,77 soniyada **78 tasi o'tkazildi, 1 tasi o'tkazilmay qoldi**. O'tkazilmay qolgan tekshiruv POSIX ruxsatnomalarini talab qiladi; upstream Starlette TestClient eskirish ogohlantirishi saqlanib qoladi. Yangi testlar oqimli yuklab olish/ish maydoni marshrutlash, avtorizatsiya sarlavhalari, ustiga yozishni rad etish, yo'naltirishlar, qisqartirilgan javoblar, e'lon qilingan/haqiqiy o'lcham cheklovlari, chegaralangan o'qishlar, tozalash, qattiq havolalarsiz fayl tizimlari, tayyorlikdagi xatolar va paketlarni o'rnatmasligi kerak bo'lgan ishga tushirish rejimlarini qamrab oladi. Eksport testlari ish maydoni ichidagi mahalliy vaqtinchalik fayllar va tanlab olingan yetim fayllarni tozalashni tasdiqlaydi.

Chromium qabul qilish jarayoni barcha 36 ta ro'yxatga olingan ssenariyni sahifadagi JavaScript xatolarisiz muvaffaqiyatli yakunladi. U mock phone/code/2FA kirishni, sessiyalarni konvertatsiya qilishni, ikki ish maydonini va alohida yo'nalishlar/holatlarni, kuzatuvlarni, imzo va tekshiruv nuqtalarini hamda vaqt tamg'asi so'rovlarini sinovdan o'tkazadi, shuningdek:

- Stol usti va 320/390-pikselli maketlar, gorizontal ortiqcha joyga chiqmaslik, ko'rinadigan navigatsiya, va dastlabki 844-pikselli ko'rinish oynasida birinchi kirish maydoni.
- WCAG AA matn chegaralarida mustahkam orqa fonli matn kontrasti. Nofaol boshqaruv elementlari, opastlik va rasm/gradient orqa fonlar kiritilmagan; bu to'liq WCAG auditi emas.
- Haqiqiy mahalliy eksport javobi soxta OS fayl tanlovchi/yoziladigan modul orqali yozilgan, so'ng mustaqil ZIP tekshiruvi; bekor qilish eksport so'rovini yubormaydi.
- Yozish mumkin bo'lgan xato manzilni bekor qiladi; 128 MiB zaxira haddan tashqari katta e'lon qilingan javobni mos yuklamani ajratmasdan rad etadi.
- Ingliz tilidagi mahalliy qo'llanma ish stoli hamda ikkala tor kenglikda.

Operatsion tizim saqlash dialogi va haqiqiy ko'p gigabaytli brauzer yozuvlari avtomatlashtirilmagan yoki tasdiqlanmagan. Python yuklab olish testlari chegaralangan bo'laklar va loopback moslamalaridan foydalanadi. Haqiqiy Telegram bilan to'liq joriy etishni qabul qilish alohida qoladi.

Oddiy o'rnatuvchi `.venv`ni 0.4.0 ga yangiladi. Manba va o'rnatilgan metadata mos keladi; `pip check` muvaffaqiyatli o'tdi. `python start.py --check --json` yangi sintetik yo'lda ma'lumotlar katalogini yaratmasdan tayyorligini xabar qildi. Uning mahalliy kalit saqlash bo'yicha ogohlantirishi to'g'ri qoladi: jurnallar/media ilova tomonidan shifrlanmaydi.

0.4.0 g'ildiragi yaratilib, alohida papkaga o'rnatildi. Barcha 23 ta ilova fayllari manba bilan baytma-bayt mos keladi. O'rnatilgan paket panel va inglizcha qo'llanma/resurslarni taqdim etdi, tasdiqlanmagan API-ga kirishni rad etdi va tekshiruvdan o'tgan sintetik 32-hodisali ZIP-faylni eksport qildi. Uning jonli yuklab olish buyrug'i shuningdek, ishlayotgan o'rnatilgan ilovadan mustaqil ravishda tekshirilgan ZIP-faylni ham olib keldi.

Ochiq hujjatlar va mahalliy qo'llanma ingliz tilida; mahalliy hujjat havolalari ishga tushadi. PowerShell Windows vazifa shablonini, Python esa macOS plist faylini tahlil qildi. Bular sintaksis tekshiruvlari bo'lib, xizmatni ishga tushirish emas. Hech qanday vazifa/xizmat ro'yxatga olinmadi. CI konfiguratsiyasiga hozir tayyorgarlik tekshiruvlari kiritilgan, ammo masofaviy CI bu yerda ishga tushmagan.

0.4 brauzer rejimidagi ish jarayonida yana host AdGuard in'ektsiyasini va Windows asyncio socket-tozalash OSError 10022 xatosini qayd etdi. Brauzer da'volari o'tdi; bu muhit kuzatuvlari qat'iy ilova xatti-harakatlari sifatida emas, balki saqlab qolinadi. Dastlabki OpenSSL/brauzer/pip sandbox urinishlari muvaffaqiyatsiz tugadi; muvaffaqiyatli sinov yurishlari esa sandbox tashqarisida tasdiqlangan ijroni qo'lladi.

## 0.3.1-versiya tayyorgarlik bo'yicha tuzatishlarga qaratilgan

Ta'sirlangan launcher, dalillar/saqlash va API tekshiruvlari muvaffaqiyatli o'tdi: **31 tasi o'tdi, 1 tasi o'tkazib yuborildi**, upstream Starlette bo'yicha bitta ogohlantirish. O'tkazib yuborilgan tekshiruv POSIX katalog ruxsatlarini talab qiladi va ushbu Windows mezbonida bu ruxsatlarni o'rnatolmaydi. Eski Python testi versiya/import chegarasini simulyatsiya qiladi; Python 3.10 interpretatori o'rnatilmagan yoki malakaga ega emas. Oldin muvaffaqiyatli o'tgan 0.3 to'plami quyida qayd etilgan; ushbu maqsadli o'zgarishlar uchun butun to'plam va brauzer ssenariylari qayta ishga tushirilmagan.

Oddiy ishga tushiruvchi mahalliy muhitni 0.3.1 ga yangiladi; manba va o'rnatilgan metadata mos keladi, va pip tekshiruvi muvaffaqiyatli o'tdi. Alohida o'rnatilgan 0.3.1 wheel paneli/aktivlarni ta'minladi, autentifikatsiyalanmagan API-ga kirishni rad etdi va tasdiqlangan 32-hodisali sintetik eksport yaratdi. Ish jarayoni YAML fayli tahlil qilindi, ammo yangi konteyner ijro muhiti tekshiruvi bajarilmadi: foydalanish mumkin bo'lgan mahalliy Docker/Podman/Linux ijro muhiti mavjud emas edi.

Qolgan foydalanuvchanlik, jonli xizmat va platforma bo'shliqlari bo'yicha [tayyorgarlik natijalarini](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/READINESS.md) ko'ring. Ushbu yamoq qo'shimcha operatsion tizimlarni qo'llab-quvvatlamaydi.

## 0.3.0-versiya

To'liq pinlangan ijro muhitlari to'plami muvaffaqiyatli o'tdi: **61 test**, bitta upstream Starlette TestClient eskirish ogohlantirishi bilan. Ijro metama'lumotlari TgWitness 0.3.0 va python-socks 2.8.2 ni ko'rsatadi; pip tekshiruvi muvaffaqiyatli o'tdi. Brauzer qabul qilish testi sahifadagi JavaScript xatolarisiz muvaffaqiyatli o'tdi.

0.3.0 g'ildiragi yaratilib, alohida paket katalogiga o'rnatildi. U panel va aktivlarni ta'minladi, autentifikatsiyalanmagan API so'rovini rad etdi va mustaqil tekshiruvdan o'tgan 32 hodisali sintetik jurnalni eksport qildi. Mahalliy hujjatlar havolalari ishga tushadi. MTProxy kalitsiz normalizatsiya tuzatgichidan so'ng, barcha to'qqizta ulanish/xavfsizlik testi muvaffaqiyatli qayta ishga tushirildi.

Yangi qamrov quyidagilarni o'z ichiga oladi:

- SOCKS5 foydalanuvchi nomi/paroli va HTTP CONNECT haqiqiy loopback test serverlari orqali; o'lik konfiguratsiyalangan proxy manzilga qaytish o'rniga ishdan chiqadi.
- Proxy tasdiqlash, MTProxy transportini tanlash, soxta TLS ee sirlarini rad etish, barqarorlik, ish maydoni izolyatsiyasi, kuzatish paytida o'zgarishlarni rad etish va sirni API holati va imzolangan voqealardan chiqarib tashlash.
- Sun'iy Telethon SQLite 7 va 8 sxemalarini faqat o'qish uchun konvertatsiya; manba xesh o'zgarmagan; boshqa formatlar, SQL ko'rinishlari va yakunlanmagan WAL fayl rad etilgan.
- Tashqi ombor bosh kaliti: turli hosil qilingan ish maydoni kalitlari, muvaffaqiyatli qayta ochish, noto'g'ri/yetishmayotgan kalitni rad etish va mavjud mahalliy omborlarning hech qanday bilvosita ko'chirilmasligi.
- Brauzer proksi sozlamalari, kredensiallarni tozalash, saqlashni himoya qilishni oshkor etish, mobil ulanish sahifasi, o'zgartirilgan sessiya faylini ruxsat etish, alohida yo'llar, va soxta Telegram mijozida ilgari ko'rib chiqilgan barcha yig'ish/eksport stsenariylari.

Rivojlantirish jarayonida loopback testi tengdoshning o'chirilishini cheksiz kutdi; boshqa bir ishga tushirish qo'l siqishdan so'ng Windows ulanishini qayta tiklanishini kuzatdi. Endi test butun almashuvni chegaralab, yakunlangan qo'l siqishdan keyin EOF/qayta tiklashni ulanishni yopish deb hisoblaydi. Qo'l siqish/avtorizatsiya talablari hanuzgacha zarur. Bu haqiqiy proxy-provayderlarni tasdiqlamaydi yoki Telegram transportidagi doimiy nuqson mavjudligini anglatmaydi.

Quyida tasvirlangan AdGuard host so'rovini kuzatish hanuzgacha amal qiladi. Haqiqiy Telegram hisob qaydnomasi, SOCKS/HTTP proksi yoki jonli MTProxy serveridan foydalanilmagan. MTProxy eksperimental bo'lib, uning tanlangan sozlamalari va sirni tasdiqlash tekshirilgan, ammo jonli o'zaro ishlash imkoniyati sinovdan o'tkazilmagan. Yangi tashqi kalit va sessiya konversiya buyruqlari faqat sintetik sirlar bilan sinovdan o'tkazildi. Linux/macOS/Docker bu yerda hali malakadan o'tmagan.

Quyida keltirilgan 0.2 o'tkazuvchanlik o'lchovi qayta takrorlanmagan va uni 0.3 uchun yangi ko'p hisob/proxy benchmarki sifatida taqdim etmaslik kerak.

## 0.2.0 versiyasi asosiy

Windowsda Python 3.12.10 bilan tekshirildi. Haqiqiy Telegram akkaunti ulanmagan.

| Tekshirish | Natija |
| --- | --- |
| Python to'plami | Rivojlantirish muhitida 52 ta test muvaffaqiyatli o'tdi va pinlangan ijro muhiti bilan ham 52 ta test muvaffaqiyatli o'tdi; har bir ishda bitta upstream Starlette TestClient eskirish ogohlantirishi paydo bo'ldi |
| JavaScript sintaksi | Node.js orqali o'tkazildi |
| Chromium qabul qilish | O'tdi; sahifadagi JavaScript xatolari yo'q |
| Stol/mobil tartibi | 1440 × 1060 va 390 × 844 o'lchamlarda tekshirildi; gorizontal hujjat oshib ketishi yo'q |
| HTML shaklidagi xabar mazmuni | Matn ko'rinishida; kiritilgan skript ijro etilmadi |
| Sinov akkaunti oqimi | API ma'lumotlari → telefon → kod → 2FA → guruhni tanlash → boshlash → snapshot → tanaffus → qayta yuklash |
| Brauzerdagi dalillar | Tahrir solishtirish, o'chirishdan oldingi kontent, filtrlar, ZIP yuklab olish, tekshiruv nuqtasi, imzolangan jarayon kvitasi, RFC 3161 so'rovini yuklab olish va tekshiruv nuqtasiga bog'lash |
| Ko'p akkaunt | Jurnal, kalit, manba va jonli holatlarni alohida ajratadi; brauzerni almashtirish boshqa yig'uvchini ishlashda davom ettiradi; ish maydonchalari qayta ishga tushirgandan so'ng qayta ochiladi; dublikat hisob va hisobni qayta tayinlash rad etildi |
| Kriptografik xatolar | Imzolangan maydonlar o'zgartirildi, imzolanmagan maydonlar qo'shildi, noto'g'ri kalit, shikastlangan arxiv a'zosi, o'zgartirilgan/yo'qolgan media, tekshiruv nuqtasida aniqlangan qisqartirish rad etildi |
| Saqlash | Bir vaqtda qo'shishlarni tekshiradi; yangilash/o'chirish urinishlarini rad etadi; ishga tushirish o'zgartirilgan jurnalni qo'shmasdan rad etadi va qulfini bo'shatadi |
| Media bardoshliligi | Atomik xabar/topshiriq yozuvlari; qayta tiklashni qayta boshlash; asl versiya tavsiflovchilari saqlangan; navbatni almashtirish va mavjud faylni buzish rad etildi; FloodWait saqlanib qoldi; manba xatolari ajratildi |
| Jonli uzatish | Yangi yozuvlar qo'shilarkan, barqaror prefiks eksport qilinadi; saqlangan tekshiruv nuqtasi jurnalning kesilganini aniqlaydi; eksport butun voqealar oqimini to'liq materializatsiya qilmaydi |
| RFC 3161 | OpenSSL 3.5.9 yuzaga keltirilgan so'rovlarni o'qiydi; mahalliy ravishda yaratilgan sintetik CA/TSA javobi qabul qilinadi; o'zgartirilgan ma'lumotlar, nonce va noto'g'ri CA rad etiladi; atrof-muhit CA muhiti aniq ishonchni bekor qilmaydi |
| Mahalliy sozlash | start.py --setup-only ajratilgan .venvni 0.2.0 ga yangiladi; manba va o'rnatilgan metadata mos keladi; pip tekshiruvi muvaffaqiyatli o'tdi |
| G'ildirak | 0.2.0 test-results ostida alohida o'rnatilib, qurildi; panel/assetsni taqdim etdi, tasdiqlanmagan API so'rovlarini rad etdi, 32 hodisali sintetik arxivni eksport qildi va tekshirdi |

Manba testlari FastAPI 0.159.1, Uvicorn 0.54.0, Telethon 1.45.0, cryptography 50.0.2, pytest 9.1.1 va Playwright 1.62.0 ni ishlatgan. Qulflangan ijro muhiti FastAPI 0.162.0, Starlette 1.10.0, Uvicorn 0.54.0, Telethon 1.45.0 va cryptography 50.0.2 ni ishlatadi. deploy/constraints.txt ijro etish muhitining versiya pinlarini qayd etadi; deploy/requirements.lock va deploy/build.lock har bir paket faylning SHA-256 hashini qo'shadi, va Docker hamda yuqori ishonchli serverlar faqat shu hashlar orqali o'rnatadi (pip --require-hashes). Har bir sozlangan CI platformasida moslik dalili ham yo'q. Masofaviy CI ishlamadi.

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

## Atrof-muhit kuzatuvlari

Windows sandbox cheklovlari standart pytest/pip vaqtinchalik kataloglarini va Playwright subjarayonini blokladi. Pytest loyiha ichida yangi vaqtinchalik katalogdan foydalandi; o'rnatish va brauzer jarayonlari sandbox tashqarisida tasdiqlangan ijroni talab qildi.

AdGuard dasturi brauzerga local.adguard.org manziliga so'rovlarni kiritdi. Brauzer qabulnomasida ushbu so'rovlar saqlanib qoladi. Ushbu ish jarayoni o'zgartirilmagan brauzer muhitida chiqish so'rovlari nol ekanligining dalili **emas**; ilovaning o'zi hech qanday tashqi resurs/CDN/analitika so'rovlarini o'z ichiga olmaydi. AdGuard sozlamalari o'zgartirilmagan.

Oxirgi brauzer ishga tushirishida Windows asyncio socket-tozalash OSError 10022 xatosi ham qayd etildi. Barcha brauzer da'volari muvaffaqiyatli bo'ldi va hech qanday sahifa JavaScript xatosi yuzaga kelmadi. Uning sababi aniqlanmadi va ushbu ishga tushirish host transport muammolarining yo'qligini ko'rsatmaydi.

Birinchi o'rnatilgan paket HTTP testi urllib'ning connection-close so'rovlaridan foydalanganda, sandbox ichida ham, tashqarisida ham va ikkala bog'liqlik to'plami bilan bog'lanishni qayta tiklashga duch keldi. Oxirgi test http.client orqali standart HTTP/1.1 doimiy bog'lanishlardan foydalandi va muvaffaqiyatli o'tdi. Brauzer so'rovlari ham muvaffaqiyatli bo'ldi. Qayta ulanishlarni aniq kelib chiqishi aniqlanmadi; ular barqaror ilova nuqsoni deb baholanmadi.

## Qolgan malaka

Saqlangan jonli jurnal haqiqiy yig'ish, tahrirlar, o'chirish bildirishnomalari, ilovalar, qayta tekshirishlar va tezlik chegaralashni boshqarishni qayd etadi. U to'liq yetkazib berilishni yoki rollarning ko'rinishi, reaksiya qiluvchi aktyorlar, uzoq muddatli FloodWait, hisob taqiqlanishi va tarmoq/jarayon uzilishidan tiklanish bo'yicha nazorat matritsasini aniqlamaydi. QR-token chiqarilishi yakunlangan mobil QR tasdig'idan alohida bo'lib qoladi.

Docker build/run, Linux/macOS o'rnatilishi, barqaror yuqori yuk, mustaqil xavfsizlik ko'rib chiqilishi, haqiqiy mustaqil TSA javobi, sertifikatni bekor qilish/arxivni tasdiqlash va sud-tibbiyot sertifikatlash yozib olingan malaka doirasidan tashqarida qoladi. Saqlangan MTProto holati va orqaga yetish amalga oshirilgan; atomik barqaror qayta ijro etish hali joriy etilmagan. Ma'muriy-log yig'ish, qo'shimcha reaktorlar ro'yxatlari va ustuvor qisqa so'rovlar alohida xususiyatlar bo'lib qoladi. Boshqariladigan malaka matritsasi uchun [jonli qabulni](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md) ko'ring.

Mahalliy batafsil kvitansiyalar va skrinshotlar test-results/ (Git tomonidan e'tiborsiz qoldirilgan) yo'lida joylashgan. docs/assets/ dagi ommaviy skrinshot faqat badiiy namoyish ma'lumotlarini o'z ichiga oladi.

## Jamoat veb-sayti va nashrga tayyorlash · 2026-yil 27-oktabr

`website/` alohida taqdimot va Pages qurilmasi panel tekshiruvlaridan keyin qo'shildi. Hech qanday jonli hisob sozlamalari yoki ma'lumot yig'ish mantiqi o'zgartirilmadi.

- Mavjud ilovalar to'plami quyidagicha o'tdi: 138 tasi muvaffaqiyatli, 1 tasi POSIX-ga xos bo'lgani uchun o'tkazib yuborildi va bitta yuqori oqimdagi Starlette/httpx eskirish ogohlantirishi. Qo'shilgan 11 ta sayt qurilish sinovlari mustaqil ravishda o'tdi, jumladan kutilmagan chiqishni rad etish va bog'langan kirishni rad etish.
- Ikkala ilova brauzer skriptlari project-venv Playwright va Chromium headless shell 156 yordamida o'tkazildi. Hech qanday sahifa JavaScript xatosi yoki tashqi so'rovlar qayd etilmadi. Barcha hisob akkaunt ssenariylarida soxta transport va badiiy ma'lumotlardan foydalanildi.
- `tools/check_site.py`320, 390, 768, 1024 va 1440 kengliklarda o'tkazildi, URL yo'l bo'lagi, klaviatura yorliqlari, muvaffaqiyatli/rad etilgan clipboardga kirish, kamaytirilgan harakat va o'chirib qo'yilgan JavaScript bilan. Hech qanday muvaffaqiyatsiz aktiv so'rovlari yoki tashqi so'rovlar bo'lmadi.
- `tools/build_site.py` 10 ta ruxsat etilgan ommaviy fayl yaratdi, jami taxminan 460 KB. Brauzer skrinshotlari va kvitansiya e'tiborsiz qoldirilgan `test-results/site/` da.
- build-only setuptools/wheel vositalarini loyiha muhitiga o'rnatgandan so'ng wheel muvaffaqiyatli yaratildi. Uni izolyatsiyalangan maqsadga o'rnatib, `tools/check_install.py`ni ishga tushirish natijasida quyidagilar tekshirildi: statik aktivlar, kirish nazorati, imzolangan 32-hodisali sintetik eksport va mustaqil tasdiqlangan jonli yuklab olish.
- `pip check` o'tdi. Git tomonidan tanlangan ommaviy nomzodlarning shablon bo'yicha tekshiruvi hech qanday tanib bo'ladigan xususiy kalit bloklari, GitHub/bot/AWS tokenlari, uzun so'zma-so'z sirli tayinlovlar yoki birlashtirish to'qnashuvi markerlarini aniqlamadi. Bu har bir mumkin bo'lgan sirli formatning yo'qligini isbotlamaydi. Runtime-data/session/key probe'lari Git tomonidan e'tiborsiz qoldirildi.
- GitHub CLI autentifikatsiyasi haqiqiy emas edi; masofaviy sozlama yo'q edi va dastlabki commit mavjud emas edi. Push, hosted ish jarayoni, Pages joylashtirish yoki reliz amalga oshirilmadi. Docker va jonli Telegram/platformani malakadan o'tkazish ushbu tekshiruv doirasiga kirmaydi.

Ushbu mezboning E: ish maydoni fayl tizimida Playwright yuklab olish qulfi muvaffaqiyatsiz bo'ldi. `%LOCALAPPDATA%/tgwitness-playwright` ostida Chromiumni o'rnatish va tekshiruvlar uchun shu `PLAYWRIGHT_BROWSERS_PATH`dan foydalanish muvaffaqiyatli bo'ldi. Bu muhitga oid yechim bo'lib, ilovaning ijro vaqtidagi bog'liqliklariga o'zgartirish kiritilgani yo'q.

## Interaktiv hujjatlash va veb-sayt metama'lumotlari · 29 oktyabr 2026

Ochiq sayt 12 ta ingliz tilidagi HTML sahifani tashkil etadi: bosh sahifa, qo'llanmalar indeksi va o'n ta qo'llanma. Artifaktda aniq sanab o'tilgan 28 ta taqdimot fayli mavjud, hajmi taxminan 1,85 MB va hech qanday to'plovchi ma'lumot yo'q. Ochiq veb-sayt ingliz tilida; ilova tarjimalari va tarjima qilingan ombor qo'llanmalari alohida.

- Sayt, manba-nashr va chiqarish-chegarasi testlari: **18 ta o'tdi, 2 ta o'tkazib yuborildi**. O'tkazib yuborilgan sinovlar Windows fayl tizimida simvolik bog'lanmalar (symlink) yaratishga oid. Sinovlar quyidagilarni tekshiradi: noyob sahifa metama'lumotlari, faqat ingliz tilidagi ommaviy sahifalar, kanonik URL manzillari, barcha sayt xaritasi yozuvlari, mahalliy aktivlar/ankorlar, tuzilmaviy navigatsiya va shaxsiy fayllarni istisno qilish.
- `tools/check_site.py` va `tools/check_docs_site.py` Chromium'da 320, 390, 768, 1024 va 1440 piksel o'lchamlarda loyiha URL osti yo'li ostida muvaffaqiyatli o'tdi. Qo'llanma tekshiradi barcha 11 hujjat sahifalarini, qidiruv va klaviatura navigatsiyasini, clipboard muvaffaqiyat/rad etish holatini va JavaScript'siz o'qiladigan kontentni.
- Besh interaktiv misol o'tkazildi: xabarni qayta ijro etish/qadam/to'xtatish/tiklash, harakatni sekinlashtirish va ekran tashqarisida to'xtatish bilan; asl/o'zgartirilgan/qayta qurilgan/qisqartirilgan xesh zanjirlari; guvohning qabul qilish/orqaga qaytarish/bo'linish/javobsiz qoldirish qarorlari; va to'liq/kechikkan/yetishmayotgan yetkazib berish stsenariylari; hamda tergov xaritasini bog'lovchi jo'natuvchi ID, manzil va ilova heshiga ko'ra tasavvuriy kesishma-suhbat kuzatuvlari. Tekshiruv boshqaruvlari klaviatura navigatsiyasi va JavaScript o'rnini bosuvchi tekshiruvlardan o'tdi. Brauzer SHA-256 natijalari mustaqil ravishda Pythonning `hashlib` va kanonik JSON bilan solishtirildi. Hash misoli Web Crypto mavjud bo'lmaganda ham o'zining o'qiladigan zaxira variantini saqlab qoldi.
- Yetkazib berish nisbatlari va grafik belgilar mavjud jadvalga mos keldi. Mobil o'q yorliqlari vizual ko'rib chiqilgach kattalashtirildi. Har bir misol illyustrativ yoki sintetik deb belgilangan va hech bir brauzer misoli Telegram bilan bog'lanmaydi.
- Tashqi so'rovlar, muvaffaqiyatsiz HTTP so'rovlari yoki JavaScript xatolari qayd etilmadi. Desktop/mobil skrinshotlari va kvitansiyalar `test-results/site/` va `test-results/docs-site/` ostida e'tiborsiz qoldirildi. Hujjatlar indeksi, xabar/hash misollari, Witness tartibi, yetkazib berish sxemasi va tergov xaritasi desktop/mobil o'lchamlarda tekshirildi.
- Nashr skaneri 282 ta ommaviy manba fayl va 1 426 ta mahalliy hujjat havolalari uchun muvaffaqiyatli o'tdi. Ruff o'zgartirilgan Python sayt asboblari va testlari uchun muvaffaqiyatli o'tdi.
- `docs/HOW-IT-WORKS.md` Mermaid diagrammalari va formulalarini o'z ichiga olgan GitHub Markdown hamrohini taqdim etadi. `docs/INVESTIGATION.md` butun hisob doirasini, har bir chat tarixini olish, foydalanuvchi profillari, chatlararo havolalar, vaqt chizig'i va tasdiqlangan ishni topshirishni qamrab oladi. Uning bosqichlari va cheklovlari joriy doira, yig'ish, dosye, eksport, verifikator va panel kodi bilan tekshirildi. Mehmondo'stlik qilingan GitHub renderlash tekshirilmadi.

Bu mahalliy veb-sayt/hujjatlarni tekshirishdir. U jonli Telegram ma'lumotlarini qo'shmaydi, joylashtirilgan sahifalarni ishga tushirishni, masofaviy CI muvaffaqiyatini yoki qidiruv tizimi indekslashini ta'minlamaydi. [Nashr qilish tartibi](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/PUBLISHING.md) va [veb-sayt metama'lumotlari eslatmalariga](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/SEO.md) qarang.
