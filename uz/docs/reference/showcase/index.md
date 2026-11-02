# Jamoat namoyishi

Canonical page: https://phishdestroy.github.io/TgWitness/uz/docs/reference/showcase/

Tanlangan ommaviy kanallarning saqlangan xabarlari va imzolangan snapshotlarini muddati tugaydigan, bekor qilinishi mumkin bo&#x27;lgan havolalar orqali e&#x27;lon qiling.

**Kirish → Jamoat namoyishi** mavjud access-token tizimidan foydalangan holda alohida, faqat o'qish uchun mo'ljallangan sahifa yaratadi. U o'rnatmaning saqlangan kuzatuvlarini o'qiydi. U kollektorni ishga tushirmaydi, Telegramga kirishni amalga oshirmaydi yoki tashrif buyuruvchi uchun kanalni olmadi.

## Sahifani nashr qiling

1. Ko'rsatmoqchi bo'lgan har bir ommaviy kanal uchun manba profilini saqlang. Kanal quyidagilarga ega bo'lishi kerak: o'zining so'nggi saqlangan profilida ommaviy foydalanuvchi nomi; guruhlar va xususiy suhbatlar mos kelmaydi.
2. Ochiq **kirish → Jamoat namoyishi** (yoki `/showcase-manage.html`) ma'mur sifatida.
3. 16 tagacha ish maydonida kanallarni tanlang, ommaviy sahifa sarlavhasini kiriting va havolaning amal qilish muddatini 1, 7 yoki 30 kun etarlicha belgilang. Ichki ish maydoni yorliqlari e'lon qilinmaydi. 64 tagacha kanal kiritilishi mumkin.
4. Nashr uchun tanlangan kanallar matnini ko'rib chiqing, so'ngra "**Tanlangan yozuvlarni ko'rib chiqish"** tugmasini bosing. Ko'rib chiqish tashrifchi sahifasidagi kabi server tomonidagi proyeksiyani ishlatadi.
5. **"Create showcase" havolasini** bosing. Havola ko'rinib turgan paytda uni nusxalab oling. Uni tarqatishdan oldin alohida brauzerda ochib, qabul qiluvchining sahifasini ko'rib chiqing.

Havo URL bo'lagida kirish tokeni mavjud. Sahifa API so'rovlarini yuborishdan oldin bo'lakni olib tashlaydi va uni brauzer sessiyasiga almashtiradi. Havo ulgurgan har kim tanlangan materialni muddati tugaguncha yoki bekor qilinguncha ochishi mumkin. Yangi havolalar 100 ta bir vaqtning o'zidagi sessiyaga ruxsat beradi, har biri eng ko'pi bilan bir soat davom etadi. Mavjud Kirish nazoratlari grant API orqali manzil cheklovlari va tizimga kirish limitlarini ham joriy qilishi mumkin. Oddiy ko'rib chiquvchi kirish alohida rejim bo'lib, u hanuzgacha asl ruxsat etilgan xabarlar va fayllarni o'z ichiga oladi.

## Mehmonlar nima ko'radi

| Ko'rinadigan | Maxfiy saqlanadi |
| --- | --- |
| Tanlangan ommaviy kanal sarlavhalari, foydalanuvchi nomlari va profil kuzatilgan sanalar | Hisob identifikatorlari, ichki ish maydoni yorliqlari va tanlanmagan manbalar |
| Yozib olingan matn va har bir saqlangan tahrir | Tuzilgan jo'natuvchi identifikatorlari, ismlar, foydalanuvchi nomlari, telefon raqamlari va profil qiymatlari |
| Agar mavjud bo'lsa, avval saqlangan matn bilan o'chirish kuzatuvlari | Ilovalar, avatarlar, kichik rasmlar, fayl nomlari va asl yuklamalar |
| Muallif/profil yoki ilova yozib olinganini bildiruvchi belgilovchilar | Yo'naltirish va javob metama'lumotlari, tarmoq yo'llari, IP manzillari va kirish ma'lumotlari |
| Tanlangan kanal voqealari soni, joriy yig'ish kalitlari, yurak urishi va tekshiruv nuqtasi oralig'i | Yig'ish boshqaruvlari va oddiy dalillarni eksport qilish API-lari |
| Imzolash barmoq izi, jurnal tekshiruv nuqtasi va izchillik isboti | Imzolash kalitlari va Telegram sessiyalari |

**Ochiq xabar matni avtomatik ravishda anonimlashtirilmaydi.** Xabarga yozilgan ism, tilga olish, telefon raqami yoki havola matnning bir qismi bo'lib qoladi. `Redacted`tuzilgan muallif/profil maydonlariga ham tegishli. Nashr etishdan oldin saqlangan tahrirlar va o'chirishlarni ham o'z ichiga olgan haqiqiy tanlangan kontentni ko'rib chiqing.

Moslik **so'nggi saqlangan manba profil**ini aks ettiradi, jonli Telegram qidiruvini emas. Agar keyingi profil endi ommaviy kanal foydalanuvchi nomiga ega bo'lmasa, yangi so'rovlar kanalni istisno qiladi. Manba profillarini ommaviy ko'rinish o'zgarganda yangilang. O'quvchilarda ilgari olgan materiallari allaqachon saqlangan bo'lishi mumkin.

Asl imzolangan yozuvlar o'zgarmas holda qoladi. Ko'rsatilgan proyeksiya alohida imzolanadi va uning asl yozuvlarga havola qiluvchi xeshlarini o'z ichiga oladi. Proyeksiya imzosi ko'rsatilgan bayonotni tasdiqlaydi; bu tahrirlangan baytlar ustidagi asl voqeaning imzosi emas.

## Imzolar va uzluksizlikni tekshiring

**Izzat izi va imzolangan tekshiruv nuqtasini** kengaytiring va snapshotni yuklab oling. Sahifa yangilangach, yuklab olish avvalgi brauzer snapshoti va ularning jurnal chegaralari orasidagi Merkle moslik isbotini o'z ichiga oladi. Avtomatik yangilanish sahifa ko'rinib turgan va kuzatuvlarning birinchi sahifasini ko'rsatayotgan paytda har daqiqada bir marta amalga oshiriladi.

TgWitness o'rnatilgan bo'lsa, yuklab olingan faylni oflayn tarzda tekshiring:

```
python -m tgwitness.showcase_verify showcase.json --fingerprint TRUSTED_COLLECTOR_SHA256
```

Barmoq izi alohida ishonchli manbadan olinishi kerak. O'zingiz saqlagan snapshot bilan solishtirish uchun `--previous earlier.json`; bu yuklab olish ichida keltirilgan avvalgi snapshot ustidan ustun keladi. Joriy isbot o'sha saqlangan chegaradan boshlanishi kerak. Tasdiqlangan mijozlar ushbu isbotni quyidagi usul bilan so'rashi mumkin `GET /api/showcase/{workspace_id}?challenge=<32-hex-random>&from_count=<retained-count>`. Qisqaroq jurnal chegarani jimjit qayta tiklash o'rniga HTTP 409 kodini qaytaradi.

Imzolangan tekshiruv nuqtasi **butun kollektor**jurnaliga, jumladan uning yozuvlar soni va tushunarsiz sarlavha xeshiga yozib qo'yiladi. Ko'rsatilgan xabar sonlari faqat tanlangan ommaviy kanallarga tegishli. Sahifa hech qachon boshqa jurnalning mazmunini ro'yxatlamaydi. Bu voqealar soni, noyob xabarlar soni emas. Sozlamalar joriy konfiguratsiyani, avvalgi har bir yozib olish oralig'ini emas, tasvirlaydi.

Imzo va izchillikni tekshirish saqlangan chegaraga nisbatan o'zgarishlarni aniqlay oladi. U mustaqil ravishda imzolangan hisoblagichlarni qayta hisoblamaydi, Telegram kelib chiqishini tasdiqlamaydi, uzluksiz yozib olishni namoyish etmaydi yoki mustaqil guvohni almashtirmaydi. Shu ko'rib chiqish uchun [dalillarni tekshiruvchi](https://github.com/phishdestroy/TgWitness/blob/main/docs/TRUST.md), [mustaqil guvoh](https://phishdestroy.github.io/TgWitness/uz/docs/reference/witness/) va [sinovdan o'tgan miqyos yozuvidan](https://phishdestroy.github.io/TgWitness/uz/docs/reference/verification/) foydalaning. Sun'iy o'rnatmalar ko'rinadigan tarzda "sun'iy" deb belgilangan.

## Sahifani bekor qiling yoki mezbonlik qiling

Showcase menejerida yoki mavjud **Access** bo'limida **Revoke'dan** foydalanib havolani yoping va barcha sessiyalarni yakunlang. Kiruvchi, kirish tugaganini aniqlagan so'rov orqali ko'rsatilgan yozuvlarni o'chiradi. Har bir so'rovda muddat va ruxsatlar tekshiriladi. Showcase grantlarini oddiy panelga kirishga aylantirib bo'lmaydi; rejimni o'zgartirish uchun yangi grant yarating.

Sahifani o'rnatishning mavjud HTTPS manzili orqali yetkazib bering. Havola chop etish yangi port ochmaydi, tunnel yaratmaydi yoki DNSni o'zgartirmaydi. HTML va API foydalanuvchining o'rnatmasida qoladi. Showcase tashrifchisi ushbu kirish bilan oddiy xabar, profil, media, eksport yoki boshqaruv APIlaridan foydalana olmaydi.

## Mahalliy regressiya tekshiruvlari

```
python tools/check_showcase.py
python tools/check_showcase_browser.py
```

Ikkalasi ham sintetik yozuvlar va mahalliy HTTP-serverdan foydalanadi. Ular Telegramga ulanmaydi.
