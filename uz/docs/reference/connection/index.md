# Ulanish, proksi va ma'lumotlarni himoya qilish

Canonical page: https://phishdestroy.github.io/TgWitness/uz/docs/reference/connection/

Avtorizatsiya, avtomatik proksi havzalari, IP rejimlari, zaxira siyosati, tashqi so'rovlar va maxfiy saqlash.

Ushbu hujjat TgWitness 0.8.0 xatti-harakatlari va uning cheklovlarini tasvirlaydi. Avtorizatsiya, manbaga kirish, tarmoq ulanishi va yozib olish to'liqligi alohida holatlardir. Kirish bosqichlari, fayl formatlari va bir nechta hisoblar bo'yicha [hisoblar va sessiya formatlari](https://phishdestroy.github.io/TgWitness/uz/docs/reference/accounts/) bo'limidan boshlang. Hodisalar siyosati va qayta ishga tushirish xatti-harakatlari uchun [to'plash qanday ishlashini](https://phishdestroy.github.io/TgWitness/uz/docs/reference/collection/) ko'ring.

## Yo'naltirilgan ulanishni sozlash

**Ulanishida**ma'mur quyidagilarni tanlashi mumkin:**bu hisob****guruh hisobi**yoki**barcha hisoblar**, so'ngra yo'nalishni tanlaydi. **tanlovni ko'rib chiqish**ta'sirlangan hisoblarni ro'yxatlaydi. **tayyorlash va tekshirish**taklif qilingan yo'nalishni saqlanganini o'zgartirmay sinovdan o'tkazadi. **tekshirilgan ulanishni qo'llash**yana tekshiradi, zarur bo'lsa kuzatuvni to'xtatadi, yo'nalishni saqlaydi va allaqachon ishlayotgan kuzatuvni davom ettiradi. U ilgari faol bo'lmagan hisobda hech qachon ma'lumot yig'ishni boshlamaydi. Tarixni yuklab olish to'xtatilgan holda qoladi va alohida tiklanishi mumkin. O'tishdan oldin faol eksportlarni to'xtating.

Guruh o'zgarishlari hisoblarni standart bo'yicha o'z yo'nalishi bilan saqlaydi. Ko'rinish siz mo'ljallagan o'zgarishlarni ro'yxatlasa, faqat shunda ushbu opsiyani o'chiring. Ilova har bir hisobning natijasini alohida xabar qiladi; bu ma'lumotlar bazalari bo'ylab hamma narsani birdaniga o'zgartiradigan bitta tranzaksiya emas. Muvaffaqiyatsiz almashtirish hisobning oldingi sozlamalarini tiklaydi. Jarayonni qayta boshlashning muvaffaqiyatsizligi aniq ko'rsatiladi. Oldindan ko'rishlar o'n daqiqadan so'ng amal qilmay qoladi va ulanish sozlamalari yoki guruh a'zoligidagi o'zgarishlar yangi tekshiruvni talab qiladi.

| Yo'nalish | TgWitness nimani boshqaradi |
| --- | --- |
| To'g'ridan-to'g'ri | Mehmondan ulanishlar; tashqi mehmondan VPN aniqlanmaydi yoki majburiy qo'llanilmaydi. |
| VPN | Har bir hisob uchun bitta to'liq tunel WireGuard profili, mahalliy foydalanuvchi makonidagi SOCKS5 jarayoni tomonidan boshqariladi. Hech qanday host interfeysi yoki drayver o'rnatilmagan. |
| Mening proksim | SOCKS5, HTTP CONNECT yoki MTProxy ma'lumotlari. URL manzili SOCKS5/HTTP maydonlarini to'ldirishi mumkin. Bir nechta hisoblarni tanlash kiritilgan proksini bo'lishadi. |
| Ochiq MTProto | Mavjud pool Telegram yo'nalishlarini tayinlaydi. Tashqi so'rovlar ilg'or sozlamalarda alohida mos proksi sozlanmaguncha o'chirilgan. |
| WARP | Har bir tanlangan hisob uchun alohida mahalliy tunnel, WARP ro'yxatdan o'tkazilishi va o'sha hisobning omborida saqlangan WireGuard profili bilan. |

Joriy-yo'nalish tekshiruvi hisob sessiyasidan emas, balki yangi autentifikatsiyalanmagan Telegram transportidan foydalanadi. HTTP-ga mos yo'nalishlar uchun u shuningdek o'sha yo'nalish orqali Cloudflare'ning HTTPS izini so'raydi va uning xabar qilingan chiqish IP manzili, mamlakati, WARP holati va tekshirish vaqtini ko'rsatadi. O'lchangan kechikish — bu ICMP ping emas, balki Telegram ulanishni o'rnatish vaqti. Agar iz Warp faol ekanligini ko'rsatmasa, Warp tayyorlash muvaffaqiyatsiz tugaydi. Ushbu tekshiruvlar ulanishni o'rnatadi, lekin ushlangan xabarlarning haqiqiyligini yoki to'liqligini emas. Faqatgina ishlayotgan mahalliy jarayon muvaffaqiyatli chiqish tekshiruvi hisoblanmaydi.

### Ko'chma WARP va WireGuard

Bu [wgcf 2.3.1](https://github.com/ViRb3/wgcf/releases/tag/v2.3.1) va [wireproxy 1.1.3](https://github.com/windtf/wireproxy/releases/tag/v1.1.3) yordamida amalga oshirilgan **norasmiy WARP integratsiyasi**. Ma'mur birinchi yuklab olish yoki WARP ro'yxatdan o'tishdan oldin sozlamalarni aniq qabul qiladi. Ushbu sozlash ulanishlari to'g'ridan-to'g'ri GitHub va Cloudflare ga yo'naltiriladi va kompyuterning IP-manzilini oshkor qiladi. Oddiy hisob trafigi ilova o'rnatilgunga qadar mavjud marshrut bo'ylab harakatlanishni davom ettiradi. Cloudflare chiqish manzili va mamlakatni tanlaydi; alohida tunnellar chiqish manzilini bo'lishishi mumkin. Mamlakatni tanlash, davriy IP aylantirish va butun host bo'ylab VPN o'chirish funksiyasi ushbu xususiyat tomonidan taqdim etilmaydi.

Qo'llab-quvvatlanadigan yordamchi yuklab olishlar: Linux va macOS x86-64/ARM64, hamda Windows x86-64. Artifaktlar ko'rib chiqilgan manba kodiga ilova qilingan SHA-256 hashlariga solishtiriladi, va kechirilgan ijro etiladigan fayllar ishga tushirishdan oldin yana tekshiriladi. Yordamchi PATHga qo'shilmaydi, tizim xizmati sifatida o'rnatilmaydi yoki ommaviy tinglovchi berilmaydi. Barcha fayllar ish maydonining `portable-routes/` papkasi va shifrlangan seyf yozuvlari ostida saqlanadi. Loopback SOCKS5 tinglovchisi mustaqil ravishda yaratilgan kirish ma'lumotlarini talab qiladi.

Shaxsiy profillar va WARP hisob ma'lumotlari mavjud ish maydoni seyfida shifrlanadi. Ish jarayonida yordamchi faqat egasiga tegishli oddiy matnli konfiguratsiyani talab qiladi; u odatiy to'xtatishda olib tashlanadi. Host qulashi bu faylni egasiga tegishli ma'lumotlar papkada qoldirishi mumkin. Bu diskni shifrlamaydi va uning ma'muridan himoya qilmaydi. Nazoratchi panelning ota quvuri yo'qolsa, tunnelni yopadi. Muvaffaqiyatsiz tunnel hech qachon to'g'ridan-to'g'ri qaytishni yoqmaydi. Panelni qayta ishga tushirish tanlangan tunnelni tiklaydi; muvaffaqiyatsiz boshlanishlar cheklangan kechikish bilan qayta urinadi. **Stop tunnel** ham kuzatuvni to'xtatadi va to'xtagan holatni saqlaydi. **Start tunnel** tunnelni ishga tushiradi; tayyor bo'lganda kuzatuvni alohida tiklaydi.

Yuklangan WireGuard profillari bitta Interface va bitta Peer, to'liq IPv4 va IPv6 yo'nalishlari, shuningdek hech qanday hooklar, includes, muhit o'zgaruvchilari yoki qo'shimcha tinglovchilarni o'z ichiga olishi kerak. Jamoat endpoint manzillari ishga tushishdan oldin aniqlanib, mahkamlanadi. OpenVPN/IPsec va xususiy endpointlar uchun tashqi VPN yoki SOCKS5 darvozasidan foydalaning.

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

**Konvertlangan fayl shifrlanmagan akkauntga kirish siridir.** Uni himoyalangan saqlash joyida saqlang va hech qachon uni commit qilmang yoki uchinchi tomon konversiya xizmatiga yubormang. TgWitness ruxsat etilgan sessiyani o'zining shifrlangan omborida saqlaydi. Sessiyani nusxalash alohida ruxsatnoma yaratmaydi: klonlangan avtorizatsiya kalitlari bilan bir vaqtda bir nechta klientni ishga tushirmang va mustaqil yangilanish yetkazib berilishini kutmang.

Konversiya vakolatni o'tkazadi, asl xabarlarni, ob'ekt keshini yoki doimiy yangilanish kursorini emas. U jarayon qayta ishga tushirilganda yangilanishlarni tiklashni ta'minlamaydi.

## MTProto, Telethon va proksi-serverlar

MTProto – bu Telegramning protokoli. Telethon – bu TgWitness foydalanadigan Python klient kutubxonasi. MTProxy – bu Telegram transport proksi; SOCKS5 va HTTP CONNECT umumiy tunnelarni taqdim etadi. Hech biri akkaunt autentifikatsiyasini almashtirmaydi.

Har bir ish maydoni uchun yo'nalishni **Hisob → Sozlamalar → Ulanish sozlamalari → Ulanish yo'nalishini o'zgartirish** bo'limida imzolashdan oldin saqlang. Yangi ish maydonchalari standart bo'yicha **Avtomatik MTProxy · jamoat ro'yxatlari** bilan **manzilni yashirishni** tanlaydi. To'g'ridan-to'g'ri ulanishni aniq belgilagan mavjud ish maydonchalari esa bu imkoniyatni beruvchi rejimni saqlab qoladi.

## IP rejimlari

Yo'nalish ulanishni tanlaydi. Panelning Hisob bo'limidagi IP rejimi va **IP himoyasi** server manzili qachon oshkor bo'lishini belgilaydi. Ushbu boshqaruvlar VPN o'rnatmaydi yoki butun qurilma trafigini yo'naltirmaydi.

| Rejim | Telegram | Tashqi so'rovlar |
| --- | --- | --- |
| Manishani yashirish (`hide`) | Proxy ishlating; agar hech biri ishlamasa, kuting. To'g'ridan-to'g'ri zaxira yo'q. | SOCKS5/HTTP talab etiladi; tegishli proksi bo'lmagan so'rovlar rad etiladi. |
| Oxirgi chora sifatida to'g'ridan-to'g'ri (`fallback`) | Avtomatik MTProxy sozlangan kechikishdan so'ng Direct-dan foydalanishi mumkin, keyin ishchi proksiga qaytadi. | Sozlangan tashqi proksi yoki hisobning SOCKS5/HTTP yo'nalishini afzal ko'ring; aks holda To'g'ridan-to'g'ri (Direct) ruxsat etiladi. |
| Tunnel yoki VPN ortidagi server (`tunnel`) | To'g'ridan-to'g'ri yo'nalishlar va zaxira avtomatik havzaga darhol o'tishga ruxsat beriladi. | Mos proxy sozlanmagan taqdirda Direct ruxsat etiladi. |

Tunnel yoki VPN rejimi siz o'sha tarmoqni alohida boshqarishingizni taxmin qiladi. Ishlaydigan tunnel bo'lmasa, manzillar serverning o'z manzilini ko'rishi mumkin. Rejimni variant nomiga emas, balki haqiqiy tarmog'ingizga qarab tanlang.

### Yo'nalishni tanlang

| Yo'nalish | Sozlamalar | Chegara |
| --- | --- | --- |
| Avtomatik MTProxy | O'rnatilgan ro'yxatlar yoki operator katalogi | Ishlaydigan Telegram yo'nalishini saqlab turadi; to'g'ridan-to'g'ri zaxira IP rejimiga bog'liq |
| To'g'ridan-to'g'ri | Tunnel yoki VPN rejimi | Telethon mezbonning tarmoq yo'nalishidan foydalanadi |
| SOCKS5 | Host, port, ixtiyoriy foydalanuvchi nomi/parol | python-socks, masofaviy manzil DNS yoqilgan |
| HTTP CONNECT | Host, port, ixtiyoriy foydalanuvchi nomi/parol | Oddiy HTTP CONNECT; proksiga o'zi TLS qo'llab-quvvatlanmaydi |
| MTProxy | Mehmondo'st, port, sir | Eksperimental Telethon transporti; 32 geksaditsit yoki `dd` + 32 geksaditsit |

Fake TLS `ee` sirlarini rad etadi. Telethon 1.45 ning normallashtirishi prefiks va domenni olib tashlashi mumkin, lekin bu Fake TLS ni amalga oshirmaydi. `tg://proxy?server=…&port=…&secret=…` yoki `https://t.me/proxy?server=…&port=…&secret=…` ni joylashtiring va **havoladan Maydonlarni to'ldirishni** tanlang. Bu bog'lanish yoki saqlashsiz maydonlarni tasdiqlaydi va to'ldiradi; yo'nalishni alohida ko'rib chiqing va saqlang. Qo'lda to'ldiriladigan maydonlar mavjud bo'lib qoladi. [Telegram proksi havolalarini](https://core.telegram.org/api/links#proxy-links) ko'ring.

### Sizning o'rnatishingiz taqdim etgan ommaviy proksilar

Ichki ro'yxat to'rt manbani birlashtiradi: [SoliSpirit/mtproto](https://github.com/SoliSpirit/mtproto), [zakky8/mtproto-proxy-pro](https://github.com/zakky8/mtproto-proxy-pro), [kort0881/telegram-proxy-collector](https://github.com/kort0881/telegram-proxy-collector) va [3yed-61/MTP-Collector](https://github.com/3yed-61/MTP-Collector). Biriktirilgan snapshot oxir nuqta ma'lumotlari, manba aniqligi va yuklab olish sanalarini o'z ichiga oladi. Provayder ro'yxatga kiritilgani proksi ishlaydi yoki Telegramning har bir yangilanishini yetkazib beradi degan dalil emas.

**Avtomatik MTProxy** Telegram transport bog'lanishini tekshiradi, ishlayotgan proksini saqlaydi va u ishlamay qolganda boshqasiga o'tadi. Ish maydonchalari yetarli darajada ishlayotgan yozuvlar mavjud bo'lganda turli proksilardan foydalanishni afzal ko'radi; noyob chiqish manzili kafolatlanmaydi. Muvaffaqiyatsiz proxylar keyingi urinishdan oldin dam oladi. Agar hech biri ishlamasa, IP rejimi ma'lumotlarni yig'ishni kutish kerakligini yoki to'g'ridan-to'g'ri ulanish mumkinligini aniqlaydi. Proxylarni o'zgartirish akkauntni o'zgartirmaydi yoki uning jurnalini o'chirib tashlamaydi. Yo'nalish tanlovlari va o'zgarishlari imzolangan jurnalda qayd etiladi.

Avtomatik yo'nalishlar faol bo'lganda, ro'yxatlar soatiga bir marta yangilanadi va transport tekshiruvlari standart bo'yicha har o'n daqiqada bajariladi. Ushbu oraliklarni sozlash mumkin. **Jamoat ro'yxatlarini yangilash** so'rovi yangilanishni talab qiladi; ro'yxatni faqat ko'rish saqlangan qo'lda yo'nalishni o'zgartirmaydi.

**Telegram trafigi va HTTPS so'rovlari turli yo'llardan foydalanadi.** Ro'yxatni yuklab olish alohida HTTPS ulanish va taqdim etilgan external-request yo'lidan foydalanadi. `TGWITNESS_PROXY_FEED_PROXY` bu yo'lni HTTP/SOCKS5 proksi bilan aniq bekor qiladi; ikkala collector Compose varianti ham uni yo'naltiradi. Orqa fondagi pool asosiy ish maydonchasiga ergashadi. Telegram sessiyasi, API ma'lumotlari, panel tokeni yoki bot tokeni feed provayderlariga yuborilmaydi. Provayder nomlari, snapshot sanalari va yuklab olish yo'li **"Ro'yxat qayerdan olingan"** bo'limida ko'rsatiladi.

MTProxy faqat Telegram trafigini o'tkazadi. Ish maydoni HTTP amaliyotlari, masalan, vaqt tamg'alari, bildirishnomalar, masofaviy nusxalar va manba tekshiruvlari, sozlanganida alohida SOCKS5/HTTP proksidan, keyin hisobning SOCKS5/HTTP yo'nalishidan foydalanadi. Ikkalasiz, Hide the address so'rovni rad etadi; boshqa rejimlar Direct-ni ruxsat etadi. Tashqi so'rovlarni o'chirib qo'yish mumkin. Aniq sozlangan feed-download proksi alohida operator ustunligi bo'lib qoladi. Mustaqil guvoh xizmati o'z yo'lini saqlab qoladi.

Operator boshqariladigan xususiy xizmatlar uchun mavjud server muhit sozlamasi `TGWITNESS_ALLOW_PRIVATE_DESTINATIONS=1` xususiy manzillarni ruxsat etadi va proxy tomonidan host nomini aniqlashni saqlaydi. Uni panel orqali yoqib bo'lmaydi. Faqat ommaviy rejim `.onion` manzillarini ommaviy resolver so'ralmasidan oldin rad etadi; Tor onion xizmatlari aniq xususiy manzil sozlamasi va mos proxy talab qiladi. Ushbu DNS xatti-harakatlari Telegram transportiga emas, balki tashqi HTTP operatsiyalariga tegishli. Cloudflare [JSON DNS oxirgi](https://developers.cloudflare.com/1.1.1.1/encryption/dns-over-https/make-api-requests/dns-json/) nuqtasini hujjatlashtiradi.

****Avtomatik havza parametrlari**** **Parametrlar → Avtomatik MTProxy** bo'limida xato chegarasi, sovish vaqti, rejalashtirilgan rotatsiya, proksi ulashish va ruxsat etilgan zaxira kechikishini sozlang. | Nazorat | Bo'sh | | --- | --- | | Almashishdan oldin uzilishlar | 10 daqiqa ichida 3 marta | | Har bir ulanish urinishida sinab ko'riladigan proksi-lar | 3 | | Xato bo'lgandan keyingi birinchi / maksimal dam olish | 10 daqiqa / 6 soat | | Rejalashtirilgan aylantirish | O'chirilgan; xato bo'lganda yoqiladi | | Har bir proksi bo'yicha hisoblar | 0: alohida kirishlarni afzal ko'ring, kerak bo'lganda ulashing. Eksklyuziv kirishni kutish uchun 1 ni belgilang. | | Ruxsat etilgan to'g'ridan-to'g'ri zaxiraga qaytishdan oldingi kechikish | 10 daqiqa; Manzilni yashirish hanuzgacha to'g'ridan-to'g'ri ulanishni rad etadi | | Ma'lumot oqimini yangilash / transport tekshiruvlari | 60 / 10 daqiqa; asosiy ish maydoni qiymatlari umumiy zaxiraga ham tegishli | Turli proxy-serverlar turli chiqish manzillarini kafolatlamaydi. Ushbu sozlamalar Telegram limitlarini bekor qilmaydi yoki anonimlikni isbotlamaydi.

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
