# Telegram · Bir ishni baham ko'ring

Canonical page: https://phishdestroy.github.io/TgWitness/uz/docs/access/

Kimga kerak bo'lsa, shu holatni ulashing. Qolganlarini nazorat ostida saqlang.

01**Dalilni tanlang**

Butun ish maydonlari yoki alohida chatlar.

02**Harakatlarni tanlang**

Ko'rish, eksport yoki faqat ularga kerakli amallar.

03**Chegaralarni belgilang**

Xohlasangiz amal qilish muddati, sessiya cheklovlari va IP qoidalari bilan shaxsiy token.

Yig'ish doirasi nimalar qayd etilishini belgilaydi. Kirish doirasi esa shaxs nimalarni ko'rishi va bajarishi mumkinligini belgilaydi.

## Kimgadir kirish huquqini bering

1. Administrator sifatida **Kirish**ni oching.
2. Nom bering, ish maydonlari va chatlarni tanlang.
3. Ko'rib chiquvchiga faqat **Ko'rish** kerak. Yuklab olish uchun **Eksport** qo'shing.
4. Chegaralarni belgilang, so'ngra **Kirishni yaratish tugmasini** bosing.
5. Tokenni nusxalang (bir marta ko'rsatiladi) va panel manzili bilan maxfiy yuboring.
6. Avval alohida brauzer sessiyasida ular nimani ko'rishini tekshiring.

## Ular bajarishi kerak bo'lgan ishdan boshlang

| Shaxs | Kirish | Natija |
| --- | --- | --- |
| Ko'rib chiquvchi | Tanlangan suhbatlar; faqat ko'rish | Chatni o'qiydi, hech narsani o'zgartira olmaydi. |
| Tahlilchi | Tanlangan suhbatlar; ko'rish va eksport qilish | Ishga keraklisini o'qiydi va yuklab oladi. |
| Operator | Tanlangan butun ish maydonchalari; manbalar va to'plam | Nima kuzatilishini hal qiladi, kollektorlarni ishga tushiradi va to'xtatadi. |

Bular shunchaki misollar, qat'iy rollar emas. Chat bilan cheklangan kirish hech qachon hisob sozlamalari yoki to'liq jurnal eksportini olmaydi. Barcha ish maydonlariga kirish keyin qo'shilgan hisoblarni ham o'z ichiga oladi.

## Ixtiyoringizni istalgan vaqtda o'zgartirishingiz mumkin

Kirishni istalgan vaqtda tahrirlang, u keyingi so'rovdan kuchga kiradi. Bitta sessiyani tugating yoki hammasini bekor qiling. Yuklab olingan fayllarni qaytarib bo'lmaydi. Yig'ish davom etadi.

**Sessiya va IP cheklovlari**

Parallel sessiyalar va kirishlarni cheklang, tugash sanasini belgilang, IP yoki subnetlarga ruxsat bering yoki birinchi kirish IP'siga bog'lang. Amal qilish muddati nofaollikdan hisoblanadi, ochiq panel faol hisoblanadi. Proksi ortida ilova qaysi mijoz IP'sini ko'rishini tekshiring.

**Asosiy kalit va faoliyat joriy yozuvlari**

Asosiy token administratorda qoladi. Berilgan kirish boshqalarning kirishini boshqara olmaydi yoki administrator konsolini ocha olmaydi. Kirish o'zgarishlari va sessiyalar tokensiz jurnalga imzolanadi. Server administratori baribir hamma narsani ko'ra oladi.

Yettala ruxsat va sessiya qoidalari: [kirish ma'lumotnomasi](https://phishdestroy.github.io/TgWitness/uz/docs/reference/access/).
