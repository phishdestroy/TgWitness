# Dalil formati

Canonical page: https://phishdestroy.github.io/TgWitness/uz/docs/reference/evidence/

Imzolangan ZIP tarkibi, yozuv turlari, jarayon kvitansiyalari, odamlar profillari, masofaviy nusxalar va oflayn tekshirish.

TgWitness hisobga ko'rinadigan Telegram kuzatuvlarini imzolangan jurnalda saqlaydi. Qabul qiluvchilar saqlangan yozuvlar, ilovalar va hisobotlarni ishonchli yig'uvchi kalitiga nisbatan tekshirib, so'ng jurnalni mustaqil saqlangan nazorat nuqtasiga solishtirishlari mumkin. Ushbu sahifa formatlar, tekshiruvlar va topshirish uchun saqlanishi kerak bo'lgan materiallarni tasvirlaydi.

## Imzolangan nima

| Material | Himoya | Saqlab qo'yish kerak bo'lgan narsalar |
| --- | --- | --- |
| Har bir jurnal kuzatuvi, jumladan operatsion voqealar | Har bir voqea uchun SHA-256 zanjiri va Ed25519 imzosi | `events.jsonl` original, ishonchli kalit izi va saqlangan tekshiruv nuqtasi |
| Dalil ZIP tarkibi | `manifest.sig` kontent fayllarining hashlarini ro'yxatlaydigan kanonik manifestni imzolaydi | To'liq ZIP arxivi, manifesti va imzosi bilan |
| Saqlangan ilovalar | SHA-256 va bayt soni imzolangan `media.saved` voqeasida; fayl xesh imzolangan ZIP manifestida | Tekshirilgan ZIP ichidagi asl baytlar |
| Tekshiruv nuqtasi | Jurnal bo'ylab Ed25519 imzosi, sarlavha xesh, jamoat kaliti va yaratilish vaqti | Mujadala ostidagi o'zgarishdan oldin saqlangan mustaqil nusxa |
| Jo'natish kvitasi | Alohida imzolangan kollektor o'lchovlari; shuningdek imzolangan `process.started` hodisasiga kiritilgan | Qabul qilingan hujjat va unga tegishli jurnal; o'lchovlar o'z-o'zini xabar qilish asosida |
| O'qiladigan hisobotlar: `report.html` va uning bo'laklari, `report.json`, `report.pdf`, `chat.pdf` | Har bir faylning mazmuni bo'yicha Ed25519 muhri; PDF shuningdek standart PDF imzosi ham mavjud (qarang [o'qiladigan hisobotlar](https://phishdestroy.github.io/TgWitness/uz/docs/reference/evidence/#readable-reports)) | Qabul qilingan fayl va ishonchli kalit barmoq izi; u tasvirlaydigan ZIP |
| Mustaqil CSV | Mustaqil kriptografik imzo yo'q; faqat voqea xeshlari yetarli emas | Butunlikni tekshirish uchun tasdiqlangan ZIP ichidagi aniq nusxani ishlating |
| Brauzer tomonidan yaratilgan skrinshotlar, chop etilgan nusxalar yoki PDF | Derivativda TgWitness imzosi yo'q | Asl tasdiqlangan paketni saqlang va uning asosida yaratilgan derivativ qanday tayyorlanganini hujjatlashtiring |

Yig'uvchi har bir eksport formatini yaratishdan oldin jurnal imzolarini tekshiradi. O'qiladigan HTML va PDF hisobotlari o'z muhrlariga ega; mustaqil CSV imzolangan ZIP tarkibida tekshiriladi. Ilovaga tegishli baytlar va manifestni saqlash uchun ZIP-ni saqlang, shuningdek jurnalni avvalgi chegaraga nisbatan tekshirish uchun alohida tekshiruv nuqtasini yarating.

## Tergovni topshirish

1. Holat yozuvlaringizga ish bo'yicha ma'lumotnoma, operator, Telegram hisobidagi raqamli ID, tanlangan manbalar, yig'ish siyosati va yig'ish davrini qayd eting. TgWitness kuzatuvlarni saqlaydi va [Case Board](https://phishdestroy.github.io/TgWitness/uz/docs/reference/case-board/)'da manbaga bog'langan eslatmalar hamda yig'indilarni qo'llab-quvvatlaydi. Ko'chirish va saqlash yozuvlarini ish materiallaringiz bilan birga saqlang. Mo'ljallangan yig'ish sozlamalarini [jonli qabul qilish tartibi](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md) bilan tekshiring.
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

Muvaffaqiyatli tekshiruv ishonchli yig'uvchi kaliti va saqlangan chegaraga nisbatan yaxlitlikni ta'minlaydi. [Tekshiruv doirasiga](https://phishdestroy.github.io/TgWitness/uz/docs/reference/evidence/#verification-scope) qarang – ishonch taxminlari va bajarilgan tekshiruvlar bo'yicha [tasdiqlash natijalari](https://phishdestroy.github.io/TgWitness/uz/docs/reference/verification/) uchun.

## Topshirish qismi

Imzolangan ZIP butun ish maydoni jurnalini o'z ichiga oladi. Sud, advokat yoki suiiste'mol bo'limi faqat ba'zi suhbatlar, ma'lum bir davr yoki ayrim shaxslarga oid ma'lumotlarga muhtoj bo'lganda, **Eksportlar → Handover extract** tanlangan oshkor qilish qoidalariga muvofiq minimallashtirilgan nusxa (`tgwitness-handover-v1`) tayyorlaydi. Operator maqsadni bildiradi va suhbatlarni, ixtiyoriy davrni (UTC), ekstrakt qaysi odamlar haqida ekanligini, qolganlarga nima bo'lishini (ko'rsatiladi, P01 psevdonimlari bilan almashtiriladi, P02… yoki chiqarib tashlanadi), qaysi xabar matnlari qoladi, qaysi ilovalar va profil rasmlari kiritiladi, hamda matnlardagi telefon raqamlari va elektron pochta manzillari niqoblanadimi. Maqsad va ushbu qoidalar imzolangan manifestda va hisobotda ko'rsatiladi; jurnal faylni tayyorlagan foydalanuvchining kirish huquqi bilan`handover.exported` yozuvini qayd etadi, mazmuni emas, balki faylning SHA-256 qiymatini.

`verify.py` ekstraktni ikki usulda tekshiradi. O'zgarmagan holda ko'rsatilgan yozuv to'liq tasdiqlanadi: uning mazmuni hash bilan, Ed25519 imzosi va kiritilgan avvalgi yozuvga havolasi orqali tekshiriladi. Minimalizatsiya qilingan yozuv asl xesh va imzoni saqlab qoladi, shuning uchun imzo hanuzgacha tekshiriladi, lekin yashirilgan maydonlarni undan qayta hisoblash mumkin emas; yozuvda nima yashirilgani ko'rsatiladi va hisobot buni belgilaydi. Manifest jurnal uzunligi va sarlavhani, sarlavha ustida esa yig'uvchining imzosini ko'rsatadi, shuningdek chiqarib tashlangan yozuvlar sonini hisoblaydi; `coverage.json` tanlangan suhbatlarni tasvirlaydi. Fayl nomlaridagi ismlar aniqlanmaydi. Ulashishdan oldin yakuniy fayllarni ko'rib chiqing: erkin matn, fayl nomlari va tanlangan ilovalar hanuzgacha odamlarni aniqlashi mumkin. To'liq imzolangan ZIP-ni saqlang: undan olingan nusxa ma'lumotni oshkor qiladi, almashtirish emas.

## Oson o'qiladigan hisobotlar

Imzolangan dalillar, topshirish va chat ZIP-fayllari tanlangan hisobot tilida o'qiladigan HTML va JSON hisobotlarini, shuningdek zarur shriftlar mavjud bo'lganda PDF-ni o'z ichiga oladi. Har bir hisobot ish maydonining Ed25519 kaliti bilan muhrlanadi va alohida tekshirilishi mumkin: `python -m tgwitness.verify FILE --fingerprint KEY [--evidence ZIP]`.

- `report.html` / `chat.html`: muhr bayonoti (`tgwitness-report-seal-v1`) faylni yopadi va undan oldingi har bir baytning SHA-256ini imzolaydi. Uzoq jurnallar va suhbatlar sozlanadigan o'lchamdagi bo'laklarga bo'linadi (Hisobot sozlamalari, 500 dan 100 000 gacha yozuv; standart bo'yicha 5 000): `records/records-0001.html` yoki `messages/messages-0001.html`, har biri o'z raqami, diapazoni va jami bilan muhrlanadi va imzolangan manifestda SHA-256 bilan ro'yxatga olinadi. Kollektor yurak urishlari ketma-ketligi bitta satrda ko'rsatiladi, agar Hisobot sozlamalari ularni alohida-alohida ro'yxatga olishni belgilamagan bo'lsa.
- `report.json` (`tgwitness-report-json-v1`, kalitlar `format`, `report`, `seal`): muhr SHA-256 ning kanonik JSON dagi `report` ni imzolaydi, shunda faktlar ish yuritish tizimlari va skriptlar tomonidan o'qilishi mumkin va imzolangan fayl butunligicha saqlanib qolgan holda ulardan ma'lumotlarni himoya qilish uchun tanlov amalga oshirilishi mumkin.
- `report.pdf` / `chat.pdf`: chop etish va arxivlash uchun rasmiy hujjat, bir xil baytlar bo'yicha ikki marta imzolangan, imzo qiymatidan tashqari butun fayl (`/ByteRange`). Standart PDF imzosi (`adbe.pkcs7.detached`, SHA-256 va ECDSA P-256 bilan CMS) o'z-o'zini chiqargan hujjatni imzolash sertifikatidan foydalanadi, u ish maydoni xazinachisida saqlanadi; uning sub'ekt seriyali raqami Ed25519 kalit barmoq izidir. Ed25519 muhri CMS ichida imzolanmagan atribut sifatida harakatlanadi `2.25.240684792623320047764573196045913242332` va sertifikatning SHA-256 hashini bilan nomlaydi.Standart PDF imzosi (, SHA-256 va ECDSA P-256 bilan CMS) ish maydoni seyfida saqlanadigan o'z-o'zini chiqargan hujjatni imzolash sertifikatidan foydalanadi; uning sub'ekt seriyali raqami Ed2 `"content": "pdf-byte-range"`, shuning uchun Ed25519 kaliti sertifikatni tasdiqlaydi. PDF o'quvchisi fayl imzolangandan keyin o'zgarganini ko'rsatadi va sertifikat ishonchli bo'lmaguncha imzolovchini noma'lum deb ataydi; buning o'rniga Ed25519 barmoq izini solishtiring. Xitoycha, yaponcha va koreyscha PDF fayllariga serverda (yoki `TGWITNESS_FONT_DIR`); font bo'lmasa ZIP faqat HTML va JSON hisobotlarini o'z ichiga oladi.

Telegram kanalida yoki superguruhda xabarlarni 1, 2, 3… tartib bilan raqamlaydi. Chat eksporti birinchi va oxirgi raqamni, nechta xabar mavjudligini va `message-ids.json` dagi har bir ketma-ket kelmagan raqamni manifest va `chat.json` sarlavhasida ro'yxatlaydi hamda har bir bo'shliqni transkriptda qayerda joylashganini belgilaydi. `verify.py` ularni `chat.json` dan qayta sanaydi. Yo'qolgan raqam – bu Telegram qaytarmagan xabar (eksportdan oldin o'chirib tashlangan yoki hisobga ko'rinmaydigan); shaxsiy suhbatlarda va oddiy guruhlarda raqamlar hisobning barcha suhbatlari bo'ylab ulashiladi va bo'shliqlar hisobga olinmaydi.

Tarixni o'qigandan so'ng, eksport har bir mavjud bo'lmagan raqam bo'yicha yana Telegram dan so'raydi (`channels.getMessages`, 10 000 tagacha raqam). Natija `message-ids.json` va hisobotda ko'rsatiladi. Bo'sh javob Telegramda ushbu hisob uchun o'sha raqam ostida hech qanday xabar yo'qligini anglatadi; u xabar o'chirilgan yoki hech qachon hisobga ko'rinmaganligini ko'rsatmaydi. Agar Telegram xabarni qaytarib bersa, demak u o'qish paytida o'tkazib yuborilgan va eksportga `found_on_recheck` belgilab qo'shiladi.

Har bir hisobot**bilan boshlanadi. Qisqacha**: bir paragraf, keyin material nimani ko'rsatishini va nimani ko'rsatmasligini (hisob ortida kim turgani, yetkazib berish to'liqligi, kuzatuvdan oldin o'chirishlar, vaqt belgilovchi bo'lmasdan soat vaqti). Sahifaning o'z muhr tamg'asi sahifani emas, muhr imzosini tekshirganda ambra rangiga aylanadi: brauzer sahifaga o'z baytlarini bermaydi. U faqat o'quvchi faylni sahifaning oxiridagi tekshiruvga tashlaganda va har bir bayt mos kelganda yashil rangga aylanadi, shuningdek, ko'rsatilgan sahifa aynan shu fayl bo'lsa; aks holda u qizilga aylanadi.

Har bir hisobot dastur nomini aniq ko'rsatadi: git commit, agar yig'uvchi checkoutdan ishga tushsa yoki o'rnatuvchi `TGWITNESS_COMMIT` ni belgilasa, va manba fayllarining SHA-256 (`source_tree_sha256`, yo'lning kanonik JSON → har bir `.py` ning SHA-256, `.js`, `.css`, `.html` va `.svg` fayli paketda), bu commitni checkout qilish fayllar o'zgartirilmagan bo'lsa, qayta yaratadi. Telegram klienti o'z kutubxonasi, API qatlami va ma'lumotlar markazi nomi bilan ataladi. Kuzatuv boshlanganda va suhbat eksporti boshlanib tugagach, yig'uvchi Telegram'dan vaqtini (`updates.getState`, butun soniyalarda) so'raydi va yig'uvchining soatidan Telegram vaqtini ayirib, qaytish vaqti noaniqligini hisobga olgan holda qayd etadi; hisobotlarda bu o'lchovlar "Zanjir nazorati" bo'limida ko'rsatiladi. Suhbat eksporti shuningdek xabarlar sanalaridan tashqari, tarixni qachon o'qigani sanasini ham qayd etadi.

### Oflayn hisobot ko'ruvchi va arxiv bo'yicha qo'llanma

`chat.html` yoki `report.html` ni ochishdan oldin to'liq ZIP arxivini chiqarib oling. Ko'ruvchi qidiruv, filtrlar, ishtirokchilar, ko'rsatkichlar, yozuv tafsilotlari va serversiz JSON/CSV tanlovlarini taqdim etadi. `viewer/` va `media/` ni hisobot yonida saqlang. Tanlovlar hosilalar: ularni imzolangan arxiv bilan solishtirish uchun `verify.py SELECTION.json
--evidence ARCHIVE.zip` dan foydalaning. Verifikator hisobot IDsi, imzolash kaliti, arxiv chegarasi va har bir tanlangan elementni tekshiradi; tahrirlangan, yo'qolgan va takroriy elementlar rad etiladi. Tanlov izohlar va yaratilish vaqti imzolanmagan metadata bo'lib qoladi.

Xabar-raqam bo'shliqlari faqat to'liq, filtrlanmagan osib boruvchi chat oqimida ko'rsatiladi. Kategoriyani yashirish yoki ma'lumot bo'lagini yuklamaslik o'chirib tashlangan qatorni yo'qolgan xabar dalili deb hisoblashga olib kelmasligi kerak. Qidiruv ta'kidlashlari oddiy matnda ishlaydi, HTML qochirilishidan oldin va so'zma-so'z belgilashni saqlaydi.

Brauzer imzo manifestlari, hisobot ID va kaliti hamda ro'yxatda keltirilgan barcha fayl hashlarini tekshiradi. U noaniq yoki noto'g'ri tuzilgan ZIP tuzilmalarini, takroriy nomlarni va xavfsiz bo'lmagan yo'llarni rad etadi hamda fayllarni 256 MiB, e'lon qilingan jami hajmni esa 4 GiB bilan cheklaydi. Katta arxivlar uchun mustaqil verifikatorni ishlating. Ushbu brauzer tekshiruvi verifikatorning jurnal zanjirlari va ma'lumotlar semantikasini tekshirishini to'ldiradi.

`README.txt` boshlang'ich qo'llanma, moslashtirilgan fayllar ro'yxati, tasdiqlash bo'yicha ko'rsatmalar va hisobot tilidagi ma'lumot formatiga oid eslatmalarni o'z ichiga oladi, undan keyin to'liq inglizcha qo'llanma keltiriladi. `SHA256SUMS` o'zini, `manifest.json` va `manifest.sig` fayllarini istisno qilgan holda ichida ro'yxatga olingan fayllarni qamrab oladi; imzolangan manifestga `SHA256SUMS` ham kiritilgan. Asl ZIP-ni o'zgarmas holda saqlang va ishlayotgan fayllarni chiqarilgan papkadan tashqarida saqlang. PDF hisobotlariga bo'lim belgilari va keyingi sahifalarda ish/hisobot identifikatsiyasi kiritilgan.

### Eksport vaqtidagi suhbat

Chat eksporti eksport boshlanganida chat haqidagi Telegram ma'lumotlarini qayd etadi: Telegramning o'z yorliqlari (`scam`, `fake`, `restricted` sabablari bilan, `verified`), foydalanuvchi nomlari, tavsif, a'zo va admin soni, bog'langan muhokama, kontentni himoya qilish, yangi a'zolarning oldingi xabarlarni ko'rishi va ushbu hisobdagi tarixni qaysi xabardan boshlab ko'rishi (`available_min_id`), chat yaratilgan paytdagi 1-xabar sanasi va chat fotosuratining SHA-256i (`media/`da saqlangan). Bu eksport qilinayotgan hisobning chatdagi o'rnini qayd etadi: roli, qo'shilgan sanasi, kim taklif qilgani va admin uchun uning huquqlari. Telegram rad etgan so'rov esa uning o'rniga nomlanadi.

Eksport qilayotgan hisob ma'mur bo'lsa, eksport suhbatning ma'mur logini (Telegram taxminan 48 soat saqlaydi) `admin-log.json` ga o'qiydi: mazmun va harakat qilgan hisob bo'yicha o'chirishlar va tahrirlar. Bu o'chirishni kim amalga oshirganini ko'rsatadigan yagona yozuvdir.

### Ko'rsatkichlar

Hisobotlar ro'yxati va arxiv `indicators.csv` , `indicators.stix.json` (STIX 2.1 ) va `indicators.misp.json` (MISP hodisasi) orqali qayd etilgan xabarlarda suiiste'mol bo'yicha bo'lim qaysi harakatlarni amalga oshirishi mumkinligini ko'rsatadi: havolalar va domenlar (shuningdek matn ortida, tugmalarda va havola ko'rinishlarida yashirilgan), kriptovalyuta manzillari, Telegram foydalanuvchi nomlari va taklif havolalari, telefon raqamlari, elektron pochta manzillari va saqlangan rasmlar. Bitcoin, Litecoin, Dogecoin va TRON manzillari faqat ularning base58 tekshiruv yig'indisi to'g'ri bo'lganda, segwit manzillari ularning bech32 yoki bech32m tekshiruv yig'indisi to'g'ri bo'lganda va TON manzillari ularning CRC to'g'ri bo'lganda ro'yxatga olinadi; EVM va Solana manzillari tekshirilmagan deb belgilangan. Rasmlar SHA-256 va perceptual hash (dHash, 64 bit) bilan belgilangan bo'lib, qayta siqilgan yoki o'lchami o'zgartirilgan nusxalarda deyarli o'zgarmas qoladi. Hisobotlar ko'rsatkichlarni tasodifan ochilmasligi uchun yozadi (`hxxps[://]example[.]com` ); fayllar esa qiymatlarni o'z holicha saqlaydi. Har bir indikator noma'lum va avtomatik aniqlash uchun mo'ljallanmagan deb belgilangan (STIX `indicator_types: unknown` , MISP `to_ids: false` , o'z tashkilotiga tarqatish): ro'yxatda bo'lish xabar unda mavjudligini anglatadi, zararli ekanligini emas. Hisobotda matni ochiladigan manzildan farq qiladigan havola belgilangan.

PDF hisobotlari qo'l bilan imzolanadigan tekshiruvchi bayonoti, notarius yoki sud eksperti uchun tekshiruv ro'yxati va hisobot IDsi, kalit barmoq izi hamda vakolatli ma'lumotlarning SHA-256 bilan QR-kod (birinchi sahifada ham) bilan yakunlanadi, shunda chop etilgan nusxa uning arxiviga qaytadi.

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

Telegram hisobni qabul qilishni to'xtatganda, kuzatuvni yakunlovchi `coverage.gap` yozuvi `cause` (`account_banned`, `account_frozen`, `account_deleted`, `session_duplicated`, `session_revoked`, `session_expired`, `session_ended` yoki `not_authorized`) va Telegram xatosini o'z ichiga oladi; `verify.py` davr yakunida sababni belgilaydi.

Qamrov ushbu yig'uvchi nima yozib olganini tasvirlaydi. Bu Telegram uzluksiz davr mobaynida har bir yangilanishni yetkazganining isboti emas.

## Ishlab chiquvchi

Dalillar ZIP-arxivlari, suhbat eksportlari, guvoh jurnallari va shaxsiy profil fayllari bayonotining imzolangan manifesti `producer` ni o'z ichiga oladi: dasturiy ta'minot, versiya, loyiha (PhishDestroy), bosh sahifa va manba ombori. HTML hisobotida ham xuddi shu satr ko'rsatiladi, va `verify.py` uni tekshirgan narsalarning bir qismi sifatida chop etadi. Ushbu maydon mavjud bo'lmasdan oldin yaratilgan arxivlar oldingi holatni tasdiqlaydi va ularning yaratilganligi to'g'risida ma'lumot beruvchi ko'rsatilmaganligi qayd etiladi.

Har bir `observation.started` yozuvi shuningdek kuzatgan Telegram mijozining nomini ham ko'rsatadi: uning `api_id` (hech qachon hash emas), bu ichki ommaviy juftlikmi yoki operatorning o'z ilovasi ekanligini, Telegram ulanish so'rovida yuborilgan mijoz tavsifini va IP rejimidagi ulanish yo'nalishi turini (proxy manzili yoki sir yo'q). Hisobot va `custody.json` har bir alohida mijoz va yo'nalishni ular qachon qayd etilgani bilan, shuningdek ro'yxatda keltirilmagan proxy javob bermagan va Telegram server manzilini ko'rgan vaqtlarni ko'rsatadi. Buni shu vaqtdan oldin yozilgan jurnallar ham tasdiqlaydi.

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

## Verifikatsiya doirasi

Imzolar yig'uvchi kalitini aniqlaydi va saqlangan materialni himoya qiladi. Uning barmoq izini mustaqil ravishda bog'lang, shunda bu kalit kutilayotgan yig'uvchi bilan bog'lanadi. Telegram yangilanishlari yig'ish uchun kirish ma'lumotlari hisoblanadi; TgWitness ushbu yangilanishlar bo'yicha kuzatuvlarini imzolaydi. Ushbu imzolar Telegram yoki xabar mualliflari tomonidan berilgan imzolar emas.

Saqlangan tekshiruv nuqtasi yoki guvoh yozuvi avvalgi jurnal prefiksining o'zgarganini aniqlaydi, jumladan nusxa olingan yig'uvchi kaliti bilan imzolangan almashtirishni ham. Birinchi mustaqil tekshiruv nuqtasidan oldin yaratilgan yozuvlar manba tasdiqini talab qiladi: yig'uvchi kalit egasi yangi materialni imzolashi mumkin. Imzo kalitiga kirishni nazorat ostida saqlang va havolalarni alohida saqlang.

Qamrov yozuvlari va nazorat ostidagi testlardan foydalangan holda hisobning ko'rinishi va yetkazib berilishini baholang. Mustaqil vaqtni belgilash uchun tasdiqlangan tashqi vaqt belgisi (timestamp)dan foydalaning. Jo'natuvchi ID Telegram hisobini aniqlaydi; uni tergov orqali shaxsga bog'lang. Dastur kvitansiyalari va bulut tekshiruvlari yig'uvchi tomonidan xabar qilingan o'lchovlar va joylashtirish konfiguratsiyasini tasvirlaydi. O'lchangan xatti-harakatlar va uning doirasiga oid [tasdiqlash natijalarini](https://phishdestroy.github.io/TgWitness/uz/docs/reference/verification/) ko'ring.

## Ilovalar

Media/ katalogi ostida fayllar SHA-256 hashiga ko'ra manzillanadi. media.saved hodisasi haesh va bayt uzunligini ma'lum bir xabar hodisasi bilan bog'laydi. Xom fayl nomlari metama'lumot bo'lib, hech qachon mahalliy yo'l bo'lmaydi. Media baytlari asinxron tarzda yuklanadi, shuning uchun darhol o'chirish ularni qayd etilishini to'xtatishi mumkin. To'plamni o'chirib qo'yish, katta hajmli/noma'lum hajmli fayllar, yuklab olishdagi xatoliklar va uzilgan yuklab olishlar natijalar sifatida ko'rinadi. Jarayon qulashi bog'lanmagan qisman fayllarni qoldirishi mumkin; ular eksportga kiritilmaydi.

ZIP eksporti saqlangan media fayllarini ularning nomlari bilan solishtiradi. JSONL, CSV va HTML eksportlari voqea imzolarini tekshiradi, lekin media baytlarini o'z ichiga olmaydi. Qo'shimcha hisobotlar qulaylik uchun mo'ljallangan; events.jsonl voqealarning haqiqiy vakilidir.

To'liq chat eksporti ish maydonining ilovalar sozlamalaridagi ilovalarni media/ katalogiga SHA-256 nomi bilan saqlaydi. chat.jsondagi har bir xabar yozuvi o'z faylini (`file`, `file_sha256`) yoki uning yo'qligining sababini (`file_status`), shuningdek o'quvchiga matn atrofida ko'ringan narsalarni: matn ortidagi havolalar, yuboruvchi manbai, bot tugmalari, imzo, ko'rinishlar va avtomatik o'chirish taymerini qayd etadi. `verify.py` har bir nomlangan faylning shu xesh ostidagi imzolangan manifestda mavjudligini tekshiradi.

## Chidamli yig'ish va jarayon kvitansiyalari (0.2)

Media ish va uning xabar voqeasi bitta tranzaktsiyada yozib qo'yiladi. Ish asl TL xabar tavsiflagichini saqlaydi; imzolangan kuzatuv uning SHA-256, hisob va hajm siyosatini bog'laydi. Tiklash yuklab olishdan oldin bu bog'lanishni tekshiradi. U hech qachon joriy xabarni olib kelmaydi va jimjit ravishda yangiroq ilovani almashtiradi. To'xtab qolgan ishlar qayta urinadi, lekin doimiy xato aniq natija bo'lib qoladi.

Har bir ish maydonining o'z jurnali va imzolash identifikatori mavjud. process.started hodisasi run ID, mahalliy soatlar, bog'liqlik versiyalari, manba-fayl hashlarini, dastlabki hisob/doirani va yozib olish sozlamalarini o'z ichiga oladi. Heartbeatlar run ID, monotonik vaqt va navbat holatini o'z ichiga oladi. Jarayon kvitansiyasi alohida imzolangan bayonot sifatida ham yuklab olinishi mumkin. Fayl o'lchovlari o'z-o'zini xabar qilishga asoslangan bo'lib, ishonchli apparat tasdig'i hisoblanmaydi.

Avtomatik tekshiruv nuqtalari dastur ishga tushirilganda, kuzatuv paytida har besh daqiqada (**Parametrlar → Imzolangan tekshiruv nuqtasi har**) va tartibli to'xtashda mahalliy ravishda saqlanadi. Boshlanishdagi tekshiruv va eksport jurnalni eng so'nggi saqlangan mahalliy tekshiruv nuqtasiga solishtiradi. Bu tekshiruv nuqtasi saqlanib qolganda ma'lumotlar bazasining orqaga qaytishini aniqlashi mumkin; ikkalasini ham nazorat qilayotgan operator esa ularni baribir almashtira oladi. Mustaqil saqlash va tashqi ishonchli vaqt tamg'alari alohida talablar bo'lib qoladi.

Qayta ishga tushirilgandan so'ng saqlangan Telegram yangilanish pozitsiyasi (`catch_up_from`da `observation.started`) tiklanadi va o'tkazib yuborilgan yangilanishlar so'raladi. Davriy qayta tekshirish o'tkazib yuborilgan xabarlar uchun `message.recovered`ni va Telegram saqlangan xabarni qaytarmasa `message.missing_on_recheck`ni qayd etadi; ikkinchisi o'chirish bildirishnomasi emas va o'chiruvchini ham, vaqtni ham ko'rsatmaydi.

### S3da nusxa olish va tiklash

Joydan tashqari nusxa (eksportlar, standart bo'yicha o'chirilgan) jurnal segmentlarini, saqlangan fayllarni, tekshiruv nuqtalarini ularning vaqt tamg'alari bilan va yakunlangan suhbat eksportlarini S3-ga mos omborga yuklaydi, AES-256-GCM bilan shifrlaydi AES-256-GCM bilan yuklashdan oldin ish maydoni seyfida saqlanadigan kalit ostida shifrlanadi; Object Lock saqlash qoidasi bucket uni qo'llab-quvvatlaganda amal qiladi. Yuklab olingan kalitsiz nusxa o'qilmaydi. Tiklash va tasdiqlash uchun `python -m tgwitness.replica restore --key-file KEY.json --out DIR`.

Qayta tiklash bo'sh oddiy katalogni talab qiladi. Yuklab olingan va dekript qilingan obyektlar butun jurnal va har bir saqlangan tekshiruv nuqtasi tasdiqlanguncha shaxsiy vaqtinchalik saqlash joyida qoladi. Xavfsiz bo'lmagan obyekt yo'llari, nomuvofiq segment diapazonlari va tekshiruv nuqtasidan qisqaroq jurnallar rad etiladi; muvaffaqiyatsiz tasdiqlash hech qanday tiklangan fayllarni e'lon qilmaydi. Saqlash tekshiruvlari qaytarilgan Object Lock rejimi va sanani yuklash paytida yuborilgan muddat bilan solishtiradi (bir soniya atrofida xatolik chegarasi). Muddati o'tgan, noto'g'ri yoki qisqartirilgan muddat tasdiqlangan hisoblanmaydi. Statusi esa shu yuklash bosqichi uchun saqlash ma'lumotlari o'qilgan namunaviy obyektni ko'rsatadi.

Yo'qolgan yoki shikastlangan mahalliy media fayl o'tkazish jarayonidagi xato sifatida qayd etiladi va media kursorini uning oldidagi pozitsiyada ushlab turadi, shuning uchun fayl keyingi o'tkazishda yana sinab ko'riladi; undan keyingi fayllar, tekshiruv nuqtalari va eksportlar esa baribir nusxalanadi. Tiklash tekshiruvlari saqlangan media havolalarini dekriptaj qilingan xeshlar va qayd etilgan o'lchamlarga muvofiq tekshiradi. Uzilgan yuklashlardan kelib chiqqan bir xil ustma-ust keluvchi jurnal segmentlari takrorlanishdan tozalang; ziddiyatli ustma-ust kelishlar rad etiladi. Yuklash jarayonida yaratilgan nazorat nuqtalari ularning qamrab olgan jurnal yozuvlari nusxalanganiga qadar kechiktiriladi, shuning uchun yakunlangan bosqich o'z jurnalidan oldinda nazorat nuqtasini e'lon qilmaydi.

### Streaming eksporti snapshotlari

Streaming eksportlari barqaror SQLite o'qish snapshotidan foydalanadi. Yuklab olish tugagach, uning bosh qismi joriy jonli jurnaldan eski bo'lishi mumkin. Ushbu snapshotdan keyin yaratilgan tekshiruv nuqtasi arxivning qisqaroq ekanligini to'g'ri ko'rsatadi; eksport qilingan prefiksdagi yoki undan oldingi tekshiruv nuqtasi bilan solishtiring, tasodifiy keyingi tekshiruv nuqtasi bilan emas.

## RFC 3161 tayyorgarligi va javobni tasdiqlash (0.2)

Dalil rejimi (defoltda o'chirilgan) har bir imzolangan tekshiruv nuqtasining faqat SHA-256 hashini ro'yxatga kiritilgan RFC 3161 vakolatli organlariga va OpenTimestamps taqvimlariga ish maydoni marshruti orqali yuboradi va hech qachon MTProxy orqali emas. Javoblar `checkpoints/anchors/`da saqlanadi, eksport qilinadi va `verify.py` tomonidan tekshiriladi (`--tsa-ca` TSA imzosini tekshiradi; OpenTimestamps isbotlarini `ots upgrade` va `ots verify` bilan tasdiqlaydi).

Panel canonical checkpoint.json baytlarini, SHA-256 xabar izini va timestamp.tsq, checksums hamda ko'rsatmalardagi tasodifiy nonse-ni o'z ichiga olgan so'rov arxivini tayyorlaydi. Hech qanday tarmoq so'rovi amalga oshirilmaydi. Tayyorlash ishonchli vaqt shtampi hisoblanmaydi.

`python -m tgwitness.anchor verify` ikki marta OpenSSL ts-ni chaqiradi: bir marta tekshiruv nuqtasi baytlari bo'yicha va bir marta asl so'rov bo'yicha. Ishonchli CA fayli aniq ko'rsatilishi kerak; Ilovaga kiritilgan sertifikatlar avtomatik ravishda ishonchli hisoblanmaydi. CLIda so'rovni tekshirish ixtiyoriy bo'lib, shuning uchun nonse tekshirish uchun --request parametrini saqlang va kiritgan holda ishlating. Natija tekshirilgan yoki tekshirilmaganligini ko'rsatadi. Yig'uvchining tekshiruv nuqtasi imzosi va jurnalini ishonchli yig'uvchi barmoq izi bilan alohida tasdiqlash kerak.

Verifikatsiya javob imzosi, tekshiruv nuqtasi baytlarini va taqdim etilganda, belgilangan CA ishonchi ostida asl so'rovni tekshiradi. Revokatsiya tekshiruvlari va sertifikat muddati tugagach uzoq muddatli arxivlashni tasdiqlash joriy verifikator doirasidan tashqarida. [Protsedura](https://phishdestroy.github.io/TgWitness/uz/docs/reference/timestamp/) va [tasdiqlash natijalarini](https://phishdestroy.github.io/TgWitness/uz/docs/reference/verification/) ko'ring.

## Dalil rejimidagi ixtiyoriy yozuvlar: drand va Telegram qurilmalari

Yana ikkita yozuv vaqt belgilari bo'yicha bir xil o'tishlarda ishlashi mumkin. Ikkalasi ham standart bo'yicha o'chirilgan va faqat dalillar rejimi yoqilganda amalga kiradi: Qo'shimchalar → Dalillar va zaxira nusxalar → **Qo'shimcha guvohlar · ixtiyoriy**, yoki `"drand": true` va `"devices": true` da `POST /api/evidence`. Birining ishlamay qolishi ikkinchisiga yoki vaqt tamg'alariga ta'sir qilmaydi; panel har birining eng so'nggi natijasini shakl ostida ko'rsatadi.

**drand** (`beacon.drand` ). Har bir o'tish drand quicknet'ning eng yangi raundini, Entropiya Ligasi ommaviy tasodifiyligini (har 3 soniyada bir raund), jurnalga yozadi: `chain` , `round` , `randomness` , `signature` , `round_time` va javob bergan `relay` . Tasdiqlangan, oldindan aytib bo'lmaydigan raund keyingi hash-bog'langan material uchun pastki vaqt manbasini ta'minlaydi. Keyingi tekshiruv nuqtasidagi tasdiqlangan vaqt tamg'asi yuqori vaqt referensiyasini ta'minlaydi. Ushbu tekshiruvlar bog'langan materialni chegaralab qo'yadi; to'plam qamrovi alohida baholanadi. Yig'uvchi avvalo `drand.cloudflare.com` ga murojaat qiladi, so'ngra Protocol Labs relelari orqali ish maydoni yo'li bo'yicha har bir o'tishda bitta so'rov yuboradi.

`verify.py` har bir tasodifiylik uning imzosi SHA-256 ekanligini va raund vaqti to'g'ri ekanligini tekshiradi, shuningdek raundlarni, raundsiz eng uzun davrni va drand yig'uvchining soati qanchalik orqada qolganini hisobot qiladi. U BLS imzosi tekshirilmaydi. `--check-drand` raundlarni Cloudflare va Protocol Labs releylari bilan solishtiradi, barchasini yoki uzun jurnalda 100 tadan tasodifiy namunani; farqli raund tasdiqlashni rad etadi.

**Telegram qurilmalari** (`account.devices`). Har bir o'tish hisobning sessiyalarini o'qiydi `account.getAuthorizations`, Telegram Sozlamalar → Qurilmalar bo'limida ko'rsatiladigan ro'yxatni o'qiydi va uni qayd etadi: oldingi tekshiruvdan beri o'zgargan bo'lsa to'liq, bilan `added` va `removed` session hashlarini, aks holda faqat uning soni va SHA-256 ni yozib oladi. Qurilma modeli, platforma, ilova va versiyasi, yaratilgan va oxirgi faoliyat vaqti, mamlakat va mintaqa saqlanadi; IP-manzillar esa saqlanmaydi, chunki dalillar eksporti sizning nazoratingizdan chiqadi. Yig'uvchining o'z sessiyasi doim faol bo'ladi, shuning uchun faqat boshqa sessiyalarning faolligi o'zgarish sifatida hisoblanadi. `verify.py` Ro'yxat qancha tez-tez yozib olingani va har bir yangi hamda yakunlangan sessiyani hisobot beradi. U ro'yxatni faqat kuzatuv davom etayotgan paytda o'qiydi.

Ular nimani ko'rsatmaydi: drand jamoat vaqti bo'yicha yozuvlar tartibidan boshqa hech narsani isbotlamaydi, va qurilmalar ro'yxati — bu yig'uvchi orqali berilgan, har bir boshqa yozuv kabi yig'uvchi tomonidan imzolanganTelegram bayonotidir.

**Cloudflare Gateway logi** (`cloudflare.gateway_dns`). Cloudflare Gateway ([Gateway DNS](https://phishdestroy.github.io/TgWitness/uz/docs/reference/high-assurance/#cloudflare-as-an-outside-witness)) orqali so'rovni hal qiladigan server uchun, har bir pass oldingi nusxa olinganidan beri Gateway tomonidan qayd etilgan ma'lumotlarni nusxalaydi: har bir uch soatgacha bo'lgan oynada bittadan yozuv, `from`, `until`, `location_id`, serverning `address` (agar sozlangan bo'lsa) va `queries` (`[at, name, type, rcode, decision, colo]`) bo'yicha, hatto hech qanday yozuv bo'lmagan paytda ham. **Cloudflare Gateway log**ostar ostida sozlang: hisob, joylashuv, ixtiyoriy manzil va faqat o'qish uchun token (Hisob Analytics Read; Zero Trust PII Read (ulashilgan joyning bitta manzilini saqlash uchun). Panel ularni saqlashdan oldin bitta so'rov bilan tekshiradi; token shifrlangan holda qoladi va hech qachon jurnalga kiritilmaydi. `verify.py` oynalarni, eng ko'p qidirilgan nomlarni va nusxa qamrab olmagan har qanday vaqtni ro'yxatlaydi; so'rovlari soni ularning so'rovlari soniga mos kelmaydigan yozuv muvaffaqiyatsiz bo'ladi. Bir soniyada bir nechta sahifani o'z ichiga olgan oynada o'sha sahifani saqlab, qolganlari yo'qligini bildiradi. Nusxa — kollektor orqali Cloudflare javobidir, kollektor tomonidan imzolangan; 24 soat ichida faqat o'qish huquqiga ega tokeni bo'lgan har kim uni Cloudflare bilan solishtirishi mumkin.
