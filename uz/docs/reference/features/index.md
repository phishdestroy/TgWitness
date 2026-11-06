# Imkoniyatlar va cheklovlar

Canonical page: https://phishdestroy.github.io/TgWitness/uz/docs/reference/features/

Joriy yig'ish modeli, ko'p hisobli ish jarayonlari, eksportlar va TgWitness'ning operatsion chegaralari.

TgWitness ulanilgan hisoblarga kirish mumkin bo'lgan Telegram suhbatlarini saqlaydi, kuzatilgan o'zgarishlarni qayd etadi va tekshirilishi mumkin bo'lgan eksportlarni tayyorlaydi. Ushbu qo'llanma to'plash modelini, joriy ish jarayonlarini va ularning chegaralarini tasvirlaydi.

## Mustaqil ilova

TgWitness o'zining o'rnatish jarayoni, ma'lumotlar katalogi va chiqarish hayotiy tsiklga ega. Ilovaga kiritilgan veb-interfeys sozlash va tekshirishni boshqaradi; eksport qilingan yozuvlar mustaqil ravishda ishlatilishi mumkin.

Operator o'z hisoblarini bog'laydi, har birida ko'rinadigan manbalarni tanlaydi va saqlangan kuzatuv jurnalini oladi. Panel kontentni, saqlangan o'zgarishlarni, kuzatuv kelib chiqishini va ma'lum bo'shliqlarni ko'rsatadi. Boshqa tergovchi eksport qilingan materialni tasdiqlay oladi.

Panel akkauntni avtorizatsiya qilish, manbaga kirish, yig'uvchi faoliyati va qayd etilgan qamrovni ajratib ko'rsatadi. Kam xabarli intervallarni yoki ulanish muammosini baholashda ushbu holatlarni birgalikda ko'rib chiqing.

## Hamkorlikdagi tergovlar

Administrator ish maydonlari va yakka chatlarga mo'ljallangan, har bir harakat uchun ruxsatnomalar, IP-cheklovlar, amal qilish muddati, tizimga kirish limitlari va sessiya nazorati bilan [kirish tokenlarini](https://phishdestroy.github.io/TgWitness/uz/docs/reference/access/) berishi mumkin. Faqat o'qish huquqiga ega ko'rib chiquvchi Telegram avtorizatsiyasini yoki asosiy panel kalitini olmasdan ishni tekshirishi mumkin. Suhbat bilan cheklangan kirish akkaunt bo'ylab sozlamalar va to'liq jurnal eksportlaridan alohida bo'lib qoladi.

Avtomatik MTProxy to'rtta ommaviy manba yoki operator katalogidan Telegram ishchi yo'nalishlarini saqlab turadi. [IP rejimlari](https://phishdestroy.github.io/TgWitness/uz/docs/reference/connection/#ip-modes) nosozlikda boshqa proksiga kutish kerakmi yoki aniq ruxsat etilgan to'g'ridan-to'g'ri yo'nalishdan foydalanish mumkinligini belgilaydi. Tashqi HTTP so'rovlariga alohida yo'nalish va o'chirish tugmasi mavjud.

## Arxiv vositalari

0.7.1-da [tarixni olish](https://phishdestroy.github.io/TgWitness/uz/docs/reference/history/), [arxiv qidiruvi va tahlili](https://phishdestroy.github.io/TgWitness/uz/docs/reference/analysis/),[faqat o'qish uchun mo'ljallangan MCP](https://phishdestroy.github.io/TgWitness/uz/docs/reference/mcp/), [mahalliy OCR/transkripsiya](https://phishdestroy.github.io/TgWitness/uz/docs/reference/media-analysis/) va[chiquvchi webhooks funksiyalari](https://phishdestroy.github.io/TgWitness/uz/docs/reference/webhooks/) mavjud. Analitik hisobotlar va tan olingan matn yozib olingan voqealardan alohida saqlanadi.

[Case Board](https://phishdestroy.github.io/TgWitness/uz/docs/reference/case-board/) ish maydonida manbaga bog'langan belgilamalar, iqtiboslar, eslatmalar va to'plamlarni qo'shadi. [Hisobot konstruktori](https://phishdestroy.github.io/TgWitness/uz/docs/reference/case-reports/) material, bo'limlar va qo'llab-quvvatlanadigan HTML/PDF eksportlari uchun sakkiz xil dizayndan birini tanlaydi.

## Ixtiyoriy qo'shimchalar

Har kunlik sozlash: hisob → manbalar → kuzatuv. **Qo'shimchalar** – Telegram Witness bot va GitHub yozuvni ko'rish uchun alohida manzil. Har biri sozlamalarni ko'rsatishdan oldin mavjudligi va talablarini bildiradi. Kartani tanlash ko'rsatmalarni ochadi; u ro'yxatdan o'tmaydi va xizmatni ishga tushirmaydi.

Botni sozlash uch bosqichdan iborat: faqat o'qish huquqini yaratish, nashriyot sozlamalarini tanlash va guvoh mezbonida ishga tushirish. Tarmoq va nashriyot opsiyalari, mavjud ulanishlar va tasdiqlash buyruqlari talabga binoan ko'rsatiladi. Yuklab olingan konfiguratsiya ishga tushgan guvohdan farq qiladi. Qo'shimchalarni almashtirish loyihani saqlab qoladi; hisob qaydnomasi o'zgarishlari va qulflash vaqtinchalik token va shaklni tozalaydi. Ichki qo'llanma ishga tushirish bo'yicha ko'rsatmalarni o'z ichiga oladi. [GitHub Actions ishga tushirishni qayd etadi](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md), forkingizdan biriktirilgan kollektorni ishga tushiradi, bitta suhbatni yozib oladi va ish jarayoni kelib chiqishini ko'rsatadigan shifrlangan topshiruv hujjatini yaratadi.

## Protokol va xususiy manbalar

**MTProto — Telegramning protokoli; Telethon esa TgWitness MTProto bilan muloqot qilish uchun ishlatadigan Python kutubxonasi.** Ular muqobil ulanish usullari emas. Collection MTProto'dan foydalanadi; ixtiyoriy guvoh Bot API orqali imzolangan tekshiruvlarni e'lon qiladi.

Har bir ish maydoni o'zining vakolatli klient va hisob ma'lumotlarini yangilash oqimiga ega. TgWitness sozlangan manbalardan kuzatuvlarni tanlaydi va tarix snopshotlari hamda media yuklab olish kabi funksiyalar uchun alohida aniq so'rovlar yuboradi.

Xususiy manba uchun ommaviy foydalanuvchi nomi kerak emas. Telegram tengdosh turi va raqamli ID identifikatorlar hisoblanadi; sarlavhalar va foydalanuvchi nomlari o'zgarishi mumkin. Kirish mavjud a'zolik va ruxsatnomalarga bog'liq. TgWitness manbalarga avtomatik qo'shilmaydi yoki qo'shilishni tasdiqlashni chetlab o'tmaydi. Boshqa hisobdagi kirish xesh universallikda kirish tokeni hisoblanmaydi.

Yig'ish modeli guruhga qo'shilishdan oldingi yashirin tarix, ishtirokchi/admin rollari, sessiyani bekor qilish, ruxsatnomalarni olib tashlash yoki o'zgartirish, guruhdan superguruhga ko'chirish, mavzular/forumlar, bog'langan muhokamalar, kanal identifikatorlari va mavjud bo'lmagan ilovalarni hisobga olishi kerak. Har bir kombinatsiya jonli muhitda sinovdan o'tmagan.

Manba ko'rinishi yig'uvchi ishga tushirilganda tekshiriladi. Cheklangan dialog natijasidan manba yo'qolishi **kirish tasdiqlanmaganligini** anglatadi, bu o'chirish isbotlanmaganligini bildiradi. Bitta mavjud bo'lmagan manba boshqa mavjud manbalarni kuzatishga to'sqinlik qilmaydi. Hech qachon taklif havolalari yoki haqiqiy sessiyalarni ommaviy joylarga joylamang.

## Bir nechta hisoblar

Panel istalgan sonli **ish maydonlar**ini qo'llab-quvvatlaydi, har biri o'ziga xos:

- Avtorizatsiya, shifrlangan ombor va ulanish yo'li.
- SQLite jurnali va Ed25519 imzolash identifikatori.
- Tanlangan manbalar, media navbati va yozib olish sozlamalari.
- Kuzatuv holati, xatolar, tekshiruv nuqtalari va eksportlar.

Ko'rsatilayotgan ish maydonini o'zgartirish boshqa yig'uvchini to'xtatmaydi. Ish maydonlari bo'ylab bir xil hisobni avtorizatsiya qilish takrorlanishi rad etiladi. Allaqachon bir Telegram hisobiga bog'langan jurnalni boshqa hisobga o'tkazib bo'lmaydi; bir xil hisobni qayta ulash esa ruxsat etiladi. Bu hisob identifikatori va tegishli xabar-ID doirasini saqlab qoladi.

Ilova doimiy ish maydonlari sonini belgilamaydi. Har bir ish maydoni ulanishni monitoring qilish, media yuklab olish, qayta tekshirish va yangi suhbatlarni qabul qilish bo'yicha Collector vazifalarini umumiy Python jarayoni va voqea sikli ichida bajaradi. Ishlash tezligi yuklanishga bog'liq. Jarayonlarni izolyatsiya qilish uchun alohida o'rnatishlar, portlar va ma'lumotlar kataloglaridan foydalaning.

Har bir akkauntga uning kirish imkoniga ega bo'lgan manbalarni tayinlang. Turli akkauntlar bir xil guruhni kuzatishi mumkin, lekin ularning kuzatuvlari alohida bo'lib qoladi va kelib chiqishini saqlaydi. Operator nazoratidagi bir mashina ustidagi ikki akkaunt ikki mustaqil guvoh emas. **Eksport guruhi** alohida imzolangan ish maydoni ZIP-fayllarini ularning ish maydoni ID-lari, xeshlari va imzo kaliti barmoq izlarini o'z ichiga olgan imzolangan fayllar ro'yxati bilan birlashtiradi. Har bir jurnal o'z chegarasini saqlaydi. Ish yozuvlari yoki tahlil vositalarida manba havolalarini saqlagan holda birlashtirilgan kesma-ish maydoni vaqt chizig'ini yarating.

## Yozib olish va mansubligini aniqlash

Manbalar har bir akkaunt bo'yicha yangi xabarlar, tahrirlar, o'chirishlar, munosabatlar va a'zolik uchun alohida kalitlarni taqdim etadi. Oldindan sozlamalar barcha toifalarni yoki xabarlar/tahrirlar/o'chirishlarni saqlab qoladi. Ushbu siyosat ish maydonining tanlangan guruhlariga tatbiq etiladi, qayta ishga tushirishdan keyin ham saqlanadi va o'zgartirishlardan oldingi/keyingi imzolar bilan tasdiqlanadi. Standart sozlamalar barcha toifalarni saqlab qoladi. Kategoriyani o'chirish eski yozuvlarni olib tashlamaydi; uni qayta yoqish esa o'tkazib yuborilgan voqealarni tiklamaydi. Operativ yozuvlar, boshqa guruh xizmat voqealari va aniq tarix snapshotlari alohida hisoblanadi. Qayd etilgan Telegram obyektlari alohida yangilanish kalitlaridan qat'i nazar, ichiga o'rnatilgan metama'lumotlarni saqlab qolishi mumkin. Hozircha guruh bo'yicha kategoriyalarni ustuvor belgilash mavjud emas.

| Material | Hozir qayd etildi | Chegara |
| --- | --- | --- |
| Xabar | Matn, peer/xabar IDlari, jo'natuvchining metadata ma'lumotlari, javoblar va asl yangilanish konverti | Yig'uvchi tomonidan imzolangan va hisobga ko'rinadigan kuzatuv sifatida saqlangan |
| Tahrir | Yangi kuzatilgan versiya va ilgari saqlangan har qanday versiyalar | Vaqtinchalik to'xtash davrida oraliq tahrirlar yo'qolishi mumkin; jo'natuvchi har doim tahrirchi bo'lmasligi mumkin |
| O'chirish | Bildirishnoma va oldindan olingan kontent, agar mavjud bo'lsa | Odatda o'chiruvchi ma'lum emas yoki aniq harakat vaqti ko'rsatilmagan |
| Hisob darajasidagi o'chirish bildirishnomasi | Asl bildirishnoma; hal qilingan yozuvlar saqlangan suhbat va korrelyatsiya usulini o'z ichiga oladi | Doirada aniq bir marta oldin saqlangan shaxsiy suhbat yoki oddiy guruh mos kelishini talab qiladi; boshqa IDlar `deletion.unscoped` holatda qoladi. Kanal va superguruh IDlari ushbu korrelyatsiyadan mustasno. |
| Reaksiya | Yetkazilgan hisoblagichlar va ko'rinadigan yaqinda aniqlangan shaxslar | To'liq mavjud reaktorlar ro'yxati uchun alohida so'rovlar talab etiladi; kanallar shaxsiyatlarni yashirishi mumkin |
| A'zolik | Xizmat xabarlari va ishtirokchilarga yetkazilgan yangilanishlar | Ko'rinish roli va suhbat turiga bog'liq; yo'qolgan voqealar yo'qligini tasdiqlamaydi |
| Ma'mur harakatlari | Mavzuga oid yetkazilgan yangilanishlar va admin-log snapshoti kanal/superguruh chat eksportlarida | Eksport mavjud bo'lganda eksport qilayotgan admin akkauntining logini o'qiydi; admin-logni uzluksiz so'rov qilish ushbu yo'ldan tashqarida |
| Ilova | Asl versiya tavsifi, yuklab olingan baytlar/SHA-256 va urinish natijalari | Yo'qolgan fayl tiklanmasligi mumkin; eng so'nggi versiya o'rniga qo'yilmaydi |
| Tarix | Joriy ko'rinadigan xabarlarning aniq snapshoti | Barcha tahrirlar yoki o'chirilgan kontentni qayta tiklamaydi |
| Yig'uvchi jarayon | Boshlash/to'xtatish, yurak urishi, xatolar, sozlamalar, doira va imzolangan ijro kvitasi | Mahalliy inventarizatsiya; GitHub va TDX [mustaqil muhit tekshiruvlarini](https://phishdestroy.github.io/TgWitness/uz/docs/reference/evidence/#verification-scope) qo'shadi |

Interfeys manba hodisasida taqdim etilgan akkaunt nomini belgilaydi va kuzatilgan nomlar hamda foydalanuvchi nomlarini saqlaydi. Hodisa o'z ijrochisini ko'rsatmasa, hisobot bu maydonni aniqlanmagan holda qoldiradi.

## Sig'im va Telegram cheklovlari

Kafolatlangan sifat bilan kuzatib borilishi mumkin bo'lgan universal chatlar soni yo'q. Quvvat sekuntiga maksimal voqealar soni, ilovalar hajmi va o'lchamlari, qo'shimcha RPC-so'rovlar, faol hisoblar, disk kechikishi/bo'sh joy, tarmoq sharoitlari, Telegram cheklovlari, qabul qilinadigan kechikish va navbat chuqurligiga bog'liq.

Telegram passiv yetkazib berishni faol qisqa so'rovlardan ajratadi. Uning yangilanish hujjatlari ochiq kanallar/superguruhlar uchun qo'shimcha `updates.getChannelDifference` chaqiruvlarini tasvirlaydi va **bir vaqtning o'zida** eng ko'pi bilan **o'n ta qisqa so'rov qilingan manbalarni** tavsiya etadi. Bu o'n ta tanlangan guruh chegarasi yoki to'liqlik kafolati emas.

| Rejim | Maqsad | Holat |
| --- | --- | --- |
| Standart kuzatuv | Tanlangan manbalardan olingan yangilanishlarni qayd eting | Amalga oshirildi |
| Prioritetli qayta tekshiruvlar | Yulduzchali manbalar o'zlarining sozlanadigan intervallaridan foydalanadi va har bir chegaralangan qayta tekshirish bosqichida ustunlikka ega bo'ladi | Tarix va xabar so'rovlari bilan amalga oshirilgan |

Prioritet yulduzi ushbu qayta tekshiruvlarni nazorat qiladi. Qo'shimcha`updates.getChannelDifference` qisqa so'rovlari alohida foydalanuvchi rejimida taqdim etilmagan.

FloodWait-ni e'tiborsiz qoldirish yoki qo'shimcha hisoblardan chiziqli sig'imni taxmin qilish bilan istalgan yuqori chastotali so'rov yig'ish o'lchamlarini aniqlash uchun haqiqiy model emas. Standart cheklovlar – ro'yxatda keltirilgan birinchi 1 000 dialog, har bir tarix nusxasida 500 tagacha xabar. Har bir to'plangan fayl turi bo'yicha 1–2 000 MiB va siqilmagan imzolangan ZIP kontenti uchun 4 GiB; har biri **Parametrlar** bo'limidagi ish maydoni bo'yicha o'zgartiriladi. Eksportlarga voqealar soni bo'yicha aniq cheklov qo'yilmagan. Brauzer zaxira rejimi bo'yicha 128 MiB bilan cheklangan; oqimli CLI sozlanadigan uzatish chegarasiga ega, bo'yicha 5 GiB.

## Ishonchlilik va tiklash

Amaldagi xulq-atvorga SQLite WAL/sinkron tranzaktsiyalar; atomik xabar va media-topshiriq yozuvlari; doimiy topshiriqlar va qayta urinish kechikishlari; asl-versiya tavsiflagichlari; cheklangan qayta urinishlar; saqlangan media FloodWait; matn voqeasining tarmoq kutishidan tashqarida media yuklab olish; keyingi yozuvlar davom etarkan barqaror prefiksli eksport; atom sozlamalari va audit yozuvlari; muvaffaqiyatsiz almashtirishga kirishga urinishdan so'ng ishchi ruxsatnomani saqlash; zararlangan qo'shimcha ish maydonini izolyatsiya qilish; aniq qayta ulanish urinishlari; alohida ruxsatnoma yo'qotilishini xabar qilish; va monoton soat yordamida haqiqiy vaqt o'zgarishini aniqlash.

Hisob va kanal pts/qts/seq qayta ishga tushirilgandan so'ng saqlanadi va tiklanadi, kuzatilgan suhbatlar esa muntazam ravishda qayta tekshiriladi; [dalil formatiga](https://phishdestroy.github.io/TgWitness/uz/docs/reference/evidence/#durable-collection-and-process-receipts-02) qarang. Pozitsiyani muntazam saqlash jurnalni qabul qilishning atomli, yo'qotishsiz tasdig'i emas.

Har bir jarayon boshlanishi oldingi bosh sarlavha va tarmoqsiz chegarani qayd etadi. Joriy tarix bo'shliqlarni to'ldirish sifatida ko'rilmaydi. Telegramning farqlarni saqlash imkoniyati cheklangan; `differenceTooLong` yo'qolgan barcha kontentni qayta tiklay olmaydi. Qayta tiklanmaydigan bo'shliqlar keyingi tarixiy snapshot muvaffaqiyatli bo'lsa ham aniq ko'rsatilishi kerak.

## Dalil modeli

Har bir voqea ketma-ketlikni, mahalliy UTC kuzatuv vaqtini, manba vaqti (taqdim etilgan bo'lsa), turini, manbasini, ijrochisini (taqdim etilgan bo'lsa), asl yuklamani, oldingi xesh va imzoni qayd etadi. Xabar kuzatuvlari shuningdek yig'uvchi hisobini/ijro kontekstini saqlab qoladi.

Imzolangan jarayon kvitasi tasodifiy ishchi ID; TgWitness/Python/OS/qaramlik versiyalari; manba-fayl SHA-256 qiymatlari va umumiy barmoq izi; dastlabki hisob, doira va sozlamalar; UTC/monotonik o'qishlar; hamda avvalgi jurnal boshini o'z ichiga oladi. Sozlamalar o'zgarishlari, ishga tushirish/to'xtatish va xatoliklar bir xil jurnalga kiritiladi. Tekshiruv nuqtalari dastur ishga tushirilganda, kuzatuv davomida har besh daqiqada (o'zgartirilishi mumkin) va tartibli to'xtatishda saqlanadi. Saqlangan mahalliy tekshiruv nuqtasi avvalgi jurnal prefiksiga qaytishni aniqlay oladi.

| Mexanizm | U nimani tasdiqlaydi |
| --- | --- |
| Fayl SHA-256 | Baytlar ma'lum digestga mos keladi |
| Voqea xesh zanjiri | Ma'lum chegaraga nisbatan yozuvlarni tartibga solish/bog'lash |
| Ed25519 | Muayyan kalit ostidagi imzo |
| Mustaqil saqlangan tekshiruv nuqtasi | Keyingi material saqlangan chegaraga mos keladi |
| Proqram-fayl o'lchovi | O'lchangan fayllar bo'yicha Collector o'z-o'zini hisobot |
| Haqiqiy mustaqil TSA javobi | TSA vaqti bo'yicha aniq ishonch farazlari ostida ma'lum baytlarning mavjudligi |

RFC 3161 so'rovini tayyorlash va OpenSSL javobini tasdiqlash amalga oshirilgan. Dalil rejimi shuningdek tekshiruv nuqtasi xeshlarini sozlangan vaqt belgilash xizmatlariga yuboradi. Mustaqil vaqt nuqtasini o'rnatish uchun vakolatli organ javobini saqlab, tasdiqlang. Qarang: [TIMESTAMP.md](https://phishdestroy.github.io/TgWitness/uz/docs/reference/timestamp/).

Tekshiruv nuqtalarini mustaqil saqlang, imzolash kalitlariga kirishni nazorat qiling, uzatish yozuvlarini saqlang va eksportlarni ishonchli dasturiy ta'minot yordamida tasdiqlang. [Verifikatsiya doirasi](https://phishdestroy.github.io/TgWitness/uz/docs/reference/evidence/#verification-scope) bu tekshiruvlar bir-birini qanday to'ldirishini va qaysi ishonch taxminlari qo'llanilishini tushuntiradi.

## Eksport, joriy etish va topshirish

Imzolangan ZIP hujjat asl JSONL, CSV, HTML fayllarni, saqlangan ilovalarni, xeshlarni, imzolangan manifestni va qulay tekshiruvchi dasturni o'z ichiga oladi. U bitta ish maydonini va doimiy to'liq jurnal prefiksini qamrab oladi. Panel qidiruv filtrlari yozuvlarni sukut bo'yicha olib tashlamaydi. Maxfiy kalitlar, tokenlar va Telegram sessiyalari chiqarib tashlanadi; asl kuzatuvlar hanuz shaxsiy ma'lumotlar va Telegram metama'lumotlarini o'z ichiga olishi mumkin.

ZIP digestini, ishonchli barmoq izini, tekshiruv nuqtasini, jarayon kvitansiyasini va topshirish yozuvini alohida saqlang. Faoliyat kodiga faqat tekshirilgan ZIP-da mavjudligi sababli ishonish o'rniga, ishonchli o'rnatmadan olingan verifikatoridan foydalaning.

Brauzer interfeysi Node.js, CDN yoki tashqi shriftlarsiz mahalliy ravishda ishlaydi. O'rnatishni bitta operator tokeni boshqaradi. Masofaviy kirish uchun HTTPS yoki SSH tunneli talab etiladi. Python va konteyner ta'riflari taqdim etilgan, [deploy/](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md) ostida xizmat misollari keltirilgan; bajariladigan platforma tekshiruvlari alohida ro'yxatga olingan.

Standart ish maydoni ma'lumotlar ildiz papkasidan foydalanadi; qo'shimcha ish maydonchalari esa `profiles/<id>/` papkasidan foydalanadi. Zaxira nusxa olish to'xtatilgan jarayon va to'liq ma'lumot/kalit to'plamini talab qiladi. Dalil ZIP-fayllari ilova zaxira nusxalari emas. Sirlar yangi ma'lumotlar papkasi uchun tashqi bosh kalitdan foydalanishi mumkin; jurnal/media shifrlash operatorning disk/hajmi tomonidan ta'minlanadi. [CONNECTION-SECURITY.md](https://phishdestroy.github.io/TgWitness/uz/docs/reference/connection/) va [OPERATIONS.md](https://phishdestroy.github.io/TgWitness/uz/docs/reference/operations/) hujjatlariga qarang.

## Barqaror chiqarish mezonlari

Barqaror chiqarilishdan oldin, aniqlang:

1. Haqiqiy xususiy guruhlar, superguruhlar, forumlar va kanallar a'zo/admin rollari hamda yashirin/ko'rinadigan tarix bilan, jumladan kirish/2FA, bekor qilish va kirish huquqining yo'qolishi.
2. Boshqariladigan tahrirlar, o'chirishlar, munosabatlar, a'zolik va media ma'lum harakatlarga qarshi.
3. Protsess/server qulashi, disk nosozliklari/disk to'lishi, muddati o'tgan fayl havolalari, FloodWait, tarmoq uzilishi, shikastlangan fayllar va ma'lumotlar bazasini qayta tiklash.
4. O'lchangan kechikish, navbatlar, xotira va diskni hisobga olgan holda bir nechta akkauntni uzluksiz ishlatish, jim va shovqinli manbalarni birlashtirgan holda.
5. MTProto holatini yangilash va jurnalni qabul qilish orasidagi uzilish.
6. Mo'ljallangan OS/konteyner matritsasida toza o'rnatish va tasdiqlangan zaxira nusxasini tiklash.
7. Xavfsizlik, imzo va atributsiya/dalil da'volarining mustaqil ko'rib chiqilishi.

Panelga cheklangan kirish huquqi [Access and Permissions](https://phishdestroy.github.io/TgWitness/uz/docs/reference/access/) bo'limida tasvirlangan. 0.6-versiya [ACCOUNTS.md](https://phishdestroy.github.io/TgWitness/uz/docs/reference/accounts/) hujjatida keltirilgan chegaralangan yagona hisobli TData va hisob-fayl importini qo'llab-quvvatlaydi. Nashr etishdan oldin Telegram API shartlarini ko'rib chiqing. Tadqiqot manbalari va platforma topilmalari [RESEARCH.md](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/RESEARCH.md) hujjatida keltirilgan.
