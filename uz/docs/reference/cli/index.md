# Buyruq satri

Canonical page: https://phishdestroy.github.io/TgWitness/uz/docs/reference/cli/

Qidiruv, kontekstni o'qish, faoliyatni hisoblash va skriptlar hamda agentlardan saqlangan xabarlarni eksport qilish, --json chiqish, barqaror chiqish kodlari va doirali faqat o'qish uchun tokenlar bilan.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Hujjatlash](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md)

![Archive integrations](https://phishdestroy.github.io/TgWitness/assets/chapter-integrations.svg)

[Faqat o'qish uchun MCP](https://phishdestroy.github.io/TgWitness/uz/docs/reference/mcp/) · [To'liq matnli qidiruv](https://phishdestroy.github.io/TgWitness/uz/docs/reference/search/) · [Wiki](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

**Oldindan ko'rish.** `tgwitness search`, `context`, `messages`, `stats` va `export` o'qish skriptlar va sun'iy intellekt agentlari uchun saqlangan kuzatuvlar. Ular Telegramga hech narsa yubora olmaydi, sozlamalarni o'zgartira olmaydi yoki imzolangan jurnalni tahrir qila olmaydi.

Bilan `--json`, stdout aniq bir JSON hujjatni uzatadi (`export` JSON Lines yozadi). Taraqqiyot, ishoralar va xatoliklar stderr ga yuboriladi. Chiqish kodlari barqaror:

| Kod | Ma'no |
| --- | --- |
| `0` | Muvaffaqiyat, bo'sh natija ham kiritilgan |
| `1` | Xato: erishib bo'lmaydigan panel, o'qib bo'lmaydigan ma'lumot, uzilgan eksport |
| `2` | Foydalanish xatosi yoki noto'g'ri so'rov: noto'g'ri sana, noma'lum parametr, qidiruv indeksi noto'g'ri |
| `3` | Hozirda mavjud emas: ish maydoni ishga tushirilgan panelda ochiq yoki panel keyinroq qayta urinishni so'raydi (cheklov, vaqt tugashi) |
| `4` | Kirish rad etildi: token yetishmayapti, muddati tugagan yoki bekor qilingan, doirasidan tashqaridagi suhbat, ruxsat berilmaydigan vosita |

## Ikki o'qish usuli

**Panel orqali (`--url`).** Bu buyruq MCP kabi bir xil doiraviy arxiv API-dan foydalanadi. **Integratsiyalar → MCP** bo'limida ulanish yarating: ish maydonchalari va suhbatlarni, vositalarni va amal qilish muddatini tanlang, so'ng tokenni bir marta nusxalang. Ulanish faqat o'qish uchun mo'ljallangan, faqat shu suhbatlar bilan cheklangan, daqiqasiga 60 ta so'rov bilan tezlik bo'yicha cheklangan va istalgan vaqtda bekor qilinishi yoki aylantirilishi mumkin. Panelga kirish tokenlari va Telegram ma'lumotlari bu yerda ishlamaydi.

```
export TGWITNESS_URL=https://panel.example.org      # default http://127.0.0.1:8787
export TGWITNESS_MCP_TOKEN=tgw_mcp_...              # or --token-file path
tgwitness search 'перевод карта' --json
```

Masofaviy panel uchun HTTPS talab etiladi; oddiy HTTP faqat uchun qabul qilinadi `127.0.0.1`, `localhost` va `::1`Proxy muhit o'zgaruvchilari e'tiborsiz qoldiriladi va yo'naltirishlar rad etiladi, shuning uchun token faqat siz bergan manzilga yetib boradi.

**To'xtatilgan ish maydonidan to'g'ridan-to'g'ri (`--data-dir`).** Tokensiz, to'liq mahalliy kirish huquqi bilan ma'lumotlar katalogini o'qiydi. Ma'lumotlar katalogining nusxasida yoki yig'ish to'xtatilgan paytda ishlating. Imzolangan yozuvlar hech qachon o'zgartirilmaydi; panel kabi, ish maydonini ochish uning hosil qilingan indekslari yangilanishi mumkin. Panel ish maydonini ochgan paytda, buyruq kod bilan chiqadi `3`; o'rniga paneldan o'qish. `--data-dir`, `TGWITNESS_DATA`, `./data/live` yoki buyrug'ni bajarayotgan o'rnatmaning ma'lumotlar katalogi ishlatiladi.

`--workspace ID` ish maydonini tanlaydi (bo'sh `default`). `tgwitness messages
--workspaces` o'qish huquqiga ega bo'lganlarini ro'yxatlaydi.

## Buyruqlar

| Buyruq | Natija |
| --- | --- |
| `tgwitness search QUERY [--chat ID] [--since] [--until] [--any] [--limit N] [--offset N]` | Avvalo eng yaxshi mos keladiganlar, so'z shakllari, aniq iboralar ikki nuqtali qavs ichida, domenlar va `@username` ([sintaksis](https://phishdestroy.github.io/TgWitness/uz/docs/reference/search/#search-syntax)) |
| `tgwitness search QUERY --exact [--before SEQ]` | Aniq matn, eng yangi avval, indeksisiz |
| `tgwitness context CHAT_ID MESSAGE_ID` | Saqlangan xabarlar har ikkala tomondagi o'n xabar ID oralig'ida |
| `tgwitness messages` | O'qishingiz mumkin bo'lgan suhbatlar |
| `tgwitness messages CHAT_ID [--since] [--until] [--before SEQ]` | Suhbatning saqlangan xabarlari, eng yangilari birinchi |
| `tgwitness messages CHAT_ID --message ID` | Har bir saqlangan versiya va bitta xabarning o'chirish yozuvi |
| `tgwitness stats [--chat ID] [--sender ID] [--since] [--until] [--top N]` | Quyida faoliyat statistikasi |
| `tgwitness export [--chat ID] [--since] [--until] [--output FILE]` | Saqlangan kuzatuvlar jurnal tartibida JSON Lines shaklida |

Sanalar `2026-10-01` (UTC yarim kecha) yoki vaqt zonasini hisobga olgan ISO vaqtlari, `2026-10-01T09:00+03:00`. Uchun `search`, `messages` va `export` ular kuzatuv vaqtini tanlaydilar. Sahifalar 50 tagacha yozuvni saqlaydi: kuzatib boring `next_offset` (`--offset`) reytingli qidiruv va `next_before` (`--before`) boshqa joylarda.

Ranked search stops at 1,000 results. The final page may be shorter than `--limit`; narrow the query, chat or period when more matching observations exist.

Har bir xabar natijasi quyidagilarni o'z ichiga oladi `untrusted_content: true`, ish maydoni, suhbat va xabar IDlari, jurnal ketma-ketligi, saqlangan yozuvning xeshini va panel havolasini o'z ichiga oladi. Tahrirlar, o'chirish bildirishnomalari va `missing_on_recheck` alohida yozuvlardir. Yozuvning yo'qligi voqeaning hech qachon sodir bo'lmagani isbotlanmaydi.

### Faoliyat statistikasi

`stats` bir suhbat, bir jo'natuvchi yoki doiradagi barcha suhbatlar bo'yicha saqlangan kuzatuvlarni hisoblaydi:

- xabarlar UTC soati va haftaning kunlari bo'yicha (dushanba birinchi), eng gavjum soatlar va kunlar;
- tahrirlangan, o'chirilgan va `missing_on_recheck` ulashishlar;
- xabar soni va birinchi hamda oxirgi xabar yuborilgan vaqtlari bilan yuboruvchilar;
- eng ko'p uchraydigan domenlar va `@handles`, saqlangan versiyalar bo'ylab har bir xabar uchun bir marta hisoblanadi;
- qamrov: `coverage.gap` yozuvlarni va butun ish maydoniga kirish uchun davrlarni ulangan kollektor yuragi bo'lmagan davrlar (`collector_liveness`).

Davr **Telegram tomonidan xabar vaqtini hisobot berish** muddatini belgilaydi. Soat va hafta kunlari soni jo'natuvchining vaqt zonasini taxmin qilishda yordam berishi mumkin; ularni aniq belgilamaydi. Raqamlar jurnal so'rovi bo'yicha hisoblanadi va saqlanmaydi. Har bir natija ish maydoningiz bo'ylab kirishingiz davom etganda qamrab oladigan jurnal sarlavhasini nomlaydi. Paneldan besh soniya o'tgach o'qish to'xtaydi, yoki `--timeout` sekund (defolt 30); so'ngra `complete` noto'g'ri bo'ladi va `partial` o'qilmagan birinchi yozuvni nomlaydi. Bu holda faqat eng so'nggi yozuvlar hisobga olinadi.

### Eksport

`export` saqlangan kuzatuv uchun bitta JSON ob'ektini yozadi (yangi xabarlar, snapshotlar, tahrirlar, tiklangan xabarlar, o'chirish bildirishnomalari, `missing_on_recheck` va saqlangan media yozuvlari jurnal tartibida yoziladi. Har bir satr boshqa natijalar kabi bir xil maydonlarga ega bo'lib, to'liq matnni o'z ichiga oladi. `--output`, fayl quyidagi yo'lda yoziladi `.partial` nomini oladi va faqat panel yakuniy yozuvidan keyin qayta nomlanadi; to'xtatilgan eksport hech qanday fayl qoldirmaydi va kod bilan chiqadi `1`. `--output` mavjud faylni hech qachon ustiga yozmaydi. `--output` va `--json`, stdout orqali qisqacha hisobot chiqariladi: yozuvlar soni, oxirgi jurnal ketma-ketligi va butun ish maydoni bo'yicha kirish huquqi bo'lsa, jurnal sarlavhasi.

Panel orqali eksport qilish uchun **"Xabarlarni eksport qilish"**ga ruxsat beruvchi ulanish talab etiladi **(faqat buyruq satri)**; bu bo'yicha avtomatik tanlanmagan. Ushbu fayl ishlash nusxasi bo'lib, dalil emas: tekshiriladigan topshirish uchun "**Eksportlar**" bo'limidagi imzolangan eksportdan foydalaning, `python -m tgwitness.verify`tekshiradi.

The panel rechecks access before emitting each record, including the completion record. Revoked or expired access leaves an incomplete export. Lazy page reads share the archive worker limit with other queries and have a bounded wait.

## Agent mahorati

[`.agents/skills/tgwitness-cli/SKILL.md`](https://github.com/phishdestroy/TgWitness/blob/main/.agents/skills/tgwitness-cli/SKILL.md) agentga bu buyruqlarni qanday ishlatishni, yozuvlarni qanday keltirishni va ushlangan matnni qanday qayta ishlashni tushuntiradi. O'qiydigan agentlar `.agents/skills` Uni ombordan yuklab oling. Claude Code uchun, nusxa ko'chiring `tgwitness-cli` papkaga `.claude/skills/` loyihangizga nusxa ko'chiring yoki `~/.claude/skills/`.

## MCP va buyruq qatori

Ikkalasi ham bir xil ulanishlar, doira tekshiruvlari va cheklovlardan foydalanadi. MCP natijalari bitta 64 KiB sahifaga cheklangan, shuning uchun MCP ommaviy eksportni taklif qilmaydi; buyruq satri uni oqim sifatida chiqaradi. `get_activity_stats` har ikkala holatda ham mavjud.
