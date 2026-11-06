# Telegram · Xavfsiz saqlang

Canonical page: https://phishdestroy.github.io/TgWitness/uz/docs/security/

Kompyuteringizdan nima chiqadi, har bir sir nimani ochadi va himoyalar nimani qamraydi, nima esa sizning zimmangizda.

**127.0.0.1**paneldagi manzil bo'yicha

**256 bitli**tasodifiy panel tokeni

**0**CDNlar, analitika yoki masofaviy shriftlar

**Ed25519**har bir yozuvda imzo

## Hammasi shu yerda

Kollektor, panel va har bir yozuv kompyuteringizda qoladi. Standart holatda faqat Telegram bilan bog'laniladi; qolgan hammasi alohida kalit.

06 / NIMA MASHINADAN CHIQADISizning o'rnatishingiz

SIZNING KOMPYUTERINGIZ YOKI SERVERINGIZ

**Panel**127.0.0.1:8787· egasi token

**Yig'uvchi**har bir ish maydoni uchun bitta Telegram klient

MA'LUMOTLAR KATALOGI

**Jurnal**SQLite · hash zanjirli · imzolangan

**Media**SHA-256 bo'yicha nomlangan fayllar

**Ombor**Fernet · sessiya, API juftligi, imzolash kaliti, proksi

- **Telegram**Har doim · sizning yo'nalishingiz bo'ylab

  Hisobning MTProto ulanishi: to'g'ridan-to'g'ri, SOCKS5, HTTP yoki MTProxy. IP ni yashirish rejimi ishlaydigan proksini kutadi. To'g'ridan-to'g'ri zaxira ulanish uchun uni aniq ruxsat etadigan rejim talab etiladi.
- **Sayt tashqarisidagi nusxa**Ixtiyoriy · standart bo'yicha o'chirilgan

  Jurnal, fayllar va tekshiruv nuqtalari S3-mos omborga yuklanishdan oldin AES-GCM bilan shifrlanadi. Kalit sizda qoladi; ilovalar ularning kontent hashi emas, balki kalitli hashlar bo'yicha nomlanadi.
- **Bildirishnomalar**Ixtiyoriy · standart bo'yicha o'chirilgan

  Suhbat sarlavhalari bilan muammolar va o'zgarishlar soni. Xabar parchalarini faqat ularni yoqganingizda yuboriladi.
- **Vaqt tamg'asi vakolati**Ixtiyoriy · standart bo'yicha o'chirilgan

  Faqat imzolangan tekshiruv nuqtasining SHA-256 hash qadami va tasodifiy nonse. Xabarlar yo'q, suhbat nomlari yo'q.
- **Guvoh**Ixtiyoriy · standart bo'yicha o'chirilgan

  Faqat o'qish uchun mo'ljallangan token yordamida imzolangan tekshiruv nuqtalarini va yozib olish hisoblagichlarini oladi. Suhbatlarni o'qiy olmaydi yoki sozlamalarni o'zgartira olmaydi.

Standart bo'yicha: faqat Telegram ulanishi ushbu mashinadan chiqadi.

Ixtiyoriy manzillar har bir ish maydoni bo'yicha sozlanadi. Xabar matni va media ma'lumotlari shifrlanmagan holda ma'lumotlar katalogida saqlanadi: uni disk shifrlash va fayl ruxsatnomalari bilan himoya qiling.

## Har bir sir nimani ochadi

| Maxfiy | Qayerda saqlanadi | Nimani ochadi | Agar u oshkor bo'lsa |
| --- | --- | --- | --- |
| **Panel tokeni** | Ma'lumotlar katalogidagi `panel-token.txt`; brauzer uni har bir yorliq uchun saqlaydi | Har bir ish maydonidagi hamma narsa | TgWitness'ni to'xtating, `panel-token.txt` ni o'chiring, qayta ishga tushiring: yangisini olasiz |
| **Telegram sessiyasi** | Vault, shifrlangan (`credentials.enc`) | Telegram akkaunti o'zi | Telegramda Sessiyani tugatish → *Sozlamalar → Qurilmalar* |
| **Imzolash kaliti** | Vault, shifrlangan (`signing.enc`) | Yozuvlarni sizning barmoq izingiz ostida imzolash | Boshqa joyda saqlangan nazorat nuqtalari, guvoh va vaqt belgilari avval nima bo'lganini baribir ko'rsatadi |
| **Ombor kaliti** | Ma'lumotlar yonidagi `vault.key` yoki tashqi asosiy kalit | Seyf | Sessiya va imzolash kaliti ham sizib chiqqan deb hisoblang |
| **Witness tokeni** | Witness hostida | Faqat o'qish: nazorat nuqtalari va holat | Uni Guvoh sahifasida o'chiring, yangisini yarating |
| **Off-site nusxa kaliti** | Ombor; tiklash uchun bir marta yuklab oling | Off-sayt nusxasi | Bucket'ga ham ega bo'lgan kishi uni ocha oladi: nusxani oshkor bo'lgan deb hisoblang |

## Qanday himoyalar qamrab olinadi

### qamrab olindi

- O'zgartirilgan, olib tashlangan yoki tartibi buzilgan yozuv: xesh zanjiri yoki imzo buziladi.
- Nazorat nuqtasini boshqa joyga saqlaganingizdan keyin qisqartirilgan yoki qayta qurilgan jurnal: nazorat nuqtasi mos kelmay qoladi.
- Tokenni taxmin qilish: 256 tasodifiy bit, doimiy vaqtli solishtirish, daqiqasiga 15 ta xato va manzil bloklanadi.
- Dushmanona chat mazmuni: matn matnligicha qoladi, hech qachon HTML emas; ilovalar fayl sifatida yuklab olinadi; panel boshqa saytlardan hech narsa yuklamaydi.
- Tashqi seyf kaliti bilan o'g'irlangan ma'lumotlar katalogi: sessiyalar va kalitlar shifrlangan qoladi.

### Sizga qoldirildi

- Asosiy token hamma narsani qila oladi. Boshqalarga cheklangan kirish bering va asosiysini o'zingizda saqlang.
- Kompyuterda administrator bo'lgan kishi hamma narsani o'qiy oladi va jurnalni qayta imzolay oladi. Barmoq izi va nazorat nuqtalarini boshqa joyda saqlang.
- TgWitness xabarlar va mediani shifrlamaydi. Diskni shifrlang, ruxsatlarni qattiqlashtiring.
- localhost'dan tashqarida oddiy HTTP tokenni sizdiradi. HTTPS yoki SSH tunnelidan foydalaning.
- Imzolar nima o'tkazib yuborilganini aytmaydi. O'z hisoblaringiz va manbalaringizda qamrovni tekshiring va yetkazishni sinang.

Ruxsatlar, amal qilish muddati va sessiya cheklovlari bilan [ishga kirishni ulashing](https://phishdestroy.github.io/TgWitness/uz/docs/access/).

## O'rnatishni mustahkamlash

8 dan 0 tasi bajarildi

1. **Maxsus Telegram hisobidan foydalaning**, hech qachon asosiysidan emas.
2. **Panelni 127.0.0.1 da saqlang.** Masofaviy kirish faqat HTTPS (birga keladigan Caddy) yoki SSH tunneli orqali.
3. **Diskni shifrlang**, unda ma'lumotlar katalogi bor, xabarlar va media boricha saqlanadi.
4. **Ma'lumotlar katalogini cheklang** xizmat hisobiga (Unix'da 0700, Windows'da papka ruxsatlari).
5. **Serverlarda seyf kalitini boshqa joyda saqlang**: birinchi ishga tushirishdan oldin `TGWITNESS_VAULT_KEY_FILE` ni o'rnating.
6. **Barmoq izi va nazorat nuqtalarini saqlang** boshqa tizimda, guvohni boshqa xostda ishga tushiring.
7. `data/`, sessions, `panel-token.txt` yoki vault kalitlarini GitHubga yoki chatga **hech qachon yuklamang**.
8. `Authorization` sarlavhalarini yoki reverse proxy orqali keladigan so'rov tanalarini **qayd etmang**.

**Panel tokenini ma'lumotlarni yo'qotmasdan o'zgartira olamanmi?**

Ha, u faqat panelni ochadi. TgWitness'ni to'xtating, `panel-token.txt` ni o'chiring, qayta ishga tushiring. Jurnal, sessiyalar va kalitlar qoladi. Agar `TGWITNESS_TOKEN` o'rnatilgan bo'lsa, uning qiymati fayldan ustun turadi.

**Nega xabarlar saqlash vaqtida shifrlanmaydi?**

Kollektor qidirish, solishtirish va eksport qilish uchun ularni o'qishi kerak. Xuddi shu kompyuterdagi kalit o'sha kompyuterni baribir o'qiy oladigan odamni to'xtatmaydi. Disk shifrlash o'g'irlangan diskni, ruxsatlar ishlab turgan tizimni himoya qiladi.

## Zaiflikni xabar qiling

GitHub'da **Security → Report a vulnerability**. Versiya, ta'sir va soxta ma'lumotlar bilan minimal qayta ishlab chiqarish. Hech qachon hisob ma'lumotlari, hisob papkalari yoki haqiqiy dalillarni yubormang. Maxfiy xabar berish o'chirilgan bo'lsa, ekspluatatsiya tafsilotlarisiz maxfiy kanal so'rab issue oching.
