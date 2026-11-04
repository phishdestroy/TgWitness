# Barcha suhbatlarni tergov qiling

Canonical page: https://phishdestroy.github.io/TgWitness/uz/docs/cases/

Kanallar, guruhlar, shaxsiy chatlar va botlar bo'ylab butun bir ish: yig'ing, bog'lang, xronologiyani tiklang, topshiring.

Bitta to'qima hodisa, boshidan oxirigacha. Yig'ish, qidiruv va shaxs profillari yozuvlarni topadi, [Case Board](https://phishdestroy.github.io/TgWitness/uz/docs/case-board/) ularni tartibga soladi, [Report studio](https://phishdestroy.github.io/TgWitness/uz/docs/reports/) taqdim etadi.

KO'RILGAN ISH / O'ZGARTIRILGAN TO'LOV MANZILI

### Bir hodisa. To'rt suhbat. Qoldiq izni qayta tiklash.

Kanal posti botga ishora qiladi. Guruh yangi to'lov havolasi haqida gaplashadi va bot uni ko'rsatadi. Post tahrirlanadi, shaxsiy chat havolani takrorlaydi, guruhdagi xabar yo'qoladi.

Har bir versiyani kim joyladi?Havo kim paydo bo'ldi?Qaysi fayl saqlangan?Nima o'zgardi va qachon?

Tarixni yuklash, AI, MCP, OCR va webhook'lar: [Arxiv bilan ishlash](https://phishdestroy.github.io/TgWitness/uz/docs/archive/).

## 1. Butun hisob bo'ylab qamrovni o'rnatish

Butun hisob doirasi faqat maxsus hisobda. Asosiy hisobga tanlangan chatlar yoki papka beriladi.

1. [Hisobni ulang](https://phishdestroy.github.io/TgWitness/uz/docs/accounts/) o'z ish maydonida. Ish raqami, hisob ID, ish maydoni va kalit barmoq izini yozib qo'ying.
2. **Manbalar → Kuzatuv doirasi → Tergov rejimi**: **Butun hisob**, to'rtala manba turi, **O'z harakatlari**. Har bir yangi chatning profili va oxirgi **200 ta ko'rinadigan xabar**i saqlanadi. **Doirani saqlash** va tasdiqlang.
3. **Chatlarni yuklash** va hisobning chatlar ro'yxati bilan solishtiring. Cheklov 1,000 ta suhbat (**Parametrlar → Hisob ro'yxatidan o'qiladigan chatlar**da 20,000 gacha); undan ortiq chatlar faollashganda ko'rinadi.
4. **Yozib olish sozlamalari** → **Barcha ko'rinadigan faollik**, ilova cheklovlari va disk joyini tekshiring. Boshlang, so'ng bitta xabar, bitta tahrir va bitta o'chirish bilan sinang.

KanalGuruhlarShaxsiy suhbatlarBotlar

BIR AKKAUNT / BIR IMZO KALITI**Tanlangan va akkauntda ko'rinadigan barcha faoliyat → bitta jurnal**

Xabarlar · tahrirlar · o'chirish bildirishnomalari · ko'rinadigan munosabatlar · a'zolik voqealari · o'z harakatlari

"Butun hisob" bu hisob ocha oladigan har bir chat, istisnolardan tashqari. Maxfiy chatlar yo'q. Yangi chatlar paydo bo'lganda qo'shiladi; eski tarix avtomatik yuklab olinmaydi.

## 2. Tarixni olish va fayllarni saqlash

Case Board to'plamini yarating va muhimlarini xatcho'p qiling. Manbalar reyestrini yuriting: chat ID, sarlavha, hisob, rol, jonli yozib olish boshlanishi, tarix natijasi, media natijasi, bo'shliqlar.

| Kerak | Panelda harakat | U nimani taqdim etadi |
| --- | --- | --- |
| Yoqilgan suhbatlardagi tarix | Manbalar → To'liq tarixni yuklash | Mavjud avvalgi xabarlar ish maydonining jurnaliga kiritiladi, to'xtatish/davom ettirish va imzolangan ijro hisobotiga ega. [Tarix bo'yicha yo'riqnoma](https://phishdestroy.github.io/TgWitness/uz/docs/reference/history/). |
| Jurnalning mavjud suhbat konteksti | Manbalar → Yozuv sozlamalari → Tarixni snapshot qilish | So'nggi xabarlar imzolangan yozuvlar sifatida. Standart 500, **Parametrlar → Eng katta tarix snapshot'i**da 10,000 gacha. |
| Hozirda ko'rinadigan bitta suhbatning to'liq tarixi | To'liq suhbat eksporti → To'liq suhbatni eksport qilish, yoki Suhbatlar → Suhbatni eksport qilish | `chat.json` va `chat.html` bilan alohida imzolangan to'plam, har bir chatga bittadan. |
| Yangi suhbat paydo bo'lganda kontekst | Kuzatuv doirasi → Yangi suhbat yoki bot paydo bo'lganda | Uning profili va 1,000 tagacha so'nggi xabar (Tergov rejimida 200). Mavjud chatlarga qo'llanmaydi. |
| Ilova baytlari | Ko'rinadigan ilovalarni yuklab oling + har bir tur bo'yicha limitlar | SHA-256 va o'lcham bilan `media.saved` ni qidiring. Navbatda, o'tkazib yuborilgan yoki muvaffaqiyatsiz saqlanmaganini bildiradi. |

Chat eksporti jurnal yoki shaxs profillariga kirmaydi. TgWitness ichida eski tarixni qidirish uchun **To'liq tarixni yuklash** yoki snapshot'lardan foydalaning.

Bu yerda: kanal, guruh, bot chati va shaxsiy chat, shuningdek hisob-faktura fayli va uning xeshi. Yozib olishdan oldin o'chirilgan narsa yo'qolgan.

## 3. Rivojlanayotgan suhbat va o'z harakatlaringizni saqlang

Ishlashda davom etsin. Qizg'in chatlarni ustuvorlik uchun yulduzcha bilan belgilang, **Yozib olish sozlamalari → Qayta tekshirish**da qayta tekshirishni sozlang va `recheck.completed`, FloodWait hamda media natijalarini kuzating.

**Chatlar → Profil → Profilni hozir saqlash** chat tavsifi, bot buyruqlari va boshqa metama'lumotlarni saqlaydi.

**Botni yoki taklifni ish yurituvi doirasida kuzatish**

1. **Chatlar → Telegram havolasini ochish**, avval oldindan ko'rishni saqlang. Havola va oldindan ko'rish imzolangan yozuvga aylanadi.
2. Kerak bo'lsa, **Qo'shilish / ochish va kuzatish** chatga qo'shiladi yoki botni boshlash parametri bilan ishga tushiradi.
3. Harakatni hujjatlashtirish uchun paneldan javob bering yoki **Tugmani bosish**dan foydalaning. Bot javobi bilan `interaction.requested` va `interaction.result` olasiz.

Bular haqiqiy harakatlar. Boshqa ilovada bosilgan tugmalar ko'rinmaydi, faqat bot javobi. Veb-ilovalar, to'lovlar yoki telefon/joylashuv yo'q.

## 4. Suhbatlar bo'ylab odamlar, havolalar va fayllarni kuzatib boring

1. **Jurnal**, **Barcha manbalar**, ibora, domen yoki foydalanuvchi nomini qidiring. Natijalarni oching va **Taxtaga** yuboring.
2. **Chatlar → Odamlar → Profillarni yoqish**, shaxsni tanlang: ismlar tarixi, javoblar, faollik, **Shuningdek…**, havolalar, hamyonlar, telefonlar. Iqtibos keltirilgan yozuvlarni oching.
3. Xuddi shu raqamli foydalanuvchi ID'sini boshqa chatlarda kuzating. Mos ism, hamyon yoki avatar iz, dalil emas.
4. Fayl xeshlarini solishtiring. Bir xil SHA-256 = bir xil baytlar. Ularni kim ulashgani boshqa savol.

ISH XARITASI / MANBALARGA E'TIBOR BERINGBadiiy holat · jonli grafika emas

KANAL / E'LON**Asl → tahrirlangan manzil**

Yozuvlar #101, #188 Xabar #84 · jo'natuvchi aniqlanmagan

GURUH / AMALIYOTLAR**Foydalanuvchi 71001 yangi havolani joylaydi**

Yozuv #146 · xabar #309 Saqlangan fayl kvitasi #151

BOT / BUYURUQ SUHBATI**Bir tugma o'sha manzilga yo'naltiradi**

Yozuv #173 · xabar #12 Tugma metama'lumotlari qaytarildi

MAXFIY / KUZATUV**Foydalanuvchi 71001 manzilni takrorlaydi**

Yozuv #205 · xabar #922 Saqlangan fayl kvitasi #209

To'rtta suhbat turli kuzatuvlarni taqdim etadi. Har bir ulanish uchun manba yozuvlarini kuzating; kanal postining jo'natuvchisi aniqlanmagan.

Raqamli identifikatorlar va yozuv havolalari ushbu bosqichma-bosqich ko'rsatma uchun ixtiro qilingan. Ushbu tushuntiruvchi xarita qidiruv natijalari, profillar va tekshirilgan yozuvlarni qanday bog'lashni ko'rsatadi; Case Board tegishli kartalar va manba havolalarini saqlaydi.

| Ulanish | Kuzatuvni qo'llab-quvvatlash | Saqlash uchun xulosa |
| --- | --- | --- |
| Xuddi shu Telegram akkaunti | Foydalanuvchi ID 71001 #146 guruhida va #205 shaxsiy suhbatida | Ikkala chatda bir xil yuboruvchi ID. U haqiqatda kimligi boshqa savol. |
| Takroriy manzil | `pay.example.invalid/new` #146-da, tugma metadatalari #173-da, tahrirlangan post #188 va #205-da | Bir xil havola to'rt joyda. Uni kim boshqarishi uchun boshqa manbalar kerak. |
| Bir xil fayl baytlari | Tugallangan media kvitansiyalari #151 va #209 dagi SHA-256 qiymatlari teng | Ikkala fayl baytma-bayt bir xil. |

Profillar faqat *bu ish maydoni*da biror narsa yozgan odamlarni qamraydi, a'zolar ro'yxatini emas. Har bir faktga iqtiboslar: **Parametrlar → Har bir faktga keltirilgan yozuvlar**.

## 5. Ketma-ketlikni qayta tiklang va bo'shliqlarni belgilang

**Chatlar**da versiyalar, so'ng **Jurnal**da **Barcha manbalar** + **Tahrirlar**, **O'chirishlar**, **Qamrov**. Xronologiyaga ikkala vaqtni yozing: Telegram sanasi va kuzatilgan vaqt.

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

Jurnal tartibi kelish tartibi, voqealar sodir bo'lgan tartib bo'lishi shart emas. Jonli yozuvlar, snapshot'lar, tiklangan xabarlar, o'chirishlar va "qayta tekshiruvda yo'q"ni alohida saqlang va har bir bo'shliqni noma'lum deb belgilang.

## 6. Ishni boshqa yig'ish hisoblariga ham kengaytirish

Har bir hisobga bitta ish maydoni, xuddi shu qadamlar. Har birining rolini va barmoq izini yozing. Xabar raqamlari hisobga bog'liq, shuning uchun doim qaysi ish maydoni va chat ekanini ayting.

[Hisoblar guruhi](https://phishdestroy.github.io/TgWitness/uz/docs/groups/) holatni ko'rsatadi, sozlamalarni ulashadi va hammasini birga eksport qiladi, har biri o'z jurnali va kaliti bilan. Hisoblararo xronologiyani eslatmalaringizda o'zingiz tuzasiz.

Uzoq ishmi? [Mustaqil guvoh](https://phishdestroy.github.io/TgWitness/uz/docs/witness/) qo'shing va har bir hisob haqiqatan nimani ushlashini sinang.

## 7. Tekshiriladigan ish paketini yetkazib bering

Har bir ish maydonidan imzolangan ZIP (doim to'liq jurnal, filtrlar ahamiyatsiz), shuningdek shaxs profillari, chat eksportlari va fayllar.

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

Barmoq izlarini alohida yuboring. Hammasini o'z ish maydoniga nisbatan tekshiring:

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
python -m tgwitness.verify profiles-operations.json --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --evidence evidence.zip
python -m tgwitness.verify history-channel.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256
```

Tekshiruvchi natijasi, asl fayllar, qamrov va topshirish yozuvini topilmalaringiz bilan saqlang. Hisobotni Report studio'da yozing. Qabul qiluvchiga kamroq kerak bo'lsa, [qisqartirilgan topshirish](https://phishdestroy.github.io/TgWitness/uz/docs/handover/) tayyorlang.
