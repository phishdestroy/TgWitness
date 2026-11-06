# Hisobotni sozlash va tekshirish

Canonical page: https://phishdestroy.github.io/TgWitness/uz/docs/reference/case-reports/

Hisobot filtrlari, sakkizta dizayn, kontent uchun oldindan belgilangan sozlamalar, saqlangan o'zgarish tarixlari va imzolangan eksportlarga kiritilgan baholash.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Hujjatlash](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Tergov](https://phishdestroy.github.io/TgWitness/uz/docs/reference/investigation/)

![Tergov](https://phishdestroy.github.io/TgWitness/assets/chapter-investigate.svg)

Tanlangan kuzatuvlarni ishning o'qiladigan hisobotiga aylantiring: uning savoli, doirasi, saqlangan o'zgarishlari, diagrammalari, topilmalari va manba havolalari. Har bir hisobot qabul qiluvchiga yetkazilgan materialni tekshirish va uning to'plam qamrovini ko'zdan kechirish imkonini beradi.

**Ishonch va cheklovlar** bo'limi jurnal, topshirish, suhbat, hisob va ulashish hisobotlarida paydo bo'ladi. Jurnal va topshirish bo'yicha PDF-fayllar imzolangan `report.json`-fayl bilan bir xil baholashdan foydalanadi. ZIP manifestlari imzolangan manifestda `case_assessment` ni o'z ichiga oladi. Ushbu baholash eksport qilingan material bilan birga yuboriladi. Asl kuzatuvlar o'z mavjud imzolarini saqlab qoladi.

## Hujjat formatlari va o'qish tartibi

### Report studio

**Exportlarni** oching **→ Sozlash va ko'rinishni ko'rish**. **Ma'lumotlar → Dizayn va mazmun → Ko'rinish** bo'ylab ishlang:

1. Butun ish maydonini yoki suhbatlar, mualliflar, UTC kuzatuv sanalari va voqea turlarini tanlang. Suhbatlar va mualliflarni qidirish uchun katalogni yuklang yoki ularning Telegram IDlarini kiriting. Muallif filtrlari yozib olingan jo'natuvchi IDlariga mos keladi; jo'natuvchisiz o'chirish bildirishnomasiga muallif filtri mos kelmaydi.
2. Sahifa dizaynini tanlang, so'ngra grafikalarni, ishtirokchilar yorliqlarini, transkriptni va yozma xulosalaringizni tanlang. Dizaynni o'zgartirish ushbu tanlovlarni saqlab qoladi.
3. Ko'rinishni tuzing. U haqiqiy sonlarni, faoliyatni, ishtirokchilarni, namunaviy yozuvlarni, saqlangan o'zgarishlarni va yo'qolgan xabar raqamlari diapazonlarini ko'rsatadi. Tanlovni o'zgartirish ko'rinishni eskirgan deb belgilaydi. HTML, imzolangan PDF, imzolangan JSON yoki dalillar ZIP faylini yuklab olishdan oldin saqlang.

Ma'lumotlarning oldindan ko'rinishi to'liq barqaror jurnal prefiksini hisoblaydi, dastlabki namunani emas. Faqat ko'rsatilgan namunaviy qatorlar va uzun ro'yxatlar chegaralangan; ularning kiritilmagan sonlari ko'rsatiladi. Keyingi eksport yangi barqaror snapshot oladi, shuning uchun davom etayotgan yig'ish raqamlarni oshirishi mumkin. Doira, sonlar va manba identifikatori imzolangan hisobotga kiritilgan. Formani ochish yoki ko'rinishini ko'rish uni saqlamaydi.

**Yurisdiktsiya bo'yicha ko'rsatmalar.** Hujjat tafsilotlari bo'limida **Yurisdiktsiya bo'yicha ko'rsatmalar · ixtiyoriy** bo'limini ochib, yurisdiktsiya hamda fuqarolik/tijorat yoki jinoyat protsedurasini tanlash mumkin. Ilovada huquqiy asos, manba havolalari, tayyorlash eslatmalari va tadqiqot holati keltirilgan. Yig'ishni himoya qilish choralari bo'yicha mahalliy tilidagi qisqacha mazmun va izohlar ixtiyoriy. Hech qanday yurisdiktsiya standart bo'yicha tanlanmaydi. Ushbu tanlovlar ish maydoniga tegishli bo'lib, saqlangan tartib sozlamalari va bilvosita ulashish/nusxa ko'chirish bo'yicha standart parametrlardan chiqarib tashlanadi. Qarang: [standart parametrlar, qo'llab-quvvatlanadigan hisobotlar va tadqiqot cheklovlari](https://github.com/phishdestroy/TgWitness/blob/main/docs/JURISDICTION_GUIDANCE.md) .

**Qabul qiluvchining nusxasini tanlang.** Jadvallar va transkript tanlangan yozuvlardan foydalanadi. To'liqlik, saqlash va qamrov butun manba jurnalini tasvirlaydi. Dalil ZIP hujjati uning asl yozuvlari va ilovalarini o'z ichiga oladi. Qabul qiluvchi faqat tanlangan, ruxsat etilgan ma'lumotlarni olishi kerak bo'lgan hollarda [minimal topshirishdan](https://phishdestroy.github.io/TgWitness/uz/docs/reference/evidence/#handover-extract) foydalaning.

### Tahrirlar, o'chirishlar va yetishmayotgan IDlarni o'qing

Tahrir saqlangan **oldingi** va **keyingi** matnni ko'rsatadi va o'zgartirilgan so'zlarni ajratib ko'rsatadi. O'chirish bildirishnomadan oldin saqlangan oxirgi versiyani ko'rsatadi. Agar ilgari hech qanday kontent qayd etilmagan bo'lsa, hisobot shuni bildiradi. Faqat tahrirlar yoki o'chirishlarni tanlaganingizda, oldingi versiyalar filtrlardan tashqarida aniq belgilangan kontekst sifatida mavjud bo'lib qoladi. Alomat qo'yilmagan xabarlar ushbu tarixlarga qo'shilmaydi.

**Ko'rilmagan xabar IDlari** tanlangan suhbatlardagi ma'lum raqamlar va sana asosidagi ID diapazoni orasidagi bo'shliqlardir. Har bir ma'lum manba yozuvi raqamni ko'rilmagan deb e'lon qilishdan oldin tekshiriladi: boshqa muallifni, voqea turini yoki sanani filtrlash soxta bo'shliq hosil qila olmaydi. Yonma-yon saqlangan xabarlar kontekst deb belgilangan. Yetishmayotgan raqam xabar mavjud bo'lgan yoki o'chirilganligini aniqlamaydi; o'chirish bildirishnomalari va muvaffaqiyatsiz qayta tekshiruvlar alohida hodisa turlari bo'lib qoladi.

### Dizaynni tanlang

Jurnal va yakka suhbat uchun HTML hamda imzolangan PDF hisobotlari uchun sakkiz sahifali dizaynlar mavjud. Ular bir xil yozuvlar va hisob-kitoblardan foydalanadi, ammo muqovalari, tipografiyasi, bob sarlavhalari, jadvallari va bo'shliqlari turlicha.

| Dizayn | O'qish uslubi |
| --- | --- |
| Klassik | Qorong'i muqovali va raqamlangan bo'limlarga ega an'anaviy dosye. |
| Tahririy | Ramkali serifli sarlavha sahifasi, keng marjalar va tor bo'lim paneli. |
| Brifing | Ko'k rangli qattiq muqovali, qisqa sarlavhalar va zich joylashgan jadvallar bilan. |
| Analitika | So'rovnoma uslubidagi muqova, modulli diagramma plastinkalari va monospaced rasmlar. |
| Texnik | Chiziqli ro'yxat, raqamlangan ma'lumotlar poyasi va aniq solishtirish jadvallari. |
| Ushbu dastur foydalanuvchi hujjatlari TgWitness, Telegramni saqlash va tergov dasturi uchun | Panoramik muqova, keng bo'shliq va ko'zga tashlanadigan qisqacha ma'lumot grafikalar. |
| O'qish seriyasi | Topilmalar, doira, o'zgarishlar va kuzatuv jurnali uchun bo'lim paneli va guruhlangan boblar. |
| Ledjer va marja | Keng chekkali raqamlangan boblar, aniq diagramma jadvallari va alohida xabar transkripti. |

Dizayn har bir ish maydoni bo'yicha saqlanadi va imzolangan eksport manifestida qayd etiladi. HTML oflayn ishlaydi, yorug' va qorong'i mavzularni qo'llab-quvvatlaydi hamda tor ekranlar va o'ngdan chapga yoziladigan tillarga moslashadi. Mahalliy PDF-fayllar biriktirilgan shriftlardan foydalanadi; Editorial dizayni o'zining biriktirilgan SIL Ochiq Shrift Litsenziyasi ostida Noto Serifni o'z ichiga oladi. O'qish seriyalari va Ledger & margin hisob ko'rinishlari, hisob suhbatlari va nusxalarni ulashishga ham tegishlidir.

Xitoycha, yaponcha va koreyscha PDF fayllar uchun serverda Noto Sans CJK kabi mos shrift o'rnatilgan bo'lishi yoki u `TGWITNESS_FONT_DIR` papkasiga joylashtirilishi kerak. Agar u mavjud bo'lmasa, ZIP HTML va JSON hisobotlarni saqlaydi.

Ushbu ikki dizayn JavaScript'siz o'qiladigan jurnalni o'z ichiga oladi. Katta eksportlar uchun bu ko'rinish 8 MiB kirish byudjeti doirasida 500 tagacha to'liq yozuvni o'z ichiga oladi; hisobot chegarani belgilaydi va to'liq ko'ruvchi hamda manba yozuvlariga havolalar beradi. Hisob katalogi va munosabatlar indeksi shu o'qish namunasini tasvirlaydi, barcha ishtirokchilarni emas. To'liq jurnal diagrammalari o'z alohida ko'rsatilgan doirasini saqlab qoladi.

### Mavzularni tanlang

| Mavzular oldindan belgilangan | O'rnatilgan holda kiritilgan |
| --- | --- |
| Ish hujjatlari | Faoliyat, kuzatuv vaqtlari, ishtirokchilar, suhbatlar va yozuv transkripti. |
| Brifing | Ishtirokchilarning reytinglari yoki transkriptisiz faoliyat ko'rinishi. |
| Faoliyatni ko'rib chiqish | Faoliyat, kuzatuv vaqtlari, ishtirokchilar, suhbatlar va tarkib, manba havolalari va aniq raqamlar bilan. |
| Moslashtirilgan hisobot | Grafiklar, transkript va ko'rinishlarning o'zingiz tuzgan kombinatsiyasi. |

Oldindan sozlamani o'zgartirish dizayningizni, ish tafsilotlarini va yozma tahlilingizni saqlab qoladi. Butunlik tekshiruvlari, qamrov, cheklovlar va tasdiqlash bo'yicha ko'rsatmalar har bir dizaynda saqlanib qoladi. Jadvali yoki transkripti yashirilganda ZIP-dagi manba yozuvlari o'zgarmay qoladi.

Ixtiyoriy **Tekshiruv eslatmalari** hisobot muallifi tomonidan yozilgan savol, usul, natijalar va xulosani o'z ichiga oladi. Natijalar bo'limida manba faylini va yozuv raqamlarini keltiring. Imzo ushbu muallif bayonotlarini hisobot bilan birga saqlaydi; manba kuzatuvlari va muallifning talqini aniqlanishi mumkin bo'lib qoladi. Minimalizatsiyalangan topshirishlar ushbu shaxsiy eslatmalarni va to'liq jurnal diagrammalarini o'tkazmaydi. Jurnal hisobotlariga diagramma va tekshiruv tanlovlari tatbiq etiladi.

Vaqt bo'yicha faoliyatni, UTC haftaning kunlari/soatlari bo'yicha issiqlik xaritani, ishtirokchilar reytinglarini, suhbat reytinglarini va yozuv tuzilmasini tanlang. 5–30 ta reytingdagi guruh va neytral ishtirokchi taxalluslari yoki hisob IDlarini tanlang. Noma'lum jo'natuvchilar va qolgan ishtirokchilar alohida qatordir. Taxalluslar faqat diagrammalarga ta'sir qiladi; manba yozuvlari hanuzgacha ularning shaxsiyatini o'z ichiga oladi.

Dizayn ko'rinishi saqlanmagan loyihadan ishlab chiqarish muqovasi, tekshiruv va grafik komponentlaridan foydalangan holda yangilanadi, birinchi 50 000 manba yozuvidagi mos keluvchi yozuvlar bilan cheklangan. Quyidagi ma'lumotlar ko'rinishi to'liq tanlovni hisoblaydi. U aniq imzolanmagan va tahrirlarni saqlamaydi. Muqova va Grafikler tugmalari uning bo'limini almashtiradi. Bu to'liq PDF ko'rinishi emas. **Hisobot sozlamalarini saqlash** tanlovlarni kelgusi eksportlarga qo'llaydi; mavjud imzolangan fayllar o'zgarmasdir. PDF tanlangan muqova, tipografiya, bob tartibi va HTML hamda imzolangan JSON dagi kabi bir xil tanlangan agregatlardan foydalanadi.

Ishonchni baholash, qamrov cheklovlari va tekshirish bo'yicha ko'rsatmalar saqlanib qoladi. Grafiklarni yoki o'qiladigan transkriptni yashirish ZIP-dan vakolatli manba qatorlarini olib tashlamaydi. O'chirib qo'yilgan grafik seriyalari analitik JSON-dan chiqarib tashlanadi; manba yozuvlarini oshkor qilishni cheklash uchun minimallashtirilgan eksportdan foydalaning.

Ma'lumot tanlash filtrlari jurnal hisobotlariga qo'llaniladi; hisob va ulashish eksportlari o'zlarining olish va oshkor qilish doirasini saqlab qoladi.

Ushbu dizayn/diagramma sozlamalari yangi suhbat/hisob eksportlariga va hisob ulashish oldindan ko'rishlariga muhrlanadi. Hisob/ulashish tili va maxfiylik sozlamalari mustaqil bo'lib qoladi; shaxsiy ish va tekshiruv eslatmalari ushbu eksportlarga nusxa ko'chirilmaydi. Hisob va ulashish hisobotlari o'zlarining imzolangan arxiv manifesti bilan HTML shaklida himoyalangan bo'lib qoladi. Jurnal, minimallashtirilgan jurnal topshiruvi va yakka suhbat to'plamlari ham imzolangan PDF-fayllarni taqdim etadi.

### Jadvalar nima sanaydi

Jurnal faoliyati va issiqlik xaritalari yangi, tarixiy, tiklangan, tahrirlangan, o'chirilgan va qayta tekshirishda yo'qolgan **kuzatuvlarni** UTC bo'yicha yig'uvchi kuzatuv vaqtiga qarab hisoblaydi. Heartbeats va ilova kvitansiyalari hisobga olinmaydi. Ishtirokchi reytinglari faqat yangi, tarixiy va tiklangan xabar kuzatuvlarini hisoblaydi: jo'natuvchi tahrirlovchi yoki o'chiruvchi deb e'lon qilinmaydi. Takroriy kuzatuvlar bir xil Telegram xabarini tasvirlashi mumkin.

Jurnal analitikasi turiga ko'ra, birinchi/oxirgi yozuv havolalari va manba `events.jsonl` SHA-256 bo'yicha hisoblarni saqlab qoladi. Rasmlarda HTML va PDF formatida aniq qiymatlar keltirilgan. Kunlik bloklar 366 kunlik yozib olingan davrdan keyin oylarga o'tadi; grafiklar ularni eng ko'pi bilan 36 ta teng kenglikdagi intervallarga birlashtiradi. 100 000 dan ortiq alohida identifikatorlar yoki 1 200 oy bo'lsa, tegishli diagramma mavjud bo'lmaydi, biroq aniq umumiy hisob-kitoblar mavjud bo'lib qoladi.

Snapshot va hisob-ma'lumotlarni baham ko'rish diagrammalari faqat xizmatga tegishli bo'lmagan xabar qatorlarini hisobga oladi, ularning yozib olingan xabar vaqtini ishlatadi. Ulashish agregatlari redaksiya va filtrlashdan keyin hisoblanadi. Ushbu diagrammalar eng ko'pi bilan 90 ta teng kenglikdagi UTC sana oralig'idan foydalanadi va 10 000 tagacha guruhlash qiymatlarini saqlaydi; ortiqcha sonlar aniq ko'rsatiladi va muvofiqlashtiriladi. Oxirgi intervall qisqaroq bo'lishi mumkin. Noma'lum yoki sodda sanalar vaqt diagrammalariga kiritilmaydi.

Bo'sh interval hech qanday kuzatuv kiritilmaganligini anglatadi; bo'shliqlar uchun qamrovni ko'ring. Ushbu diagrammalar saqlangan faoliyatni tasvirlaydi. Noma'lum jo'natuvchilar alohida toifa bo'lib qoladi va har bir tekshiruv alohida hisobot qilinadi.

Qo'shilganda, `analytics.json` arxivning imzolangan fayl xeshlari bilan himoyalangan. Journal `report.json` shu tanlangan agregatni o'z ichiga oladi. Imzo tekshiruvi o'zgargan baytlarni aniqlaydi. Raqamlarni tekshirish uchun jurnal agregatlarini qayta hisoblang `report_analytics.Analytics` va `selected` bilan, yoki snapshot agregatlarini `snapshot_analytics.collect` va `project` bilan.

### Anomaliya ko'rsatkichlari

**Oldindan ko'rish.** Dalil hisobotlariga ro'yxatdan o'tgan protsessorlar (`tgwitness/metrics/`, har bir metrika uchun alohida fayl) tomonidan hisoblangan **Anomaliya ko'rsatkichlari** bo'limi qo'shiladi. Hisobot har bir protsessorni uning versiyasi bilan birga nomlaydi va jadval ostida uning usulini chop etadi, shunda hisoblashni `events.jsonl` faylidan `tgwitness.metrics.run` yordamida takrorlash mumkin.

| Protsessor | U nimani ko'rsatadi |
| --- | --- |
| `first_time_posters_over_time` v1 | Har bir UTC kunida birinchi marta post qilgan foydalanuvchilar va xabarlar soni. Bayroq uchun kamida beshta birinchi marta post qilgan foydalanuvchi va ularning mediani uch barobariga teng bo'lgan xabarlar soni, xabar hajmi esa mediani ko'pi bilan 1.5 barobar bo'lishi talab etiladi. Asosiy chiziq 7 kunlik tayyorgarlikdan so'ng, so'nggi 14 ta kalendar kun ichida kamida 7 ta kuzatilgan kunni hisobga oladi. |
| `service_vs_message_ratio` v1 | Har bir suhbat bo'yicha alohida saqlangan xabar raqamlari va xizmat xabarlari ulushi. Bu raqamlashni tasvirlaydi; ma'lum bir yo'qolgan raqamni tushuntirmaydi. |
| `join_leave_per_month` v1 | Qo'shilishlar, tark etishlar va oylik, shaxs, suhbat, o'zgarish va kun bo'yicha olib tashlashlar yoki taqiqlar. |
| `pinned_per_month` v1 | Oylik chat holati snapshotlari orasida qo'shilgan yoki olib tashlangan xizmat xabarlari, bildirishnomalar va biriktirilgan xabarlar. |

**Parametrlar → Hisobot metrikalari** protsessorlar va ko'rsatiladigan qatorlar sonini tanlaydi, shu jumladan filtrlangan hisobotlarda ham. Kunlik va oylik jadvallar so'nggi qatorlarni ko'rsatadi, xizmat ulushi jadvallari esa saqlangan xabarlar soniga qarab suhbatlarni reytinglaydi. Yakunlar har bir qatorni o'z ichiga oladi.

Manba kodini olgandan so'ng, yuqorida sanab o'tilgan sakkizta dizaynni bir xil badiiy jurnal asosida tuzing:

```
python tools/build_report_styles.py --output test-results/report-styles
```

Natijada hosil bo'lgan `index.html` faylini ochib, to'liq HTML hisobotlar, imzolangan PDF va ZIP fayllarni solishtiring. Har bir dizayn bir xil manba jurnalidan foydalanadi. Har bir ishga tushirish uchun yangi chiqish katalogidan foydalaning, shunda oldin imzolangan namunalar saqlanib qoladi.

![Badiiy HTML hujjat](https://phishdestroy.github.io/TgWitness/assets/dossier-en.png)

HTML hujjat ish yuzasidagi muqova va asosiy ma'lumotlar bilan ochiladi. Raqamlangan dalillar xaritasi har bir topilma, uning qo'llab-quvvatlovchi faktlari, cheklovlari va mustaqil ko'rib chiqishga havola qiladi. Qidiriladigan yozuvlar va barqaror yozuv havolalari oflayn ko'ruvchida ham mavjud bo'ladi. Dizayn tor ekranlarga, shuningdek JavaScript o'rnatilmagan brauzerlar va mavzularga moslashadi.

Imzolangan PDF hujjat maxsus A4 qoplama, hisobot referensi va QR-kodi, ijrochi xulosasi, dalillar xaritasi, raqamlangan natijalar va hujjat belgilari (bookmarks) bilan jihozlangan. Uning sahifa sarlavhalari va pastki qismlari hisobotni aniqlaydi. QR-kod materialni aniqlaydi; u mustaqil tasdiqlash natijasi emas. Brauzerdan chop etilgan nusxalar ushbu kriptografik imzolangan PDF hujjatdan alohida.

Kuzatuv vaqti yozib olingan kuzatuv davrlari va uzilishlarni bir xil UTC o'qida joylashtiradi. Bo'sh joy qamrovni anglatmaydi; batafsil jadvallar aniq oraliklarni saqlaydi. ZIP ichida o'qiladigan hisobotlar, imzolangan JSON, manba yozuvlari va tekshirish bo'yicha ko'rsatmalar mavjud.

Rivojlantirish muhiti o'rnatilgan yangi, badiiy Ingliz/Rus/Nemis dosye yaratish:

```
python tools/build_dossier_example.py --output test-results/my-new-dossier
```

Har bir til katalogida `report.html`, `report.pdf`, `report.json` va `dossier.zip` fayllari mavjud. Mavjud namunaviy kataloglar hech qachon ustiga yozilmaydi. Uni yaratishda Telegram hisob qaydnomasi, tashqi vaqt belgilash xizmati yoki tarmoq ulanishi ishlatilmaydi.

![Badiiy imzolangan PDF-ning birinchi uch sahifasi](https://phishdestroy.github.io/TgWitness/assets/dossier-pdf.png)

## Konkret ishni o'qish

1 200 ta yozuvdan iborat jurnalning 1 000-yozuvida tasdiqlangan vaqt tamg'asi bo'lsa, hisobot shu vaqt tamg'asining chegarasidan tashqaridagi 200 ta keyingi yozuvni aniqlaydi. Bu tekshiruv nuqtasining mavjudligiga oid yuqori chegarani belgilaydi, har bir xabarning yuborilgan vaqtini isbotlamaydi. Agar yana uchta vaqt belgilash fayli tasdiqdan o'tmasa yoki tasdiqlanmasa, ular alohida hisoblanadi va ijobiy xulosani bera olmaydi.

Foydalanish mumkin bo'lgan vaqt tamg'asi quyidagi barcha tekshiruvlardan o'tishi kerak: uning izi tekshiruv nuqtasiga mos kelishi, imzosi tamg'alangan vaqtdagi ishonchli TSA ildiziga zanjirlanishi, hamda tekshiruv nuqtasining imzosi, kaliti, hisobi va boshi aniq jurnal prefiksiga mos kelishi. Faqat timestampni tahlil qilish yoki OTS kvitansiyasiga ega bo'lish yetarli emas. O'quvchi ishonchli TSA ildizini mustaqil ravishda tanlashi va tasdiqni takrorlashi kerak. OTSga o'zining Bitcoin tasdiqlash tekshiruvi kerak.

| Hisobot holati | Ma'no |
| --- | --- |
| Eksport paytida tekshiriladi | Eksportyor aytilgan tekshiruvni amalga oshirdi; mustaqil takrorlash hanuzgacha zarur. |
| Yozib olindi; ko'rib chiqish talab etiladi | Asosiy kuzatuv yoki operator bayonoti qayd etiladi; bu mustaqil tasdiq emas. |
| Ushbu nusxaga kiritilmagan | Matnda bu da'voni qo'llab-quvvatlovchi hech qanday artefakt yo'q. U boshqa joyda mavjud emasligini aytmaydi. |
| Mustaqil ravishda tekshirilmagan | Hisobot mustaqil tasdiqlash natijasini taqdim etmaydi. |
| Toʻliq emas yoki mavjud emas | Material yoki talab qilinadigan tekshiruv yetishmayapti, to'liq emas yoki muvaffaqiyatsiz tugadi. |

Har bir tekshiruvni yozib olingan to'plam qamrovi bilan birga alohida ko'rib chiqing.

## Qanday kuchli konfiguratsiya saqlanishi kerak

1. Yig'ishga tayanishdan oldin, yig'uvchining kalit barmoq izini alohida ishonchli kanal orqali saqlab qo'ying. Ushbu referensni eksportni imzolash kaliti bilan solishtiring.
2. Mustaqil ravishda vaqt belgilangan tekshiruv nuqtalarini saqlang va agar ishlatilsa, yig'uvchining ma'muriy nazorati tashqarisidagi guvoh jurnalini saqlang. Ularni eksport qilingan jurnal bilan solishtirib, uning avvalgi chegaralarini tekshiring.
3. Yozuvlarni olish doirasi, bo'shliqlar, filtrlar, cheklovlar va yig'ishdagi o'zgarishlarni aniqlang. Amaldagi da'vo bilan bog'liq etishmayotgan davrlarni tushuntiring, kuzatilmagan xabar IDlari, o'chirish bildirishnomalari va muvaffaqiyatsiz qayta tekshiruvlarni alohida ajratib ko'rsating.
4. Asl ZIP-fayllarni va ularning hashlarini saqlang. Har bir saqlovchi, uzatish, sana va maqsadini qayd eting. Tegishli operator bayonotlari va ish yozuvlarini ular bilan birga saqlang.
5. Maxfiy VMlar uchun iqtibos, chaqiriq, Intel sertifikat zanjiri, o'lchovlar, aniq manba va kalit boshqaruv shartlarini saqlang va mustaqil ravishda tasdiqlang. Attestatsiya tekshiruv natijasini ko'rib chiqilgan artefaktlar bilan birga saqlang.

Har bir rejimda ma'lumotlarni olish, arxiv yaxlitligi, vaqt va to'plam qamrovini tekshirish uchun [tekshiruv doirasiga](https://phishdestroy.github.io/TgWitness/uz/docs/reference/evidence/#verification-scope) qarang.

## Qabul qiluvchi ko'rib chiqishi

TgWitness'ning ishonchli o'rnatilgan versiyasidan va mustaqil ravishda olingan barmoq izidan foydalaning:

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --tsa-ca tsa-root.pem
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --witness witness.zip --witness-fingerprint WITNESS_SHA256 --require-witness
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_SHA256 --check-drand
```

Witness ZIP mustaqil ishonchli manbadan olinishi kerak; uning kaliti va kelib chiqishini ham saqlang. Buyruqlar, vosita versiyasi, chiqishlar, ko'rib chiqilgan kirish hashlar va hal qilinmagan savollarni saqlang. Beacon tasdiqlash alohida onlayn tekshiruvdir; hisobotni render qiluvchi hech qachon faqat hisobotni ko'rsatish uchun xizmatga murojaat qilmaydi.

Muayyan xabar bo'yicha tortishuv yuzaga kelganda, arxiv referensiyasini, vakolatli fayl va yozuv referensiyasini keltiring, so'ng tegishli vaqt chegaralari, qamrov bo'shliqlari, tanlov va tasdiqlovchi materiallarni ta'riflang. Taqsimlash nusxasi uchun yozib olingan o'zgartirish va uning manba arxiviga bo'lgan havolalarini ham ko'rib chiqing. Xususiy filtrlar va identifikatsiya xaritalash ommaviy baholashdan tashqarida qoladi.

Imzolangan PDF-ni tekshirish qoplangan baytlarda o'zgarishlarni aniqlaydi. Asl raqamli fayl va tekshirish natijasini har qanday skrinshotlar yoki chop etilgan nusxalar bilan birga saqlang.
