# Ulashish uchun nusxa tayyorlang

Canonical page: https://phishdestroy.github.io/TgWitness/uz/docs/handover/

Faqat keraklisini ulashing, asl nusxa daxlsiz qoladi.

Topshirish alohida imzolangan ekstrakt: chatlar va odamlarni tanlang, shaxslar yoki matnni yashiring, fayllar va jamoa eslatmalarini tanlang. Manifest nima saqlangan, qisqartirilgan va chiqarib tashlanganini qayd etadi.

## Qabul qiluvchining ekstraktini tayyorlang

1. **Eksportlar → Topshirish ekstrakti**: maqsadni yozing, chatlar va davrni tanlang, ismli odamlar kerak bo'lsa **Tanlangan chatlardagi odamlarni yuklash**.
2. Qolgan hammasi: taxalluslar, chiqarib tashlangan yoki yozilganidek. Matn va fayllar alohida kalitlar; telefonlar va e-pochtalarni niqoblash mumkin.
3. Case Board: hech narsa, xatcho'plar va kesimlar yoki izohli kartalar. Jamoa ismlarini taxalluslarga almashtirish mumkin.
4. **Topshirish ekstraktini yuklab olish**, oching, tekshiring, yuborishdan oldin ko'zdan kechiring.

### Bir asl nusxa, ataylab ulashish uchun mo'ljallangan nusxa

Sun'iy misol · faqat identifikatsiya uchun illyustratsiya

1. **Tanlang.** Ish suhbatini kiritib, ekstrakt qaysi shaxs haqida ekanligini aniqlang.
2. **Minimalizatsiya.** Ulashish nusxasida boshqa ishtirokchi qanday ko'rinishini tanlang.
3. **Tekshirish.** Yuborishdan oldin hosil qilingan arxivning hisobotini va yozuvlarini oching.
4. **Ulaing.** Tekshirilgan nusxani yetkazib, uning ishonchli barmoq izini alohida xabar qiling.

#### Asl kuzatuv

Nora · foydalanuvchi 71002

"Men yangilangan havolani oldim."

Manba jurnali ushbu saqlangan kuzatuvni saqlaydi.

#### Qabul qiluvchining nusxasi

Yozib olinganidek ko'rsating: Nora · foydalanuvchi 71002 · "Men yangilangan havolani oldim."

Psevdonim: P01 · "Men yangilangan havolani oldim."

Omit: ushbu ishtirokchining xabari nusxadan chiqarib tashlanadi.

#### Haqiqiy fayllarni tekshiring

report.html va records.json fayllarini o'qing.

Identitetlarni, matnni, ilovalarni va ixtiyoriy jamoa izohlarini tekshiring.

#### Imzolangan ekstrakt

Tanlov + fayl hashlar + imzolangan manifest

Manba jurnali chegarasiga bog'langan alohida paket

## Boshqaruv elementlarini birgalikda ishlating

| Boshqaruv | Matnga ta'sir |
| --- | --- |
| Odamlar | Tanlangan odamlar ismi bilan qoladi; boshqalar taxallus oladi yoki chiqarib tashlanadi. |
| Matn | Barcha matn, faqat tanlangan odamlar va hisobingiz matni yoki hech narsa. |
| Fayllar | Tanlangan odamlar va hisobingiz fayllari, barcha ko'rsatilgan fayllar yoki hech narsa. |
| Case Board | Hech narsa, xatcho'plar va kesimlar yoki muhokamali kartalar. |

Matn va fayllarni ham o'qing: taxallus xabar yoki ilova ichida yozilgan ismlarni olib tashlamaydi. Tanlangan fayl yo'q bo'lsa, uni tiklang yoki ilovalarni chiqarib tashlang.

## Matnni mustaqil ravishda tekshirish mumkin bo'lgan holda saqlang

```
python -m tgwitness.verify handover.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256
```

Asl arxiv va nazorat nuqtalarini o'zingiz saqlang. Qabul qiluvchi butun ish maydonini olmasdan o'z nusxasini tekshira oladi. Dizayn: [Report studio](https://phishdestroy.github.io/TgWitness/uz/docs/reports/). Ishonchli ma'lumotnomalar: [eksportni tekshirish](https://phishdestroy.github.io/TgWitness/uz/docs/exports/).
