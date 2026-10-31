# Uni ishlashda davom ettiring

Canonical page: https://phishdestroy.github.io/TgWitness/uz/docs/server/

Yig'gichni doimiy ravishda ishlashga tayyor holda saqlang va qayta ishga tushirishlar davomida uning ma'lumotlari saqlansin.

## Boshlash usulini tanlang

Mahalliy o'rnatish uchun [deploy](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md)/dagi [ishga tushiruvchi](https://phishdestroy.github.io/TgWitness/uz/docs/start/) fayl va xizmat misollaridan foydalaning. Docker uchun Compose yordamida Docker-ni o'rnating va loyiha katalogidan ishga tushiring:

```
docker compose up -d --build --wait
docker compose exec tgwitness cat /data/panel-token.txt
```

O'rnatilgan panel mezbonning loopback manzili, 8787-port orqali tinglaydi. Uni mahalliy tarmoqda yoki SSH tunneli orqali oching. Panelni ochish uchun ikkinchi buyruqdagi tokenni ishlating.

## Butun ma'lumotlar katalogini saqlang

Mahalliy o'rnatishlar `data/live` dan foydalanadi. Docker esa doimiy `tgwitness-data` hajmdan foydalanadi. Jurnalni, hisob sessiyalarini, kalitlarni va operatsion holatni birga saqlaydi. Imzolangan eksport foydali dalildir, lekin bu to'liq o'rnatish zaxira nusxasi emas.

1. Muntazam zaxira nusxasini olishdan oldin yig'ishni to'xtating.
2. To'liq shaxsiy ma'lumotlar katalogini mezbonning tashqarisidagi himoyalangan saqlash joyiga nusxalang.
3. Zaxira nusxaga tayanishdan oldin uni izolyatsiyalangan o'rnatishga sinov tiklash.

## Qayta ishga tushirgandan so'ng tekshiring

Kutilayotgan ish maydoni va kalitni, Telegram ulanishini, tanlangan manbalarni va yangi xabarni qayd etishni tasdiqlang. Saqlangan MTProto holati va orqada qolgan yangilanishlarni tiklash yordami Telegram hali saqlab turgan yangilanishlarni qaytarib olishga yordam beradi. Ular muddati tugagan har bir yangilanishni yoki qayd etishdan oldin o'chirib tashlangan tahrirni qayta tiklay olmaydi.

Kontener holati veb-server javob berishini anglatadi. Yig'ish va tashqi e'lon qilishni baholash uchun nazoratli xabar va guvoh tekshiruvidan foydalaning.

## Faqat niyat qilgan narsangizni e'lon qiling

Joylashtirish bo'yicha qo'llanmada HTTPS misollari, doimiy hajmli buyruqlar, yangilash va tiklash bosqichlari keltirilgan. Joylashtirish uchun Docker buyruqlari taqdim etilgan; joriy [tasdiqlash yozuvi](https://phishdestroy.github.io/TgWitness/uz/docs/reference/verification/) haqiqatan sinovdan o'tkazilgan muhitlarni aniqlaydi.
