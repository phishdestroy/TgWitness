# Telegram · Manba tarixini yuklash

Canonical page: https://phishdestroy.github.io/TgWitness/uz/docs/reference/history/

Yoqilgan manbalardan avvalgi xabarlarni yuklang, to'xtating va davom ettiring, shuningdek imzolangan progress hisobotini tasdiqlang.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Hujjatlash](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Yig'ma](https://github.com/phishdestroy/TgWitness/blob/main/docs/COLLECTION-MODES.md)

![Yig'ma](https://phishdestroy.github.io/TgWitness/assets/chapter-collect.svg)

**Manbalar** bo'limida yoqilgan suhbatlarni ko'rib chiqing, kuzatuvni to'xtating, Standart API yoki Takeout eksportini tanlang, so'ngra **To'liq tarixni yuklashni** tanlang. Jarayon manbalar ro'yxatini mustahkamlaydi va ularning mavjud bo'lgan avvalgi xabarlarini Suhbatlarga hamda imzolangan kuzatuv jurnaliga o'qiydi. Media mavjud ilova sozlamalari va uzoq muddatli yuklab olish navbatidan foydalanadi. Bu har bir suhbat bo'yicha imzolangan JSON/HTML eksportidan alohida.

Hisob bo'ylab to'plash uchun **Butun hisob**ni tanlang, manba ro'yxatini yuklash uchun kuzatuvni boshlashingiz va tarixni boshlashdan oldin ushbu ro'yxatni ko'rib chiqishingiz kerak. Dialog-ro'yxat chegarasi hanuz amalda (o'rnatilgan holda 1,000, Parametrlarda sozlanishi mumkin). Muvaffaqiyatli ish har bir hisob dialogi ro'yxatga olinganini isbotlamaydi. Keyinchalik topilgan yoki yoqilgan suhbatlar uchun yana bir marta ishga tushirish zarur. Tarixni boshlashdan oldin kuzatuvni to'xtating; bir vaqtning o'zida faqat bitta hisob ma'lumotlari olinadi.

Birdan besh tagacha ilova ishchilarini tanlang va mavjud So'nggi Harakatlarni saqlab qolish hamda avval saqlangan versiyalarni solishtirishni tanlang. Chiqarish Telegramda tasdiqni va server tomonidan belgilangan kutishni talab qilishi mumkin. Ushbu parametrlar qayta boshlaganda ham o'zgarmas qoladi. Transport, qayta urinish va ishonch tafsilotlari uchun [Backfill xatti-harakatlari va dalillar shartnomasiga](https://github.com/phishdestroy/TgWitness/blob/main/docs/BACKFILL.md) qarang.

## Tanaffus, qayta boshlash va qisman natijalar

- **Tanaffus tarixi** o'qishni to'xtatadi. **Davom ettirish** har bir manbada oxirgi yozilgan xabardan boshlanadi; ilovani qayta ishga tushirish ham ishni to'xtatilgan holatda qoldiradi. Davom ettirish uchun bir xil faol Telegram akkaunti talab etiladi.
- Xabarni kuzatish, ilova ishini bajarish va kursorni commit qilish bitta tranzaktsiyada amalga oshiriladi. Qayta boshlangan ijro allaqachon commit qilingan kuzatuvlarni takrorlamaydi. Jonli yozib olish yoki alohida, aniq boshlangan ijro mustaqil ravishda bir xil xabarni kuzatishi mumkin.
- Har bir manba (Takeout'dagi har bir Telegram bo'lingan diapazon) birinchi o'qishda yuqori xabar ID'ini belgilaydi. Yangi xabarlar jonli kuzatuvga tegishli, manbaning qolgan tarixiy sahifalariga emas.
- Kirib bo'lmaydigan manbalar va olish jarayonida o'chirib qo'yilgan manbalar muvaffaqiyatsiz yoki o'tkazib yuborilgan holda ko'rinadi. Boshqa manbalar davom etadi; umumiy natija to'liq emas.
- FloodWait kechikishlari saqlangan hisobning kutish oralig'iga rioya qiladi. Vaqtinchalik xatoliklar besh martagacha qayta urinadi; resurslar tugashi va disk joyining kamayishi kursorni saqlagan holda to'xtaydi.
- **Bu history run tugagach** saqlangan kuzatuvlar saqlanib qoladi. U ularni o'chirib tashlamaydi yoki standart API ilovalarini bekor qilmaydi. Takeout tugagach, qolgan Takeout fayllarini o'tkazib yuborilgan deb belgilaydi; to'xtatish esa ularni qayta boshlash imkonini saqlaydi. Yangi ish yoqilgan manbalarni qayta o'qiydi.

Tarixni to'ldirish faqat o'qish rejimida tarixni ko'rsatadi. Ilovalar kutib turishi, muvaffaqiyatsiz bo'lishi yoki sozlangan siyosat tomonidan istisno qilinishi mumkin. Jurnal va ilovalar navbatidagi media kvitansiyalarini tekshiring; saqlangan ilova faqat saqlangan baytlarga ega bo'lgan yakuniy kvitansiya hisoblanadi. Tarix operatsiyasi aniq snapshot so'rovi bo'lib, kelajakdagi jonli voqealar toifalarini tanlaydigan kalitlardan alohida.

## Ko'chirish va tekshirish

**Imzolangan ijro hisobot**ini saqlang, so'ng **dalillarni eksport qilish** funksiyasidan foydalanib jurnal va saqlangan ilovalarni yuklab oling. Keyingi dalillar eksporti qo'shimcha yozuvlarni o'z ichiga olishi mumkin; hisobot o'z hisoblagichlarini yaratilgan paytdagi jurnal prefiksiga bog'laydi. Verifikatorni ushbu versiyaning ishonchli chiqishidan ishga tushiring:

```
python tgwitness/verify.py tgwitness-history-report.json --evidence evidence.zip --fingerprint TRUSTED_FINGERPRINT
```

Kutilayotgan imzolash kaliti barmoq izini alohida saqlang. Verifikator hisobot imzosi, dalillar arxivi, hisobot tekshiruv nuqtasi, manba rejasini, hisobni va saqlangan/mavjud bo'lmagan xabarlar sonini tekshiradi. Yangi ishlar manba rivoji va parametrlarni imzolangan kursor voqealariga bog'laydi. `--evidence`siz u faqat imzolangan hisobot va uning ichki izchilligini tekshiradi. Eski rivoj maydonchalari va ilova xulosalari imzolangan yig'uvchi bayonotlari bo'lib qoladi. Dalillar verifikatori arxivlangan media baytlarini tekshiradi.

Imzolash ham, mavjud tarixni yakunlash ham Telegramning kelib chiqishini, atomik snapshotini yoki tarixiy to'liqligini isbotlamaydi. Xabarlar o'qish jarayonida o'zgartirilishi mumkin; o'chirilgan xabarlar va mavjud Yaqin Harakatlar va Sirli Suhbatlar doirasidan tashqaridagi oraliq tahrirlar qayta tiklanmaydi. Imzolash kalitini boshqaruvchi operator tashqi majburiyatlar mavjud bo'lishidan oldin jurnalni soxtalashtirishi mumkin. Hujjatlashtirilgan aralashuvni aniqlash xususiyatlari uchun alohida saqlangan tekshiruv nuqtalaridan yoki mustaqil guvohdan foydalaning.

Yozib olish kursori mahalliy ish maydonining holatini bildiradi. Faqat dalillar ZIP-faylini tiklash kutib turgan yozib olish ishini yoki Telegram sessiyasini tiklamaydi. Agar asl ishni davom ettirish zarur bo'lsa, ish maydonining zaxira nusxasini saqlang.
