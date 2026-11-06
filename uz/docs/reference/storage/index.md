# Saqlash va tiklash

Canonical page: https://phishdestroy.github.io/TgWitness/uz/docs/reference/storage/

Zaxira nusxalari, eski fayllarni bulutga ko&#x27;chirish, Object Lock ostidagi nusxalar va yangi qurilmada tiklash.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Hujjatlash](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Joylashtirish va tiklash](https://phishdestroy.github.io/TgWitness/uz/docs/reference/deployment/)

![Joylashtirish va tiklash](https://phishdestroy.github.io/TgWitness/assets/chapter-operate.svg)

Panel uchta vazifani ajratadi:

| Vazifa | U nima qiladi |
| --- | --- |
| Zaxira nusxasini saqlang | Imzolangan jurnal, tekshiruv nuqtalari, saqlangan fayllar va navbatga qo'yilgan eksportlarni sozlangan S3 manziliga nusxalash. |
| Mahalliy bepul xotira joyi | Tanlangan eski ilovalarni S3 yoki rclone bulutli masofaviy joyga nusxalash, ularni to'liq qayta o'qish, shifrlangan baytlarni tasdiqlash, so'ngra tasdiqlangan mahalliy nusxani o'chirish. |
| Dalil nusxasini saqlang | S3 Object Lock sozlamalarini o'rnating va qaytarilgan saqlash muddatini tekshiring. Xizmat so'ralgan rejim va sanani tasdiqlashi kerak. |

Joyni bo'shatish imzolangan jurnalni hech qachon o'chirib tashlamaydi yoki qayta yozmaydi. Har bir ilova o'zining asl SHA-256i va tiklash kvitansiyasini saqlaydi. Ixtiyoriy gzip siqish autentifikatsiyalangan shifrlashdan oldin amalga oshiriladi. Bulut fayl nomlari Telegram nomlari, suhbat IDlari yoki asl ilova nomlarini o'z ichiga olmaydi. Bitta ilova 32 GiB gacha bo'lishi mumkin.

Faylni yuklash bo'yicha javob o'zi faylni o'chirishga ruxsat emas.TgWitness to'liq shifrlangan obyektni yuklab oladi va uning hajmi hamdaSHA-256 ni tekshiradi, kvitansiyani saqlaydi, so'ng faylni o'chirishdan oldin mahalliy baytlarni yana bir bor tekshiradi. Yuklash muvaffaqiyatsiz bo'lsa, qayta o'qish boshqacha bo'lsa yoki uzatish bekor qilinsa, mahalliy fayl o'z o'rnida qoladi. Agar yoqilgan dalil zaxirasi hali o'sha faylni nusxalamagan bo'lsa, o'chirish ham uning nusxasini kutadi.

**Ushbu sahifada**

- [Disk to'lib borayotganda](https://phishdestroy.github.io/TgWitness/uz/docs/reference/storage/#when-the-disk-is-filling-up)
- [Maqsadni ulang](https://phishdestroy.github.io/TgWitness/uz/docs/reference/storage/#connect-a-destination)
- [Qayta tiklash faylini saqlang](https://phishdestroy.github.io/TgWitness/uz/docs/reference/storage/#keep-the-recovery-file)
- [O'rnatishni yo'qotgandan keyin tiklash](https://phishdestroy.github.io/TgWitness/uz/docs/reference/storage/#recover-after-losing-the-installation)
- [Operator bot va yakunlash bildirishnomalari](https://phishdestroy.github.io/TgWitness/uz/docs/reference/storage/#operator-bot-and-completion-notices)

## Diskdagi joy kamayganda

Bo‘sh joy **Parametrlar → Biriktirmalar → diskdagi bo‘sh joy** qiymatidan (odatda 1 GiB) kamayganda biriktirmalarni yuklash to‘xtab turadi, navbat saqlanadi. Matn kuzatuvlari davom etadi. Bu bildirishnomalarga bog‘liq emas: ularni o‘chirish yuklash zaxirasi yoki saqlash himoyalarini o‘chirmaydi.

Oldinroq choralar ko‘rish uchun **Avtomatik ishga tushirish**ni yoqing, **Joy bo‘shatish uchun mahalliy faylni o‘chirish**ni tanlang va **Diskda joy kamayganda qo‘shimcha ko‘chirishni boshlash**ni yoqing. Ixtiyoriy qoida odatda bo‘sh joy 5120 MiB dan kam bo‘lganda boshlanadi va 10240 MiB bo‘shaguncha guruhlar bilan ishlaydi. Ikkala chegara sozlanadi. Qo‘lda ishga tushirishdagi manzil, faylning eng kam yoshi, guruh hajmi, to‘liq qayta o‘qib tekshirish va dalillar zaxira nusxasi talablari ishlatiladi. Manzil o‘z-o‘zidan yoqilmaydi. Tekshiruv har 30 soniyada; xato yoki siljish bo‘lmasa keyingi urinish besh daqiqaga kechiktiriladi. Holat va qayta urinish vaqti qayta ishga tushirishda saqlanadi. Qoida faol bo‘lmasa, rejali jarayonlar odatdagi oraliqda ishlaydi.

Panel bo‘sh joy, qadoqlash zaxirasi, qoida tayyorligi va vaqtinchalik joy yetishmagani uchun o‘tkazib yuborilgan fayllarni ko‘rsatadi. Qadoqlash va tiklash boshlanishdan oldin eng yuqori vaqtinchalik joy talabini, yozish paytida esa mavjud joyni tekshiradi. Yuklash uchun belgilangan zaxira ishlatiladi, saqlash operatsiyalari uchun u kamida 64 MiB. Bu fayl tizimi kvotasi emas: boshqa jarayon tekshiruvlar orasida joyni egallashi mumkin.

Gzip masofaviy obyektlarni yo‘qotishsiz siqadi; faol jurnalni kichraytirmaydi va mahalliy arxiv yaratmaydi. JPEG, video va ZIP fayllari juda oz kichrayishi yoki biroz kattalashishi mumkin. Siqish yoqilganda qadoqlash vaqtincha biriktirma hajmining taxminan ikki baravari va zaxira miqdorida joy talab qilishi mumkin. Eng katta fayllarga yetadigan erta boshlash chegarasini tanlang. Tayyorlash uchun juda katta fayl saqlanadi va xabar qilinadi; kichik fayllar hamda oldin tekshirilgan masofaviy nusxalar joy bo‘shata oladi. Tekshirilgan nusxa bo‘lsa, yana qadoqlash faylini yaratmasdan mahalliy faylni olib tashlash mumkin. Tiklash ham vaqtinchalik joy talab qiladi va joy bo‘lguncha rad etilishi mumkin.

Ko‘chirishga mos fayl yoki sozlangan manzil bo‘lmasa, TgWitness joyni avtomatik bo‘shata olmaydi. Saqlash boshqaruvi imzolangan jurnalni hech qachon qisqartirmaydi yoki qayta yozmaydi. Yangi matn kuzatuvlari uchun baribir joy kerak.

## Maqsadni ulang

**Qo'shimchalar → Saqlash va disk joyi → Saqlashni boshqarish**-da vazifa va manzilni tanlang, uni saqlang, so'ngra **Sinov yuklash va yuklab olish**-ni tanlang. Test kichik tasodifiy probani yuklaydi va uni qayta o'qiydi. U Telegram kontentidan foydalanmaydi.

S3 uchun provayderning haqiqiy endpoenti, mintaqasi va bucketidan foydalaning. Wasabi, Backblaze, Cloudflare R2 va boshqa mos xizmatlar bir xil S3 sozlamalarini ishlatadi. Faqat mos API Object Lock qo'llab-quvvatlanishini anglatmaydi. Governance rejimi ruxsat etilgan ma'murga saqlash muddatini chetlab o'tishga imkon berishi mumkin; Compliance rejimida esa boshqa cheklovlar mavjud. Saqlash muddatiga tayanishdan oldin qaytarilgan Object Lock holatini o'qing.

rclone manzili uchun rclone'ning provayder sozlamalari yordamida bir masofaviy ob'ekt yarating va o'sha masofaviy ob'ektning `[name]` bo'limini paneldagi tegishli joyga joylashtiring. O'rnatilgan yordamchi MEGA, Google Drive, OneDrive, Dropbox, Box, pCloud va tanlovchida ko'rsatilgan boshqa provayderlarni qo'llab-quvvatlaydi. Kirish ma'lumotlari ushbu ish maydonining shifrlangan omborida saqlanadi. OAuth yangilanishlari ham omborda saqlanadi. Kirish ma'lumotlari jurnal voqealariga qo'shilmaydi va tiklash yuklamalariga kiritilmaydi.

Yordamchi ish maydoni ichida o'rnatiladi, pinlangan versiya vaSHA-256 bilan. U tizim PATHiga qo'shilmaydi. Sozlash fayllari va ish fayllari shu ish maydoni ichidagi vaqtinchalik fayllardir. Kommanda asosidagi va mahalliy faylga masofaviy ulanishlar rad etiladi. rclone hozirda tashqi so'rovlar uchun aniq tanlangan **To'g'ridan-to'g'ri** yo'nalishni talab qiladi. Ish maydoni uchun SOCKS5 yoki HTTP yo'nalishda mahalliy S3 saqlashdan foydalaning; rclone mavjud bo'lmagan yo'nalishni jimjit chetlab o'tmaydi.

## Qayta tiklash faylini saqlang

Fayllarni nusxalashdan keyin **tiklash faylini saqlashni** tanlang va uni o'rnatish joyidan alohida joyda saqlang. Unda dekripsiya kaliti va imzolangan ob'ekt kvitansiyalari mavjud, shuning uchun uni shaxsiy kalit zaxira nusxasi sifatida muomala qiling. Asl masofaviy konfiguratsiyani va manzil ma'lumotlarini ham alohida saqlang. Keyingi nusxa olishdan oldin olingan tiklash fayli o'sha keyingi faylning kvitansiyasini o'z ichiga olmaydi.

Imzo kalitining barmoq izi alohida yozib qo'yilgan bo'lishi kerak. Faqat shu faylda taqdim etilgan kalitga qarshi tekshirilgan imzo kimning tiklash fayli ekanligini aniqlamaydi.

Mavjud ish maydonchasidagi yo'qolgan saqlash kvitansiyalarini tiklash uchun **saqlangan tiklash faylidan "Fayllarni tiklash"ni** oching va kerakli faylni tanlang. Panel imzoni tekshiradi va xuddi shu ish maydonchasi imzolash kalitini talab qiladi. U boshqa saqlash kalitini almashtirishni rad etadi. Keyin **"Barcha fayllarni tiklash"ni** tanlang. Tiklash avtomatik saqlash qoidasini to'xtatadi, shunda keyingi rejalashtirilgan bosqich tiklangan fayllarni darhol yana o'chirib tashlamaydi. Mahalliy nusxalar bilan ishingiz tugagach, qoidani qayta yoqing.

Qayta tiklash shifrmatni tekshiradi, deşifrlashni autentifikatsiya qiladi, zarur bo'lsa siqilgan ma'lumotni dekompressiya qiladi va faylni joylashtirishdan oldin asl ravshan matn SHA-256ni tekshiradi `media/`. Shikastlangan masofaviy obyekt hech qachon mahalliy faylni almashtirmaydi. Turli baytlarga ega bo'lgan mavjud mahalliy fayl ustidan yozib tashlash o'rniga ko'rib chiqish uchun saqlanadi.

## O'rnatishni yo'qotgandan keyin tiklash

TgWitness-ni boshqa mashinaga o'rnating. Xususiy tiklash faylidan, alohida yozib olingan barmoq izidan va asl manzil ma'lumotlaridan foydalaning:

```
python -m tgwitness.storage recover \
  --recovery storage-recovery.json \
  --fingerprint TRUSTED_WORKSPACE_SHA256 \
  --credentials original-rclone.conf \
  --output recovered-attachments
```

S3 uchun, `--credentials` maxfiy JSON faylga ishora qiladi `access_key` va `secret_key`; imzolangan tiklash fayli manzil sozlamalarini taqdim etadi. Komanda to'g'ridan-to'g'ri tashqi ulanishdan foydalanadi va rclone masofaviy ulanishi bunga muhtoj bo'lganda mahkamlangan yordamchi dasturni yuklab oladi. U mavjud chiqish katalogini rad etadi.

Qayta tiklangan asl baytlarga yoziladi `recovered-attachments/media/`, ularning SHA-256i bo'yicha nomlangan. `recovery-log.jsonl` — tiklash operatsiyalarining imzolanmagan yozuvi. Bu buyruq yo'qolgan imzolangan jurnalni yoki uning imzolash kalitini qayta yaratmaydi. Ular uchun to'liq ish maydoni zaxira nusxasini saqlang. Saqlashni tiklash fayli to'liq ish maydoni zaxira nusxasi emas.

## Operator bot va yakunlash bildirishnomalari

Telegram boti operatorga tegishli. Uni BotFather orqali yarating va panelda uning tokeni, manzil chat hamda aniq ruxsat etilgan Telegram foydalanuvchi identifikatorlarini sozlang. Jo'natuvchi hamda chat mos kelishi kerak. Boshqa botlardan kelgan yo'naltirilgan xabarlar va buyruqlar e'tiborsiz qoldiriladi.

`/status` va `/stats` bo'lsa, standart faqat holat rejimida mavjud. Ixtiyoriy boshqaruv rejimi qo'shadi `/pause`, `/resume` va `/copy`. `/copy` sozlangan saqlash vazifasini so'raydi; bu masofaviy yuklash allaqachon tugaganligini anglatmaydi. Buyruqlar ixtiyoriy URL manzillarni, fayllarni yoki shell dasturlarini taqdim eta olmaydi.

Ogohlantirishlar va vazifani bajarish uchun alohida bildirishnoma sozlamalaridan foydalaning. Bajarish bildirishnomalari bo'shliqlar bilan hisob eksportini to'liq eksportdan ajratib ko'rsatadi va tarix hamda saqlash hajmlari sonini ko'rsatadi. Xabar parchalarini bildirishnoma sozlamalarida alohida yoqilmagan taqdirda kiritilmaydi. Xizmat tanlovchisi provayder misollarining doimiy to'plami o'rniga haqiqiy o'rnatilgan Apprise katalogidan shakllantiriladi.
