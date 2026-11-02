# Eksport va tekshirish

Canonical page: https://phishdestroy.github.io/TgWitness/uz/docs/exports/

Qabul qiluvchiga yig'ish ish maydoni va uning saqlangan tarixi bilan solishtirib tekshirishi mumkin bo'lgan fayllarni taqdim eting.

Manbani saqlashImzolangan ZIP-ni eksport qilingQabul qiluvchi tasdiqlaydi

Imzolar va tekshiruv nuqtalariga yangi boshlamoqdamisiz? [Namuna yozuvni o'zgartiring](https://phishdestroy.github.io/TgWitness/uz/docs/concepts/#chain) va qaysi tekshiruvlar uni aniqlashini ko'ring.

Nusxani yig'uvchidan uzoqda saqlashni xohlaysizmi? [S3 sozlamalar](https://phishdestroy.github.io/TgWitness/uz/docs/exports/#s3)iga o'ting, [Object Lock](https://phishdestroy.github.io/TgWitness/uz/docs/exports/#s3-retention) yoki [tasdiqlangan tiklashni tanlang](https://phishdestroy.github.io/TgWitness/uz/docs/exports/#s3-restore).

## Ishonchli manbani saqlab qo'ying

Ish maydonining jamoat kaliti barmoq izini yig'uvchidan tashqarida saqlang. Yig'ish jarayonida imzolangan tekshiruv nuqtalarini boshqa joyda saqlang yoki [mustaqil guvoh](https://phishdestroy.github.io/TgWitness/uz/docs/witness/)dan foydalaning. Ushbu havolalar qabul qiluvchiga kalitni va avvalgi jurnal chegarasini tekshirish imkonini beradi.

## Imzolangan ZIP-faylni yuklab oling

**Exportsni** oching va imzolangan dalillar ZIP-faylini yarating. U to'liq ish maydoni jurnali va imzolangan fayllar manifestini o'z ichiga oladi. [Report Studio](https://phishdestroy.github.io/TgWitness/uz/docs/reports/)'dan foydalanib, o'qiladigan hisobotni shakllantiring yoki faqat tanlangan, minimallashtirilgan ma'lumotlarni yetkazish uchun [handover ekstrakt](https://phishdestroy.github.io/TgWitness/uz/docs/handover/)ini yarating.

HTML, PDF va JSON hisobotlari o'z imzolangan muhrlariga ega bo'lib, ularni alohida tekshirish mumkin. CSV tahlil uchun qulay nusxa bo'lib, uning yaxlitligini tekshirish uchun tasdiqlangan ZIP ichidagi aniq CSV faylidan foydalaning. Agar qabul qiluvchi manba yozuvlari va ilovalarni ham talab qilsa, imzolangan ZIP faylni saqlang.

## TgWitness'ning ishonchli nusxasi bilan tasdiqlang

O'rnatilgan loyiha muhitida namunaviy barmoq izi va fayl yo'llarini quyidagilar bilan almashtiring:

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
```

Ikkala havola ham o'tganida, natija `key_pinned: true` va `checkpoint_checked: true` ni qayta hisobot beradi. Verifikatsiya natijasini asl arxiv bilan birga saqlang. Saqlangan tekshiruv nuqtasi eksport chegarasida yoki undan oldin bo'lishi kerak.

## Verifikatsiya natijasidan foydalaning

- **Yetkazib berilgan fayllarni tekshiring:** manifest ularning hashlarini bog'laydi, yozuv imzolari esa saqlangan jurnalni bog'laydi. O'zgargan fayl yoki uzilgan yozuv zanjiri aniqlanadi.
- **Ish maydoni identifikatorini tekshiring:** mustaqil saqlangan barmoq izi siz kutgan imzolash kalitingizni aniqlaydi.
- **Oldingi chegarani solishtiring:** saqlangan tekshiruv nuqtasi topshirishdan oldin saqlangan jurnal prefiksi bilan eksportni tekshiradi.
- **Ko'rib chiqish yig'indisi qamrovi:** bo'shliqlar, olish natijalari va nazoratli jo'natish → tahrirlash → o'chirish testi ushbu sozlama tomonidan qayd etilgan voqealarni tasvirlaydi.

Ushbu natijalarni qabul qiluvchining nusxasi bilan birga saqlang. Tekshiruvlar doirasini hamda manba da'volari va yig'ish qamrovini alohida baholashni aniqlash uchun [qanday tasdiq o'rnatilganini](https://phishdestroy.github.io/TgWitness/uz/docs/reference/evidence/#verification-scope) ko'ring.

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

1. Provayderingizda bucket yarating, so'ng uning manzili va kirish ma'lumotlarini kiriting. Tayyorlanayotganda "**Offsayt nusxasini saqlash"**ni belgilamagan holda qoldiring, so'ng "**Offsayt nusxasini saqlash"ni** tanlang.
2. **Ulanishni sinab ko'rishni** tanlang. Bu shifrlangan test ob'ektini yuklaydi va saqlash javobini tekshiradi.
3. **Yuklab olish shifrlash kalitini** tanlang. Ushbu faylni kollektor (ma'lumot yig'uvchi)dan alohida saqlang; u tiklash uchun zarur.
4. **Offsayt nusxasini saqlash** katagini belgilang va yana saqlang. Qo'lda ijro etish uchun "**Nusxani hozir ko'chirish**"ni tanlang yoki jadvalni ishga tushirib qo'ying.

## Saqlash muddatini va nusxa ko'chirish jarayonini tekshirish

**Qo'shimcha sozlamalar** bo'limida, baketingiz Object Lock-ni qo'llab-quvvatlaganda saqlash muddatini kunlarda belgilash va `GOVERNANCE` yoki `COMPLIANCE` ni tanlang. TgWitness yuklangan obyektning saqlash rejimi va muddatini qayta o'qiydi. Alohida saqlash natijasini ko'rib chiqing: tasdiqlangan, saqlash muddati yetishmayotgan yoki tekshiruv muvaffaqiyatsiz bo'lgan.

Panel oxirgi o'tish, ob'ektlar soni, uzatilgan baytlar, nusxalangan jurnal chegarasi va har qanday xatoni ko'rsatadi. Yo'qolgan yoki o'zgartirilgan mahalliy media qayd etilib, keyingi o'tishda qayta sinovdan o'tkaziladi. O'sha media ortidagi fayllar, tekshiruv nuqtalari va navbatga qo'yilgan eksportlar hanuzgacha nusxalanishi mumkin.

Yuklashlar ish maydonining Direct, SOCKS5 yoki HTTP yo'nalishidan foydalanadi. S3 nusxa ko'chirish uchun ushbu yo'nalishlardan birini tanlang; faqat MTProxy yo'nalishi nusxani xato bilan kutib turadi.

## Qayta tiklash kalitini alohida saqlang

Yuklab olingan JSON dekodlash kaliti, manzil sozlamalari, ish maydoni ob'ektlari prefiksi va imzolash kalitining barmoq izini o'z ichiga oladi. Tiklash uchun ushbu kalit fayli hamda bucketga o'qish huquqiga ega alohida saqlash ma'lumotlari talab etiladi. Ularni tiklash reyangizda hisobga oling.

Agar endpoint, bucket yoki papka prefiksini o'zgartirsangiz, kalit faylni qayta yuklab oling, shunda uning manzil sozlamalari mos keladi. Ilova yangi manzilda mahalliy saqlangan jurnal, fayllar va tekshiruv nuqtalari nusxasini ishga tushiradi. Mahalliy yuklash navbatidan allaqachon olib tashlangan yakunlangan suhbat eksportlari avvalgi manzilida qoladi.

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

Qayta tiklangan materiallarni mustaqil saqlangan tekshiruv nuqtangiz yoki guvoh yozuvlaringiz bilan solishtiring, so'ng kerakli davr uchun yozib olingan to'plam qamrovini ko'rib chiqing.
