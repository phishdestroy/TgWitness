# Case Board havolasi

Canonical page: https://phishdestroy.github.io/TgWitness/uz/docs/reference/case-board/

Belgilar, aniq ajratmalar, harakat bo'laklari, muhokamalar, chegaralangan kirish va Case Board tomonidan ishlatiladigan imzolangan izohlar tarixi.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Hujjatlash](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Investigation](https://phishdestroy.github.io/TgWitness/uz/docs/reference/investigation/)

![Investigation](https://phishdestroy.github.io/TgWitness/assets/chapter-investigate.svg)

Case Board tergov guruhiga saqlangan materiallarning umumiy ishlash ko'rinishini taqdim etadi. Kuzatuvni belgilash, aniq parchani ajratib ko'rsatish, bir qator harakatlarni saqlash va uni hamkasblar bilan muhokama qilish mumkin. Kartalar manba havolalarini va imzolangan tahrir tarixini saqlaydi. Guruh izohlari ish maydonida qoladi, ular asl Telegram kuzatuvlaridan alohida ajratib ko'rsatiladi.

[Dalil modeli](https://phishdestroy.github.io/TgWitness/uz/docs/reference/evidence/) · [Kirish](https://phishdestroy.github.io/TgWitness/uz/docs/reference/access/) · [Hisobotlar](https://phishdestroy.github.io/TgWitness/uz/docs/reference/case-reports/)

![Sun'iy tergov lentasi](https://phishdestroy.github.io/TgWitness/assets/case-board.png)

**On this page**

- [Work with a case](https://phishdestroy.github.io/TgWitness/uz/docs/reference/case-board/#work-with-a-case)
- [Permissions](https://phishdestroy.github.io/TgWitness/uz/docs/reference/case-board/#permissions)
- [Stored contracts](https://phishdestroy.github.io/TgWitness/uz/docs/reference/case-board/#stored-contracts)
- [API and exports](https://phishdestroy.github.io/TgWitness/uz/docs/reference/case-board/#api-and-exports)
- [Operating limits](https://phishdestroy.github.io/TgWitness/uz/docs/reference/case-board/#operating-limits)

## Ish bilan ishlash

**Tergovni** oching**→ Ish taxtasi** Standart yoki Mutaxassis rejimida. Til paneldagi sozlamalarga muvofiq bo'ladi. Jurnal yozuvi yoki saqlangan chat xabari yonidagi **To doskasidan** foydalaning, yoki unga e'tiborni qaratib, **B tugmas**ini bosing. Belgi bitta bosishda Kirish qutisiga qo'shiladi. Uning sarlavhasini, yorliqlarini va izohini tahrirlang, yoki uni to'plamga ko'chiring. O'zgartirilgan kartochka imzolangan tahrirni ilova qiladi; uni o'chirish tarixni saqlaydi.

Birinchi ish uchun to'plamni tanlang va bitta savolga javob beradigan yozuvlarni qo'shing. Izohlar bo'limidan foydalanib talqinni ko'rib chiqing, so'ngra **Prezentatsiya** bo'limida kartalar va manba kontekstini bosqichma-bosqich ko'rib chiqing. Yetkazib beriladigan hisobotni tayyorlayotganda [Report studio](https://phishdestroy.github.io/TgWitness/uz/docs/reference/case-reports/)'da Case Board materialini alohida tanlang. Slice saqlash hisobotning ma'lumot filtrlarini avtomatik sozlamaydi.

Saqlangan chat xabaridagi matnni tanlang, **Highlight → board** ni ko'rsatish uchun. Uning rangini tanlang va eslatma qo'shing. Server aniq iqtibos va saqlangan versiyani, jumladan emoji, RTL matn va biriktirish belgilarini tekshiradi. Interfeys tanlovni niqoblangan yoki o'zgartirilgan matn orqali xaritalamaydi.

Bir suhbatdagi ikki yozuvni Shift-bosish orqali ajratib, **ularning orasida Slice** qilishingiz, **vaqt bo'yicha Slice** qilishingiz yoki jurnalning joriy suhbat, davr va voqea-turi filtrlarini saqlashingiz mumkin. Saqlangan slice o'zining haqiqiy predikati (predicate)ga ega: uni Journal'da ochish bir nechta suhbatlar, xabar raqami chegaralari va aktor filtrlarini ham qo'llaydi. **Belgilanma qo'yilganidan beri qo'shilgan yozuvlarni ko'rsatish** keyingi qo'shimchalarni ajratib ko'rsatadi. Journal filtrlarini o'zgartirish bo'lakdan chiqishni ta'minlaydi. Odamlar bo'limidan, "**Ushbu shaxsning harakatlarini bo'laklash"** yozib olingan ijrochi ID'dan foydalanadi; u xabar muallifi xabarni tahrirlagan, o'chirgan yoki unga munosabat bildirgan deb taxmin qilmaydi.

Slice oynasi yaratishga ruxsat berishdan oldin sonlarni oldindan ko'rsatadi. `all` har bir qayd etilgan turni o'z ichiga oladi, jumladan snapshotlar, tahrirlar, o'chirishlar, munosabatlar, a'zolik/xizmat yangilanishlari, o'z harakatlari, tugmalar, media natijalari, tiklangan xabarlar va kelajakdagi voqea turlari. Tanlov saqlangan kuzatuvlarni tasvirlaydi. Noma'lum-chatni o'chirish bildirishnomalari alohida kontekst bo'lib, faqat butun ish maydoniga kirish huquqiga ega bo'lganlarga ko'rinadi va tanlangan chatlardan biriga hech qachon bog'lanmaydi.

To'plamlarga chat doirasi belgilangan. Bo'sh doira butun ish maydonini anglatadi. To'plam o'z doirasidan tashqaridagi kartalarni o'z ichiga ololmaydi; chat bilan cheklangan ishtirokchi kengroq to'plamni o'qiy olmaydi. Kirish qutisi – belgilanmagan kartalar uchun virtual to'plam. Qidiruv va filtrlar faqat ko'rinadigan kartalarni qamrab oladi; iplar va tilga olishlar ota kartaning kirish huquqini meros qilib oladi. O'chirilgan izohlar muhokamada qabr toshiga ega bo'ladi. Ko'ruvchi tarixi qayd etilmaydi.

**Taqdimot** tanlangan to'plamdagi barcha kartalarni ochadi, Card, Source konteksti va Team izohlari ko'rinishlari hamda klaviaturadagi Oldingi/Keyingi boshqaruv tugmalari bilan. U tahrirlash boshqaruv elementlarini taqdim etmaydi. Oddiy oqim sahifalangan; taqdimot ro'yxatni sahifalar bo'yicha yuklaydi va har safar bitta kartaning tafsilotlarini oladi.

## Ruxsatlar

Barcha operatsiyalar `view`, ish maydoni/suhbat doirasi va `board.read` huquqlarini talab qiladi. `board.write` kartalar, izohlar, harakatlar hamda ochish/ko'rib chiqish holatlarini qo'shadi. `board.manage` yig'ishni boshqarish, tasdiqlangan/rad etilgan holatlar hamda boshqalarning kartalarini tahrirlash/o'chirish imkonini beradi. Holat jamoaviy qarordir, kriptografik tekshiruv natijasi emas.

Kirish shakli sozlamalari: Ko'rib chiquvchi = o'qish; Tahlilchi = o'qish/yozish; Operator = o'qish/yozish/boshqarish, ularning mavjud ruxsatlariga qo'shimcha ravishda. Mavjud grantlar yangi huquqlarni jimjit ravishda olmaysdi. Asosiy administrator barcha huquqlarga ega va **"Asosiy administrator"** sifatida post qiladi. Attributlash uchun nomlangan grantlardan foydalaning. Tilga olishlar ro'yxatida faqat to'liq ota kartochkasini o'qish huquqiga ega joriy kirishlar ko'rsatiladi.

A chat uchun grant A+B uchun karta yoki bo'lak ololmaydi, hatto uning ID-sini taxmin qilsa yoki noto'g'ri `target.chat_id` ko'rsatsa ham. Maqsad metama'lumotlari serverdagi imzolangan voqea xeshidan aniqlanadi. Yig'indilar, muhokama sonlari, bog'liq kartalar va jonli bildirishnomalar javobdan oldin filtrlanadi. Eksportlar uchun `export` hamda `board.read` zarur; doska huquqisiz mavjud eksportlovchi jamoa eslatmalarsiz oddiy dalillar arxivini oladi. SSE har bir partiya oldidan amaldagi ruxsatnomalarni qayta tekshiradi.

## Saqlangan shartnomalar

Kuzatuvlar kabi, izohlar ish maydonidagi faqat qo'shib boriladigan SQLite jadvaliga tranzaktsion tarzda yoziladi. `annotations.jsonl` — bu `events.jsonl` bilan bir xil o'qish snapshotidan olingan aniq kanonik eksportdir. Ikkinchi raqobatdosh izoh ombori yo'q va `board.activity` jurnal hodisasi ham mavjud emas.

Har bir satrda aniq:

```
{
  "seq": 1,
  "at": "2026-11-02T14:00:00.000+00:00",
  "access_id": "admin",
  "access_label": "Main administrator",
  "kind": "board.bookmark",
  "payload": {"id": "32 lowercase hex digits", "target": {"event_hash": "64 lowercase hex digits"}},
  "previous_hash": "64 zeroes for the first record",
  "hash": "SHA-256 described below",
  "signature": "base64 Ed25519 signature"
}
```

Yuqoridagi qisqartirilgan misol konvertni ko'rsatadi; haqiqiy yuklamalar ularning model bo'yicha standart qiymatlari va server tomonidan aniqlangan maqsad maydonlarini o'z ichiga oladi. API so'rovi sxemalari [`tgwitness/schemas`](https://github.com/phishdestroy/TgWitness/blob/main/tgwitness/schemas/board-bookmark.json) ostida joylashgan bo'lib, ular ijro vaqtidagi Pydantic modellari asosida `python tools/build_board_schemas.py` orqali yaratiladi. Qo'shimcha so'rov maydonlari rad etiladi. IDlar kiritilmagan taqdirda server tomonida yaratiladi. Mualliflik, vaqt, snapshot va imzo chaqiruvchi tomonidan taqdim etilmaydi. Grant IDlari Access-ning mavjud 16-hex formatiga mos keladi; karta IDlari 32 hex.

Standart JSON – bu UTF-8, tartiblangan ob'ekt kalitlari, tokenlar orasida bo'shliq yo'qligi, eskap qilinmagan Unicode va NaN/cheksizliklar yo'qligi. Izoh xesh qiymati – bu `format: "tgwitness-annotations-v1"` va barcha yetti konvert maydonlarini `previous_hash`gacha o'z ichiga olgan standart ob'ektning SHA-256 xeshidir. Ushbu format tegi uning xesh domenini kuzatuvlardan ajratadi. Imzo 32 xom hash bayt ustida Ed25519 algoritmi bo'yicha yaratiladi. Ketma-ketlik 1 dan boshlanadi. Tahrirlar karta ID-sini saqlab qoladi va oldingi annotatsiya hashiga `supersedes` so'zini qo'shadi; ular chat doirasini o'zgartira olmaydi. Ko'chirishlar, holatlar va olib tashlash alohida yozuvlardir. SQLite jadvali UPDATE va DELETE operatsiyalarini rad etadi.

`case-board.json` fayli `{statement, signature}` ni o'z ichiga oladi. Kanonik bayonot ish maydoni kaliti bilan imzolangan bo'lib, quyidagilarni o'z ichiga oladi: `format: "tgwitness-case-board-v1"`, `public_key`, `created_at`, `journal_head`, `meaning` va `state`. Holat deterministik qayta ijro etishdan iborat: `annotations_head`, tartibli `items` massiv (to'plamlar, kartochkalar, izohlar, jumladan bekor qilinganlar) va `status_history`. Elementlar o'zlarining oxirgi annotatsiya xeshini, tartibini, muallifini va vaqtini, shuningdek, asl yaratuvchini va yaratilgan vaqtini qayta ko'rib chiqishlar davomida saqlab qoladi. Qayta ijro etish qayta ko'rib chiqishlarni, ota-onalarni, kollektsiya havolalarini va takroriy harakat IDlarini tekshiradi. `manifest.json` va yangi tekshiruv nuqtalari ham `annotations_head`ni bog'laydi. Qisqartirish yoki nusxa olingan imzo kaliti bilan qayta yozishni aniqlash uchun tekshiruv nuqtasini mustaqil ravishda saqlang.

### Matn versiyalari

`range.start` nolga asoslangan Unicode kod nuqtasi ofseti, `length` ijobiy kod nuqtasi soni, va `quote` maqsadli voqeadagi `payload.text` yoki `payload.caption` ning aniq substringiga teng bo'lishi kerak. Hech qanday NFC/NFKC, katta-kichik harflarni birlashtirish yoki grafema normallashtirish qo'llanilmaydi. Python satr kesmalari va JavaScript `Array.from(text)` bir xil indekslashni amalga oshiradi. Belgilar va ZWJ emojilarini birlashtirish bir nechta kod nuqtalarini egallashi mumkin. `range.version` maqsadli voqea xeshidir, joriy xabar versiyasi yoki Telegramning UTF-16 birlik ofseti emas. Keyingi tahrirlar hech qachon avtomatik ravishda ajratmani ko'chirib qo'ymaydi.

### Shaxsiyat va vaqtni bo'laklarga ajrating

`query` aniq bir `chat_id` yoki bo'sh bo'lmagan `chat_ids`, ixtiyoriy ichiga oluvchi `from`/`to`, ichiga oluvchi xabar-ID chegaralari (faqat bitta chat uchun), `kinds: "all"` yoki aniq/prefix wildcard turlari, aniq `actors`, `search`, `hide_system` va `include_unscoped` ni qabul qiladi. Journal tur guruhlari o'zlarining aniq predikatlariga kengaytiriladi. Qidiruv jurnalning NFC/case-folded yuklamasini imzolangan manba matnini o'zgartirmay qidiradi. Sana va vaqt zonasi talab qilinadi va UTC ga muvofiqlashtiriladi. Sanalar **observed_at ni** filtrlaydi. Telegramning `source_at` alohida ko'rsatiladi. Manba vaqti ko'rsatilmagan o'chirish uchun ixtiro qilingan o'chirish vaqti mavjud emas. Vaqt oralig'idan tashqarida kuzatilgan kechikgan yozuv unga kiritilmaydi; message-ID bo'lagi o'sha xabar IDlari uchun keyingi o'chirishni o'z ichiga olishi mumkin.

`snapshot` yaratish vaqtini, jurnal ketma-ketligi/hash chegarasini, mos kelish sonini, birinchi/oxirgi ketma-ketlikni va `result_hash` ni belgilaydi. Oxirgi qiymat leksikografik tartibda saralangan mos keluvchi voqea hashlarining UTF-8 kanonik JSON massivining SHA-256 hashidir, bo'sh bo'lak uchun `[]` ham kiritilgan. U shuningdek aniq turlar soni va 24-bo'limli kuzatuv vaqtining kichik nusxasini o'z ichiga oladi. Bir bo'lak so'rovni saqlaydi, manba yozuvlarining takrorlarini emas. Eksportda `board/slices/<id>.json` hozirgi hashlar va qo'shilgan/o'chirilgan ketma-ketliklarni ro'yxatlaydi. Verifikator avval yaratilish chegarasida asl natijani, keyin esa joriy natijani qayta tiklaydi. Qo'shilgan yozuvlar o'zgarish hodisasi sifatida qayd etiladi. Asl voqeani o'chirish o'zgarmas dalillar zanjirini buzadi; u oddiy bo'lakdan o'chirish kabi jim qabul qilinmaydi.

Reaksiya snapshotlari yaqinda ishtirok etgan aktyorlar ro'yxatini to'liq aks ettirmaydi. Explorer bir xil chat/xabarning yonma-yon snapshotlarini, jumladan kesimdan tashqaridagi avvalgi snapshotni solishtiradi va **kuzatuvlar orasidagi** umumiy son o'zgarishlarini hisobot qiladi. Yaqinda ishtirok etgan aktyorlarning yo'qolishi reaksiya o'chirilganligini anglatmaydi. Birinchi snapshotda ilgari holat aniqlanmagan. Aktsyor kuzatuvlari ular taqdim etilgan snapshotga tegishli bo'lib qoladi, ixtiro qilingan harakat vaqtiga emas.

## API va eksportlar

`GET /api/board` collection/chat/author/label/state/from/to/q/kind/comments, offset/limit va newest/oldest tartibni qabul qiladi. `GET /api/board/card/{id}` card, source preview, thread, status history va bog'liq kartalarni qaytaradi. Ishtirokchilar subyo'li mos keladigan tilga olish variantlarini qaytaradi. `POST /api/board/{bookmark|highlight|slice|collection|comment|status|move|remove}` yozuvni ilova qiladi. `POST /api/board/slice-preview` so'rovni hisoblaydi. Bo'lak yozuvlari `GET /api/board/slice/{id}/records` bo'yicha sahifalangan; qayta hisoblash har doim joriy barqaror o'qish snapshotidan foydalanadi. Jonli `/api/stream` jurnal kursorlaridan alohida, yuk bo'lmagan `board` bildirishnomalarini chiqaradi.

`GET /api/board/export` imzolangan hujjatni qaytaradi. Chatga cheklangan kirish aniq belgilangan imzolangan **oshkor etish**ni oladi, hech qachon boshqa chatning izohlari yoki to'liq zanjirni emas. To'liq dalil ZIP-fayllari `annotations.jsonl`, imzolangan `case-board.json` va slice JSON ilovalarini o'z ichiga oladi. HTML/PDF/JSON hisobot sozlamalari hech qanday doska, muhokamasiz belgilamalar/bo'laklar yoki izohli kartochkalarni tanlash imkonini beradi. Bo'lim jamoa fikrlarini kuzatuvlardan aniq ajratadi. Hisobot ma'lumotlari filtrlari o'qiladigan eslatmalarni ham cheklaydi; dalillar ZIP-faylidagi to'liq imzolangan manba fayllari esa to'liq saqlanadi.

`GET /api/board/slice/{id}/export` imzolangan `tgwitness-board-selection-v1` JSON parchasi hosil qiladi; `?format=csv` mustaqil imzosiz qulay jadval hosil qiladi. JSON va ZIPni saqlang:

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_KEY_SHA256 --board
python -m tgwitness.verify board-slice.json --evidence evidence.zip --fingerprint TRUSTED_KEY_SHA256
python -m tgwitness.verify case-board.json --evidence evidence.zip --fingerprint TRUSTED_KEY_SHA256
```

Selection check imzolangan bayonotni, aniq manba yozuvlarini va so'rovning belgilangan chegaradagi to'liqligini tasdiqlaydi. Dalil ZIP yangilanishi mumkin, lekin o'sha prefiksni o'z ichiga olishi shart. Bog'lanmagan maqsad aniq xabar qilinadi. Boshqa original slice snapshot, o'zgartirilgan izoh, mos kelmaydigan qayta ijro holati yoki o'zgartirilgan manba muvaffaqiyatsiz bo'ladi. Eskirgan arxivlar annotatsiyalarsiz mavjud tekshirish xulq-atvorini saqlab qoladi.

Topshirish bo'yicha standart sozlama – **"Kiritilmasin"**. Ochiq kiritish allaqachon minimallashtirilgan yozuvlar orqali kartalarni o'tkazadi, kirib bo'lmaydigan/chetda qoldirilgan maqsadlarni o'tkazmaydi, manba matni minimallashtirilgan qaydlarni yashiradi, jamoa matnini bir xil tilga olish/aloqa qoidalari bilan tozalaydi va ixtiyoriy ravishda tergovchi yorliqlarini metama'lumotlarda va eslatmalardagi ma'lum uchrashuvlarda R01, R02… bilan almashtiradi. `annotations.jsonl`ning asl nusxasi oshkor etilmaydi. Imzolangan `tgwitness-case-board-handover-v1` yon fayli va hisobotda bir xil qisqartirilgan material mavjud. Slice sonlari faqat oshkor qilingan yozuvlarni tasvirlaydi, asl snapshot/so'rov ijrochisi tafsilotlari esa yashiriladi. Minimizatorga noma'lum bo'lgan erkin matndagi nomlar ham oddiy topshirishlarda bo'lgani kabi ko'rib chiqishni talab qiladi. Ushbu hosil qilingan versiya qizil chiziq tortilgandan so'ng asl annotatsiya imzolarini saqlab qolishni da'vo qilmaydi.

## Ishlash chegaralari

Parametrlarga 10 000 kartochka va 50 000 izoh uchun yumshoq limitlar, 5 000 yozuvgacha bo'lgan slice sahifasi va media-ko'rinishni boshqarish kiradi. Yumshoq limitlar tarixni o'chirmasdan ogohlantiradi. Feed sahifalari eng ko'pi bilan 200 kartadan iborat. Alohida JSON parchalari 64 MiB bilan cheklangan; so'rovni toraytiring yoki katta material uchun imzolangan ZIP-fayldan foydalaning. Alohida tekshiruvchi izohlarni qayta ijro etishni 256 MiB bilan cheklaydi. Case Board tomonidan hech qanday tashqi izoh bildirishnomalari yoqilmagan yoki amalga oshirilmagan.

Ushbu xususiyatning avtomatlashtirilgan qabul qilishi saqlash, kirish, renderlash va eksportni tekshirish uchun badiiy ma'lumotlar va simulyatsiya qilingan Telegram transportidan foydalanadi. Dalillar tekshiruvi doirasini ko'rish uchun [tasdiqlash doirasiga](https://phishdestroy.github.io/TgWitness/uz/docs/reference/evidence/#verification-scope) qarang.
