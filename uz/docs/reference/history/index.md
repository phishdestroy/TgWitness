# Manba tarixini yuklash

Canonical page: https://phishdestroy.github.io/TgWitness/uz/docs/reference/history/

Yoqilgan manbalardan avvalgi xabarlarni yuklang, to'xtating va davom ettiring, shuningdek imzolangan progress hisobotini tasdiqlang.

**Hozirgi asosiy:** manbadan olinadi; 0.7.0 portativ ko'rinishiga kiritilmagan.

**Manbalar** bo'limida yoqilgan suhbatlarni ko'rib chiqing, kuzatuvni boshlang, so'ngra **"To'liq tarixni yuklash"ni** tanlang. Ushbu jarayon manbalar ro'yxatini tuzatadi va ularning mavjud avvalgi xabarlarini Suhbatlarga hamda imzolangan kuzatuv jurnaliga yuklaydi. Media mavjud ilova sozlamalari va barqaror yuklab olish navbatidan foydalanadi. Bu har bir suhbat bo'yicha imzolangan JSON/HTML eksportidan alohida.

Hisob bo'yicha to'liq yig'ish uchun "**Butun hisob**"ni tanlang, manba ro'yxatini yuklash uchun kuzatuvni boshlashingiz va tarixni boshlashdan oldin ushbu ro'yxatni ko'rib chiqishingiz kerak. Dialog-ro'yxat chegarasi hanuz amalda (o'rnatilgan bo'yicha 1 000, Parametrlarda sozlanishi mumkin). Muvaffaqiyatli ish har bir hisob-dialog ro'yxatga olingani dalil emas. Keyinchalik topilgan yoki yoqilgan suhbatlar uchun yana bir marta ishga tushirish kerak bo'ladi.

## Tanaffus, qayta boshlash va qisman natijalar

- **Tarixni to'xtatish** o'qishni to'xtatadi. **Tarixni davom ettirish** har bir manbadagi oxirgi yozilgan xabardan boshlanadi; ilovani qayta ishga tushirish ham uni qayta boshlanmaguncha to'xtatilgan holda qoldiradi. Avvalo kuzatuvni qayta ishga tushiring. Davom ettirish uchun bir xil Telegram hisob qaydnomasi talab etiladi.
- Xabarni kuzatish, ilova ishini bajarish va kursorni commit qilish bitta tranzaktsiyada amalga oshiriladi. Qayta boshlangan ijro allaqachon commit qilingan kuzatuvlarni takrorlamaydi. Jonli yozib olish yoki alohida, aniq boshlangan ijro mustaqil ravishda bir xil xabarni kuzatishi mumkin.
- Har bir manba birinchi o'qishida yuqori xabar IDni belgilaydi. Yangi xabarlar jonli kuzatuvga tegishli, manbaning qolgan tarixiy sahifalariga emas.
- Kirib bo'lmaydigan manbalar va olish jarayonida o'chirib qo'yilgan manbalar muvaffaqiyatsiz yoki o'tkazib yuborilgan holda ko'rinadi. Boshqa manbalar davom etadi; umumiy natija to'liq emas.
- FloodWait kechikishlari saqlangan hisobning oraliq vaqtlariga rioya qiladi. Transport vaqt chegaralarining tugashi va disk joyining kamayishi ishni kursor saqlangan holda to'xtatadi. Sababini bartaraf etgach, ishni davom ettiradi.
- **Ushbu history run tugagach**, saqlangan kuzatuvlar saqlanib qoladi. U ularni o'chirib tashlamaydi yoki oldin navbatga qo'yilgan ilova yuklamalarini bekor qilmaydi. Yangi ish yoqilgan manbalarni qayta o'qiydi.

Tarixni to'ldirish faqat o'qish rejimida tarixni ko'rsatadi. Ilovalar kutib turishi, muvaffaqiyatsiz bo'lishi yoki sozlangan siyosat tomonidan istisno qilinishi mumkin. Jurnal va ilovalar navbatidagi media kvitansiyalarini tekshiring; saqlangan ilova faqat saqlangan baytlarga ega bo'lgan yakuniy kvitansiya hisoblanadi. Tarix operatsiyasi aniq snapshot so'rovi bo'lib, kelajakdagi jonli voqealar toifalarini tanlaydigan kalitlardan alohida.

## Ko'chirish va tekshirish

**Imzolangan ijro hisobot**ini saqlang, so'ng **dalillarni eksport qilish** funksiyasidan foydalanib jurnal va saqlangan ilovalarni yuklab oling. Keyingi dalillar eksporti qo'shimcha yozuvlarni o'z ichiga olishi mumkin; hisobot o'z hisoblagichlarini yaratilgan paytdagi jurnal prefiksiga bog'laydi. Verifikatorni ushbu versiyaning ishonchli chiqishidan ishga tushiring:

```
python tgwitness/verify.py tgwitness-history-report.json --evidence evidence.zip --fingerprint TRUSTED_FINGERPRINT
```

Kutilayotgan imzolash kaliti barmoq izini mustaqil ravishda saqlang. Tekshiruvchi hisobot imzosi, dalillar arxivi, hisobot tekshirish nuqtasi, manba rejasini, hisobni va saqlangan/mavjud bo'lmagan xabarlar sonini tekshiradi.`--evidence`siz u faqat imzolangan hisobot va uning ichki izchilligini tekshiradi. Rivojlanish bosqichlari, sarlavhalar, kursorlar va ilovalar xulosalari — bu hisobot tekshiruvchisi tomonidan mustaqil ravishda qayta tiklanmagan, balki yig'uvchi imzolangan bayonotlari hisoblanadi. Dalillarni tasdiqlovchi baribir arxivlangan media baytlarini tekshiradi.

Imzolash yoki mavjud tarixni yakunlash Telegram kelib chiqishini, atomik snapshotni yoki tarixiy to'liqlikni isbotlamaydi. Xabarlar o'qish paytida o'zgartirilishi mumkin; o'chirilgan xabarlar, ko'rilmagan oraliq tahrirlar va Sirli Suhbatlar tiklanmaydi. Imzolash kalitini boshqaruvchi operator tashqi majburiyatlar mavjud bo'lmasdan oldin jurnalni soxtalashtirishi mumkin. Hujjatlashtirilgan manipulyatsiyani aniqlash xususiyatlari uchun alohida saqlangan tekshiruv nuqtalaridan yoki mustaqil guvohdan foydalaning.

Yozib olish kursori mahalliy ish maydonining holatini bildiradi. Faqat dalillar ZIP-faylini tiklash kutib turgan yozib olish ishini yoki Telegram sessiyasini tiklamaydi. Agar asl ishni davom ettirish zarur bo'lsa, ish maydonining zaxira nusxasini saqlang.
