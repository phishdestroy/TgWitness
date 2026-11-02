# Kirish va ruxsatnomalar

Canonical page: https://phishdestroy.github.io/TgWitness/uz/docs/reference/access/

Hisoblar va suhbatlarga cheklangan kirish huquqini bering, ruxsatlarni tanlang, sessiyalar va IP-manzillarni cheklang hamda kirishni bekor qiling.

Ko'rib chiquvchiga bitta suhbatga, tahlilchiga ishni eksport qilishga yoki operatorga tanlangan hisoblarni boshqarishga ruxsat bering. Har bir kishiga o'z tokeni beriladi. Asosiy panel tokeni administrator qo'lida qoladi.

[Hisobni sozlash](https://phishdestroy.github.io/TgWitness/uz/docs/reference/accounts/) · [Ulanish yo'nalishlari](https://phishdestroy.github.io/TgWitness/uz/docs/reference/connection/) · [Xavfsizlik modeli](https://phishdestroy.github.io/TgWitness/uz/docs/reference/security/)

## Ikki maqsad, ikki xil vazifa

**Yig'ish doirasi** hisob qaydnomasining nimani qayd etishini belgilaydi: tanlangan suhbatlar, Telegram papkasi yoki butun hisob qaydnomasi. **Kirish doirasi esa** qayd etilgan hisob qaydnomalari va suhbatlardan qaysilarini boshqa shaxs ko'rishi va ulardan foydalanishi mumkinligini aniqlaydi. Kirish huquqini berish Telegram suhbatiga qo'shilishni, yig'ishni boshlashni yoki Telegram hisob qaydnomasi ruxsatlarini berishni anglatmaydi.

Kirish tanlangan ish maydonlarini, ular ichidagi tanlangan suhbatlarni, barcha ish maydonlarini yoki [hisob](https://phishdestroy.github.io/TgWitness/uz/docs/reference/accounts/#bulk-import-and-account-groups)guruhidagi har bir hisobni ochishi mumkin. **Barcha ish maydonlari, keyinchalik qo'shilganlari** ham kelajakdagi hisoblarni qamrab oladi. Guruhga berilgan kirish ham keyinchalik guruhga qo'shilgan hisoblarni qamrab oladi. Ish faqat shu ish maydonlari bilan cheklanishi kerak bo'lgan holatlarda ish maydonlarini aniq tanlang.

## Kimgadir kirish huquqini bering

1. Asosiy administrator sifatida tizimga kiring va **kirishni** oching.
2. "**Kimgadir kirish huquqini berish**" bo'limida jurnalida taniydigan nomni kiriting.
3. Ish maydonlarini tanlang va kerak bo'lganda alohida suhbatlarni ham tanlang.
4. Bu shaxs nima qilishi mumkinligini tanlang. **Ko'rish** har doim kiritilgan.
5. Muddat tugashini, tizimga kirish/sessiya limitlarini va ruxsat etilgan manzillarni zarur bo'lganda sozlang.
6. **Kirishni yaratish tugmasini** bosing. Tokenni hozir nusxalang: u faqat bir marta ko'rsatiladi.
7. Panel manzili va tokenni shaxsiy tarzda yuboring. Qabul qiluvchi o'sha tokenni odatiy kirish sahifasida kiritadi; ularga sizning asosiy panel tokeningiz yoki Telegram sessiyangiz kerak emas.

Ajratilgan token bilan panelni alohida brauzer sessiyasida oching va uni topshirishdan oldin ko'rinadigan suhbatlar va ruxsat etilgan harakatlarni tekshiring.

## Ruxsatlarni tanlang

Matnli ommaviy namoyish uchun oddiy ko'rib chiquvchi kirish o'rniga **Public showcase**-dan foydalaning. U aniq tanlangan ommaviy kanallar, saqlangan tahrirlar va o'chirishlar hamda imzolangan statistikani ko'rsatadi, muallif maydonchalari o'chirib tashlangan va fayllar API chegarasida yopiq bo'ladi. [Showcase yarating va tekshiring](https://github.com/phishdestroy/TgWitness/blob/main/docs/LIVE-SHOWCASE.md).

| Ruxsat | U nimaga imkon beradi |
| --- | --- |
| `view` | Ruxsat etilgan suhbatlar, yozib olingan xabarlar, profillar, fayllar va filtrlangan jurnal yozuvlarini o'qing. Har doim kiritilgan. |
| `export` | Suhbat tarixi va dosyealarni eksport qilishga ruxsat beriladi. Butun ish maydoni bo'yicha dalillarni eksport qilish uchun butun ish maydoniga kirish talab etiladi. |
| `sources` | Manbalarni, snapshotlarni va profilni qayd etishni boshqarish. Suhbatlar bo'yicha cheklangan kirish faqat ruxsat etilgan suhbatlarda amalga oshirilishi mumkin; hisob bo'ylab manba aniqlash va doira sozlamalari yopiq bo'lib qoladi. |
| `collect` | Yig'uvchini ishga tushiring yoki to'xtating. Yig'ish hisobga ta'sir qilgani uchun butun ish maydoni bo'yicha ruxsat talab etiladi. |
| `interact` | Kirish doirasida qo'llab-quvvatlanadigan Telegram o'zaro ta'sirlarini amalga oshiring. Chatga cheklangan kirish hisob bo'yicha havola oldindan ko'rish imkoniyatidan foydalanolmaydi. |
| `settings` | Yig'ish sozlamalari, vaqt tamg'alari, bildirishnomalar, masofaviy nusxalar va parametrlarni o'zgartiring. Butun ish maydoni bo'yicha kirish huquqini talab qiladi. |
| `account` | Telegramga kirish yoki chiqish va ulanish yo'llarini boshqarish. Butun ish maydoniga kirish huquqini talab qiladi. |
| `board.read` | Case Board eslatmalarini faqat ruxsat etilgan ish maydoni va suhbatlarda o'qing. |
| `board.write` | Belgilar, ajratmalar, bo'laklar, izohlar hamda ochilgan/ko'rib chiqilgan holatlarini qo'shish. Shuningdek, `board.read` funksiyasi ham kerak. |
| `board.manage` | To'plamlarni, jamoaning yakuniy holatlarini va boshqa ishtirokchilarning kartalarini boshqarish. Shuningdek, dosye o'qish/yozish huquqi ham talab etiladi. |

Ruxsatlar va doirasi birgalikda tekshiriladi. Ruxsatni belgilash boshqa suhbatlarni ochmaydi yoki suhbatga cheklangan kirish uchun ish maydoni bo'ylab operatsiyani yoqmaydi. Paralel eksport uchun, kirish har bir tanlangan hisobdagi eksport qilinayotgan suhbatni qamrab olishi kerak. Berilgan kirish yangi kirishlarni yaratishi, boshqa odamlarning sessiyalarini boshqarishi yoki administrator konsolini ochishi mumkin emas.

### Uchta foydali sozlama

| Shaxs | Doira | Ruxsatlar |
| --- | --- | --- |
| Ko'rib chiquvchi | Bir ish bo'yicha yozib olingan suhbatlar | `view` |
| Analitik topshiriqni tayyorlamoqda | Tergov va eksport qilish uchun suhbatlar | `view`, `export`; faqat ular Telegram orqali harakat qilishi kerak bo'lsa `interact` ni qo'shing |
| Yig'ish operatori | Tanlangan butun ish maydonchalari | `view`, `sources`, `collect`; faqat zarur bo'lganda `settings` yoki `account` ni qo'shing |

Kirish formasining boshlang'ich sozlamalariga Case Board ham kiritilgan: ko'rib chiquvchi o'qishi mumkin, tahlilchi o'qishi va yozishi mumkin, operator esa boshqarishi mumkin. Sozlamalar tahrirlanishi mumkin bo'lib qoladi va mavjud ruxsatlar avtomatik ravishda kengaytirilmaydi. Meros qilib olingan suhbat doiralari va eksport maxfiyligi uchun [Case Board-](https://phishdestroy.github.io/TgWitness/uz/docs/reference/case-board/)ga qarang.

## Cheklovlar va sessiyalar

| Sozlamalar | Qanday ishlaydi |
| --- | --- |
| Parallel sessiyalar | Bir vaqtning o'zida faol bo'lgan sessiyalar sonini 1–100 tagacha cheklang. Limitga yetganda keyingi kirishni rad eting yoki eng eski sessiyani tugating. |
| Kirishlar ruxsat etilgan | Tokenni faqat sessiyalarni boshlash uchun muvaffaqiyatli ishlatishni cheklang. Mavjud sessiyalar faqat oxirgi ruxsat etilgan kirish ishlatilgani uchun tugamaydi. |
| Amaldor | Kirish uchun mutlaq muddat cheklovi. Muddati tugagan kirish tizimga kira olmaydi va so'rovlar yuborishni davom ettira olmaydi. |
| Faoliyatsiz daqiqalar | Sessiya faoliyatsizligi vaqti tugashi, 5 daqiqadan 30 kungacha. Muvaffaqiyatli so'rovlar uni uzaytiradi; ochiq panel esa polling orqali o'z faoliyatini saqlab turishi mumkin. |
| Ruxsat etilgan manzillar | Ma'lum IP-manzillar yoki CIDR subtorlarini qabul qiling. Agar birinchi kirish bog'lanishi yoqilmagan bo'lsa, har qanday manzilga ruxsat berish uchun bo'sh qoldiring. |
| Birinchi kirishga bog'lash | Birinchi muvaffaqiyatli tizimga kirish ushbu kirish uchun ruxsat etilgan manzilni belgilaydi. |

IP — bu ilova ko'radigan mijoz manzili. Teskari proxy yoki tunnel ortida bo'lsa, IP qoidalariga tayanishdan oldin **Open sessions** bo'limida ko'rsatilgan manzilni tekshiring: aks holda bir nechta foydalanuvchilar proxy manzilini baham ko'rayotgandek ko'rinishi mumkin.

## Kirishni o'zgartirish yoki bekor qilish

**Kirishlar** bo'limida yozuvni tahrirlab uning doirasi, ruxsatlari yoki cheklovlarini o'zgartiring. Doirasi va ruxsatlardagi o'zgarishlar keyingi so'rovlarda, jumladan allaqachon ochilgan sessiyalardan keladigan so'rovlarda ham tekshiriladi. Kirishni bekor qilish uning sessiyalarini tugatadi va berilgan tokenni ishlatilmaydigan holga keltiradi. **Ochilgan sessiyalar** administratorga butun kirishni bekor qilmasdan alohida sessiyani yakunlash imkonini ham beradi.

Saqlangan eksport nusxalari ularning yaratuvchisi, ish maydoni, suhbat doirasi va zarur ruxsatlarini saqlab qoladi. Berilgan ruxsat faqat o'sha ruxsatlar amal qilayotgan paytda o'z nusxalarini ro'yxatga olish yoki yuklab olish imkonini beradi; Case Board nusxalari ham `board.read` huquqini talab qiladi. Administrator barcha nusxalarni qaytarib olishi mumkin. Ushbu metadata va guruh paketlarisiz eski nusxalar faqat administrator uchun mo'ljallangan. Yuklab olish chiptalari va tayyorlangan fayl javoblari faylni tayyorlagandan so'ng, uning baytlarini yuborishdan oldin ruxsatni qayta tekshiradi.

Bekor qilish allaqachon yuklab olingan fayllarni qaytarib ololmaydi. Tizimdan chiqish, panelni qulflash yoki sessiyani yakunlash ishlayotgan yig'uvchini to'xtatmaydi.

## Administrator nima ko'rishi mumkin

Tekshiruvchilar va tahlilchilar proxy oxir nuqtalari, pool diagnostikasi, server yo'llari yoki xom ulanish xatolarisiz to'plam holatini ko'rishadi. Ulanish diagnostikasi butun ish maydoni bo'yicha `account` ruxsatini talab qiladi. Bildirishnomani o'qish, masofaviy nusxa va parametr sozlamalari `settings` ruxsatini talab qiladi.

User-Agent to'liq brauzer satrlari kirish sessiyalarida saqlanmaydi. Yangi versiya ularni o'zgaruvchan sessiya keshidan ham olib tashlaydi. Panel jarayon logi IP-manzillarni, URL ma'lumotlarini va belgilangan sirlarni yashiradi. Mahalliy xizmat jurnalari va ilgari imzolangan jurnal yozuvlari qayta yozilmaydi. Kirish qoidalari va imzolangan tizimga kirish yozuvlari hanuzgacha mijoz manzilidan foydalanadi.

### Asosiy kalitni almashtiring

**Access → My limits → Reissue administrator key**-dan foydalaning yoki panel ishlayotgan paytda boshqariladigan o'rnatishdan `tgwitness token rotate`-ni ishga tushiring. Mavjud barcha brauzer sessiyalari, jumladan hamkasb tokenlari bilan ochilgan sessiyalar ham tugaydi. So'rov qiluvchi brauzer yangi sessiyani oladi; yangi administrator kalitini yashirishdan oldin saqlang. Berilgan hamkasb tokenlari alohida bekor qilinmaguncha amal qiladi. `TGWITNESS_TOKEN`dan foydalangan holda o'rnatish muhit sozlamasini o'zgartirishi va qayta ishga tushirishi kerak.

### So'rov va proksi chegaralari

API har bir mijoz IP manzili bo'yicha daqiqasiga 600 tagacha so'rovni qabul qiladi. Bir daqiqa ichida o'n marta rad etilgan autentifikatsiya eksponensial sovutish muddatini boshlaydi, u bir soniyadan besh daqiqagacha davom etadi. Sovutish muddati tugagach, muvaffaqiyatsiz urinish muddatni uzaytiradi; agar sovutish davrida muvaffaqiyatsiz urinish bo'lmasa, muddat qayta boshlanadi. Rad javoblari HTTP 429 va `Retry-After` kodlarini qaytaradi. Cheklovlar bir panel jarayonidagi ish maydonlari bo'ylab ulushlanadigan xotirada saqlanadi; qayta ishga tushirish ularni tozalaydi. Jonli oqimlar har bir bearer tokeni uchun to'rtta va panel jarayoni uchun 32 taga cheklangan. Oqimni ochish ham API so'rov byudjetini sarf qiladi.

Talab tanalari qabul qilish bo'yicha 60 soniyalik muddatga ega (MCP uchun 8 soniya). Har bir ilova yakunlanmagan tanalarni 32 ta so'rov va 64 MiB ajratilgan yo'l imtiyozlari bilan cheklaydi. Haddan oshgan tanalar 413 kodli xatoni, muddatdan o'tgan tanalar 408 kodli xatoni, tanalar sig'imi tugaganida esa 503 kodli xatoni va `Retry-After` parametrini qaytaradi.

Yuborilgan IP sarlavhalari e'tiborsiz qoldiriladi, agar haqiqiy TCP tengdosh `TGWITNESS_TRUSTED_PROXIES`ga tegishli bo'lmasa (vergul bilan ajratilgan IP manzillari yoki CIDRlar). `TGWITNESS_PROXY_HEADER`ni `x-forwarded-for` yoki `cf-connecting-ip`ga o'rnating. XFF yaqinroq proksidan birinchi ishonchsiz tengdoshga qarab tekshiriladi. Noto'g'ri yoki takroriy ishonchli manzil metama'lumotlari rad etiladi, shuning uchun ular ruxsat etilgan proksi manzilini meros qilib ololmaydi. Boshqariladigan tezkor tunnel mahalliy Cloudflare konnektoriga ishonadi; o'z domeni sozlamasi mahalliy Caddy'ga ishonadi. To'g'ridan-to'g'ri joylashtirishlar standart bo'yicha hech qanday proksiga ishonmaydi. Agar Uvicornni o'zingiz ishga tushirayotgan bo'lsangiz, uning proksi-sarlavha qayta ishlashini o'chirib qo'ying, shunda bu chegarada haqiqiy tengdosh olinadi.

`TGWITNESS_PANEL_ALLOWED_IPS` barcha paneldagi kirishni, jumladan administratorni ham, ro'yxatga kiritilgan IP manzillari yoki CIDR bloklariga cheklaydi. O'rnatuvchining routing-identity probe ommaviy bo'lib qoladi va hech qanday hisob ma'lumotini qaytarmaydi. Allowlistni yoqishdan oldin zarur mahalliy ma'muriy marshrutni kiritish kerak. Boshqariladigan o'rnatishning **START-HERE** qo'llanmasiga xizmat konfiguratsiyasi va tiklash bo'yicha ko'rsatmalar kiritilgan.

`ws` so'rov selektori so'rov yo'lida ish maydonini aniqlashi kerak; noma'lum, nomuvofiq va takroriy selektorlar 404 bilan rad etiladi.

Panel skriptlari va uslublari SHA-384 yaxlitlik metama'lumotlarini o'z ichiga oladi. Import-map brauzerlarning import-map yaxlitligini qo'llab-quvvatlaydiganlarida mahalliy import qilingan JS modullarini ham qamrab oladi. Dinamik ravishda hosil qilingan til javobi alohida. Ushbu tekshiruvlar yetkazib berilgan sahifaga nisbatan aktivlarning almashtirilishini aniqlaydi; ular sahifa va uning xeshlarini almashtira oladigan buzilgan serverga ishonchni o'rnatmaydi.

**Ushbu boshlanishdan beri log** jarayon yozuvlarini har bir ish maydonidan kelgan jurnal faoliyati bilan birlashtiradi: tizimga kirishlar, rad etishlar, yo'nalish o'zgarishlari va operator harakatlari. Bu joriy jarayon uchun xotiradagi konsol bo'lib, har bir xabarning doimiy nusxasi emas. Tez-tez sodir bo'ladigan xabar voqealari konsolni to'ldirish o'rniga jurnalda qoladi.

Kirishni berish, o'zgartirish va bekor qilish hamda sessiyalarni boshlash yoki yakunlash ham imzolangan `access.*` jurnal yozuvlarini yaratadi. Tokenlar ushbu yozuvlarga kiritilmaydi. Berilgan tokenlar va sessiya ma'lumotlari shifrlangan omborxonada xeshlar ko'rinishida saqlanadi.

****Asosiy administrator va ishonch chegarasi**** Asosiy panel tokeni cheklovsiz qoladi. U bilan brauzer orqali tizimga kirish administrator sozlagan sessiya cheklovlariga bo'ysunadigan sessiyalarni yaratadi. Asosiy tokenni to'g'ridan-to'g'ri yuboradigan skriptlar to'liq kirish huquqini saqlab qoladi va brauzer sessiyalari sifatida hisoblanmaydi. Bu bitta o'rnatishda ilova darajasidagi kirishni nazorat qilishdir. Barcha ish maydonchalari server jarayonini baham ko'radi; bu mezbon ma'muridan izolyatsiya emas. Asosiy token, Telegram sessiyalari, imzolash kalitlari va ma'lumotlar katalogini maxfiy saqlang. Guvoh tokeni alohida tekshiruv nuqtasi/sog'liq guvohnomasi bo'lib, panelga kirish tokeni emas.
