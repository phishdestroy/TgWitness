# Ulanish, proksi va ma'lumotlarni himoya qilish

Canonical page: https://phishdestroy.github.io/TgWitness/uz/docs/reference/connection/

Avtorizatsiya, avtomatik proksi havzalari, IP rejimlari, zaxira siyosati, tashqi so'rovlar va maxfiy saqlash.

Ushbu hujjat TgWitness 0.7.0 xatti-harakatlari va uning cheklovlarini tasvirlaydi. Avtorizatsiya, manbaga kirish, tarmoq ulanishi va yozib olish to'liqligi alohida holatlardir. Kirish bosqichlari, fayl formatlari va bir nechta hisoblar bo'yicha [hisoblar va sessiya formatlari](https://phishdestroy.github.io/TgWitness/uz/docs/reference/accounts/) bo'limidan boshlang. Hodisalar siyosati va qayta ishga tushirish xatti-harakatlari uchun [to'plash qanday ishlashini](https://phishdestroy.github.io/TgWitness/uz/docs/reference/collection/) ko'ring.

## Avtorizatsiya usullari

**API ID va API xesh ilovani aniqlaydi; ular hisobga kirishni almashtirmaydi.** Ular TgWitness'da ixtiyoriydir. Uстунлик tartibi: avval formaga kiritilgan juftlik, keyin import qilingan hisob JSON'idan olingan juftlik, keyin ish maydonida saqlangan juftlik, so'ngra 50 ta juftlikdan iborat o'rnatilgan bazadan juftlik (2040) mos Telegram Desktop mijoz tavsifi bilan yuboriladi. [my.telegram.org](https://my.telegram.org) saytidagi API Development Tools bo'limidan olingan o'zingizning juftlikni barcha hisoblaringiz bilan ishlatishingiz mumkin; har bir hisobning alohida ruxsati saqlanadi.

| Uslub | Talablar | TgWitness qo'llab-quvvatlashi |
| --- | --- | --- |
| Telefon, kod, ixtiyoriy 2FA | Hisobga kirish; API juftligi ixtiyoriy | Panelga kirish |
| Auth kaliti HEX + DC ID | To'liq 512 belgili kalit va DC 1–5 | **Avtorizatsiya kaliti** yorlig'i; avtorizatsiya saqlanishidan oldin ixtiyoriy Foydalanuvchi ID tekshiriladi |
| Telethon StringSession | Amaldagi sessiya satri | Panelga kirish |
| Telethon SQLite `.session` | Yopiq, izchil nusxa | Sxemalarni 7/8 to'g'ridan-to'g'ri panel importi; ixtiyoriy oflayn CLI |
| Pyrogram SQLite `.session` | Yopiq ishlab chiqarish foydalanuvchi sessiyasi | Sxemalarni paneldan to'g'ridan-to'g'ri import qilish 2/3 |
| Telegram Desktop TData ZIP | Bir zamonaviy hisob; mahalliy parol bilan himoyalangan | Tekshirish summalari va dekripsiya tekshiruvlari bilan xotiradagi konvertatsiya |
| Hisob JSON | Qo'llab-quvvatlanadigan API/sessiya/kalit maydonlari | Faqatgina metadata API ma'lumotlarini to'ldiradi; sessiya/kalit yoki telefon/QR orqali kirish hanuzgacha talab etiladi |
| QR orqali kirish | Ruxsat berilgan Telegram ilovasidan tasdiq | Mahalliy QR kod yaratish, amal qilish muddati/qayta urinish, ixtiyoriy 2FA |
| TDLib / Pyrogram StringSession | Boshqa kutubxona-spetsifik formatlar | Qo'llab-quvvatlanmaydi |
| Bot tokeni | O'zining kirish/yangilash modeliga ega bot | Ushbu to'plovchi tomonidan ishlatilmagan |

Telegram kod yetkazib berishni tanlaydi; SMS kafolatlanmaydi. API xesh bekor qilingan sessiyani tiklay olmaydi yoki unutib qo'yilgan 2FA parolini almashtira olmaydi. TgWitness kirish kodlarini yoki Telegram 2FA parolini diskka saqlamaydi.

Shaxsiy manba uchun hisob allaqachon kirish huquqiga ega bo'lishi kerak. Guruh foydalanuvchi nomi keraksiz. Proksi yoki sessiya importi na a'zolik, na administrator huquqlarini bermaydi. Joriy a'zolik oldingi a'zolik tarixiga kirishni kafolatlamaydi.

## Telethon sessiya faylini import qiling

Telethon SQLite, Pyrogram SQLite va Telegram Desktop TData turli formatlardan foydalanadi. Panel qo'llab-quvvatlanadigan tuzilmalarni aniqlaydi va konvertatsiya qiladi; fayl nomini o'zgartirish konvertatsiya hisoblanmaydi. **Fayllar** bo'limida bir sessiyani va uning hamrohi JSON-ni tanlang, so'ngra **"Hisobni bog'lash"** tugmasini bosing. To'rtta mos keladigan fayl va jami 8 MiB gacha qabul qilinadi. TData/JSON tafsilotlari uchun [format cheklovlariga](https://phishdestroy.github.io/TgWitness/uz/docs/reference/accounts/) qarang. Parolni tiklash imkoni yo'q. Telefon/2FA yoki QR orqali kirish alohida ruxsatnoma yaratadi.

Ixtiyoriy Telethon-ga xos buyruq qatori yo'li ham mavjud bo'lib qoladi:

1. Asl sessiyani ishlatayotgan mijozni to'xtating va izchil nusxa yarating. Konverter yakunlanmagan WAL/jurnalga ega fayllarni rad etadi. Ushbu tekshiruvni chetlab o'tish uchun fayllarni o'chirish o'rniga asl mijozni to'g'ri yoping.
2. TgWitness muhitidan quyidagini ishga tushiring:

```
python -m tgwitness.sessions account.session --out account.tgwitness-session
```

1. **Hisob qo'shish → Fayllar** bo'limida natijani yuklang yoki uning satrini joylang va davom eting.
2. Ko'rsatilgan raqamli akkaunt IDni tekshiring, manbalarni tanlang va kuzatuvni boshlang.

Konverter SQLite'ni faqat o'qish rejimida ochadi, sxema yangilanishi yoki tarmoq so'rovini bajarmaydi va sessiyani chop etmaydi. U sxema versiyasini, jadvallar turini, bitta sessiya qatorini, IP/port/DC va kalit uzunligini tekshiradi. CLI kiritilishi 64 MiB bilan cheklangan; StringSession matni 4 KiB bilan cheklangan. Panel konversiyasi fayllarni autentifikatsiyalangan TgWitness serveriga yuklaydi, ularni xotirada qayta ishlaydi va yuklangan asl nusxalarni saqlamasdan, normalizatsiya qilingan ma'lumotlarni shu brauzerga qaytaradi. Masofaviy server uchun HTTPS dan foydalaning.

**Konvertlangan fayl shifrlanmagan akkauntga kirish siridir.** Uni himoyalangan saqlash joyida saqlang va hech qachon uni commit qilmang yoki uchinchi tomon konversiya xizmatiga yubormang. TgWitness ruxsat etilgan sessiyani o'zining shifrlangan omborida saqlaydi. Sessiyani nusxalash alohida ruxsatnoma yaratmaydi: klonlangan avtorizatsiya kalitlari bilan bir vaqtda bir nechta klientni ishga tushirmang va mustaqil yangilanish yetkazib berilishini kutmang.

Konversiya vakolatni o'tkazadi, asl xabarlarni, ob'ekt keshini yoki doimiy yangilanish kursorini emas. U jarayon qayta ishga tushirilganda yangilanishlarni tiklashni ta'minlamaydi.

## MTProto, Telethon va proksi-serverlar

MTProto – bu Telegramning protokoli. Telethon – bu TgWitness foydalanadigan Python klient kutubxonasi. MTProxy – bu Telegram transport proksi; SOCKS5 va HTTP CONNECT umumiy tunnelarni taqdim etadi. Hech biri akkaunt autentifikatsiyasini almashtirmaydi.

**Hisob → Sozlamalar → Ulanish sozlamalari → Ulanish yo'nalishini o'zgartirish** bo'limida har bir ish maydoni uchun yo'nalishni saqlang va tizimga kirishdan oldin sozlang. Yangi ish maydonchalari standart bo'yicha IP-ni yashirish xususiyatiga ega **avtomatik MTProxy · ommaviy ro'yxatlar** rejimida yaratiladi. To'g'ridan-to'g'ri ulanishni aniq belgilagan mavjud ish maydonchalari esa bu imkoniyatni beruvchi rejimni saqlab qoladi.

## IP rejimlari

Yo'nalish ulanishni tanlaydi. IP rejimi server manzili qachon oshkor bo'lishini belgilaydi. Ushbu boshqaruvlar VPN o'rnatmaydi va barcha qurilma trafigini yo'naltirmaydi.

| Rejim | Telegram | Tashqi so'rovlar |
| --- | --- | --- |
| IPni yashirish (`hide`) | Proxy ishlating; agar hech biri ishlamasa, kuting. To'g'ridan-to'g'ri zaxira yo'q. | SOCKS5/HTTP talab etiladi; tegishli proksi bo'lmagan so'rovlar rad etiladi. |
| Zaxira variantini ruxsat eting (`fallback`) | Avtomatik MTProxy sozlangan kechikishdan so'ng Direct-dan foydalanishi mumkin, keyin ishchi proksiga qaytadi. | Sozlangan tashqi proksi yoki hisobning SOCKS5/HTTP yo'nalishini afzal ko'ring; aks holda To'g'ridan-to'g'ri (Direct) ruxsat etiladi. |
| Tunnel / VPN (`tunnel`) | To'g'ridan-to'g'ri yo'nalishlar va zaxira avtomatik havzaga darhol o'tishga ruxsat beriladi. | Mos proxy sozlanmagan taqdirda Direct ruxsat etiladi. |

Tunnel/VPN rejimi siz o'sha tarmoqni alohida boshqarishingizni taxmin qiladi. Ishlaydigan tunnel bo'lmasa, manzillar serverning o'z manzilini ko'rishi mumkin. Rejimni variant nomiga emas, balki haqiqiy tarmog'ingizga qarab tanlang.

### Yo'nalishni tanlang

| Yo'nalish | Sozlamalar | Chegara |
| --- | --- | --- |
| Avtomatik MTProxy | O'rnatilgan ro'yxatlar yoki operator katalogi | Ishlaydigan Telegram yo'nalishini saqlab turadi; to'g'ridan-to'g'ri zaxira IP rejimiga bog'liq |
| To'g'ridan-to'g'ri | Tunnel/VPN rejimi | Telethon mezbonning tarmoq yo'nalishidan foydalanadi |
| SOCKS5 | Host, port, ixtiyoriy foydalanuvchi nomi/parol | python-socks, masofaviy manzil DNS yoqilgan |
| HTTP CONNECT | Host, port, ixtiyoriy foydalanuvchi nomi/parol | Oddiy HTTP CONNECT; proksiga o'zi TLS qo'llab-quvvatlanmaydi |
| MTProxy | Mehmondo'st, port, sir | Eksperimental Telethon transporti; 32 geksaditsit yoki `dd` + 32 geksaditsit |

Fake TLS `ee` sirlarini rad etadi. Telethon 1.45 ning normallashtirishi prefiks va domenni olib tashlashi mumkin, lekin bu Fake TLS ni amalga oshirmaydi. `tg://proxy?server=…&port=…&secret=…` yoki `https://t.me/proxy?server=…&port=…&secret=…` ni joylashtiring va **havoladan Maydonlarni to'ldirishni** tanlang. Bu bog'lanish yoki saqlashsiz maydonlarni tasdiqlaydi va to'ldiradi; yo'nalishni alohida ko'rib chiqing va saqlang. Qo'lda to'ldiriladigan maydonlar mavjud bo'lib qoladi. [Telegram proksi havolalarini](https://core.telegram.org/api/links#proxy-links) ko'ring.

### Sizning o'rnatishingiz taqdim etgan ommaviy proksilar

Ichki ro'yxat to'rt manbani birlashtiradi: [SoliSpirit/mtproto](https://github.com/SoliSpirit/mtproto), [zakky8/mtproto-proxy-pro](https://github.com/zakky8/mtproto-proxy-pro), [kort0881/telegram-proxy-collector](https://github.com/kort0881/telegram-proxy-collector) va [3yed-61/MTP-Collector](https://github.com/3yed-61/MTP-Collector). Biriktirilgan snapshot oxir nuqta ma'lumotlari, manba aniqligi va yuklab olish sanalarini o'z ichiga oladi. Provayder ro'yxatga kiritilgani proksi ishlaydi yoki Telegramning har bir yangilanishini yetkazib beradi degan dalil emas.

**Avtomatik MTProxy** Telegram transport bog'lanishini tekshiradi, ishlayotgan proksini saqlaydi va u ishlamay qolganda boshqasiga o'tadi. Ish maydonchalari yetarli darajada ishlayotgan yozuvlar mavjud bo'lganda turli proksilardan foydalanishni afzal ko'radi; noyob chiqish manzili kafolatlanmaydi. Muvaffaqiyatsiz proxylar keyingi urinishdan oldin dam oladi. Agar hech biri ishlamasa, IP rejimi ma'lumotlarni yig'ishni kutish kerakligini yoki to'g'ridan-to'g'ri ulanish mumkinligini aniqlaydi. Proxylarni o'zgartirish akkauntni o'zgartirmaydi yoki uning jurnalini o'chirib tashlamaydi. Yo'nalish tanlovlari va o'zgarishlari imzolangan jurnalda qayd etiladi.

Avtomatik yo'nalishlar faol bo'lganda, ro'yxatlar soatiga bir marta yangilanadi va transport tekshiruvlari standart bo'yicha har o'n daqiqada bajariladi. Ushbu oraliklarni sozlash mumkin. **Jamoat ro'yxatlarini yangilash** so'rovi yangilanishni talab qiladi; ro'yxatni faqat ko'rish saqlangan qo'lda yo'nalishni o'zgartirmaydi.

Har bir feed javobi sakkiz soniyalik so'rov timeouti va 20 soniyalik umumiy yuklab olish muddati bilan 1 MiB bilan cheklangan; yo'naltirishlar rad etiladi. Manba bo'yicha 64 tagacha mos yozuv saqlanadi va takrorlari olib tashlanadi. Parser qo'llab-quvvatlanadigan hexadecimal va base64url sirlar hamda JSON feedni qabul qiladi. Soxta TLS `ee`, noto'g'ri havolalar, xususiy/zaxira IP-manzillar va mahalliy hostnomalar e'tiborsiz qoldiriladi. Hostnomalar foydalanishdan oldin aniqlanib tekshiriladi va tanlangan IP-manzil o'sha ulanish uchun mahkamlanadi. Avtomatik qayta olish hostnomani yana aniqlaydi; uni yana aniqlash uchun qo'lda kiritishni qayta qo'llang.

Muvaffaqiyatsiz, bo'sh yoki mos kelmaydigan feed javoblari oldingi manba snapshotini saqlab qoladi. Yangilanishlar atomik, ketma-ketlashtirilgan va har bir ish maydoni bo'yicha daqiqasiga bitta urinish bilan cheklangan. Muvaffaqiyatli transport probe ulanishni o'rnatadi, anonimlikni yoki to'liqlikni emas.

**Telegram trafigi va HTTPS so'rovlari turli yo'llardan foydalanadi.** Ro'yxatni yuklab olish alohida HTTPS ulanish va taqdim etilgan external-request yo'lidan foydalanadi. `TGWITNESS_PROXY_FEED_PROXY` bu yo'lni HTTP/SOCKS5 proksi bilan aniq bekor qiladi; ikkala collector Compose varianti ham uni yo'naltiradi. Orqa fondagi pool asosiy ish maydonchasiga ergashadi. Telegram sessiyasi, API ma'lumotlari, panel tokeni yoki bot tokeni feed provayderlariga yuborilmaydi. Provayder nomlari, snapshot sanalari va yuklab olish yo'li **"Ro'yxat qayerdan olingan"** bo'limida ko'rsatiladi.

MTProxy faqat Telegram trafigini o'tkazadi. Ish maydoni HTTP operatsiyalari, masalan, vaqt tamg'alari, bildirishnomalar, masofaviy nusxalar va manba tekshiruvlari, sozlangan taqdirda alohida SOCKS5/HTTP proksidan, keyin hisobning SOCKS5/HTTP yo'nalishidan foydalanadi. Ularsiz Hide IP so'rovni rad etadi; boshqa rejimlar Direct-ni ruxsat etadi. Tashqi so'rovlar o'chirib qo'yilishi mumkin. Aniq sozlangan feed-download proksi alohida operator ustunligi bo'lib qoladi. Mustaqil guvoh xizmati o'z yo'nalishini saqlab qoladi.

****Avtomatik havza parametrlari**** **Parametrlar → Avtomatik MTProxy** bo'limida xato chegarasi, sovish muddati, rejalashtirilgan aylanish, proxy ulashish va ruxsat etilgan zaxira kechikishini sozlang. | Nazorat | Standart | | --- | --- | | Almashishdan oldin uzilishlar | 10 daqiqa ichida 3 marta | | Ulanish urinishida sinab ko'riladigan proxylar | 3 | | Xato bo'lgandan keyingi birinchi / maksimal tanaffus | 10 daqiqa / 6 soat | | Rejalashtirilgan rotatsiya | O'chirilgan; xato bo'lganda yoqish | | Har bir proksi bo'yicha hisoblar | 0: alohida kirishlarni afzal ko'ring, kerak bo'lganda ulashing. Eksklyuziv kirishni kutish uchun 1 ni belgilang. | | Ruxsat etilgan to'g'ridan-to'g'ri zaxiraga qaytishdan oldingi kechikish | 10 daqiqa; IP-ni yashirish hanuzgacha to'g'ridan-to'g'ri ulanishni rad etadi | | Feed yangilanishi / transport tekshiruvlari | 60 / 10 daqiqa; asosiy ish maydoni qiymatlari umumiy havzaga tatbiq etiladi | Turli proksi-serverlar turli chiqish manzillarini kafolatlamaydi. Ushbu sozlamalar Telegram limitlarini bekor qilmaydi yoki anonimlikni isbotlamaydi.

Ommaviy ro'yxatni o'zingizning operator katalogingiz bilan almashtirish uchun quyidagi ustunlikni sozlang. Bu tashqi obunalarni butunlay o'chirib qo'yadi, hatto uning `proxies` massivida hech narsa bo'lmaganida ham.

[Bo'sh katalogni](https://github.com/phishdestroy/TgWitness/blob/main/deploy/proxies.config.example) `proxy-config/proxies.json` ga nusxalang va joylashtirilgan ommaviy endpointlaringizni qo'shing:

```
{"format": "tgwitness-proxy-catalog-v1", "proxies": [
  {"id": "project-eu", "label": "Project EU",
   "link": "tg://proxy?server=REPLACE_HOST&port=443&secret=REPLACE_SECRET"}
]}
```

Namuna qiymatlari almashtirilishi kerak. 32 tagacha alohida yozuv qabul qilinadi. Avtorizatsiyalangan ro'yxat sirli ma'lumotlarsiz labelar/mehmonlar/portlarni qaytaradi; birini tanlash uning kreditsialarini ish maydoni seyfiga saqlaydi. Mavjudlik aniq transport testi o'tkazilmaguncha sinovdan o'tmagan hisoblanadi. Noto'g'ri tuzilgan katalog qo'lda sozlashni talab qiladi.

Mahalliy ishga tushirish: `TGWITNESS_PROXY_CATALOG` ni mahalliy JSON yo'liga o'rnating. Docker:

```
docker compose -f compose.yaml -f deploy/compose/compose.proxies.yaml up -d --build
```

Qo'shimcha qatlam faqat o'qish uchun`proxy-config`ni o'rnatadi; fayllar konteyner UID 10001 tomonidan o'qilishi kerak. Ushbu papka Git, Docker build konteksti va manba arxivlaridan chiqarib tashlangan. Ushbu katalog ma'lumotlarni yig'uvchi akkauntlarni sozlaydi; [TgWitness boti](https://phishdestroy.github.io/TgWitness/uz/docs/reference/witness/) MTProxy emas, balki o'zining HTTP/SOCKS5 marshrutidan foydalanadi.

To'g'ridan-to'g'ri zaxira yuqoridagi IP rejimiga binoan boshqariladi. Yo'nalishni o'zgartirishdan oldin kuzatuvni to'xtating. Saqlash eski mijozlarni uzib qo'yadi va yakunlanmagan tizimga kirishni bekor qiladi; yangi mijoz saqlangan yo'nalishdan foydalanadi. Hisobning jurnal/sessiya bog'lanishi saqlanib qoladi. Sozlamalar avvalgi yo'nalishni almashtiradi: uni tahrirlashda proksi ma'lumotlarini qayta kiriting.

Kirish ma'lumotlari `network.enc`da shifrlangan. API foydalanuvchi nomi, parol yoki sirli kalitni qaytarmaydi. Imzolangan yozuvlarda yo'nalish turi va kirish ma'lumotlari mavjudligi ko'rsatiladi, manzil va sirli kalitlar kiritilmaydi. Operator paneldagi manzilni ko'rishi mumkin. Sirli maydonlar saqlash, qulflash yoki ish maydonlarini almashtirishdan so'ng tozalanadi.

**Telegram ulanishini sinab ko'radi**, shuningdek tizimga kirishdan oldin ham mavjud bo'lib, yo'nalish orqali vaqtinchalik ruxsatsiz Telegram ulanishini ochadi va yopadi. U IP-tekshiruv saytiga murojaat qilmaydi. Muvaffaqiyat transport ulanishini o'rnatadi, guruhga kirish, to'liq yetkazib berish yoki anonimlikni emas.

Proxy Telegram klientining ulanishlariga, jumladan Telegram DC media yuklamalariga qo'llaniladi. Brauzer, pip, SSH va qo'lda ishga tushirilgan TSA vositalarining alohida yo'llari mavjud. Proxy host nomi mahalliy tarzda aniqlanishi mumkin. `rdns` manzil host nomlariga ta'sir qiladi; Telegram ko'pincha raqamli DC IP-manzillarini taqdim etadi.

SOCKS5 va oddiy HTTP CONNECT proxy ma'lumotlarini yoki mijozdan proxyga bo'lgan tunnelni shifrlamaydi. MTProto Telegram trafigini alohida himoya qiladi. Ishonchsiz tarmoqdagi proksiga mos keladigan xavfsiz kanalni ishlating. Xususiy guruhlar bulutli suhbatlardir; MTProto ularni oxirigacha shifrlangan Sirli Suhbatlarga aylantirmaydi.

## Shifrlash va imzo

| Qatlam | Amalga oshirildi | Operator mas'uliyati |
| --- | --- | --- |
| Telegram trafigi | Telethon MTProto | Platforma ishonchliligi, yo'nalish va mavjudlik |
| Veb-panel | Ega tokeni, loopback bo'yicha standart, so'rovlarga cheklovlar | Masofaviy kirish uchun HTTPS yoki SSH tunneli |
| Sirlar | API akkount ma'lumotlari, sessiya, proksi akkount ma'lumotlari va imzolash uchun xususiy kalit uchun Fernet | Dekripsiya kalitini va ishchi hostni himoya qiling |
| Ombor kaliti | Mahalliy kalit yoki yangi o'rnatish uchun tashqi bosh kalit | Maxsus himoyalangan saqlash va kalit zaxira |
| Xabarlar va ilovalar | Oddiy matnli ilova saqlash | Shifrlangan disk/hajm |
| ZIP/JSONL/CSV/HTML | Butunlik tekshiruvlari, kontentni shifrlash yo'q | Eksport qilingan nusxalar va uzatmalarni himoya qiling |
| Manba va vaqt | Imzolangan jurnal, jarayon kviti, RFC 3161 vositalari | Ishonchli kalit, mustaqil tekshiruv punktlari/TSA va saqlash tartibi |

Hisobdagi **saqlash himoyasi** ushbu holatlarni ko'rsatadi. Panel tokeni shifrlash paroli emas, balki kirish siridir. U administratorga kirish huquqini beradi; [chiqarilgan tokenlar](https://phishdestroy.github.io/TgWitness/uz/docs/reference/access/) hisoblar va suhbatlar bo'yicha chegaralangan bo'lishi mumkin. Ish maydonchalari host jarayonini baham ko'radi va alohida izolyatsiyalangan tenantlar emas.

Ochiq-oydin boshlangan, izolyatsiyalangan sintetik demo to'g'ridan-to'g'ri loopback ulanishi orqali avtomatik ravishda ochilishi mumkin. Bu alohida jarayon umr-muddati imkoniyatidan foydalanadi; u sozlangan panel tokenini oshkor qilmaydi va haqiqiy ish maydonlariga kirish huquqini bermaydi. Masofaviy, proksi orqali yoki cross-origin so'rovlar ushbu avtomatik kirish imkoniyatini ololmaydi yoki undan foydalana olmaydi. Bu qulaylik haqiqiy hisob ma'lumotlari uchun autentifikatsiya chegarasini olib tashlamaydi.

BitLocker, LUKS, FileVault yoki boshqariladigan shifrlangan hajm tegishli tahdid modellariga muvofiq saqlashni himoya qilishi mumkin. Yechilmagan holda ishlayotgan mashinaning ma'murchisi hanuzgacha ma'lumotlarni o'qishi mumkin. Saqlash rejalashtirishda SQLite WAL/SHM, media, vaqtinchalik eksportlar, swap, zaxira nusxalar va brauzer yuklamalarini hisobga oling. Docker hajmi faqatgina hajm bo'lgani uchun shifrlanmaydi. TgWitness SQLCipher yoki obyekt shifrlashni amalga oshirmaydi.

## Tashqi bosh kalit

**Yangi** o'rnatish uchun master kalitni ma'lumotlar katalogidan tashqariga joylashtiring. Bu mavjud mahalliy kalit omborini avtomatik ko'chirib o'tkazmaydi. Faqat xizmat identifikatori kirish huquqiga ega bo'lgan kalit katalogini tayyorlang, so'ngra quyidagi buyruqni ijro eting:

```
python -m tgwitness.security create-master-key /private/keys/tgwitness-master.key
export TGWITNESS_VAULT_KEY_FILE=/private/keys/tgwitness-master.key
python -m tgwitness --data-dir /private/observations/new-case
```

PowerShell, o'rnatilgan loyiha muhitidan foydalangan holda:

```
python -m tgwitness.security create-master-key E:\PrivateKeys\tgwitness-master.key
$env:TGWITNESS_VAULT_KEY_FILE = 'E:\PrivateKeys\tgwitness-master.key'
python -m tgwitness --data-dir E:\PrivateData\new-case
```

Docker'da faylni `/data` tashqarisida faqat o'qish uchun (read-only) joylashtiring, masalan `/run/secrets/tgwitness-master.key` ga, va muhit o'zgaruvchisini shu yo'lga o'rnating. Xizmatning UID'si uni o'qiy olishi kerak. Yo'lni, kalit baytlarni emas, muhit/sozlash fayllari orqali uzating.

Har bir ish maydoni tasodifiy ommaviy salt va HKDF-SHA256 orqali hosil qilingan o'zining Fernet kalitini oladi. `vault.external.json` derivatsiya metama'lumotlarini saqlaydi, asosiy kalitni emas. Kalit yo'qolgan yoki noto'g'ri bo'lsa, u jimjit almashtirmasdan ishga tushishni rad etadi. Tiklash uchun ham salt metama'lumotlarini, ham asosiy kalitni saqlang.

Barcha ish maydonchalari bitta asosiy kalitdan kelib chiqadi; uning buzilishi butun o'rnatishga ta'sir qiladi. Ish jarayoni sirlarni dekript qila oladi. Bu HSM yoki parol KDF emas. Tasodifiy kalit o'rniga ixtiyoriy inson parollari qabul qilinmaydi.

Mavjud o'rnatmalarda maqsadli migratsiya amalga oshirilib, tekshirilguncha joriy kalitni saqlang. `vault.key`ni o'chirish yoki bosh kalitni almashtirish sessiyalarga/imzolash kalitlariga kirishni yo'qotishiga olib kelishi mumkin. Shifrlangan zaxira nusxalar va kalitlarni alohida saqlang hamda tiklashni izolyatsiyalangan muhitda sinab ko'ring.

## Manbalar va tekshiruv doirasi

2026-yil 26-oktabrda ko'rib chiqilgan:

- https://core.telegram.org/api/auth
- https://core.telegram.org/api/obtaining_api_id
- https://docs.telethon.dev/en/stable/basic/signing-in.html
- https://docs.telethon.dev/en/stable/concepts/sessions.html
- https://core.telegram.org/mtproto/mtproto-transports
- https://github.com/telegramdesktop/tdesktop/blob/dev/Telegram/SourceFiles/storage/storage_account.cpp
- Telethon 1.45.0: SQLiteSession, StringSession, String`Connection._proxy_connect`, String `TcpMTProxy.normalize_secret` va yuklab olish usullari.

Mahalliy testlar loopback SOCKS5/HTTP CONNECT ulanishlari, sun'iy SQLite sessiyalari, yo'nalish izolyatsiyasi, maxfiy istisno va kalit yo'qligi rad etilishini qamrab oladi. Ular haqiqiy Telegram/proxy o'zaro mosligini yoki jonli MTProxy xulq-atvorini ta'minlamaydi. [VERIFICATION.md](https://phishdestroy.github.io/TgWitness/uz/docs/reference/verification/) va [LIVE_ACCEPTANCE.md](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md) hujjatlariga qarang.
