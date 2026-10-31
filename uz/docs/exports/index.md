# Eksport va tekshirish

Canonical page: https://phishdestroy.github.io/TgWitness/uz/docs/exports/

Imzolangan yozuvni ulashing, boshqalar uni tekshira oladi.

Manbani saqlashImzolangan ZIP-ni eksport qilingQabul qiluvchi tasdiqlaydi

Imzolar va tekshiruv nuqtalariga yangi boshlamoqdamisiz? [Namuna yozuvni o'zgartiring](https://phishdestroy.github.io/TgWitness/uz/docs/concepts/#chain) va qaysi tekshiruvlar uni aniqlashini ko'ring.

Nusxani yig'uvchidan uzoqda saqlashni xohlaysizmi? [S3 sozlamalar](https://phishdestroy.github.io/TgWitness/uz/docs/exports/#s3)iga o'ting, [Object Lock](https://phishdestroy.github.io/TgWitness/uz/docs/exports/#s3-retention) yoki [tasdiqlangan tiklashni tanlang](https://phishdestroy.github.io/TgWitness/uz/docs/exports/#s3-restore).

## Ishonchli manbani saqlab qo'ying

Ish maydonining jamoat kaliti barmoq izini yig'uvchidan tashqarida saqlang. Yig'ish jarayonida imzolangan tekshiruv nuqtalarini boshqa joyda saqlang yoki [mustaqil guvoh](https://phishdestroy.github.io/TgWitness/uz/docs/witness/)dan foydalaning. Ushbu havolalar qabul qiluvchiga kalitni va avvalgi jurnal chegarasini tekshirish imkonini beradi.

## Imzolangan ZIP-faylni yuklab oling

**Eksportni** oching va imzolangan dalillar ZIP-faylini yarating. Unda ish maydoni jurnali va imzolangan fayllar manifesti mavjud. Panel filtrlari bu to'liq jurnal eksportini cheklamaydi: materialni ulashishdan oldin ko'rib chiqing.

Mustaqil HTML va CSV yuklab olishlari o'qish va tahlil qilish uchun foydalidir. Imzolangan ZIP-ni tekshiriladigan asl nusxa sifatida saqlang; alohida HTML yoki CSV faylda mustaqil imzo yo'q.

## TgWitness'ning ishonchli nusxasi bilan tasdiqlang

O'rnatilgan loyiha muhitida namunaviy barmoq izi va fayl yo'llarini quyidagilar bilan almashtiring:

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
```

Ikkala havola ham o'tganida, natija `key_pinned: true` va `checkpoint_checked: true` ni qayta hisobot beradi. Verifikatsiya natijasini asl arxiv bilan birga saqlang. Saqlangan tekshiruv nuqtasi eksport chegarasida yoki undan oldin bo'lishi kerak.

## Natijani tushunish

- **Buzilmaslik:** qayd etilgan tarix va eksport qilingan fayllar o'z imzolari bilan mos keladi.
- **Oldingi kuzatuv:** tashqi nazorat nuqtasi eksportni oldin saqlangan jurnal prefiksi bilan solishtirishga imkon beradi.
- **Yetkazib berish:** nazorat ostida jo'natish → tahrirlash → o'chirish testi yozib olingan yozuv bilan ma'lum voqealarni tekshiradi.

Amaldagi imzo har bir Telegram hodisasining yetib kelganini, manbaning rost gapirganini yoki yig'uvchining soati to'g'ri bo'lganini isbotlamaydi.

## S3 tashqi nusxasini sozlash

Joriy ish maydoningizda **Eksportlar → Off-sayt nusxasi** bo'limini oching. Ushbu ixtiyoriy funksiya AWS S3 va boshqa S3-ga mos xizmatlar bilan ishlaydi. U jurnal segmentlarini, saqlangan fotosuratlar va fayllarni, vaqt shtampi bilan belgilangan tekshiruv nuqtalarini hamda yakunlangan suhbat eksportlarini nusxalaydi. Har bir ob'ekt yuklanishdan oldin to'plovchida`AES-256-GCM` bilan shifrlanadi.

Onlayn demo yuklash funksiyasi o'chirilgan holda bir xil boshqaruv elementlarini ko'rsatadi. Saqlash ma'lumotlarini faqat o'zingizning ish muhitingizda kiriting.

[![To'liq Off-site nusxa paneli: oxirgi nuqta, mintaqa, bucket, kirish kalitlari, jadval, Object Lock va tiklash kaliti boshqaruvlari](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)

Kengaytirilgan ilg'or opsiyalar bilan to'liq panel. Saqlash ma'lumotlari ko'rsatilmagan.

| Maydon | Nimani kiritish |
| --- | --- |
| Oxirgi nuqta | Saqlash xizmati URL manzili, bucket yo'li yoki kirish ma'lumotlarisiz. Badiiy misol: `https://s3.example.invalid` |
| Mintaqa | Provayderingiz talab qiladigan mintaqa. Ilovaning standart qiymati `us-east-1`. |
| Bucket | Kirishingiz mumkin bo'lgan mavjud bucket. Badiiy misol: `example-case-backup`. |
| Chelakdagi papka | Ob'ekt prefiksi; standart qiymati `tgwitness`. Ilova ushbu ish maydonining imzolash kaliti barmoq izidan olingan prefiksni qo'shadi. |
| Kirish kaliti ID / Maxfiy kirish kaliti | Saqlash ma'lumotlarini ikkitasini ham birga kiriting. Ular ish maydoni seyfida saqlanadi. Keyingi saqlashlarda ikkitasini ham bo'sh qoldiring, shunda saqlangan juftlik saqlanib qoladi. |
| Yo'l-uslubidagi manzillar | Provayderga ko'ra, yoqilganda `endpoint/bucket`, o'chirib qo'yilganda `bucket.endpoint` dan foydalaning. |
| Ko'chirma oraligi | 1 dan 1 440 daqiqagacha; standart 5 daqiqa. Rejalashtirilgan nusxalar olinishi uchun ilova ishga tushirilgan bo'lishi kerak. |
| Object Lock saqlash | Object Lock-ni qo'llab-quvvatlaydigan bucket uchun saqlash muddati va rejimi. Nol kun bucketning standart saqlash muddatini amalda qoldiradi. |

1. Manzil va kirish ma'lumotlarini kiriting. Tayyorlanayotganda **tashqi nusxani** tekshiruvsiz qoldiring, so'ngra "**Tashqi nusxani saqlash"ni** tanlang.
2. **Ulanishni sinab ko'rishni** tanlang. Bu shifrlangan test ob'ektini yuklaydi va saqlash javobini tekshiradi.
3. **Yuklab olish shifrlash kalitini** tanlang. Ushbu faylni kollektor (ma'lumot yig'uvchi)dan alohida saqlang; u tiklash uchun zarur.
4. **Offsayt nusxasini saqlash** katagini belgilang va yana saqlang. Qo'lda ijro etish uchun "**Nusxani hozir ko'chirish**"ni tanlang yoki jadvalni ishga tushirib qo'ying.

**Qilmaydi**. Saqlash konteynerini yaratmaydi. Rejalashtirilgan yuklamalar ilova to'xtaganda to'xtaydi.

## Saqlash muddatini va nusxa ko'chirish jarayonini tekshirish

**Qo'shimcha sozlamalar** bo'limida saqlash muddatini kunlarda va Object Lockni qo'llab-quvvatlaydigan bucket uchun `GOVERNANCE` yoki `COMPLIANCE` ni tanlang. TgWitness yuklangan obyektning saqlash rejimi va muddatini qayta o'qiydi. Status hisobotlari tasdiq, saqlash muddatining yetishmasligi yoki tekshiruv xatosini ko'rsatadi; faqatgina muvaffaqiyatli yuklash saqlashni tasdiqlamaydi.

Panel oxirgi o'tish, ob'ektlar soni, uzatilgan baytlar, nusxalangan jurnal chegarasi va har qanday xatoni ko'rsatadi. Yo'qolgan yoki o'zgartirilgan mahalliy media qayd etilib, keyingi o'tishda qayta sinovdan o'tkaziladi. O'sha media ortidagi fayllar, tekshiruv nuqtalari va navbatga qo'yilgan eksportlar hanuzgacha nusxalanishi mumkin.

Yüklashlar ish maydonining Direct, SOCKS5 yoki HTTP yo'nalishidan foydalanadi. MTProxy orqali S3 nusxa ko'chirish mavjud emas; ilova to'g'ridan-to'g'ri ulanishga qaytmaydi.

U buni**bajarmaydi.** Yuklash qabul qilinganligi sababli provayder Object Lockni majburlamaydi.

## Qayta tiklash kalitini alohida saqlang

Yuklab olingan JSON dekodlash kaliti, manzil sozlamalari, ish maydoni ob'ektlari prefiksi va imzolash kalitining barmoq izini o'z ichiga oladi. U S3ga kirish parollari (credentials)ni o'z ichiga olmaydi: tiklash uchun bucketga o'qish huquqiga ega alohida parollar talab etiladi.

Agar endpoint, bucket yoki papka prefiksini o'zgartirsangiz, kalit faylni qayta yuklab oling, shunda uning manzil sozlamalari mos keladi. Ilova yangi manzilda mahalliy saqlangan jurnal, fayllar va tekshiruv nuqtalari nusxasini ishga tushiradi. Mahalliy yuklash navbatidan allaqachon olib tashlangan yakunlangan suhbat eksportlari avvalgi manzilida qoladi.

U **qilmaydi**. Eksport qilingan kalitsiz nusxani dekriptlamaydi. Saqlashga kirish ma'lumotlari o'sha kalitni almashtira olmaydi.

## Boshqa qurilmada tiklash va tekshirish

TgWitness'ning ishonchli o'rnatilgan nusxasini, yuklab olingan kalit JSON faylini, o'qish huquqiga ega saqlash ma'lumotlarini va bo'sh chiqish katalogini ishlating. Quyidagi badiiy ma'lumot o'rnini bosuvchi o'rinbosarlarni haqiqiy ma'lumotlar bilan almashtiring.

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

Yuklab olingan va dekriptlangan obyektlar shaxsiy vaqtinchalik saqlashda qoladi, shu vaqtda butun jurnal, saqlangan tekshiruv nuqtalari hamda saqlangan media hash va o'lchamlari tekshiriladi. Xavfsiz bo'lmagan yo'llar, to'qnashuvchi jurnal segmentlari va tekshiruv nuqtasidan qisqaroq jurnal rad etiladi. Tekshirish muvaffaqiyatsiz bo'lsa, tiklangan fayllar e'lon qilinmaydi.

Muvaffaqiyatli tiklash natijasida nusxada mavjud material uchun `events.jsonl`, `media/`, `checkpoints/` va `exports/` hosil bo'ladi. Buyruqning JSON natijasini tiklangan material bilan birga saqlang.

U **buni bajarmaydi**: jurnalga hech qachon yetib bormagan kuzatuvlarni qayta tiklamaydi yoki mustaqil saqlangan tekshiruv nuqtasi yoki guvohni almashtirmaydi.
