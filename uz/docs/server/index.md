# Uni ishlashda davom ettiring

Canonical page: https://phishdestroy.github.io/TgWitness/uz/docs/server/

Kollektorni ishlab turgan va ma'lumotlarni qayta ishga tushirishlarda xavfsiz saqlang.

## Boshlash usulini tanlang

Mahalliy: [ishga tushirgich](https://phishdestroy.github.io/TgWitness/uz/docs/start/) va [deploy/](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md) dagi xizmat shablonlari. Docker, loyiha papkasidan:

```
docker compose up -d --build --wait
docker compose exec tgwitness cat /data/panel-token.txt
```

Panel localhost:8787 da tinglaydi. Uni mahalliy yoki SSH tunneli orqali, ikkinchi buyruqdagi token bilan oching.

## Butun ma'lumotlar katalogini saqlang

Mahalliy: `data/live`. Docker: `tgwitness-data` hajmi. Jurnallar, sessiyalar va kalitlar birga bo'lishi kerak. Imzolangan eksport dalil, zaxira nusxa emas.

1. Avval yig'ishni to'xtating.
2. Butun ma'lumotlar katalogini xostdan tashqaridagi xavfsiz joyga nusxalang.
3. Ishonishdan oldin uni alohida o'rnatmada tiklab ko'ring.

## Qayta ishga tushirgandan so'ng tekshiring

Ish maydoni va kalit, ulanish, manbalar va yangi xabarlar kelayotganini tekshiring. TgWitness Telegram'da hali bor narsani to'ldiradi, o'chiq turgan paytda sodir bo'lgan hamma narsani emas.

"healthy" konteyner veb-server javob berayotganini bildiradi. Yig'ish ishlayaptimi, buni sinov xabari va guvoh aytadi.

## Faqat niyat qilgan narsangizni e'lon qiling

HTTPS, hajmlar, yangilanishlar va tiklash joylashtirish ma'lumotnomasida. Haqiqatan sinovdan o'tgan narsa: [tasdiqlash yozuvi](https://phishdestroy.github.io/TgWitness/uz/docs/reference/verification/).
