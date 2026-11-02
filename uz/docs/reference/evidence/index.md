# Dalil formati

Canonical page: https://phishdestroy.github.io/TgWitness/uz/docs/reference/evidence/

Imzolangan ZIP tarkibi, yozuv turlari, jarayon kvitansiyalari, odamlar profillari, masofaviy nusxalar va oflayn tekshirish.

Kuzatuv xulosa emas. Jo'natuvchi ID haqiqiy dunyo identifikatori emas. Hisobga ko'rinadigan xizmat yangilanishi manba hisoblanadi; Telegram bu saqlangan yozuvlarni uchinchi tomon tergovchisi uchun kriptografik imzo bilan tasdiqlamaydi.

## Imzolangan nima

| Material | Himoya | Saqlab qo'yish kerak bo'lgan narsalar |
| --- | --- | --- |
| Har bir jurnal kuzatuvi, jumladan operatsion voqealar | Har bir voqea uchun SHA-256 zanjiri va Ed25519 imzosi | `events.jsonl` original, ishonchli kalit izi va saqlangan tekshiruv nuqtasi |
| Dalil ZIP tarkibi | `manifest.sig` kontent fayllarining hashlarini ro'yxatlaydigan kanonik manifestni imzolaydi | To'liq ZIP arxivi, manifesti va imzosi bilan |
| Saqlangan ilovalar | SHA-256 va bayt soni imzolangan `media.saved` voqeasida; fayl xesh imzolangan ZIP manifestida | Tekshirilgan ZIP ichidagi asl baytlar |
| Tekshiruv nuqtasi | Jurnal bo'ylab Ed25519 imzosi, sarlavha xesh, jamoat kaliti va yaratilish vaqti | Mujadala ostidagi o'zgarishdan oldin saqlangan mustaqil nusxa |
| Jo'natish kvitasi | Alohida imzolangan kollektor o'lchovlari; shuningdek imzolangan `process.started` hodisasiga kiritilgan | Qabul qilingan hujjat va unga tegishli jurnal; o'lchovlar o'z-o'zini xabar qilish asosida |
| Mustaqil CSV yoki HTML | Mustaqil kriptografik imzo yo'q; faqat voqea xeshlari yetarli emas | Butunlikni tekshirish uchun tasdiqlangan ZIP ichidagi aniq nusxani ishlating |
| Brauzer tomonidan yaratilgan skrinshotlar, chop etilgan nusxalar yoki PDF | Derivativda TgWitness imzosi yo'q | Asl tasdiqlangan paketni saqlang va uning asosida yaratilgan derivativ qanday tayyorlanganini hujjatlashtiring |

Yig'uvchi har bir eksport formatini yaratishdan oldin jurnal imzolarini tekshiradi. Ushbu manba tekshiruvi alohida yuklab olingan CSV yoki HTML faylda imzo yaratmaydi. Shuningdek, JSONL hodisasi uchun haqiqiy imzo ilova baytlarini taqdim etmaydi yoki butun kuzatilgan jurnalning yetkazilganligini mustaqil ravishda tasdiqlamaydi.

## Tergovni topshirish

1. Holatga oid ma'lumotlarda ish referensiyasi, operator, Telegram hisobidagi raqamli ID, tanlangan manbalar, yig'ish siyosati va yig'ish davrini qayd eting. TgWitness kuzatuvlarni saqlaydi; ishni tayinlash va hibsga olish yozuvlari ilovadan tashqarida boshqariladi. Mo'ljallangan yig'ish sozlamalarini [jonli qabul qilish tartibi](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md) bilan aniqlang.
2. Ishlash maydonining jamoat kaliti barmoq izini uning eksportlariga tayanishdan oldin mustaqil ravishda saqlang. Yig'ish jarayonida imzolangan tekshiruv nuqtalarini yig'uvchidan tashqarida saqlang. To'xtashlar va hisobning ko'rinish chegaralarini qayd eting.
3. **Imzolangan ZIP**-faylni eksport qiling va imzolangan ish jarayoni kvitansiyasini saqlang. Eksport qilingan jurnal chegarasida yoki undan oldin nazorat nuqtasidan foydalaning. Keyingi nazorat nuqtasi avvalgi eksportni juda qisqa deb to'g'ri rad etishi mumkin. Eksportlar panel filtrlaridan qat'i nazar to'liq ish maydoni jurnalini o'z ichiga oladi; materialni ulashishdan oldin ko'rib chiqing.
4. Qabul qiluvchidan ZIP-ni ishonchli nusxa ko'chirish vositasi va mustaqil taqdim etilgan barmoq izi/nazorat nuqtasi yordamida tasdiqlashini so'rang. Ishonchli checkout-dan, Python muhiti yoqilgan holda:

   ```
   python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
   ```

   Muvaffaqiyatli chiqish hisobotlari `key_pinned: true` va `checkpoint_checked: true` bo'ladi, agar ikkala kirish ham taqdim etilgan va qabul qilingan bo'lsa. Verifikatsiya natijasini saqlang.

   ```
   For a handover requiring the final exported record to be witnessed, use
   `--witness witness.zip --witness-fingerprint TRUSTED_WITNESS_SHA256 --require-witness`.
   This refuses an export with an unwitnessed tail. See the
   [witness handover procedure](WITNESS.md#require-a-witnessed-export-boundary).
   ```

   1. Arxivning SHA-256 hashini, eksport chegarasini, uzatish sanasini, yuboruvchi va qabul qiluvchini o'z saqlash yozuvingizga qayd eting. Asl paketni o'z holicha saqlang va nusxalar bilan ishlang. Ilovaning maxfiy ma'lumotlar papkasi (unda hisob sessiyalari va imzolash sirlari ham mavjud) o'rniga dalil fayllarini ulashing. Uzatish uchun eksport parol bilan himoyalangan AES-256 ZIP-faylga joylashtirilishi mumkin. Parol faqat maxfiylikni ta'minlaydi va saqlanmaydi; qabul qiluvchi arxivni chiqaradi va ichidagi imzolangan eksport o'zgarmaganligini tekshiradi.
   2. Agar mustaqil vaqtga bog'lash zarur bo'lsa, [RFC 3161 protseduras](https://phishdestroy.github.io/TgWitness/uz/docs/reference/timestamp/)iga rioya qiling va so'rov, tekshiruv nuqtasi, ishonchli CA ma'lumotlari hamda tasdiqlangan vakolatli javobni saqlang. Faqatgina so'rov tayyorlash vaqt tamg'asini olishga yetarli emas.

Muvaffaqiyatli tekshiruv ishonchli yig'uvchi kaliti va saqlangan chegaraga nisbatan yaxlitlikni tasdiqlaydi. Manba haqiqati, Telegram xabarlarining to'liq yetkazilishi, ishonchli vaqt va qonuniy qabul qilinishi alohida dalillarni talab qiladi. Ushbu versiya jonli Telegram kvalifikatsiyasini yoki mustaqil sud-tibbiyot/xavfsizlik bahosini o'tkazmagan.

Ko'chirilgan yig'uvchi kaliti soxta almashtirilgan jurnalni imzolashi mumkin. Mustaqil saqlangan tekshiruv nuqtasi yoki guvoh yozuvi bilan tekshirish avvalgi prefiks o'zgarganini aniqlaydi; faqat imzo tekshiruvi buni aniqlay olmaydi. Guvox yig'uvchi taqdim etgan narsani tasdiqlaydi, shuning uchun u birinchi tashqi nazorat nuqtasidan oldin yaratilgan soxta yozuvlarning rostligini mustaqil ravishda aniqlamaydi. Bulutga joylashtirish hisobotlari konfiguratsiyani va yig'uvchi tomonidan xabar qilingan o'lchovlarni tekshiradi; ular boshlang'ich sozlash jarayonida shaxsiy kalit hech qachon nusxalanmaganligini aniqlamaydi.

Apprise orqali yuborilgan bildirishnomalar ish maydoni va suhbat nomlari hamda sonini o'z ichiga oladi; o'chirilgan va tahrirlangan xabarlardan qisqa parchalar faqat operator ularni yoqganda (defoltda o'chirilgan) qo'shiladi. Ular qulaylik signali bo'lib, dalil emas: yetkazib berilishi kafolatlanmaydi va faqat jurnal hamda uning imzolangan eksportlari kuzatilgan narsalarni qayd etadi. Ish maydoni proksisi bilan bildirishnomalar bir xil yo'nalishdan foydalanadi; undan foydalana olmaydigan xizmatlar va MTProxy yo'nalishlari rad etiladi.

## Voqealarni kanoniklashtirish

Hash kirish aynan quyidagi maydonlardan iborat:

```
seq, observed_at, source_at, kind, chat_id, message_id, actor_id, payload, previous_hash
```

Python bilan mos keladigan JSON yordamida serializatsiya qiling: UTF-8, tartiblangan ob'ekt kalitlari, ASCII kodlashsiz, ahamiyatsiz bo'shliqlarsiz va NaN/cheksizliksiz:

```
json.dumps(value, ensure_ascii=False, sort_keys=True,
           separators=(",", ":"), allow_nan=False).encode("utf-8")
```

Ushbu baytlarning SHA-256 hash qiymati voqea hashiga aylanadi. Imzo 32 xom hash baytiga Ed25519 algoritmi bo'yicha qo'llanib, keyin base64 kodlanadi. Birinchi previous_hash 64 ta noladan iborat. Ketma-ketlik raqamlari 1 dan boshlanadi va 1 taga oshadi. Barcha voqealar, jumladan operativ voqealar ham, bitta zanjirni baham ko'radi. Takroriy yetkazib berishni bostirish yo'q: takroriy kuzatuvlar alohida kvitansiyalar bo'lib, ular alohida Telegram harakatlari da'vosini anglatmaydi.

Xom Telegram sanalari ISO satrlaridir; binar maydonlar bytes_base64 ob'ektlarini o'z ichiga olgan ob'ektlarga aylanadi. Xabar matni, birliklar, media tavsiflovchilari, javob metadata, reaksiyalar va xizmat harakatlari taqdim etilganda xom xabar metadata'ida saqlanadi.

observed_at — ma'lumot to'plovchining UTC devar soatidir. source_at esa mavjud bo'lganda Telegram taqdim etgan sana hisoblanadi. O'chirish bildirishnomalari aniq o'chirish vaqtini bermaydi, shuning uchun source_at nol bo'lib qoladi. Transport qabul qilish tartibi manba-voqea tartibiga to'g'ri kelmasligi mumkin. Tarix snopshotlari eski manba sanalarini, lekin joriy kuzatuv vaqtlarini ishlatadi.

## Aktyor semantikalari

message.new actor_id xabar jo'natuvchisidir. message.edited bo'yicha tahrir qiluvchi aniqlanmaydi; payload.sender_id kuzatilgan xabar jo'natuvchisini qayd etadi. O'chirish actor_id nol bo'lib qoladi. A'zolik xizmati xabarlari jo'natuvchi va harakat turini saqlab qoladi, har bir olib tashlashni ixtiyoriy tark etishga aylantirmaydi. Xom ishtirokchi yangilanishlari actor_id ni taqdim etilganidek saqlab qoladi. Reaksiya snapshotlari o'zgarish aktyorini ixtiro qilmaydi.

Shaxsiy suhbatlar va oddiy guruhlar uchun o'chirish bildirishnomalari faqat xabar IDlarini o'z ichiga oladi. Ushbu suhbatlar bir hisob bo'ylab yagona ID ketma-ketligini baham ko'radi, shuning uchun ID ushbu hisobdagi bitta xabarni aniqlaydi. Agar shu IDga ega xabar ilgari ushbu jurnalda saqlangan bo'lsa, o'chirish ushbu suhbatda message.deleted sifatida qayd etiladi va payload.chat_resolution nomli metod chaqiriladi. Hech qachon saqlanmagan IDlar esa chat_id bo'lmasdan deletion.unscoped sifatida saqlanadi; hech narsa taxmin qilinmaydi. Kanal va superguruhlar har bir suhbat bo'yicha xabarlarni sanab boradi va shu tarzda hech qachon mos kelmaydi. Agar o'chirilgan xabar kuzatilayotgan akkaunt tomonidan yuborilgan bo'lsa, payload.deleted_message_was_outgoing qiymati true bo'ladi; o'chiruvchi hanuzgacha taqdim etilmaydi.

## Qamrov: uzluksizlik, bo'shliqlar va sezilmagan identifikatorlar

Har bir imzolangan ZIP `coverage.json` ni o'z ichiga oladi, HTML hisobot ham xuddi shu xulosadan boshlanadi va `verify.py` faylga ishonish o'rniga uni `events.jsonl` dan qayta hisoblaydi:

- **X dan Y gacha uzluksiz kuzatiladi.** Davr `observation.started` bilan boshlanadi va pauza, to'xtash, Telegram ulanishining yo'qolishi, tizimdan chiqish, tartibli to'xtashsiz jarayon boshlanishi yoki kuzatuv paytida hech qanday yozuv bo'lmasdan uch daqiqadan ortiq vaqt o'tishi bilan yakunlanadi. (yurak urishlari har daqiqada yozib boriladi, shuning uchun sukut jarayon to'xtaganini, muzlaganini yoki kompyuter uxlab qolganini anglatadi). **Parametrlarda** yurak urishi oralig'i o'zgartirilganda, har bir yurak urishi buni qayd etadi va ruxsat etilgan sukut uch intervalga teng bo'ladi, hech qachon uch daqiqadan kam bo'lmaydi.
- **Bo'shliqlar** davrlar orasidagi vaqtni va sababini ko'rsatadi. Oxirgi yozuvda hali ham ochiq bo'shliq `not_resumed_by_last_record` bilan belgilangan.
- **Xabar IDlari kuzatilmagan.** Kanal va superguruhlarda, chatlardagi xabarlar sonini hisoblashda, kuzatilgan IDlar orasidagi yo'qolgan IDlar diapazonlar sifatida ro'yxatga olinadi. Ular "*kuzatilmagan*" deb qayd etiladi — o'chirib tashlangan, hech qachon yetkazilmagan yoki saqlangan tarixdan tashqarida bo'lgan — lekin hech qachon o'chirib tashlangan deb ko'rsatilmaydi. Shaxsiy suhbatlar va oddiy guruhlar hisob bo'ylab yagona ketma-ketlikni baham ko'radi, shuning uchun u yerdagi bo'shliqlar hech narsani anglatmaydi va ro'yxatga kiritilmaydi.
- Suhbat darajasidagi bo'shliq bildirishnomalari (masalan, Telegram bir kanalda farqni tiklashni so'rashi) eslatma sifatida hisoblanadi; ular global qamrovni to'xtatmaydi.

Qamrov ushbu yig'uvchi nima yozib olganini tasvirlaydi. Bu Telegram uzluksiz davr mobaynida har bir yangilanishni yetkazganining isboti emas.

## Ishlab chiquvchi

Dalillar ZIP-arxivlari, suhbat eksportlari, guvoh jurnallari va shaxsiy profil fayllari bayonotining imzolangan manifesti `producer` ni o'z ichiga oladi: dasturiy ta'minot, versiya, loyiha (PhishDestroy), bosh sahifa va manba ombori. HTML hisobotida ham xuddi shu satr ko'rsatiladi, va `verify.py` uni tekshirgan narsalarning bir qismi sifatida chop etadi. Ushbu maydon mavjud bo'lmasdan oldin yaratilgan arxivlar oldingi holatni tasdiqlaydi va ularning yaratilganligi to'g'risida ma'lumot beruvchi ko'rsatilmaganligi qayd etiladi.

## Foydalanuvchi profillari

Profil fayli (`tgwitness-dossier-v1`, JSON) jurnalga allaqachon kiritilgan yozuvlardan so'rov asosida bitta suhbat uchun tuziladi; Telegramdan hech narsa olinmaydi va profil mazmuni hech qachon jurnalga yozilmaydi (profilni yoqish va o'chirish `dossier.changed` sifatida qayd etiladi). Saqlangan xabarga ega har bir kishi uchun ism va foydalanuvchi nomi tarixi, Telegram belgilari (bot, firibgarlik, soxta, premium, tasdiqlangan, cheklangan, o'chirilgan) xabar saqlangan paytdagi holatga ko'ra, profil mahalliy avatar keshidagi avatarlarning foto IDlari, SHA-256 va sezgir xesh (pHash, `imagehash.phash` bilan mos keladi), shunga o'xshash avatarlar, faoliyat (birinchi va oxirgi xabar, hisoblar, tahrirlangan va o'chirilgan ulashuvlar, UTC soatiga ko'ra xabarlar), kim kimga javob berayotgani, boshqa suhbatlar bu jurnalda shaxs nimalarni yozgani, hamyonlarni (BTC, EVM, TRON, TON, LTC, DOGE, XMR, SOL; Base58Check manzillari checksum-validatsiya qilingan) tilga olgani, telefon raqamlari, foydalanuvchi nomlari va havolalar, jumladan matn ortida yashirilgan havolalar.

Har bir fakt o'z kelib chiqqan jurnal yozuvlarini (`seq`) ro'yxatlaydi va `record_hashes` har bir ko'rsatilgan yozuvning xeshini o'z ichiga oladi. Bayonot ish maydoni kaliti bilan imzolangan:

```
python verify.py tgwitness-dossier-CHAT.json --fingerprint TRUSTED_SHA256 --evidence tgwitness-evidence.zip
```

imzoni tekshiradi, dalillar eksportini o'zi (imzo, xesh zanjiri va fayllar) tasdiqlaydi va har bir havola qilingan yozuv o'sha ish maydonining shu eksportida o'zgarmas holda mavjudligini aniqlaydi. Avatar xeshlari mahalliy keshdan olinganligi bilan belgilangan (jurnal yozuvlari emas). Tilga olishlar naqsh mosligi asosida aniqlanadi — tekshirish uchun yo'l-yo'riq, tasdiqlangan fakt emas. Profil(lar) har bir suhbat bo'yicha yoqiladi, parol bilan himoyalangan AES-256 ZIP fayli sifatida eksport qilinishi mumkin va manbalardan suhbat olib tashlanganda yoki profil o'chirilganda o'chiriladi.

## Mustaqil guvoh

Guvoҳ jurnali (`tgwitness-witness-v1`) va uning kanal postlari `verify.py --witness … --channel …` yordamida eksport qilingan dalillar bilan solishtiriladi; [mustaqil guvoҳga](https://phishdestroy.github.io/TgWitness/uz/docs/reference/witness/) qarang.

## Manifest va tekshiruv nuqtalari

manifest.json format, eksport vaqtini, jamoat kalitini, barmoq izini, jurnal uzunligini, bosh xeshini, doirasini, ishlab chiqaruvchini, cheklovlarni va `manifest.json` hamda `manifest.sig` o'zlari bundan mustasno, har bir kontent a'zosining SHA-256 ko'rsatkichini o'z ichiga oladi. manifest.sig esa kanonik manifest JSON ustidagi base64 Ed25519 imzodir. Verifikator kutilmagan/yetishmayotgan a'zolarni, takroriy nomlarni, shikastlangan fayllarni, uzilgan ketma-ketlik/zanjirni, noqonuniy imzo(lar)ni va taqdim etilgan tekshiruv nuqtasiga nomuvofiqlikni rad etadi. U hech qachon arxiv yo'llarini chiqarib olmaydi. U umumiy e'lon qilingan siqilmagan hajmni 4 GiB gacha cheklaydi;`--max-gib N` esa oshirilgan **Parameters** limiti bilan yaratilgan kattaroq arxivlarni yo'l qo'yadi.

Verifikatsiya kodini ishonchli manba yoki tekshirilgan mustaqil nusxadan oling. Ishonchsiz arxiv ichidagi verifikator — bu arxiv muallifi taqdim etgan ijro etiladigan material; uning mavjudligi portativlik qulayligidir, mustaqil ishonch nuqtasi emas.

Checkpoint ommaviy kalit, jurnal uzunligi, sarlavha xesh va yaratilish vaqtini o'z ichiga olgan bayonotni imzolaydi. Verifikator keyingi arxivda xuddi shu prefiks mavjudligini tekshirishi mumkin. Bahslidirgan o'zgarishdan oldin kollektor tashqarisida checkpoint saqlang: arxiv va checkpoint ustidan nazoratni qo'lga kiritgan hujumchi ikkalasini ham almashtira oladi.

Belgilanmagan kalitdan olingan haqiqiy imzo faqat ichki izchillikni ta'minlaydi. Hatto belgilangan kalit ham yozib olishdan oldin ma'lumot to'plovchi yoki kalit buzilgan bo'lsa, manbaning haqiqiyligini isbotlay olmaydi. Tashqi vaqt belgilash va ishonchli usulda olish alohida talablar hisoblanadi. TgWitness dalil sifatida qabul qilinishini yoki sud-tibbiy ekspertiza sertifikatini kafolatlamaydi.

## Ilovalar

Media/ katalogi ostida fayllar SHA-256 hashiga ko'ra manzillanadi. media.saved hodisasi haesh va bayt uzunligini ma'lum bir xabar hodisasi bilan bog'laydi. Xom fayl nomlari metama'lumot bo'lib, hech qachon mahalliy yo'l bo'lmaydi. Media baytlari asinxron tarzda yuklanadi, shuning uchun darhol o'chirish ularni qayd etilishini to'xtatishi mumkin. To'plamni o'chirib qo'yish, katta hajmli/noma'lum hajmli fayllar, yuklab olishdagi xatoliklar va uzilgan yuklab olishlar natijalar sifatida ko'rinadi. Jarayon qulashi bog'lanmagan qisman fayllarni qoldirishi mumkin; ular eksportga kiritilmaydi.

ZIP eksporti saqlangan media fayllarini ularning nomlari bilan solishtiradi. JSONL, CSV va HTML eksportlari voqea imzolarini tekshiradi, lekin media baytlarini o'z ichiga olmaydi. Qo'shimcha hisobotlar qulaylik uchun mo'ljallangan; events.jsonl voqealarning haqiqiy vakilidir.

## Chidamli yig'ish va jarayon kvitansiyalari (0.2)

Media ish va uning xabar voqeasi bitta tranzaktsiyada yozib qo'yiladi. Ish asl TL xabar tavsiflagichini saqlaydi; imzolangan kuzatuv uning SHA-256, hisob va hajm siyosatini bog'laydi. Tiklash yuklab olishdan oldin bu bog'lanishni tekshiradi. U hech qachon joriy xabarni olib kelmaydi va jimjit ravishda yangiroq ilovani almashtiradi. To'xtab qolgan ishlar qayta urinadi, lekin doimiy xato aniq natija bo'lib qoladi.

Har bir ish maydonining o'z jurnali va imzolash identifikatori mavjud. process.started hodisasi run ID, mahalliy soatlar, bog'liqlik versiyalari, manba-fayl hashlarini, dastlabki hisob/doirani va yozib olish sozlamalarini o'z ichiga oladi. Heartbeatlar run ID, monotonik vaqt va navbat holatini o'z ichiga oladi. Jarayon kvitansiyasi alohida imzolangan bayonot sifatida ham yuklab olinishi mumkin. Fayl o'lchovlari o'z-o'zini xabar qilishga asoslangan bo'lib, ishonchli apparat tasdig'i hisoblanmaydi.

Avtomatik tekshiruv nuqtalari dastur ishga tushirilganda, kuzatuv paytida har besh daqiqada (**Parametrlar → Imzolangan tekshiruv nuqtasi har**) va tartibli to'xtashda mahalliy ravishda saqlanadi. Boshlanishdagi tekshiruv va eksport jurnalni eng so'nggi saqlangan mahalliy tekshiruv nuqtasiga solishtiradi. Bu tekshiruv nuqtasi saqlanib qolganda ma'lumotlar bazasining orqaga qaytishini aniqlashi mumkin; ikkalasini ham nazorat qilayotgan operator esa ularni baribir almashtira oladi. Mustaqil saqlash va tashqi ishonchli vaqt tamg'alari alohida talablar bo'lib qoladi.

Qayta ishga tushirilgandan so'ng saqlangan Telegram yangilanish pozitsiyasi (`catch_up_from`da `observation.started`) tiklanadi va o'tkazib yuborilgan yangilanishlar so'raladi. Davriy qayta tekshirish o'tkazib yuborilgan xabarlar uchun `message.recovered`ni va Telegram saqlangan xabarni qaytarmasa `message.missing_on_recheck`ni qayd etadi; ikkinchisi o'chirish bildirishnomasi emas va o'chiruvchini ham, vaqtni ham ko'rsatmaydi.

### S3da nusxa olish va tiklash

Joydan tashqari nusxa (eksportlar, standart bo'yicha o'chirilgan) jurnal segmentlarini, saqlangan fayllarni, tekshiruv nuqtalarini ularning vaqt tamg'alari bilan va yakunlangan suhbat eksportlarini S3-ga mos omborga yuklaydi, AES-256-GCM bilan shifrlaydi AES-256-GCM bilan yuklashdan oldin ish maydoni seyfida saqlanadigan kalit ostida shifrlanadi; Object Lock saqlash qoidasi bucket uni qo'llab-quvvatlaganda amal qiladi. Yuklab olingan kalitsiz nusxa o'qilmaydi. Tiklash va tasdiqlash uchun `python -m tgwitness.replica restore --key-file KEY.json --out DIR`.

Qayta tiklash bo'sh oddiy katalogni talab qiladi. Yuklab olingan va dekript qilingan obyektlar butun jurnal va har bir saqlangan tekshiruv nuqtasi tasdiqlanguncha shaxsiy vaqtinchalik saqlash joyida qoladi. Xavfsiz bo'lmagan obyekt yo'llari, nomuvofiq segment diapazonlari va tekshiruv nuqtasidan qisqaroq jurnallar rad etiladi; muvaffaqiyatsiz tasdiqlash hech qanday tiklangan fayllarni e'lon qilmaydi. Saqlash tekshiruvlari qaytarilgan Object Lock rejimi va sanani yuklash paytida yuborilgan muddat bilan solishtiradi (bir soniya atrofida xatolik chegarasi). Muddati o'tgan, noto'g'ri yoki qisqartirilgan muddat tasdiqlangan hisoblanmaydi. Statusi esa shu yuklash bosqichi uchun saqlash ma'lumotlari o'qilgan namunaviy obyektni ko'rsatadi.

Ko'chirish jarayoni manzil va shifrlash kalitiga cheklangan. Manzil, bucket yoki prefiksni o'zgartirish mahalliy saqlangan jurnal, media va tekshiruv nuqtalarini shu manzilga to'liq nusxalashni boshlaydi. Eski, cheklanmagan jarayon saqlanib qoladi, lekin yangilanishdan keyin bir marta qayta ijro etiladi. Mahalliy chiqish qutisidan allaqachon olib tashlangan tarixiy suhbat eksportlari avvalgi manzilida qoladi.

Yo'qolgan yoki shikastlangan mahalliy media fayl o'tkazish jarayonidagi xato sifatida qayd etiladi va media kursorini uning oldidagi pozitsiyada ushlab turadi, shuning uchun fayl keyingi o'tkazishda yana sinab ko'riladi; undan keyingi fayllar, tekshiruv nuqtalari va eksportlar esa baribir nusxalanadi. Tiklash tekshiruvlari saqlangan media havolalarini dekriptaj qilingan xeshlar va qayd etilgan o'lchamlarga muvofiq tekshiradi. Uzilgan yuklashlardan kelib chiqqan bir xil ustma-ust keluvchi jurnal segmentlari takrorlanishdan tozalang; ziddiyatli ustma-ust kelishlar rad etiladi. Yuklash jarayonida yaratilgan nazorat nuqtalari ularning qamrab olgan jurnal yozuvlari nusxalanganiga qadar kechiktiriladi, shuning uchun yakunlangan bosqich o'z jurnalidan oldinda nazorat nuqtasini e'lon qilmaydi.

### Streaming eksporti snapshotlari

Streaming eksportlari barqaror SQLite o'qish snapshotidan foydalanadi. Yuklab olish tugagach, uning bosh qismi joriy jonli jurnaldan eski bo'lishi mumkin. Ushbu snapshotdan keyin yaratilgan tekshiruv nuqtasi arxivning qisqaroq ekanligini to'g'ri ko'rsatadi; eksport qilingan prefiksdagi yoki undan oldingi tekshiruv nuqtasi bilan solishtiring, tasodifiy keyingi tekshiruv nuqtasi bilan emas.

## RFC 3161 tayyorgarligi va javobni tasdiqlash (0.2)

Dalil rejimi (defoltda o'chirilgan) har bir imzolangan tekshiruv nuqtasining faqat SHA-256 hashini ro'yxatga kiritilgan RFC 3161 vakolatli organlariga va OpenTimestamps taqvimlariga ish maydoni marshruti orqali yuboradi va hech qachon MTProxy orqali emas. Javoblar `checkpoints/anchors/`da saqlanadi, eksport qilinadi va `verify.py` tomonidan tekshiriladi (`--tsa-ca` TSA imzosini tekshiradi; OpenTimestamps isbotlarini `ots upgrade` va `ots verify` bilan tasdiqlaydi).

Panel canonical checkpoint.json baytlarini, SHA-256 xabar izini va timestamp.tsq, checksums hamda ko'rsatmalardagi tasodifiy nonse-ni o'z ichiga olgan so'rov arxivini tayyorlaydi. Hech qanday tarmoq so'rovi amalga oshirilmaydi. Tayyorlash ishonchli vaqt shtampi hisoblanmaydi.

`python -m tgwitness.anchor verify` ikki marta OpenSSL ts-ni chaqiradi: bir marta tekshiruv nuqtasi baytlari bo'yicha va bir marta asl so'rov bo'yicha. Ishonchli CA fayli aniq ko'rsatilishi kerak; Ilovaga kiritilgan sertifikatlar avtomatik ravishda ishonchli hisoblanmaydi. CLIda so'rovni tekshirish ixtiyoriy bo'lib, shuning uchun nonse tekshirish uchun --request parametrini saqlang va kiritgan holda ishlating. Natija tekshirilgan yoki tekshirilmaganligini ko'rsatadi. Yig'uvchining tekshiruv nuqtasi imzosi va jurnalini ishonchli yig'uvchi barmoq izi bilan alohida tasdiqlash kerak.

Joriy verifikator bekor qilish ma'lumotlarini olmadi va sertifikat muddati tugagach uzoq muddatli arxivni tasdiqlashni amalga oshirmaydi. Imzo tekshiruvining muvaffaqiyatli o'tishi sanali muhr yoki huquqiy qabul qilinish bilan tenglashtirilmasin. Ishlab chiqish jarayonida haqiqiy mustaqil TSA bilan bog'lanilmagan. [Protseduraga](https://phishdestroy.github.io/TgWitness/uz/docs/reference/timestamp/) qarang.
