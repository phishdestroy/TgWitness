# Tergov rejimi

Canonical page: https://phishdestroy.github.io/TgWitness/uz/docs/reference/investigation/

Kanal, guruh, shaxsiy suhbatlar va botlar bo'ylab butun hisob tekshiruvlari, dastlabki doiradan tasdiqlangan ish paketigacha.

Bir ishni kanallar, guruhlar, shaxsiy suhbatlar va botlar bo'ylab dastlabki olishdan tortib, keltirilgan vaqt chizig'i va tasdiqlanadigan topshirishgacha kuzatib boring. Interaktiv veb-sayt versiyasi `/docs/cases/` manzilida; [ko'rinishni oldindan ko'rish bo'yicha ko'rsatmalar](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/PUBLISHING.md#preview-the-website-locally).

## Tahlil qilingan holat: manzil to'rtta suhbat davomida o'zgargan

E'lon botga ishora qiladi. Amaliyot guruhi yangi to'lov manzilini muhokama qiladi, botning klaviaturasi uni ko'rsatadi va shaxsiy keyingi xabar uni takrorlaydi. Keyin e'lon tahrirlanadi va guruh xabari yo'qoladi.

Savollar quyidagilar: o'zgarishdan oldin va keyin nima kuzatilgan, Telegram akkauntlaridan qaysi biri har bir elementni joylagan, manzil qayerda paydo bo'lgan, qaysi ilova baytlari saqlangan va qaysi oraliklar noma'lum bo'lib qolmoqda?

Ushbu misoldagi barcha ismlar, identifikatorlar, vaqtlar va jurnal havolalari badiiydir. Ish jarayoni joriy xususiyatlardan foydalanadi; ish holati xaritasi esa ilova tomonidan avtomatik yaratilgan grafik emas, balki illyustratsiyadir.

Oqim sxemasi · Kanal → Ish maydoni jurnali; Guruhlar → Ish maydoni jurnali; Shaxsiy suhbatlar → Ish maydoni jurnali; Botlar → Ish maydoni jurnali; Ish maydoni jurnali → Barcha manbalarni qidiring; Ish maydoni jurnali → Yozuv referensiyalari bilan odamlar profillari; Ish maydoni jurnali → Saqlangan versiyalar va ilova kvitansiyalari; Barcha manbalarni qidiring → Tahlilchi vaqt chizig'i va manba ro'yxati; Yozuv referensiyalari bilan odamlar profillari → Tahlilchi vaqt chizig'i va manba ro'yxati; Saqlangan versiyalar va ilova kvitansiyalari → Tahlilchi vaqt chizig'i va manba ro'yxati; Ish maydoni jurnali → Imzolangan dalillar ZIP; Tahlilchi vaqt chizig'i va manba ro'yxati → Holatni alohida tasdiqlangan artefaktlar bilan topshirish; Imzolangan dalillar ZIP → Holatni alohida tasdiqlangan artefaktlar bilan topshirish · Kanal · Guruhlar · Shaxsiy suhbatlar · Botlar · Ish maydoni jurnali · Barcha manbalarni qidiring · Yozuv referensiyalaribilan odamlar profillari · Saqlangan versiyalar vailova kvitansiyalari · Imzolangan dalillar ZIP · Tahlilchi vaqt chizig'i vamanba ro'yxati · Holatni alohidatasdiqlangan artefaktlarbilan topshirish

**Diagramma matn sifatida**

1. Kanal → Ish maydoni jurnali
2. Guruhlar → Ish maydoni jurnali
3. Shaxsiy suhbatlar → Ish maydoni jurnali
4. Botlar → Ish maydoni jurnali
5. Ish maydoni jurnali → Barcha manbalarni qidiring
6. Ish maydoni jurnali → Yozuv referensiyalari bilan odamlar profillari
7. Ish maydoni jurnali → Saqlangan versiyalar va ilova kvitansiyalari
8. Barcha manbalarni qidiring → Tahlilchi vaqt chizig'i va manba ro'yxati
9. Yozuv referensiyalari bilan odamlar profillari → Tahlilchi vaqt chizig'i va manba ro'yxati
10. Saqlangan versiyalar va ilova kvitansiyalari → Tahlilchi vaqt chizig'i va manba ro'yxati
11. Ish maydoni jurnali → Imzolangan dalillar ZIP
12. Tahlilchi vaqt chizig'i va manba ro'yxati → Holatni alohida tasdiqlangan artefaktlar bilan topshirish
13. Imzolangan dalillar ZIP → Holatni alohida tasdiqlangan artefaktlar bilan topshirish

## 1. Holatni aniqlang va butun hisobotni to'plang

1. Yig'ish hisobini o'z ish maydonida bog'lang. Tashqi ish yozuvlarida ish referensiyasi, hisob IDsi, ish maydoni, kuzatuv boshlanishi va ishonchli imzo kaliti barmoq izini qayd eting.
2. Ochiq **manbalar → Kuzatuv doirasi → Tergov rejimi**. Oldindan sozlama **butun hisobni**, kanallar/guruhlar/shaxsiy suhbatlar/botlarni, o'z harakatlaringizni, manba profillarini va yangi topilgan manbalar uchun so'nggi 200 ta ko'rinadigan xabarni tanlaydi. Uni ko'rib chiqing, "**Doirani saqlash**" tugmasini bosing va doirani tasdiqlashni yakunlang.
3. **Suhbatlarni yuklang** va manbalarni hisobning dialog ro'yxati bilan solishtiring. Istisnolarni tekshiring. **Parametrlar → Hisob ro'yxatidan o'qilgan suhbatlar**bo'yicha standart qiymat 1 000 ga teng va 20 000 gacha ruxsat etiladi. Ro'yxat chegarasidan oshgan manbalar ular faollashganda qo'shiladi. Haqiqatan qaysi manbalar sanab o'tilganini qayd eting.
4. **Yozib olish sozlamalar**ida "**Barcha ko'rinadigan faoliyat**"ni tanlang va monitoring sozlamalarini saqlang. Ilova turlari/cheklovlarini hamda bo'sh disk joyini ko'rib chiqing.
5. Kuzatuvni boshlang. Nazorat ostidagi yangi xabar, tahrir va o'chirishni tasdiqlang, so'ngra test ma'lumotlarini va har qanday xatolarni saqlab qo'ying.

Butun hisob doirasi saqlangan sozlamalar doirasida hisobda ko'rinadigan faoliyatni qayd etadi. U maxfiy suhbatlarga kira olmaydi yoki har bir bog'langan guruhga avtomatik qo'shilmaydi. Shuningdek, u mavjud bo'lgan barcha suhbatlarni to'ldirmaydi. [Qayd etish doirasini](https://phishdestroy.github.io/TgWitness/uz/docs/reference/collection/#observation-scope-chosen-chats-a-folder-or-the-whole-account) ko'ring.

## 2. Har bir manbani ro'yxatlab, uning tarixiy kontekstini aniqlang

Har bir suhbat uchun alohida qator bilan manba ro'yxatini saqlang:

| Maydon | Yozib qo'ying |
| --- | --- |
| Shaxsiyat | Ish maydoni, hisob ID, raqamli chat ID, sarlavha va tur |
| Ko'rinish | A'zolik/rol, kirish tasdiqlangan yoki tasdiqlanmagan, istisnolar |
| Jonli yozib olish | Boshlanish vaqti, tanlangan voqea turlari va keyingi siyosat o'zgarishlari |
| Jurnal tarixi | Snapshot so'raldi/tayyorlandi, cheklov, vaqt va yozuv referenslari |
| To'liq tarix | Har bir suhbat bo'yicha eksport fayl nomi, chegarasi va yakunlanishi/muvaffaqiyatsizligi |
| Ilovalar | Yakunlangan media kvitansiyalari, xeshlar, hajmlari hamda o'tkazib yuborilgan/muvaffaqiyatsiz natijalar |
| Qamrov | To'xtashlar, to'liq bo'lmagan qabul qilish, FloodWait, mavjud bo'lmagan xabarlar va boshqa bo'shliqlar |

Har bir manba uchun to'g'ri olish usulini qo'llang:

- **Manbalar** bo'limida **to'liq tarixni yuklash** (hozirgi `main`) yoqilgan manbalardan mavjud avvalgi xabarlarni ish maydoni jurnaliga yuklaydi. U pauza/davom ettirish va imzolangan progress hisobotini qo'llab-quvvatlaydi. [Tarixni olish bo'limiga](https://phishdestroy.github.io/TgWitness/uz/docs/reference/history/) qarang.
- **History snapshot** yaqinda ko'rinadigan so'nggi xabarlarni kuzatuv jurnaliga saqlaydi. Uning standart maksimal qiymati 500; **Parametrlar → Eng katta history snapshot** buni 10 000 gacha oshirishi mumkin. Bu joriy tarix kuzatuvlari bo'lib, qayta tiklangan tahrirlar emas.
- **To'liq suhbat eksporti → To'liq suhbatni** yoki **Suhbatlar → Suhbatni eksport qilish** hozirda ko'rinadigan bitta suhbat tarixini alohida imzolangan `chat.json`/`chat.html` paketiga oladi. Ish manbalari bo'yicha takrorlang va har bir natijani saqlang.
- **Yangi chat yoki bot paydo bo'lganda**uning profilini va so'nggi 1 000 tagacha xabarni saqlash mumkin; tekshiruv rejimi 200 tasini tanlaydi. Mavjud chatlarga bu retroaktiv tarzda qo'llanilmaydi, agar rejim yoqilganda.
- **Ko'rinadigan ilovalarni yuklab olish** sozlangan siyosat bo'yicha baytlarni saqlab qoladi. SHA-256 va bayt soni bilan to'ldirilgan `media.saved` kvitansiyasi talab etiladi. Navbatga qo'yilgan topshiriq, kichik rasm yoki fayl nomi saqlangan ilova hisoblanmaydi.

To'liq chat eksporti jurnalni yoki odamlar profilini barcha xabarlar bilan to'ldirmaydi. TgWitness ichida tahlil qilmoqchi bo'lgan tarix uchun **"To'liq tarixni yuklash**" yoki "Cheklangan jurnal snapshotlari"dan foydalaning. Tarixni ishga tushirishdan oldin yoqilgan manba ro'yxatini tekshiring. Hech bir usul Telegram endi qaytarmaydigan materialni tiklamaydi.

## 3. Rivojlanayotgan ish holatini va ataylab yuritilgan o'zaro munosabatlarni saqlash

Yulduzcha bilan belgilangan faol ish suhbatlari ustuvor manba sifatida. Tekshirish va qayta tekshirish oralig'ini, davom etayotgan to'ldirish va media natijalarini ko'rib chiqing. Hisobdan foydalanganda to'plovchini kuzatishda davom ettiring. **Suhbatlar → Profil → Profilni hozir saqlashni** ishlating, manba metama'lumotlarini, masalan ta'riflar va bot buyruqlarini saqlash uchun. Bu saqlangan xabarlardan olingan odamlar profilidan alohida.

Agar ish manbani kuzatish yoki bot bilan o'zaro ta'sir qilishni o'z ichiga olsa:

1. **Telegram havolasini ochish → Saqlash** va **ko'rinishni** yozib olish berilgan havolani va harakatdan oldin qaytarilgan ko'rinishni **saqlaydi**.
2. **Join / open and observe** qo'shilish/ochishni bajaradi va botning start parametrini taqdim etilganda yuboradi. Tasdiqlanishini kutayotgan qo'shilish so'rovi "pending" (kutishda) deb qayd etiladi.
3. Panel tomonidan yuborilgan matnli javoblar va qo'llab-quvvatlanadigan tugma bosishlari `interaction.requested` va `interaction.result` kodlarini saqlab qoladi. Callback kvitansiyalari qaytarilgan pop-up matnini, ogohlantirish holatini va URL manzilini saqlab qolishi mumkin.

Bu haqiqiy akkaunt harakatlari. Boshqa Telegram ilovasidagi Callback bosishlari yig'uvchi tomonidan ko'rinmaydi, garchi natijada paydo bo'lgan xabarlar yoki tahrirlar ko'rinishi mumkin. Mini-klient veb-ilova, to'lov, telefon yoki joylashuv bo'yicha ish jarayonlarini bajarmaydi. Aniq xulq-atvor uchun [panel o'zaro ta'sirlariga](https://phishdestroy.github.io/TgWitness/uz/docs/reference/collection/#act-from-the-panel) qarang.

## 4. Suhbatlar bo'ylab kuzatuvlarni bog'lash

Jurnalda "**Barcha manbalar**"ni tanlang va yozib olingan kontentni qidiring. Mos yozuvlarni oching va ish maydoni, suhbat, xabar IDsi, ketma-ketlik hamda yozuv xeshini saqlang.

Muvofiq chatda **Odamlar → Profillarni yoqishni** tanlang va shaxsni tekshiring:

- Vaqt o'tishi bilan kuzatilgan ismlar/foydalanuvchi nomlari va raqamli Telegram ID.
- Manba yozuvlari havolalari bilan javob munosabatlarini ko'rsating.
- **Shuningdek…** ushbu ish maydoni jurnalidagi boshqa suhbatlarda ham o'sha ID yozgan.
- Faoliyat, tahrirlar/o'chirishlar hamda tilga olingan hamyonlar, telefonlar, foydalanuvchi nomlari va havolalar.
- Saqlangan avatar metama'lumotlari va ularning alohida kelib chiqishiga ega shunga o'xshash kesh-avatarlar.

Xulosada hosil qilingan profilni ishlatishdan oldin keltirilgan yozuvlarni oching. Profil(lar) saqlangan xabarga ega shaxslarni qamrab oladi, guruhning har bir a'zosini emas. **Parametrlar → fakt bo'yicha keltirilgan yozuvlar**soni havolalar ro'yxatini cheklaydi, asosiy faoliyat sonini emas. Tilga olinishlar va avatar o'xshashligi yo'nalish ko'rsatadi; ular egalik huquqi yoki shaxsni aniqlamaydi.

Ishlangan misolda:

| Havo | Yozib oladi | Qo'llab-quvvatlanadigan kuzatuv |
| --- | --- | --- |
| Xuddi shu jo'natuvchi hisob | Guruh #146 va shaxsiy keyingi kuzatuv #205 | Ikkalasi ham Telegram jo'natuvchi ID 71001 ni taqdim etadi |
| Xuddi shu manzil | #146, bot klaviatura #173, kanal tahriri #188, shaxsiy xabar #205 | Barchasida`pay.example.invalid/new` mavjud; egalik/nazorat aniqlanmagan |
| Xuddi shu saqlangan fayl | Yakunlangan media kvitansiyalari #151 va #209 | Saqlangan baytlar uchun to'liq SHA-256 qiymatlari mos keladi |
| Kanalga tegishlilik | #101 va #188 | Tasdiqlangan jo'natuvchi bo'lmasa, kanal postini foydalanuvchi 71001 ga tegishli deb hisoblamang |

Ilovadagi hashlarni va ularga tegishli xabar havolalarini solishtiring. Bir xil fayllar muallif, tarqatuvchi yoki umumiy operatorni aniqlamaydi. Bir xil ism va o'xshash avatarlar o'zi ikki Telegram IDni bitta shaxsga biriktirmaydi.

## 5. Sohil-chatlar bo'yicha voqealar jadvalini tuzing

**Suhbatlardagi** saqlangan versiyalar va ularning **Jurnal yozuvidagi #…** havolalaridan foydalaning. Jurnalda **Barcha manbalarni Tahrirlar**, **O'chirishlar** va **Qamrov** bilan birlashtiring. Taqdim etilgan hollarda ham `source_at`, ham `observed_at` ni saqlang.

| Illyustrativ kuzatuv vaqti | Manba | Kuzatuv |
| --- | --- | --- |
| 09:00 | Kanal #101 | Asl manzil qayd etildi |
| 09:12 | Guruh #146; media #151 | Yangi manzil e'lon qilindi; fayl yuklab olindi |
| 09:16 | Bot #173 | Klaviatura yangi manzilga ishora qiladi |
| 09:20 | Kanal #188 | E'lon tahrirlangan; ikkala saqlangan versiya ham saqlanib qoladi |
| 09:24 | Shaxsiy #205; media #209 | Xuddi bir xil jo'natuvchi ID manzilni takrorlaydi; xuddi bir xil fayl baytlari saqlangan |
| 09:28 | Guruh #231 | O'chirish to'g'risida bildirishnoma qabul qilindi; o'chiruvchi va aniq o'chirish vaqti noma'lum |

Ushbu misolli havolalar orasida boshqa yozuvlar ham mavjud. Ketma-ketlik raqamlari kuzatuvlarni tartibga soladi; tarix snopshotlari eski manba sanalarini o'z ichiga olishi va jonli voqealardan keyin yetib kelishi mumkin. Snopshotlar, tiklangan xabarlar, o'chirish bildirishnomalari va qayta tekshirishda yo'qligi natijalarini ajratib ko'rsating. Qamrovdagi bo'shliqlarni noma'lum intervallar sifatida belgilang. Keyingi tarixiy ma'lumotlarni olish uzluksiz kuzatuvni retroaktiv ravishda ta'minlamaydi.

## 6. Hisob nuqtai nazarlarini ularning kelib chiqishini yo'qotmasdan qo'shish

Har bir alohida akkaunt uchun alohida ish maydonidan foydalaning va uning inventarizatsiyasini takrorlang. Har bir solishtirishda akkaunt IDsi, roli, imzolash kaliti barmoq izi va manba havolalarini saqlang. Xabar raqamlari suhbatlar/akkauntlar bo'ylab global identifikator hisoblanmaydi.

Turli ish maydonlari o'rtasidagi korrelyatsiya tashqi ish holatlari eslatmalari yoki tahlil vositalarida amalga oshiriladi. Hozirda TgWitness'da global miqyosda turli ish maydonlari bo'ylab qidiruv, birlashtirilgan vaqt chizig'i, tergov grafi yoki birlashtirilgan ish holatlari arxivi mavjud emas. **Bitta** kanal/superguruhning ko'p hisobga eksport qilinishi hisob jurnallarini birlashtirish emas, balki alohida operatsiyadir.

Uzoq muddatli ishda [mustaqil guvoh](https://phishdestroy.github.io/TgWitness/uz/docs/reference/witness/) bilan chegaralarni saqlang. Har bir hisobning yozib olish yo'li va ko'rinishini aniqlash uchun nazoratli yetkazib berish tekshiruvlaridan foydalaning.

## 7. Ishni topshirishni yig'ish va tasdiqlash

Ularni tahlilchi tuzgan ish direktoriyasida birga saqlang:

| Material | Maqsad |
| --- | --- |
| Holat yozuvlari va manba ro'yxati | Savol, yig'ish siyosati, kirish/rol, natijalar, muqobil izohlar va bo'shliqlar |
| Vaqt chizig'i | Har bir yozuv uchun vaqt hamda ish maydoni/suhbat/xabar/ketma-ketlik ma'lumotlari |
| Har bir ish maydoni uchun imzolangan dalillar ZIP | To'liq yozib olingan jurnal, manifest va ilova qilingan saqlangan media; panel filtrlari jurnal eksportini cheklamaydi |
| Alohida imzolangan foydalanuvchi profil fayllari | Olingan manbalar tegishli ish maydoni dalillari bilan solishtirib tekshirildi |
| Imzolangan to'liq chat eksportlari | Joriy ko'rinadigan tarixni olish, kuzatuv jurnalidan alohida |
| Ishonchli barmoq izlari va avvalgi tekshiruv nuqtalari | Asosiy identifikator va saqlangan jurnal chegaralari |
| Witness artefaktlari, agar sozlangan bo'lsa | Alohida jurnal, imzolangan postlar va guvoh barmoq izi |
| Verifikatsiya natijalari va yetkazib berilgan fayl hashlar | Nima tekshirildi, qaysi baytlar kimga uzatildi |

Ishonchli o'rnatmadan, fayl nomlari va har bir ish maydonining haqiqiy barmoq izi bilan:

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
python -m tgwitness.verify profiles-operations.json --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --evidence evidence.zip
python -m tgwitness.verify history-channel.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256
```

Haqiqiy tekshiruv natijalari va asl artefaktlar saqlanadi. Eng yuqori darajadagi ish katalogi, manba registri va tahlilchi xulosalari tashqarida saqlanadi; har bir TgWitness artefaktining o'z imzosi va tekshiruv tartibi mavjud.

## Tergovni moslashtiring

| Holat | Iz | Yetkazib bering |
| --- | --- | --- |
| Bot tomonidan boshqariladigan buyurtma/to'lov nizosi | Yozuv e'lon qilish → saqlangan havola ko'rinishi → botni ishga tushirish parametri → xabar va klaviatura versiyalari → panel chaqiruvlari kvitansiyalari → shaxsiy/guruh bo'yicha keyingi kuzatuv | Kuzatilgan taklif/javob vaqt chizig'i va tasdiqlangan manbalar; faqat to'lov havolasi to'lovni isbotlamaydi |
| Voqeadan keyin o'chirib tashlangan xabarlar | Ta'sirlangan barcha suhbatlar → saqlangan asl nusxalar/tahrirlar → o'chirish yoki qayta tekshirishda yo'qolish natijalari → saqlangan media → yoritish va boshqa hisob nuqtai nazarlari | Saqlangan versiyalar va aniq noma'lum oraliklar; ixtiro qilingan o'chirish sub'ekti yo'q |
| Ishtirokchi suhbatlar bo'ylab ismlarini o'zgartiradi | Raqamli jo'natuvchi ID → ism/foydalanuvchi nomi tarixi → javoblar → boshqa kuzatilgan suhbatlar → keltirilgan manzillar/fayllar | Keltirilgan Telegram-akun faoliyati kronologiyasi, real dunyo shaxsiyati va munosabatlar bo'yicha taxminlar alohida saqlangan |

[Yig'ish manbai](https://phishdestroy.github.io/TgWitness/uz/docs/reference/collection/) · [Foydalanuvchi profilini tasdiqlash](https://phishdestroy.github.io/TgWitness/uz/docs/reference/evidence/#people-profiles) · [Dalillarni topshirish](https://phishdestroy.github.io/TgWitness/uz/docs/reference/evidence/#investigation-handoff) · [Validatsiya yakunlandi](https://phishdestroy.github.io/TgWitness/uz/docs/reference/verification/)
