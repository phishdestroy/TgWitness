# Hisoblar va sessiya formatlari

Canonical page: https://phishdestroy.github.io/TgWitness/uz/docs/reference/accounts/

Telefon, QR kod yoki avtorizatsiya kaliti orqali tizimga kiring, Telethon, Pyrogram yoki Telegram Desktop sessiyalarini import qiling va bir nechta akkauntlarni boshqaring.

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

Telegram API ilovasini yaratmasdan tizimga kirishingiz mumkin. Agar ish maydonida hech qanday juftlik kiritilmagan, import qilinmagan yoki allaqachon saqlanmagan bo'lsa, TgWitness o'zining ichki 50 ta ommaviy API juftligi (`tgwitness/api_pool.py`) havzasidan tasodifiy tartibda juftlikni tanlaydi. Agar Telegram juftlikni rad etsa (`API_ID_INVALID`, `API_ID_PUBLISHED_FLOOD`, `UPDATE_APP_TO_LOGIN`), keyingisi sinab ko'riladi, kirishda sakkiztagacha; rad etilgan juftliklar qayta ishga tushirilgunga qadar o'tkazib yuboriladi. Kirish uchun imzolangan juftlik hisob bilan saqlanadi va shu hisob uchun qayta ishlatiladi. Telegram ilovasini aniqlash uchun **API ID** va **API xesh**idan foydalaniladi; ular o'z-o'zidan hisobni tasdiqlamaydi.

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

- Fayllar TgWitness serveringiz **xotirasida** konvertlanadi. Yuklamalar saqlanmaydi, ZIP arxivlari diskka chiqarilmaydi va hech qanday tashqi xizmatga murojaat qilinmaydi.
- Olingan sessiya keyin Telegram bilan tekshiriladi. Agar faylda foydalanuvchi ID ko'rsatilgan bo'lsa, u Telegram xabar qiladigan hisobga mos kelishi kerak.
- Turli hisoblar yoki turli API ma'lumotlarini tasvirlovchi fayllar qabul qilinmaydi ularning birini tanlash o'rniga.
- **Parol yoki sessiya matni** TData mahalliy parol maydonini o'z ichiga oladi, u StringSession va **Read**fayllarini**imzolamasdan**joylashtirish uchun mo'ljallangan qutidir (Telegram bilan bog'lanmasdan shaklni to'ldiradi).

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
- `phone`, `device`, `sdk`, `app_version`, `lang_pack` yoki saqlangan `twoFA` paroli kabi boshqa maydonlar **e'tiborsiz** qoldiriladi. Agar hisobda 2FA yoqilgan bo'lsa, TgWitness uni so'raydi.
- Faqat JSON o'zi faqat metadata hisoblanadi. Sessiya faylsiz telefon yoki QR orqali tizimga kirishni davom ettiring.

### Telegram Desktop (TData)

TData — bu Telegram Desktop ilovasining (desktop.telegram.org saytidan olingan ko'p platformali ilova) `tdata` papkasi.

| Tizim | `tdata` bo'yicha standart joylashuv |
| --- | --- |
| Windows | `%APPDATA%\Telegram Desktop\tdata` (portativ Telegram: `Telegram.exe` yonida) |
| Linux | `~/.local/share/TelegramDesktop/tdata` |
| macOS | `~/Library/Application Support/Telegram Desktop/tdata` |

Uni import qilish uchun:

> **Parallel sessiya ogohlantirishi.** TData import qilish Telegram Desktop'ning avtorizatsiya kalitidan qayta foydalanadi; u mustaqil kirishni yaratmaydi. Ushbu kalitni Desktop va TgWitness'da bir vaqtda ishlatmang. Telegram `AUTH_KEY_DUPLICATED` bilan avtorizatsiyani bekor qilishi mumkin, natijada yangi kirish amalga oshirilguncha ikkala nusxa ishlay olmaydi.
>
>
>
> Desktop ilovasini to'liq yoping, jumladan tray jarayonini ham, va TgWitness import qilingan sessiyadan foydalangan paytda o'sha nusxani yopiq holda saqlang. **Chiqib ketish (Quit) tugmasini bosing, sessiyani tugatmang yoki bekor qilmang:** bekor qilish import qilingan nusxani ham bekor qiladi. Agar ikkala ilovani ham ishlatishingiz kerak bo'lsa, TgWitnessga telefon yoki QR kod orqali kirib, alohida ruxsatnoma yarating. Alohida hisob yaratish tavsiya etiladi, ammo bu klonlangan kalitlarni parallel ravishda ishlatish uchun xavfsiz qilmaydi.
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
| `string_session` (`session_string`, `session`) | Telethon StringSession matni, fayl nomi emas |
| `auth_key` (`auth_key_hex`) + `dc_id` | 512 belgili Auth kalitini va DC 1–5 ni to'ldiring |
| `user_id` (`id`) | Ixtiyoriy; ruxsat saqlanmasidan oldin Telegramda tekshiriladi |

Agar taxallus va asosiy ism ikkalasi ham mavjud bo'lsa, ular mos kelishi kerak. Misollar:

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

Bir nechta hisob qo‘shish, fayllarni asosiy nomi bo‘yicha juftlash va har bir kirish natijasini ko‘rish uchun **Hisoblar → Hisoblarni import qilish** bo‘limidan foydalaning. Har bir hisob alohida ish maydoniga ega. Guruhlar seanslar, kalitlar yoki dalillarni birlashtirmasdan namunadan tanlangan sozlamalarni nusxalashi mumkin. [import va guruhlar qo‘llanmasi](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Accounts.md#import-accounts-and-share-settings) va [MTProxy havuzi boshqaruv paneli](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Proxies.md#pool-dashboard-and-custom-sources)ga qarang.

## Chiqish

**Hisob → Telegramdan chiqish** (kuzatish to'xtatilgan holda) Telegramdan sessiyani yakunlashni so'raydi, shuning uchun u hisobning **Sozlamalar → Qurilmalar** bo'limidan ham yo'qoladi va ish maydoni shifri omboridan sessiyani o'chirib tashlaydi. Jurnal, manbalar, sozlamalar va imzolash kaliti saqlanib qoladi, va jurnal chiqishni qayd etadi. Ish maydoni hanuzgacha o'z hisobiga tegishli bo'lib qoladi: faqat shu hisob qayta ulanishi mumkin. Agar Telegram javob bermasa ham, sessiya bu yerda baribir o'chiriladi va panel bunga oid xabarni ko'rsatadi; Telegramda **Sozlamalar → Qurilmalar** bo'limida sessiyani yakunlang.

## Telethon sessiyasini oflayn rejimga aylantiring

Panel `.session` fayllarini to'g'ridan-to'g'ri import qiladi. Oflayn konvertatsiya uchun StringSession fayliga, loyiha papkasidan quyidagi buyrug'ni ishga tushiring:

```
.venv\Scripts\python.exe -m tgwitness.sessions account.session --out account.tgwitness-session   # Windows
```

```
.venv/bin/python -m tgwitness.sessions account.session --out account.tgwitness-session          # Linux/macOS
```

Konverter faqat Telethon SQLite (64 MiB gacha) faylini o'qiydi, kirishni hech qachon o'zgartirmaydi, tarmoq so'rovlarini amalga oshirmaydi va mavjud chiqish faylini ustiga yozishni rad etadi.

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
| Proxy ulanishi muvaffaqiyatsiz bo'ldi | Yo'nalish va IP rejimini tekshiring. Avtomatik MTProxy boshqa ishlaydigan kirishni sinab ko'radi. IP yashirish rejimi kutadi; aniq tanlangan zaxira rejimi sozlangan kechikishdan so'ng to'g'ridan-to'g'ri ulanishi mumkin. [Yo'naltirish rejimlarini](https://phishdestroy.github.io/TgWitness/uz/docs/reference/connection/#ip-modes) ko'ring. |

Shuningdek qarang: proksi va shifrlash uchun [ulanish va xavfsizlik](https://phishdestroy.github.io/TgWitness/uz/docs/reference/connection/), hamda tizimga kirgandan keyin [qanday ma'lumotlar yig'ilishi](https://phishdestroy.github.io/TgWitness/uz/docs/reference/collection/).
