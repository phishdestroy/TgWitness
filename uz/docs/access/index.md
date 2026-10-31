# Bir ishni baham ko'ring

Canonical page: https://phishdestroy.github.io/TgWitness/uz/docs/access/

Kimga kerak bo'lsa, shu holatni ulashing. Qolganlarini nazorat ostida saqlang.

01**Dalilni tanlang**

Butun hisob ish maydonlarini yoki alohida yozib olingan suhbatlarni tanlang.

02**Harakatlarni tanlang**

Kuzatish, eksport qilish yoki shaxsga kerak bo'lgan maxsus operativ ruxsatlarni berish.

03**Chegaralarni belgilang**

Muddatli shaxsiy token chiqaring, sessiya chegaralari va ixtiyoriy IP-cheklovlar bilan.

Yig'ish doirasi nimalar qayd etilishini belgilaydi. Kirish doirasi esa shaxs nimalarni ko'rishi va bajarishi mumkinligini belgilaydi.

## Kimgadir kirish huquqini bering

1. Administrator sifatida tizimga kiring va **kirishni** yoqing.
2. Kirishni nomlang va ish maydonlari hamda suhbatlarni tanlang.
3. Ko'rib chiquvchi uchun **Ko'rishni** saqlang. Agar ular yozuvlarni yuklab olishni xohlasa, **Eksportni** qo'shing.
4. Chegaralarni belgilang, so'ngra **Kirishni yaratish tugmasini** bosing.
5. Ko'rsatilgan tokenni bir marta nusxalang. Uni panel manzili bilan shaxsiy ravishda yuboring.
6. Uni topshirishdan oldin alohida brauzer sessiyasida ruxsat etilgan ko'rinishni tekshiring.

## Ular bajarishi kerak bo'lgan ishdan boshlang

| Shaxs | Kirish | Natija |
| --- | --- | --- |
| Ko'rib chiquvchi | Tanlangan suhbatlar; faqat ko'rish | Yozib olingan suhbatni yig'ish tartibini o'zgartirmay o'qing. |
| Tahlilchi | Tanlangan suhbatlar; ko'rish va eksport qilish | Ish uchun zarur yozuvlarni ko'rib chiqing va yuklab oling. |
| Operator | Tanlangan butun ish maydonchalari; manbalar va to'plam | Kuzatilganlarni boshqaring va kollektorlarni ishga tushiring yoki to'xtating. |

Bu siz tanlaydigan konfiguratsiyalar bo'lib, doimiy rollar emas. Hisob bo'ylab sozlamalar va to'liq jurnal eksportlari, hatto boshqa ruxsat berilgan bo'lsa ham, suhbat darajasidagi cheklangan kirish bilan yopiq bo'lib qoladi. Butun ish maydoni bo'ylab kirish kelajakdagi hisoblarni ham o'z ichiga oladi.

## Ixtiyoringizni istalgan vaqtda o'zgartirishingiz mumkin

Keyingi so'rovlar nima qilishi mumkinligini o'zgartirish uchun kirishni tahrirlang. Bir sessiyani tugating yoki barcha sessiyalarni tugatish uchun butun kirishni bekor qiling. Allaqachon yuklab olingan fayllarni qaytarib bo'lmaydi. Panel sessiyasini tugatish ma'lumotlarni yig'ishni to'xtatmaydi.

**Sessiya va IP cheklovlari**

Parallel sessiyalar va muvaffaqiyatli tizimga kirishlarni cheklang, mutlaq yakun sanasini belgilang, IP-manzillar yoki submanzillarni ruxsat eting yoki kirishni birinchi tizimga kirish manzili bilan bog'lang. Sessiyaning tugash muddati faoliyatsizlikni aniqlaydi; ochiq panelning so'rovlari faoliyat sifatida hisoblanadi. Proksi yoki tunnel ortida ishlaganda ilova ko'rsatadigan klient manzilini tekshiring.

**Asosiy kalit va faoliyat joriy yozuvlari**

Administrator asosiy panel tokenini saqlaydi. Berilgan ruxsat boshqalarning kirish huquqlarini boshqarishga yoki administrator konsolini ochishga imkon bermaydi. Konsol ish maydonlari bo'ylab joriy jarayon faoliyatini ko'rsatadi; imzolangan kirish yozuvlari tokenlarsiz ruxsat berish va sessiya voqealarini saqlab qoladi. Ish maydonlari host jarayonini baham ko'radi va server administratoridan ma'lumotlarni ajratmaydi.

Barcha yetti ruxsat, sessiya qoidalari va administrator chegarasi uchun [to'liq ruxsat havolas](https://phishdestroy.github.io/TgWitness/uz/docs/reference/access/)idan foydalaning.
