# Hisoblar va sessiya formatlari

Canonical page: https://phishdestroy.github.io/TgWitness/uz/docs/reference/accounts/

Telefon, QR kod yoki avtorizatsiya kaliti orqali tizimga kiring, Telethon, Pyrogram yoki Telegram Desktop sessiyalarini import qiling va bir nechta akkauntlarni boshqaring.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Hujjatlash](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Boshlash](https://phishdestroy.github.io/TgWitness/uz/docs/reference/quickstart/)

![Boshlash](https://phishdestroy.github.io/TgWitness/assets/chapter-start.svg)

TgWitness **Telegram foydalanuvchi**hisobiga (bot emas) MTProto orqali Telethon yordamida kiradi. Har bir hisob o'zining alohida **ish** maydonida (API va buyruq qatori vositalarida "*workspace*" deb ataladi) joylashadi, o'z sessiyasi, manbalari, jurnali va imzolash kalitiga ega.

Sessiya fayllari, sessiya satrlari va Auth kalitlari **hisob ma'lumotlari ruxsatnomalaridir**: ularni egallagan har kim o'sha hisob sifatida harakat qilishi mumkin. Ular xabarlar tarixini o'z ichiga olmaydi.

> [!OGOHLANTIRISH] **Yo'qotishga qodir bo'lmagan narsani ishlatmang.** Shaxsiy yoki boshqa qimmatli hisoblarni ulashni va qadrlaydigan hisobingizda API ID / API xesh yaratishni qat'iyan tavsiya qilmaymiz. Bu TgWitness sinovdan o'tmaganligi haqida emas: Telegram hisoblarni oldindan aytib bo'lmaydigan tarzda cheklaydi va doimiy ravishda taqiqlaydi — u ortiqcha deb hisoblaydigan so'rov hajmlari uchun, mijoz yoki maqsadga qaramasdan, yetarli hujjatlashtirishsiz. Ko'plab taqiqlar qaytarib bo'lmaydi. Maxsus hisoblardan foydalaning. Sinovlarning muammosiz o'tishi Telegramga bog'liq, dasturiy ta'minotga emas, va keyinchalik hech narsani kafolatlamaydi.

- [Bir qarashda](https://phishdestroy.github.io/TgWitness/uz/docs/reference/accounts/#at-a-glance)
- [Boshlashdan oldin: API ID va API xesh](https://phishdestroy.github.io/TgWitness/uz/docs/reference/accounts/#before-you-start-api-id-and-api-hash)
- [Telefon raqami](https://phishdestroy.github.io/TgWitness/uz/docs/reference/accounts/#phone-number) · [QR kod](https://phishdestroy.github.io/TgWitness/uz/docs/reference/accounts/#qr-code) · [Auth kaliti + DC identifikatori](https://phishdestroy.github.io/TgWitness/uz/docs/reference/accounts/#auth-key--dc-id)
- [Hisob fayllari](https://phishdestroy.github.io/TgWitness/uz/docs/reference/accounts/#account-files): [Telethon .session](https://phishdestroy.github.io/TgWitness/uz/docs/reference/accounts/#telethon-session) · [Pyrogram .session](https://phishdestroy.github.io/TgWitness/uz/docs/reference/accounts/#pyrogram-session) · [Sessiya + JSON juftligi](https://phishdestroy.github.io/TgWitness/uz/docs/reference/accounts/#session--json-pair) · [TData](https://phishdestroy.github.io/TgWitness/uz/docs/reference/accounts/#telegram-desktop-tdata) · [StringSession](https://phishdestroy.github.io/TgWitness/uz/docs/reference/accounts/#telethon-stringsession) · [Hisob JSON](https://phishdestroy.github.io/TgWitness/uz/docs/reference/accounts/#account-json)
- [Nimangiz borligini aniqlang](https://phishdestroy.github.io/TgWitness/uz/docs/reference/accounts/#identify-what-you-have) · [Qo'llab-quvvatlanmaydigan formatlar](https://phishdestroy.github.io/TgWitness/uz/docs/reference/accounts/#unsupported-formats)
- [Bir nechta hisoblar](https://phishdestroy.github.io/TgWitness/uz/docs/reference/accounts/#multiple-accounts) · [Hisob fayllarini xavfsiz saqlash](https://phishdestroy.github.io/TgWitness/uz/docs/reference/accounts/#keeping-account-files-safe) · [Muammolarni bartaraf etish](https://phishdestroy.github.io/TgWitness/uz/docs/reference/accounts/#troubleshooting)

## Bir qarashda

| Sizda nima bor | **Hisob qo'shish** yorlig'i | Shuningdek, sizga quyidagilar ham kerak bo'ladi |
| --- | --- | --- |
| Telefon raqami va uning kirish kodlariga kirish | **Telefon** | Agar yoqilgan bo'lsa, 2FA paroli |
| Telegram boshqa qurilmada ochiq | **QR kod** | Agar yoqilgan bo'lsa, 2FA paroli |
| `.session` fayli (Telethon yoki Pyrogram) | **Fayllar** | Ilova sozlamalari uchun ixtiyoriy hamroh JSON |
| `.session` va `.json`, bir xil nomga ega | **Fayllar** (ikkalasini ham tanlang) | Odatda boshqa hech narsa |
| `tdata` uchun Telegram Desktop papkasi | **Fayllar** (ZIP ko'rinishida) | Agar belgilangan bo'lsa, ish stoli mahalliy paroli |
| Telethon StringSession (matn, `.txt`, `.tgwitness-session`) | **Fayllar** | Alohida API juftligi talab etilmaydi |
| `.json` sessiya yoki Auth kaliti bilan | **Fayllar** | Alohida API juftligi talab etilmaydi |
| Auth kaliti (512 geksadetsimal belgilar) va uning DC raqami | **Auth kaliti** | Ixtiyoriy foydalanuvchi ID |

TgWitness fayllarni ularning nomiga qarab emas, **mazmuniga** qarab aniqlaydi. Fayl nomini o'zgartirish uni hech qachon konvertatsiya qilmaydi.

## Boshlashdan oldin: API ID va API xesh

Telegram API ilovasini yaratmasdan tizimga kira olasiz. Agar ish maydonida hech qanday juftlik kiritilmagan, import qilinmagan yoki allaqachon saqlanmagan bo'lsa, TgWitness o'zining ichki 50 jamoat API juftliklaridan (`tgwitness/api_pool.py`) yangi kirish uchun avvalo Telegram Desktopni afzal ko'radi va saqlangan juftlikni birinchi o'ringa qo'yadi; qolgan nomzodlar aralashtiriladi. Agar Telegram juftlikni rad etsa (`API_ID_INVALID`, `API_ID_PUBLISHED_FLOOD`, `UPDATE_APP_TO_LOGIN`), keyingisi sinab ko'riladi, kirishda sakkiztagacha; rad etilgan juftliklar qayta ishga tushirilguncha o'tkazib yuboriladi. Kirish uchun ishlatilgan juftlik hisob bilan saqlanadi va undan qayta foydalaniladi. Telegram uchun ilovani aniqlashda **API ID** va **API xesh**idan foydalaniladi; ular o'zlari hisobni avtorizatsiya qilmaydi.

Ulanish maydonlari yo'q bo'lsa, biriktirilgan [opentele2 2.0.0 kataloglaridan](https://github.com/DedInc/opentele2/tree/7e973bc71cd7a714ad13ac703c0895a90d36a735) deterministik qurilma/OS juftligi ishlatiladi: Desktop `2040`, Android `6`, Android X `21724`, iOS `10840`, macOS `2834` va Web `2496`. Androidning manba-build IDsi `4` ham [Telegram Android'ning BuildVars'ida](https://github.com/DrKLO/Telegram/blob/master/TMessagesProj/src/main/java/org/telegram/messenger/BuildVars.java) ko'rsatilganidek Android katalogidan foydalanadi. Web bo'yicha standart A; import qilingan `K` ilova-versiya qo'shimchasi yoki `macos` til paketi K ni tanlaydi, versiya `0.7.0` esa Webogram ni tanlaydi. Noma'lum ilova IDlari Telethon'ning host bo'yicha standart sozlamalarini saqlaydi. Import qilingan maydonlar har doim ustun keladi, jumladan eski ilova versiyasi va bo'sh til paketi. Katalog API ID/hashni hech qachon o'zgartirmaydi. Uning versiya snapshoti aloҳида ko'rib chiqiladi, kirish paytida olinmaydi. Saqlangan profil yangilanishlardan keyin barqaror bo'lib qoladi.

`account.getAuthorizations` Telegramning saqlangan ruxsatnoma metama'lumotlarini qaytaradi; u har bir yangi `initConnection` chaqirilishining aks sadosi emas. Uni haqiqiy yuborilgan profil bilan solishtiring. Mavjud ruxsatnomani bog'lash uning hamroh API xeshini tasdiqlamaydi: `initConnection` API IDni yuboradi, xesh esa kirish so'rovlari tomonidan ishlatiladi.

Yangi telefon yoki QR avtorizatsiyadan so'ng, TgWitness sozlamalarni, eng yaqin DCni, onlayn holatni, tillarni (tillar paketi bo'sh bo'lmaganida), ilova yangilanishlarini va xizmat ko'rsatish shartlari yangilanishlarini so'raydi, so'rovlar orasidagi vaqt 0.3–1.5 soniyaga teng. Statusi yangilash hisobni qisqa muddat onlayn deb belgilaydi. Ushbu ketma-ketlik faqat tizimga kirish yakunlanganda bir marta bajariladi, import qilish, qayta ulanish yoki qayta ishga tushirishda emas. Avtorizatsiya avval saqlanadi; muvaffaqiyatsiz so'rov ketma-ketlikni qayta urinmay yoki tizimga kirishni bekor qilmay to'xtatadi. Natijalar javob tanalariga emas, balki xato nomlariga asoslanib `account.initialized` sifatida qayd etiladi. Ushbu ketma-ketlik hisob cheklovlariga qarshi kafolat emas.

`tdesktop` uchun, agar `tz_offset` ko'rsatilmagan bo'lsa, serverning mahalliy UTC ofseti ishlatiladi, [opentele2 algoritmi](https://github.com/DedInc/opentele2/blob/7e973bc71cd7a714ad13ac703c0895a90d36a735/crates/opentele2-core/src/fingerprint.rs) (MIT; litsenziya `tgwitness/client_profiles.LICENSE` da) yordamida 900 soniyaga to'liqlashtiriladi. U har bir ulanishda yangilanadi, shunda yozgi vaqt o'zgarishlari aks ettiriladi. Import qilingan `tz_offset` barcha platformalarda ustunlikka ega bo'lib, aniq saqlanadi, shu jumladan nol qiymatda. Boshqa `initConnection.params` yozuvlari saqlanib qoladi. HTTP kirish formasida fayl importi orqali qaytarilgan raqamli vaqt zonasini qabul qiladi; boolean qiymatlar, fraksion sonlar va qo'llab-quvvatlanadigan diapazondan tashqaridagi ofsetlar rad etiladi.

To'g'ridan-to'g'ri, SOCKS5 va HTTP CONNECT yo'nalishlari Telethonning `ConnectionTcpObfuscated` (obfuskatsiyalangan qisqartirilgan MTProto)dan foydalanadi. HTTPS CONNECT proksi tomon TLSni saqlab qoladi va tunnel ichida xuddi shu obfuskatsiyalangan transportdan foydalanadi. MTProxy o'zining zarur tasodifiylashtirilgan oraliq transporti va maxfiy ma'lumotlarni boshqarishni saqlab qoladi. Yo'nalish almashtirishlar ham xuddi shu tanlovlarni qo'llaydi. Obfuskatsiya paket ramkalashni o'zgartiradi; u hisobni yoki uning klient metama'lumotlarini Telegram'dan yashirmaydi va cheklovlarga qarshi immunitetni anglatmaydi.

Ruxsat berilgan mijoz ulanib bo'lgach, TgWitness konfiguratsiyani, eng yaqin DCni, joriy avtorizatsiyani, ko'rib chiqilgan qatlam asosini, tillarni, ilova yangilanishlarini va xizmat ko'rsatish shartlari yangilanishlarini tekshiradi. Ushbu diagnostika har bir mijoz instantsiyasida, ma'lumotlarni yig'ishdan oldin bir marta ishga tushadi va ulanish tafsilotlari ostida vaqti bilan birga ko'rsatiladi. `account.connection_checked` sessiya xeshlarisiz, IP-manzillar, tokenlar yoki API xeshlarisiz natijani qayd etadi. Ular hech qachon shartlarni qabul qilmaydi yoki yangilanishlarni o'rnatmaydi. So'rov muvaffaqiyatsiz tugasa yoki FloodWait keyingi so'rovlarni to'xtatsa, yo'qolgan natija noma'lum bo'lib qoladi. Tarmoq tekshiruvlari o'tkazilmay qolgan bo'lsa ham, mahalliy tekshiruvlar o'z natijalarini hali ham hisobot qilishi mumkin.

FloodWait diagnostikasi muvaffaqiyatsiz bo'lgan TL usulini, har qanday Takeout/range o'ramlarini, server tomonidan so'ralgan kutishni va `telegram.backoff` dagi samarali muddatni saqlab qoladi. Ulanish tafsilotlari so'rovlar to'xtatilgan paytda usul va muddatni ko'rsatadi. Diagnostika har bir usul bo'yicha mijoz chaqiruvlari hisoblagichlarini o'z ichiga oladi; bu hisoblagichlar ushbu mijoz yaratilganidan beri ichki tengdosh hal qilishni alohida hisoblaydi, ammo paketlarni yoki Telethonning ichki qayta urinish urinishlarini hisoblamaydi. Joriy hisoblagichlar status APIda `collector.rpc_activity` sifatida ham mavjud. Hech qanday so'rov argumentlari, foydalanuvchi nomlari, kirish hashlari yoki istisno matni kiritilmagan. Oxirgi diagnostika va to'liq muddat qayta ishga tushirishdan keyin saqlanadi. Metod yozuvi bo'lmagan avvalgi kutishlar keyinchalik aniqlab bo'lmaydi. Manbaani ko'rib chiqish uchun [eksport limitlariga](https://github.com/phishdestroy/TgWitness/blob/main/docs/EXPORT-LIMITS.md) va kashfiyot bilan tarixni olish o'rtasidagi farqqa qarang.

`official_app=True` yoki `False` — bu Telegramning joriy-ruxsat berish bayrog'i. Hech biri hisob cheklangan, ishonchli yoki kuzatuv ostida ekanligini aniqlamaydi. Mavjud dalil-rejimidagi `account.devices` snapshotlari barcha kirish amalga oshirilgan qurilmalar tarixini saqlab qoladi; ulanish diagnostikasi esa faqat joriy qurilma tavsifini saqlaydi.

Ulanishdan oldin, maslahati tekshiruvlar API platformasi, til paketi, qurilma/OS va ilova-versiya formatlari, mobil tizim lokalizatsiyasi hamda Telethonning haqiqiy sxema qatlamini ko'rib chiqilgan katalog asosiy chizig'i bilan solishtiradi. Ogohlantirishlar server logida va hisob ma'lumotlari metadasida paydo bo'ladi; ular hech qachon import qilingan qiymatlarni almashtirmaydi yoki sxema qatlamini o'zgartirmaydi. Boshqa qatlam moslikni tekshirish signali bo'lib, buzilgan yoki cheklangan akkaunt dalili emas. Ushbu tekshiruvlar va `official_app` Telegram akkauntni cheklovlardan xavfsiz deb hisoblashini tasdiqlamaydi. Ulanmagan akkaunt holati yangi qurilma tavsifini yaratish o'rniga saqlangan profilni ishlatadi.

Buning o'rniga o'zingizning ilovangizdan foydalanish uchun (ilovani ro'yxatdan o'tkazgan hisob xavf ostida; [Qo'shimcha API havzasi nima uchun?](https://github.com/phishdestroy/TgWitness/blob/main/docs/PROJECT-GUIDE.md#connect-a-telegram-account) bo'limiga qarang):

1. [my.telegram.org saytini](https://my.telegram.org) oching va o'zingizga tegishli istalgan telefon raqami bilan tizimga kiring. Kod Telegram ilovasiga keladi, SMS orqali emas.
2. **API ishlab chiqish vositalarini** tanlang.
3. Ilova yarating: istalgan sarlavha va qisqa nom (5–32 harf), platforma: **ish stoli**. URL va tavsif bo'sh qoldirilishi mumkin.
4. **App api_id** (raqam) va **App api_hash** (32 geksadesimal belgilar) nusxasini oling.

Panelda kirish formasining ostida ochiq **API ID va Hashni** ko'ring. Siz bitta `api_id:api_hash` juftligini **API ID**ga joylashtirishingiz mumkin va ikkala maydon ham to'ldiriladi. Bir juftlik barcha hisoblaringiz uchun ishlatilishi mumkin. Muvaffaqiyatli tizimga kirgandan so'ng u faqat shu ish maydonida shifrlangan holda saqlanadi va hech qachon brauzerga qaytmaydi.

Uch xil turdagi akkaunt ma'lumotlari ishtirok etadi:

| Maxfiy | Ochiladi | Joylashuvi |
| --- | --- | --- |
| Panel tokeni | TgWitness veb-paneli | Ma'lumotlar katalogida `panel-token.txt` yoki `TGWITNESS_TOKEN` |
| API ID + xesh | O'zi hech narsa emas; ilovani aniqlaydi | O'rnatilgan juftlik, import qilingan sozlamalar yoki my.telegram.org saytida o'zingizning ilovangiz |
| Hisobni avtorizatsiya qilish | Telegram akkaunti | Telefon/QR logini orqali yaratilgan yoki sessiya sifatida olib kelingan |

Agar Telegramga proksi orqali ulanish kerak bo'lsa, avvalo **Hisob → Sozlamalar → Ulanish sozlamalari → Ulanish yo'nalishini o'zgartirish** bo'limida sozlang.

## Telefon raqami

1. **Hisobni** oching, **"Telefon**" yorlig'iga o'ting va raqamni xalqaro formatda kiriting, masalan, `+44 7700 900123`. Bo'shliqlar va chiziqchalar avtomatik ravishda olib tashlanadi.
2. **Davom etish tugmasini** bosing. API ID va Hash bo'sh qoldirilishi mumkin.
3. Telegram yuboradigan kodni kiriting (odatda Telegram ilovasiga; SMS kafolatlanmaydi).
4. Agar akkauntda ikki bosqichli tasdiqlash yoqilgan bo'lsa, o'sha parolni kiriting. Bu panel tokeni yoki qurilma paroli emas.
5. Kirishdan so'ng ko'rsatilgan hisob IDni tekshiring, so'ng manbalarni tanlang.

Kirish kodlari va 2FA paroli hech qachon diskka yozilmaydi.

## QR kod

Hisob allaqachon telefon yoki boshqa kompyuterda tizimga kirgan bo'lsa, buni ishlating.

1. **QR kod** yorlig'i → **QR kodni ko'rsatish**. API ID va Hash bo'sh qoldirilishi mumkin.
2. Kirish qilingan qurilmada: **Sozlamalar → Qurilmalar → Desktop qurilmasini bog'lash**, kodni skanerlang va tasdiqlang.
3. Telegram so'rasa, TgWitness'ga 2FA parolini kiriting.

QR tasviri mahalliy ravishda yaratiladi. Kodlarning amal qilish muddati tugaydi; qayta urinib ko'rish uchun **"Yana bir QR kod yaratish"** tugmasini bosing. Panelni qulflash, ish maydonini almashtirish yoki boshqa kirishni boshlash kutib turgan kodni bekor qiladi.

## Auth kaliti + DC identifikatori

Auth kaliti har bir Telegram sessiyasining asosiy 256 baytli ruxsat kalitidir, u **512 geksadesimal**belgida, ma'lumot markazi raqami **DC 1–5** bilan birga yozilgan.

1. Tab **Auth kaliti**. To'liq kalitni joylashtiring; `…`ni o'z ichiga olgan qisqartirilgan kalit ishlamaydi.
2. Kalit bilan birga taqdim etilgan DC ID ni tanlang.
3. Ixtiyoriy ravishda **Foydalanuvchi ID**-ni kiriting. Agar Telegram boshqa hisobni xabar qilsa, TgWitness ulanishni rad etadi.
4. **Connect hisobini** bosing.

Auth kaliti (512 belgili) API xeshidan (32 belgili) farq qiladi. Xuddi shu kalitni JSON shaklida ham import qilish mumkin, qarang: [Hisob JSON](https://phishdestroy.github.io/TgWitness/uz/docs/reference/accounts/#account-json).

## Hisob fayllari

**Hisobga qo'shish → Fayllar** bo'limiga o'ting va **bitta hisobga tegishli**, jami **8 MiB** gacha bo'lgan to'**rt**ta**faylni** tanlang, so'ng **Hisobni bog'lash tugmasini** bosing.

**Files** va **Auth kaliti** hamda ommaviy import shakllari ulanishdan oldin parallel sessiya ogohlantirishini ko'rsatadi. Standart bo'yicha import qilingan ruxsatnomalar qayta ishlatiladi. Bu yerda uning kaliti ishlatilayotgan paytda asl mijozni yopiq holda saqlang. **Files** va **Auth kaliti** shuningdek quyida tavsiflangan **mustaqil ruxsatnoma yaratish**imkonini ham beradi. Ommaviy import hanuzgacha to'g'ridan-to'g'ri rejimdan foydalanadi. Telefon va interaktiv QR orqali tizimga kirish alohida ruxsatnomalar yaratadi. Ogohlantirish sarlavhasi import shaklida ko'rinib turadi; fayllar yoki kalit/seans satri taqdim etilganda uning to'liq izohi avtomatik ochiladi. O'qib bo'lgach, uni yopish mumkin, shunda fayl tanlovchisi va ulanish boshqaruvlari telefonida ham ishlatilishi mumkin bo'ladi.

- Fayllar TgWitness serveringiz **xotirasida** konvertlanadi. Yuklamalar saqlanmaydi, ZIP arxivlari diskka chiqarilmaydi va hech qanday tashqi xizmatga murojaat qilinmaydi.
- Olingan sessiya keyin Telegram bilan tekshiriladi. Agar faylda foydalanuvchi ID ko'rsatilgan bo'lsa, u Telegram xabar qiladigan hisobga mos kelishi kerak.
- Turli hisoblar yoki turli API ma'lumotlarini tasvirlovchi fayllar qabul qilinmaydi ularning birini tanlash o'rniga.
- **Parol yoki sessiya matni** TData mahalliy parol maydonini o'z ichiga oladi, u StringSession va **Read**fayllarini**imzolamasdan**joylashtirish uchun mo'ljallangan qutidir (Telegram bilan bog'lanmasdan shaklni to'ldiradi).

### Mustaqil avtorizatsiya yarating

Import qilingan fayllarni yoki Auth kalitini bog'lashdan oldin **mustaqil ruxsatnomani yarating**. TgWitness import qilingan donorni qisqa muddatga bog'laydi, uni yangi mijozning QR kirish tokenini tasdiqlash uchun ishlatadi va tasdiqlangandan so'ng donorni darhol uzib qo'yadi. Yangi mijozning o'z ruxsat kaliti va alohida tanlangan ish stoli profili mavjud. Donor tomonidan taqdim etilgan API ma'lumotlari va qurilma profili faqat donor ulanishi uchun ishlatiladi. Hech qanday mavjud ruxsat bekor qilinmaydi yoki bekor qilinishi qayd etilmaydi.

**Ushbu bosqichda donorning asl mijozini to'liq yopiq holda saqlang.** Dastlabki ulanish hanuzgacha nusxalangan kalitdan foydalanadi, shuning uchun bu rejim dastlabki parallel foydalanish xavfini bartaraf eta olmaydi. Yangi avtorizatsiya ulanishi bilan egasi asl mijozni qayta ochib, ikkalasini mustaqil ravishda ishlatishi mumkin. Interaktiv **QR kodli** kirish asl mijozga kalitni bu yerga nusxalamasdan yoki ulamasdan kirishni tasdiqlash imkonini beradi.

Agar Telegram 2ni so'rasa, ushbu rejim mavjud bo'lsa, tanlangan JSON-dagi `twoFA`dan foydalanadi yoki parolni so'raydi. Rad etilgan import qilingan parol parol formasiga qaytadi. Parollar saqlanmaydi. Nomzod kalit `independent_login.enc`da shifrlangan holda saqlanadi, jumladan ma'lumotlar markazi migratsiyasi paytida bo'lgan o'zgarishlar bilan. Tuzilish uzilgach, saqlangan nomzodni davom ettirish uchun bir xil donor va ushbu opsiyani tanlang. Ish maydoni shu hisob uchun ajratilgan holda qoladi; muvaffaqiyatsiz yakunlash yangi ish maydonini o'chirib tashlamaydi. Uning ma'lumotlar katalogi va ombor kalitini saqlang. Yakuniy kirish ma'lumotlari va `account.authorized` jurnal yozuvida import usuli, kirish formatlari va donor API ID ko'rsatiladi, donor kaliti yoki paroli kiritilmaydi.

On 5 Noyabr 2026, maxsus hisob Telethon, Pyrogram va TData donorlari bilan jonli tekshiruvlardan oʻtdi: 2FAni yakunlash, alohida yangi avtorizatsiya kalitlari, donor va yangi mijozning bir vaqtda kirish huquqi hamda ommaviy kanalni o'qish. Telethon holatida parol bosqichidagi uzilishdan so'ng saqlangan nomzod qayta tiklandi. Har bir yangi avtorizatsiya kirishdan keyingi oltita dastlabki tashabbus so'rovlarini bajarib, uning imzolangan jurnali tasdiqlandi. Asl sessiya taqdim etilgan to'rt formatning barchasida ishlatilishi mumkin bo'lib qoldi.

Telegram [RPC xatoliklar ma'lumotlar bazasi](https://core.telegram.org/api/errors.json) `FRESH_CHANGE_ADMINS_FORBIDDEN` ni administratorlarni o'zgartirish bilan, `FRESH_CHANGE_PHONE_FORBIDDEN` ni telefon raqamini o'zgartirish bilan va `FRESH_RESET_AUTHORISATION_FORBIDDEN` ni boshqa sessiyalarni bekor qilish, ularning umrini o'zgartirish yoki passkey ro'yxatdan o'tkazish bilan bog'laydi. `SESSION_TOO_FRESH_*` va `PASSWORD_TOO_FRESH_*` egalikni o'tkazish hamda daromad yoki sovg'alarni yechib olish bilan bog'liq. Bu yig'im operatsiyalari emas; yangi kirish 24 soatlik o'qish taqiqini anglatmaydi. Eksport alohida holda `TAKEOUT_INIT_DELAY_*` ni qaytarishi mumkin. TgWitness server tomonidan so'ralgan tanaffuslarni saqlab qoladi va cheklovlarni chetlab o'tish uchun tokenni avtomatik qabul qilishni qayta urinmaydi yoki sessiyalarni bekor qilmaydi.

### Telethon `.session`

|  |  |
| --- | --- |
| Bu nima | SQLite ma'lumotlar bazasi Telethon asosidagi vositalar tomonidan yaratiladi, masalan `my_account.session` |
| Tomonidan tan olingan | Jadvalar`sessions` (`dc_id`, `server_address`, `port`, `auth_key`) va `version` = 7 yoki 8 |
| Talablar | Aniq bir ruxsat berilgan sessiya qatori; yopiq, to'liq ma'lumotlar bazasi |

Avvalo faylni yaratgan dasturni yoping. Agar uning yonida `my_account.session-journal` yoki `my_account.session-wal` mavjud bo'lsa, ma'lumotlar bazasi yakunlanmagan: asl klientni toza ochib, toza yoping. Ushbu yon fayllarni o'chirish buzilgan nusxa qoldirishi mumkin.

### Pyrogram `.session`

|  |  |
| --- | --- |
| Bu nima | SQLite ma'lumotlar bazasi Pyrogram asosidagi vositalar yaratadi |
| Tomonidan tan olingan | `sessions` va `dc_id`, `auth_key`, `test_mode`, `user_id`, `is_bot`; `version` = 2 yoki 3 |
| Talablar | Ishlab chiqarish tarmog'ida bitta ruxsat etilgan **foydalanuvchi** sessiyasi. Bot va test-DC sessiyalari rad etiladi |

Saqlangan foydalanuvchi identifikatori tizimga kirish paytida Telegram bilan tekshiriladi.

### Sessiya + JSON juftligi

Hisoblar ko'pincha bir xil nomga ega ikki fayl ko'rinishida tarqatiladi, masalan `447700900123.session` va `447700900123.json`. **Ikkalasini** bir vaqtda tanlang.

- JSONdan TgWitness `app_id`/`api_id` va `app_hash`/`api_hash` ni ishlatadi, shuning uchun odatda API ma'lumotlarini kiritishingiz shart emas.
- Ulanish profili quyidagi parametrlardan foydalanadi: `device_model` (`device` nomi bilan ham), `system_version` (`sdk` nomi bilan ham), `app_version`, `lang_code`, `system_lang_code` (`system_lang_pack` nomi bilan ham), `lang_pack` va ixtiyoriy `tz_offset` (UTCdan soniyalarda, -43200 dan 50400 gacha). Taqdim etilgan maydonlar avtomatik hosil qilingan qiymatlar va panel/brauzer tilidan ustun turadi. To'qnashuvchi aliaslar rad etiladi. Hal qilingan profil shifrlangan ish maydoni ma'lumotlarida saqlanadi va qayta ishga tushirilgandan so'ng, jumladan uning ilova versiyasi bilan qayta ishlatiladi.
- `phone`, proxy sozlamalari va qurilma tokenlari **e'tiborsiz** qoldiriladi. `twoFA` faqat o'qish uchun mo'ljallangan **Mustaqil avtorizatsiya yaratish** tanlanganda; to'g'ridan-to'g'ri importda e'tiborsiz qoldiriladi.
- Qo'llab-quvvatlanadigan avtorizatsiya maydoni bo'lmagan JSON faqat metadata hisoblanadi. Uning sessiya faylini qo'shing yoki telefon yoki QR orqali tizimga kirishni davom ettiring. Qo'llab-quvvatlanadigan sessiya yoki Auth kalitini o'z ichiga olgan JSON mustaqil ravishda avtorizatsiya qilishi mumkin; [Account JSON-ga](https://phishdestroy.github.io/TgWitness/uz/docs/reference/accounts/#account-json) qarang.

### Telegram Desktop (TData)

TData — bu Telegram Desktop ilovasining (desktop.telegram.org saytidan olingan ko'p platformali ilova) `tdata` papkasi.

| Tizim | `tdata` bo'yicha standart joylashuv |
| --- | --- |
| Windows | `%APPDATA%\Telegram Desktop\tdata` (portativ Telegram: `Telegram.exe` yonida) |
| Linux | `~/.local/share/TelegramDesktop/tdata` |
| macOS | `~/Library/Application Support/Telegram Desktop/tdata` |

Uni import qilish uchun:

> **Parallel sessiya ogohlantirishi.** To'g'ridan-to'g'ri TData importi Telegram Desktop'ning avtorizatsiya kalitidan qayta foydalanadi. Ushbu kalitni Desktop va TgWitness'da bir vaqtda ishlatmang. Telegram avtorizatsiyani `AUTH_KEY_DUPLICATED` xatosi bilan bekor qilishi mumkin va yangi tizimga kirishgacha ikkala nusxa ishlamay qoladi.
>
>
>
> TgWitness import qilingan sessiyadan foydalanganda Desktop-dan, jumladan uning tray jarayonidan to'liq chiqib ketib, shu nusxani yopiq holda saqlang. **Chiqib ketishni tanlang, tizimdan chiqish yoki sessiyani bekor qilishni bajarmang:** bekor qilish import qilingan nusxani ham bekor qiladi. Agar ikkala klientni ham ishlatishingiz kerak bo'lsa, **Mustaqil avtorizatsiya yaratishni** tanlang va yangi kirish muvaffaqiyatli bo'lguncha Desktop-ni yopiq holda saqlang, yoki TgWitness-ga telefon yoki QR orqali kirishni bajaring. Alohida akount tavsiya etiladi, ammo bu nusxalangan kalitlarni parallel ravishda ishlatishni xavfsiz qilmaydi.
>
>
>
> Bu shuningdek import qilingan `.session` fayllariga, StringSession matni va Auth Key HEX ga ham tegishli. O'zining mustaqil yaratilgan ruxsatnomalariga ega boshqa mijozlar ham tizimga kirgan holda qolishi mumkin. [Telegramning AUTH_KEY_DUPLICATED hujjatlarini](https://core.telegram.org/api/errors#406-not-acceptable) ko'ring.

1. Telegram Desktop'dan to'liq chiqing.
2. `tdata`-dan **faqat** ushbu ikkita elementni o'z ichiga olgan ZIP yarating:

   - `key_datas`
   - `s` bilan tugaydigan 16 belgili fayl yonida, odatda `D877F783D5D3EF8Cs`

   Media keshini o'z ichiga olgan butun papkani siqib yuborish odatda limitlardan oshadi (512 ta yozuv, 32 MiB ochilmagan holatda). 3. Fayllarda ZIP-ni tanlang. Agar Telegram Desktop'da **mahalliy parol** bo'lsa, avvalo uni **Passcode yoki sessiya matni** satriga kiriting. Bu 2FA paroli emas.

Qo'llab-quvvatlanadi: har bir arxiv uchun bitta hisob, zamonaviy `key_datas`/`key_data0`/`key_data1` saqlash, mahalliy parol. Qo'llab-quvvatlanmaydi: bir nechta tizimga kirgan hisoblarga ega papkalar, eski Desktop tartiblari, parol bilan himoyalangan ZIP-fayllar va macOS uchun alohida mahalliy "Telegram for macOS" ilovasi.

### Telethon StringSession

Bir qatorli matn, odatda `1` bilan boshlanib, taxminan 350 belgidan iborat. Uni `.txt` yoki `.tgwitness-session` fayli sifatida yuklang (eng ko'pi bilan 4 KiB) yoki **Passcode yoki session matni** ostiga joylashtiring. Faqat Telethon satrlari qabul qilinadi; Pyrogram va TDLib satrlari boshqa formatlardan foydalanadi.

### Hisob JSON

**`.json`** bilan tugaydigan faylda, maksimal **64 KiB** hajmdagi bitta JSON ob'ekti.

| Maydon (laqablari) | Ma'no |
| --- | --- |
| `api_id` (`app_id`) | Ilova ID, ijobiy son |
| `api_hash` (`app_hash`) | Ilova xesh, 32 geksadesimal belgilar |
| `string_session` (`session_string`, `session_str`; eski `session`) | Telethon StringSession matni, fayl nomi emas |
| `auth_key` (`auth_key_hex`) + `dc_id` | 512 belgili Auth kalitini va DC 1–5 ni to'ldiring |
| `user_id` (`id`) | Ixtiyoriy; ruxsat saqlanmasidan oldin Telegramda tekshiriladi |
| `device_model` (`device`) | Ulanish qurilmasi tavsifi |
| `system_version` (`sdk`) | Connection OS versiyasi |
| `app_version` | Telegramga yuborilgan ilova versiyasi |
| `lang_code`, `system_lang_code` (`system_lang_pack`), `lang_pack` | Kliyent tili, tizim tili va kliyent til paketi; bo'sh `lang_pack` ruxsat etiladi |
| `tz_offset` | Ixtiyoriy UTC ofseti soniyalarda, `initConnection.params` ga yuboriladi; butun yoki o'nlik butun sonli satr |

Agar taxallus va asosiy nom ikkalasi ham mavjud bo'lsa, ular mos kelishi kerak. Aniq Telethon sessiya maydonchalari boshqa formatdagi umumiy `session` blobiga nisbatan ustunlikka ega. Agar ikkalasi ham tanib bo'ladigan Telethon sessiyalarini o'z ichiga olsa, ular bir xil avtorizatsiyani tasvirlashi kerak. Aniq maydoncha bo'lmasa, `session` haqiqiy Telethon StringSession bo'lishi kerak. Misollar:

```
{ "app_id": 1234567, "app_hash": "0123456789abcdef0123456789abcdef" }
```

```
{
  "api_id": 1234567,
  "api_hash": "0123456789abcdef0123456789abcdef",
  "auth_key": "REPLACE_WITH_ALL_512_HEXADECIMAL_CHARACTERS",
  "dc_id": 2,
  "user_id": 123456789
}
```

Birinchi misol faqat API ma'lumotlarini to'ldiradi; telefon yoki QR orqali tizimga kiring yoki sessiya faylini qo'shing. Ko'p hisob ro'yxatlari (hisoblarning JSON massiv) qabul qilinmaydi.

## Nimangiz borligini aniqlang

| Ko'ryapsiz | Bu | Foydalaning |
| --- | --- | --- |
| `*.session`; uni matn muharririda ochish yuqorida `SQLite format 3` ko'rinishini ko'rsatadi | Telethon yoki Pyrogram SQLite | **Fayllar** (avtomatik aniqlangan) |
| `tdata` papkasi ichida `key_datas` | Telegram Desktop TData | Ikki faylni ZIP qiling, so'ngra **Fayllar** |
| `1` bilan boshlanadigan bitta matn qatori, taxminan 350 belgili | Telethon StringSession | **Fayllar** |
| `*.json` va `app_id`/`app_hash` | Qo'shimcha metadata | **Fayllar**, sessiyasi bilan birga |
| `*.json`, `auth_key` yoki `string_session` bilan | Hisob JSON | **Fayllar** |
| 512 belgilar `0-9a-f` | Avtorlik kaliti | **Auth kaliti** |
| 32 belgilar`0-9a-f` | API xesh | **API ID + Hash** |
| `td.binlog` yoki TDLib ilovasidan `db.sqlite` | TDLib saqlash | Qo'llab-quvvatlanmaydi |
| `123456789:AA…` | Bot tokeni | Qo'llab-quvvatlanmaydi |

## Qo'llab-quvvatlanmaydigan formatlar

| Format | Alternativ |
| --- | --- |
| TDLib saqlash (`td.binlog`) va TDLib eksportlari | Telefon yoki QR orqali tizimga kiring |
| Pyrogram sessiya **satrlari** | Pyrogram `.session` faylidan yoki telefon/QR kodidan foydalaning |
| Bir nechta tizimga kirgan hisoblar bilan TData | Telegram Desktop'dagi boshqa hisoblardan chiqib turing yoki har bir hisob uchun alohida sessiya faylidan foydalaning |
| Bot tokenlari | Qo'llab-quvvatlanmaydi: TgWitness foydalanuvchi hisobini kuzatadi |
| Ko'plab akkauntlarning CSV/JSON ro'yxatlari | Qo‘llab-quvvatlanadigan sessiya fayllarini **Hisoblar → Hisoblarni import qilish** orqali import qiling yoki alohida ishchi maydonlarda telefon/QR orqali kiring |
| Test-DC yoki bot sessiyalari | Ishlab chiqarish foydalanuvchi hisobini ishlating |

## Bir nechta hisoblar

Hisob tanlovchisining yonidagi **+** tugmasini bosing yoki **Hisob → Sozlamalar → Ulanish sozlamalari → Ish maydonlari bo'limini** oching, yorliq kiriting va kirishni bosing.

- Asosiy ish maydoni hamda istalgan sonli boshqa ish maydonchalari mavjud. Har birining o'z sessiyasi, proxy yo'li, manbalari, yozib olish siyosati, jurnali, imzolash kaliti, tekshirish nuqtalari va eksportlari mavjud.
- Ko'rsatilayotgan ish maydonini almashtirish boshqalarni to'xtatmaydi.
- Jurnal uni yaratgan akkauntga bog'langan bo'lib qoladi. Boshqa akkauntga kirish uchun alohida ish maydoni talab etiladi va bir akkaunt ikki ish maydoniga tayinlanishi mumkin emas.
- Asosiy panel tokeni barcha ish maydonlarini nazorat qiladi. [Berilgan kirish](https://phishdestroy.github.io/TgWitness/uz/docs/reference/access/) boshqalarni tanlangan hisoblar va suhbatlarga, alohida ruxsatnomalar va sessiya cheklovlari bilan cheklashi mumkin.
- **Hisoblar** ish maydonini qayta nomlaydi va qo'shilgan ish maydonini sessiyasi, jurnali, manbalari va imzolash kaliti bilan o'chirib tashlaydi. Asosiy ish maydoni paneldan o'chirilmaydi.

### Ommaviy import va hisob guruhlari

**Hisoblar → Hisoblarni import qilish** orqali bir nechta hisobni qo'shing, fayllarni bazaviy nom bo'yicha juftlang va har bir kirish natijasini ko'ring. Har bir hisobga alohida ish maydoni beriladi.

Guruh tegishli hisoblarni ularning sessiyalari, kalitlari yoki dalillarini birlashtirmasdan birga saqlaydi. **Hisoblar** bo'limidagi **Ochiq guruhni** bosish uning sahifasiga olib boradi `/groups/<id>`:

- **Hisoblar:** har bir a'zoning ulanish yo'li, kuzatuvi va oxirgi xabari, **Barchasini** boshlash va **barchasini to'xtatish**.
- **E'tibor talab qiladi:** tizimdan chiqarilgan, mavjud bo'lmagan yoki ulanish, qabul qilish, manba yoki media bilan bog'liq muammo bo'lgan hisoblar; har bir nom uning kartasiga olib boradi.
- **Suhbatlar bir nechta hisoblarni ko'rsatadi:** ulashilgan manbalar, ularni kuzatayotgan hisoblar va mavjud ish maydoni-kuzatuv davrida (7 kungacha) uzilishlar. **N ta hisob bilan eksport** kanal yoki superguruh eksportini ularga bo'lib beradi va bitta arxivni imzolaydi.
- **Guruhni eksport qilish:** har bir hisobning imzolangan eksporti bilan bitta ZIP `accounts/` va `manifest.json` SHA-256 va kalit barmoq izlarini ro'yxatlab, asosiy ish maydoni tomonidan imzolangan `manifest.signature.json`. Har bir akkaunt arxivini alohida tarzda bilan tasdiqlang. `python -m tgwitness.verify` va o'sha hisobning ishonchli barmoq izi yordamida.

A'zolar guruh sozlamalarini baham ko'radi; hisob o'z qiymatlarini saqlab qolishi mumkin. Qarang [ulashilgan sozlamalar](https://phishdestroy.github.io/TgWitness/uz/docs/reference/settings/#account-groups), [import va guruhlar bo'yicha qo'llanma](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Accounts.md#import-accounts-and-share-settings) va [MTProxy pool boshqaruv paneli](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Proxies.md#pool-dashboard-and-custom-sources).

## Chiqish

**Hisob → Telegramdan chiqish** (kuzatish to'xtatilgan holda) Telegramdan sessiyani yakunlashni so'raydi, shuning uchun u hisobning **Sozlamalar → Qurilmalar** bo'limidan ham yo'qoladi va ish maydoni shifri omboridan sessiyani o'chirib tashlaydi. Jurnal, manbalar, sozlamalar va imzolash kaliti saqlanib qoladi, va jurnal chiqishni qayd etadi. Ish maydoni hanuzgacha o'z hisobiga tegishli bo'lib qoladi: faqat shu hisob qayta ulanishi mumkin. Agar Telegram javob bermasa ham, sessiya bu yerda baribir o'chiriladi va panel bunga oid xabarni ko'rsatadi; Telegramda **Sozlamalar → Qurilmalar** bo'limida sessiyani yakunlang.

## Hisob fayllarini xavfsiz saqlash

- Har bir `.session`, TData ZIP, StringSession, Auth Key va hisob JSON faylini parol kabi muomala qiling. TgWitness import qilingan ruxsatnomalarni shifrlangan omborida saqlaydi; keyin asl fayllarni o'chirib tashlashingiz mumkin.
- Bir xil ruxsatni ikki dasturda bir vaqtda ishga tushirmang. Telegram uni bekor qilishi mumkin (`AUTH_KEY_DUPLICATED`), va ikkala nusxa ham ishlamay qoladi.
- Muddatidan o'tgan yoki bekor qilingan sessiyani konversiya orqali qayta tiklash mumkin emas. Qayta tizimga kiring.

## Muammolarni bartaraf etish

| Xabar yoki simptom | Nima qilish kerak |
| --- | --- |
| *Ushbu sessiyani o'qib bo'lmaydi. Uning asl mijozini yoping…* | SQLite fayl ochiq yoki yakunlanmagan (`-journal`/`-wal` yon fayl). Asl dasturni toza tarzda yoping va faylni yana nusxalang. |
| *Qo'llab-quvvatlanadigan Telethon SQLite sxemalari: 7 va 8* / *Pyrogram … 2 va 3* | Faylni juda eski yoki noma'lum kutubxona versiyasi yaratgan. Buning o'rniga telefon/QR orqali tizimga kiring. |
| *Faqat ruxsat etilgan ishlab chiqarish foydalanuvchi sessiyalari qo'llab-quvvatlanadi* | Pyrogram fayli botga yoki test tarmog'iga tegishli. |
| *TData arxivi 512 yozuvdan yoki 32 MiBdan oshadi* | Faqat `key_datas` va `D877F783D5D3EF8Cs` ZIP, butun papka emas. |
| *TData ni dekript qilib bo'lmadi. Desktop mahalliy parolini tekshiring* | **Passcode yoki sessiya matni** satriga Telegram Desktop mahalliy parolini kiriting. |
| *Bir vaqtning o'zida bitta TData hisobini import qiling* | Telegram Desktop bir nechta hisoblarga ega edi; [qo'llab-quvvatlanmaydigan formatlarga](https://phishdestroy.github.io/TgWitness/uz/docs/reference/accounts/#unsupported-formats) qarang. |
| *Tanlangan fayllar turli hisoblar yoki API ma'lumotlarini tasvirlaydi* | Fayllarni faqat bitta akkauntdan tanlang. |
| *JSONda qo'llab-quvvatlanadigan API ma'lumotlari yoki avtorizatsiya yo'q* | [Hisob JSON](https://phishdestroy.github.io/TgWitness/uz/docs/reference/accounts/#account-json)idagi maydon nomlarini tekshiring. |
| *Faqat API metama'lumotlari* | JSONda sessiya yo'q. `.session` faylini qo'shing yoki telefon/QR-koddan foydalaning. |
| *Auth kaliti HEX barcha 512 geksadesimal belgini o'z ichiga olishi kerak* | Kalit qisqartirilgan yoki unda`…` mavjud. |
| Hisob IDi import qilingan hisob bilan mos kelmaydi | Faylning foydalanuvchi IDi Telegram xabar qilganidan farq qiladi; fayl boshqa hisob uchun mo'ljallangan. |
| Hisob allaqachon boshqa ish maydoniga tegishli | Hisobni ikki marta qo'shish o'rniga o'sha ish maydonini oching. |
| Ulanish mavjud, ammo **Manbalar** chat ro'yxatida shaxsiy guruh yo'q. | A'zolikni tekshiring. Tanlovchi birinchi 1 000 ta dialogni tekshiradi; **parametrlar** bo'limida limitni oshiring. |
| Proxy ulanishi muvaffaqiyatsiz bo'ldi | Yo'nalish va IP rejimini tekshiring. Avtomatik MTProxy boshqa ishlaydigan kirishni sinab ko'radi. "Adressni yashirish" kutadi; "To'g'ridan-to'g'ri" esa oxirgi chora sifatida sozlangan kechikishdan so'ng to'g'ridan-to'g'ri ulanishi mumkin. [Yo'naltirish rejimlarini](https://phishdestroy.github.io/TgWitness/uz/docs/reference/connection/#ip-modes) ko'ring. |

Shuningdek qarang: proksi va shifrlash uchun [ulanish va xavfsizlik](https://phishdestroy.github.io/TgWitness/uz/docs/reference/connection/), hamda tizimga kirgandan keyin [qanday ma'lumotlar yig'ilishi](https://phishdestroy.github.io/TgWitness/uz/docs/reference/collection/).
