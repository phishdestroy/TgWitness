# Telegram · Eksport va tekshirish

Canonical page: https://phishdestroy.github.io/TgWitness/uz/docs/exports/

Kimgadir ish maydoningizga solishtirib o'zi tekshira oladigan fayllarni bering.

Manbani saqlashImzolangan ZIP-ni eksport qilingQabul qiluvchi tasdiqlaydi

Imzolar va nazorat nuqtalari sizga yangimi? [Namuna yozuvni o'zgartiring](https://phishdestroy.github.io/TgWitness/uz/docs/concepts/#chain) va qaysi tekshiruv uni ushlashini ko'ring.

Nusxani yig'uvchidan uzoqda saqlashni xohlaysizmi? [S3 sozlamalar](https://phishdestroy.github.io/TgWitness/uz/docs/exports/#s3)iga o'ting, [Object Lock](https://phishdestroy.github.io/TgWitness/uz/docs/exports/#s3-retention) yoki [tasdiqlangan tiklashni tanlang](https://phishdestroy.github.io/TgWitness/uz/docs/exports/#s3-restore).

## Ishonchli manbani saqlab qo'ying

Ish maydoni kalitining barmoq izini kollektordan boshqa joyga yozing. Yig'ish davomida imzolangan nazorat nuqtalarini ham boshqa joyda saqlang yoki [mustaqil guvoh](https://phishdestroy.github.io/TgWitness/uz/docs/witness/)ni ishga tushiring. Qabul qiluvchi kalitni va jurnalning oldingi holatini aynan shular bilan tekshiradi.

## Imzolangan ZIP-faylni yuklab oling

**Eksportlar** → imzolangan dalil ZIP. Unda butun jurnal va imzolangan fayl manifesti bor. O'qilishi oson hisobotni [Report studio](https://phishdestroy.github.io/TgWitness/uz/docs/reports/)'da shakllantiring yoki faqat tanlangan ma'lumotlarni [topshirish ekstrakti](https://phishdestroy.github.io/TgWitness/uz/docs/handover/) sifatida yuboring.

HTML, PDF va JSON hisobotlarining o'z muhrlari bor. CSV shunchaki ishchi nusxa; yaxlitlik uchun tekshirilgan ZIP ichidagi CSV'dan foydalaning.

## TgWitness'ning ishonchli nusxasi bilan tasdiqlang

Loyiha muhitida, o'z barmoq izingiz va yo'llaringiz bilan:

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
```

Muvaffaqiyatda `key_pinned: true` va `checkpoint_checked: true` ko'rinadi. Bu natijani arxiv yonida saqlang. Nazorat nuqtasi eksport oxirida yoki undan oldin bo'lishi kerak.

## Verifikatsiya natijasidan foydalaning

- **Fayllar:** manifest ularning xeshlarini, imzolar jurnalni bog'laydi. Har qanday o'zgarish ko'rinadi.
- **Shaxs:** saqlagan barmoq izingiz bu siz kutgan kalit ekanini isbotlaydi.
- **Oldingi holat:** nazorat nuqtasi eksportni topshirishdan oldin saqlangan jurnal boshi bilan solishtiradi.
- **Qamrov:** bo'shliqlar, olish natijalari va yuborish → tahrirlash → o'chirish sinovi bu sozlama haqiqatan nimani ushlaganini ko'rsatadi.

Batafsil: [tekshiruv nimani isbotlaydi va nimani isbotlamaydi](https://phishdestroy.github.io/TgWitness/uz/docs/reference/evidence/#verification-scope).

## S3 tashqi nusxasini sozlash

Ish maydoningizda **Eksportlar → Off-sayt nusxasi**. AWS S3 va har qanday S3-mos xizmat bilan ishlaydi. Jurnal segmentlari, saqlangan fayllar, vaqt belgilari bilan nazorat nuqtalari va tugallangan chat eksportlarini nusxalaydi, har biri kollektordan chiqishdan oldin `AES-256-GCM` bilan shifrlanadi.

Onlayn demo bu boshqaruvlarni yuklash o'chirilgan holda ko'rsatadi. Haqiqiy hisob ma'lumotlarini faqat o'z o'rnatmangizda kiriting.

[![To'liq Off-site nusxa paneli: oxirgi nuqta, mintaqa, bucket, kirish kalitlari, jadval, Object Lock va tiklash kaliti boshqaruvlari](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)

Kengaytirilgan ilg'or opsiyalar bilan to'liq panel. Saqlash ma'lumotlari ko'rsatilmagan.

| Maydon | Nimani kiritish |
| --- | --- |
| Oxirgi nuqta | Saqlash URL manzili, bucket yo'li yoki hisob ma'lumotlarisiz. Misol: `https://s3.example.invalid`. |
| Mintaqa | Provayderingiz talab qilgan qiymat. Standart `us-east-1`. |
| Bucket | Yozish huquqingiz bor mavjud bucket. Misol: `example-case-backup`. |
| Chelakdagi papka | Prefiks, standart `tgwitness`. Uning ustiga har bir ish maydoni prefiksi qo'shiladi. |
| Kirish kaliti ID / Maxfiy kirish kaliti | Ikkalasi birga, seyfda saqlanadi. Keyinroq ikkalasini bo'sh qoldirsangiz, saqlanib qoladi. |
| Yo'l-uslubidagi manzillar | Yoqilgan: `endpoint/bucket`. O'chirilgan: `bucket.endpoint`. Provayderga bog'liq. |
| Ko'chirma oraligi | 1 dan 1,440 daqiqagacha, standart 5. Faqat ilova ishlayotganda. |
| Object Lock saqlash | Kunlar va rejim, agar bucket Object Lock'ni qo'llasa. Nol bucket standartini saqlaydi. |

1. Bucket yarating, **Off-sayt nusxasini saqlash** belgilanmagan holda manzil va hisob ma'lumotlarini to'ldiring, **Off-sayt nusxasini saqlash** tugmasini bosing.
2. **Ulanishni sinash** shifrlangan sinov obyektini yuklaydi.
3. **Shifrlash kalitini yuklab olish** va uni kollektordan uzoqda saqlang. Kalit yo'q, tiklash yo'q.
4. **Off-sayt nusxasini saqlash**ni belgilang, saqlang, so'ng **Hozir nusxalash** yoki jadval ishlasin.

## Saqlash muddatini va nusxa ko'chirish jarayonini tekshirish

**Boshqa variantlar** ostida saqlash kunlarini va `GOVERNANCE` yoki `COMPLIANCE`ni tanlang. TgWitness saqlash sozlamasini yuklangan obyektdan qayta o'qiydi va aytadi: tasdiqlandi, yo'q yoki tekshiruv muvaffaqiyatsiz.

Panel oxirgi o'tishni, obyektlar sonini, baytlarni, nusxalangan jurnal chegarasini va xatolarni ko'rsatadi. Yo'qolgan mahalliy fayl xabar qilinadi va keyingi o'tishda qayta uriniladi, qolgani nusxalanishda davom etadi.

Yuklashlar to'g'ridan-to'g'ri, SOCKS5 yoki HTTP orqali o'tadi. Faqat MTProxy marshrutida nusxa xato bilan kutadi.

## Qayta tiklash kalitini alohida saqlang

Kalit JSON'ida shifrni ochish kaliti, manzil, prefiks va kalit barmoq izi bor. Tiklash uchun u va o'qish huquqli saqlash hisob ma'lumotlari kerak.

Endpoint, bucket yoki prefiksni o'zgartirdingizmi? Kalitni qayta yuklab oling. Yangi nusxa yangi manzilda boshlanadi; eski chat eksportlari joyida qoladi.

## Boshqa qurilmada tiklash va tekshirish

Sizga ishonchli TgWitness o'rnatmasi, kalit JSON, faqat o'qish uchun saqlash hisob ma'lumotlari va bo'sh papka kerak:

### Windows PowerShell

```
$env:TGWITNESS_S3_ACCESS_KEY = 'YOUR_READ_ACCESS_KEY'
$env:TGWITNESS_S3_SECRET_KEY = 'YOUR_READ_SECRET_KEY'
python -m tgwitness.replica restore --key-file tgwitness-replica-key.json --out restored-evidence
```

### Linux / macOS

```
export TGWITNESS_S3_ACCESS_KEY='YOUR_READ_ACCESS_KEY'
export TGWITNESS_S3_SECRET_KEY='YOUR_READ_SECRET_KEY'
python -m tgwitness.replica restore --key-file tgwitness-replica-key.json --out restored-evidence
```

Hammasi avval shaxsiy vaqtinchalik papkada tekshiriladi: butun jurnal, nazorat nuqtalari, fayl xeshlari va o'lchamlari. Xavfli yo'llar, ziddiyatli segmentlar yoki nazorat nuqtasidan qisqa jurnal muvaffaqiyatsiz bo'ladi va shunda hech narsa yozilmaydi.

Muvaffaqiyatda `events.jsonl`, `media/`, `checkpoints/` va `exports/` olasiz. Buyruqning JSON natijasini ular bilan saqlang va o'zingiz saqlagan nazorat nuqtalari yoki guvoh yozuvlari bilan solishtiring.
