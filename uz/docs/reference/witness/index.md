# Telegram · Mustaqil guvoh

Canonical page: https://phishdestroy.github.io/TgWitness/uz/docs/reference/witness/

O'z kaliti va botiga ega Witnessni ishga tushiring, imzolangan tekshiruv nuqtalarini kanalga joylashtiring va eksportlarni ularga solishtiring.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Hujjatlash](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Dalil va tasdiqlash](https://phishdestroy.github.io/TgWitness/uz/docs/reference/evidence/)

![Dalil va tasdiqlash](https://phishdestroy.github.io/TgWitness/assets/chapter-evidence.svg)

[Eksport va tekshirish](https://phishdestroy.github.io/TgWitness/uz/docs/reference/evidence/) · [Yuqori ishonchlilik](https://phishdestroy.github.io/TgWitness/uz/docs/reference/high-assurance/) · [Panel bo'yicha qo'llanma](https://phishdestroy.github.io/TgWitness/uz/docs/reference/panel/#extras)

Guvox imzolangan tekshiruv nuqtalarini yig'uvchidan alohida saqlaydi. U yig'uvchining imzosi va jurnal uzluksizligini tekshiradi, natijani o'z kaliti bilan imzolaydi va Telegram kanalida e'lon qiladi. Uni yig'uvchining guvoxlik oxirgi nuqtasiga faqat o'qish huquqi bilan alohida serverda ishga tushiring.

Oqim sxemasi · Yig'uvchi → Guvoh (imzolangan tekshiruv nuqtasi: yozuvlar soni + sarlavha xesh); Guvoh → Witness jurnali, o'z kalitingiz; Guvoh → Telegram kanali (o'z boti orqali imzolangan post); Dalil ZIP → verify.py; Witness jurnali, o'z kalitingiz → verify.py; Telegram kanali → verify.py (Telegram Desktop eksporti yoki t.me/s sahifasi) · Yig'uvchi · Guvoh · Witness jurnali, o'zkalitingiz · Telegram kanali · Dalil ZIP · verify.py · imzolangan tekshiruv · nuqtasi: yozuvlar soni + · sarlavha xesh · o'z boti orqali imzolangan · post · Telegram Desktop eksporti · yoki t.me/s sahifasi

**Diagramma matn sifatida**

1. Yig'uvchi → Guvoh (imzolangan tekshiruv nuqtasi: yozuvlar soni + sarlavha xesh)
2. Guvoh → Witness jurnali, o'z kalitingiz
3. Guvoh → Telegram kanali (o'z boti orqali imzolangan post)
4. Dalil ZIP → verify.py
5. Witness jurnali, o'z kalitingiz → verify.py
6. Telegram kanali → verify.py (Telegram Desktop eksporti yoki t.me/s sahifasi)

**Ushbu sahifada**

- [Guvoh nimani oladi va nimani olmaydi](https://phishdestroy.github.io/TgWitness/uz/docs/reference/witness/#what-the-witness-gets-and-what-it-does-not)
- [U nima tekshiradi va qayd etadi](https://phishdestroy.github.io/TgWitness/uz/docs/reference/witness/#what-it-checks-and-records)
- [Witnessni ishga tushiring](https://phishdestroy.github.io/TgWitness/uz/docs/reference/witness/#run-a-witness)
- [Bir nechta ish maydonchalari uchun ommaviy isbot sahifasi](https://phishdestroy.github.io/TgWitness/uz/docs/reference/witness/#public-proof-page-for-several-workspaces)
- [Tasdiqlang](https://phishdestroy.github.io/TgWitness/uz/docs/reference/witness/#verify)

## Guvoh nimani oladi va nimani olmaydi

| Guvohda | Guvoh hech qachon |
| --- | --- |
| Bir ish maydoni uchun faqat o'qish huquqiga ega **guvoh tokeni** | Yig'uvchining Telegram sessiyasi yoki API ma'lumotlari |
| O'zining Ed25519 kaliti va jurnali | Yig'uvchining ombori, imzolash kaliti yoki panel tokeni |
| O'z Telegram bot tokeni | Xabar mazmuni: sarlavha yozuvlar soni va xesh |

Token **Extras → Mustaqil guvoh** bo'limida yaratiladi, bir marta ko'rsatiladi va faqat SHA-256 sifatida saqlanadi. U aniq bir endpointni ochadi, `GET /api/witness/head`, u yangi imzolangan tekshiruv nuqtasini, shuningdek imzolangan, kontentsiz to'plam hisoblagichlari va operatsion holatini qaytaradi. U panelni ocholmaydi, xabar kontentini o'qiy olmaydi yoki sozlamalarni o'zgartira olmaydi va panel tokeni u yerda qabul qilinmaydi. Tokenni shu sahifada bekor qiling. Yig'uvchi qayd etadi yangi guvoh kaliti tekshirishni qachon boshlaganini (`witness.seen`) va har bir token bo'yicha oxirgi tekshiruvni ko'rsatadi; 2,5 intervaldan ortiq tekshirilmagan guvoh kechikkan deb belgilangan.

Yangi guvohlar har bir so'rov bo'yicha tasodifiy chaqiriq yuboradilar; capture bayonoti uni kollektor imzosining ostida aks ettiradi. Hisoblagichlar aniq nazorat nuqtasiga bog'langan va imzolangan guvoh postlariga kiritilgan. Meros boshliqlar mustaqil guvoh tomonidan qabul qilinishda davom etadi. Jurnal hajmining o'sishi alohida yangi xabar sifatida hisobga olinmaydi.

## Nimani tekshiradi va qayd etadi

Har bir intervaldan (o'rnatilgan bo'yicha 10 daqiqa) guvoh:

1. bosh qismni o'zi oladi (yig'uvchi uni sura olmaydi yoki o'tkazib yubora olmaydi);
2. yig'uvchining imzosini, mahkamlangan yig'uvchi kalitini (`--collector-fingerprint` yoki birinchi ko'rilgan kalit), kamaymaydigan hisobni va o'zgarmagan hisobda o'zgarmagan boshni tasdiqlaydi. Merkle kiritish va moslik isbotlari o'sib borayotgan jurnal saqlangan tekshiruv nuqtasini kengaytirishini tasdiqlaydi. Uzluksizlik isbotlari bir marta qo'llangach, ularni olib tashlash rad etiladi;
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

Paneldagi **Extras → Mustaqil guvoh → Sozlashni** oching. Uch bosqichda faqat o'qish huquqi, kanal va interval sozlanadi, so'ngra guvoh ishga tushiriladi. Nashr siyosati, ixtiyoriy HTTP/SOCKS5 proksi va maxsus Bot API manzili **Kengaytirilgan sozlamalarda** joylashgan. Forma yuklab olinadi `witness.json` ushbu ish maydonining yig'uvchi kaliti (collector key) belgilangan holda. Yangi yaratilgan faqat o'qish uchun mo'ljallangan tokenni "**Save access file** as" orqali yuklab oling. `witness-token.txt`; uni va bir `bot-token.txt`host'da yaratilgan JSON yoniga joylang. Collector bot tokenini hech qachon olmaydi. Yuklab olish xizmatni ishga tushirmaydi yoki xabar e'lon qilmaydi. Hech qanday joylashtirilgan loyiha guvohi avtomatik ravishda ro'yxatdan o'tkazilmaydi.

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

### Discordga e'lon qiling

Guvoh Telegram o'rniga Discord kanaliga post qilishi mumkin. Discord'da **Kanalni tahrirlash → Integratsiyalar → Webhooks bo'limini** oching, webhook yarating va uning URL manzilini nusxalang. Panelda 2-qadamda **Discord webhook · o'zingizning kanalni** tanlang. Guvoh mezbonida URL manzilini sifatida saqlang `discord-webhook.txt` yonida `witness.json`; u hech qachon yig'uvchiga yetib bormaydi.

```
python -m tgwitness.witness run --collector https://your-collector.example.org \
    --token-file witness-token.txt --discord-webhook-file discord-webhook.txt
```

Guvohda faqat bitta nashriyotchi bo'ladi: Telegram kanali yoki Discord webhook, ikkalasi ham emas. Postlar bir xil imzolangan bayonotni o'z ichiga oladi va hech kimga ping yubora olmaydi. Discord'ning 2 000 belgidan uzun post qisqa satr bilan almashtiriladi, to'liq tekshiruv esa ilova qilingan holda `witness-check.txt`. Har bir post ID quyidagicha qayd etiladi `witness.posted`. `verify.py --channel`Telegram kanal eksportlarini o'qiydi, shuning uchun Discord uchun guvoh jurnalini saqlang: u har bir tekshiruvni o'z ichiga oladi.

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

Yig'uvchi manzili, tokenlar va kanal keladi `--collector`, `--token` yoki `--token-file`, `--bot-token` yoki `--bot-token-file`, `--discord-webhook-file` va `--channel`, yoki `_COLLECTOR`, `_TOKEN`, `_TOKEN_FILE`, `_BOT_TOKEN`, `_BOT_TOKEN_FILE`, `_DISCORD_WEBHOOK_FILE` va `_CHANNEL`, bu jarayonlar ro'yxatidan sirlarni yashiradi.

Konfiguratsiya fayli opsion nomlarini tirelar bilan, shuningdek `texts` ni ishlatadi, u kanal postlaridagi so'zlarni almashtiradi:

```
{"collector": "https://your-collector.example.org", "token_file": "witness-token.txt",
 "bot_token_file": "bot-token.txt", "channel": "@your_witness_channel",
 "interval": 5, "timeout": 30, "post": "changes", "title": "Partner witness",
 "texts": {"ok": "journal head", "no_response": "no answer from the collector", "records": "records"}}
```

`texts` kalitlari: `ok`, `key_changed`, `rollback`, `fork`, `invalid`, `no_response`, `collector`, `records`, `head`. Kommanda qatori muhitdan ustun, muhit esa fayldan ustun. Noma'lum parametrlar yoki matnli kalitlar e'tiborsiz qoldirilish o'rniga xabar bilan guvohni to'xtatadi. Matn hech qachon tasdiqlashga ta'sir qilmaydi: verify.py har bir post oxirida imzolangan tokenni tekshiradi. `--post changes` yoki `problems` bilan joylanmagan tekshiruvlar ham guvoh jurnalida qoladi va `verify.py` ularni hech qachon joylanmagan deb ro'yxatlaydi; boshlang'ich yozuv siyosatni nomlaydi. Har bir tekshiruv jurnalda paydo bo'ladi, shuning uchun kamroq postlar kamroq mustaqil Telegram vaqtlarini anglatadi, tekshiruvlar soni esa kamaymaydi.

Kanal bo'lmasa ham guvoh o'z jurnalini saqlab qoladi. Guvoh kalit barmoq izini (`python -m tgwitness.witness fingerprint`) boshqa joyda saqlang.

## Bir nechta ish maydonchalari uchun ommaviy tasdiqlash sahifasi

`python -m tgwitness.proof` bir vaqtning o'zida 32 tagacha ish maydonini kuzatadi va har birining so'nggi imzolangan tekshiruvini o'z ichiga olgan faqat o'qish uchun mo'ljallangan sahifani taqdim etadi. Har bir ish maydoni ma'lumotlar papkasi ostida o'z guvoh kaliti va jurnalini hamda biriktirilgan to'plovchi kalitni oladi; Telegram kanaliga post qilish har bir ish maydoni uchun ixtiyoriy hisoblanadi. [proof.config.](https://github.com/phishdestroy/TgWitness/blob/main/deploy/proof.config.example)example-dan boshlang:

| Maydon | Ma'no |
| --- | --- |
| `title` | Sahifa sarlavhasi, 1–100 belgilar |
| `data_dir` | Guvoh kalitlari va jurnallari, faylga nisbatan; standart `proof-data` |
| `interval`, `timeout` | Tekshiruvlar orasidagi daqiqalar (1–1440, standart 5); kutish soniyalari (5–600, standart 20) |
| `workspaces[].id`, `label` | Qisqa kichik harfli taxallus va ko'rsatilgan nom |
| `workspaces[].collector` | Yig'uvchi manzili; boshqa ish maydonchalari bilan tugaydi `/profiles/<workspace ID>` |
| `workspaces[].collector_fingerprint` | Talab qilinadi, har bir ish maydoni uchun turlicha |
| `workspaces[].token_file` | Ushbu ish maydonining faqat o'qish uchun mo'ljallangan guvoh tokeni bilan fayl |
| `workspaces[].channel`, `bot_token_file` | Ixtiyoriy, birgalikda: har bir tekshiruvni kanalga joylashtirish |
| `workspaces[].proxy`, `bot_api` | Ixtiyoriy yo'nalish va Bot API manzili |

```
python -m tgwitness.proof --config proof.json --check-config
python -m tgwitness.proof --config proof.json --host 127.0.0.1 --port 8790
```

Birinchi buyruq fayl va token fayllarini ulanishni ochmasdan tekshiradi. Sahifa faqat GET va HEAD so'rovlariga javob beradi:

- `/` har bir ish maydonini ko'rsatadi; 2.5 intervallarni tekshirmasdan qoldirilgan ish maydoni eskirgan deb belgilangan.
- `/api/proof` JSON kabi bir xil natijani qaytaradi.
- `/api/proof/<id>` so'nggi imzolangan bayonotni yuklab oladi (`tgwitness-public-proof-v1`): guvoh yozuvi raqami va xesh, holat, biriktirilgan yig'uvchi kaliti, tekshiruv nuqtasi, yig'ma hisoblagichlar va kanal postining muvaffaqiyatli ekanligi, ushbu ish maydonining guvoh kaliti bilan imzolangan.
- `/healthz` ish maydonining monitori to'xtaganida 503-javobni qaytaradi.

Sahifaga [Caddyfile.proof.example](https://github.com/phishdestroy/TgWitness/blob/main/deploy/Caddyfile.proof.example) kabi o'z host nomini bering. Tekshirish uchun ish maydonining guvoh jurnalini eksport qiling `python -m tgwitness.witness export --data-dir proof-data/<id> --out witness.zip` va uni quyida tavsiflangandek ishlating.

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

Witness jurnalini va uning biriktirilgan kalitini alohida saqlang. Onlayn tekshiruvlar nazorat nuqtalari o'rtasidagi uzluksizlikni tasdiqlaydi; oflayn tekshiruv esa saqlangan har bir nazorat nuqtasini eksport bilan solishtiradi. Uzluksizlik isbotlarisiz eski boshqaruv elementlari oflayn solishtirishni saqlab qoladi va onlayn uzluksizlik tekshiruvisiz hisobotga kiritiladi. Hisobotda guvohning ishlamagan vaqtlari va intervallar bo'yicha muvaffaqiyatsiz nashrlar ko'rsatiladi.

### Kundalik muhrlar va mavjud bo'lmagan timestamp taqvimlari

Guvoh avvalgi UTC kunining jurnal chegarasini muhrlaydi va imzolangan muhrning xeshini OpenTimestampsga yuboradi. Taqvim topshirig'i dalillarni kutmoqda; faqat mustaqil ravishda tekshirilgan Bitcoin majburiyatlari verifikator tomonidan tasdiqlanadi.

Agar barcha taqvimlar ishdan chiqsa, imzolangan muhr va muvaffaqiyatsiz urinish jurnalda qoladi. Soatlik texnik xizmat ko'rsatish pasporti ushbu dastlabki yozuvni qayta sinab ko'radi, jumladan qayta ishga tushirish yoki sana o'zgarishi holatlarida ham. U eng ko'pi bilan32ta muhrni skanerlaydi, eng ko'pi bilan ikkita yetishmayotgan topshiruvni yuboradi va har bir urinishda qayta urinishlarga eng ko'pi bilan 60 soniya sarflaydi. Doimiy kursor eski muhrlar bo'ylab aylanib turadi. Saqlangan topshiruvlar mavjud isbotni yangilash yo'lini kuzatadi.

Qayta urinish muhrni qayta yozmaydi, uning asl sanasini o'zgartirmaydi yoki kalendar uni erta qabul qilganini da'vo qilmaydi. Keyingi Bitcoin majburiyati keyingi tashqi tasdiq bo'lib qoladi. Yetishmayotgan isbotlar `none` bo'lib qoladi; kutayotgan isbotlar esa verifikator ularni mustaqil tekshirgunga qadar `pending` bo'lib qoladi.
