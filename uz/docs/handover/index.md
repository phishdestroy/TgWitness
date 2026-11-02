# Ulashish uchun nusxa tayyorlang

Canonical page: https://phishdestroy.github.io/TgWitness/uz/docs/handover/

Asl ish maydonini saqlagan holda tegishli kuzatuvlarni ulashing.

Handover alohida imzolangan qismdir. Suhbatlar va ishtirokchilarni tanlang, identifikatorlar yoki matnni qisqartiring va qaysi fayllar hamda jamoa eslatmalari qabul qiluvchining nusxasiga kirishini aniqlang. Uning manifesti tanlovni hamda o'zgarmagan, qisqartirilgan va o'tkazib yuborilgan yozuvlar sonini qayd etadi.

## Qabul qiluvchining ekstraktini tayyorlang

1. **Exportlar → Handover ekstraktini** oching. Uning maqsadini yozing, suhbatlarni va ixtiyoriy UTC davrini tanlang, so'ng agar nomlangan sub'ektlar kerak bo'lsa, **tanlangan suhbatlardagi odamlarni yuklashni** tanlang.
2. Boshqalar bilan qanday muomala qilishni tanlang: taxalluslar, ularning xabarlarini o'chirish yoki yozib olingan holda ko'rsatish. Xabar matni va ilovalarni mustaqil sozlang; ixtiyoriy ravishda telefon raqamlari va elektron pochta manzillarini yashirish mumkin.
3. Case Board kitob belgilari va bo'laklarini yoki izohli kartochkalarni kiritishni tanlang. Tergovchi taxalluslari ushbu nusxada jamoa nomlarini almashtirishi mumkin.
4. **Yuklab olish handover ekstraktini** tanlang. Hosil qilingan hisobot va tanlangan yozuvlarni mahalliy ravishda oching, arxivni tekshiring va jo'natishdan oldin nusxani ko'rib chiqing.

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
| Odamlar | Tanlangan sub'ektlarni aniqlash mumkin bo'ladigan qilib saqlang; boshqa ishtirokchilarni xohishga ko'ra psevdonimlashtiring yoki chiqarib tashlang. |
| Matn | Barcha matnni, faqat tanlangan shaxslar va kuzatuv hisobidagi matnni kiritish yoki xabar matni va matnni o'z ichiga olgan tafsilotli maydonlarni o'chirib tashlash. |
| Fayllar | Tanlangan shaxslar va kuzatuv hisobvarag'i fayllarini tanlang, barcha ko'rsatilgan xabarlar fayllarini yoki hech qanday faylni tanlamang. |
| Case Board | Board materiallarini, belgilamalarni va bo'laklarni yoki jamoaviy muhokama kartalarini tanlamang. |

Erkin shakldagi matn va fayl mazmunini hamda identifikatorlarni ko'rib chiqing: psevdonim xabarda yoki ilovada yozilgan har bir nomni avtomatik ravishda olib tashlamaydi. Agar tanlangan saqlangan fayl mavjud bo'lmasa, uni tiklang yoki ekstraktni yaratishdan oldin ilovalarni aniq belgilab chiqarib tashlang.

## Matnni mustaqil ravishda tekshirish mumkin bo'lgan holda saqlang

```
python -m tgwitness.verify handover.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256
```

Asl imzolangan dalillar arxivi va tekshiruv nuqtalarini alohida saqlang. Topshirish o'z proyeksiyasini qayd etadi, shunda qabul qiluvchi butun ish maydonini olmasdan yetkazib berilgan nusxani tekshirishi mumkin. [Report studio](https://phishdestroy.github.io/TgWitness/uz/docs/reports/) o'zining o'qish dizaynini taqdim etadi; [eksportni tasdiqlash](https://phishdestroy.github.io/TgWitness/uz/docs/exports/) ishonchli manbalarni tushuntiradi.
