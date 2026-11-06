# Nima sinovdan o'tkazilgan

Canonical page: https://phishdestroy.github.io/TgWitness/uz/docs/reference/verification/

Jonli Telegram sinovi, avtomatlashtirilgan tekshiruvlar, brauzer tekshiruvlari va hali tasdiqlanmagan narsalar.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Hujjatlash](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Dalil va tasdiqlash](https://phishdestroy.github.io/TgWitness/uz/docs/reference/evidence/)

![Dalil va tasdiqlash](https://phishdestroy.github.io/TgWitness/assets/chapter-evidence.svg)

**Yangilangan: 6 noyabr 2026.** Natijalar har bir ishga tushirishda qayd etilgan tahrir, muhit va yuklanishga bog'langan. [Joriy imkoniyatlar](https://github.com/phishdestroy/TgWitness/blob/main/docs/STATUS.md) mavjud ish jarayonlarini tasvirlaydi; ushbu sahifa esa haqiqatan tekshirilgan narsalarni qayd etadi.

[Ijro grafiklari](https://phishdestroy.github.io/TgWitness/docs/validation/) · [Imzolangan inglizcha audit](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/REPORT.md) · [Yuklab olinadigan o'lchovlar](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/MEASUREMENTS.csv)

| So'nggi dalillar | Natija | Doira |
| --- | --- | --- |
| Chiqarish auditi · 6-noyabr | 1,461 ta asosiy test o'tdi; 37 ta platforma testlari o'tkazib yuborildi | Manba `92e539af40d8`; ochiq natijalar saqlangan |
| Yangi eksportlar · 6-noyabr | 127.713 va 141.781 yozuv/s, to'liq tsikl | Har bir serverda ikkita akkaunt; matn va metadata WARP orqali |
| Saqlangan arxivlar · 6-noyabr | 48 arxiv; 3,598,381 yozuv tasdiqlandi | Mavjud arxivlar pinlangan ish maydoni kalitlari bilan tekshiriladi |
| Ishonchli jonli · 5-noyabr | CPU yozuvini himoya qilish va WARP tekshiruvlari | Rasmiy ish stoli tizimiga kirish va mahalliy eksport hali ham aniqlanmagan |
| Phala / Intel TDX · 4-noyabr | 16ta verifikator tekshiruvlari keyingi ishga tushirishlarda muvaffaqiyatli o'tdi | Tarixiy joylashtirish; CVMda Telegram hisob qaydnomasi yo'q |

**Ushbu sahifada**

- [Chiqarish auditi va yangi eksportlar · 6 Noyabr 2026](https://phishdestroy.github.io/TgWitness/uz/docs/reference/verification/#release-audit-and-fresh-exports--6-november-2026)
- [Trusted Live CPU Ubuntu va WARP · 5 noyabr 2026](https://phishdestroy.github.io/TgWitness/uz/docs/reference/verification/#trusted-live-cpu-ubuntu-and-warp--5-november-2026)
- [Jonli Phala bulutini joylashtirish · 4-noyabr 2026](https://phishdestroy.github.io/TgWitness/uz/docs/reference/verification/#live-phala-cloud-deployment--4-november-2026)
- [Jonli server jurnal inventarizatsiyasi · 1-noyabr 2026](https://phishdestroy.github.io/TgWitness/uz/docs/reference/verification/#live-server-journal-inventory--1-november-2026)
- [Yaqinda o'tkazilgan oflayn va xato kiritish tekshiruvlari · 1 Noyabr 2026](https://phishdestroy.github.io/TgWitness/uz/docs/reference/verification/#recent-offline-and-fault-injection-checks--1-november-2026)
- [Jonli Telegram sinovi, to'liq hisob · 29 oktyabr 2026](https://phishdestroy.github.io/TgWitness/uz/docs/reference/verification/#live-telegram-test-whole-account--29-october-2026)
- [Parol bilan himoyalangan eksport libarchive yordamida ochildi · 29 Oktyabr 2026](https://phishdestroy.github.io/TgWitness/uz/docs/reference/verification/#password-protected-export-opened-with-libarchive--29-october-2026)
- [Jonli Telegram sinovi · 27dan 29gacha, 2026](https://phishdestroy.github.io/TgWitness/uz/docs/reference/verification/#live-telegram-test--27-to-29-october-2026)
- [Sun'iy mahalliy quvvat o'lchovi](https://phishdestroy.github.io/TgWitness/uz/docs/reference/verification/#synthetic-local-capacity-measurement)
- [Bir million xabarda to'liq matnli qidiruv · 5-noyabr 2026](https://phishdestroy.github.io/TgWitness/uz/docs/reference/verification/#full-text-search-on-one-million-messages--5-november-2026)
- [Qolgan malaka](https://phishdestroy.github.io/TgWitness/uz/docs/reference/verification/#remaining-qualification)

## Chiqarish auditi va yangi eksportlar · 6 Noyabr 2026

Auditorlik tekshiruvi manba kodida v0.9.1 versiyasidan foydalandi `92e539af40d8368d198ff5e040f1d876f2c1310e`, `92e539af40d8-83e41104669e` chiqishi. O'rnatilgan paketning smoke tekshiruvlari uchta serverda muvaffaqiyatli o'tdi. Imzolangan hisobot o'sha paytda kuzatilgan holatni saqlab qoladi.

[![Ikki yangi ish yuklamasi uchun olish va to'liq eksport stavkalari](https://phishdestroy.github.io/TgWitness/assets/performance.svg)](https://phishdestroy.github.io/TgWitness/docs/validation/)

| Ish yuklamasi | Yozib oladi | Olish | Tsiklni yakunlash | To'liq sikl tezligi |
| --- | --- | --- | --- | --- |
| Server A · ikki akkaunt | 27,030 | 189.043 s | 211.647s | 127.713 yozuv/s |
| Server B · ikki akkaunt | 29,299 | 182.513 s | 206.650s | 141.781 yozuv/s |

Ikkala eksport ham resume'siz boshlandi, ilovalar va avatarlar chiqarib tashlandi va nol takroriy yoki qayta ishlatilgan yozuvlar bilan yakunlandi. To'liq tsikl tayyorgarlik, olish, tanlash, qadoqlash va arxivni tekshirishni o'z ichiga oladi. Server A shuningdek himoyalangan suhbatni o'qish tekshiruvini o'tkazdi. A'da to'rtta FloodWait hodisasi va B'da uchta hodisa bajarildi. Ushbu kuzatuvlar umumiy o'tkazuvchanlik kafolatini bermaydi.

| Tekshirish | Natija | Malaka |
| --- | --- | --- |
| Asosiy pytest | 1,461 o'tdi | 37 platforma sakrashlari |
| Brauzer / brauzer foydalanuvchi tajribasi / dalil / sayt | 102/66/15/9 o'tdi | Ushbu dasturlar boshqa testlar bilan kesishadi; hisoblar qo'shilmaydi |
| Qo'shimcha qo'shish | 124 o'tdi | Talab qilinadigan Chromium sandbox tomonidan bloklangan uchta rasmiy veb-tekshiruv |
| API avtorizatsiyasi | 269 yo'nalishlari; 538 so'rovlari muvaffaqiyatli o'tdi | Yo'qolgan kirish ma'lumotlari va bekor qilingan kirish huquqi |
| Saqlangan arxivlar | 48dan 48i tasdiqlandi | 3,598,381 yozuv; mahkamlangan ish maydoni kalitlari |
| Jonli flot o'qish tekshiruvlari | 40 ta profildan 24 tasi o'tdi | 16ta WARP marshrutlari malaka sinovidan o'tmadi; bu profillar ulanmagan edi |

[Imzolangan hisobot](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/REPORT.md) barcha ochiq topilmalarni qayd etadi, jumladan audit qilingan asosiy to'plamdan yo'q bo'lgan e'lon qilinmagan maxfiy suhbat snapshotidagi uchta nuqsonni. Oldingi [ommaviy tarix bo'yicha malaka](https://github.com/phishdestroy/TgWitness/blob/main/docs/EXPORT-BENCHMARK-2026-11-06.md) boshqa tahrir va ish yukini ishlatgan; uning ko'rsatkichlari ushbu taqqoslash bilan birlashtirilmasligi kerak.

[Biriktirilgan kalit va verifikator](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/README.md#verify-the-original-files) yordamida asl hisobotni tasdiqlang. Uning imzosi operator hisobotini o'zgartirishdan himoya qiladi. Bu mustaqil tasdiqlash, Telegram muallifligini isbotlash yoki GDPR sertifikati emas.

## Trusted Live CPU Ubuntu va WARP · 5 noyabr 2026

Saqlangan integratsiya testi RunPod CPU mezbonida QEMU ostida faqat CPU ishlatilgan Ubuntu 24.04.5 mehmoni (4 vCPU, 8 GiB) yordamida bajarildi. Yig'uvchi `14e642a5` ni, tekshiruv esa `02072461` ni ishlatdi. Oxirgi tuzatishlar [PR #114](https://github.com/phishdestroy/TgWitness/pull/114) ga `755f78f6` sifatida qo'shildi, uning daraxti sinovdan o'tkazilgan PR boshiga mos keldi. Bu TEE emas edi.

- Haqiqiy WARP Connector sog'lomligini xabar qildi; proksi orqali HTTPS WARP va Gateway yoqilganligini xabar qildi. Uchta probe bir xil chiqish manzilini ko'rdi, bu esa doimiy IP kafolati emas.
- WARP ulanishini uzish proksi orqali yuborilgan so'rovni muvaffaqiyatsiz qildi. Gateway-service'ning to'g'ridan-to'g'ri HTTPS so'rovi rad etildi. Yozuvchi namespace'da to'g'ridan-to'g'ri IPv4/IPv6, tashqi DNS va Docker'ning o'rnatilgan UDP resolveri bloklandi.
- Cheklangan faqat o'qish huquqiga ega provayder tokeni health/connections ma'lumotlarini o'qishi mumkin edi, ammo connector enrollment tokenini o'qiy olmadi. Imzolangan provayder kuzatuvlariga aniq mavjud bo'lmagan namunalar kiritilgan edi. Guvoh operatorning mezbonida ishladi, shuning uchun bu mustaqil uchinchi tomon nazorati emas, balki yozib olish va saqlashni namoyish etadi.
- Rasmiy ish stoli autentifikatsiyalanmagan kirish ekrani ochildi. Himoyalangan klaviatura kiritilishi yozib olish paytida rad etildi. Uchta H.264 displey segmenti deko­rlanib, ularning soat qoplamasi tekshirildi. 18 voqeali preflight arxivi tasdiqlandi va belgilangan yozuvchi kalitga moslab saqlab qolindi.
- Oxirgi capture testlari Windows va Linux CIda haqiqiy Chromium/FFmpeg bilan 114 holatni muvaffaqiyatli o'tkazdi. Besh ta anchor testi va bog'liqlik bo'yicha maslahat tekshiruvlari muvaffaqiyatli yakunlandi.

Boshlang'ich 2 vCPU/4 GiB konfiguratsiyasi bir vaqtda tasvir yaratish yuklamasi ostida vaqt chegarasidan oshib to'xtadi va himoyachi orqali to'xtatildi; bu muvaffaqiyat deb hisoblanmaydi. Qo'lda test hisobiga kirish, mahalliy chat eksporti, haqiqiy gibrid solishtirish va Telegram tomonidan chiqish hali ham kutishda qoldi. Hech qanday taqdim etilgan Telethon sessiyasi import qilinmadi. Ilovalar, avtomatik OCR, mahalliy drand BLS tasdiqlash va Trusted Live TDX tasdiqlovi malaka olmadi.

## Live Phala Cloud joylashtirish · 2026-yil 4-noyabr

**Tarixiy natija:** keyingi joylashtirishlar barcha 16ta verifikator tekshiruvlaridan o'tdi, jumladan Intel TDX va tezkor tunnel. Dalillarni qayta ishga tushirish, imzolangan manzilni aniqlash va hisobot vaqt belgilari alohida tekshirildi. Har bir test CVM o'z ijrosidan so'ng olib tashlandi.

| Sozlash | Qayd etilgan qiymat |
| --- | --- |
| Provayder | Phala Cloud · `tdx.small` · US-WEST-1 |
| Joylashtirish | `--provider phala --quick-tunnel`; dastlab bo'sh ish maydoni |
| Boshlang'ich yig'uvchi | `df7d860c` · v0.8.1 |
| Barcha tuzatishlar kiritilgan yig'uvchi | `53a0f7e9` |
| Ishlab chiqarish mehmoni | `dstack-0.5.12`; SSH-ga kirish o'chirilgan |
| Tashqi xizmatlar | ntfy.sh, GitHub va Intel PCS |
| Kuzatilgan xarajat | Yetti CVM, jami taxminan 1.9 AQSh senti; tarixiy test narxlari |

Quyidagi ketma-ketlik dastlabki nosozliklar, tuzatishlar va yakunlangan tekshiruvlarni ajratadi. Ushbu CVMlarga hech qanday Telegram hisobi ulanmagan.

**Joylashtirishlar 1–2 · provayder farqlari va regressiya tekshiruvlari**

Birinchi ikkita joylashtirish simulyatsiya qilingan Phala Cloud'dan beshta farqni aniqladi. [`tools/check_phala.py`](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_phala.py) endi har birini qayta hosil qiladi va tuzatishsiz xato beradi:

| Phala Cloudda | Tuzatishdan oldin | Tuzatish |
| --- | --- | --- |
| `compose_file.name` talab etiladi | HTTP 422, hech narsa yaratilmadi | Docker Compose konfiguratsiyasi CVM nomini o'z ichiga oladi |
| Bo'sh qiymat ko'rsatilmagan taqdirda, Phala o'lchangan app-comple ga o'zining ishga tushirishdan oldingi skriptini qo'shadi (v0.0.20: Docker login, `docker compose pull`, root paroli, `user_config` dan SSH kalitlari) | `tdx_compose` xato beradi: nashr etilgan Docker Compose konfiguratsiyasidan tashqaridagi kod | app-compose `pre_launch_script` ni `""` ga o'rnatadi; Phala esa uni hisobga olmaydi |
| `image` bo'lmasa, Phala `dstack-dev-0.5.12`, rivojlantirish versiyasini, SSH-kirish yoqilgan holda tanlaydi | `server_state` muvaffaqiyatsiz bo'ladi. Faqat uskunani tasdiqlash yozuvi ushbu tasvirdan o'tdi; faqat provayder yozuvi va `tdx_os` uni ko'rsatadi. | Joylashtirish Phala'ning joriy chiqarilishining, `dstack-0.5.12`, ishlab chiqarish versiyasini so'raydi |
| dstack gateway o'chirilganda, CVM tafsilotlari hech qachon `instance_id` kodini olmadi | Joylashtirish 30 daqiqa kutadi va muvaffaqiyatsiz tugaydi | Instance ID CVM holatidan o'qiladi |
| Qayta ishga tushirish, to'xtatish va ishga tushirish — bu CVM operatsiyalari, ilova reviziyalari emas. | `provider_actions` qayta ishga tushirishlarni ro'yxatga olmadi | Operatsiyalar ham o'qiladi |

**Joylashtirish3· tasdiqlash, kirish tekshiruvlari va qayta ishga tushirish dalillari**

- CVM `dstack-0.5.12` ni SSH kirish o'chirilgan holda ishga tushirdi. Kollektor yaratilganidan taxminan 1,5 daqiqa o'tib o'z imzolangan manzilini joyladi. Keyin Deploy `tdx_binding` va `tdx_quote` (Intel TCB UpToDate, apparat guvohnoma yozuvi v4, FMSPC `20a06f000000`, xatolik tuzatish rejimida emas, ko'chirilmaydigan, Intel'dan olingan kriptografik tasdiqlash ma'lumotlarini qo'llab-quvvatlaydi), `tdx_compose_hash`, `tdx_compose` (byte for byte) va `tdx_identity` (KMS kalitlari).
- trycloudflare.com manzildagi panel tokenisiz yoki noto'g'ri token bilan 401 kodini, panel tokeni bilan esa 200 kodini qaytardi.
- `verify` bilan `--source` commit arxivini GitHubga o'rnatish va barmoq izi alohida uzatilgan: server, `server_state`, firewall (yo'lchiqarsiz, ommaviy nuqtasi yo'q), provayder logi, bayonot, barmoq izi, manba xesh, yuklash va beshta `tdx_*` tekshiruvlari o'tkazildi. Cloudflare va `tdx_os` mavjud emas edi, shuning uchun natija TO'LAKAMAS bo'ldi.
- Phala API orqali ikki marta qayta ishga tushirish: har safar CVM ikki daqiqadan kam vaqt ichida bir xil yig'uvchi kalit, yangi imzolangan manzil va eski manzil 530-kod bilan javob bergan holda qayta ishga tushdi. `verify` yangi yuklashni va ikkala qayta ishga tushirishni REVIEW (ko'rib chiqish) deb xabar qildi. `--evidence` jurnal imzolarini va uchta ishga tushirishni tasdiqladi, har biri bir xil CVMdan olingan o'z Intel TDX apparat guvohnoma yozuviga ega edi.
- `destroy` faqat o'sha CVMni o'chirib tashladi. Shundan so'ng ish maydoni bo'shab qoldi va panel manzili javob berishni to'xtatdi.
- Panel ustasi narx tekshiruvi `tdx.small` soatiga $0.058 ni ko'rsatdi. Noto'g'ri kalit oddiy "API kalitini qabul qilmadi" xabarini berdi.

**Keyingi tuzatishlar · imzolangan manzilni aniqlash va operatsion tizim o'lchovlari**

- Agar manzil kaliti bo'lmasa, `verify` manzil mavzusidagi eng yangi to'g'ri tuzilgan postni kuzatdi, u nashr etilgan Docker Compose konfiguratsiyasida chop etilgan. Bir soxta post uni mavjud bo'lmagan hostga yubordi, va `statement` muvaffaqiyatsiz bo'ldi: soxtalashtiruvchi yig'uvchi sifatida o'tolmaydi, lekin blok qilishi mumkin uchinchi tomon tasdiqlashni soxta kelajak vaqt belgisi bilan 12 soatgacha amalga oshiradi. Endi yig'uvchi o'z manzilini o'z kaliti bilan imzolab post qiladi, `verify` faqat yig'uvchi tomonidan qilingan bunday postlarni qabul qiladi va postlar ntfy.sh tomonidan qabul qilingan vaqt bo'yicha tartiblanadi. [`tools/check_cloud_wizard.py`](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_cloud_wizard.py) soxta postlarni qayta ijro etadi. CVM buni faqat uni o'z ichiga olgan commitdan ishga tushiradi, shuning uchun ushbu ijro etuvchi collector hali o'z manzilini imzolamagan va `verify` shuni bildirgan.
- `tdx_os` `dstack-mr`siz ishga tushmaydi, uning joriy versiyasida hujjatlarda ko'rsatilgan `measure --json` o'rniga `measure-os` mavjud. Verifikator endi nashr etilgan image va VM shakli, jumladan ACPI jadvallari asosida MRTD va RTMR0-2 ni o'zi hisoblaydi.

**Joylashtirish 4 · barcha 16 tekshiruvlari, hisobot muhrlari va qayta ishga tushirishni tasdiqlash**

- Deploy bir marta e'lon qilingan `dstack-0.5.12` ni yuklab olib, uni CVM xabar qilgan OS tasviri hashiga moslashtirdi va `tdx_os` o'tdi: MRTD, RTMR0, RTMR1 va RTMR2 QEMU uchun hisoblangan qiymatlarga teng. 8.2.2, 1 vCPU va 2 GiB. Xuddi shu hisob-kitob da'vo qilingan 4 GiB, 2 vCPU, QEMU 9.2.1 yoki ikkinchi tarmoq kartasi uchun boshqa RTMR0 berdi va o'zgartirilgan yadro, firmware yoki buyruq qatori hamda rivojlantirish tasviri uchun muvaffaqiyatsiz bo'ldi.
- `verify` o'zining 16 ta tekshiruvining barchasidan, jumladan Quick Tunnel konnektori tekshiruvidan ham muvaffaqiyatli o'tdi, shuning uchun natija PASS bo'ldi. U Belgiya hukumati vaqt belgilash bo'limi TSU 202301 (Belgiyaning ishonchli ro'yxatiga kiritilgan) tomonidan berilgan malakali eIDAS vaqt belgilashi, FreeTSA vaqt belgilashi va verifikator imzosi bilan raqamli muhrlangan HTML va PDF sertifikatini yaratdi; `check-report` ularning barchasini va PDF imzosi tasdiqladi.
- Qayta ishga tushirgandan so'ng, `verify --evidence` ikkita ishga tushirishni tasdiqladi, har biri CVM ichida yaratilgan apparat guvohnomasi bilan birga bo'lib, har biri e'lon qilingan `dstack-0.5.12` dan yuklangan; qayta ishga tushirish va yangi yuklash REVIEW bo'ldi.
- `destroy` ish maydonini bo'sh qoldirdi.

**Joylashtirish 5 · collector-signed discovery va forged-post rad etish**

Yig'uvchi `53a0f7e9` commitidan boshlab ishlaydi, u yuqoridagi tuzatishlarni o'z ichiga oladi.

- Yig'uvchi o'z kaliti bilan imzolangan manzilini operatorning HMAC posti yoniga joylashtirdi. Keyin mavzuga ikkita soxta post qo'shildi: biri HMAC qiymati nolga teng qilingan, ikkinchisi boshqa Ed25519 kaliti bilan imzolangan; ikkalasi ham 2096 yildagi vaqtni da'vo qilgan. `verify` kollektor kaliti bilan imzolangan manzilni oldi va barcha 16 tekshiruvdan o'tkazdi; muhr yana malakali Belgiya vaqti shtampi, FreeTSA vaqti shtampi va verifikator imzosi bilan edi, va `check-report` ularni tasdiqladi.
- Qayta ishga tushgach, yig‘uvchi yangi manzilni imzolab e’lon qildi: `verify` uni darhol, operatorning **Joriy manzilni topish** funksiyasi esa HMAC xabaridan 27 soniya keyin topdi. Ikkalasi ham soxta xabarlarni e’tiborsiz qoldirdi. `verify --evidence` ikki ishga tushirish `dstack-0.5.12` dan yuklanganini tasdiqladi.
- Deploy chop etdi: Phala CVMga diskni ham qo'shib qancha to'lov solishini: soatiga $0.06078.

### Panel ustasi va qolgan doira

Panel ustasi Phala Cloud'da ikki marta ishga tushirildi: bir marta uning ish API'si orqali va bir marta haqiqiy Chromium brauzeri orqali: narxni tekshirish, **Advanced** ostidagi commit bilan yaratish, barcha oltita tasdiqlash tekshiruvlarining muvaffaqiyatli o'tishi, serverlar ro'yxatida to'langan narx (oyiga 44,37 USD) ko'rsatilishi, **Joriy manzilni topish**, o'lchangan Docker Compose konfiguratsiyasini yuklab olish va o'chirish. Brauzer hech qanday sahifa xatolarini ko'rmadi. Har safar undan keyin ish maydoni bo'sh bo'ldi.

Qamrab olinmagan: Phala'dagi Cloudflare domeni, CVM'dagi Telegram akkaunti va `dstack-0.6.1` image. Yaratishdan oldin wizard narxi faqat Phala hisoblash narxi bo'lib, uning API mavjud CVM uchun faqat disk narxini ko'rsatadi; serverlar ro'yxati esa yaratilgandan keyingi hisob-kitob narxini ko'rsatadi. Ushbu bo'limdagi barcha narxlar 4 noyabr 2026-yilda kuzatilgan. 4 Noyabr 2026.

## Jonli server jurnalining ro'yxati · 1 Noyabr 2026

Taxminan UTC bo'yicha 19:15da ketma-ket faqat o'qish uchun mo'ljallangan SQLite `query_only` so'rovlari serverda ishlayotgan o'nta ish maydoni ma'lumotlar bazasidagi voqealarni hisoblab chiqdi. So'rovlar davomida yig'ish davom etganligi sababli, bu ish maydonlari bo'ylab atomik snapshot emas.

| O'nta ish maydoni ma'lumotlar bazalarida kuzatildi | Hisob |
| --- | --- |
| `message.new` voqeasiga kamida bitta ega bo'lgan ish maydonchalari | 8 |
| Jurnal yozuvlari, jumladan operatsion voqealar | 1,610,818 |
| `message.new` voqealari | 900,232 |
| `message.edited` voqealari | 80,683 |
| `message.deleted` voqealari | 400,536 |
| `message.recovered` voqealari | 53,403 |
| `message.snapshot` voqealari | 2,183 |
| `media.saved` voqealari | 50,418 |
| `media.failed` hodisalari | 5,575 |
| `coverage.gap` voqealari | 11 |
| WAL fayllari va media fayllarini istisno qilgan holda ma'lumotlar bazasi baytlari | 7,909,003,264 |

Ushbu **voqealar soni**, noyob bo'lmagan xabarlar, odamlar yoki media fayllar emas. Bir xil xabar bir nechta ish maydonida paydo bo'lishi mumkin, va tahrirlash yoki o'chirish yana bir jurnal hodisasini keltirib chiqarishi mumkin. `media.failed` tarixiy xato hodisalarini hisoblaydi, hozirgi media navbatini emas. So'rovlar qilgan **yo'q** imzolarni va barcha to'liq hash zanjirini yangidan tasdiqlash 1,610,818 yozuvlarni, yetkazib berish yoki o'tkazuvchanlikni o'lchash yoki har bir Telegram hodisasi qayd etilganligini aniqlash. Bu yerda xabar mazmuni, hisob yoki suhbat identifikatorlari, ish maydoni yorliqlari, kirish ma'lumotlari yoki shaxsiy fayllar e'lon qilinmaydi.

Ushbu ko'rib chiqishda alohida sozlangan ommaviy monitor uchta manbani qamrab oldi: bitta javob olish muvaffaqiyatli bo'ldi va ikkitasi `no_response` deb xabar berdi. Ushbu monitor o'nta ish maydoni holati bo'yicha qisqacha hisobot emas. `no_response` degani kuzatuvchi ushbu tekshiruvda javob ololmagan; bu xabar yo'qolishini anglatmaydi. Quyidagi kichikroq 29 oktabr sinovi o'zining aniq imzosi va xesh-zanjir tekshiruviga ega.

## Yaqinda o'tkazilgan oflayn va xato kiritish tekshiruvlari · 1 Noyabr 2026

Ushbu tekshiruvlar badiiy ma'lumotlar va mahalliy fayllardan foydalanadi; ular joriy manba uchun regressiya dalillarini qo'shadi, boshqa jonli Telegram yetkazib berish o'lchovini emas:

| Tekshirish | U nimani sinovdan o'tkazdi |
| --- | --- |
| [Manba arxivi](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_source_archive.py) | Ikki ta build manba kod baytlari bo'yicha bir xil, lekin fayl vaqtlari o'zgartirilgan holda bir xil ZIP va tekshiruv yig'indisini hosil qildi. Aniq arxivlangan baytlar va fayl hashlar mos keldi; shaxsiy test fayllari esa arxivga kiritilmadi. Simulyatsiya qilingan yozuv xatosi oldingi arxiv va tekshiruv yig'indisini o'zgarmas holda qoldirdi. |
| [Hisob eksportini tiklash](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_account_export_recovery.py) | Ikkinchi ZIP a'zosida simulyatsiya qilingan disk xatosi hech qanday e'lon qilingan yoki qisman ZIP fayl qoldirmadi. Resume har bir imzolangan kvitansiyani baytma-bayt bir xil saqlab qoldi, kutilgan imzolash barmoq izi yordamida mustaqil ravishda tekshiriladigan arxiv yaratdi va sintetik qamrov bo'shlig'ini qisman natija sifatida saqlab qoldi. Scale da'volari tarixlar o'sib borishi bilan vazifa va kvitansiya skanerlarining takrorlanishidan himoya qiladi. |
| [Minimal oshkor etish maxfiyligi](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_disclosure_privacy.py) | Sun'iy Unicode nomlari va taxalluslar, o'ralgan metadata, noma'lum jo'natuvchilar va media maydonchalari uch xil identifikatsiya rejimida hamda matnni qoldirish bilan tekshirildi. Maskirlash chegarasi xatosi redaktsiyani jimjit zaiflashtirmadi; asl imzolangan hisob eksporti o'zgarmadi. |
| [Linux media dekoderi va OCR](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_media_worker.py) | `5a9e0814`-dagi [Linux Docker CI tekshiruvi](https://github.com/phishdestroy/TgWitness/actions/runs/41341200341/job/124951395192) muvaffaqiyatli o'tdi: Ogg/Opus, MP3, M4A, videoli MP4, WAV va FLAC kirish fayllari; soxta-davomiylik va ikkilamchi-fayl-manba nazoratlari; hamda 48 ta o'zgartirilgan parser fiksturasi (34 rad etildi, 14 chegaralar ichida dekodlandi) yaratildi. Haqiqiy Tesseract OCR asl baytlarni o'zgartirmay ishladi. Dekoder va OCR Whisper modeli bo'lmagan, tarmoqdan izolyatsiyalangan konteynerlarda ishladi. |

Tekshiruvlar [pull-request](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/pr-check.yml) va [to'liq Checks](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/checks.yml) ish jarayonlarida ishlaydi. Ular ushbu nosozlik chegaralarini sinovdan o'tkazadi, har bir mumkin bo'lgan saqlash xatosini yoki ma'lumotni oshkor qilish avtomatik ravishda e'lon qilishga xavfsizligini emas. Media tekshiruvi nutqni tanish aniqligini yoki Telegram yetkazib berishni o'lchamaydi. Har bir hosilani ulashishdan oldin ko'rib chiqing.

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

## Bir million xabarda to'liq matnli qidiruv · 2026-yil 5-noyabr

Komanda: `python tools/bench_fulltext.py --messages 1000000 --work <empty directory>`

200 ta suhbatda 1 000 000 ta sintetik xabardan iborat deterministik imzolangan jurnal (rus so'z shakllari, ukrain, ingliz, xitoy, yapon, havolalar va foydalanuvchi nomlari) 71 soniyada indekslangan; indeks 1,50 GiB jurnalga qo'shimcha ravishda 58 MiB joy egallagan. Eng mos qidiruvlar 9 dan 190 ms gacha (mediана) vaqt oldi, avvalgi substring qidiruvida esa 2,4 dan 3,2 soniyagacha vaqt ketgan. To'liq natijalar, apparat va cheklovlar: [To'liq matnli qidiruv](https://phishdestroy.github.io/TgWitness/uz/docs/reference/search/#benchmark). `tools/test_fulltext.py` shuningdek, to'liq matnli qidiruvdan oldin yaratilgan imzolangan arxivni ham tasdiqlaydi (`tools/fixtures/evidence-before-fulltext.zip`) hozirgi verifikator yordamida, shuningdek, to'liq matnli qidiruvdan oldin yaratilgan imzolangan arxivni (2) o'sha arxivning o'z `verify.py`.

## Qolgan malaka

Saqlangan jonli jurnal haqiqiy yig'ish, tahrirlar, o'chirish bildirishnomalari, ilovalar, qayta tekshirishlar va tezlik chegaralashni boshqarishni qayd etadi. U to'liq yetkazib berilishni yoki rollarning ko'rinishi, reaksiya qiluvchi aktyorlar, uzoq muddatli FloodWait, hisob taqiqlanishi va tarmoq/jarayon uzilishidan tiklanish bo'yicha nazorat matritsasini aniqlamaydi. QR-token chiqarilishi yakunlangan mobil QR tasdig'idan alohida bo'lib qoladi.

Docker/Compose va o'rnatish tekshiruvlari CIda qayd etilgan; haqiqiy Phala joylashtirish va tashqi vaqt belgilari tasdig'i yuqorida tavsiflanadi. Ular barqaror yuqori yuk, to'liq jonli platforma/rol matritsasi, mustaqil xavfsizlik ko'rigini, uzoq muddatli arxivlashtirishni tasdiqlash yoki sud-tibbiyot sertifikatini ta'minlamaydi. Saqlangan MTProto holati va orqaga qaytish (catch-up) amalga oshirilgan; atom yo'qotishsiz jonli qayta ijro etish hali amalga oshirilmagan. Yangi backfill commitlari xabarlar va kursorlarni atomik tarzda kiritadi hamda mavjud Yaqinda bajarilgan amallarni saqlab qoladi, lekin uning sintetik qamrovi jonli malaka olishdan farq qiladi. Nazorat qilinadigan malaka olish matritsasi uchun [jonli qabul qilishni](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md) ko'ring.

[Ommaviy audit papkasi](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/README.md) faqat imzolangan hisobot va umumiy o'lchovlarni o'z ichiga oladi. Batafsil operatsion kvitansiyalar, xom yozuvlar va hisob ma'lumotlari shaxsiy bo'lib qoladi. `docs/assets/`dagi ilova skrinshotlari badiiy namoyish ma'lumotlaridan foydalanadi.
