# Faqat o'qish uchun MCP

Canonical page: https://phishdestroy.github.io/TgWitness/uz/docs/reference/mcp/

MCP mijozini tanlangan ish maydonlari va suhbatlarga muddati tugaydigan, bekor qilinishi mumkin bo'lgan kirish huquqi bilan ulashing.

Tahlilchi mijozini tanlangan ish maydonlari va chatlarga ulang. TgWitness **panel jarayonida `/mcp` manzilida Streamable HTTP** xizmatini ko‘rsatadi. Har bir ulanish o‘zining tokeni, amal qilish muddati va ruxsat etilgan vositalariga ega. MCP Telegram xabarlarini yubora olmaydi, sozlamalarni o‘zgartira olmaydi yoki imzolangan jurnalni tahrirlay olmaydi.

[Ish jarayoni bo'yicha qo'llanma](https://phishdestroy.github.io/TgWitness/docs/archive/) · [Wiki](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

## O‘rnatish va tekshirish

Panelni ishga tushiradigan Python muhitidan foydalaning. Manba kodlari yuklab olingan katalogdan:

```
# Windows PowerShell
& .\.venv\Scripts\python.exe -m pip install -c deploy/constraints-mcp.txt -e '.[mcp]'
& .\.venv\Scripts\python.exe start.py --check
```

```
# Linux / macOS
.venv/bin/python -m pip install -c deploy/constraints-mcp.txt -e '.[mcp]'
.venv/bin/python start.py --check
```

O‘rnatishdan so‘ng panelni odatdagi ma’lumotlar katalogi va ishga tushirish argumentlari bilan qayta ishga tushiring. Tayyorlik holatida `[PASS] mcp: streamable-http available` bo‘lishi kerak. **Integrations → MCP** bo‘limida ish vaqti (runtime) holati va ushbu serverning haqiqiy Python bajariladigan faylidan foydalangan holda o‘rnatish buyrug‘i ko‘rsatiladi. **Re-check** tugmasi sahifani qayta yuklamasdan ushbu holatni yangilaydi; u paketlarni o‘rnatmaydi yoki serverni qayta ishga tushirmaydi.

MCP extra rasmiy [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)'dan foydalanadi.`deploy/constraints-mcp.txt` sinovdan o'tgan SDK va uning bog'liqliklarini belgilaydi.

## Ulanish yaratish

1. Yorliq kiriting va mijoz o‘qishi mumkin bo‘lgan ish maydonlari hamda chatlarni tanlang.
2. Vositalarni alohida-alohida tanlang yoki tayyor shablondan foydalaning. Faqat amalga oshirilgan vositalar taklif etiladi.
3. 1, 7, 30 yoki 90 kunni, yoxud bir daqiqadan 90 kungacha bo‘lgan maxsus amal qilish muddatini tanlang.
4. **Create connection** tugmasini bosing. Token mijoz konfiguratsiyasi yonida bir marta ko‘rinadi.
5. Token va konfiguratsiyani nusxalab oling, so‘ngra **Check connection** tugmasini bosing. U MCP ni ishga tushiradi va ruxsat etilgan vositalar ro‘yxatini chiqaradi; **hech qanday xabar o‘qilmaydi**. Natijada protokol talqini, vosita nomlari, ularning soni va sarflangan vaqt ko‘rsatiladi.
6. Hisob ma’lumotlari saqlanganidan so‘ng **Done** tugmasini bosing. Davriy so‘rovlar (polling) shaklni va bir marta ko‘rsatiladigan kartani saqlab qoladi. Panelni qulflash ekranda ko‘rsatilgan maxfiy ma’lumotlarni tozalaydi.

Ro‘yxatda so‘nggi foydalanish, oxirgi vosita, manzil va so‘nggi daqiqadagi so‘rovlar soni ko‘rsatiladi. **Revoke** kirish huquqini to‘xtatadi. **Rotate token** eski hisob ma’lumotlarini bekor qiladi va xuddi shu qamrov, vositalar hamda amal qilish muddati bilan yangisini yaratadi; yangisini bir marta nusxalab oling. Panelga kirish tokenlari va Telegram hisob ma’lumotlari MCP tokenlari sifatida ishlamaydi.

## Mijozingizni ulash

Panelda mijozni tanlang va yaratilgan konfiguratsiyani nusxalab oling. Konfiguratsiyalarda maxfiy havolalar yoki aniq o‘rinbosarlar (placeholders) ishlatiladi; token alohida nusxalanadi.

| Mijoz | Konfiguratsiya | Ulanish |
| --- | --- | --- |
| Claude Code | `.mcp.json` | HTTP, `type: "http"`, bearer sarlavhasi |
| Claude Desktop | `claude_desktop_config.json` | Lokal stdio ko‘prigi |
| Cursor | `.cursor/mcp.json` | Muhit o‘zgaruvchisi sarlavhasiga ega HTTP |
| VS Code Local | `.vscode/mcp.json` | Parolli `promptString` kiritmasiga ega HTTP |
| Windsurf | `mcp_config.json` | Bearer sarlavhasi o‘rinbosariga ega HTTP |
| Boshqa mijozlar | URL va Authorization sarlavhasi | Streamable HTTP |

TgWitness OAuth aniqlashisiz bearer tokenlardan foydalanadi. Masofaviy ulagichi OAuth talab qiladigan mijozlar uchun lokal stdio ko‘prigidan foydalaning. VS Code uchun kiritish o‘zgaruvchilari **Local** muhitiga taalluqli bo‘lib, Copilot sessiyalariga uzatilmaydi. Konfiguratsiya bo‘yicha ma’lumotnomalar: [Claude Code](https://code.claude.com/docs/en/mcp), [Cursor](https://prod.cursor.com/docs/mcp), [VS Code](https://code.visualstudio.com/docs/agents/reference/mcp-configuration).

Lokal ko‘prik uchun standart kirish nuqtasi:

```
python -m tgwitness.mcp_server --url https://your-panel.example/mcp
```

Mijozning MCP qo‘shimcha paketi o‘rnatilgan lokal Python muhitidan foydalaning. Uning himoyalangan muhitida `TGWITNESS_MCP_TOKEN` o‘zgaruvchisini o‘rnating. Hisob ma’lumotlarini buyruq argumentlari va URL manzillariga kiritmang. `tgwitness-mcp` xuddi shu kirish nuqtasidir. Eski `tgwitness.mcp_bridge` moduli va `TGWITNESS_ARCHIVE_TOKEN` nomi ogohlantirish bilan moslik yo‘llari sifatida saqlanib qolgan; yangi konfiguratsiyalarda `mcp_server` va `TGWITNESS_MCP_TOKEN` ishlatiladi.

## Cloudflare Tunnel

Panelning `/mcp` yo‘nalishini yo‘naltiring va bearer sarlavhasini saqlab qoling. Administrator sifatida MCP sozlamalarini ochish ushbu ishga tushirish jarayoni uchun panelning joriy manbasini (origin) ro‘yxatdan o‘tkazadi. Qayta ishga tushirilgandan so‘ng darhol mavjud bo‘ladigan barqaror manzil uchun, panelni ishga tushirishdan oldin `TGWITNESS_PUBLIC_URL` o‘zgaruvchisini panelning HTTPS manbasi bilan sozlang. Ixtiyoriy Host va yo‘naltirilgan sarlavhalar ishonchli manzilni ro‘yxatdan o‘tkazmaydi. Host va Origin tekshiruvlari aloqador bo‘lmagan brauzer manbalarini rad etadi. Javoblarda `Cache-Control: no-store` ishlatiladi; avtorizatsiya qiymatlari hech qachon jurnalga yozilmaydi.

`*.trycloudflare.com` manzili vaqtinchalik hisoblanadi. Tunnelni qayta ishga tushirish xost nomini o‘zgartirganda, sozlangan ommaviy URL va har bir mijozning MCP URL manzilini yangilang. Saqlangan mijoz konfiguratsiyalari uchun barqaror xost nomidan foydalaning.

## Vositalar va chegaralar

| Vosita | O‘qiydi |
| --- | --- |
| `list_workspaces` | Ruxsat berilgan ish maydonlari |
| `list_chats` | Ruxsat berilgan chatlar |
| `search_messages` | Tanlangan davr ichida saqlangan xabar matni |
| `get_message_versions` | Qayd etilgan talqinlar va o‘chirish kuzatuvlari |
| `get_message_context` | Yaqin atrofdagi qayd etilgan xabar ID lari |
| `get_journal_event` | Manba havolasiga ega bitta tozalangan (sanitized) yozuv |
| `get_capture_status` | Yig‘ish holati va ruxsat etilgan qamrov yozuvlari |

`tools/list` faqat ushbu ulanishga ruxsat berilgan vositalarni qaytaradi. Boshqa vositalarga chaqiruvlar rad etiladi. Guruh konteksti, epizod, terminologiya va javoblar zanjiri vositalari ushbu yig‘mada taklif etilmaydi; ularning alohida kontekst-paket bekendi kiritilmagan.

Har bir o‘qish amali token, vosita va ish maydoni/chat qamrovini, jumladan ma’lumotlar bazasi ishi tugaganidan keyin ham tekshiradi. Cheklovlar: daqiqasiga 60 ta so‘rov, har bir sahifada 50 ta yozuv, har bir natija uchun 64 KiB va arxiv uchun sakkiz soniyalik yakuniy muddat. Vaqti tugagan MCP chaqiruvi torroq davrni yoki kamroq cheklovni so‘rab vosita xatosini qaytaradi.

Xabar natijalari `untrusted_content: true`, ish maydoni/chat/xabar ID lari, hodisa ketma-ketligi, saqlangan xesh va panel havolasini o‘z ichiga oladi. Xom Telegram obyektlari, kirish xeshlari, sessiyalar va kalitlar tushirib qoldiriladi. Matn qisqartirilganligi belgilanadi. Tahrirlar, o‘chirish bildirishnomalari va `missing_on_recheck` alohida kuzatuvlar hisoblanadi. Yozuvlarning yo‘qligi hodisa hech qachon sodir bo‘lmaganligini isbotlamaydi.

Qayd etilgan xabarlar ichidagi ko‘rsatmalarga hech qachon mijoz ko‘rsatmalari sifatida emas, balki dalil sifatida qarang. Faqat o‘qish uchun kirish huquqi arxiv o‘zgarishlarining oldini oladi; biroq mijoz o‘ziga o‘qishga ruxsat berilgan kontentni saqlab qolishi mumkin. Xeshlar saqlangan yozuvlarni aniqlaydi va yaxlitlikni tekshirishni qo‘llab-quvvatlaydi; ular Telegram muallifligini yoki to‘liq qayd etilganlikni isbotlamaydi.
