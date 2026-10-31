# Bir jurnal. To'rt yig'ish rejimi. Sakkiz tasdiqlash darajasi.

Canonical page: https://phishdestroy.github.io/TgWitness/uz/guides/modes.html

Rejimlar, ssenariylar va dalillar darajalari

TgWitness U bog'langan hisobning kuzatishlarini qayd etadi. Uchinchi tomon mustaqil ishonchli kalit yordamida qaydning yaxlitligini tasdiqlay oladi.

[Yig'ish rejimlari](https://phishdestroy.github.io/TgWitness/uz/guides/modes.html#scope)[Ssenariylar](https://phishdestroy.github.io/TgWitness/uz/guides/modes.html#scenarios)[Dalil darajalari](https://phishdestroy.github.io/TgWitness/uz/guides/modes.html#levels)

3–5 daqiqalik umumiy ko'rinish · badiiy misollar · joriy amalga oshirish

1. **Telegram**

   Hisobga ko'rinadigan yangilanishlar
2. **Yig'uvchi**

   Ulanishgan yozuvlar, har biri imzolangan
3. **Verifikator**

   Ishonchli kalit + saqlangan chegarasi

`h₁ → h₂ → h₃ · Ed25519`Buzilmaslik tekshiriladi. Telegram kelib chiqishi va xabar haqiqati alohida masalalardir.

## Kuzatuv doirasini tanlang

Uch doira va bir tergov oldindan sozlama. Istisnolar va yoqilgan manba turlari hanuz amal qiladi.

O'rnatilgan**Tanlangan suhbatlar**

Yozuvlar

Faqat qo'lda tanlangan manbalar.

Yangi suhbatlar

Avtomatik qo'shilmaydi.

Tanlang

Ma'lum kanallar yoki guruhlar to'plami. Hech qanday belgilangan chat sig'imi tasdiqlanmagan.

**Qilmaydi** U boshqa suhbatlarni aniqlamaydi va avvalgi tarixni to'ldirmaydi.

Hisob katalogi**Telegram papkasi**

Yozuvlar

Papka tarkibiga kiritish va toifalar, sozlanganda istisno qilingan elementlar va arxivlangan suhbatlar.

Yangi suhbatlar

Mos keladigan faol suhbatlar; papka o'zgarishlari bir soat ichida.

Tanlang

Analitik allaqachon ish hujjatlari papkasini yuritmoqda. Yig'ishni maxsus hisobda tasdiqlang.

**Qilmaydi** U papkaning o'zgaruvchanligini qo'llamaydi muted/read sharoitlarini qo'llamaydi.

Doirani tasdiqlang**Butun hisob**

Yozuvlar

Hisobga ko'rinadigan suhbatlar, jumladan shaxsiy suhbatlar va botlar, tanlangan turlar doirasida.

Yangi suhbatlar

Birinchi yangilanish kelganda qo'shiladi.

Tanlang

Maxsus kuzatuv hisobvarag'i, jumladan ishda ishtirok etayotgan hisobvarag'i.

**Qilmaydi** U avtomatik ravishda suhbatlarga qo'shilmaydi yoki manbaaga kirishni chetlab o'tmaydi.

Butun hisob-kitob oldindan sozlama**Tergov rejimi**

Yozuvlar

Barcha manba turlari, o'z harakatlari, manba profillari va yangi topilgan manbalarning so'nggi 200 ta ko'rinadigan xabarlari.

Yangi suhbatlar

Yangi chat yoki bot profil va tarixning snapshotini oladi.

Tanlang

Panel orqali jamoaga qo'shiling yoki bot bilan o'zaro ta'sirlaning. Oldindan sozlangan parametrlarni ko'rib chiqing va saqlang.

**Qilmaydi** U mavjud bo'lgan barcha suhbatlarni snapshot qilmaydi yoki boshqa klientda bosilgan callback'larni kuzatmaydi.

Ushbu kartalar mahalliy taqqoslash uchun mo'ljallangan, jonli kollektor nazorat vositalari emas. Ular hisobni o'zgartirmaydi.

**Qilmaydi** Hech bir rejim sirli suhbatlarni o'qimaydi, jarayon to'xtatilgan paytda yozuv olib bormaydi, manbalarni mustaqil ravishda birlashtirmaydi yoki so'ralganidan tashqari oldingi tarixni qayta tiklamaydi snapshot/export.

[Tafsilotlarni o'qing](https://phishdestroy.github.io/TgWitness/uz/docs/reference/collection/)

## GitHub Actions orqali yig‘ish (dastlabki versiya)

Telegram’ga yangi kirish, bitta chat, shifrlangan arxiv va GitHub kelib chiqish tasdig‘i.

[Yig‘ish yordamchisini ochish](https://phishdestroy.github.io/TgWitness/uz/docs/capture/)

## Qayd etilgan narsa

Faqat yetkazilgan yoki aniq so'ralgan kuzatuvlar yozuvga kiritiladi. Noma'lum mansubiyat noma'lum bo'lib qoladi.

 O'tkazgichlarni qayd eting · mahalliy illyustratsiyaYangi xabarlarTahrirlarO'chirishlarReaksiyalarA'zolik

Panel ushbu kalitlarni har bir ish maydoni bo'yicha qo'llaydi. Uni o'chirish mavjud yozuvlarni saqlab qoladi; uni qayta yoqish esa o'tkazib yuborilgan voqealarni qayta tiklamaydi.

**Voqea matritsasi: saqlangan material va qolgan noma'lumlar**

| Kategoriya | Saqlangan | Noma'lum bo'lib qoladi |
| --- | --- | --- |
| Xabar | Matn, IDlar, jo'natuvchi metama'lumotlari, javob konteksti va asl yangilanish konverti. | Uchinchi tomon tomonidan tasdiqlanadigan Telegram imzosi yo'q. |
| Tahrir | Har bir kuzatilgan versiya, avvalgilarini ustiga yozmasdan. | O'rtadagi tahrirlar e'tibordan chetda qolishi mumkin; jo'natuvchi albatta muharrir emas. |
| O'chirish | Agar mavjud bo'lsa, eslatma va oldin saqlangan matn. | O'chirish va aniq harakat vaqti taqdim etilmaydi. |
| Doirasi belgilanmagan o'chirish | Hisob darajasidagi ogohlantirish; noma'lum tengdosh aniq ko'rsatiladi. | Taxmin qilingan suhbat yo'q. Korrelatsiya imkon qadar oldin saqlangan hisob-doirasidagi identifikatorlardan foydalanadi. |
| Reaksiya | Yetkazilgan hisoblagichlar va ko'rinadigan yaqinda foydalanilgan identifikatorlar. | Har bir reaktor ko'rinadigan emas; to'liq mavjud ro'yxat uchun alohida so'rovlar kerak. |
| A'zolik | Yetkazilgan xizmat xabarlari va ishtirokchi yangilanishlari. | Rol va suhbat turi ko'rinishni cheklaydi; sukut bo'lmaslik mavjud emasligini anglatmaydi. |
| Ilova | Asl-versiya tavsiflagichi, saqlangan baytlar, SHA-256 va urinish natijalari. | Yo'qolgan fayl mavjud bo'lmasligi mumkin; yangiroq versiya uni almashtirmaydi. |
| Tarix snappoti | Hozirda ko'rinadigan xabarlar tarix kuzatuvlari sifatida belgilangan. | Oldingi tahrirlar va yo'qolgan kontent tiklanmaydi. |
| O'z harakatlari | Chiquvchi messages/edits va mos keluvchi javob-klaviatura button_press metadata. | Boshqa Telegram mijozida bosilgan callbacklar ko'rinmaydi. |
| Bot tugmalari | Callback, URL, veb-ilova va so'rovning metadata'lari xabar bilan saqlanadi. | URL manzillari va phone/location so'rovlar matn bo'lib, avtomatik ochilmaydi yoki ijro etilmaydi. |

### Standart ilova cheklovlari

Foto

20 MiB

Video

100 MiB

Fayllar

50 MiB

Animatsiyalar

20 MiB

Video eslatmalar

50 MiB

Ovoz

20 MiB

Audio

50 MiB

Stikerlar

5 MiB

**Qilmaydi** Kalit o'rnatilgan metama'lumotlarni tahrirlamaydi yoki operatsion yozuvlarni o'chirib tashlamaydi. Qayd qilish Telegram taqdim etmagan ijrochining kimligini aniqlamaydi.

[Tafsilotlarni o'qing](https://phishdestroy.github.io/TgWitness/uz/docs/reference/collection/)

## Qo'lingizdagi vakolatlardan foydalaning

Har bir akkauntning o'z ish maydoni, jurnali, imzolash kaliti, marshruti va navbati mavjud.

### Telefon + kod

Kiriting 2FA faollashtirilganda.

### QR kod

Ruxsat berilgan qurilmadan skanerlang; 2FA hali ham talab qilinishi mumkin.

### Telethon .session

Hisobning sessiya faylini import qiling.

### Pyrogram .session

Qo'llab-quvvatlanadiganlarni import qiling Pyrogram sessiya formatini import qiling.

### TData ZIP

Qo'llab-quvvatlanadigan bitta Desktop hisob; agar sozlangan bo'lsa, mahalliy parol.

### StringSession matn

Joylashtiring Telethon StringSession.

### .session + .json

Sessiyani va mos keluvchi hamroh metama'lumotlarni tanlang.

### Avtorlik kaliti HEX + DC ID

Hisob ma'lumotlarini uning ma'lumotlar markazi identifikatori bilan import qiling.

**API juftlik**

Sizning API juftlik ixtiyoriydir. U bo'lmasa, TgWitness ommaviy juftliklar havzasidan foydalanadi, jumladan rasmiy Telegram Desktop juftliklari.

`Direct · SOCKS5 · HTTP CONNECT · MTProxy`MTProxy eksperimental; o'rnatilgan ommaviy MTProxy Ro'yxatlar mavjud. Muvaffaqiyatsiz proxy yo'li to'g'ridan-to'g'ri ulanishga qaytmaydi.

Bir kompyuterdagi ikki ish maydoni ikki mustaqil guvoh emas.

**Qilmaydi** Import Telegram avtorizatsiyasini chetlab o'tmaydi, 2FA yoki qo'llab-quvvatlanmagan sessiya formatlarini. Hisoblar hanuzgacha ilova jarayonini baham ko'radi.

[Hisob formatlari](https://phishdestroy.github.io/TgWitness/uz/docs/reference/accounts/)

## Panel orqali harakat qiling

Yuborish yoki javob berish uchun joriy bot tugmasini bosing, havola ko'rinishini saqlang, so'ng aniq chatga qo'shiling yoki botni start parametriga ega holda ishga tushiring.

`interaction.preview``interaction.requested``interaction.result`

Ko'rinish, so'rov va natija kvitansiyalari imzolanadi. Tugmani bosishdan oldin server xabarni qayta oladi va o'zgartirilgan klaviaturani rad etadi. Qaytarilgan callback matni va URL manzillari kontekstda qayd etilgan bo'lib qoladi.

**Qilmaydi** Veb-ilovalar, to'lovlar, phone/location ulashish yoki inline so'rovlar. URL ko'rsatish uni ochmaydi.

[Tafsilotlarni o'qing](https://phishdestroy.github.io/TgWitness/uz/docs/reference/collection/)

## Qayta tiklash va uzluksizlik

Bo'shliqlar ko'rsatiladi, yashirilmaydi.

### Saqlangan pozitsiyani tiklash

Qayta ishga tushirilgandan so'ng Telegramdan o'tkazib yuborilgan yangilanishlar so'raladi. Cheklangan saqlash muddati va muddati tugagan farqlar bo'shliqlar qoldirishi mumkin.

### Ko'rinadigan xabarlarni qayta tekshiring

O'rnatilgan sozlamalar: ustuvor manbalar har 15 daqiqada, boshqalar har 6 soatda. Natijalar quyidagilarni o'z ichiga oladi message.recovered va message.missing_on_recheck.

### O'qish coverage.json

Imzolangan eksportga kuzatuv davrlari, sabablar bilan tushib qolgan bo'shliqlar va kuzatilmagan IDlar ilova qilinadi. Qayta tekshirishda yo'qolgan yozuv o'chirish bildirishnomasi emas.

**Qilmaydi** Keyingi tarix snopsisiz uzilishni o'chirib tashlamaydi yoki yo'qolgan har bir versiyani tiklamaydi. Saqlangan kursor jurnal qabul qilinganiga yo'qotishsiz tasdiq emas.

[Tafsilotlarni o'qing](https://phishdestroy.github.io/TgWitness/uz/docs/reference/evidence/)

## Yetti daraja. Turli savollar.

Har bir mexanizm chegaralangan savolga javob beradi. Tashqi xizmatlarni alohida sozlang va ularning ishonch nuqtalarini yig'uvchidan tashqarida saqlang.

1. ### Yozib qo'ying

   SHA-256 zanjir + Ed25519 har bir voqea uchun; birinchi previous_hash birinchi 64 ta nol.

   **Uchinchi tomon tekshiruvlari** Biriktirilgan yig'uvchi kalit ostida buyurtma berish va imzo.

   **Qilmaydi** Bu Telegramning kelib chiqishini yoki to'liqligini isbotlamaydi.

   **Verifikatsiya buyrug'i**

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256
   ```
2. ### Kontener

   manifest.json fayl hashlarini ro'yxatlaydi; manifest.sig imzolaydi. media.saved ilovadagi baytlarni voqeaga bog'laydi.

   **Uchinchi tomon tekshiruvlari** Taqdim etilgan fayllar imzolangan manifest va media kvitansiyalari bilan mos keladi.

   **Qilmaydi** U alohida yuklab olingan narsani imzolamaydi CSV, HTML yoki skrinshotni imzolamaydi.

   **Verifikatsiya buyrug'i**

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256
   ```
3. ### Saqlangan chegarasi

   Boshlanishda tekshiruv nuqtasi, standart bo'yicha har 5 daqiqada va tartibli to'xtash. Nusxasini boshqa joyda saqlang.

   **Uchinchi tomon tekshiruvlari** Keyingi eksport avval saqlangan uzunlik va bosh bilan mos keladi; rollback aniqlanishi mumkin.

   **Qilmaydi** U jurnal va barcha saqlangan tekshiruv nuqtalarining ikkalasini ham almashtirilishini aniqlamaydi.

   **Verifikatsiya buyrug'i**

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --checkpoint checkpoint.json
   ```
4. ### Tashqi vaqt

   Dalil rejimi tekshiruv nuqtasini yuboradi SHA-256 ga RFC 3161 vakolatli organlar (FreeTSA, DigiCert) va OpenTimestamps taqvimlar.

   **Uchinchi tomon tekshiruvlari** Tasdiqlangan TSA javobi o'sha baytlarni sanalashadi; tasdiqlangan OpenTimestamps tasdiqlangan ___ ularni Bitkoin bilan bog'laydi.

   **Qilmaydi** U tayyorlangan so'rov yoki kutayotgan taqvim kvitansiyasini tasdiqlangan vaqt tamg'asi deb hisoblamaydi.

   **Verifikatsiya buyrug'i**

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --tsa-ca trusted-ca.pem
   ots upgrade checkpoint.ots
   ots verify checkpoint.ots
   ```
5. ### Mustaqil guvoh

   Alohida host, doirali faqat o'qish uchun mo'ljallangan nuqta, yangi chaqiriq, o'zining key/journal va TGW1 kanal postlari.

   **Uchinchi tomon tekshiruvlari** Oldin qabul qilingan sarlavhalar; holatlari yaxshi, key_changed, rollback, fork, invalid va no_response.

   **Qilmaydi** Bu bitta to'plovchi mezbonidagi ikki ish maydonini mustaqil guvohlarga aylantirmaydi.

   **Verifikatsiya buyrug'i**

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --witness witness.zip --witness-fingerprint WITNESS_SHA256 --channel result.json
   ```
6. ### Joydan tashqari nusxa

   S3-ga mos nusxa, bilan shifrlangan AES-256-GCM; Object Lock agar bucket bunga qo'llab-quvvatlasa.

   **Uchinchi tomon tekshiruvlari** Restore faqat jurnal, tekshiruv nuqtasi va saqlangan media tekshiruvi muvaffaqiyatli bo'lgach fayllarni e'lon qiladi.

   **Qilmaydi** U eksport qilingan kalitsiz tiklanmaydi va saqlash javobini tekshirmay saqlanganligini taxmin qilmaydi.

   **Verifikatsiya buyrug'i**

   ```
   python -m tgwitness.replica restore --key-file KEY.json --out EMPTY_DIR
   ```
7. ### Kelib chiqishni ishga tushiring

   Imzolangan ijro kvitasi: manba xeshlari, bog'liqlik versiyalari va jarayon konteksti. O'z-o'zini xabar qilgan.

   **Uchinchi tomon tekshiruvlari** Imzolash yig'uvchisi o'z ijrosi haqida nima xabar berdi.

   **Qilmaydi** U mustaqil jarayonni tasdiqlashni ta'minlamaydi va yozib olishdan oldin buzilishni istisno qilmaydi.

   **Verifikatsiya buyrug'i**

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256
   ```

### Hech bir daraja isbotlamaydigan narsa

Har bir Telegram yangilanishining yetkazilishi; matnning haqiqiyligi; jo'natuvchi ID haqiqiy shaxsni aniqlashi; yozib olishdan oldin ma'lumot yig'uvchining buzilmasligi; sudda qabul qilinishi.

[Mustaqil guvoh](https://phishdestroy.github.io/TgWitness/uz/docs/reference/witness/)

Mahalliy SHA-256 eksperiment

### 2-yozuvni o'zgartirib ko'ring

Keyingi yozuv oldin saqlangan havolani saqlaydi. Matnni o'zgartirish 2-yozuvning hisoblangan xeshini o'zgartiradi.

Yozuv 2 matni

Yozuv 1`h1`64 ta nol bilan boshlanadi

Yozuv 2`h2`Saqlanganlarni o'z ichiga oladi h1

Yozuv 3`h3`Saqlanganlarni o'z ichiga oladi h2

Statik misol: h2 "11:00 da uchrashamiz"ni qamrab oladi. Ushbu matnni o'zgartirish h2; 3-yozuv hali ham saqlangan ma'lumotga murojaat qiladi h2.

**To'liq digestlarni tekshiring**

Saqlangan yozuv 2 xesh

`SHA-256(e₂)`

Qayta hisoblangan yozuv 2 xesh

`SHA-256(e₂)`

Ushbu namuna hashlarni hisoblaydi, imzo emas. Haqiqiy tasdiqlovchi har bir imzo va havolani ishonchli kalitga nisbatan tekshiradi.

 [Tafsilotlarni o'qing](https://phishdestroy.github.io/TgWitness/uz/docs/reference/how-it-works/)

## Dalillar bo'ylab yo'l tanlang

Badiiy vaziyatlar. Tegishli voqeadan oldin yig'ishni boshlang; kontent bilan birga chegaralar va bo'shliqlarni saqlang.

### Kanal to'lov tafsilotlarini o'zgartiradi

Rejim → voqealar

Tanlangan suhbatlar → xabarlar, tahrirlar, o'chirishlar.

Chiqish

Kuzatilgan post versiyalari va ilovalar xesh bo'yicha.

Verifikatsiya

Imzolangan ZIP + saqlangan tekshiruv nuqtasi + tasdiqlangan TSA javobi.

**Qilmaydi** U hech qachon qayd etilmagan asl nusxani tiklamaydi.

### Xabarlar hodisadan so'ng yo'qoladi

Rejim → voqealar

Papka yoki butun hisob → barcha voqea toifalari.

Chiqish

Saqlangan asl nusxalar, o'chirish bildirishnomalari va bo'shliqlar bilan qamrov.

Verifikatsiya

Imzolangan ZIP + mustaqil guvoh jurnali.

**Qilmaydi** U hech qanday ijrochi ko'rsatilmagan bildirishnoma orqali o'chiruvchini aniqlamaydi.

### Do'kon botini o'rganing

Rejim → voqealar

Tergov oldindan sozlamalari → tugmalar, havola ko'rinishlari va aniq botni ishga tushirish.

Chiqish

Imzolangan o'zaro ta'sir kvitansiyalari, qaytarilgan callback-lar va saqlangan profillar.

Verifikatsiya

Imzolangan ZIP; har qanday dosye­ni unga qarshi tekshirish ZIP.

**Qilmaydi** U bot veb-ilovasini ochmaydi, to'lov amalga oshirmaydi yoki boshqa mijozning callback-larini qayd etmaydi.

### Ishtirokchi suhbatlar bo'ylab ismlarini o'zgartiradi

Rejim → voqealar

Har qanday doira → kuzatilgan sender/profile metadata.

Chiqish

Nom/foydalanuvchi nomi tarixi raqamli ID bo'yicha, "hamda" havolalari va olingan aloqalar.

Verifikatsiya

Dossye JSON imzolangan nusxa bilan solishtirildi ZIP.

**Qilmaydi** Bu hamyon, telefon uslubidagi satr yoki foydalanuvchi nomini tasdiqlangan shaxsiyatga aylantirmaydi.

### Masofaviy nusxa bilan uzoq muddatli kuzatuv

Rejim → voqealar

Har qanday doira → Dalil rejimi va bir S3 qo'llab-quvvatlanadigan replika Object Lock.

Chiqish

Shifrlangan nusxa, saqlangan tekshiruv nuqtalari va vaqt tamg'asi javoblari.

Verifikatsiya

Eksport qilingan kalit bilan tiklang, so'ng asl serverisiz tasdiqlang.

**Qilmaydi** Bu mustaqil guvohni yoki alohida saqlangan dekripsiya kalitini almashtirmaydi.

[Tafsilotlarni o'qing](https://phishdestroy.github.io/TgWitness/uz/docs/reference/investigation/)

## Tekshirilishi mumkin bo'lgan paketni topshiring

Imzolangan asl nusxa, mustaqil saqlangan kalit barmoq izi, tegishli tekshiruv nuqtasi va tasdiqlash natijasini taqdim eting.

- Imzolangan ZIP
- JSONL
- CSV
- HTML
- Tekshiruv nuqtasi
- Qabul kvitasi
- Suhbat eksporti: chat.json / chat.html
- Dossye JSON
- Parol bilan himoyalangan AES-256 ZIP
- Bir nechta hisoblar uchun alohida eksportlar
- Streaming CLI: 5 GiB o'rnatilgan limit

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --checkpoint checkpoint.json
```

Verifikatorni tekshirilayotgan arxivdan emas, balki ishonchli nusxadan oling.

**Qilmaydi** Mustaqil CSV va HTML imzolangan konteynerlar emas. Parol uzatmaning maxfiyligini himoya qiladi, haqiqiyligini emas. Bir nechta eksportlar hisob jurnallarini birlashtirmaydi.

[Tafsilotlarni o'qing](https://phishdestroy.github.io/TgWitness/uz/docs/reference/evidence/)

## Yetkazib berilgan artefaktni solishtiring

Qo'shimcha imzolash, vaqt tamg'asi yoki guvoh tizimlarisiz asosiy artefaktlar. Skriptlar va loggerlar implementatsiyaga qarab farq qiladi; "qisman" – faqat yozib olingan yoki ko'rinadigan material bilan cheklangan.

| Yondashuv | Tahrirlar / o'chirishlar | Imzoni yozib qo'ying | Tashqi vaqt | Mustaqil guvoh | Qamrov / bo'shliqlar | Muallifsiz tasdiqlash |
| --- | --- | --- | --- | --- | --- | --- |
| Telegram Desktop eksporti | Qisman | Yo'q | Yo'q | Yo'q | Yo'q | Yo'q |
| Telethon snapshot skripti | Qisman | Yo'q | Yo'q | Yo'q | Yo'q | Yo'q |
| O'chirish yozuvchisi: matnli log | Qisman | Yo'q | Yo'q | Yo'q | Yo'q | Yo'q |
| Ekran tasvirlari / veb-ushlash | Qisman | Yo'q | Yo'q | Yo'q | Yo'q | Yo'q |
| TgWitness sozlangan qo'shimchalar bilan | Qisman | Ha | Ha | Ha | Qisman | Ha |

**Qilmaydi** Jadval har bir skript yoki loglash mahsulotini baholamaydi. Ixtiyoriy vaqt va guvoh tekshiruvlari o'z xizmatlari va ishonch nuqtalarini talab qiladi; hech biri manba haqiqatini aniqlamaydi.

[Tafsilotlarni o'qing](https://phishdestroy.github.io/TgWitness/uz/docs/reference/evidence/)

## Chegaralarni dalillar bilan saqlang

Verifikatsiya uning doirasi aniq bo'lganda foydalidir.

- Yashirin suhbatlar mavjud emas.
- Jarayon to'xtatilgan paytda hech narsa qayd etilmaydi; tiklash cheklangan.
- Verifikatsiyalangan yozuv uning mazmuni rostligini isbotlamaydi.
- Kalitga ega operator istalgan kontentni imzolashi mumkin. Mustaqil guvohlar va vaqt tamg'alari keyingi o'zgartirishlarni cheklaydi, dastlabki nohalol ushlashni emas.
- Asosiy hisobingizni emas, maxsus hisobni ishlating.
- Telegram so'rov hajmi tufayli hisoblarni cheklashi mumkin.

**Qilmaydi** Hech qanday rejim yoki dalil darajasi huquqiy qabul qilinishni, Telegram xabarlarining to'liq yetkazilishini yoki haqiqiy dunyo identifikatsiyasini tasdiqlamaydi.

[O'rnatish bo'yicha qo'llanma](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=uz)[Maxsus hisob](https://phishdestroy.github.io/TgWitness/uz/docs/dedicated-account/)[EVIDENCE.md](https://phishdestroy.github.io/TgWitness/uz/docs/reference/evidence/)[TERGOV.md](https://phishdestroy.github.io/TgWitness/uz/docs/reference/investigation/)
