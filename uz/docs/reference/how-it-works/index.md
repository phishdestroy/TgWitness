# Dalil qanday ishlaydi

Canonical page: https://phishdestroy.github.io/TgWitness/uz/docs/reference/how-it-works/

Hash zanjiri, imzolar, tekshiruv nuqtalari va guvohlar verifikator ishlatadigan aniq formulalar bilan tushuntirilgan.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Hujjatlash](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Dalil va tasdiqlash](https://phishdestroy.github.io/TgWitness/uz/docs/reference/evidence/)

![Dalil va tasdiqlash](https://phishdestroy.github.io/TgWitness/assets/chapter-evidence.svg)

TgWitness yig'uvchi akkaunt tomonidan kuzatilganlarni saqlaydi, bu kuzatuvlarni imzolangan jurnalga bog'laydi va boshqa shaxsga ishonchli kalit hamda oldin saqlangan tekshiruv nuqtasiga nisbatan eksportni tasdiqlash imkonini beradi.

[Mahalliy hujjatlar veb-sayti](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/PUBLISHING.md#preview-the-website-locally)`/docs/concepts/` manzilida interaktiv misollar, `/docs/witness/` manzilida Checkpoint qarorlar eksplorerini va [Case Board](https://phishdestroy.github.io/TgWitness/uz/docs/reference/case-board/), [hisobot dizayni](https://phishdestroy.github.io/TgWitness/uz/docs/reference/case-reports/) hamda [topshirish](https://phishdestroy.github.io/TgWitness/uz/docs/reference/evidence/#handover-extract) bo'yicha bosqichma-bosqich ko'rsatmalarni o'z ichiga oladi. Barcha misol xabarlar, hisoblar va kechikishlar tasodifiydir. Zanjirli qumdonidagi xeshlar brauzerda SHA-256 yordamida hisoblanadi. Hech narsa Telegramga yuborilmaydi.

**Ushbu sahifada**

- [Xabar o'zgaradi; kuzatuvlar to'planadi](https://phishdestroy.github.io/TgWitness/uz/docs/reference/how-it-works/#a-message-changes-observations-accumulate)
- [Hash nima qamrab oladi](https://phishdestroy.github.io/TgWitness/uz/docs/reference/how-it-works/#what-a-hash-covers)
- [Oldingi tekshiruv nuqtasi nimani qo'shadi](https://phishdestroy.github.io/TgWitness/uz/docs/reference/how-it-works/#what-an-earlier-checkpoint-adds)
- [Guvoh qayerda tegishli](https://phishdestroy.github.io/TgWitness/uz/docs/reference/how-it-works/#where-a-witness-belongs)
- [Ma'lum harakatlarga qarshi test yetkazib berish](https://phishdestroy.github.io/TgWitness/uz/docs/reference/how-it-works/#test-delivery-against-known-actions)
- [Ish jarayonini tanlang](https://phishdestroy.github.io/TgWitness/uz/docs/reference/how-it-works/#pick-a-workflow)

## Xabar o'zgaradi; kuzatuvlar to'planadi

Ketma-ketlik diagrammasi · Telegram → Yig'uvchi: Yangi xabar: Soat 10:00 da uchrashamiz; Yig'uvchi → Imzolangan jurnal: xabar.yangi ilova qiling; Telegram → Yig'uvchi: Tahrir: Soat 11:00 da uchrashamiz; Yig'uvchi → Imzolangan jurnal: Xabarni ilova qiling.tahrirlangan; Telegram → Yig'uvchi: O'chirish to'g'risidagi bildirishnoma; Yig'uvchi → Imzolangan jurnal: Qo'shimcha: message.deleted; Imzolangan jurnal bo'yicha eslatma: Asl xabar + tahrir + o'chirish kuzatuvi qoladi · Telegram · Yig'uvchi · Imzolangan jurnal · Yangi xabar: Soat 10:00 da uchrashamiz · xabar.yangi ilova qiling · Tahrir: Soat 11:00 da uchrashamiz · Xabarni ilova qiling.tahrirlangan · O'chirish to'g'risidagi bildirishnoma · Qo'shimcha: message.deleted · Asl xabar + tahrir + o'chirish kuzatuvi qoladi

**Diagramma matn sifatida**

1. Telegram → Yig'uvchi: Yangi xabar: Soat 10:00 da uchrashamiz
2. Yig'uvchi → Imzolangan jurnal: xabar.yangi ilova qiling
3. Telegram → Yig'uvchi: Tahrir: Soat 11:00 da uchrashamiz
4. Yig'uvchi → Imzolangan jurnal: Xabarni ilova qiling.tahrirlangan
5. Telegram → Yig'uvchi: O'chirish to'g'risidagi bildirishnoma
6. Yig'uvchi → Imzolangan jurnal: Qo'shimcha: message.deleted
7. Imzolangan jurnal bo'yicha eslatma: Asl xabar + tahrir + o'chirish kuzatuvi qoladi

Ushbu soddalashtirilgan ketma-ketlik Telegram har bir yangilanishni yetkazganini va tanlangan akkaunt uni ko'ra olganini taxmin qiladi. Operatsion voqealar ham jurnalga kiritiladi. O'chirish to'g'risidagi bildirishnoma o'chiruvchini yoki aniq o'chirish vaqtini ko'rsatmaydi. Takroriy yetkazib berishlar alohida kuzatuvlar bo'lib, jurnal bo'ylab nusxa ko'chirishni bostirish mavjud emas.

## Hash nima qamrab oladi

![Kuzating, kodlang, xeshlang va imzolang: har bir yangi voqea oldingi xeshni o'z ichiga oladi.](https://phishdestroy.github.io/TgWitness/assets/evidence-chain-animated.svg)

Formulani ichkaridan tashqariga o'qing: **C** to'qqizta maydonni aniq baytlarga aylantiradi; **SHA-256** ularning digestini hosil qiladi; **hex** esa shu digestni qanday saqlanishini ko'rsatadi. Oldingi hash allaqachon voqeada mavjud. **unhex** saqlangan hashni Ed25519 imzolaydigan 32 baytga qaytaradi.

[Statik zanjir diagrammasi](https://github.com/phishdestroy/TgWitness/blob/main/docs/assets/presentation/evidence-chain-static.svg)

C(ei)ni to'qqizta voqea maydonining kanonik UTF-8 JSONi deb oling. Birinchi `previous_hash` 64 ta nol belgisidan iborat. Keyingi har bir yozuv oldingi yozuvning geksadesimal xeshini o'z ichiga oladi:

hi = hex(SHA256(C(ei)))

σi = Ed25519.Sign(sk,unhex(hi))

Imzo 32 xom digest baytlarini qamrab oladi. Hash kirishiga aynan quyidagilar kiradi: `seq`, `observed_at`, `source_at`, `kind`, `chat_id`, `message_id`, `actor_id`, `payload` va `previous_hash`. Ob'ekt kalitlari tartiblangan; bo'sh joylar va ASCII qochirishlari chiqarib tashlanadi; NaN va cheksizlik rad etiladi. [Aniq kodlash](https://phishdestroy.github.io/TgWitness/uz/docs/reference/evidence/#event-canonicalization)ni ko'ring.

Oqim sxemasi · 64 nol belgisi → Yozuv 1 / hash h1; Yozuv 1 / hash h1 → Yozuv 2 ga h1 / hash h2 kiradi; Yozuv 2 ga h1 / hash h2 kiradi → Yozuv 3 h2 / hash h3 ni o'z ichiga oladi; Yozuv 3 h2 / hash h3 ni o'z ichiga oladi → Imzolangan tekshiruv nuqtasi: 3-bosqich, h3 sarlavhasi (boshqa joyda saqlash) · 64 nol belgisi · Yozuv 1 / hash h1 · Yozuv 2 ga h1 / hashh2 kiradi · Yozuv 3 h2 / hash h3ni o'z ichiga oladi · Imzolangan tekshiruvnuqtasi: 3-bosqich, h3sarlavhasi · boshqa joyda saqlash

**Diagramma matn sifatida**

1. 64 nol belgisi → Yozuv 1 / hash h1
2. Yozuv 1 / hash h1 → Yozuv 2 ga h1 / hash h2 kiradi
3. Yozuv 2 ga h1 / hash h2 kiradi → Yozuv 3 h2 / hash h3 ni o'z ichiga oladi
4. Yozuv 3 h2 / hash h3 ni o'z ichiga oladi → Imzolangan tekshiruv nuqtasi: 3-bosqich, h3 sarlavhasi (boshqa joyda saqlash)

| Taqdim etilgan jurnalga o'ting | Nima uni aniqlaydi |
| --- | --- |
| 2-yozuvni o'zgartiring, saqlangan xeshini esa o'zgarmas holda qoldiring | Qayta hisoblangan voqea xeshidan farq qiladi; uning imzosi o'zgartirilgan voqeani endi qamrab olmaydi |
| O'zgartirilgan yozuvni va keyingi barcha hashlarni qayta tuzing | Asl imzolar muvaffaqiyatsiz bo'ladi; ta'sirlangan chegaradagi saqlangan tekshiruv nuqtasi ham nomuvofiqlik ko'rsatadi |
| Oxirgi qismini olib tashlang, lekin qolgan prefiksni o'z holicha saqlang | Taqdim etilgan prefiksdan keyin saqlangan oldingi tekshiruv nuqtasi eksport juda qisqa ekanligini ko'rsatadi |
| Zaxira jurnalni boshqa kalit bilan qayta imzolash | Alohida ishonchli kalit barmoq izi almashtirilgan shaxsni rad etadi |

![Saqlangan maydonni o'zgartirish uning digesti o'zgarishiga olib keladi; hashlarni qayta hisoblash esa asl imzolarni tiklamaydi.](https://phishdestroy.github.io/TgWitness/assets/evidence-tamper-animated.svg)

**Yozuv 2da mantiqni sinab ko'ring:** saqlangan voqeada `Meet at 11:00`ni `Meet at 12:00`ga o'zgartiring. Uning qayta hisoblangan xeshida moslik qolmaydi. Keyingi zanjirni qayta hisoblash uning bog'lanmalarini tiklashi mumkin, ammo dastlabki imzolar yangi digestlarni qamrab ololmaydi. Aksincha, kuzatilgan Telegram tahriri yangi jurnal yozuvi bo'lib qoladi.

[Statik o'zgarish diagrammasi](https://github.com/phishdestroy/TgWitness/blob/main/docs/assets/presentation/evidence-tamper-static.svg)

Hash havolalari o'z-o'zidan kimnidir almashtirilgan zanjirni qayta hisoblashdan to'xtatmaydi. Ishonch mustaqil ishonchli kalit ostidagi imzo tekshirish va kollektor tashqarisida saqlangan havolalar bilan solishtirish orqali paydo bo'ladi.

## Oldingi tekshiruv nuqtasi nimani qo'shadi

![3-raqamni saqlang va h3 sarlavhasini qo'ying; keyinchalik 4 ta yozuvni 3-pozitsiyada tekshirish amalga oshiriladi.](https://phishdestroy.github.io/TgWitness/assets/evidence-checkpoint-animated.svg)

**Jurnal o'sib borgan sari referensiya o'zgarmas qoladi.** Agar tekshiruv nuqtasi "3 yozuv, boshlang h3" desa, to'rt yozuvli eksport 3-pozitsiyadagi h3 ga mos kelib o'tishi mumkin. Uning eng yangi boshi h4 bo'lib, u farq qilishi kutiladi. Faqat ikki yozuvli eksport esa muvaffaqiyatsiz tugaydi.

[Statik tekshiruv nuqtasi diagrammasi](https://github.com/phishdestroy/TgWitness/blob/main/docs/assets/presentation/evidence-checkpoint-static.svg)

Tekshiruv nuqtasining imzosini tasdiqlaganingizdan so'ng, quyidagilarni talab qiling:

Nexport ≥ Ncheckpoint and hexport[Ncheckpoint] = Hcheckpoint

Eksport tekshiruv nuqtasidan tashqariga cho'zilishi mumkin. U saqlangan chegarada mos kelishi kerak. Haqiqiy verifikator har bir voqeaning ketma-ketligi, avvalgi havolasi, xesh va imzosini ham tekshiradi. Faqat oxirgi saqlangan bosh qismini solishtirish o'zgartirilgan ichki yozuvni, uning saqlangan xeshi yangilanmagan bo'lsa, aniqlamaydi.

## Guvoh o'z o'rnida

Oqim sxemasi · Yig'uvchi / hisob sessiyasi / kalit A → Faqat o'qish uchun mo'ljallangan tekshiruv nuqtasi oxiri; Witness / mahkamlangan yig'uvchi kalit / o'z kalit B → Alohida imzolangan guvoh jurnali; Witness / mahkamlangan yig'uvchi kalit / o'z kalit B → Faqat o'qish uchun mo'ljallangan tekshiruv nuqtasi oxiri (Tekshiruvni so'rang); Faqat o'qish uchun mo'ljallangan tekshiruv nuqtasi oxiri → Witness / mahkamlangan yig'uvchi kalit / o'z kalit B (Imzolangan javob); Witness / mahkamlangan yig'uvchi kalit / o'z kalit B → Imzolangan TGW1 postlari kanali (Bot API / o'z tokeni) · Mehmondo'st A · Mehmon B · Yig'uvchi / hisobsessiyasi / kalit A · Faqat o'qish uchunmo'ljallangan tekshiruvnuqtasi oxiri · Witness / mahkamlanganyig'uvchi kalit / o'zkalit B · Alohida imzolangan guvohjurnali · Imzolangan TGW1 postlarikanali · Tekshiruvni so'rang · Imzolangan javob · Bot API / o'z tokeni

**Diagramma matn sifatida**

1. Yig'uvchi / hisob sessiyasi / kalit A → Faqat o'qish uchun mo'ljallangan tekshiruv nuqtasi oxiri
2. Witness / mahkamlangan yig'uvchi kalit / o'z kalit B → Alohida imzolangan guvoh jurnali
3. Witness / mahkamlangan yig'uvchi kalit / o'z kalit B → Faqat o'qish uchun mo'ljallangan tekshiruv nuqtasi oxiri (Tekshiruvni so'rang)
4. Faqat o'qish uchun mo'ljallangan tekshiruv nuqtasi oxiri → Witness / mahkamlangan yig'uvchi kalit / o'z kalit B (Imzolangan javob)
5. Witness / mahkamlangan yig'uvchi kalit / o'z kalit B → Imzolangan TGW1 postlari kanali (Bot API / o'z tokeni)

Guvoh rollbackni, bir xil hisobda boshqa sarlavhani, o'zgartirilgan kalitlarni, noto'g'ri javoblarni va yetishmayotgan javoblarni qayd etadi. Faqat katta hisob har bir avvalgi yozuv o'zgarmaganligini aniqlamaydi; saqlangan tekshiruv nuqtalari bilan eksportni solishtiring. Boshqa mezbonidagi guvoh yig'uvchining mezbonidagi uzilishni bo'lishishdan saqlaydi; alohida operator esa qo'shimcha mustaqillik beradi.

Guvox yig'uvchining xabar bergan jurnal holatini tasdiqlaydi. Telegram harakatlarining qaysilari yig'uvchi hisobga yetib borganini o'lchash uchun nazoratli yetkazib berish testidan foydalaning. [Guvoxni sozlashni](https://phishdestroy.github.io/TgWitness/uz/docs/reference/witness/) ko'ring.

## Ma'lum harakatlarga qarshi test yetkazib berish

Nazorat guruhidan foydalaning, alohida yig'ish akkauntlari va yangi marker belgilang. Jo'nating, tahrirlang va o'chirib tashlang, bosqichlar orasida yozib olishni tekshirib turing. Natijalarni ko'zdan kechirishdan oldin kutilayotgan harakatlar va kesish nuqtasini aniqlang.

R = |observed∩expected| / |expected| Δ t = treceipt - taction

Faqat mos kelgan kutilgan harakatlar hisobga olinadi; takroriy kvitansiyalar hisoblagichni oshirmaydi. Qisminom nol bo'lmasligi kerak. Yo'qolgan kvitansiyada o'lchangan kechikish bo'lmaydi. Hujjatda soat noaniqligini qayd eting; Telegram aniq o'chirish vaqtini taqdim etmagani uchun o'zingiz nazorat qiladigan o'chirish harakati vaqtidan foydalaning. 5/6 (83,3%) kabi natija test harakatlarini tasvirlaydi, barcha Telegram trafigining to'liqligini emas.

## Ish jarayonini tanlang

[To'liq tergov bosqichlari](https://phishdestroy.github.io/TgWitness/uz/docs/reference/investigation/) kanalda, guruhda, botda va shaxsiy suhbatda sodir bo'lgan hodisani kuzatadi:

1. Maxsus yig'ish hisobida butun hisobni tergov rejimiga o'tkazing va inventorizatsiya qilinadigan suhbatlarni yoqish. Asosiy hisob uchun tanlangan suhbatlar yoki papkani ishlating.
2. Jurnal snapshotlarini, har bir chat bo'yicha to'liq tarixni va saqlangan ilovalarni oling.
3. Jonli o'zgarishlarni va paneldagi har qanday ataylab amalga oshirilgan o'zaro ta'sirlarni ularning kvitansiyalari bilan saqlang.
4. Raqamli jo'natuvchi IDlari, javob munosabatlari, takroriy manzillar va fayl hashlarini keltirilgan yozuvlar va shaxs profillari bo'ylab kuzating.
5. Case Board'da manba-bog'langan eslatmalar va to'plamlar qo'shing. Chatlararo kronologiyani vaqt belgilari va aniq bo'shliqlar bilan qayta tiklang.
6. Boshqa hisob ma'lumotlari ish maydonlarini ularning kelib chiqishi va kalitlarini alohida saqlagan holda solishtiring.
7. Imzolangan jurnal, profil va tarix eksportlarini ish yozuvlari bilan birga to'plang va tekshiring.

Veb-saytning `/docs/cases/` qo'llanmasida botlar bo'yicha nizolar, o'chirilgan xabarlar va ishtirokchilarning ismlarini o'zgartirishi uchun interaktiv ish holati xaritasi hamda variantlar mavjud. Case Board eslatmalar va kollektsiyalarni ish maydonida saqlaydi. Guruh eksportlari alohida ish maydoni paketlarini to'playdi; ish maydonlari o'rtasidagi korrelyatsiya va birlashtirilgan vaqt chizig'i tahlilchining vazifasi bo'lib qoladi.

[Yakunlangan tasdiqlash va qolgan ishlar](https://phishdestroy.github.io/TgWitness/uz/docs/reference/verification/) · [Eksport va tekshirish](https://phishdestroy.github.io/TgWitness/uz/docs/reference/evidence/#investigation-handoff) · [Bir akkaunt bilan boshlang](https://phishdestroy.github.io/TgWitness/uz/docs/reference/quickstart/)
