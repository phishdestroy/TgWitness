# Mustaqil guvoh

Canonical page: https://phishdestroy.github.io/TgWitness/uz/docs/reference/witness/

O'z kaliti va botiga ega Witnessni ishga tushiring, imzolangan tekshiruv nuqtalarini kanalga joylashtiring va eksportlarni ularga solishtiring.

[Bot va proxy sozlamalari rus tilida](https://github.com/phishdestroy/TgWitness/blob/main/docs/ru/WITNESS.md).

Yig'uvchi o'z jurnalini imzolaydi, shuning uchun yig'uvchi va uning kalitini nazorat qiluvchi har kim nazariy jihatdan jurnalni qayta yozishi yoki qisqartirishi va uni yana imzolashi mumkin. Guvox buni aniqlashga imkon beradi. Bu alohida jarayon — yana bir konteyner yoki, yaxshisi, kimdir boshqarayotgan server — bo'lib, u har bir necha daqiqada kollektorning imzolangan jurnal boshini oladi, ko'rganlarini o'z kaliti bilan imzolaydi, uni o'z jurnalida saqlaydi va Telegram kanaliga joylaydi.

Oqim sxemasi · Yig'uvchi → Guvoh (imzolangan tekshiruv nuqtasi: yozuvlar soni + sarlavha xesh); Guvoh → Witness jurnali, o'z kalitingiz; Guvoh → Telegram kanali (o'z boti orqali imzolangan post); Dalil ZIP → verify.py; Witness jurnali, o'z kalitingiz → verify.py; Telegram kanali → verify.py (Telegram Desktop eksporti yoki t.me/s sahifasi) · Yig'uvchi · Guvoh · Witness jurnali, o'zkalitingiz · Telegram kanali · Dalil ZIP · verify.py · imzolangan tekshiruv · nuqtasi: yozuvlar soni + · sarlavha xesh · o'z boti orqali imzolangan · post · Telegram Desktop eksporti · yoki t.me/s sahifasi

**Diagramma matn sifatida**

1. Yig'uvchi → Guvoh (imzolangan tekshiruv nuqtasi: yozuvlar soni + sarlavha xesh)
2. Guvoh → Witness jurnali, o'z kalitingiz
3. Guvoh → Telegram kanali (o'z boti orqali imzolangan post)
4. Dalil ZIP → verify.py
5. Witness jurnali, o'z kalitingiz → verify.py
6. Telegram kanali → verify.py (Telegram Desktop eksporti yoki t.me/s sahifasi)

## Guvoh nimani oladi va nimani olmaydi

| Guvohda | Guvoh hech qachon |
| --- | --- |
| Bir ish maydoni uchun faqat o'qish huquqiga ega **guvoh tokeni** | Yig'uvchining Telegram sessiyasi yoki API ma'lumotlari |
| O'zining Ed25519 kaliti va jurnali | Yig'uvchining ombori, imzolash kaliti yoki panel tokeni |
| O'z Telegram bot tokeni | Xabar mazmuni: sarlavha yozuvlar soni va xesh |

Token panelning **Witness** sahifasida yaratiladi, bir marta ko'rsatiladi va faqat SHA-256 ko'rinishida saqlanadi. U aynan bitta endpointni, `GET /api/witness/head` ni ochadi, u yangi imzolangan tekshiruv nuqtasini hamda mazmunsiz to'plam hisoblagichlari va operatsion holatini imzolab qaytaradi. U panelni ocholmaydi, xabar mazmunini o'qiy olmaydi yoki sozlamalarni o'zgartira olmaydi, va panel tokeni u yerda qabul qilinmaydi. Tokenni shu sahifada bekor qiling. Yig'uvchi yangi guvoh kaliti tekshirishni boshlagan vaqtni (`witness.seen`) qayd etadi va har bir token bo'yicha oxirgi tekshiruvni ko'rsatadi; 2,5 intervallarda tekshirilmagan guvoh muddati o'tgan deb belgilangan.

Yangi guvohlar har bir so'rov bo'yicha tasodifiy chaqiriq yuboradilar; capture bayonoti uni kollektor imzosining ostida aks ettiradi. Hisoblagichlar aniq nazorat nuqtasiga bog'langan va imzolangan guvoh postlariga kiritilgan. Meros boshliqlar mustaqil guvoh tomonidan qabul qilinishda davom etadi. Jurnal hajmining o'sishi alohida yangi xabar sifatida hisobga olinmaydi.

## Nimani tekshiradi va qayd etadi

Har bir intervaldan (o'rnatilgan bo'yicha 10 daqiqa) guvoh:

1. bosh qismni o'zi oladi (yig'uvchi uni sura olmaydi yoki o'tkazib yubora olmaydi);
2. to'plovchining imzosini, biriktirilgan to'plovchi kalitini (`--collector-fingerprint` yoki birinchi ko'rilgan kalit), kamaymaydigan hisobni va o'zgarmagan hisobdagi o'zgarmagan boshni tasdiqlaydi;
3. o'z jurnaliga imzolangan yozuvni ilova qiladi: `witness.anchor`, `ok`, `key_changed`, `rollback` (oldingisiga qaraganda kamroq yozuvlar), `fork` (uzunligi bir xil, boshqacha sarlavha) yoki `invalid` (javob tasdiqdan o'tmadi), yoki `witness.no_response` (to'plovchi javob bermaganida);
4. natijani kanalga joylaydi, imzolangan, shu jumladan "no answer", guvoh ishlayotgan va Bot API ga ulanish imkoniga ega bo'lgan paytda. Post ID yozib olinadi (`witness.posted`), shuningdek muvaffaqiyatsiz post ham (`witness.post_failed`).

Post quyidagicha ko'rinadi; oxirgi satr imzolangan bayonotni o'z ichiga oladi:

```
TgWitness witness #42 · journal head
Collector 3fa9c2d1e0b4a7f6: 18234 records
Head 9b1f…c07e
2026-10-28T19:40:00.123+00:00
TGW1.eyJhdCI6…<statement>.<signature>
```

## Witnessni ishga tushiring

Sizga Telegram boti (uni @BotFather yordamida yarating), o'sha bot ma'mur bo'lgan kanal va guvohdan erishiladigan kollektor manzili kerak — xususiy tarmoqdan tashqarida HTTPS orqali (joylashtir[ish](https://phishdestroy.github.io/TgWitness/uz/docs/reference/deployment/)dagi HTTPS profiliga qarang).

**Qo'shimchalarni** oching **→ Kanalingizdagi bot →** Paneldagi **botni sozlang** . Uch bosqichda faqat o'qish huquqi, kanalingiz va intervallar sozlanadi, so'ngra guvoh ishga tushiriladi. Nashr siyosati, ixtiyoriy HTTP/SOCKS5 proksi va maxsus Bot API manzili **Kengaytirilgan sozlam** alarda joylashgan. Forma ushbu ish maydonining yig'uvchi kaliti (collector key) biriktirilgan holda `witness.json` ni yuklab oladi. Yangi yaratilgan faqat o'qish uchun mo'ljallangan tokenni "**Save access file** as" `witness-token.txt` orqali yuklab oling; uni va guvoh mezbonida yaratilgan `bot-token.txt` ni shu JSON yoniga joylashtiring. Yig'uvchi bot tokenini hech qachon olmaydi. Yuklab olish xizmatni ishga tushirmaydi yoki xabarni e'lon qilmaydi. Hech qanday joylashtirilgan loyiha guvohi avtomatik ravishda ro'yxatdan o'tkazilmaydi.

```
python -m tgwitness.witness run --config witness.json --check-config
python -m tgwitness.witness run --config witness.json
python -m tgwitness.witness fingerprint --config witness.json
```

Birinchi buyruq tarmoq so'rovlari yoki kalit yaratilishisiz konfiguratsiya va maxfiy fayllarni tekshiradi. JSONdagi yo'llar shu faylga nisbatan nisbiy; CLI/muhit yo'llari esa ishchi katalogga nisbatan nisbiy. Guvoh barmoq izini uning mezboni tashqarisida saqlang. Yig'uvchining oxirgi so'rov ko'rsatkichi faqat so'rovni tasdiqlaydi; nashr Proof orqali xabar qilinadi yoki guvoh jurnalida va kanalda tekshiriladi.

Agar paneli SSH tunneli ortida qolsa, faqat Witness skop nuqtasini alohida HTTPS hostnomada [ushbu Caddy misoli](https://github.com/phishdestroy/TgWitness/blob/main/deploy/Caddyfile.witness.example) bilan ochiq qoldiring. O'rnatilgan ish maydoni keyin `https://witness.example.org`dan foydalanadi, boshqa ish maydonchalari esa `https://witness.example.org/profiles/ID`dan foydalanadi. Tokenlar hanuzgacha talab etiladi; panel va uning boshqa API yo'nalishlari o'sha virtual host orqali yo'naltirilmaydi.

`all`ni muntazam e'lon qilinadigan tekshiruv nuqtalari uchun tanlang. Besh daqiqalik oraliq har bir ish maydoni uchun kuniga taxminan 288 ta post degani. `changes` va `problems` maqsadli ravishda ba'zi tekshiruvlarni e'lon qilmaydi. MTProxy yig'uvchining Telegram ilovasi uchun mo'ljallangan. Witness HTTP so'rovi va Telegramning HTTPS Bot API o'zining to'g'ridan-to'g'ri/HTTP/SOCKS5 yo'nalishidan ([Bot API](https://core.telegram.org/bots/api)) foydalanadi.

**Yig'uvchiga qo'shimcha ravishda, Docker bilan** (bir xil host — mustaqil jarayon va kalit, lekin operator bir xil): `.env`ga qiymatlarni kiritib, profilni ishga tushiring.

```
TGWITNESS_WITNESS_TOKEN=tgww_...
TGWITNESS_WITNESS_BOT_TOKEN=123456:ABC...
TGWITNESS_WITNESS_CHANNEL=@your_witness_channel
# another workspace: TGWITNESS_WITNESS_COLLECTOR=http://tgwitness:8787/profiles/<workspace ID>

docker compose --profile witness up -d
docker compose logs witness     # prints the witness key fingerprint
```

E'lon qilingan rasm uchun `docker compose --project-directory . -f deploy/compose/compose.image.yaml --profile witness up -d` ni ishlating.

**Boshqa birovning serverida** (haqiqiy mustaqil guvoh): repozitoriyni o‘sha yerga nusxalang, `.env` faylida `TGWITNESS_WITNESS_COLLECTOR=https://your-collector.example.org` va yuqoridagi uchta qiymatni belgilang, so‘ng

```
docker compose --project-directory . -f deploy/compose/compose.witness.yaml up -d
```

yoki Docker'siz:

```
python -m tgwitness.witness run --collector https://your-collector.example.org \
    --token-file witness-token.txt --bot-token-file bot-token.txt --channel @your_witness_channel
```

### Imkoniyatlar

| Variant | Muhit | O'rnatilgan | Ma'no |
| --- | --- | --- | --- |
| `--interval` | `TGWITNESS_WITNESS_INTERVAL` | 10 | Tekshiruvlar orasidagi daqiqalar, 1–1440 |
| `--timeout` | `_TIMEOUT` | 30 | Kollektor va Bot API uchun kutish soniyalari, 5–600 |
| `--post` | `_POST` | `all` | `all`: har bir tekshiruv; `changes`: yangi bosh yoki muammo; `problems`: faqat muammolar va javobsiz savollar |
| `--title` | `_TITLE` | `TgWitness witness` | Har bir kanal postining birinchi so'zlari |
| `--collector-fingerprint` | `_COLLECTOR_FINGERPRINT` | – | Birinchi javobga ishonish o'rniga yig'uvchi kalitni belgilang |
| `--proxy` | `_PROXY` | to'g'ridan-to'g'ri | `socks5://host:port` yoki `http://host:port` |
| `--bot-api` | `_BOT_API` | `https://api.telegram.org` | Bot API manzili, masalan, mahalliy Bot API serveri |
| `--data-dir` | `_DATA` | `witness-data` | Witness kaliti va jurnali |
| `--config` | `_CONFIG` | – | Yuqoridagi istalgan variantlardan birini o'z ichiga olgan JSON fayl |

Yig'uvchi manzili, tokenlar va kanal `--collector`, `--token` yoki `--token-file`, `--bot-token` yoki `--bot-token-file` va `--channel`, yoki `_COLLECTOR`, `_TOKEN`, `_TOKEN_FILE`, `_BOT_TOKEN`, `_BOT_TOKEN_FILE` va `_CHANNEL` manzillaridan keladi, ular jarayonlar ro'yxatidan sirlarni yashiradi.

Konfiguratsiya fayli opsion nomlarini tirelar bilan, shuningdek `texts` ni ishlatadi, u kanal postlaridagi so'zlarni almashtiradi:

```
{"collector": "https://your-collector.example.org", "token_file": "witness-token.txt",
 "bot_token_file": "bot-token.txt", "channel": "@your_witness_channel",
 "interval": 5, "timeout": 30, "post": "changes", "title": "Partner witness",
 "texts": {"ok": "journal head", "no_response": "no answer from the collector", "records": "records"}}
```

`texts` kalitlari: `ok`, `key_changed`, `rollback`, `fork`, `invalid`, `no_response`, `collector`, `records`, `head`. Kommanda qatori muhitdan ustun, muhit esa fayldan ustun. Noma'lum parametrlar yoki matnli kalitlar e'tiborsiz qoldirilish o'rniga xabar bilan guvohni to'xtatadi. Matn hech qachon tasdiqlashga ta'sir qilmaydi: verify.py har bir post oxirida imzolangan tokenni tekshiradi. `--post changes` yoki `problems` bilan joylanmagan tekshiruvlar ham guvoh jurnalida qoladi va `verify.py` ularni hech qachon joylanmagan deb ro'yxatlaydi; boshlang'ich yozuv siyosatni nomlaydi. Har bir tekshiruv jurnalda paydo bo'ladi, shuning uchun kamroq postlar kamroq mustaqil Telegram vaqtlarini anglatadi, tekshiruvlar soni esa kamaymaydi.

Kanal bo'lmasa ham guvoh o'z jurnalini saqlab qoladi. Guvoh kalit barmoq izini (`python -m tgwitness.witness fingerprint`) boshqa joyda saqlang.

## Tasdiqlang

Guvoh tomonidan jurnalini eksport qiling:

```
python -m tgwitness.witness export --out witness.zip
# Docker (add -f deploy/compose/compose.witness.yaml on a witness server):
docker compose exec witness python -m tgwitness.witness export --out /witness/witness.zip
docker compose cp witness:/witness/witness.zip .
```

Keyin istalgan joyda, yig'uvchining imzolangan ZIP-fayli va Telegram Desktop'dan eksport qilingan kanal (*Suhbat tarixini eksport qilish* → JSON `result.json` beradi) yoki uning ommaviy `https://t.me/s/…` sahifasi bilan:

```
python verify.py tgwitness-evidence.zip --fingerprint COLLECTOR_SHA256 \
    --witness witness.zip --witness-fingerprint WITNESS_SHA256 --channel result.json
```

`verify.py` guvoh jurnalini (zanjir va imzolarni) tekshiradi, so'ngra **guvoh ko'rgan har bir sarlavha eksport qilingan jurnalning bir qismi ekanligini** aniqlaydi: hisobdagi yozuv aynan shu xeshga ega bo'lishi kerak. Mos kelmaydigan sarlavha tasdiqlashdan o'tmaydi — jurnal guvoh uni ko'rgandan keyin o'zgartirilgan. Shuningdek, eksportdan keyin ko'rilgan sarlavhalar, guvoh qayd etgan anomaliyalar, muvaffaqiyatsiz javoblar, ushbu eksportda mos tekshiruv nuqtalari mavjud bo'lgan davrlar ("X dan Y gacha guvohlik qilingan") va bo'shliqlar haqida ham xabar beradi. Keyingi tekshiruv nuqtalari ushbu davrlarni kengaytirmaydi. Natijaga oxirgi mos kelgan yozuv raqami va mos keladigan tekshiruv nuqtasiga ega bo'lmagan qolgan yozuvlar soni kiradi. Faqat eksportning o'z kaliti bilan imzolangan javoblar hisobga olinadi: guvoh hech qachon ko'rmagan kalit bilan imzolangan eksport guvohlik qilinmagan deb hisoblanadi va`--fingerprint`siz uning imzolovchisi pinlanmay qoladi. `--channel` bilan har bir imzolangan post guvoh jurnalidagi yozuv bilan yozuvma-yozuv mos kelishi kerak: o'zgartirilgan postlar tasdiqlashni o'tkazmaydi, yo'qolgan postlar ro'yxatga olinadi. Taqdim etilgan Telegram JSON eksportidagi sana — bu imzolangan guvoh tokenidan tashqaridagi tahrirlanadigan metadata. Tokenga mos kelish nashr etish vaqtini tasdiqlamaydi; natija nashr vaqtini tekshirish amalga oshirilmaganini aniq bildiradi.

### Guvohlik qilingan eksport chegarasini talab qiling

Topshirish jarayoniga guvohlik qilingan yakuniy yozuvni kiritish uchun `--require-witness` ni qo'shing:

```
python verify.py tgwitness-evidence.zip --fingerprint COLLECTOR_SHA256 \
    --witness witness.zip --witness-fingerprint WITNESS_SHA256 --require-witness
```

Buning uchun mustaqil ravishda saqlangan guvoh barmoq izi va aynan ushbu eksport oxirida mos keladigan tekshiruv nuqtasi talab etiladi. Faqat avvalgi prefiksni qamrab oladigan tekshiruv nuqtasi yetarli emas. Yig'ishni to'xtating, guvohga yakuniy holatni kuzatishga imkon bering va jurnalga keyingi yozuvlar kiritilmasidan oldin eksport qiling; agar jurnal o'zgarsa, boshqa tekshiruv nuqtasini saqlang va o'sha holatni eksport qiling. Keyingi tekshiruv nuqtasi yolgʻiz oʻzi qisqaroq eksportning yakuniy xeshini tasdiqlay olmaydi. `--channel` ham taqdim etilganda, da'vo qilingan, ammo yoʻqolgan postlar yoki boʻsh moslik toʻplami ushbu qat'iy tekshiruvdan oʻtmaydi. Bayroq qoʻllanilmasa, oddiy yaxlitlik tekshiruvlari guvoh ishtirokisiz yozuvlarni aniqlaydi, ammo aks holda yaxlit arxivni rad etmaydi.

Bu bayroq taqdim etilgan, mahkamlangan guvoh yozuvlari bilan izchillikni ta'minlaydi. Operator guvohning mustaqilligini aniqlashi va uning yozuvlarini alohida saqlashi kerak. Bu xabar haqiqatini, to'liq yig'ilganligini yoki mustaqil ravishda o'lchangan ijro muddatini tasdiqlamaydi.

TgWitness kollektor o'sha paytlarda nima xabar qilganini va keyingi eksportlar shunga mos kelishini ko'rsatadi. Bu kollektor Telegram yetkazgan barcha narsalarni yozib olganini yoki xabar mazmuni rostligini anglatmaydi. Bir xil operator tomonidan bir xil kompyuterda ishlatilgan TgWitness boshqa kishi tomonidan ishlatilganidan zaifroqdir.

Faqatgina oshgan hisob onlayn faqat qo'shib boriladigan uzluksizlikni ta'minlay olmaydi: oflayn solishtirish saqlangan har bir prefiks xeshini to'liq yig'uvchi eksporti bilan moslashtirishi kerak. Witness'ning ishlamay qolishi va nashr etilmasligi oraliqlarni tashqi bog'lanishlarsiz qoldiradi. Saqlangan guvoh jurnaliga qarab yo'qolgan postlar haqida xabar berish mumkin; bir xil operator nazoratidagi kanal ham, server ham o'zgarmas uchinchi tomon arxivi hisoblanmaydi.
