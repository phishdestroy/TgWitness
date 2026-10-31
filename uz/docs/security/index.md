# Xavfsiz saqlang

Canonical page: https://phishdestroy.github.io/TgWitness/uz/docs/security/

Telegram yo'llarini, ommaviy proksi ro'yxatlarini va ixtiyoriy tashqi xizmatlarni bilib oling. Har bir sir nimani ochishini, qaysi himoyalar nima qamrab olishini va nimalarni sizga qoldirishini bilib oling.

**127.0.0.1**paneldagi manzil bo'yicha

**256-bit**tasodifiy panel tokeni

**0**CDNlar, analitika yoki masofaviy shriftlar

**Ed25519**har bir yozuvda imzo

## Hammasi shu yerda

Yig'uvchi, uning paneli va har bir saqlangan yozuv uni ishga tushirgan kompyuterda yoki serverda qoladi. Telegram standart bo'yicha yagona manzil; boshqa har biri alohida kalitdir.

06 / NIMA MASHINADAN CHIQADISizning o'rnatishingiz

SIZNING KOMPYUTERINGIZ YOKI SERVERINGIZ

**Panel**127.0.0.1:8787 · bearer token

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
| **Panel tokeni** | `panel-token.txt` ma'lumotlar katalogida; brauzer uni faqat teg uchun saqlaydi | Har bir ish maydonidagi hamma narsa: o'qish va eksport qilish, doirani o'zgartirish, hisoblarga kirish | TgWitnessni to'xtating, `panel-token.txt`ni o'chiring, qayta ishga tushiring: yangi token yaratiladi |
| **Telegram sessiyasi** | Vault, shifrlangan (`credentials.enc`) | Telegram akkaunti o'zi | Telegramda Sessiyani tugatish → *Sozlamalar → Qurilmalar* |
| **Imzolash kaliti** | Vault, shifrlangan (`signing.enc`) | Imzolash yozuvlari sizning barmoq izingiz ostida tasdiqlanadi | Boshqa joyda saqlangan tekshiruv nuqtalari, guvoh va vaqt tamg'alari oldin nima mavjud bo'lganini ko'rsatadi |
| **Ombor kaliti** | Ma'lumotlar yonidagi `vault.key` yoki yangi ma'lumotlar katalogi uchun tashqi bosh kalit | Seifni dekriptirovka qilish | Sessiya va imzolash kalitini ham oshkor bo'lgan deb hisoblang |
| **Witness tokeni** | Witness hostida | Faqat o'qish uchun: imzolangan tekshiruv nuqtalari va holat | Uni Witness sahifasida o'chirib tashlang; yangi birini yarating |
| **Off-site nusxa kaliti** | Ombor; tiklash uchun bir marta yuklab oling | Sirtdagi nusxani dekriptaj qilish | Saqlangan ob'ektlarga egalik qiluvchi har kim ularni dekript qila oladi: o'sha nusxani oshkor deb hisoblang |

## Qanday himoyalar qamrab olinadi

### qamrab olindi

- Eksportda o'zgartirilgan, olib tashlangan yoki tartibi o'zgartirilgan yozuv: xesh zanjiri yoki imzo endi tasdiqlanmaydi.
- Jurnal tekshiruv nuqtasidan keyin qayta tiklangan yoki qayta qurilgan, lekin tekshiruv nuqtasi boshqa joyda saqlangan: saqlangan tekshiruv nuqtasi endi mos kelmaydi.
- Panel tokenini taxmin qilish: 256 tasodifiy bit, doimiy vaqt ichida solishtiriladi; 15 marta xato qilgandan so'ng manzil rad etiladi.
- Dushmanona chat kontenti: matn xuddi matn sifatida kiritiladi, hech qachon HTML sifatida emas; ilovalar fayllar sifatida yuklanadi; panel boshqa saytlardan hech narsa yuklamaydi.
- Tashqi ombor kaliti bilan nusxalangan ma'lumotlar katalogi: sessiyalar va imzolash kalitlari bosh kalitsiz shifrlangan holda qoladi.

### Sizga qoldirildi

- Asosiy panel tokeni to'liq nazoratga ega. Boshqa odamlarga kerakli hisoblar, suhbatlar va harakatlarga chegaralangan kirish huquqini bering; asosiy kalitni maxfiy saqlang.
- Uskunaning administratori hamma narsani o'qishi, jurnalni qayta yozishi va qayta imzolashi mumkin. Barmoq izi va tekshiruv nuqtalarini boshqa tizimda saqlang.
- TgWitness xabar matni va media fayllarini shifrlamaydi. Diskni shifrlash va qat'iy ruxsatnomalarni qo'llang.
- Localhostdan tashqaridagi oddiy HTTP tarmoqda tokenni ko'rsatadi. HTTPS yoki SSH tunneli ishlating.
- Imzolar yozib olingan ma'lumot o'zgartirilmaganligini tasdiqlaydi, har bir Telegram hodisasi yozib olinganligini emas.

Ruxsatlar, amal qilish muddati va sessiya cheklovlari bilan [ishga kirish huquqini ulashing](https://phishdestroy.github.io/TgWitness/uz/docs/access/). Guvoh tokeni alohida kirish vositasi bo‘lib qoladi.

## O'rnatishni mustahkamlash

8 dan 0 tasi bajarildi

1. **Maxsus Telegram hisobidan foydalaning** — hech qachon asosiy hisobingizni ishlatmang. Panel tokeni va sessiya unga to'liq nazorat beradi.
2. **Paneldagi manzilni 127.0.0.1 da saqlang.** Unga faqat HTTPS (biriktirilgan Caddy konfiguratsiyasi) yoki SSH tunneli orqali masofadan ulanish mumkin.
3. Ma'lumotlar katalogi saqlangan **diskni shifrlang**: xabar matni va media fayllari kelganidek saqlanadi.
4. **Ma'lumotlar katalogini** faqat xizmat akkaunti uchun **cheklang**. Unixda yangi kataloglarga 0700 rejimi beriladi; Windowsda papkaning ruxsatlarini sozlang.
5. **Saqlash omborining bosh kalitini** serverlarda **boshqa joyda saqlang**: ma'lumotlar katalogini yaratishdan oldin `TGWITNESS_VAULT_KEY_FILE` ni o'rnating.
6. **Imzolash kalitining barmoq izi va tekshiruv nuqtalarini** boshqa tizimda **saqlang** va guvohni boshqa mezbon tizimiga qo'shing.
7. `data/`, sessions, `panel-token.txt` yoki vault kalitlarini GitHubga yoki chatga **hech qachon yuklamang**.
8. `Authorization` sarlavhalarini yoki reverse proxy orqali keladigan so'rov tanalarini **qayd etmang**.

**Panel tokenini ma'lumotlarni yo'qotmasdan o'zgartira olamanmi?**

Ha. Token faqat panelni ochadi. TgWitness'ni to'xtating, ma'lumotlar katalogidan `panel-token.txt`ni o'chiring va uni qayta ishga tushiring; jurnal, sessiyalar va kalitlar o'zgarmagan holda qoladi. `TGWITNESS_TOKEN` o'rnatilganda, fayl o'rniga muhit qiymati ishlatiladi.

**Nega xabarlar saqlash vaqtida shifrlanmaydi?**

Yig'uvchi ularni o'qishi, qidirishi, versiyalarni solishtirishi va eksport qilishi kerak. Ularni shu kompyuterdagi kalit bilan shifrlash, kompyuterni o'qiy oladigan kishi uchun deyarli hech qanday himoya qo'shmaydi. Diskni shifrlash to'xtatilgan yoki o'g'irlangan diskni himoya qiladi; qat'iy ruxsatnomalar esa ishlayotgan diskni himoya qiladi.

## Zaiflikni xabar qiling

GitHub omborida **xavfsizlik → zaiflikni xabar qilish**bo'limidan foydalaning. Versiyani, ta'sir darajasini va minimal sun'iy qayta yaratishni kiritishni unutmang. Hech qachon kirish ma'lumotlari, akkaunt papkalarini yoki haqiqiy dalillar arxivlarini yubormang. Agar shaxsiy xabar berish imkoni bo'lmasa, ekspluatatsiya tafsilotlarisiz shaxsiy kanal so'rab issue oching.
