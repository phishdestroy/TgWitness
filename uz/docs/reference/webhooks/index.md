# Chiquvchi webhooks

Canonical page: https://phishdestroy.github.io/TgWitness/uz/docs/reference/webhooks/

HMAC imzolari, qayta urinishlar va yetkazib berish holati bilan HTTPS qabul qiluvchilarga doirali voqealarni yuboring.

[Ish jarayoni bo'yicha qo'llanma](https://phishdestroy.github.io/TgWitness/docs/archive/) · [Wiki](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

Tanlangan ish maydonida **Integratsiyalar → Chiquvchi webhooks** bo'limini oching. HTTPS qabul qiluvchini qo'shing, collector/media/export voqealarini tanlang va ixtiyoriy ravishda yangi kuzatuvlar va o'zgarishlar uchun suhbatlarni tanlang. Xabar matni standart bo'yicha o'chirilgan. Parchalarni yoqish xabar o'zgarishi voqealariga ko'pi bilan 1 000 belgini qo'shadi; xom Telegram maydonchalari va ma'lumotlar hech qachon yuborilmaydi.

HMAC sirini bir marta qabul qiluvchining himoyalangan sozlamalariga nusxalang. U TgWitness xazinasi ichida shifrlangan va paneldan tiklab bo'lmaydi. Maqsadni olib tashlab, uni aylantirish uchun qayta yarating. **Sintetik test** navbatlariga suhbat mazmuni bo'lmagan test **yuboring**; natijani ko'rish uchun yetkazib berish holatini yangilang.

Yetkazib berish Apprise bilan mavjud bildirishnoma tsiklini kengaytiradi. U ish maydonining tashqi yo'nalishi va mavjud xususiy manzil cheklovlaridan foydalanadi. Keyingi hech qanday to'g'ridan-to'g'ri zaxira rejasi yoki yo'naltirish mavjud emas. URL manzillarida autentifikatsiya ma'lumotlari, so'rov satrlari yoki fragmentlar bo'lmasligi kerak; xususiy manzillar uchun server darajasidagi tarmoqqa rozi bo'lish talab etiladi, bu panel foydalanuvchisi aylanib o'tolmaydigan sozlama emas.

## Yuk va imzo

Sxema: [`tgwitness.webhook/1`](https://github.com/phishdestroy/TgWitness/blob/main/integrations/webhook.schema.json). Har bir yuklama `event_id`, `timestamp`, `workspace`, `type`, `synthetic` va hisoblagichlarni o'z ichiga oladi. Jurnalga asoslangan voqealar ularning ketma-ketligi va xeshini o'z ichiga oladi. To'liq eksportning yakunlanishi va sintetik testlar yetkazib berish voqealari bo'lib, hech qanday ixtiro qilingan imzolangan jurnal havolasiga ega emas. Telegram o'chirish bildirishnomalari va `missing_on_recheck` alohida turlar bo'lib qoladi.

`X-TgWitness-Signature` sarlavhasi `t=UNIX_SECONDS,v1=HEX_HMAC_SHA256`. Ko'rsatilgan sirni UTF-8 baytlariga aylantirib, `timestamp + "." + raw_request_body` aniq baytlari bo'yicha HMAC hisoblang. Imzolarni tana qismini tahlil qilish yoki unga ishlov berishdan oldin doimiy vaqt ichida solishtiring. O'z soatingizdan besh daqiqadan ortiq bo'lgan vaqt tamg'alarini rad eting. Vaqt tamg'asi har bir yetkazib berish urinishida yangilanadi.

`event_id`ni idempotentlik kaliti sifatida bardoshli saqlashda, yon ta'sirlarga kirishdan oldin atomik noyob cheklov bilan ishlating. Faqat haqiqiy imzo yaqinda yuborilgan so'rovning qayta ijro etilishini oldini olmaydi. Ishlangan identifikatorlarni kamida butun qayta urinish oynasi davomida saqlang; agar qabul qiluvchi saqlangan voqealarni qayta ishlay oladigan bo'lsa, ularni uzoqroq saqlang.

## Qayta urinishlar

Yetkazib berishlar HTTP so'rovlaridan oldin barqaror navbatga qo'yiladi. Ular kamida bir marta yetkazish semantikasidan foydalanadi: yo'qolgan tasdiq yoki qayta boshlash voqeani bir xil ID bilan yana yetkazishi mumkin. Eksponensial kechiktirish bilan 15 soniyadan boshlab va bir soat bilan cheklangan sakkizta urinish mavjud. Muvaffaqiyat uchun 2xx javob talab etiladi. Yakunlangan ishlar ko'rinadigan xato qoldiradi; qayta urinishlar tugagach yetkazib berish kafolatlanmaydi.

Navbatda 1 000 ta yetkazib berish bo'ladi. To'lganida jurnal voqealarini skanerlash to'xtaydi va bo'sh joy paydo bo'lgach davom ettiriladi. Navbatga qo'yib bo'lmaydigan to'liq eksport yakunlanishi ko'rinadigan navbat xatosini yuzaga keltiradi. Har bir bildirishnoma o'tishida beshtagacha yetkazib berish urinishlari amalga oshiriladi va so'nggi 100 urinish yozuvlari saqlanadi. Manzilni olib tashlash uning kutayotgan yetkazib berishlarini ham olib tashlaydi.

## n8n misoli

[Namuna ish jarayonini](https://github.com/phishdestroy/TgWitness/blob/main/integrations/n8n-tgwitness.json) import qiling. U faol emas va hech qanday sirlar yoki keyingi harakatlarga ega emas. `TGWITNESS_WEBHOOK_SECRET`ni n8n ishchi muhitiga o'rnating, ushbu muhitga kirishni ruxsat bering va Code tuguni uchun `crypto` built-in funksiyasini yoqing. Misol Webhook tugunining raw-body opsiyasidan foydalanadi, imzo/yangiligi tekshiriladi va tasdiqlangan voqealarni tasdiqlaydi. Bu tugunning [hujjatlashtirilgan amalga oshirilish](https://github.com/n8n-io/n8n/blob/master/packages/nodes-base/nodes/Webhook/Webhook.node.ts)iga mos keladi.

SIEM yozuvlari yoki bildirishnomalarni qo'shishdan oldin, `event_id` bo'yicha kalitlangan barqaror idempotent saqlashni qo'shing. Tanlagan yuborish ma'lumotlariga muvofiq n8n ish jarayonini tahrirlash va ijro-log saqlash muddatini cheklang. TgWitness hech qanday kirish buyruqlarini qo'shmaydi.
