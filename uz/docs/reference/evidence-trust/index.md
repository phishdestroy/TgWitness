# Dalil va ishonch

Canonical page: https://phishdestroy.github.io/TgWitness/uz/docs/reference/evidence-trust/

Eksport qilingan ma'lumotlar, videolar, veb-arxivlar va imzolangan yozuvlar nima isbotlashi mumkinligi hamda yig'ish qurilmasi ularning ishonchliligiga qanday ta'sir qilishi.

Eksport, skrinshot yoki yozib olingan material foydali dalil bo'lishi mumkin. Uning ishonchliligi qanday to'plangan, saqlangan va tasdiqlanganligiga bog'liq. **Haqiqiy xesh yoki imzo saqlangan materialni tekshiradi; u mustaqil ravishda to'plovchi qurilma rost manba kontentini olganini aniqlamaydi.** Ushbu chegarani TgWitnessga ham qo'llash mumkin.

Ushbu qo'llanma texnik tasdiqlashni huquqiy baholashdan ajratadi. Mahsulot hujjatlari va quyidagi huquqiy qoidalar 2026-yil 1-noyabrda ko'rib chiqilgan; Hunchly taqqoslovi uning e'lon qilingan hujjatlarini, yangi mahsulot auditi emas, tasvirlaydi.

## Ishonch qaydga olish jarayoniga qo'shilganda

Oqim sxemasi · Telegram akkaunti va xizmati → Mijoz, brauzer va operatsion tizim; Mijoz, brauzer va operatsion tizim → Eksport, video yoki sahifa yozib olish; Eksport, video yoki sahifa yozib olish → Hashlar va yig'uvchi imzolari; Hashlar va yig'uvchi imzolari → Mustaqil tomon saqlagan xesh · Telegram akkaunti vaxizmati · Mijoz, brauzer vaoperatsion tizim · Eksport, video yokisahifa yozib olish · Hashlar va yig'uvchiimzolari · Mustaqil tomonsaqlagan xesh

**Diagramma matn sifatida**

1. Telegram akkaunti va xizmati → Mijoz, brauzer va operatsion tizim
2. Mijoz, brauzer va operatsion tizim → Eksport, video yoki sahifa yozib olish
3. Eksport, video yoki sahifa yozib olish → Hashlar va yig'uvchi imzolari
4. Hashlar va yig'uvchi imzolari → Mustaqil tomon saqlagan xesh

Bu yerda tahdid modeli dalillar yozib qo'yilishidan oldin yig'ish muhitini hujumchi yoki operator o'zgartirishi mumkinligini taxmin qiladi. Bu shartli tahlil bo'lib, ma'lum bir qurilma yoki mahsulot buzilganligi haqidagi da'vo emas.

Rasmiy mijoz va shifrlangan ulanish odatiy foydalanishni himoya qilishga yordam beradi. Ular atrofdagi operatsion tizim, brauzer yoki displeyni mustaqil ravishda ishonchli qilmaydi. Agar kontent dekripsiyadan keyin, lekin qayd etilishidan oldin almashtirilsa, eksport qiluvchi uni aniq saqlay oladi va imzolovchi uni to'g'ri imzolashi mumkin. Hech bir amaliyot buzilgan xesh algoritmi yoki soxta imzoga muhtoj emas.

Bir xil qurilmada yaratilgan video ham bir xil almashtirilgan taqdimotni yozib olishi mumkin. Alohida kamera displeyda nimani ko'rsatilganini tasdiqlay oladi, lekin faqatgina displey Telegram taqdim etgan narsani autentifikatsiya qilmaydi. Xuddi shunday, bir nazorat ostidagi muhitdan olingan mos keluvchi HTML, JSON, skrinshotlar va brauzer jurnallari ham bir xil xatolikni ko'rsatishi mumkin. Ularning mosligi foydali kontekstdir; bu avtomatik ravishda mustaqil tasdiq emas.

## Har bir dalil shakli nimani qo'shadi

| Material | Foydali hissa | Qolgan savol |
| --- | --- | --- |
| Telegram Desktop eksporti | O'qiladigan yoki mashina o'qiy oladigan suhbatlar va tanlangan media | Kim mijoz va eksport fayllarini nazorat qilgan, nima kiritilgan yoki chiqarib tashlangan? |
| Ekran fotosurati yoki ekran yozuvi | Ko'rinadigan kontekst, harakatlar ketma-ketligi va taqdimot | Taqdimot manbani sodiqlik bilan aks ettiradimi va yozuvdan tashqarida nima bo'lgan? |
| Mahalliy veb-arxiv, jumladan MHTML | Keyinchalik tekshirish uchun sahifa mazmuni va unga tegishli resurslar | Brauzer arxivlovchiga nima taqdim etdi va o'sha brauzerni kim nazorat qilgan? |
| Yig'uvchi imzolagan arxiv | Imzolangan baytlarga kiritilgan o'zgarishlarni ishonchli kalit va saqlangan havolaga nisbatan aniqlash mumkin | Imzolash kaliti va imzolashdan oldin kiritilgan ma'lumotni kim nazorat qilgan? |
| Mustaqil saqlangan tekshiruv nuqtasi yoki tasdiqlangan vaqt tamg'asi | Keyinchalik topshiriladigan ma'lumot bilan solishtirish uchun saqlangan xesh yoki nazorat nuqtasi | Qaysi baytlar va chegaralar qamrab olingan, va mustaqil tomon aslida nimani tasdiqlaydi? |

Telegram o'zining Desktop eksportini oflayn HTML/JSON nusxasi sifatida va Takeout API'sini tanlangan hisob ma'lumotlarini olish usuli sifatida hujjatlashtiradi. Ushbu tavsiflar qabul qiluvchi tomonidan tekshirish uchun yakuniy eksport qilingan arxiv ustida Telegram imzosi taqdim etmaydi. Bizning xulosamiz shu hujjatlangan eksport mexanizmlari bilan cheklangan; bu Telegram dalillarining huquqiy qiymati yo'qligi haqidagi da'vo emas. [Telegram Desktop eksporti](https://telegram.org/blog/export-and-more),[Takeout API](https://core.telegram.org/api/takeout).

Xuddi shu farq fon so'rovlari, kesh yozuvlari va tarmoq loglariga ham tegishli. Ular nomuvofiqliklarni aniqlashi va to'plamni tasdiqlashga yordam berishi mumkin. Ularning murakkabligi ularni kim yaratganini o'zi aniqlamaydi. Mustaqil boshqariladigan arxiv yoki alohida olingan xizmat yozuvi solishtirish uchun boshqa manbani taqdim etadi, u ham o'z to'plash va saqlash cheklovlariga ega.

## Hunchly bir xil chegarani ko'rsatadi

Hunchly hujjatlari MHTML yozuvlari, fotosuratlar va ilovalarni SHA-256 hashlash hamda mustaqil hashni tekshirishni tasvirlaydi. Shuningdek, yangi hisoblangan hash bilan birga bo'lgan o'zgartirilgan fayl qanday qilib ushbu solishtirishdan o'tishi mumkinligini tushuntiradi va qo'shimcha tekshiruvlar sifatida imzo va manba tasdiqini ko'rsatadi. [Hunchly: kontent, foto va ilovalarni hashlash](https://support.maltego.com/support/solutions/articles/15000061289-content-photo-and-attachment-hashing).

Uning e'lon qilingan *Dalillar bo'yicha qo'llanmasi*, 2018-yil 17-oktabrdagi 1.0-versiyasi, mahalliy yaratilgan GPG kalitlari va MHTML ushlab olishlar uchun imzolarni tasvirlaydi. U aniq ravishda mahalliy maxfiy kalitga kirishni o'zgartirilgan materialni qayta imzolash usuli sifatida belgilaydi. Bu hujjatlashtirilgan ishonch cheklovi bo'lib, oshkor etilmagan joriy ekspluatatsiya dalili emas. Qo'llanmada shuningdek Chrome MHTML ushlashni amalga oshirishi aytiladi. Hunchly faqat tergovchining obro'siga tayanadi deb tasvirlash ushbu texnik nazorat choralarini e'tiborsiz qoldirardi.[Hunchly Dalillar Qo'llanmasi, 2–4-bo'limlar](https://hunch.ly/resources/Hunchly%20Evidence%20Guide.pdf).

Muayyan mahsulot yordamida to'plangan material ishga qabul qilingan yoki yo'qligi tegishli qaror va sharoitlarga bog'liq. Biz bu yerda sudlar Hunchly yoki TgWitness-ni qanchalik tez-tez qabul qilishi yoki ushbu mahsulotlardan birortasining sud tomonidan umumiy tasdiqiga ega ekanligi haqida hech qanday da'vo qilmaymiz.

## TgWitness nimani qo'shadi va uning himoyasi qayerda tugaydi

TgWitness kuzatuvlarni imzolangan, bog'langan jurnalda qayd etadi va qabul qiluvchi tekshirishi mumkin bo'lgan eksportlarni taqdim etadi. Saqlangan tekshirish nuqtalari, vaqt tamg'alari va alohida guvoh ko'rib chiquvchilarga yig'uvchining joriy fayllaridan tashqari manbalarni taqdim etadi. Ular ilgari yozib qo'yilgan yozuvlardagi o'zgarishlarni aniqlashga yordam beradi. Qamrov yozuvlari va aniq yig'ish natijalari nimalar qamrab olinganini va nimalar qamrab olinmaganini tushuntirishga yordam beradi.[Dalil formati va topshirish](https://phishdestroy.github.io/TgWitness/uz/docs/reference/evidence/), [yig'ish doirasi](https://phishdestroy.github.io/TgWitness/uz/docs/reference/collection/).

Ehtimoliy almashtirish vaqti muhim:

1. **Imzolangandan so'ng, imzolash kalitiga kirish huquqisiz:** imzolangan yozuvni yoki manifestga bog'langan faylni o'zgartirish ishonchli verifikator va kalit bilan tekshiruvni muvaffaqiyatsiz yakunlaydi.
2. **Yig'uvchi kaliti bilan, mustaqil tekshiruv nuqtasi saqlanganidan so'ng:** o'rnini bosuvchi jurnalda haqiqiy yangi imzo bo'lishi mumkin, lekin o'zgartirilgan prefiks oldingi tekshiruv nuqtasi bilan solishtirishni muvaffaqiyatsiz qiladi. Faqat bir xil nazorat qilinadigan qurilmada saqlangan tekshiruv nuqtasi jurnal bilan birga o'rnini bosishi mumkin. Saqlangan chegaradan tashqaridagi yozuvlar o'z qamroviga ega bo'lishi kerak.
3. **Kuzatuvni qamrab oluvchi tekshiruv nuqtasi mustaqil ravishda saqlanmasidan oldin:** soxta kirish ma'lumotlari, jumladan avvalgi tekshiruv nuqtasidan keyin qo'shilgan yangi yozuvlar ham muvaffaqiyatli imzolanishi va bog'lanishi mumkin. Hosil bo'lgan tekshiruv nuqtasi yoki vaqt tamg'asi hanuzgacha o'sha soxta yozuvlarni qamrab oladi; u ularning rostligini tasdiqlamaydi.

TgWitness guvohi yig'uvchining imzolangan tekshiruv nuqtalarini oladi; u mustaqil ravishda Telegram suhbatini o'qimaydi. Uning kaliti va saqlangan yozuvlariga alohida ishonish kerak. Agar butun topshirilgan jurnal guvohlik qilinishi kerak bo'lsa,[yakuniy eksport chegarasini talab qiluvchi topshirish tartibidan](https://phishdestroy.github.io/TgWitness/uz/docs/reference/witness/#require-a-witnessed-export-boundary) foydalaning. Oddiy yaxlitlik tekshiruvi guvohlik qilinmagan oxirni hali ham xabar bera oladi.

Tasdiqlangan RFC 3161 javobi vakolatli organ ko'rsatgan vaqtda nazorat nuqtasi mavjud bo'lganini tasdiqlashi mumkin. Bu Telegram xabari qachon yuborilganini yoki uning mazmuni haqiqiy bo'lganini aniqlamaydi. Tayyorlangan so'rov yoki ilova qilingan javob fayli yolg'iz o'zi yetarli emas. Eksportni `tgwitness.verify` orqali tasdiqlashda ilova qilingan TSA imzolarini tekshirish uchun `--tsa-ca` orqali aniq ishonchli CA talab etiladi. OpenTimestamps kvitansiyalari mustaqil `ots verify` talab qiladi, zarur bo'lganda dalillarni yangilash bilan. [Timestamp protsedura](https://phishdestroy.github.io/TgWitness/uz/docs/reference/timestamp/), [RFC 3161](https://www.rfc-editor.org/rfc/rfc3161.html).

[GitHub Actions yozib olishda](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md), vaqtinchalik joylashtirilgan ijrochi (runner) xabarlarni to'playdi. Tasdiqlash arxivni ma'qullangan ish jarayoniga bog'laydi. Ushbu rejim hanuz GitHub, ma'qullangan dasturiy ta'minot va uning bog'liqliklari, yordamchi/brauzer va tunnelga ishonadi. Bu maxfiy apparat, Telegram imzosi yoki hech kim mezbonga kira olmaganligini isbotlovchi dalil emas. Mahalliy imzolangan ijro kvitasi ham o'z-o'zini xabar qiluvchi o'lchov bo'lib, apparat tasdiqlashi emas.

## Huquqiy og'irlik poydevorga bog'liq

To'rt savol alohida qolishi kerak: ob'ekt aytilganidekmi, yuborilgan baytlar saqlangan yozuvga mos keladimi, mazmun da'vo qilingan faktlarni qo'llab-quvvatlaydimi, va tegishli qoidalar uning ishlatilishiga ruxsat beradimi. Kriptografik tekshiruv faqat shu poydevorning bir qismini qamrab oladi.

AQSh federal sud jarayonlarida 901-qoida dalillarni tasdiqlash usullarini, jumladan bilimdon guvoh guvohligi va jarayon yoki tizim haqidagi dalillarni o'z ichiga oladi. 902(13) va 902(14)-qoidalarda ma'lum elektron yozuvlar va nusxalarni protsessual talablar bilan tasdiqlash yo'llari ko'rsatilgan. Qo'mita izohlarida autentifikatsiya eshitib aytish, dolzarblik va mansublik kabi masalalardan ajratib ko'rsatilgan. Dasturiy imzo o'zi u yerda tasvirlangan malakali shaxsning tasdig'i hisoblanmaydi. [Federal Dalillar Qoidasi 901](https://www.law.cornell.edu/rules/fre/rule_901), [Federal Dalillar Qoidasi 902](https://www.law.cornell.edu/rules/fre/rule_902).

Kanadaning Dalillar to'g'risidagi qonuni qo'llaniladigan hollarda, 31.1-bo'lim elektron hujjatlarni autentifikatsiya qilishni tartibga soladi. 31.2-bo'lim eng yaxshi dalil qoidasini tizim yaxlitligi yoki tegishli taxmindan kelib chiqish bilan bog'laydi; 31.3-bo'lim esa yaxlitlik taxmini qo'llash shartlarini belgilaydi. Bular aniqlangan dalil shartlari bo'lib, har qanday litsenziyalangan tergovchi yoki tijorat mahsuloti xatoga yo'l qo'ymaydi degan umumiy taxmin emas. [Kanada Dalillar to'g'risidagi qonuni, 31.1](https://laws-lois.justice.gc.ca/eng/acts/C-5/section-31.1.html),[31.2](https://laws-lois.justice.gc.ca/eng/acts/C-5/section-31.2.html),[31.3](https://laws-lois.justice.gc.ca/eng/acts/C-5/section-31.3.html).

Ushbu misollar boshqa yurisdiktsiyada yoki ma'lum bir ishda qabul qilinishni hal qilmaydi. Texnik tekshiruvlar da'voni qo'llab-quvvatlovchi yoki uni inkor etuvchi materiallarga izchil qo'llanilishi kerak. Ushbu qo'llanma prokuratura dalillarini mudofaa dalillariga nisbatan odatda qabul qilish osonroq, deb da'vo qilmaydi.

## Boshqa shaxs baholay oladigan yozuvni tayyorlang

- Hisob, yig'ish qurilmasi, operator, dasturiy ta'minot versiyasi, kirish huquqlari, tanlangan doira va yig'ish muddatini tasvirlang. Muvaffaqiyatli imzo tekshiruvini toza qurilma sinovi deb hisoblash o'rniga uzilishlar va mumkin bo'lgan buzilishlarni qayd eting.
- Asl paketlarni saqlang va uzatmalar, xeshlar hamda vaqt manbasini qayd eting. Kalit barmoq izini va tekshiruv nuqtalarini alohida ishonchli kanal orqali saqlang. Hisobotda tasvirlashdan oldin haqiqiy guvoh yoki vaqt tamg'asi qamrovini tasdiqlang.
- Da'vo uchun mos mustaqil tasdiqni izlang: boshqa ishtirokchining yozuvlari, mustaqil qayd yoki qonuniy olingan xizmat yozuvlari. Ularning mustaqilligi va cheklovlarini tushuntiring; nusxalar o'rtasidagi kelishuv o'zi yetarli emas.
- Muvofiq kontekstni saqlang. O'chirib tashlangan fayllar, mavjud bo'lmagan tarix va redaksiyalarni aniqlang. Zarur bo'lganda [alohida minimallashtirilgan oshkor etishni](https://github.com/phishdestroy/TgWitness/blob/main/docs/ACCOUNT-EXPORT.md#prepare-a-disclosure-for-a-lawyer-or-another-recipient)tayyorlang va uni to'liq asl nusxa sifatida ko'rsatmasdan uning o'zgartirishlarini tasvirlang.
- Qabul qiluvchiga tasdiqlash bo'yicha ko'rsatmalar va bu tekshiruvlar uchun zarur materiallarni bering. Kuzatuvlar, texnik topilmalar va tahlilchining xulosalarini ajratib ko'rsatadigan qiling.

Muayyan topshirish uchun arxiv xeshini, ishonchli kalitni, tasdiqlash natijasini va aniq tashqi qoplangan chegarani ko'rsating. Manbaning haqiqiyligini, hisobga tegishliligini, to'liqligini va huquqiy xulosalarni alohida bayon qiling. Bu keyingi ko'rib chiquvchiga tekshirish uchun aniq da'volarni beradi.
