# Telegram · To'liq matnli qidiruv

Canonical page: https://phishdestroy.github.io/TgWitness/uz/docs/reference/search/

Imzolangan jurnalga bog'langan indeks yordamida so'z shakllari, aniq iboralar, domenlar va @foydalanuvchi nomlari bo'yicha saqlangan xabarlarni toping, eng yaxshi mos keladiganlarini birinchi qilib ko'rsating.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Hujjatlash](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Tergov](https://phishdestroy.github.io/TgWitness/uz/docs/reference/investigation/)

![Tergov](https://phishdestroy.github.io/TgWitness/assets/chapter-investigate.svg)

[Arxiv tahlili](https://phishdestroy.github.io/TgWitness/uz/docs/reference/analysis/) · [Mahalliy OCR va transkripsiya](https://phishdestroy.github.io/TgWitness/uz/docs/reference/media-analysis/) · [Wiki](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

**Ko'rinish.** Jurnalda qidiruv maydoni yonidagi **Eng yaxshi moslik · so'z shakllari** ni tanlang. Natijalar BM25 bo'yicha tartiblangan va bir xil so'zning boshqa shakllariga mos keladi: *перевод* so'zi *переводом* va *переводы ni* topadi, *transfer* *so'zi* *transfers* ni topadi, xitoy iborasi bo'shliqlarsiz topiladi. **Eng yangi birinchi · aniq matn** butun yozuv bo'ylab oldingi substring qidiruvini saqlaydi.

Indeks – bu hosil qilingan ma'lumot. U imzolangan jurnal asosida qayta tuziladi, hech qachon o'zi imzolanmaydi va hech qachon eksportga kiritilmaydi. Asl yozuvlar o'zgarmaydi.

**Ushbu sahifada**

- [Qidiruv sintaksi](https://phishdestroy.github.io/TgWitness/uz/docs/reference/search/#search-syntax)
- [tillar](https://phishdestroy.github.io/TgWitness/uz/docs/reference/search/#languages)
- [Indeks qaerda joylashgan](https://phishdestroy.github.io/TgWitness/uz/docs/reference/search/#where-the-index-lives)
- [Natijalar va imzolangan jurnal](https://phishdestroy.github.io/TgWitness/uz/docs/reference/search/#results-and-the-signed-journal)
- [Tan olingan matn](https://phishdestroy.github.io/TgWitness/uz/docs/reference/search/#recognized-text)
- [Kirish](https://phishdestroy.github.io/TgWitness/uz/docs/reference/search/#access)
- [Arxiv va MCPdan so'rang](https://phishdestroy.github.io/TgWitness/uz/docs/reference/search/#ask-the-archive-and-mcp)
- [Qarorgohlar](https://phishdestroy.github.io/TgWitness/uz/docs/reference/search/#dependencies)
- [Benchmark](https://phishdestroy.github.io/TgWitness/uz/docs/reference/search/#benchmark)

## Qidiruv sintaksi

| Yozing | Topadi |
| --- | --- |
| `перевод карта` | Ikkala so'zni ham o'z ichiga olgan yozuvlar, har qanday shaklda |
| `"переводом на карту"` | Aniq ibora, aynan shu tartibda |
| `бонус OR подарок` | Istalgan so'z |
| `перевод -казино` | Chiqarib tashlangan so'zsiz yozuvlar |
| `example.com` | Domen va uning ostki domenlari, shuningdek yashirin havolalar va tugma URL-larida |
| `@username`, `t.me/username` | Hisobning tilga olinishi va havolalari, shuningdek yuborgan xabarlari |
| `#tag` | Heshteg |
| `+79991234567`, hamyon manzili, elektron pochta manzili | Matn yoki havolalardagi xuddi shu qiymat |
| `from:@username`, `from:123456` | Ushbu jo'natuvchidan kelgan xabarlar |
| `chat:-1001234567890` | Bir chat; u faqat sizning o'z kirishingizni cheklashi mumkin |
| `id:42` | 42-xabar versiyalarining saqlangan nusxalari |
| `since:2026-01-01 until:2026-01-31` | Kuzatuv davri; vaqtsiz sana butun kunni qamrab oladi |
| `kind:edited` | Faqat tahrirlar (`new`, `snapshot`, `edited`, `recovered`) |
| `source:ocr`, `source:transcription`, `source:all` | Xabarlar o'rniga yoki ular bilan birga tan olingan matn |

Boshqa so'zlar mavjud bo'lsa, predloglar va boshqa funksional so'zlar e'tiborsiz qoldiriladi. So'z ichiga aralashgan bir-biriga o'xshash harflar (Cyrillic harfi ichidagi lotin *a*), kengligi to'liq harflar va bezakli Unicode harflari hamda ko'rinmas belgilar normalizatsiya qilinadi.

## tillar

Til har bir yozuvda uning skripti va harflari asosida aniqlanadi:

| Skript | Mos kelish |
| --- | --- |
| Kirillik | [pymorphy3](https://github.com/no-plagiarism/pymorphy3) yordamida rus va ukrain lemmmalari. Ixtiyoriy ukrain lug'oti bo'lmasa, yengil ukrain stemmeri ishlatiladi. |
| Lotincha | Inglizcha Snowball stemmer; diakritik belgilar e'tiborsiz qoldiriladi |
| Xitoycha, yaponcha, koreyscha, taycha, laocha, xmercha, myanmacha | Qoplashgan harf juftliklari: bo'shliqlarsiz topilgan istalgan ibora. Xitoy so'rovlari jieba yordamida so'zlarga bo'linadi. |
| Boshqa skriptlar | Aniq so'zlar |

Ukrain tilidagi lug'at (`pymorphy3-dicts-uk`) GPL-3.0 litsenziyasi ostida tarqatiladi, shuning uchun u standart bo'yicha o'rnatilmaydi. Uni quyidagilar bilan o'rnating `pip install "tgwitness[uk-dictionary]"`; indeks yangi tahlilchisini payqab, o'zini qayta kompilyatsiya qiladi.

## Indeks qayerda joylashgan

| Rejim | Saqlash | Foydalaning |
| --- | --- | --- |
| Diskda (bo'sh) | `search/fulltext.sqlite3` ish maydoni katalogida | Katta arxivlar; qayta ishga tushirishlardan omon qoladi |
| Faqat xotirada | Diskda hech narsa yo'q; har boshlanishda qayta kompilyatsiya qilinadi | Diskda xabar matnining hech qanday hosil qilingan nusxasi |
| O'chirilgan | Indeks yo'q; **eng yangi birinchi · aniq matn** saqlanadi | Minimal o'rnatishlar |

Asosiy administrator har bir ish maydoni uchun **Jurnal → Filtrlar → Qidiruv indeksi** bo'limida rejimni tanlaydi. `TGWITNESS_FULLTEXT=disk|memory|off` o'z tanlovi bo'lmagan ish maydonchalari uchun standartni belgilaydi. Xotiraga yoki o'chirilgan holatga o'tish faylni o'chirib tashlaydi. Indeks fayli jurnal bilan bir xil himoyaga ega: u shaxsiy ma'lumotlar papkasi ichida joylashgan. U shifrlanmagan va zaxira nusxalari yoki tashqi nusxalarning tarkibiga kirmaydi.

Yangi yozuvlar fon rejimida bir necha soniya ichida indekslashadi; qidiruv ham avval qisqa orqaliqni indekslaydi, shuning uchun bir zum oldin saqlangan yozuv topiladi. Mavjud jurnal yangilanishdan so'ng panelni bloklamasdan indekslashadi; shu vaqtgacha natijalar indekslangan yozuvlarni qamrab oladi va jurnal jarayonning borishini ko'rsatadi. **Indeksni qayta qurish** birinchi yozuvdan boshlab yana boshlanadi.

```
python -m tgwitness index status --data-dir data/live
python -m tgwitness index rebuild --data-dir data/live --json
```

`rebuild` panel to'xtatilishi kerak (aks holda chiqish kodi 3 bo'ladi). `--json`, standart chiqish faqat natijani uzatadi; jarayon holati standart xato chiqishiga yoziladi.

## Natijalar va imzolangan jurnal

Indeks qamrab olgan oxirgi jurnal yozuvining ketma-ketlik raqami va hashini saqlaydi va jurnal ochilganda ularni jurnal bilan solishtiradi. O'rnini bosgan, tiklangan yoki tahrirlangan jurnal qayta tuzilishiga sabab bo'ladi. Har bir javob ushbu pozitsiyani bildiradi, va har bir topilma imzolangan jurnaldan uning ketma-ketlik raqami bo'yicha o'qiladi: indeks qaysi yozuvlarni va qanday tartibda ko'rsatishni belgilaydi, ularning mazmunini emas. Chatga kirish huquqi jurnalning o'z chat maydoniga qo'llaniladi, indeks mazmuniga emas.

## Tan olingan matn

OCR va transkriptlar shifrlangan artefaktlarda qoladi. Ularning indeksi faqat xotirada mavjud bo'lib, tan olish ishi yakunlanganda qayta tuziladi. Topilma uning `media.saved` yozuvida paydo bo'ladi, u yerda mashina tanib olish, dvigatel, model va parchasi bilan belgilangan; u hech qachon Telegramda yuborilgan matn sifatida ko'rsatilmagan. Xuddi shu indeks **tan olingan matnni qidirish** uchun xizmat qiladi, u hanuz oddiy substringlarga ham mos keladi.

## Kirish

Suhbat doirasidagi kirish faqat o'z suhbatlaridagi yozuvlarni, ularning ilovalaridagi tan olingan matnni ham o'z ichiga olgan holda topadi. `chat:` va boshqa filtrlar faqat shu to'plamni toraytirishi mumkin. Cheklangan kirishga ko'rsatilgan indeks holati jurnalning umumiy yig'indilarini o'z ichiga olmaydi. Faqat asosiy administrator rejimni o'zgartirishi yoki indeksni qayta qurishi mumkin.

## Arxiv va MCPdan so'rang

**So'rov indeks** to'liq tugagach, u manbalarni ushbu indeksten oladi: tanlangan suhbatlar bo'ylab eng yaxshi mos keluvchi natijalar, saqlangan matn esa faqat bir marta hisobga olinadi. 24 tagacha manba yuboriladi; uzun matnlar mos kelgan joyidan kesilib, qisqartirilgan deb belgilangan. Yaqinda bo'lgan o'zgarishlar, bitta xabarning saqlangan versiyalari va indeks hali shakllanayotgan paytdagi qidiruvlar bo'yicha savollar oldingi xronologik olish usulidan foydalanadi. Oldindan ko'rish qaysi usul ishlatilganini ko'rsatadi.

MCP mijozlari chaqirishi mumkin `search_messages` bilan `ranked=true` va sahifa bilan `next_offset`. Doiraga ajratilgan ulanishlar faqat o'z chatlarini oladi.

Ranglab tartiblangan sahifalash sahifa hajmiga qaramasdan, eng ko'pi bilan birinchi 1,000 ta natijani qamrab oladi. Qo'shimcha mosliklarni ko'rib chiqish uchun so'rov, suhbat yoki davrni toraytiring. Eng yangi avval qidiruvlar har bir sahifani tanlashdan oldin xabarlar, OCR va transkripsiya natijalarini tartiblaydi.

## Qaramliklar

| Paket | Litsenziya | Nega |
| --- | --- | --- |
| pymorphy3, pymorphy3-dicts-ru, DAWG2-Python | MIT | Rus va ukrain leksemalari; lug'atlar mahalliy ravishda yuklangan |
| snowballstemmer | BSD-3-band | Inglizcha stemlar, sof Python |
| jieba | MIT | Xitoycha so'rov segmentatsiyasi, sof Python (faqat manba tarqatmasi) |
| pymorphy3-dicts-uk (ixtiyoriy) | GPL-3.0 | To'liq ukraincha lug'at |

SQLite FTS5 bilan `unicode61` tokenizator talab etiladi; u joriy Python kompilyatsiyalaridagi SQLite tarkibiga kiradi. U bo'lmasa, best-match qidiruvi mavjud emasligini bildiradi.

## Benchmark

`python tools/bench_fulltext.py --messages 1000000 --work <empty directory>`200 ta chatdagi rus, ukrain, ingliz, xitoy va yapon tillaridagi aralash xabarlarning havolalar va identifikatorlar bilan deterministik imzolangan jurnalini yaratadi, indeksni tuzadi va odatiy qidiruvlarni (50 ta natija, 7 marta ijro etishning mediani) vaqt bo'yicha aniqlaydi.

Windows 11, Intel Core i9-13900K, 128 GB operativ xotira, Python 3.12.10, SQLite 3.49.1, ma'lumotlar exFAT diskida, analizator `fulltext-v1+pymorphy3-ru+light-uk+snowball-en`:

| O'lchash | Natija |
| --- | --- |
| Imzolangan jurnal | 1 000 000 xabar, 1,50 GiB, 19 daqiqada yozilgan |
| Jurnal asosida indeks tuzish | 71 s, sekundiga taxminan 14 141 xabar |
| Indeks fayli | 58 MiB, jurnalning 3,8% |
| Yangi yozuvdan keyin qidiruv | 8 ms median, 9 ms p95 |
| Avvalgi substring qidiruvi, xuddi shu jurnal | `перевод` 3.2 s, `银行转账` 2.6 s, `verify-account.example` 2.6 s |

| Qidiruv | Mos yozuvlar | Eng yaxshi moslik, mediana | p95 | Eng yangi birinchi, o'rtacha |
| --- | --- | --- | --- | --- |
| Umumiy so'z, so'z shakllari: `перевод` | 134,403 | 82 ms | 85 ms | 7 ms |
| Ikki so'z: `оплата карта` | 28,996 | 43 ms | 43 ms | 14 ms |
| Kam uchraydigan so'z: `розыгрыш подарок` | 28,881 | 42 ms | 47 ms | 13 ms |
| Aniq ibora: `"переказ коштів на картку"` | hisobga olinmagan | 35 ms | 36 ms | 6 ms |
| Subdomensiz domen: `verify-account.example` | 12,435 | 17 ms | 17 ms | 3 ms |
| @foydalanuvchi_nomi: `@support_desk_bot` | 10,331 | 15 ms | 16 ms | 3 ms |
| Bo'shliqsiz xitoycha: `银行转账` | 17,691 | 23 ms | 24 ms | 3 ms |
| Yaponcha: `リンク` | 16,603 | 23 ms | 25 ms | 3 ms |
| Inglizcha asos: `withdrawal` | 27,775 | 26 ms | 26 ms | 2 ms |
| VA istisno: `бонус OR подарок -казино` | 268,034 | 190 ms | 193 ms | 19 ms |
| Suhbat filtri: `chat:-1000000000007 перевод` | 652 | 9 ms | 9 ms | 6 ms |
| Davr filtr: `since:2026-01-01 until:2026-01-31 выплата` | 115,732 | 155 ms | 156 ms | 81 ms |

Aniq ibora nomzodlar bo'yicha tartib bo'yicha so'zma-so'z tekshiriladi, sahifa to'lib qolguncha, shuning uchun uning umumiy soni hisobga olinmaydi. Qidiruv vaqti mos yozuvlar soni ortishi bilan oshadi; suhbat yoki davrni toraytirish keng qamrovli qidiruvlarni tezlashtiradi. Sintetik korpus kichik lug'atni takrorlaydi, shuning uchun umumiy so'zlar haqiqiy suhbatlardagiga qaraganda ancha ko'proq yozuvlarga mos keladi.
