# Xabarlar o'zgaradi. Ko'rganlaringizni saqlang.

Canonical page: https://phishdestroy.github.io/TgWitness/uz/

[Ochiq manba / v0.7.0](https://phishdestroy.github.io/TgWitness/uz/docs/reference/changelog/)

Telegram xabarlarini yozib oling, ularning o'zgartirishlarini saqlang va imzolangan yozuvni eksport qiling.

[demo ochish](https://phishdestroy.github.io/TgWitness/demo/?lang=uz)[sozlash bo'yicha qo'llanma](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=uz)

Demo soxta ma'lumotlardan foydalanadi. Telegramga kirish talab qilinmaydi.

 [GitHub Actions orqali yig‘ish (dastlabki versiya)](https://phishdestroy.github.io/TgWitness/uz/docs/capture/) [S3 tashqi nusxa: sozlash va tiklash](https://phishdestroy.github.io/TgWitness/uz/#s3)

VAQT ORQALI XABAR#0042

Northstar · TadqiqotBadiiy manba / xabar 42

1. **Xabar kuzatildi**09:41:02

   Brifing 14:00 da boshlanadi.
2. **Tahrir saqlangan**09:43:18

   Brifing 15:00 da boshlanadi.

   Avvalgi versiya saqlab qoldi
3. **O'chirish to'g'risidagi bildirishnoma**10:06:45

   Yozib olingan kontent jurnalida saqlanadi.

Uch kuzatuv. Bir tarix. MISOL

Xabar yo'qoladi. Qayd etilgan tarix esa qoladi.

## Har bir qayd etilgan o'zgarish. Aynan kerak bo'lgan joyda.

Soxta namoyish ma'lumotlari bilan interfeysni ko'rib chiqing.

TgWitness / Saqlangan suhbatlarSIZNING KUZATISH ISH JOYINGIZ

![Qorong'i mavzusidagi Telegram suhbatlari, kontekstda saqlangan tahrirlar va o'chirilgan xabarlar bilan](https://phishdestroy.github.io/TgWitness/assets/chats-dark.png)

01 / Saqlangan suhbatlar Xabarlardan yonada tahrirlar va o'chirish bildirishnomalari bilan birga saqlangan tanish suhbat ko'rinishi.

TgWitness / JurnalMAHALLI ISH JOYI

![Kuzatilgan xabarlar, tahrirlar, o'chirish bildirishnomalari va qamrov hodisalarini o'z ichiga olgan jurnal](https://phishdestroy.github.io/TgWitness/assets/workspace.png)

02 / Jurnal: Hisobingiz tomonidan kuzatilgan, uzilishlar hamda boshqa hodisalarni o'z ichiga olgan qidiruv mumkin bo'lgan vaqt chizig'i.

TgWitness / Tahrir tarixiMAHALLI ISH JOYI

![Xabarni oldingi qayd etilgan va tahrirlangan versiyalarini solishtiruvchi tafsilotlar oynasi](https://phishdestroy.github.io/TgWitness/assets/detail.png)

03 / Tahrir tarixi: oldingi kuzatuvni ustma-ust yozmasdan ushlangan versiyalarni solishtirish.

TgWitness / Imzolangan eksportlarMAHALLI ISH JOYI

![Imzolangan ZIP, JSONL, CSV va oflayn HTML hisobotni taklif qiluvchi ish maydonini eksport qilish](https://phishdestroy.github.io/TgWitness/assets/exports.png)

04 / Imzolangan eksportlar Jurnalni o'zingiz bilan olib yuring, manifest va mustaqil tasdiqlovchi bilan.

01 / QAYD ETISH

### Doirani siz belgilaysiz.

Tanlangan suhbatlar, Telegram papkasi yoki butun hisob. Har bir hisob uchun alohida ish maydoni.

[yig'ish rejimlarini solishtiring](https://phishdestroy.github.io/TgWitness/uz/guides/modes.html#scope)

02 / SAQLASH

### O'zgarishlar hikoyaga qo'shiladi.

Qayd etilgan versiyalar, o'chirish bildirishnomalari va kuzatuv bo'shliqlari jurnalda saqlanadi.

[voqealar matritsasini ko'ring](https://phishdestroy.github.io/TgWitness/uz/guides/modes.html#events)

03 / TOPSHIRISH

### Sayohat qiluvchi yozuv.

Imzolangan ZIP, saqlangan fayllar va oflayn hisobot. Ixtiyoriy parol bilan himoyalash.

[ni eksport qiling va tasdiqlang](https://phishdestroy.github.io/TgWitness/uz/docs/exports/)

## Bir baytni o'zgartiring. Zanjir sizga xabar beradi.

Har bir voqea oldingi xeshga bog'lanadi va Ed25519 imzusi bilan birga keladi.

![Yozib olingan voqealar oldingi hashlarga bog'lanadi, imzolarni o'zida aks ettiradi va tekshirilishi mumkin bo'lgan eksportda uzatiladi.](https://phishdestroy.github.io/TgWitness/assets/evidence-chain-animated.svg)

![Yozib olingan yozuvni o'zgartirish uning xeshini o'zgartiradi va bog'langan yozuvni tekshirishni buzadi.](https://phishdestroy.github.io/TgWitness/assets/evidence-tamper-animated.svg)

![Alohida saqlangan tekshiruv nuqtasi qabul qiluvchiga eksport qilingan jurnalni avvalgi kuzatuv bilan solishtirish imkonini beradi.](https://phishdestroy.github.io/TgWitness/assets/evidence-checkpoint-animated.svg)

Har bir tekshirish mexanizmi nimani aniqlaydi va uning chegaralari qayerda ekanligini ko'ring.

[sakkizta dalil darajasini o'rganing](https://phishdestroy.github.io/TgWitness/uz/guides/modes.html#levels)

## Yana bir juft ko'z uchun tayyor.

Kuzatuvlar, fayllar va oflayn HTML hisobotni bitta imzolangan paketda topshirish.

[dalillar modelini o'qing](https://phishdestroy.github.io/TgWitness/uz/docs/reference/evidence/)

tgwitness-evidence.zipIMZOLANGAN TO'PLAM

- 01

  Asl kuzatuvlarJSONL yozuvlari + CSV jadvali
- 02

  O'qiladigan kontekstOflayn HTML hisobot + saqlangan media
- 03

  Mustaqil tasdiqlashImzolangan manifest + mustaqil tasdiqlovchi

Imzolar ishonchli kalitga nisbatan o'zgartirishlarni aniqlaydi. Ular Telegram manbasini isbotlamaydi va to'liq yozib olinishni kafolatlamaydi. Jurnal mazmuni va media fayllarni siz ta'minlagan shifrlangan saqlash joyiga joylashtirish kerak.

## S3 nusxalari. Tashqi tekshiruvlar.

Shifrlangan nusxalarni saqlang va mustaqil tekshiruvlarni qo'shing.

O'chirib qo'yilgan (defolt bo'yicha)

### Hammasini S3-ga mos saqlashga nusxa ko'chiring

Jurnal, fayllar, vaqt belgilangan tekshiruv nuqtalari va suhbat eksportlari — AWS S3 yoki mos omborga yuklanishdan oldin shifrlangan.

**Saqlash sozlamalari va tiklash**

Klient tomonidan shifrlash

`AES-256-GCM` ushbu mashinadagi obyektlarni shifrlaydi. Provayder shifrlangan obyektlarni qabul qiladi.

Rejalashtirilgan yoki qo'lda nusxalar

Hozir nusxa oling yoki 1 dan 1 440 daqiqagacha bo'lgan oralikni tanlang. Paneldagi jarayonni kuzating.

Object Lock

Saqlash kunlari va bucket bunga qo'llab-quvvatlaydigan rejimni tanlang. Panel yuklangan ob'ekt bo'yicha saqlash tasdiqlangani yoki yo'qligini ko'rsatadi.

Tekshirilgan tiklash

Shifrlash kalitini yuklab oling va alohida saqlang. Boshqa qurilmada tiklang; fayllar faqat tasdiqlangandan so'ng e'lon qilinadi.

![To'liq Off-site nusxa paneli: oxirgi nuqta, mintaqa, bucket, kirish kalitlari, jadval, Object Lock va tiklash kaliti boshqaruvlari](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)

Kengaytirilgan ilg'or opsiyalar bilan to'liq panel. Saqlash ma'lumotlari ko'rsatilmagan.

Jurnal va media`AES-256-GCM`S3 bilan mos ombor

[S3 ni sozlang va nusxani tiklang](https://phishdestroy.github.io/TgWitness/uz/docs/exports/#s3)[Verifikatsiya tafsilotlarini o'qing](https://phishdestroy.github.io/TgWitness/uz/docs/reference/evidence/#off-site-copy-and-restore-s3)

U eksport qilingan dekripsiya kaliti bo'lmasa ishlamaydi va mustaqil guvohni almashtirmaydi.

### Bildirishnomalar · Xabardor qilish

Muammo bildirishnomalari, suhbat o'zgarishlari va kunlik xulosalar Apprise orqali: messenjerlar, elektron pochta yoki o'zingizning JSON webhook-ingiz orqali.

U**qilmaydi.** U xabar matnini jo'natmaydi, agar siz parchalarni yoqmagan bo'lsangiz.

 [Bildirishnoma manzillarini sozlash](https://phishdestroy.github.io/TgWitness/uz/docs/reference/operations/#notifications)

### Tashqi vaqt tamg'alari

Vaqt tamg'asi tekshiruv nuqtalari hashlarini RFC 3161 va OpenTimestamps yordamida.

**Qilmaydi.** Kutayotgan kalendar kvitansiyani tasdiqlangan Bitcoin vaqt belgisi sifatida qabul qilmaydi.

 [Timestamp dalillarini tekshiring](https://phishdestroy.github.io/TgWitness/uz/docs/reference/timestamp/)

### Mustaqil guvoh

Alohida host imzolangan kuzatuvlarni saqlaydi va`TGW1` tekshiruv nuqtalarini e'lon qilishi mumkin.

U **buni bajarmaydi:** bitta to'plovchi mezbonidagi ikki ish maydonini mustaqil guvohlarga aylantirmaydi.

 [guvohini sozlang](https://phishdestroy.github.io/TgWitness/uz/docs/witness/)

### Qayta tiklash va ko'rinadigan bo'shliqlar

Qayta ishga tushirgandan keyin davom ettiring. Qayta tekshiruvlar va `coverage.json` tiklangan xabarlar va bo'shliqlarni ko'rsatadi.

U**buni bajarmaydi:** u har bir o'tkazib yuborilgan tahrir yoki yo'qolgan xabarni qayta tiklamaydi.

 [Uzluksizlik va bo'shliqlarni tekshirish](https://phishdestroy.github.io/TgWitness/uz/guides/modes.html#continuity)

## Sizning birinchi ish maydoningiz shu yerdan boshlanadi.

Avvalo demo bilan tanishing. Tayyor bo'lgach, maxsus hisobingizni ulang. Windows, Linux, macOS yoki Docker.

[sozlash bo'yicha qo'llanmani o'qing](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=uz)

**Bir import qilingan sessiya, bir ishlayotgan klient.**

Telegram Desktop va TgWitness'da import qilingan TData/session kalitini bir vaqtda ishga tushirmang. Telegram umumiy ruxsatnomani bekor qilishi mumkin (AUTH_KEY_DUPLICATED). Paralel foydalanish uchun telefon yoki QR orqali alohida TgWitness hisobini yarating.

[Sessiyani import qilish bo'yicha ogohlantirishni o'qing](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=uz#session-warning)

**Ulanishdan oldin nazar soling.**

Telegram hisobisiz badiiy ish maydonini sinab ko'ring.

[Onlayn demo oching →](https://phishdestroy.github.io/TgWitness/demo/?lang=uz)

Windows `scripts\Demo.cmd`Linux / macOS `sh start.sh --demo`

**Mahalliy o'rnatish buyruqlari**

01-qadam

### Manbani oling.

[Manba kodini ZIP-arxivdan yuklab oling](https://github.com/phishdestroy/TgWitness/archive/refs/heads/main.zip) va arxivni oching, yoki omborni klonlang:

```
git clone https://github.com/phishdestroy/TgWitness.git
cd TgWitness
```

Manba ishga tushirish uchun Python 3.11+ talab etiladi. Windows ishga tushiruvchi dastur Python yo'q bo'lsa, o'rnatishni taklif etadi.

[Chiqarilishlarni ko'rib chiqing](https://github.com/phishdestroy/TgWitness/releases)

Windowsda Python yo'qmi? [Portativ paketni yuklab oling](https://github.com/phishdestroy/TgWitness/releases/download/v0.7.0/TgWitness-0.7.0-windows-amd64-portable.zip), arxivni oching va`TgWitness.cmd` fayliga ikki marta boshingiz.

02-qadam

### Qanday ishlashini tanlang.

`Start.cmd` ustiga ikki marta bosing yoki PowerShell'da quyidagi buyruqni ijro eting:

```
.\Start.cmd
```

Faqatgina o'rganmoqchimisiz? Ajratilgan demo uchun `scripts\Demo.cmd` ustiga ikki marta bosing. Telegramga kirish shart emas.

Python 3.11+ va `venv` mavjud:

```
sh start.sh
```

Buning o'rniga badiiy jurnalni ochish uchun `sh start.sh --demo` ni ishga tushiring.

Docker ishga tushirilgan va Compose 2.20+ o'rnatilgan holda:

```
docker compose up -d --build --wait
docker compose exec tgwitness cat /data/panel-token.txt
```

Ikkinchi buyruq sizning shaxsiy panel tokeningizni ko'rsatadi. Uni kompyuteringizda saqlang.

Ishga tushirgandan so‘ng [127.0.0.1:8787](http://127.0.0.1:8787) manzilini oching.

Manba kodidan o'rnatishda token `data/live/panel-token.txt` da joylashgan. Telegramga kirish uchun o'rnatilgan API sozlamalaridan yoki [my.telegram.org](https://my.telegram.org) saytidan olingan o'zingizning juft kalitingizdan foydalanishingiz mumkin. [To'liq sozlash bo'yicha qo'llanma ↗](https://phishdestroy.github.io/TgWitness/uz/docs/reference/quickstart/)

**TgWitness 0.7.0** [Nima yangilik →](https://phishdestroy.github.io/TgWitness/uz/docs/reference/changelog/) · [Xususiyatlar va ma'lum cheklovlar →](https://phishdestroy.github.io/TgWitness/uz/docs/reference/features/)

## Aniq ko'rsatmalar. Foydali keyingi qadam.

[Qo'llanmalarni o'rganing ↗](https://phishdestroy.github.io/TgWitness/uz/docs/)

[### Rejimlar, ssenariylar va dalil darajalari To'rt yig'ish rejimi. Sakkiz tasdiqlash darajasi. Ishingiz uchun ish jarayonini toping.](https://phishdestroy.github.io/TgWitness/uz/guides/modes.html)

[01 ### Hisobni bog'lang Telefon, QR va qo'llab-quvvatlanadigan sessiya importlari.](https://phishdestroy.github.io/TgWitness/uz/docs/accounts/)[02 ### Proxy tanlang Jamoat MTProxy ro'yxatlaridan yoki o'zingizning yo'lingizdan foydalaning.](https://phishdestroy.github.io/TgWitness/uz/docs/proxies/)[03 ### Witness botini sozlang Telegram kanalida imzolangan tekshiruv nuqtalari.](https://phishdestroy.github.io/TgWitness/uz/docs/witness/)[04 ### Eksport va tekshirish Yozib olingan tarixni ulashing va uning yaxlitligini tekshiring.](https://phishdestroy.github.io/TgWitness/uz/docs/exports/)

## Arxiv ustida ishlang.

Yuklash tarixini ko'rish, sun'iy intellekt manbalarini ko'rib chiqish, MCP mijozini ulash, saqlangan media fayllarini aniqlash va imzolangan webhook'larni yuborish.

Joriy manbadan mavjud. 0.7.0 portativ ko'rinishi ushbu vositalardan oldin chiqdi.

[ish jarayonini o'rganing](https://phishdestroy.github.io/TgWitness/uz/docs/archive/)

## Boshlashdan oldin.

**Bu sahifa Telegram bilan bog'langanmi?**

Yo'q. Bu – badiiy misollar va skrinshotlar bilan statik loyiha sahifasi. Haqiqiy ilova sizning kompyuteringizda yoki serveringizda ishlaydi; tizimga kirish o'sha yerda amalga oshiriladi.

**U yozib olishdan oldin o'chirilgan xabarlarni tiklay oladimi?**

Yo'q. TgWitness yig'ish jarayoni davomida hisobingiz tomonidan kuzatilgan kontentni saqlab qo'yadi. Keyingi tarixiy snapshot o'tkazib yuborilgan tahrirlar yoki o'chirilgan xabarlarni tiklay olmaydi.

**Butun jurnalim shifrlanganmi?**

Hisob ma'lumotlari va imzolash sirlar shifrlangan omborda saqlanadi. Mahalliy xabarlar va ilovalar shifrlangan disk yoki hajmni talab qiladi. Eksportlar ixtiyoriy ravishda parol bilan himoyalangan AES-256 ZIP formatidan foydalanishi mumkin.

**Bu Telegram bilan bog'liqmi?**

Yo'q. TgWitness Telethon'dan foydalanadigan mustaqil loyiha bo'lib, MIT litsenziyasi ostida tarqatiladi. Siz o'zingizning hisoblaringizni ichki API sozlamalari yoki o'zingizning API juftligingiz orqali ruxsatlaysiz.

PROJECT NOTICE / LICENCE

## Operator incompatibility.

**Taylor Wessing PartG mbB — German core, Hamburg office.**

Our statement as the authors of TgWitness. It adds no condition to the MIT License. Read the complete notice and its source record.

[Read the complete notice](https://phishdestroy.github.io/TgWitness/docs/reference/notice/) [Original text](https://phishdestroy.github.io/TgWitness/NOTICE)

## Avvalo o'rganing. Tayyor bo'lgach sozlang.

[demo ochish](https://phishdestroy.github.io/TgWitness/demo/?lang=uz)[sozlash bo'yicha qo'llanma](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=uz)
