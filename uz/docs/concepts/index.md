# Telegram · Dalillar qanday ishlashini ko'ring

Canonical page: https://phishdestroy.github.io/TgWitness/uz/docs/concepts/

Xabarlar o'zgaradi. Ko'rganingiz haqidagi yozuv o'zgarmasligi kerak, va buni istalgan kishi tekshira olishi kerak.

Quyida ikkita kichik tajriba. Soxta xabarlar, hammasi brauzeringizda ishlaydi, Telegram'ga hech narsa ketmaydi.

## Suhbat eksportidan tekshiriladigan yozuvga

[Telegram Desktop eksporti](https://telegram.org/blog/export-and-more) hozir ko'rinib turgan tarixni HTML yoki JSON sifatida saqlaydi. TgWitness o'zgarishlarning uzluksiz jurnalini, har bir yozuvdagi imzolarni va boshqalar solishtira oladigan nazorat nuqtalarini qo'shadi.

| Vazifa | Telegram Desktop eksporti | TgWitness |
| --- | --- | --- |
| Saqlangan suhbatlarni o'qish | HTML yoki JSON tanlangan media bilan | Saqlangan suhbatlar, qidiriladigan jurnal va oflayn hisobotlar |
| Vaqt o'tishi bilan o'zgarishni kuzating | Eksport qilganda mavjud bo'lgan tarix | Eski versiyalar, keyingi tahrirlar va o'chirishlar, hammasi saqlanadi |
| Topshiruvdan so'ng fayllarni tekshiring | Standart HTML/JSON eksport fayllari imzolangan emas | Imzolangan manifest, imzolangan yozuvlar va muhrlangan hisobotlar, ishonchli kalit bilan tekshiriladi |
| Oldingi saqlangan holat bilan solishtiring | Alohida referens nusxa yoki xeshni saqlang | Imzolangan tekshiruv nuqtalari, alohida guvoh va ixtiyoriy tashqi vaqt belgilari |

Taqqoslash 2026-yil 2-noyabr holatiga ko'ra [Telegram Desktop eksport kodi](https://github.com/telegramdesktop/tdesktop/tree/768d47cda6c7f447c10a25d1f363279493a90ed7/Telegram/SourceFiles/export/output)ga asoslangan.

## Bir xabar, uch kuzatuv

Yangi xabar, tahrir va o'chirish uchta alohida yozuvga aylanadi. Tahrir birinchisining ustidan yozmaydi, o'chirish ham uni yo'q qilmaydi.

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

Telegram xabarni kim yoki aynan qachon o'chirganini aytmaydi. TgWitness taxmin qilish o'rniga bu maydonlarni bo'sh qoldiradi.

## Yozuvni o'zgartiring. Hashni kuzating.

Har bir yozuvda oldingisining xeshi bor. Boshqa joyda saqlangan nazorat nuqtasi jurnal uzunligi va oxirgi xeshni mahkamlaydi.

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

**C** to'qqizta hodisa maydoni UTF-8 JSON ko'rinishida: kalitlar tartiblangan, ortiqcha bo'shliq yo'q, ASCII escaping yo'q, NaN/cheksizlik yo'q. `previous_hash` bu hi−1, h0 64 ta nol, imzolar digestning 32 ta xom baytini qamraydi.

Maydonlar: `seq`, `observed_at`, `source_at`, `kind`, `chat_id`, `message_id`, `actor_id`, `payload`, `previous_hash`. To'liq spetsifikatsiya: [hodisa kodlanishi](https://phishdestroy.github.io/TgWitness/uz/docs/reference/evidence/#event-canonicalization).

SAQLANGAN NAZORAT NUQTASI

Nexport ≥ Ncheckpoint
hexport[Ncheckpoint] = Hcheckpoint

Nazorat nuqtasi imzosini mahkamlangan kalit bilan tekshiring, so'ng uni jurnal bilan solishtiring. Keyingi eksport uzunroq bo'lishi mumkin, lekin nazorat nuqtasida mos kelishi shart.

## Uchta savol, uch xil tekshiruv

[01 / BUTUNLIK**Bu yozuv o'zgardi-mi?** Siz ishonadigan kalitga nisbatan xeshlar va imzolar.](https://phishdestroy.github.io/TgWitness/uz/docs/exports/)[02 / DAVOMI**Avval nimalar saqlangan edi?** Eksportni guvoh saqlagan nazorat nuqtalari bilan solishtiring.](https://phishdestroy.github.io/TgWitness/uz/docs/witness/)[03 / ETKAZIB BERISH**Bu test voqealari yetib keldimi?** Sinov xabarlarini yuboring, tahrirlang va o'chiring, har bir hisob nimani ushlaganini ko'ring.](https://phishdestroy.github.io/TgWitness/uz/docs/cases/)

Imzolar "o'zgartirilganmi" degan savolga, nazorat nuqtalari "avvalgisiga mos keladimi" degan savolga, sinov xabarlari "hammasini ushladikmi" degan savolga javob beradi. [Tekshiruv nimani isbotlaydi va nimani isbotlamaydi.](https://phishdestroy.github.io/TgWitness/uz/docs/reference/evidence/#verification-scope)

Keyingisi: boshidan ish paketigacha [butun hisob bo'yicha tergov](https://phishdestroy.github.io/TgWitness/uz/docs/cases/).

[Export Clinic: watch the controlled Desktop experiment](https://phishdestroy.github.io/TgWitness/docs/export-clinic/). Compare the two-minute film, the original recording and seven pairs of test exports. Local modification is disclosed.
