# Hisobotni loyihalash

Canonical page: https://phishdestroy.github.io/TgWitness/uz/docs/reports/

O'quvchiga ish savolidan saqlangan yozuvlargacha aniq yo'lni ko'rsating.

Report studio ma'lumot tanlovini, o'zgarishlarning o'qiladigan tarixini, grafikalarni va yozma topilmalaringizni birlashtiradi. Sakkizta integratsiyalashgan dizayn qo'llab-quvvatlanadigan HTML va mahalliy PDF chiqishlariga tatbiq etiladi. HTML, PDF va JSON hisobotlari o'z imzolangan muhrlariga ega; ZIP manifesti ham paketdagi fayllarni bog'laydi. HTML va PDF oxirgi maketlash tugagach muhrlanadi.

## Uch bosqichda hisobot tuzing

1. **Exportlarni** oching **→ Sozlash va ko'rinishni oldindan ko'rish → Ma'lumotlar**. Butun ish maydonini yoki suhbatlar, mualliflar, UTC kuzatuv sanalari va yozuv turlarini tanlang. Sana TgWitness yozuvni qachon kuzatganini ko'rsatadi.
2. **Design & contents** bo'limida dizayn va kontent uchun oldindan belgilangan sozlamalarni tanlang. Faoliyat diagrammalari, ishtirokchi yorliqlari, transkript, saqlangan o'zgarishlar va ixtiyoriy Case Board materiallarini tanlang. Ish tafsilotlari va tekshiruv eslatmalarini qo'shing.
3. Hisoblar, faoliyat, ishtirokchilar, namunaviy yozuvlar va yetishmayotgan ID diapazonlarini ko'rib chiqish uchun Open **Preview-ni** oching. Sozlamalarni saqlang, so'ng kerakli formatni yuklab oling.

### O'xshash saqlangan materialni o'quvchi uchun tartibga soling

Sun'iy misol · sxematik tuzilma, generatsiya qilingan hisobot emas

1. **Tanlang.** Ish uchun ikkita suhbat va kuzatuv davrini tanlang.
2. **Yozish.** Tuzilmani va savolga javob beradigan bo'limlarni tanlang.
3. **Oldindan ko'rish.** Tanlangan sonlarni va saqlangan oldingi hamda keyingi matnni ko'rib chiqing.
4. **Tekshirish.** Yakuniy faylni hosil qiling va uning imzosini ishonchli ish maydoni barmoq izi bilan solishtiring.

#### Tanlangan kuzatuvlar

2 ta suhbat · 1 ta kuzatuv kuni

Xabarlar, tahrirlar va o'chirish bildirishnomalari

#### Hisobot tuzilmasi

##### To'lov manzili o'zgartirildi

Holat savoli → doira → natijalar → yozuvga havolalar

**Xabar konteksti**

Kuzatuv #142: "Yangi to'lov havolasidan foydalaning."

**Saqlangan o'zgarishlar**

Avval: old.example.invalid → Keyin: new.example.invalid

#### Tanlovni ko'rib chiqing

18 ta kuzatuv · 2 ta saqlangan tahrir

Yuborilgan, tahrirlangan va kuzatilgan vaqtlar alohida yorliqlarga ega.

#### Yakuniy topshiriladigan hujjat

Imzolangan PDF + imzolangan JSON, yoki o'qiladigan hisobotga ega imzolangan ZIP

Qabul qiluvchi fayl va ishonchli barmoq izini tekshiradi.

## O'qish uslubini tanlang

**Classic, Editorial, Briefing, Analytics, Technical, Overview, Reading series va Ledger & margin** turli kompozitsiyalarda bir xil asosiy yozuvlarni taqdim etadi. Dizaynni o'zgartirish ma'lumotlar tanlovini va yozma izohlarni saqlaydi. Hisobot tilini 25 ta qo'llab-quvvatlanadigan til ichidan tanlash mumkin.

Reading series bo'lim paneli atrofida ish holati, doirasi, natijalar va o'zgarishlarni guruhlaydi. Ledger & margin raqamlangan boblar va keng marjadan foydalanadi. Ikkalasi ham hisob HTML ko'rinishlari va nusxalarni ulashishni qo'llab-quvvatlaydi. Mahalliy PDF-lar biriktirilgan shriftlar bilan yaratiladi; foydalanuvchi kompyuterida PDF yaratish uchun brauzer yoki Node o'rnatilishi shart emas. Xitoycha, yaponcha va koreyscha PDF-lar uchun serverda, masalan, tizim bo'ylab o'rnatilgan yoki `TGWITNESS_FONT_DIR` papkasiga joylashtirilgan Noto Sans CJK kabi mos shrift bo'lishi kerak. Aks holda ZIP faqat HTML va JSON hisobotlarini saqlaydi.

## O'zgarishni uning konteksti bilan o'qing

Saqlangan tahrirlar oldingi va keyingi holatni ko'rsatadi. O'chirish bildirishnomasi oxirgi olingan versiya bilan birga bo'lishi mumkin. Javoblar, iqtiboslar, yo'llanmalar, munosabatlar, tugmalar va ilovalar metama'lumotlari mavjud bo'lgan havolalarni saqlaydi. Faylning SHA-256 va jurnal yozuvi hashlariga alohida yorliq qo'yiladi.

Dizayn ko'rinishi birinchi 50 000 manba yozuvlari orasidan mos keladigan yozuvlarni ishlatib muqova, tekshiruv va diagramma komponentlarini ko'rsatadi. Alohida ma'lumotlar ko'rinishi to'liq barqaror jurnal snapshotini aniq tanlov sonlari bo'yicha skanerlaydi, namuna chegaralari yorliq bilan ko'rsatiladi. Yakuniy sahifalashni tekshirish uchun PDF yarating. Toʻliq hisobot eksporti HTML koʻrinishga ega; uning alohida chat PDF-fayllari tanlangan dizayndan foydalanadi.

## Qabul qiluvchining nusxasini ongli ravishda tanlang

Hisobot filtrlari o'qiladigan hisobotni shakllantiradi. To'liq dalillar ZIP-fayli asl jurnal va ilovalarni saqlab qoladi. Qabul qiluvchi faqat tanlangan ma'lumotlarni olishi kerak bo'lsa, [minimal handover-](https://phishdestroy.github.io/TgWitness/uz/docs/handover/)dan foydalaning. [Hisobot mazmuni va tekshiruvni](https://phishdestroy.github.io/TgWitness/uz/docs/reference/case-reports/) ko'ring yoki [tayyor eksportni tasdiqlang](https://phishdestroy.github.io/TgWitness/uz/docs/exports/).
