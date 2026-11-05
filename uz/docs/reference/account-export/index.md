# Hisobni eksport qilish

Canonical page: https://phishdestroy.github.io/TgWitness/uz/docs/reference/account-export/

Hisob hozirda o&#x27;qiy oladigan narsalarni eksport qiling: doira, qayta boshlanadigan ishlar, imzolangan arxiv va minimallashtirilgan ulashish nusxalari.

Akkaunt eksporti akkauntni faqat o‘zi uchun band qiladi. Boshlash yoki davom ettirishdan oldin monitoringni yoki boshqa yig‘ish vazifasini aniq to‘xtatib turing; ilova ularni avtomatik to‘xtatmaydi.

O'rnatish ma'muri sifatida **Start here → Export my account** yoki **Exports → Telegram account → Configure account export** ni tanlang. Kerak bo'lsa tizimga kiring, hajmini ko'rib chiqing va eksportni aniq boshlang. Uzluksiz kuzatuv talab qilinmaydi. **Saqlangan kuzatuvlar** mavjud jurnalning alohida eksporti hisoblanadi; uning ZIP jurnal filtrlaridan qat'i nazar barcha manbalarni o'z ichiga oladi. Har bir ish maydoni o'z ishlariga, imzolash identifikatoriga va saqlash joyiga ega. Chiqarilgan panelga kirish, jumladan cheklanmagan oddiy eksport ruxsati, bu hisob bo'ylab yo'llarni ochmaydi.

Jo'natuvchi va xabar matni bo'yicha filtrlar **"Jo'natuvchi yoki xabar matni bo'yicha filtr"** ostida kengayadi. **Hisob ma'lumotlari va ulanish usuli** bo'limida ixtiyoriy hisob toifalari va "Export/oddiy sessiya" tanlovi mavjud; uning qisqacha mazmuni yopiq bo'lganda ham faol tanlovlarni ko'rsatadi. Ushbu bo'limlarni yopish ularning sozlamalarini saqlab qoladi. Eksport va hisobot loyihalari ko'rinishni o'zgartirish paytida ham joriy panel sessiyasida qoladi; ular brauzerni qayta yuklashda saqlanmaydi. Mavjud ishlar har ikkala eksport tanlovidan ham erishilishi mumkin.

Ushbu ish jarayoni ulangan hisobga hozirda kirish mumkin bo'lgan ma'lumotlarni eksport qiladi. Standart bo'yicha [Telegram Takeout](https://core.telegram.org/api/takeout) ishlatiladi; bu mavjud bo'lmagan yoki o'chirilgan Telegram ma'lumotlarining zaxira nusxasi emas. Maxfiy suhbatlar, kirib bo'lmaydigan tarix va avvalgi tahrirlar tiklanmaydi. Telegram Takeout boshlanishidan oldin kutish muddatini belgilashi mumkin. Panel bu kutishni ko'rsatadi; transportni jimlik bilan almashtirmaydi. Aniq regular-API opsiyasi boshqacha qamrovga ega va qo'llab-quvvatlanmagan kategoriyalarni ham yozib oladi.

## Qaysi ma'lumotlar yig'ilishini tanlang

| Sozlamalar | Ma'no |
| --- | --- |
| Maqsad | Ushbu ma'lumotni olish nima uchun zarurligini qayd eting. Bu yerga keraksiz ismlar yoki nozik ish tafsilotlarini kiritmang. |
| Hisobot tili | O'qiladigan hisobot yorliqlarining tilini tanlang. Asl xabar matni o'zgarmaydi; tarjima qilinmagan shablon yorliqlari ingliz tilida qoladi. Til imzolangan ish opsiyalari bilan belgilangan. |
| Suhbat turlari / suhbat IDlari | Barcha tanlangan turlar yoki faqat ro'yxatdagi suhbatlar; Saqlangan xabarlar shaxsiy suhbatlarga tegishli. Arxivlangan suhbatlar alohida tanlanishi mumkin. |
| Sanalar | UTC. Panelning From va Through kalendar sanalari ikkalasi ham kiritilgan. API inklyuziv `from_utc` va eksklyuziv `to_utc`; panel Throughdan keyingi kunning boshlanishini yuboradi. Bo'sh chegarani belgilash o'sha tomonni cheklovsiz qoldiradi. |
| Yuboruvchi identifikatorlari | Faqat ro'yxatda ko'rsatilgan jo'natuvchilarning xabarlari; bo'sh ro'yxat barcha jo'natuvchilarni o'z ichiga oladi. |
| Matn quyidagilarni o'z ichiga oladi | Bosh harflarga e'tibor bermaydigan so'zma-so'z iboralar OR bilan mos keladi. Jo'natuvchi/sana/o'z-xabari shartlari AND bilan birlashtiriladi. |
| O'z xabarlari | Faqat chiqadigan xabarlarni saqlang. |
| Media turlari | Ilova kategoriyalarini tanlang yoki barchasini tozalang, xabar fayllarini yuklab olishdan qochish uchun. |
| Fayl / umumiy media limitlari | Har bir fayl bo'yicha MiB va jami yuklab olingan media GiB. Matn, kvitansiyalar, o'qiladigan hisobotlar vaZIP ustki qismi qo'shimcha disk joyini talab qiladi. |
| Hisob toifalari | Profil, kontaktlar, profil rasmlari, hikoyalar, sessiya metama'lumotlari va boshqa Takeout ma'lumotlari uchun alohida boshqaruvlar mavjud. |

**Minimize yig'ish** sozlamasi fayllar va akkaunt metama'lumotlarini o'chirib tashlaydi. Jo'natuvchi/kontent filtrlari saqlangan xabar sahifalari va media yuklab olinishidan oldin qo'llaniladi. Telegram shu filtrlarni baholash uchun zarur bo'lgan xabarlarni o'z ichiga olgan API tarixi sahifalarini hali ham uzatadi: filtrlash tanlanmagan xabarlarning jarayon xotirasiga hech qachon kirmaydi, degan kafolat emas. Ish maydonchasidagi boshqa davom etayotgan kuzatuv o'z doirasi va saqlash sozlamalariga ega.

Profil-foto tarixi va hikoyalar standart bo'yicha tanlanmaydi. Ish faqat xabarlarni talab qilganda profil va kontaktlarni ham o'chirib qo'ying. Ilovalar yoki metadata keraksiz bo'lsa, ularni yig'ish paytida chiqarib tashlash ushbu eksportda yana bir xususiy nusxa saqlanishining oldini oladi.

## Qayta tiklash, qamrov va tasdiqlash

Har bir ish o'z parametrlari va hisob identifikatorini muzlatadi. Inventarizatsiya va ushlangan sahifalar imzolanadi; sahifa kvitansiyalari hashlar, kursorlar, vaqtlar, ilova natijalari va ularning oldingi kvitansiyalarini qayd etadi. Faqat tasdiqlangan sahifalar jarayonni oldinga siljitadi. Qayta boshlash/davom ettirish bu yozuvlarni davom ettirishdan oldin tekshiradi. O'zgartirilgan hisob, o'zgartirilgan imzolangan sahifa yoki nomuvofiq kvitansiya zanjiri rad etiladi. Parametrlarni yozib olish jarayonida o'zgartirish mumkin emas: boshqa doira uchun yangi ish boshlang.

Pause joriy hisob operatsiyasini to'xtatadi. Ilovani qayta ishga tushirish yakunlanmagan ishni aniq davom ettirish uchun ochiq qoldiradi. Muddati tugagan Takeout sessiyasi aniq davom ettirishni talab qiladi; Telegram bo'lingan diapazonlarini o'zgartirish yangi olishni talab qilishi mumkin. Davom ettirish avvalgi kuzatuvlarni saqlab qoladi, shuning uchun uzoq davom etadigan eksport bitta atomik snapshot emas. Hisobni o'zgartirish bo'yicha boshqa amallar va ziddiyatli eksportlar olish jarayonida bloklanadi. Ish maydonchasini o'chirishdan oldin paketlash tugashini kuting.

Resume allaqachon olingan kontentni davom ettirishdan oldin tekshiradi. Sekin saqlash qurilmasidagi katta arxivlar sozlangan **Parameters → Panel action timeout** (o'rnatilgan bo'yicha 120 soniya) muddatidan oshib ketishi mumkin. Qayta urinishdan oldin ushbu sozlamani oshiring; bekor qilish yoki saqlash uzilishi ishni to'xtatib qo'yadi, integritet tekshiruvlari muvaffaqiyatsiz bo'lsa, ish tushuntirish bilan muvaffaqiyatsiz bo'ladi. Verification fayllarini yopishdan oldin xavfsiz yakunlanishi yoki to'xtashi kerak. Sintetik tekshiruvlar orqali hech qanday katta akkaunt o'tkazuvchanligi da'vosi tasdiqlanmagan.

Panel tanlangan doirani to'liq bajarilgan va qisman arxivlangan holatlardan ajratib ko'rsatadi hamda e'tibordan chetda qolgan va o'qilmay qolgan holatlarni qayd etadi. Ataylab chiqarib tashlangan fayllar xato bo'lgan yoki mavjud bo'lmagan fayllardan farq qiladi. Integritet tekshiruvi muvaffaqiyatli bo'lsa ham qamrovni tekshirishni davom ettiring. Hech qanday mahalliy o'quvchi Telegram hech qachon mavjud bo'lgan barcha xabarlarni qaytarganini isbotlay olmaydi.

TugallanganZIPlar takroriy va HTTP-range yuklab olish uchun mavjud bo'lib qoladi. Hisob arxivi o'z ichiga oladi `manifest.json`, `manifest.sig`, imzolangan `job.json`, `inventory.json`, `receipts/`, vakolatli `data/*.jsonl`, tanlangan `media/`, imzolangan, vakolatli, tanlangan, o'qiladigan HTML va tasdiqlovchidan iborat. Yig'uvchining barmoq izini mustaqil kanal orqali belgilab, so'ng ishonchli o'rnatish yordamida tasdiqlang:

```
python -m tgwitness.verify account-export.zip --fingerprint TRUSTED_SHA256
```

Kengaytirilgan mazmuni 4 GiB dan oshadigan arxivlar uchun aniq yetarli `--max-gib`. Panel o'zining autentifikatsiyalangan, to'liq bajarilgan mahalliy arxivlarini ularning e'lon qilingan kengaytirilgan hajmi va e'lon qilingan ZIP digesti bo'yicha tekshiradi; tashqi CLI esa mustaqil hajm chegarasini saqlaydi. O'qiladigan HTMLni ochishdan oldin tekshirishni bajaring. Arxivga biriktirilgan verifikator qulay, ammo mustaqil ravishda olingan verifikator dalillarga biriktirilgan ijro etiladigan kodga ishonmaslikka imkon beradi.

Ed25519 imzosi va SHA-256 xeshlari kollektor tegishli baytlarni yozib qo'yganidan keyin o'zgarishlarni aniqlaydi. Ular **emas** isbotlaydiki, Telegram ushbu xabarlarni imzolagan, kollektor operatori halol bo'lgan, hisobning tarixi to'liq, yoki sud ushbu materialni qabul qiladi. Yozib olish vaqtlari kollektor soatiga asoslanadi. Mustaqil vaqt belgilari va mustaqil olish kelib chiqishi alohida baholanishi kerak.

## Advokat yoki boshqa qabul qiluvchi uchun oshkor etish hujjatini tayyorlang

Tayyor eksportni yuklab olgach, asl ZIPni saqlang va oching `index.html` chiqarilgan nusxadan oching. Hisobot uning doirasi, mavjud qamrovi va cheklovlarini tushuntiradi. Uning yozuv havolalari arxiv havolasi, hujjat yo'li va yozuv raqamini birlashtiradi, shunda qabul qiluvchi HTML yoki chop etilgan nusxada xuddi shu yozuvni topa oladi. Ishlangan misol uchun, [Badiiy hisobotni oching](https://phishdestroy.github.io/TgWitness/demo/report/).

Tamomlangan hisob eksportidan "**Ulashish uchun nusxa tayyorlash**"ni tanlang. Bu alohida imzolangan derivativ yaratadi. Manba ZIP o'zgarmas va maxfiy bo'lib qoladi; qabul qiluvchi uning to'liq mazmunini olishga ruxsat etilmagan bo'lsa, uni minimallashtirilgan derivativ bilan birga yubormang. Hisobot tilini alohida tanlang. Tilni yoki istalgan tanlov sozlamasini o'zgartirish yaratishdan oldin yana bir ko'rinishni talab qiladi.

1. Ochiq qilish maqsadini kiriting va sanalar, yuboruvchi identifikatorlari hamda so'zma-so'z matn mezonlarini tanlang.
2. Shaxslarni saqlab qolish, faqat ro'yxatdagi ishtirokchilarni ko'rsatish yoki hammani psevdonimlashni tanlang. Psevdonimlash rejimida chat IDlari/sarlavhalari va xabar IDlari ham almashtiriladi. Psevdonimlar bitta oshkorot ichida barqaror bo'lib, mustaqil tayyorlangan oshkorotlar orasida o'zgaradi.
3. Xabar matnini saqlang, uni butunlay o'chirib tashlang yoki mask qilish uchun haqiqiy ismlar/iboralarni qo'shing. Xususiy rejimda vosita shuningdek ma'lum yashirin jo'natuvchi nomlari va muqobil foydalanuvchi nomlari, butun tokenli jo'natuvchi identifikatorlari, bevosita suhbat nomlari, havolalar, elektron pochta manzillari va telefon ko'rinishidagi qatorlarni ham masklaydi. Ma'lum nomga moslash Unicode katta-kichik harflarning bir xil yozilishini (case folding) hisobga oladi, jumladan `Straße`/`STRASSE`. Umumiy guruh/kanal sarlavhalari xabar matnidan avtomatik ravishda olib tashlanmaydi. Agar ma'lum identifikatorni yashirish chegarasi oshib ketsa, manba eksportini toraytiring yoki matnni o'chirib tashlang; vosita keyingi nomlarni jimjit o'tkazib yubormaydi. Bu eng yaxshi urinish qoidalari bo'lib, umumiy anonimlashtirish emas.
4. Fayllarni faqat qabul qiluvchi ularga ehtiyoj sezsa qo'shmang. Ilova qilingan asl fayllar piksellar, audio, matn va metadata saqlanadi. Ular vosita tomonidan anonimlashtiriladi**emas**.
5. Hisoblarni, ogohlantirishlarni va namunaviy o'zgartirilgan xabarlarni ko'rib chiqing, so'ng yaratishni aniq tasdiqlang. Namuna har biri 12 tagacha xabar va 2 000 belgiga qadar cheklangan. Bu natijaning to'liq ko'rib chiqilishi emas, balki namunadir. Sozlamalarni o'zgartirish uchun yana bir ko'rib chiqish zarur. Ko'rib chiqish 15 daqiqadan so'ng amal qilmay qoladi va u ma'lum bir administrator sessiyasiga hamda aynan shu asl ZIP ga bog'langan; yaratilgandan so'ng qayta ishlatilmaydi. Yangi ko'rib chiqish bir xil ish va sessiya uchun avvalgisini bekor qiladi.
6. Natijaning to'liq versiyasini tekshiring `index.html` va `messages.jsonl` Topshirishdan oldin uni mahalliy tarzda to'liqva tadqiq qiling. Agar u keraksiz ma'lumotni oshkor qilsa, kuchliroq istisnolar bilan yangi oshkor qilish hujjatini yarating. Imzolangan ZIPni joyida tahrirlamang.

Minimizatsiya qilingan format tuzilgan akkaunt profillari, kontaktlar, avatarlar, sessiyalar, hikoyalar, xom Telegram obyektlari, jo'natish sarlavhalari, javob iqtiboslari, kontakt kartalari va joylashuv metama'lumotlarini o'z ichiga olmaydi. U asl JSONL fayllarini, shaxsiy filtr sozlamalarini, psevdonim kalitini va identifikatsiya xaritasini o'z ichiga olmaydi. Tanlangan matn, aniq saqlangan identifikatorlar va kiritilgan fayllar hanuzgacha o'sha filtrlarda ishlatilgan nomlar, ID-lar yoki iboralarni o'z ichiga olishi mumkin; ular alohida ko'rib chiqilishi kerak. Maxfiy siyosat va psevdonim kaliti ish uchun mahalliy omborda shifrlangan holda saqlanadi; ishni o'chirish unga bog'liq maxfiy oshkor etish yozuvlarini tozalaydi. Ommaviy siyosat yozuvlari filtr qiymatlari o'rniga filtr sonlarini hisobga oladi. Manifest va HTMLda ko'rsatilgan maqsad ommaviy bo'lib, aniq maxfiy mezonlar va psevdonimlashtirilgan rejimlarda ma'lum yashirin shaxsiyatlar ham, xabar matni o'chirib tashlanganida ham, maskalanadi. Maqsadni keraksiz shaxsiy ma'lumotlardan holi saqlang; noma'lum identifikatsiya konteksti esa qolishi mumkin.

Uning manifesti derivativ fayllarni, jamoat siyosatini va asl ZIPning hashini bog'laydi. Verifikatsiya yaxlitlikni aniqlashi va, agar manba mahalliy taqdim etilsa, mos keluvchi manba bog'lanishini o'rnatishi mumkin:

```
python -m tgwitness.verify minimized-disclosure.zip --fingerprint TRUSTED_SHA256
python -m tgwitness.verify minimized-disclosure.zip --fingerprint TRUSTED_SHA256 --evidence account-export.zip
```

Manba bog'lanishi mustaqil ravishda tanlangan o'zgartirish har bir zarur elementni tanlaganini yoki har bir identifikatsiya qiluvchi ma'lumotni olib tashlaganini isbotlamaydi. Asl oddiy matn dalil sifatida ilova qilinmagan. Ushbu hukm uchun yangi ko'rib chiqish zarur.

## Ma'lumotlarni himoya qilish va mezbonlik qilingan Capture ko'rinishi

Ushbu nazorat vositalari maqsadni cheklash va ma'lumotlarni minimallashtirishni qo'llab-quvvatlaydi; ular avtomatik ravishda huquqiy muvofiqlikni tekshirmaydi. [GDPRning 5 va 25-moddalari](https://eur-lex.europa.eu/eli/reg/2016/679/oj/eng) ushbu tamoyillar va dizayndan/defoltdan himoyani belgilaydi. Qonuniy asos, zaruriyat, tegishli hollarda maxsus toifadagi shartlar, saqlash muddati, xavfsizlik va qabul qiluvchining kirish huquqi bo'yicha ham holatga mos qaror qabul qilish zarur. Sud jarayoni maqsadi yolg'iz o'zi har bir oshkor etishni qonuniy qilmaydi. Psevdonimlangan ma'lumotlar odatda shaxsiy ma'lumot bo'lib qoladi; [EDPB tushuntirish](https://www.edpb.europa.eu/topics/ai-and-technology/anonymisation-pseudonymisation_en)iga qarang.

Erkin matn, sanalar, kam uchraydigan hodisalar va faktlar kombinatsiyalari ismlar olib tashlanganidan keyin ham odamlarni aniqlashi mumkin. Xabar mazmuni keraksiz bo'lsa, matndan so'zlarni o'chirishni afzal ko'ring; zarur bo'lganda esa to'liq hosilani tekshiring. Manba va omborni himoyalangan holda saqlang, saqlash va ulashishni mas'ul shaxs bilan kelishib oling hamda aniq qaysi ZIP topshirilganini qayd eting.

GitHub Actions Takeout yoki oddiy API orqali butun akkaunt yoki tanlangan chatlar eksportini，shuningdek bitta chat jurnalini qo‘llab-quvvatlaydi．[GitHub Actions](https://phishdestroy.github.io/TgWitness/docs/capture/) qo‘llanmasi sozlamalarni tekshirish va 120 daqiqalik cheklovni tushuntiradi．Mahalliy eksportlar va ulashish nusxalari GitHub attestatsiyasini meros qilib olmaydi，sun’iy testlar haqiqiy Telegram akkaunti bilan ishlashni isbotlamaydi．

[Dalil formati](https://phishdestroy.github.io/TgWitness/uz/docs/reference/evidence/) · [Holat hisobotlari](https://phishdestroy.github.io/TgWitness/uz/docs/reference/case-reports/)
