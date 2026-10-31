# Proxy tanlang

Canonical page: https://phishdestroy.github.io/TgWitness/uz/docs/proxies/

Hisobni ulangan holda saqlang. Qachon uning yo'li server manzilidan foydalanishi mumkinligini aniq belgilang.

## Avvalo IP rejimini tanlang

01**IPni yashirish**

Proxy-dan foydalaning. Hech biri ishlamasa, Telegramga bevosita ulanmasdan kuting.

02**Zaxira variantga ruxsat bering**

Sozlangan kechikishdan so'ng Direct ruxsat etilsin; javob berilganda ishchi proksiga qaytish.

03**Tunnel / VPN**

Mehmondo'st tarmog'i orqali to'g'ridan-to'g'ri yo'nalishlarni ruxsat eting. Ushbu opsiya VPNni o'rnatmaydi yoki tekshirmaydi.

Yo'l ulanishni tanlaydi. IP rejimi to'g'ridan-to'g'ri ulanishga ruxsat berilishini aniqlaydi.

## Let the pool maintain the route

1. **Hisobni** oching **→ Sozlamalar → Ulanish sozlamalari**.
2. IP rejimini va **avtomatik MTProxy-ni** tanlang yoki doimiy marshrutni kiriting.
3. **Telegram ulanishini sinovdan o'tkazishni** saqlang va ishga tushiring. Bu shuningdek tizimga kirishdan oldin ham ishlaydi.
4. Yig'ishni boshlagandan so'ng, nazorat ostidagi xabar jurnalga yetib kelganini tekshiring.

Yangi ish maydonchalari IP-ni yashirish xususiyatiga ega avtomatik MTProxy-dan foydalanadi. Pool to'rtta ommaviy manbani birlashtiradi, kirishlarni tekshiradi, ishchi yo'nalishlarni saqlab qoladi va ishlamay qolgan proksi-larni almashtiradi. Muvaffaqiyatsiz yuklab olishlar avvalgi snapshot-larni saqlab qoladi.

## O'zingizning proksingizdan foydalaning

SOCKS5 yoki HTTP CONNECT ma'lumotlarini kiriting, qo'llab-quvvatlanadigan Telegram proksi havolasini joylang yoki operator katalogini taqdim eting. Faol marshrutni o'zgartirishdan oldin kuzatuvni to'xtating. `ee` bilan boshlanadigan soxta TLS MTProxy sirlarini qo'llab-quvvatlamaydi.

**Aylantirish, ulashish va qayta urinish sozlamalari**

**Parametrlar → Avtomatik MTProxy** bo'limida xato chegaralarini, sovish muddatlarini, rejalashtirilgan aylantirishni va har bir proxy uchun hisoblarni sozlang. Ulashish chegarasi birga belgilanganida, eksklyuziv yozuv mavjud bo'lmaganda hisob kutishga majbur bo'ladi. Ro'yxatni yangilash va probe intervallari asosiy ish maydonining qiymatlariga amal qiladi. Alohida proxy'lar alohida chiqish IP manzillarini kafolatlamaydi.

## Telegramni tashqi so'rovlardan ajratish

MTProxy faqat Telegram trafigini o'tkazadi. Vaqt tamg'alari, bildirishnomalar, nusxalar va manba tekshiruvlari alohida SOCKS5/HTTP proksi, hisobning SOCKS5/HTTP yo'li yoki IP rejimi ruxsat etsa Direct orqali amalga oshiriladi. Ushbu tashqi so'rovlarni o'chirib qo'yish mumkin.

`TGWITNESS_PROXY_FEED_PROXY` aniq yo'lni sozlaydi. [Mustaqil guvoh](https://phishdestroy.github.io/TgWitness/uz/docs/witness/) o'z sozlamalarini saqlaydi. Ushbu boshqaruvlar tizim VPN-ni o'rnatmaydi va brauzer trafigini yo'naltirmaydi.

[Barcha rejimlar, standart sozlamalar va manba ro'yxatlarini](https://phishdestroy.github.io/TgWitness/uz/docs/reference/connection/#ip-modes) ko'ring yoki [hisob yo'nalishini kim o'zgartirishi mumkinligini tanlang](https://phishdestroy.github.io/TgWitness/uz/docs/access/).
