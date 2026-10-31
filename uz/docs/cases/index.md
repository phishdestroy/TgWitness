# Barcha suhbatlarni tergov qiling

Canonical page: https://phishdestroy.github.io/TgWitness/uz/docs/cases/

Kanallar, guruhlar, shaxsiy suhbatlar va botlar bo'ylab butun ishni yuritish: dalillarni to'plash, bog'lash, qayta tiklash va topshirish.

Ushbu bosqichma-bosqich ko'rsatma bir xayoliy hodisani to'liq hisob yozuvi orqali kuzatadi. U haqiqiy yig'ish, qidiruv, foydalanuvchi profil va eksport funksiyalaridan foydalanadi. Ish xaritasi hujjat misolidir; sizning xulosalaringiz va ish reyestri ilovadan tashqarida saqlanadi.

KO'RILGAN ISH / O'ZGARTIRILGAN TO'LOV MANZILI

### Bir hodisa. To'rt suhbat. Qoldiq izni qayta tiklash.

Kanal e'lonida botga havola qilinadi. Operatsiyalar guruhi yangi to'lov havolasini muhokama qiladi. Xususiy keyingi xabar uni takrorlaydi. Keyinroq e'lon tahrirlanadi va guruh xabari yo'qoladi.

Har bir versiyani kim joyladi?Havo kim paydo bo'ldi?Qaysi fayl saqlangan?Nima o'zgardi va qachon?

Tarixni yuklash, ixtiyoriy AI manba tekshiruvi, MCP, OCR va chiquvchi webhooks uchun [Work the archive bo'limiga](https://phishdestroy.github.io/TgWitness/uz/docs/archive/) qarang.

## 1. Butun hisob bo'ylab qamrovni o'rnatish

1. [Yig'ish akkauntini o'z ish maydonida ulanib qo'ying](https://phishdestroy.github.io/TgWitness/uz/docs/accounts/). Ishga oid ma'lumotlarga ish referensiyasi, akkaunt ID-si, ish maydoni nomi va imzolash kaliti barmoq izini qoldiring.
2. Ochiq **manbalar → Kuzatuv doirasi → Tergov rejimi**. **Butun hisobni**, to'rtta manba turini va **o'z harakatlaringizni** ko'rib chiqing. Ushbu oldindan sozlash yangi manbaning profilini va uning so'nggi **200 ta ko'rinadigan xabarini** saqlash imkonini beradi. "**Doirani saqlash"** tugmasini bosing va doirani tasdiqlashni yakunlang.
3. **Suhbatlarni yuklash** tugmasini bosing. Manbalarni hisobning dialoglar ro'yxati va ko'rib chiqishdan mustasno qilishlar bilan solishtiring. **Parametrlar → Suhbatlar** bo'limida **hisob ro'yxatidan o'qiladigan suhbatlarni ko'ring**, zarur bo'lsa dastlabki ro'yxat chegarasini o'zgartiring: standart 1 000 dialog, maksimal 20 000 gacha sozlanishi mumkin. Chegaradan oshgan suhbatlar faollashganda aniqlanadi.
4. **Yozib olish sozlamalar**ida **barcha ko'rinadigan faoliyatni** tanlab, saqlang. Ilova turlarini, hajm cheklovlarini va bo'sh disk joyini tekshiring. Sozlamalarga tayanishdan oldin kuzatuvni boshlang va nazorat ostidagi xabar, tahrir va o'chirishni tasdiqlang.

KanalGuruhlarShaxsiy suhbatlarBotlar

BIR AKKAUNT / BIR IMZO KALITI**Tanlangan va akkauntda ko'rinadigan barcha faoliyat → bitta jurnal**

Xabarlar · tahrirlar · o'chirish bildirishnomalari · ko'rinadigan munosabatlar · a'zolik voqealari · o'z harakatlari

"Butun hisob" ushbu hisob kirish huquqiga ega bo'lgan suhbatlarni, sozlangan manba turlari va istisnolar bilan qamrab oladi. Sirli suhbatlar mavjud emas. Yangilangan dialoglar yangilanishlar kelishi bilan qo'shiladi; ushbu rejimni yoqish mavjud bo'lgan har bir suhbatning to'liq eski tarixini avtomatik yuklab olmaydi.

## 2. Tarixni olish va fayllarni saqlash

Butun tergov uchun manba ro'yxatini tuzing. Har bir suhbatga uning raqamli ID-si, sarlavhasi, hisobi, kirish/roli, jonli boshlanishi, tarixni olish, media natijasi va ma'lum bo'shliqlar bilan satr ajrating. Manbani tegishli natijani tekshirgandan keyingina olingan deb belgilang.

| Kerak | Panelda harakat | U nimani taqdim etadi |
| --- | --- | --- |
| Yoqilgan suhbatlardagi tarix | Manbalar → To'liq tarixni yuklash | Joriy asosiy: mavjud eski xabarlar ish maydoni jurnaliga kiritiladi, tanaffus/davom ettirish va imzolangan progress hisobotiga ega. [Tarix bo'yicha qo'llanma](https://phishdestroy.github.io/TgWitness/uz/docs/reference/history/). |
| Jurnalning mavjud suhbat konteksti | Manbalar → Yozuv sozlamalari → Tarixni snapshot qilish | Yaqinda ko'rinadigan xabarlar imzolangan kuzatuvlar sifatida. Standart maksimal 500; **Parametrlar → Eng katta tarix nusxasi** uni 10 000 gacha oshirishi mumkin. |
| Hozirda ko'rinadigan bitta suhbatning to'liq tarixi | To'liq suhbat eksporti → To'liq suhbatni eksport qilish, yoki Suhbatlar → Suhbatni eksport qilish | `chat.json` va `chat.html` bilan alohida imzolangan paket. Har bir manba bo'yicha takrorlang; muvaffaqiyat/muvaffaqiyatsizlik natijalarini saqlang. |
| Yangi suhbat paydo bo'lganda kontekst | Kuzatuv doirasi → Yangi suhbat yoki bot paydo bo'lganda | Manba profil va so'nggi 1 000 ta ko'rinadigan xabar; Tergov rejimi 200 tasini tanlaydi. Mavjud suhbatlarga bu ma'lumot retroaktiv tarzda qo'llanilmaydi. |
| Ilova baytlari | Ko'rinadigan ilovalarni yuklab oling + har bir tur bo'yicha limitlar | `media.saved` ni, uning SHA-256 summasini va bayt sonini tekshiring. Navbatga qo'yilgan, o'tkazib yuborilgan yoki muvaffaqiyatsiz yuklab olingan fayl saqlangan fayl hisoblanmaydi. |

To'liq chat eksporti alohida snapshot hisoblanadi; u butun tarixni jurnalga yoki odamlar profiliga import qilmaydi. TgWitness ichida qidirishingiz kerak bo'lgan tarixiy material uchun yoqilgan manbalar bo'ylab **to'liq tarixni yuklash** yoki cheklangan jurnal snapshotlaridan foydalaning. Ishni boshlashdan oldin manbalar ro'yxatini ko'rib chiqing.

Ishlangan holatda e'lon kanali, operatsiyalar guruhi, bot suhbatlari va maxfiy kuzatuvni qo'lga kiritish. Chek qo'shimchasining baytlari va hashini saqlash. Bugungi kunda mavjud tarix yozib olinishidan oldin o'chirilgan yoki Telegram endi qaytarmaydigan oraliq tahrirlarni tiklay olmaydi.

## 3. Rivojlanayotgan suhbat va o'z harakatlaringizni saqlang

Ish rivojlanar ekan, kuzatuvni uzluksiz davom ettiring. Faol ish suhbatlarini ustuvor manba sifatida belgilang; **Yozib olish sozlamalari → Qayta tekshirish** bo'limida ustuvor va boshqa manbalarni qayta tekshirishni sozlang. Ish davomida `recheck.completed`, davom etayotgan ma'lumotlarni to'plash, FloodWait va media natijalarini ko'rib chiqing.

**Hozirda** manba tavsiflarini, bot buyruqlarini va Telegram qaytaradigan boshqa metama'lumotlarni saqlab qolish uchun **Söhbatlar → Profil → Profilni saqlashni** bosing. Ushbu manba profili jurnal xabarlari asosida tuzilgan shaxs profillaridan alohida.

**Botni yoki taklifni ish yurituvi doirasida kuzatish**

1. **Suhbatlar → Telegram havolasini ochishda** avval ko'rinishni saqlang. Asl havola va qaytarilgan ko'rinish imzolangan yozuvlarga aylanadi.
2. Agar tergov bunga ehtiyoj sezsa, **Join / Open funksiyalarini chaqiradi**, manbani ochadi va taqdim etilgan start parametri bilan botni ishga tushiradi. Kutib turgan qo'shilish so'rovi yozuvda kutib turgan holda qoladi.
3. Harakatni hujjatlashtirish uchun panelning matnli javobini yoki qo'llab-quvvatlanadigan "**Bosish tugmasi"** boshqaruvini ishlating. Jurnal `interaction.requested` va `interaction.result` ni, shu jumladan qaytgan callback matni yoki URL manzilini saqlab qo'yadi.

Ushbu nazoratlar haqiqiy Telegram harakatlarini bajaradi. Boshqa Telegram ilovasida bosilgan callback to'plovchiga ko'rinmaydi; botning keyingi xabari yoki tahriri esa ko'rinishi mumkin. Veb-ilovalar, to'lovlar va telefon/joylashuv so'rovlari mini-klient doirasidan tashqarida.

## 4. Suhbatlar bo'ylab odamlar, havolalar va fayllarni kuzatib boring

1. Ochiq **jurnalni** oching, manba filtrini "**Barcha manbalar**"da qoldiring va o'ziga xos ibora, domen, foydalanuvchi nomi yoki saqlangan identifikatorni qidiring. Har bir mos yozuvni oching va uning suhbat IDsi, xabar IDsi hamda jurnal ketma-ketlik raqamini qayd eting.
2. Mavzuga oid suhbatni ochish uchun **Chats → People → Profillarni yoqishni**tanlang, so'ngra shaxsni tanlang. Ism/foydalanuvchi nomi tarixini, javob munosabatlarini, faoliyatni ko'rib chiqing; **shuningdek,** boshqa kuzatilgan suhbat**larda** va olingan havolalarda, hamyonlarda yoki telefon raqamlarida **ham**. Keltirilgan jurnal yozuvlarini oching.
3. Ushbu ish maydonidagi boshqa suhbatlarda ham xuddi shu raqamli Telegram foydalanuvchi IDni kuzating. Mos keladigan ism, hamyon tilga olinishi yoki o'xshash avatarni tekshirish uchun iz sifatida qabul qiling. Tilga olingan manzil egalikni aniqlamaydi; o'xshash avatar esa bir xil shaxs ekanligini tasdiqlamaydi.
4. Saqlangan ilovalar uchun SHA-256 qiymatlarini yozuvlar bo'ylab solishtiring. Bir xil xeshlar saqlangan fayllarning bayt darajasidagi ekvivalentligini tasdiqlaydi. Kim ularni ulashganligi haqida xulosa qilishdan oldin tegishli xabar va jo'natuvchi yozuvlarini tekshiring.

ISH XARITASI / MANBALARGA E'TIBOR BERINGBadiiy holat · jonli grafika emas

KANAL / E'LON**Asl → tahrirlangan manzil**

Yozuvlar #101, #188 Xabar #84 · jo'natuvchi aniqlanmagan

GURUH / AMALIYOTLAR**Foydalanuvchi 71001 yangi havolani joylaydi**

Yozuv #146 · xabar #309 Saqlangan fayl kvitasi #151

BOT / BUYURUQ SUHBATI**Bir tugma o'sha manzilga yo'naltiradi**

Yozuv #173 · xabar #12 Tugma metama'lumotlari qaytarildi

MAXFIY / KUZATUV**Foydalanuvchi 71001 manzilni takrorlaydi**

Yozuv #205 · xabar #922 Saqlangan fayl kvitasi #209

To'rtta suhbat turli kuzatuvlarni taqdim etadi. Har bir ulanish bo'yicha manba yozuvlarini kuzating; jo'natuvchi aniqlanmagan holda kanal postini 71001 foydalanuvchiga biriktirmang.

Raqamli identifikatorlar va yozuv referensiyalari ushbu qo'llanma uchun ixtiro qilingan. Ushbu xarita qidiruv, profillar va yozuvlarni tekshirish orqali tahlilchining ish jarayonini tushuntiradi; ilova global tergov grafini yaratmaydi.

| Ulanish | Kuzatuvni qo'llab-quvvatlash | Saqlash uchun xulosa |
| --- | --- | --- |
| Xuddi shu Telegram akkaunti | Foydalanuvchi ID 71001 #146 guruhida va #205 shaxsiy suhbatida | Ikkala suhbatda ham bir xil jo'natuvchi ID taqdim etilgan. Haqiqiy dunyo identifikatori esa alohida masala bo'lib qoladi. |
| Takroriy manzil | `pay.example.invalid/new` #146-da, tugma metadatalari #173-da, tahrirlangan post #188 va #205-da | Bir xil manzil to'rt kuzatilgan kontekstda paydo bo'ladi. Bu o'zi uni kim nazorat qilishini aniqlamaydi. |
| Bir xil fayl baytlari | Tugallangan media kvitansiyalari #151 va #209 dagi SHA-256 qiymatlari teng | Saqlangan ikkita ilova bayt darajasida bir xil. Faqat fayl nomlari yoki miniatura rasmlari buni aniqlay olmaydi. |

Foydalanuvchi profillari mualliflarni o'sha suhbatdagi saqlangan xabarlari bilan qamrab oladi va ularni *bir xil ish maydoni*jurnalidagi boshqa suhbatlarga bog'laydi. Ular to'liq a'zolik katalogi emas. Avatar xeshlari alohida mahalliy keshdan olinadi; profil keltirishlari **Parametrlar → Har bir fakt bo'yicha keltirilgan yozuvlar soni** bo'limida sozlanadigan cheklovga ega.

## 5. Ketma-ketlikni qayta tiklang va bo'shliqlarni belgilang

**Suhbatlarda** saqlangan versiyalarni va ularning **Journal yozuvidagi #…** havolalarini tekshiring. **Jurnal** bo'limida **Barcha manbalar** hamda **tahrirlar**, **o'chirishlar** va **qamrov ma'lumotlaridan** foydalaning. Telegram sanasi va yig'uvchining kuzatuv vaqtini hisobga olgan holda ish kronologiyasini tuzing.

1. 09:00 · #101**Kanal posti qayd etildi**

   Asl manzil saqlanadi.
2. 09:12 · #146 / #151**Guruh boshqa havolani taqdim etadi**

   Foydalanuvchi 71001 uni joylaydi; ilova yuklab olinadi.
3. 09:16 · #173**Bot bir xil manzilni ko'rsatadi**

   Saqlangan klaviatura metama'lumotlari havolani o'z ichiga oladi.
4. 09:20 · #188**Kanal e'lonidagi o'zgarishlar**

   Asl va tahrirlangan kuzatuvlar ikkalasi ham saqlanadi.
5. 09:24 · #205 / #209**Shaxsiy keyingi kuzatuv uni takrorlaydi**

   Saqlangan ilova #151 bilan bir xil to'liq SHA-256 ga ega.
6. 09:28 · #231**Guruhni o'chirish to'g'risidagi bildirishnoma keladi**

   Avvalgi kuzatuv hanuzgacha amalda; na o'chiruvchi, na aniq o'chirish vaqti taqdim etilmagan.

Illyustrativ kuzatuv vaqtlari va manbalari. Ushbu yozuvlar orasida boshqa jurnal yozuvlari mavjud.

Jurnal ketma-ketligi kelib tushish tartibini ko'rsatadi, lekin albatta Telegram'dagi asl harakatlar tartibini emas. Yangi jonli xabar oldinroq olingan tarixiy snapshot'dan keyin kelishi mumkin. Jonli kuzatuvlar, snapshot'lar, tiklangan xabarlar, o'chirish bildirishnomalari va "qayta tekshirishda yo'qolgan" holatlarini alohida saqlang. Qamrovda bo'shliq ko'rinadigan har joyga aniq noma'lum oraliqni qo'shing; keyingi snapshot bu bo'shliqni bekor qilmaydi.

## 6. Ishni boshqa yig'ish hisoblariga ham kengaytirish

Har bir alohida akkaunt uchun ish maydonini qo'shing va doira hamda tarix inventarizatsiyasini takrorlang. Har birining a'zolik/rol va imzolash kaliti barmoq izini qayd eting. Identifikatorlarni ish maydoni va suhbat bo'yicha aniqlang: bir xil xabar raqami global akkauntlararo identifikator hisoblanmaydi.

Holat yozuvlaringiz yoki tahlil vositalaringizdagi tegishli kuzatuvlarni har bir qatordagi hisob va jurnal ma'lumotlarini saqlagan holda solishtiring. TgWitness hozirda ish maydonlari bo'ylab yagona qidiruv, birlashtirilgan vaqt chizig'i, odamlar grafi yoki ish hujjatlari arxivini taqdim etmaydi. Bitta kanal yoki superguruhning ko'p hisobli to'liq eksporti alohida xususiyat bo'lib, bu barcha hisob jurnallarini birlashtirish emas.

Uzoq muddatli ish davomida avvalgi chegaralarni saqlab qolish uchun [mustaqil guvoh](https://phishdestroy.github.io/TgWitness/uz/docs/witness/)ni qo'shing. Hisoblarning qamrab olish yo'llari va ko'rinishini aniqlash uchun boshqariladigan yetkazib berish pilotidan foydalaning.

## 7. To'liq, tekshirilishi mumkin bo'lgan ish paketini yetkazib bering

Har bir ish maydonidan imzolangan jurnal ZIP-faylini eksport qiling. U panel qidiruv filtrlaridan qat'i nazar to'liq yozib olingan jurnalni o'z ichiga oladi. Tegishli odamlar profillarini alohida eksport qiling, har bir to'liq suhbat tarixi paketini saqlang va to'liq ilova dalillarini saqlang.

```
CASE-001/                         # assembled by the analyst
  case-notes.md                   # question, findings, alternative explanations
  sources.csv                     # every chat, role, acquisition result and gap
  timeline.csv                    # account + chat + message + seq + both times
  workspace-A/
    evidence.zip                  # complete signed observation journal
    retained-checkpoint.json
    profiles-operations.json      # separately signed people profiles
    history-channel.zip           # signed current-history export
    history-group.zip
    verification.txt
  workspace-B/                    # separate journal and trusted fingerprint
  witness/                        # retained checks, journal and signed posts
  SHA256SUMS                      # hashes of the delivered files
```

Ishonchli barmoq izlarini alohida kanal orqali saqlang. Ishonchli o'rnatishdan, har bir artefaktni uning o'z ish maydoni identifikatori bo'yicha tekshiring:

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
python -m tgwitness.verify profiles-operations.json --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --evidence evidence.zip
python -m tgwitness.verify history-channel.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256
```

Haqiqiy verifikatsiya natijalarini tekshiring, asl nusxalarni saqlang va topilmalaringiz bilan birga qamrov hisobotini, olishdagi xatoliklarni hamda uzatish yozuvlarini saqlang. Eng yuqori darajadagi ish papkasi va tahlilchi xulosalari tashqarida tuziladi; alohida TgWitness artefaktlari esa o'z imzolariga ega.

## Boshqa tergovlar uchun ham xuddi shu usulni qo'llang

**Bot tomonidan boshqariladigan buyurtma yoki to'lov bo'yicha nizо**

**Savol:** bot nima va'da qilgan edi, qaysi tugma manzili taqdim etilgan edi va keyin nima o'zgardi?

**Iz:** kanalga yozuv post → saqlangan bot-havola ko'rinishi → bot boshlang'ich parametri → xabarlar va klaviatura versiyalari → har qanday panel tomonidan berilgan callback kvitasi → guruh/shaxsiy keyingi kuzatuv. Har bir manzilni uning manba yozuviga mos keltiring; profil tavsiflarini va yakunlangan media ma'lumotlarini saqlang.

**Taqdim eting:** kuzatilgan taklif va javoblarning vaqt chizig'i, manba havolalari va tasdiqlangan eksportlar. Ko'rsatilgan to'lov havolasi to'lov amalga oshganligiga dalil emas.

**Suhbatlararo hodisadan so'ng o'chirib tashlangan xabarlar**

**Savol:** tegishli xabarlar yo'qolishidan oldin nima allaqachon kuzatilgan edi?

**Iz:** barcha ta'sirlangan suhbatlar → asl xabarlar → yetkazilgan tahrirlar → o'chirish bildirishnomalari yoki keyingi qayta tekshirishda yo'qolish natijalari → saqlangan ilovalar → hodisa atrofidagi qamrov. Mustaqil hisob kuzatuvlarini ularning ko'rsatilgan ko'rinishlari bilan solishtiring.

**Yetkaziladi:** saqlangan versiyalar ketma-ketligi va aniq noma'lum oraliklar. Yo'q bo'lgan tarix xabarini ma'lum bir shaxs uni o'chirganligiga dalil deb qabul qilmang.

**Ishtirokchi bir nechta suhbatlarda ismlarini o'zgartiradi**

**Savol:** nomlar o'zgargan bo'lsa-da, qaysi kuzatilgan faoliyat bir xil Telegram hisobiga tegishli?

**Iz:** raqamli jo'natuvchi ID → saqlangan ism/foydalanuvchi nomi tarixi → javoblar → ish maydonidagi boshqa suhbatlar → tilga olingan manzillar va saqlangan fayllar. Har bir da'vo qilingan bog'lanish uchun manba yozuvlarini tekshiring; o'xshash hisoblarni alohida saqlang.

**Taqdim eting:** manbaga tayanib ko'rsatilgan hisob-faoliyat kronologiyasi va munosabatlar haqidagi alohida gipotezalar. Ism o'xshashligi va avatar pHash – bu taxminlar bo'lib, shaxsni isbotlovchi dalil emas.
