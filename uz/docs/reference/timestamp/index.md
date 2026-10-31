# Vaqt tamg'alari

Canonical page: https://phishdestroy.github.io/TgWitness/uz/docs/reference/timestamp/

RFC 3161 timestamplari imzolangan tekshiruv nuqtalari uchun: vakolatli organiga nima yuboriladi va javob qanday tasdiqlanadi.

TgWitness RFC 3161 so'rovlarini tayyorlaydi va timestamp authority (TSA) javoblarini tasdiqlaydi. Ushbu qo'lda bajariladigan protsedura na TSA tanlaydi, na ma'lumot yuboradi; dalil rejimi esa bularning ikkalasini ham jadval ([dalil formati](https://phishdestroy.github.io/TgWitness/uz/docs/reference/evidence/#rfc-3161-preparation-and-response-verification-02)) bo'yicha bajaradi. Tayyorlangan so'rov **hali timestamp isbotini** tashkil **etmaydi**.

## Dalil nima bilan bog'lanadi

Oqim sxemasi · Hisob kuzatuvlari → SHA-256 zanjiri va Ed25519 imzolari; SHA-256 zanjiri va Ed25519 imzolari → Imzolangan tekshiruv nuqtasi; Imzolangan tekshiruv nuqtasi → Aniq baytli xesh va tasodifiy nonse; Aniq baytli xesh va tasodifiy nonse → RFC 3161 so'rovi; RFC 3161 so'rovi → Mustaqil TSA; Mustaqil TSA → Imzolangan TSA javobi; Imzolangan tekshiruv nuqtasi → Ma'lumotlarni, nonse va aniq CA ishonchini tasdiqlang; Imzolangan TSA javobi → Ma'lumotlarni, nonse va aniq CA ishonchini tasdiqlang · Hisob kuzatuvlari · SHA-256 zanjiri vaEd25519 imzolari · Imzolangan tekshiruvnuqtasi · Aniq baytli xesh vatasodifiy nonse · RFC 3161 so'rovi · Mustaqil TSA · Imzolangan TSA javobi · Ma'lumotlarni, nonseva aniq CA ishonchinitasdiqlang

**Diagramma matn sifatida**

1. Hisob kuzatuvlari → SHA-256 zanjiri va Ed25519 imzolari
2. SHA-256 zanjiri va Ed25519 imzolari → Imzolangan tekshiruv nuqtasi
3. Imzolangan tekshiruv nuqtasi → Aniq baytli xesh va tasodifiy nonse
4. Aniq baytli xesh va tasodifiy nonse → RFC 3161 so'rovi
5. RFC 3161 so'rovi → Mustaqil TSA
6. Mustaqil TSA → Imzolangan TSA javobi
7. Imzolangan tekshiruv nuqtasi → Ma'lumotlarni, nonse va aniq CA ishonchini tasdiqlang
8. Imzolangan TSA javobi → Ma'lumotlarni, nonse va aniq CA ishonchini tasdiqlang

Yig'uvchining imzosi yozuvlarni uning kalitiga bog'laydi. Ishonchli TSA javobi TSA tomonidan ko'rsatilgan vaqtda ma'lum bir nazorat-o'tkazish punkti mavjud bo'lganini tasdiqlashi mumkin. Nazorat-o'tkazish punkti keyin jurnal prefiksini bog'lashi mumkin. Bu har bir Telegram harakati vaqtini yoki qayd etilgan kontentning rostligini aniqlamaydi.

## Protsedura

1. Yig'uvchi kalit barmoq izini alohida ishonchli kanal orqali saqlang. Faqat tekshirilgan ZIP taqdim etgan kalit yig'uvchini aniqlash uchun yetarli emas.
2. **Eksportlar → Timestamp so'rovini tayyorlash** bo'limidan tanlangan ish maydonining so'rov ZIP-faylini yuklab oling. `checkpoint.json`, `timestamp.tsq`, `SHA256SUMS` va `README.txt` fayllarini arxivdan chiqarib oling. Checkpoint baytlarini o'zgartirmang.
3. Tergovga mos TSA tanlang. `timestamp.tsq` ni hujjatlashtirilgan usuli orqali yuboring, HTTP xizmati uchun `application/timestamp-query` ni ishlating. Asl ikhtiyoriy javobni `timestamp.tsr`, endpoint, olingan vaqt va so'rov natijasini saqlang. So'rov xabarlar o'rniga xesh va nonse-dan iborat; tarmoq metama'lumotlari esa so'rovni hanuzgacha oshkor qiladi.
4. Javobdan qat'i nazar ishonchli ildiz sertifikatini va zarur bo'lgan barcha oraliq sertifikatlarni oling. Javobda keltirilgan sertifikat faqat shu sababli ishonchli bo'lib qolmaydi.
5. Ishonchli TgWitness o'rnatilmasidan tekshiring:

```
python -m tgwitness.anchor verify --checkpoint checkpoint.json --request timestamp.tsq --response timestamp.tsr --ca trusted-tsa-root.pem
```

Kerak bo'lsa `--intermediates tsa-intermediates.pem` yoki `--openssl /path/to/openssl` ni qo'shing. OpenSSL `ts` ni qo'llab-quvvatlashi kerak. Windowsda verifikator shuningdek standart Git o'rnatilishini ham qidiradi. OpenSSL 3.5.9 sintetik CA/TSA bilan mahalliy sharoitda sinovdan o'tkazilgan.

1. Chekpointdan keyin imzolangan jurnalni ZIP-fayl sifatida eksport qiling, shunda u shu prefiksni o'z ichiga oladi. Mustaqil ravishda ma'lum barmoq izi yordamida tekshiring:

```
python tgwitness/verify.py evidence.zip --fingerprint TRUSTED_SHA256 --checkpoint checkpoint.json
```

1. ZIP-faylni, tekshiruv nuqtasini, so'rov va javoblarni, sertifikat zanjirini, tasdiqlash natijalarini va topshirish yozuvini kollektor tashqarisida saqlang. Qabul qilinganda tasdiqlashni takrorlang.

Saqlangan tekshiruv nuqtasidan so'rov tayyorlash:

```
python -m tgwitness.anchor prepare checkpoint.json --out timestamp-request.zip
```

Tayyorlash JSONni kanoniklashtiradi va arxivga mos checkpointni kiritadi. TSA tasdiqlash uchun **o'sha arxivdagi checkpoint baytlar**idan foydalaning, hattoki kirish faylida bo'sh joylar boshqacha bo'lsa ham.

## Verifikatsiya chegaralari

| Tekshirish | Joriy xatti-harakat |
| --- | --- |
| Ma'lumotlar | Aniq checkpoint baytlari SHA-256 hashi javob bilan mos kelishi kerak |
| So'rov | `--request` yordamida asl so'rov va nonse tasdiqlanadi |
| TSA imzosi | OpenSSL imzo va aniq CA zanjirini tasdiqlaydi |
| Yig'uvchi imzosi | Alohida tarzda jurnal verifikatori tomonidan mahkamlangan kalit yordamida tasdiqlangan |
| Bekor qilish | Avtomatik OCSP/CRL olish yo'q |
| Uzoq muddatli haqiqiylik | Sertifikat muddati tugagach arxivni tasdiqlash bo'lmaydi |
| Rejalashtirilgan topshirish | Dalil rejimi, standart bo'yicha o'chirilgan |

`--request` texnik jihatdan ixtiyoriy, lekin uni kiritmaslik asl nonse-ni tasdiqlashni oldini oladi. Ushbu to'liq protsedura uchun natijaning `request_checked` rost bo'lishi kerak. Sertifikatlashni tekshirish o'rnatilgan OpenSSL qoidalari va tasdiqlash vaqtiga muvofiq amalga oshiriladi. Uzoq muddatli saqlash uchun alohida sertifikat/bekor qilish dalillari siyosati kerak.

Amaldagi kriptografik imzo avtomatik ravishda malakali vaqt tamg'asi yoki huquqiy qabul qiluvchanlikni aniqlashni anglatmaydi. Agar operator vaqt tamg'asi qo'yishdan oldin kuzatuvlarni soxtalashtirgan bo'lsa, TSA o'sha baytlarni mahkamlaydi; bu ularning rostligini tasdiqlamaydi.

## Topshirish yozuvi

Ish identifikatori, yuboruvchi va qabul qiluvchi, UTC bo'yicha uzatish vaqti va uning manbai, maqsadi, fayl nomlari/SHA-256 qiymatlari, yig'uvchining barmoq izi, ketma-ketlik diapazoni, ma'lum bo'shliqlar, tekshiruvchi versiyasi va tekshiruv natijasini qayd eting. Ushbu yozuvni imzolang va uni tashkilotingiz jarayoni orqali mustaqil ravishda saqlang. TgWitness'da ko'p foydalanuvchili saqlash yozuvi tizimi joriy etilmagan.

Rivojlantirish jarayonida mustaqil jonli TSA bilan bog'lanilmagan. Mahalliy testlar moslikni va o'zgartirilgan ma'lumotlar, nonse yoki CA rad etilishini tekshirish uchun sintetik CA/TSA yaratadi.
