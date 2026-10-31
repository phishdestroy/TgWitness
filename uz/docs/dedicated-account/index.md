# Alohida hisobdan foydalaning. Aslo asosiy hisobingizni emas.

Canonical page: https://phishdestroy.github.io/TgWitness/uz/docs/dedicated-account/

Hisobni bog'lashdan oldin o'qing

Asosiy hisobingizdan foydalanmang, degan maslahatimiz hazil emas. Bu haqiqat.

Asosiy hisob

- Sizning ilova xeshingiz: 99% tizimdan chiqib ketgan
- Faqat past ishonchlilik tufayli taqiqlar tez-tez uchraydi
- Undan foydalanish juda ahmoqona g'oya

Jamoat juftliklaridagi qo'shimcha hisob

- Ushbu juftliklar orqali bir milliondan ortiq hisob yozilgan
- Juftliklar 5 yildan ortiq vaqtdan beri faol
- Ular orqali hech kim sizning hech narsangizni ko'ra olmaydi

01

## Nega asosiy hisobingiz emas

Bu aniq ma'lumot. Biz bu muammolarning xavfli joylari aynan qaerda ekanligini bilamiz.

1. ### Sizning ilova xeshingiz: 99% tizimdan chiqib ketgan

   Kirish huquqingiz bo'lmagan hisobdan my.telegram.org saytiga kirib, ilova hashini olish va keyin shu ilova hashiga asoslangan har qanday so'rov hisobingizni 99% ehtimol bilan tizimdan chiqarilgan bo'lishiga olib keladi. Buni tekshirishingiz mumkin.
2. ### Faqat past ishonchlilik tufayli taqiqlar tez-tez uchraydi

   Hisoblar Telegram ularga ishonmaydiganligi sababli oddiygina taqiqlanadi, va bunday taqiqlar tez-tez uchraydi. Buni ham tekshirishingiz mumkin. O'zingizning hisobingizdan foydalanish juda ahmoqona g'oya.
3. ### Ko'chirilgan sessiya kalitlari bekor qilinishi mumkin

   Import qilingan TData/session kalitini Telegram Desktop va TgWitness'da bir vaqtda ishlatish `AUTH_KEY_DUPLICATED` xatosini keltirib chiqarishi mumkin. Telegram ushbu ruxsatnomani bekor qiladi, shuning uchun har ikkala nusxa uchun yangi kirish talab etiladi. Alohida hisob bu muammoni bartaraf etmaydi.

   Asl klientdan to'liq chiqib, import qilingan sessiyadan foydalanganda uni yopiq holda saqlang. Paralel foydalanish uchun telefon yoki QR orqali TgWitnessga alohida ruxsatnoma yarating; boshqa alohida ruxsatnomaga ega klientlar esa tizimda qolishi mumkin.

   [Sessiyani import qilish bo'yicha ogohlantirishni o'qing](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=uz#session-warning)

Telegram hujjatlari

- [Chiqish xatolari: AUTH_KEY_UNREGISTERED, SESSION_REVOKED](https://core.telegram.org/api/errors)
- [O'zingizning ilova xeshini yaratish: api_id olish](https://core.telegram.org/api/obtaining_api_id)

02

## Nega TgWitness jamoat ilova xesh/ilova ID juftliklari orqali ishlaydi

Shuning uchun biz TgWitness-ni ommaviy ilova hash/ilova ID juftliklari asosida yaratdik. Bizning mantiqimizga ko'ra, ular bilan taqiqlanish ehtimoli kamroq: bu juftliklar orqali milliondan ortiq Telegram akkauntlari ro'yxatdan o'tkazilgan va turli dasturlar ular orqali ishlaydi. Bizning mantiqimizga ko'ra, bu shaxsiy ilova xeshidan to'g'ridan-to'g'ri foydalanishdan afzalroq: bu juftliklar kamida 5 yildan beri mavjud.

### O'zingizning yangi juftligingiz

Hisobingizdan my.telegram.org saytida yaratilgan.

- Hisoblarning taxminan 99% logout qilingan
- Bir yangi ilova, bitta hisob

### Poolning jamoat juftliklari

Ko'pgina dasturlar ishlatadigan bir xil juftliklar.

- Bir milliondan ortiq hisob yozilgan
- Ko'plab turli dasturlar
- 5 yildan ortiq ishlaydi

### Nega hech kim ushbu juftliklar orqali sizning hech narsangizni ko'ra olmaydi

- #### Juftlik — bu nom, kalit emas

  Telegram dastur ulanayotganda va kirish kodini so'rayotganda API ID hamda API xeshini so'raydi. Ular ilovani aniqlaydi va hech qanday akkauntga kirish huquqini bermaydi; Telethon hujjatlarida bitta juftlik istalgan telefon raqami bilan ishlashi qayd etilgan.
- #### Sizning sessiya kalitingiz hech qachon serveringizdan tashqariga chiqmaydi

  Kirish Diffie–Hellman almashinuvi orqali sizning TgWitness va Telegram o'rtasida avtorizatsiya kalitini yaratadi; kalitning o'zi hech qachon yuborilmaydi. Telegram hujjatlariga ko'ra: avtorizatsiyadan so'ng kalit foydalanuvchi bilan bog'lanadi va ushbu kalit bilan qilingan har bir chaqiriq shu foydalanuvchi sifatida bajariladi. Xuddi shu juftlikka ega boshqa dasturlarning o'z kalitlari bo'ladi va ular siznikini ishlata olmaydi.
- #### Trafik sizning kalitingiz bilan shifrlanadi

  Har bir so'rov va javob sessiyaning ruxsat kaliti bilan shifrlanadi, API xesh bilan emas. API xeshni bilish hech narsani deşifrlamaydi.
- #### Juftlik egasi hech narsa ko'rmaydi

  Telegramda API ID bo'yicha akkauntlar, sessiyalar yoki xabarlarni ro'yxatlaydigan usul yo'q. Juftlik egasi my.telegram.org saytida faqat o'z ilova sozatuvlarini ko'radi.
- #### Faqat sizning hisobingiz qaysi ilova ekanligini ko'radi

  Sozlamalar → Qurilmalar bo'limida sizning hisobingizdagi har bir sessiyaning ilova nomi va API IDi, qurilma, IP manzili hamda sanalari ko'rsatiladi. Hech kim boshqa bu ro'yxatni ko'rmaydi.

Telegram hujjatlari

- [Foydalanuvchini avtorizatsiya qilish: kalit foydalanuvchiga aylanadi](https://core.telegram.org/api/auth)
- [auth.sendCode: api_id, api_hash](https://core.telegram.org/method/auth.sendCode)
- [Ulanishni boshlash](https://core.telegram.org/method/initConnection)
- [Ruxsat kalitini yaratish](https://core.telegram.org/mtproto/auth_key)
- [MTProto shifrlash](https://core.telegram.org/mtproto/description)
- [account.getAuthorizations](https://core.telegram.org/method/account.getAuthorizations)
- [Sessiya yozuvi nimani o'z ichiga oladi](https://core.telegram.org/constructor/authorization)
- [api_id olish](https://core.telegram.org/api/obtaining_api_id)
- [Telegram ilovalarining ochiq manba kodi](https://telegram.org/apps#source-code)

Kutubxonalar va muhokamalar

- [Telethon: tizimga kirish](https://docs.telethon.dev/en/stable/basic/signing-in.html)
- [opentele: rasmiy ilova API-lari](https://opentele.readthedocs.io/en/latest/documentation/authorization/api/)
- [opentele: TelegramClient](https://opentele.readthedocs.io/en/latest/documentation/telethon/telegramclient/)
- [Stack Overflow: api_hashni maxfiy saqlash kerakmi?](https://stackoverflow.com/questions/49490818/should-telegram-api-hash-be-kept-secret)

### Boshqa dasturlardagi xuddi shu juftliklar 7

Rasmiy Telegram ilovalari juftliklari ommaviy bo'lib, ko'plab mustaqil dasturlar va kutubxonalarga kiritilgan:

- [opentelePython · src/api.py](https://github.com/anmv/opentele/blob/4df17bd8c443d6452afc5a2d29ec7922fad1a5c3/src/api.py#L575)

  - Desktop 2040
  - Android 6
  - Telegram X 21724
  - iOS 10840
  - macOS 2834
  - Web 2496
- [opentele2Rust · opentele2-core/src/api.rs](https://github.com/DedInc/opentele2/blob/7e973bc71cd7a714ad13ac703c0895a90d36a735/crates/opentele2-core/src/api.rs#L641)

  - Desktop 2040
  - Android 6
  - Telegram X 21724
  - iOS 10840
  - macOS 2834
  - Web 2496
- [GrampoPython · Grampo/ut/api.py](https://github.com/abbas-bachari/Grampo/blob/00aa662d853c4ac2180432371c5e0d9444bbfe9e/Grampo/ut/api.py#L526)

  - Desktop 2040
  - Android 6
  - Telegram X 21724
  - iOS 10840
  - macOS 2834
  - Web 2496
- [tgmanagePython · api/schemas/api_app.py](https://github.com/xdsnich/tgmanage/blob/f67c46be0ab234bd04526a8663d3936bd98a8597/api/schemas/api_app.py#L47)

  - Android 6
  - iOS 8
  - Desktop 2040
  - macOS 2834
  - Telegram X 21724
  - Web K 2496
- [LyChatBotTDLib · helpers/tdlib/index.js](https://github.com/LyoSU/LyChatBot/blob/fac0ae5d5f2cddb8a26312014f51c0f6f40ec191/helpers/tdlib/index.js#L11)

  - macOS 2834
- [hsadasdPython · config.py](https://github.com/herobrinovaleksandr-png/hsadasd/blob/6842c74895038c16e219324fcd07dbe8153f37f0/config.py#L68)

  - Desktop 2040
  - Desktop 17349
  - Telegram X 21724
  - macOS 2834
  - iOS 10840
  - Web 2496
  - +4
- [blb.teamblb.team/threads/…294](https://blb.team/threads/app-hash-app-id-ofitsial-nykh-kliyentov.294/)

  - Android 4 · 5 · 6
  - iOS 8
  - Desktop 2040
  - Desktop 17349
  - macOS 2834
  - Telegram X 21724

  Forumda hisoblarni ro'yxatdan o'tkazish uchun e'lon qilingan rasmiy ilova juftliklari ro'yxati

03

## Qo'shimcha hisob yaratish usullari

Telegram hisobiga kirish kodini qabul qiladigan telefon raqami kerak. Hisob qancha vaqt davomida faol bo'lishi kerakligini tanlang.

- Eng yaxshi tanlov

  ### Oldindan to'langan SIM yoki eSIM

  ********

  So'nggi

  Uni doim to'ldirib tursangiz

  Diqqat qiling

  Eng ishonchlisi: Telegram haqiqiy mobil raqamlarni eng yaxshi qabul qiladi. Operator qaytarib olgan raqam boshqaga tegishli bo'ladi.
- ### Virtual raqam ilovasi

  ********

  So'nggi

  Ilova raqamni saqlab turgan paytda

  Diqqat qiling

  Telegram virtual raqamni rad etishi, kodni yetkazmasligi yoki yangi hisobni darhol cheklashi mumkin; ba'zi ilovalar esa ishlatilmayotgan raqamlarni qaytarib oladi.
- ### Raqam ijarasi

  ********

  So'nggi

  Ijara muddati

  Diqqat qiling

  U tugagach, raqam keyingi mijozga oʻtadi.
- ### Bir martalik faollashtirish

  ********

  So'nggi

  Bir kod

  Diqqat qiling

  Raqam darhol havzaga qaytadi, ko'pincha avvalgi egalarining tarixi bilan. Boshqa hech narsa qilmasdan oldin bulut parolini o'rnating.

Keyinchalik raqamni egallagan shaxs kirish kodini so'rab olishi mumkin. Bulutli parol (ikki bosqichli tekshiruv) ularning tizimga kirishini to'xtatadi; u bo'lmasa, hisob raqamning keyingi egasiga tegishli bo'ladi.

Telegram hujjatlari

- [Spam FAQ: virtual raqamlar va avvalgi egalar](https://telegram.org/faq_spam)
- [Ikki bosqichli tasdiqlash](https://core.telegram.org/api/srp)

### Ijara +888 raqamlari (Fragment)

Ba'zi bozorlar va xizmatlar Fragment'dan Telegram'ning rasmiy +888 raqamlarini vaqtincha ijaraga olishni taklif qiladi.

Taxminiy narxi: kuniga 20 AQSh dollari.

- Hisobni bevosita Telegram Web yoki Telegram Desktop'da ro'yxatdan o'tkazishingiz mumkin.
- Hisoblarni raqam bo'yicha o'chirib, yangi hisoblar yaratishingiz mumkin.
- Ushbu hisoblar odatda kamroq firibgarlikka qarshi tekshiruvlardan o'tadi, lekin ular immunitet yoki maxsus imtiyozlar bermaydi.

Raqam sizniki emas. Ijara muddati tugagach, egasi uni qaytarib olishi mumkin. Darhol bulut parolini o'rnating va hisobni uzoq muddatli deb qabul qilmang.

+888 raqamiga o'zingiz egalik qilish yoki nazorat qiladigan oldindan to'langan SIM-kartadan foydalanish hanuzgacha ishonchliroq.

### Bozorlardagi tayyor akkauntlar

Ba'zi bozorlar (masalan, G2G yoki Z2U) tayyor Telegram hisoblarini – yangi, yoshi kattaroq yoki sessiya fayllari bilan – sotadi.

- [G2G: Telegram hisob ro'yxatlari](https://www.g2g.com/uk/categories/telegram-accounts)
- [Z2U: Telegram hisob ro'yxatlari](https://www.z2u.com/telegram/accounts-5-15140)

ASLO ASOSIY HISOBINGIZDAN FOYDALANMAING! Shu tarzda olingan maxsus hisob TgWitnessga asosiy Telegram hisobingizni kiritishdan ancha xavfsizroqdir.

#### Sotib olishdan oldin ogohlantirishlar

- Bu Telegram Xizmat ko'rsatish shartlarini buzadi.
- Ko'plab hisoblar ommaviy ro'yxatdan o'tkazilgan (avtomatik ro'yxatdan o'tkazish) yoki ularning tarixi noma'lum.
- Ba'zi sotuvchilarda hali ham tiklash huquqi bo'lishi mumkin.
- Bunday bozorlardagi hisoblar keyinchalik tez-tez taqiqlanadi yoki cheklanadi.
- Ochiqchasiga stealerlar, phishing vositalari yoki aniq o'g'irlangan hisoblarni sotadigan bozorlardan qoching.
- Hisob sotib olish — hattoki avtomatik ro'yxatdan o'tkazilgani aytilgan bo'lsa ham — phishlash vositalari, ma'lumot o'g'irlash dasturlari, o'g'irlangan sessiyalar yoki hisoblarni ochiqchasiga sotadigan platformalardan Telegram Xizmat ko'rsatish shartlarini hamda aksariyat mamlakat qonunlarini buzadi. Bu keyinchalik dalillaringizni bekor qilishi mumkin. Ehtiyotkorlik bilan tanlang.

#### Agar ushbu opsiyani ishlatsangiz

1. Hisobni bir martalik deb qabul qiling.
2. Boshqa barcha sessiyalarni tugating, bulut parolini o'rnating va tiklash usullarini darhol o'zgartiring.
3. Turli provayderlarning yoki o'zingiz ro'yxatdan o'tkazgan 2–3 ta akkauntdan foydalaning.

**Premium, o'chirish va yetti kunlik kechikish**

Agar hisob Premium bo'lsa, telefon raqamiga kirish huquqiga ega kishi hisobni darhol o'chira olmaydi. Siz bildirishnoma olasiz va o'chirishdan oldin yetti kuningiz bor.

Bu muhim, chunki tergov hisobga bog'liq: sizda zaxira tayyorlash uchun vaqt bor.

**Yangi hisoblar va API ma'lumotlari**

Agar siz SMS xizmatidan olingan raqam yordamida o'zingiz ro'yxatdan o'tkazgan yangi akkauntdan o'zingizning api_id/api_hashni olib, undan foydalansangiz, birinchi API so'rovi yoki sessiya avtorizatsiyasi paytida akkauntdan chiqarilishingiz mumkin. Tergovni rejalashtirayotganda buni yodda tuting.

04

## Hisob yaratish

Raqamdan birinchi qayd etilgan suhbatgacha.

1. ### Raqam oling

   Hisob uzoq muddat ishlashi kerak bo'lsa oldindan to'langan SIM yoki eSIM; qisqa muddatli ish uchun ijaraga olish yoki bir martalik faollashtirish. Xizmatlar quyida keltirilgan.
2. ### Asosiy hisobingizdan alohida ro'yxatdan o'ting

   Rasmiy Telegram ilovasida asosiy hisobingiz yonida emas, balki alohida qurilma, emulyator yoki telefon profilida ro'yxatdan o'ting.
3. ### Uni bulut paroli bilan qulflang

   Darhol bulut parolini va faqat shu yerda ishlatiladigan tiklash elektron pochtasini belgilang.
4. ### Maxfiylik sozlamalarini yoping

   Telefon raqami **Hech kim**, meni raqamim bo'yicha toping **Mening kontaktlarim**, oxirgi ko'rilgan vaqti, profil rasmlari va bio **Hech kim** yoki **Mening kontaktlarim**; kontaktlarni sinxronlashtirishni o'chirib qo'ying.
5. ### O'zini o'chirib yuborishining oldini oling

   Hisobni o'z-o'zini yo'q qilish muddatini eng uzoq muddatga o'rnating, shunda to'xtatilgan TgWitness sizga hisobingizni yo'qotishga olib kelmaydi.
6. ### Unga neytral profil bering

   Boshqa hisoblaringizdan ism, foto, foydalanuvchi nomi yoki bio olmang, shaxsiy kontaktlar bo'lmasin.
7. ### Uni isitib oling

   Dastlab kuniga bir nechta suhbatga qo'shiling. Shoshilayotgan yangi hisoblar birinchi navbatda cheklanadi.
8. ### Botlar bilan hech narsa ulashing

   Bot uchun hech qachon "Telefon raqamini ulashish" yoki "Joylashuvni ulashish" tugmasini bosmang. Uskunada havolalar va Mini ilovalarni VPN yoki proksi orqali oching.
9. ### Uni TgWitnessga ulang

   O'z ish maydoningizda **Hisob → QR kod** orqali ulaning, so'ng **Manbalar → Tergov rejimi tugmasini** bosing. Ilova – bu siz harakat qiladigan joy, TgWitness esa yozuvdir.

Telegram hujjatlari

- [Ikki bosqichli tasdiqlash](https://core.telegram.org/api/srp)
- [Maxfiylik sozlamalari](https://core.telegram.org/api/privacy)
- [Hisobni o'z-o'zini yo'q qilish](https://core.telegram.org/method/account.setAccountTTL)

05

## Xizmatlar soni

Boshlash uchun variantlar. Mamlakatlar, narxlar va Telegram raqamni o'zgartirishni qabul qiladimi-yo'qligi tez-tez o'zgaradi; to'lov qilishdan oldin tekshiring.

### Oldindan to'langan SIM va eSIM 11

- [SMARTYsmarty.co.uk](https://smarty.co.uk)

  - UK
  - SIM
- [VOXIvoxi.co.uk](https://www.voxi.co.uk)

  - UK
  - SIM
- [iD Mobileidmobile.co.uk](https://www.idmobile.co.uk)

  - UK
  - SIM
- [Threethree.co.uk](https://www.three.co.uk)

  - UK
  - SIM
- [Asda Mobilemobile.asda.com](https://mobile.asda.com)

  - UK
  - SIM
- [Ultra Mobileultramobile.com](https://www.ultramobile.com)

  - US
  - Oldindan to'langan

  PayGo rejasi, juda arzon
- [US Mobileusmobile.com](https://www.usmobile.com)

  - US
  - Oldindan to'langan
- [Mint Mobilemintmobile.com](https://www.mintmobile.com)

  - US
  - Oldindan to'langan
- [Tracfonetracfone.com](https://www.tracfone.com)

  - US
  - Oldindan to'langan
- [eSIM Plusesimplus.me](https://esimplus.me)

  - eSIM
- [Numero eSIMnumeroesim.com](https://numeroesim.com)

  - eSIM

### Virtual raqam ilovalari 20

- [Google Voicevoice.google.com](https://voice.google.com)

  - US

  Faqat AQSh uchun; ro'yxatdan o'tish uchun AQSh raqami kerak
- [TextNowtextnow.com](https://www.textnow.com)

  - US
  - CA

  Agar undan foydalanmasangiz, raqam bekor qilinadi
- [TextFreetextfree.us](https://www.textfree.us)

  - US
- [2ndLine2ndline.co](https://www.2ndline.co)

  - US
  - CA
- [Talkatonetalkatone.com](https://www.talkatone.com)

  - US
- [TextMego-text.me](https://go-text.me)

  - US
  - CA
  - Boshqa mamlakatlar
- [textPlustextplus.com](https://textplus.com)

  [Google Play](https://play.google.com/store/apps/details?id=com.gogii.textplus)
- [FreeToneGoogle Play](https://play.google.com/store/apps/details?id=com.textmeinc.freetone)

  - US

  [TextMe Up · textmeup.com](https://www.textmeup.com)
- [Nextplusnextplus.me](https://nextplus.me)

  - US
- [Dingtonedingtone.me](https://www.dingtone.me)

  - US
  - CA
- [Burnerburnerapp.com](https://www.burnerapp.com)

  - US
  - CA
  - To'langan

  Sinov davri bilan
- [Hushedhushed.com](https://hushed.com)

  - Ko'plab mamlakatlar
  - To'langan

  Arzon
- [Sidelinesideline.com](https://www.sideline.com)

  - US
- [MySudomysudo.com](https://mysudo.com)

  - US
  - CA
  - UK
- [2NumberGoogle Play](https://play.google.com/store/apps/details?id=com.bpmobile.second.phone)

  [App Store](https://apps.apple.com/app/id1216135390)
- [SLYNUMBERslynumber.com](https://slynumber.com)

  [Google Play](https://play.google.com/store/apps/details?id=com.dev.slynumber)
- [Phonerphonerapp.com](https://phonerapp.com)
- [Onoffonoff.app](https://www.onoff.app)

  - EU

  Ilovadagi Yevropa mobil raqamlari
- [Sonetelsonetel.com](https://sonetel.com)

  - Ko'plab mamlakatlar
  - Bepul raqam
- [Zadarmazadarma.com](https://zadarma.com)

  - Ko'plab mamlakatlar

  Virtual raqamlar

### Ijara va faollashtirishlar soni 12

Ijara bir necha hafta yoki oy davomida raqamni saqlaydi. Bir martalik faollashtirish bitta kod beradi: ro'yxatdan o'tgan zahoti bulut parolini o'rnating.

- [OnlineSimonlinesim.io](https://onlinesim.io)

  - Ijara
  - Faollashtirishlar
- [SMSPVAsmspva.com](https://smspva.com)

  - Ijara
  - Faollashtirishlar
- [5SIM5sim.net](https://5sim.net)

  - Ijara
  - Faollashtirishlar
- [SMSPoolsmspool.net](https://www.smspool.net)

  - Ijara
  - Bir martalik
- [VAK-SMSvak-sms.com](https://vak-sms.com)

  - Ijara
  - Faollashtirishlar
- [TextVerifiedtextverified.com](https://www.textverified.com)

  - Ijara
  - Faollashtirishlar
- [JuicySMSjuicysms.com](https://juicysms.com)

  - Ijara
  - Faollashtirishlar
- [365SMS365sms.org](https://365sms.org)

  - Ijara
  - Faollashtirishlar
- [SIMSMSsimsms.org](https://simsms.org)

  - Ijara
  - Faollashtirishlar
- [GrizzlySMSgrizzlysms.com](https://grizzlysms.com)

  - Bir martalik
- [SMS-MANsms-man.com](https://sms-man.com)

  - Bir martalik
- [Tiger SMStiger-sms.com](https://tiger-sms.com)

  - Bir martalik
