# Faqat o'qish uchun MCP

Canonical page: https://phishdestroy.github.io/TgWitness/uz/docs/reference/mcp/

MCP mijozini tanlangan ish maydonlari va suhbatlarga muddati tugaydigan, bekor qilinishi mumkin bo'lgan kirish huquqi bilan ulashing.

**Hozirgi asosiy:** manbani chiqarib olishdan foydalaning; 0.7.0 portativ ko'rinishi ushbu xususiyatdan oldin yaratilgan.

[Ish jarayoni bo'yicha qo'llanma](https://phishdestroy.github.io/TgWitness/docs/archive/) · [Wiki](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

TgWitness loyihasi katalogidan ixtiyoriy serverni o'rnating:

```
python -m pip install '.[mcp]'
```

Panelda **Integratsiyalar → MCP** bo'limini oching. Ulanish nomini kiriting, uning ish maydonchalari va suhbatlarini tanlang va amal qilish muddatini belgilang. Arxiv tokenini bir marta nusxalang; uni keyin qayta tiklab bo'lmaydi. Yo'qolgan tokenlarni bekor qiling va ularni yangilari bilan almashtiring. Panel tokenlari va Telegram kirish ma'lumotlari MCP kirish ma'lumotlari hisoblanmaydi.

## Klientni ulanish

Panel o'zining [hujjatlangan konfiguratsiyasidan](https://code.visualstudio.com/docs/agents/reference/mcp-configuration) foydalangan holda **VS Code Local harness** uchun`.vscode/mcp.json` ni yaratadi. Yuklab olingan faylni shu joyga saqlang, **MCP: List Servers ni** ishga tushiring va TgWitness ni ishga tushiring. VS Code parol kirish oynasi orqali tokenni so'raydi. Yuklab olingan JSON token emas, balki so'rov havolasini o'z ichiga oladi. MCP extra o'rnatilgan muhitdan Python ijro etiladigan faylni ishlating.

Boshqa stdio mijozlari uchun quyidagilarni bajaring:

```
python -m tgwitness.mcp_server --api-url http://127.0.0.1:8787
```

`TGWITNESS_ARCHIVE_TOKEN` ni mijozning himoyalangan muhitida o'rnating. Uni buyruq argumentlariga yoki URL manzillariga kiritmang. Ko'prik panelning ruxsat berilgan arxiv API orqali o'qiydi; u bevosita ma'lumotlar bazasiga ulanmaydi. Stdout faqat MCP xabarlarini uzatadi.

Masofaviy mijozlar uchun panel yonida xizmatni ishga tushiring:

```
python -m tgwitness.mcp_server --transport streamable-http \
  --api-url http://127.0.0.1:8787 --port 8766 \
  --public-url https://archive.example.org/mcp
```

`/mcp` ni HTTPS teskari proxy orqali `127.0.0.1:8766/mcp` ga uzating, `Authorization: Bearer …` sarlavhasini saqlagan holda. Avtorizatsiya sarlavhalari va so'rov/javob tanalarini loglashni o'chirib qo'ying. Loopbackdan tashqariga bog'lanishni faqat kerak bo'lganda, `--host` va `--public-url` ni ishlatib yoqing. Endpoint rasmiy [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) dasturidagi Streamable HTTP dan foydalanadi. U aniq sozlangan bearer kreditsiyalarini qo'llab-quvvatlaydi, OAuth kashfiyotini emas; faqat OAuth talab qiladigan mijozlar qo'llab-quvvatlanmaydi.

**Tekshiruv protokoli va kirish** haqiqiy MCP mijozini ishga tushiradi va vositalarni ro'yxatlaydi. U xabarlarni olib kelmaydi. Masofaviy tekshiruv uchun tanlangan MCP server arxiv tokenini oladi. Faqat o'zingiz boshqaradigan yoki ishonadigan serverni sozlang.

## Doira va natijalar

Mavjud vositalar: `list_workspaces`, `list_chats`, `search_messages`, `get_message_versions`, `get_message_context`, `get_journal_event` va `get_capture_status`. Telegram harakatlari, sozlamalarni o'zgartirish yoki ommaviy eksport vositalari mavjud emas. Har bir o'qish ish maydoni/suhbatga kirishni qayta tekshiradi; muddati tugagan va bekor qilingan ma'lumotlar ishlashni to'xtatadi. Cheklovlar: har bir ma'lumotnoma bo'yicha daqiqada 60 API so'rovi, har bir sahifada 50 yozuv, 64 KiB javob va sakkiz soniyalik API muddati.

Xabar natijalariga ish maydoni, suhbat/xabar IDlari, voqealar ketma-ketligi, saqlangan xesh va panel havolasi kiradi. Havolani ochadigan ko'ruvchida o'zining ruxsat etilgan panel sessiyasi bo'lishi kerak. Xom Telegram obyektlari, kirish xeshlari, fayl havolalari, sessiya materiallari va kalitlar kiritilmagan. Qidiruv xabar matnini tekshiradi, xom maydonlarni emas. Matn chegaralangan va qisqartirilgan joylar belgilanadi. Tahrirlar, Telegram o'chirish bildirishnomalari va `missing_on_recheck` alohida kuzatuvlar sifatida qoladi. Sohaga oid kirish butun ish maydonidagi operatsion voqealarni ko'ra olmaydi; yozib olish holati bu cheklovni aniq belgilaydi.

Arxiv matni ishonchsiz kirish hisoblanadi. Xabarlardagi ko'rsatmalar qo'shimcha imtiyoz bermaydi va ularni mijoz ko'rsatmalari deb hisoblash mumkin emas. Tashqi sun'iy intellekt modeli MCP-mijoz so'raydigan har qanday kontentni qabul qilishi mumkin. Faqat o'qish huquqi arxivni o'zgartirishni oldini oladi; ammo bu mijozning o'qigan ma'lumotlarini saqlashiga to'sqinlik qilmaydi.

Hashlar saqlangan yozuvlarni aniqlaydi va yaxlitlik tekshiruvlarini qo'llab-quvvatlaydi. Ular mustaqil ravishda Telegram muallifligini yoki har bir xabar qabul qilinganini isbotlamaydi.
