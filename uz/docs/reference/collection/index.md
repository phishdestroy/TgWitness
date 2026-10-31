# Yig'ish qanday ishlaydi

Canonical page: https://phishdestroy.github.io/TgWitness/uz/docs/reference/collection/

Kuzatuv doirasi, jonli yangilanishlar, qayta tekshiruvlar, ilovalar, o'z harakatlari va bo'shliq nima anglatishi, har bir yozuv bo'yicha.

TgWitness ulanib turgan Telegram hisobining kuzatganlarini qayd etadi. Jurnal ushbu kuzatuvlarni, ularning ketma-ketligini va ularga biriktirilgan kontekstni saqlab qoladi. U yo'qolgan xabardan yoki hisob ulanib turganligidan ko'rinmaydigan harakatlarni taxmin qilmaydi.

## Kirishdan jurnalga

Oqim sxemasi · Foydalanuvchi hisobini ruxsat berish → Kirish mumkin bo'lgan guruhlar va kanallarni tanlang; Kirish mumkin bo'lgan guruhlar va kanallarni tanlang → Voqea va ilova sozlamalarini saqlash; Voqea va ilova sozlamalarini saqlash → Kuzatuvni boshlang; Kuzatuvni boshlang → Faol mijozdan yangilanishlarni oling; Faol mijozdan yangilanishlarni oling → Manba va voqea siyosatini qo'llash; Manba va voqea siyosatini qo'llash → Imzolangan kuzatuvni ilova qiling; Imzolangan kuzatuvni ilova qiling → Jurnalni ko'rib chiqing yoki eksport qiling; Imzolangan kuzatuvni ilova qiling → Navbatga qo'yilgan har qanday ilovani qayta ishlang; Navbatga qo'yilgan har qanday ilovani qayta ishlang → Yuklab olish natijasini ilova qiling · Foydalanuvchi hisobiniruxsat berish · Kirish mumkin bo'lganguruhlar va kanallarnitanlang · Voqea va ilovasozlamalarini saqlash · Kuzatuvni boshlang · Faol mijozdanyangilanishlarni oling · Manba va voqeasiyosatini qo'llash · Imzolangan kuzatuvniilova qiling · Jurnalni ko'ribchiqing yoki eksportqiling · Navbatga qo'yilgan harqanday ilovani qaytaishlang · Yuklab olishnatijasini ilovaqiling

**Diagramma matn sifatida**

1. Foydalanuvchi hisobini ruxsat berish → Kirish mumkin bo'lgan guruhlar va kanallarni tanlang
2. Kirish mumkin bo'lgan guruhlar va kanallarni tanlang → Voqea va ilova sozlamalarini saqlash
3. Voqea va ilova sozlamalarini saqlash → Kuzatuvni boshlang
4. Kuzatuvni boshlang → Faol mijozdan yangilanishlarni oling
5. Faol mijozdan yangilanishlarni oling → Manba va voqea siyosatini qo'llash
6. Manba va voqea siyosatini qo'llash → Imzolangan kuzatuvni ilova qiling
7. Imzolangan kuzatuvni ilova qiling → Jurnalni ko'rib chiqing yoki eksport qiling
8. Imzolangan kuzatuvni ilova qiling → Navbatga qo'yilgan har qanday ilovani qayta ishlang
9. Navbatga qo'yilgan har qanday ilovani qayta ishlang → Yuklab olish natijasini ilova qiling

Avtorizatsiya, manbaga kirish, doimiy yig'uvchi va to'liq yetkazib berish – bular turli masalalardir. Muvaffaqiyatli tizimga kirish har bir guruhga kirish huquqini bermaydi. Ulanib turgan transport har bir tegishli yangilanishning yetib kelganini kafolatlamaydi.

## Kuzatuv doirasi: tanlangan suhbatlar, papka yoki butun hisob

Manbalar → **Kuzatuv doirasi** ish maydonchasi qaysi suhbatlarni yozib olishini belgilaydi.

| Rejim | Yozib oladi | Yangi suhbatlar |
| --- | --- | --- |
| Tanlangan suhbatlar (bo'sh) | Faqat qo'lda qo'shgan suhbatlaringiz | Avtomatik qo'shilmagan |
| Telegram papkasi | Hisobning bir papkasi ichidagi suhbatlar: nomiga ko'ra kiritilgan suhbatlar, papka kategoriyalari (kontaktlar, kontakt bo'lmaganlar, guruhlar, kanallar, botlar), chiqarib tashlangan suhbatlar va, agar papkada shunday belgilangan bo'lsa, arxivlangan suhbatlar | Mos keladigan suhbatlar ular faol bo'lishi bilan darhol qo'shiladi; Telegram'da papkaga qo'shgan suhbatlaringiz esa bir soat ichida qabul qilinadi |
| Butun hisob | Hisob ko'radigan har bir suhbat | Har bir yangi chat, guruh, shaxsiy chat yoki bot uning birinchi yangilanishi kelishi bilan qo'shiladi |

- **Manba turlari** (kanallar, guruhlar, shaxsiy suhbatlar, botlar) papkani va butun hisob rejimlarini cheklaydi. Tanlangan suhbatlar istalgan turda bo'lishi mumkin, jumladan shaxsiy suhbatlar va botlar.
- **Chiqarib tashlangan suhbatlar** hech qachon yozib olinmaydi, hech qanday rejimda. Papka va butun hisob rejimlarida manbada *Chiqarib tashlash* yoki *O'chirish* amalga oshirilganda u ushbu ro'yxatga kiritiladi, shuning uchun doira uni qayta qo'shmaydi. Suhbatni manbalarda yoki Suhbatlar bo'limidan qo'lda qayta tanlash uni ro'yxatdan chiqaradi. Ro'yxat 5 000 tagacha suhbatni saqlay oladi; undan ortiq bo'lsa, *O'chirish* rad etiladi va uning o'rniga suhbatni to'xtatib turish mumkin.
- **O'z harakatlari** (tavsiya etilgan holda yoqilgan): ushbu hisob yuboradigan xabarlar, ularning tahrirlari va javob klaviaturasi tugmalarini bosishlar. O'chirilganda, chiquvchi xabarlar va tahrirlar e'tiborsiz qoldiriladi.
- Papkaga yoki butun akkauntga o'tish tasdiqni so'raydi: bu rejimlar uchinchi tomonlarning shaxsiy suhbatlari va xabarlarini yozib oladi va faqat maxsus akkauntda bo'lishi kerak. Tasdiq va har bir doira o'zgarishi imzolangan `scope.changed` yozuvlari bilan qayd etiladi.
- Dastur doirasiga qo'shilgan suhbatlar manba sifatida *"auto"* deb belgilangan holda paydo bo'ladi va ular `scope.applied` (boshlanishda va har soat boshida) yoki `source.discovered` (kuzatish paytida yangi suhbat) bilan yozib olinadi. Tanlangan suhbatlarga qaytish esa har bir avtomatik qo'shilgan manbani to'xtatadi.

Ushbu rejimlar qila olmaydigan narsalar:

- **Maxfiy suhbatlar** ikki qurilma o'rtasida oxirigacha shifrlanadi va hech qachon TgWitnessga yetib bormaydi, hech qanday rejimda.
- **TgWitness ishlamayotgan paytda hech narsa qayd etilmaydi.** Qayta ishga tushirilgandan so'ng u Telegramdan o'tkazib yuborilgan yangilanishlarni so'raydi va suhbatlarni qayta tekshiradi, lekin Telegram uzoq uzilishlardan keyin hamma narsani qaytarib bermaydi. Hisobotlar va `verify.py` bunday davrlarni bo'shliqlar sifatida ko'rsatadi ([qamrovga](https://phishdestroy.github.io/TgWitness/uz/docs/reference/evidence/#coverage-continuity-gaps-and-unobserved-ids) qarang).
- Boshlanishda faqat birinchi 1 000 dialog ro'yxatga olinadi (chegara **Parametrlarda** belgilangan); eski suhbatlar keyingi faollashuvida qo'shiladi. Qo'shilgan suhbatning avvalgi tarixi olinmaydi — kerak bo'lganda tarixni snapshot qilib oling yoki butun suhbatni eksport qiling.
- Doimiy ravishda o'zgarib turadigan papka holatlari (jim, o'qilgan) qo'llanilmaydi: bunday suhbatlar kuzatuvda qoladi.
- **Inline (callback) bot tugmalari** boshqa ilovada bosilganda ikkinchi sessiyada ko'rinmaydi; botning javobi yoki tahriri qayd etiladi. Reply-klaviatura bosishlari chiqish xabarlari sifatida keladi va ularga`button_press` yorlig'i beriladi.
- Ko'proq suhbatlar ko'proq so'rovlarni anglatadi. Telegram o'zining ortiqcha deb hisoblaydigan hajmdagi hisoblarni cheklaydi, bu esa maxsus hisoblardan foydalanish uchun yana bir sababdir.

## Doira va voqealarni tanlash

Har bir ish maydoni o'z manbalariga ega. TgWitness guruhlarga qo'shilmaydi, takliflarni qabul qilmaydi yoki har bir a'zoni avtomatik ravishda sanab chiqmaydi. Manbalar hisobga allaqachon kirish imkoniga ega bo'lishi kerak. Dastur ishga tushirilganda, yig'uvchi tanlangan manbalarni hisobning ko'rinadigan dialoglari bilan solishtiradi; **Parametrlar → Suhbatlar** bo'limida **hisob ro'yxatidan o'qish bo'yicha** boshqa sozlama ko'rsatilmagan bo'lsa, dastlabki 1000 ta dialog tekshiriladi. Mavjud bo'lmagan manba **"kirish tasdiqlanmagan**" deb belgilanadi, uni sizni o'chirib tashlagan deb hisoblanmaydi.

| Sozlamalar | Yig'adi | O'chirib qo'yilganda ta'siri |
| --- | --- | --- |
| Yangi xabarlar | Oddiy yetkazilgan xabarlar | Keyingi tahrirlar/o'chirishlar solishtirish uchun avvalgi yozib olingan matn bo'lmasligi mumkin. |
| Tahrirlar | Tahrirlangan xabar versiyalari yetkazildi | Oraliq o'zgarishlar keyinchalik tiklanmaydi. |
| O'chirishlar | Doiraga kiritilgan o'chirish bildirishnomalari va doiraga kiritilmagan hisob darajasidagi bildirishnomalar | O'chirish bildirishnomalari jurnalga kiritilmaydi. |
| Reaksiyalar | Yetkazilgan reaksiya snopshotlari | Alohida reaktsiya yangilanishlari qo'shilmaydi. |
| A'zolik | A'zolik xizmatlari va ishtirokchilarga oid yangilanishlar xabarlarini yetkazish | Ushbu a'zolik kuzatuvlari qo'shilmagan. |

Sozlamalar ish maydonidagi barcha tanlangan manbalarga qo'llaniladi. O'zgartirishlarni qo'llash uchun shaklni saqlang; o'zgartirishlar imzolangan oldingi/keyingi qiymatlar bilan qayd etiladi. Toifani o'chirish oldingi yozuvlarni olib tashlamaydi. Uni qayta yoqish esa o'tkazib yuborilgan yangilanishlarni to'ldirmaydi.

Operatsion yozuvlar va boshqa guruh xizmat voqealari ushbu kalitlardan alohida bo'lib qoladi. A'zolik xizmati xabarlari a'zolik yoqilganda, hatto oddiy yangi xabarni qabul qilish o'chirilgan bo'lsa ham, xabar yozuvlarini yaratishi mumkin. Qabul qilingan Telegram obyektlari ichiga o'rnatilgan metama'lumotlarni saqlab qoladi; kalit tahrirlash qoidasi emas.

**Shaxsiy suhbatlardagi va oddiy guruhlardagi o'chirishlar** suhbatsiz xabar IDlari sifatida keladi. Ushbu suhbatlar bitta hisob bo'ylab yagona xabar ID ketma-ketligini baham ko'radi, shuning uchun agar shu IDga ega xabar ilgari saqlangan bo'lsa, uning suhbati ma'lum bo'ladi: o'chirish o'sha suhbatda qayd etiladi va buning qanday amalga oshirilganini `chat_resolution` izohlaydi. IDlari hech qachon saqlanmagan **o'chirishlar** aniq noma'lum manba bilan **chegaralanmagan holda** qoladi; to'plovchi taxmin qilmaydi. Telegram hech qachon kim xabarni o'chirganini aytmaydi; agar o'chirilgan xabar ushbu hisob tomonidan yuborilgan bo'lsa, yozuvda shunday qayd etiladi (`deleted_message_was_outgoing`), o'chiruvchini nomma-nom ko'rsatmasdan.

## O'z harakatlari

Kuzatilayotgan akkaunt tomonidan yuborilgan xabarlarda `outgoing` tegisi qo'yiladi. Chiqayotgan xabar tahrirlanganda, shaxsiy suhbatlar va guruhlarda uni faqat muallifi tahrirlashi mumkinligi, kanaldagi postlarni esa boshqa administratorlar ham tahrirlashi mumkinligi qayd etiladi. Chiqayotgan xabar o'sha suhbatdagi eng yangi saqlangan javob klaviaturasi tugmasining matnini takrorlaganda, u klaviatura yozuviga havola bilan`button_press` belgisini o'zida aks ettiradi.

O'z harakatlarini istisno qilish fon tekshiruvlari va avtomatik yangi suhbat tarixiga ham tegishli. O'tkazib yuborilgan chiquvchi xabarlar qayta tekshirish pozitsiyasini oldinga siljitadi, shunda ular keyinchalik keladigan kiruvchi xabarlarni to'sib qo'ya olmaydi. Aniq panel harakatlari va qo'lda so'ralgan tarix snapshotlari yozib qo'yilgan holda qoladi.

## Tergov rejimi: jamoalarga qo'shilish va botlar bilan muloqot qilish

**Manbalar → Kuzatuv doirasi → Tergov rejimi** doirani jamoa suhbatlariga qo'shiladigan, botlarni ishga tushiradigan va ularga xabar yozadigan maxsus hisob uchun tayyorlaydi: butun hisob, har bir manba turi, o'z harakatlari va paydo bo'ladigan har bir suhbat yoki bot uchun uning profili hamda so'nggi 200 ta ko'rinadigan xabari. Formani ko'rib chiqing va "**Domenni saqlash" tugmasini** bosing; butun hisobga o'tish odatdagi tasdiqni so'raydi.

- **Tugmalar.** Xabar ostidagi tugmalar xabar bilan birga saqlanadi va **Söhbatlarda** ko'rsatiladi: havolalar, veb-ilovalar, kirish havolalari, nusxalanadigan matnlar, qaytish ma'lumotlari, ichki so'rovlar, telefon raqami yoki joylashuvni so'rash. Havolalar matn ko'rinishida ko'rsatiladi va panel tomonidan hech qachon ochilmaydi. Bot faqat tugmalarni (masalan, yangi to'lov havolasini) o'zgartirsa, bu jonli yangilanishlar va qayta tekshiruvlar bo'yicha xabar versiyasining yangi versiyasi hisoblanadi.
- **Yangi suhbatlar va botlar.** Papka va butun hisob rejimlarida, **yangi suhbat yoki bot paydo bo'lganda**, paydo bo'lishi bilanoq saqlanadi:

  - `source.profile` yozuvi sifatidagi profili: bot tavsifi va buyruqlari, foydalanuvchi, guruh yoki kanal haqidagi matn a'zolari, Telegram qaytaradigan bog'langan chat va taklif havolasi;
  - uning so'nggi ko'rinadigan xabarlari (1 000 tagacha) tarix snapsoti sifatida `new_chat` belgisi bilan: yaqinda qo'shilgan jamoaviy chatning avvalgi xabarlari yoki bot chatni kuzatishni boshlashidan oldin aytganlari oldinroq saqlangan xabarlar takrorlanmaydi.

  Rejim yoqilganda ro'yxatda allaqachon mavjud bo'lgan suhbatlar snapshotlarsiz qo'shiladi. FloodWait bu ishni to'xtatadi va keyin davom ettiradi; xatoliklar qayd etiladi va suhbatni jonli yozib olish davom etadi. - **Profil so'rovi bo'yicha. Suhbatlar → Profil → Profilni saqlash endi** istalgan manbaning joriy profilini saqlaydi; eng yangisi xabarlar ustida ko'rsatiladi. - **Ko'rinmaydi.** Boshqa Telegram ilovasida bosilgan ichki (callback) tugmalar, botning javobida paydo bo'ladigan pop-up yoki havola, shuningdek boshqa ilovada ishlatilgan taklif havolalari TgWitnessga yetib bormaydi. Bot keyinchalik yuboradigan yoki tahrirlaydigan narsalar yozib olinadi.

### Panel orqali harakat qiling

**Suhbatlar** endi tanlangan ish maydonining Telegram hisobini ishlatadigan mini-klientni o'z ichiga oladi:

- Oddiy matnli xabar yozing yoki saqlangan xabar ostidagi **"Javob berish"**ni tanlang. Jo'natilgan xabar, hattoki doira jo'natilgan yangilanishlarni o'z ichiga olmasa ham, qayd etiladi.
- **Press tugmasini** joriy callback yoki matnli tugma ostida bosing. Server xabarni qayta oladi va klaviatura saqlangan versiyadan farq qilganda harakatni rad etadi. Callback kvitansiyalari Telegramning pop-up matni, ogohlantirish bayrog'i va URL manzilini saqlaydi; javob suhbat ostida ham ko'rsatiladi. URL manzillari tanlanadigan matn bo'lib qoladi va avtomatik ochilmaydi.
- **Telegram havolasini** kengaytiring, `@username`, ommaviy `https://t.me/name` havolasi, `https://t.me/+invite` / `joinchat/invite` yoki `?start=parameter` parametrli bot havolasini kiriting va " **Ko'rinishni saqlash**" tugmasini bosing. Asl havola va Telegramning ko'rinishi qo'shilishdan oldin imzolanadi. **Qo'shilish / ochish va kuzatish** guruh/kanalga qo'shilishni yoki foydalanuvchi/botni ochishni amalga oshiradi, suhbatni yoqilgan manba sifatida qo'shadi va botga uning boshlang'ich parametrini o'z ichiga olgan `/start` buyrug'ini yuboradi. Administrator tasdig'ini kutayotgan qo'shilish so'rovi a'zolik emas, balki kutish holati sifatida qayd etiladi.

Kiruvchi javoblarni jonli ravishda qayd etish uchun **«Kuzatuvni boshlash**»ni yoqing. Kuzatuv to'xtatilgan paytda paneldagi harakatlar ishlaydi, lekin faqat ularning to'g'ridan-to'g'ri javoblari saqlanishi kafolatlanadi. Kuzatuv davom etayotganda yangi qo'shilgan manbalar sozlangan profil/tarixni yig'ishni ishlatadi. Manba to'xtatilganda, uning tugmalarini bosish yoki xabar yuborishdan oldin uni **«Manbalar»** bo'limida yoqing.

`interaction.preview`, `interaction.requested` va `interaction.result` oddiy imzolangan jurnal voqealari bo'lib, ular dalillar eksportiga kiritilgan. So'rovlar hisobni, xabar/tugma yoki ko'rinish yozuvini hamda kuzatuv ishlamoqda bo'lgan-yo'qligini aniqlaydi. Kvitalar muvaffaqiyat, rad etish, tasdiqlanishni kutish va noma'lum natijani ajratib ko'rsatadi. To'xtatilgan so'rov Telegramga yetib borgan bo'lishi mumkin: yangi harakatni boshlashdan oldin suhbatni tekshiring. So'rov ID'sini qayta ishlatish, harakatni takrorlamasdan, qayta ishga tushirgandan keyin ham, uning saqlangan kvitansiyasini oladi. Panel hozirgi sahifa sessiyasi davomida bir xil harakat uchun noaniq javob kelganda ham ID'ni saqlab qoladi. Shuningdek, muvaffaqiyatli harakatdan so'ng ko'rinishni yangilash muvaffaqiyatsiz tugagach ham u shu ID'ni saqlaydi: kvitansiyasi ko'rinib turaveradi va uni yana bosish uni qaytarib oladi. Callback va join RPClar bitta urinishga ega; qayta urinish mumkin bo'lgan o'qishlar o'zlarining sozlangan qayta urinish siyosatini saqlab qoladi. Suhbatlarni almashtirish loyihani va javob maqsadini darhol tozalaydi va yangi suhbat yuklanmaguncha yuborishni o'chirib qo'yadi.

Ushbu mini-klient matn va qaytish chaqiruv tugmalari bilan ishlaydi. Veb-ilovalar, kirish/telefon/joylashuv so'rovlari, to'lovlar, ichki so'rovlar va ilovalar hanuz Telegram klientini talab qiladi; ularning saqlangan tugma metama'lumotlari ko'rinib turadi. Yangi boshqaruv elementlari ingliz tilidagi matndan foydalanadi.

## Qayta tekshirish bosqichlari

Qayta tekshirishlar o'tkazib yuborilgan xabarlar, tahrirlar va Telegram endi qaytarmaydigan xabarlar uchun Telegramga yana murojaat qiladi. Yulduzcha bilan belgilangan manbalar **ustuvor** manbalar bo'lib, ular standart bo'yicha har 15 daqiqada qayta tekshiriladi; boshqa barcha manbalar esa har 6 soatda. Tanlangan suhbatlar ustuvor manbalar sifatida boshlanadi, papka yoki butun hisobga qo'shilgan suhbatlar esa oddiy manbalar sifatida. Har bir tekshirishda maksimal 30 manba qayta tekshiriladi va qolganlari keyingi daqiqagacha kutadi; qayta ulanishdan so'ng, ustuvor manbalar birinchi bo'lib tekshiriladi. Ikkala intervalli ham Manbalar → Yozib olish sozlamalari → Qayta tekshirish bo'limida o'rnatiladi (0 qiymati bosqichni o'chiradi) va `recheck.changed` deb qayd etiladi.

Oʻtkazib yuborilgan xabarlar oldingi tekshirish toʻxtagan joydan yuqoriga qarab olinadi, har bir tekshirish bosqichi uchun **Parametrlar → har bir tekshirishda yangi xabarlar soni** (oʻrnatilgan qiymat boʻyicha 1 000) bilan cheklangan. Uzoq to'xtashdan so'ng qayta tekshiruv bo'shliqni to'liq to'ldiradi, hatto bo'shliqdan keyingi yangi jonli xabarlar avval saqlangan bo'lsa ham. Hali ham xabarlarni yuklab olishda bo'lgan suhbat, o'zining tier intervali kutmasdan, keyingi daqiqada yana qayta tekshiriladi; `recheck.completed` tugaguncha `continues_after` ni ko'rsatadi.

Solishtirishlarga xabar matni, ob'ektlar, klaviaturalar (o'chirishlar ham), hamda ilova kontenti/identiteti kiradi. Faylga kirish hashlarini yoki faylga havolalarni o'zgartirish o'zgartirish hisoblanmaydi, shuningdek Telegramning o'zi to'ldiradigan ma'lumotlar ham: havola oldindan ko'rish yuklanishi, story ko'rinishlari, ushbu hisob orqali ochilgan pullik media, kvitansiyaning rasmiy kvitasi. Söhbatlardagi har bir saqlangan versiya o'zining to'liq jurnal yozuviga, jumladan media metama'lumotlariga havola qiladi.

## Xabarlar tarixi va mansubligi

Faraz qilaylik, yig'uvchi "Uchrashuv soat 10:00 da" deb kuzatadi, keyin "Uchrashuv soat 11:00 da" deb ko'radi va so'ngra o'chirish bildirishnomasini oladi. Bu uch xil kuzatuvni ilova qiladi. Asl matn saqlanib qoladi, tahrir alohida versiya sifatida ajratiladi va bildirishnoma o'chirish kuzatilganini qayd etadi.

Agar yig'ish birinchi versiya yo'qolgandan keyin boshlandi, o'sha matn mavjud emas. Agar jarayon oflayn bo'lgan paytda bir nechta tahrirlar amalga oshirilgan bo'lsa, faqat keyinchalik kuzatilgan versiyalar saqlanishi mumkin. O'chirish bildirishnomasi hech qachon qayd etilmagan kontentni tiklay olmaydi.

Xabar yuboruvchi avtomatik ravishda tahrirchi hisoblanmaydi. Telegram odatda xabarni o'chirgan shaxsni yoki aniq o'chirish vaqtini taqdim etmaydi. Noma'lum shaxslar noma'lum bo'lib qoladi. Reaksiya snopshotlari va ishtirokchi yangilanishlari faqat hisobga Telegram tomonidan ko'rsatiladigan son va identifikatorlarni o'z ichiga oladi.

Ketma-ketlik raqamlari kuzatuv tartibini bildiradi. Yig'uvchining UTC vaqti bo'yicha timestamp uning mahalliy soatidir; Telegram manbaasining timestampi taqdim etilganda alohida saqlanadi. Ikkalasi ham mustaqil ishonchli timestamp hisoblanmaydi.

## Tarix snopshotlari

Snapshot yoqilgan manbadan so'nggi ko'rinadigan xabarlarni, har bir so'rov bo'yicha 500 tagacha so'raydi. Natijalar tarix kuzatuvlari deb belgilangan. Ular jonli yozib olish bilan to'qnashishi mumkin va takroriy kuzatuvlar alohida yozuvlar sifatida saqlanadi.

Snapshotlar ilova siyosatiga rioya qiladi, ammo jonli-voqea kalitlaridan alohida bo'lib qoladi. Ular o'chirilgan xabarlarni yoki o'tkazib yuborilgan oraliq versiyalarni qayta tiklamaydi. To'xtatilgan paytda bittasini so'rashingiz mumkin; u navbatga qo'ygan har qanday ilovalar kuzatuv boshlanib, yuklab olish ishchisi ishga tushguncha kutadi.

## Ilovalar bilan ishlash

Ilovalarni yuklab olish standart bo'yicha yoqilgan va bo'sh disk maydoni 1 GiB dan kam bo'lganda to'xtaydi. Yig'uvchi xabarni kuzatish va yuklab olish ishlarini birgalikda bajaradi. Ish original media tavsiflagichi va o'lcham siyosatini saqlab qoladi, shuning uchun keyinchalik tahrirlangan ilova jimjit almashtirilmaydi.

Yuklab olishlar xabarni ushlagandan keyin amalga oshiriladi. To'liq yakunlangan yuklab olish o'zining SHA-256 hashini va bayt sonini o'z ichiga olgan`media.saved` yozuvini yaratadi. O'tkazib yuborilgan, muvaffaqiyatsiz, qayta urinilgan va to'xtatilgan ishlarning alohida natijalari mavjud. Navbatga qo'yilgan ish fayl saqlanganligiga dalil bo'lmaydi. Yakunlangan fayl shuningdek asl kuzatilgan ilova tavsifnomasidagi bayt soniga mos kelishi kerak. Qisqa yoki kutilmagan darajada uzoq javob saqlangan media sifatida qayd etilmaydi.

Cheklovlar **turga qarab** belgilanadi: fotosuratlar, videolar, GIF va animatsiyalar, aylana video xabarlari, ovozli xabarlari, musiqa va audio, stikerlar va fayllar. Har bir turni o'chirib qo'yish mumkin va ularning har biri 1 dan 2 000 MiB gacha o'z o'lcham chegarasiga ega; yangi ish maydonchalari fotosuratlar uchun 20 MiB, videolar uchun 100 MiB, fayllar, audio va dumaloq videolar uchun 50 MiB, ovozli xabarlar va GIFlar uchun 20 MiB bilan boshlanadi va Stikerlar uchun 5 MiB. *Maksimal fayl o'lchami* barcha turlarga bir vaqtda qo'llaniladi. Har bir tur bo'yicha alohida limitlar belgilanishidan oldin saqlangan siyosatlar har bir tur uchun yagona limitni saqlab qoladi. O'chirib qo'yilgan tur `media.skipped` yozuvini hosil qiladi; noma'lum o'lchamli yoki haddan tashqari katta fayllar yuklab olinmaydi. Katta fayllar kamida 256 KiB/s tezlikda yuklanadi. Ishlar qayta ishga tushirishdan keyin ham saqlanadi, lekin muddati tugagan havolalar, yo'qolgan kirish huquqi yoki o'chirilgan fayllar tiklashga to'sqinlik qilishi mumkin. Mavjud ishlar ularga biriktirilgan siyosatni saqlab qoladi.

## Tanaffus, qulflash, ulanishni uzish va qayta ishga tushirish

| Harakat yoki holat | Ta'sir |
| --- | --- |
| Ish maydonini o'zgartiring | Panel ko'rinishini o'zgartiradi; boshqa to'plovchilar o'z holatini saqlab qoladi. |
| Panelni qulflash yoki yorliqni yopish | Server va kuzatuvni ishga tushirib qo'yadi. |
| Kuzatuvni to'xtatish | Ushbu to'plovchini to'xtatadi va navbatga qo'yilgan ilovalar ishlarini saqlab qoladi. |
| Manbani o'chirish | Kelajakdagi doiraviy ushlab olishni to'xtatadi; unga mo'ljallangan navbatdagi media ishlar to'xtatilgan paytda kutib turadi. |
| Manbani olib tashlash | U manba sifatida uni unutadi va foydalanuvchi profillarini o'chirib tashlaydi; allaqachon saqlangan yozuvlar faqat qo'shib boriladigan jurnalda qoladi. Hali kutayotgan ilovalar (attachments) esa muvaffaqiyatsiz (`source_removed`) deb qayd etiladi. Papka va butun hisob rejimlarida ham u istisno qilinadi. |
| Ulanish yo'nalishini o'zgartiring | Tanaffusni talab qiladi, eski klientlarni yopadi va yakunlanmagan kirishni bekor qiladi. |
| Python jarayonini to'xtating | Barcha ish maydonlarini to'xtatadi; u tarmoqdan tashqarida bo'lganida hech qanday kuzatuv amalga oshirilmaydi. |
| Faol kuzatuvdan so'ng qayta ishga tushiring | Saqlangan sessiya yordamida saqlangan doirani tiklashga urinishlar. Qo'lda pauza qilish bu niyatni bekor qiladi. |

Yig'uvchi aniqlangan ulanish uzilishlari, qayta urinishlar, xatolar, boshlanish/to'xtashlar va yurak urishlarini qayd etadi. Qisqa uzilishlar davriy ulanish tekshiruvlari orqali e'tibordan chetda qolishi mumkin. Qayta ishga tushirilgandan so'ng, saqlangan yangilanish pozitsiyasidan o'tkazib yuborilgan yangilanishlar so'raladi va kuzatilgan suhbatlar muntazam ravishda qayta tekshiriladi; [dalil formatiga](https://phishdestroy.github.io/TgWitness/uz/docs/reference/evidence/#durable-collection-and-process-receipts-02) qarang. Snapshot kontekstni taqdim etadi; u bo'shliq tuzatilganini isbotlamaydi.

## Hisobni izolyatsiya qilish va tasdiqlash

Har bir ish maydoni o'z jurnali, ruxsatnomasi, imzolash kaliti, siyosati va navbatiga ega. Faqat uning faol klienti jonli kuzatuvlarni kiritishi mumkin. Rad etilgan, kutayotgan, yangilangan va ulanish-sinov klientlari uning jurnaliga jonli yangilanishlarni yozolmaydi. Turli hisoblar bir xil guruhni kuzatishi mumkin, lekin ularning jurnallari alohida bo'lib qoladi.

Har bir voqeada avvalgi xesh va Ed25519 imzosi mavjud. Eksportlar belgilangan ketma-ketlik raqami orqali butun ish maydoni jurnalini qamrab oladi. Panel filtrlari eksportni filtrlamaydi; tayyorlanayotgan paytda yig'ish uning chegaralaridan tashqarida ham davom etishi mumkin.

**Jurnal tekshiruvchisi** ko'rsatilgan chegarada voqealar zanjiri va imzo(lar)ni tekshiradi. Natija ish maydoni o'zgarganda tozalangadi va panel tekshiruvdan keyin qo'shilgan yangi yozuvlarni aniqlaydi. ZIP eksporti ham yig'ilgan media ma'lumotlarini tekshiradi.

Amaldagi imzo Telegram kelib chiqishi yoki mazmunining rostligi emas, balki ishonchli kalitga nisbatan yaxlitlikni ta'minlaydi. Barmoq izlari va tekshirish nuqtalarini mustaqil saqlang. Ishonch va yetkazib berish talablari uchun [dalillar model](https://phishdestroy.github.io/TgWitness/uz/docs/reference/evidence/)ini, [kundalik operatsiyalarni](https://phishdestroy.github.io/TgWitness/uz/docs/reference/operations/) va [jonli qabul qilish tartibini](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md) ko'ring.
