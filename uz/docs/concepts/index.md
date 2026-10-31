# Dalillar qanday ishlashini ko'ring

Canonical page: https://phishdestroy.github.io/TgWitness/uz/docs/concepts/

Xabar o'zgarishi mumkin. Siz kuzatgan narsalarning yozuvi tekshirib ko'rilishi mumkin bo'lib qolishi kerak.

Quyida ikkita kichik tajribani o'rganing. Ular badiiy xabarlarni ishlatadi, brauzeringizda qoladi va hech qachon Telegramga ulanmaydi.

## Bir xabar, uch kuzatuv

Telegram yangi xabar, tahrir va o'chirish bildirishnomasini yetkazganda, yig'uvchi uchta alohida kuzatuvni qo'shadi. Tahrir birinchi yozuvni almashtirmaydi. O'chirish bildirishnomasi uni o'chirib tashlamaydi.

01 / XABAR SAFARIIllyustrativ ketma-ketlik

Telegram delivers an update to the collector, which appends a journal record. · Telegram · Yig'uvchi · Jurnal · yangilash → · qo'shish →

Joriy suhbat ko'rinishi Xabar #42

Xabar o'chirildi

Xabar suhbat ko'rinishidan yo'qoldi.

KUZATISH JURNALI 3 yozuv

1. 01

   `message.new`

   10:00 da uchrashing

   ✓
2. 02

   `message.edited`

   11:00 da uchrashing

   ✓
3. 03

   `message.deleted`

   #42 uchun o'chirish bildirishnomas

   ✓

Uchala qabul qilingan kuzatuvlar jurnalda saqlanadi.

Allaqachon tanlangan bitta manba uchun soddalashtirilgan yo'l. Operatsion yozuvlar ham haqiqiy jurnalni baham ko'radi. Qayd qilish hisob qaydnomasi nima ko'rishi va Telegram nima yetkazishiga bog'liq.

O'chirish bildirishnomasi na ishonchli o'chirish vaqtini, na xabarni o'chirgan shaxsni ko'rsatmaydi. Ushbu qiymatlarni noma'lum saqlash kuzatuv bilan taxmin o'rtasidagi farqni saqlab qoladi.

## Yozuvni o'zgartiring. Hashni kuzating.

Har bir yozuv oldingi yozuvning hashini o'z ichiga oladi. Uning o'z hashi, shu havolani ham o'z ichiga olgan holda, voqea maydonlarini qamrab oladi. Tashqarida saqlanadigan tekshiruv nuqtasi jurnalning ma'lum uzunligi va boshlang'ich hashini belgilaydi.

02 / HASH-ZAJIR SANDBOXHaqiqiy SHA-256 · namunaviy yozuvlar

Yozuv 01**Xabar qabul qilindi**`h₁ = SHA-256(e₁)`64 ta nolga havolalar

Yozuv 02**11:00 da uchrashing**`h₂ = SHA-256(e₂)`h₁ ni o'z ichiga oladi

Yozuv 03**O'chirish kuzatildi**`h₃ = SHA-256(e₃)`h₂ ni o'z ichiga oladi

Boshqa joyda saqlangan**3 yozuv · bosh `h₃`**Ushbu belgilangan chegarani taqdim etilgan jurnal bilan solishtiring.

Voqeani o'zgartirish uning hashini o'zgartiradi. Zanjirni qayta qurish uning boshini o'zgartiradi. Oxirini olib tashlash uni saqlangan tekshiruv nuqtasidan qisqaroq qiladi.

**2-yozuvni va to'liq hashlarni tekshiring**

Bu misolda ko'rsatilgan aniq UTF-8 JSON hashi. Qadriyatlar tasodifiy; to'qqizta maydon va serializatsiya jurnal formatiga mos keladi.

```

```

Saqlangan yozuv 2 xesh

``

Yozuv 2 hashni qayta hisobladi

``

Ushbu sandbox hashlarni hisoblaydi, imzolarni emas. Haqiqiy verifikator har bir voqeaning Ed25519 imzosini, ketma-ketligini va bog'lanishini ham tekshiradi. Hashlarni qayta tuzish ishonchli kalit ostida haqiqiy imzolarni yaratmaydi.

## Asl qoidalar, bir necha satrda

HASH + IMZO

h0 = 064
hi = hex(SHA-256(C(ei)))
σi = Ed25519.Sign(sk, unhex(hi))

**C** to'qqizta voqea maydonini UTF-8 JSON shaklida serializatsiya qiladi: tartiblangan kalitlar, ortiqcha bo'shliqlar yo'q, ASCII qochirish yo'q va NaN/cheksizlik yo'q. Voqeaning `previous_hash` hi−1 ga teng. Ko'rsatilgan h0 esa 64 ta nol belgisini anglatadi; imzo esa 32 ta xom digest baytlarini qamrab oladi.

To'qqizta maydon: `seq`, `observed_at`, `source_at`, `kind`, `chat_id`, `message_id`, `actor_id`, `payload` va `previous_hash`. Bu TgWitness'ning [hujjatlashtirilgan JSON kod](https://phishdestroy.github.io/TgWitness/uz/docs/reference/evidence/#event-canonicalization)lashidir; hash va imzo o'zlari hash-kirish maydonlari emas.

SAQLANGAN NAZORAT NUQTASI

Nexport ≥ Ncheckpoint
hexport[Ncheckpoint] = Hcheckpoint

Mahkamlangan yig'uvchi kalit ostidagi tekshiruv nuqtasi imzosini tasdiqlang, so'ng uning chegarasini tasdiqlangan jurnal bilan solishtiring. Keyingi eksport ko'proq yozuvlarni o'z ichiga olishi mumkin; u baribir avvalgi tekshiruv nuqtasida mos kelishi kerak.

## Uchta savol, uch xil tekshiruv

[01 / BUTUNLIK**Bu yozuv o'zgardi-mi?** Hashlar va imzolarni alohida ishonchli kalitga qarshi tekshiring.](https://phishdestroy.github.io/TgWitness/uz/docs/exports/)[02 / DAVOMI**Avval nimalar saqlangan edi?** Imzolangan eksportni alohida guvoh tomonidan saqlangan tekshiruv nuqtalari bilan solishtiring.](https://phishdestroy.github.io/TgWitness/uz/docs/witness/)[03 / ETKAZIB BERISH**Bu test voqealari yetib keldimi?** Har bir akkaunt jurnalida amalga oshirilgan jo'natish, tahrirlash va o'chirish harakatlarini mos keltiring.](https://phishdestroy.github.io/TgWitness/uz/docs/cases/)

Mos keladigan xesh zanjiri yaxlitlik savoliga javob beradi. U Telegram xabarining to'liq yetkazilganini, xabar haqiqatini yoki mustaqil ishonchli kuzatuv vaqtini aniqlamaydi.

[Hisobni to'liq o'rganish](https://phishdestroy.github.io/TgWitness/uz/docs/cases/)ni ma'lumotlarni olishdan ish hujjatlari paketini tayyorlashgacha kuzating.
