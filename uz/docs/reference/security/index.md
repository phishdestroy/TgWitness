# Xavfsizlik va ma'lumotlarni boshqarish

Canonical page: https://phishdestroy.github.io/TgWitness/uz/docs/reference/security/

Xavf modeli, kirish modeli, saqlashdagi sirlar, tarmoqdagi ochiqlik, sessiya importlari va zaiflikni qanday xabar qilish.

TgWitness sizning shaxsiy kompyuteringizda yoki serveringizda ishlaydi. Hisob ma'lumotlari ulanishlari, ommaviy proxy-ro'yxatni yuritish va ixtiyoriy tashqi xizmatlar aniq marshrutlash siyosatiga ega. Bildirishnomalar, vaqt tamg'alari, masofaviy nusxalar va guvoh alohida sozlanadi. Ushbu sahifada nima himoyalanganligi, qanday himoyalanganligi va operatorga qanday vazifalar qoldirilganligi ko'rsatilgan.

| Soha | Qisqasi |
| --- | --- |
| Kirish | Administrator kaliti va hisoblar/suhbatlarga chegaralangan kirish, yetti ruxsat va bekor qilinishi mumkin bo'lgan sessiyalar; standart bo'yicha localhost |
| Saqlangan sirlar | Sessiya, API juftligi, imzolash kaliti va proksi sozlamalari Fernet bilan shifrlangan |
| Xabarlar va media | Shifrlanmagan holda saqlanadi: diskni shifrlash va qat'iy ruxsatnomalarni qo'llang |
| Buzilmaslik | Har bir yozuvda SHA-256 xesh zanjiri va Ed25519 imzosi |
| Qamrab olinmagan | Mashina ma'muri, oshkor bo'lgan panel tokeni, yozib olish to'liqligi |

Zaifliklar bo'yicha hisobotlar uchun [xavfsizlik siyosat](https://github.com/phishdestroy/TgWitness/blob/main/.github/SECURITY.md)iga qarang.

## Kirish modeli

Asosiy panel tokeni to'liq nazoratni beradi. Boshqa foydalanuvchilar o'zlariga [moslashtirilgan kirish huquqini](https://phishdestroy.github.io/TgWitness/uz/docs/reference/access/) olishlari mumkin: tanlangan ish maydonchalari va suhbatlar, ruxsatnomalar, amal qilish muddati, IP-cheklovlar, tizimga kirish limitlari va bekor qilinishi mumkin bo'lgan sessiyalar. Suhbatlarga cheklangan kirish huquqi, hatto tegishli ruxsat belgilangan bo'lsa ham, butun ish maydonchasi bo'yicha amaliyotlarni bajarolmaydi. Ish maydonchalari jarayonni baham ko'radi va ma'lumotlarni mezbon ma'muridan ajratmaydi.

Panel mahalliy tarmoq (localhost) orqali standart bo'yicha tinglaydi. Brauzerda tizimga kirish sessiya ma'lumotini kirish tokeniga almashtiradi; brauzer uni bearer tokeni sifatida yuboradi. U autentifikatsiya cookie o'rniga sessionStorage'da saqlanadi. Qulflash/chiqish brauzer sessiyasini tozalaydi. Brauzerni yopish yoki sessiyani tugatish ma'lumotlarni yig'ishni to'xtatmaydi.

Chiqarilgan tokenlar va sessiya ma'lumotlari shifrlangan omborda xeshlar ko'rinishida saqlanadi. Bekor qilish tegishli sessiyalarni tugatadi; ruxsat o'zgarishlari keyingi so'rovlarga ta'sir qiladi. Yuklab olingan fayllarni qaytarib olib bo'lmaydi. Administrator o'z brauzer sessiyalarini ham cheklashi mumkin, ammo asosiy panel tokenidan to'g'ridan-to'g'ri foydalanadigan skriptlar to'liq kirishni saqlab qoladi va brauzer sessiyasi cheklovlarini chetlab o'tadi.

Avtorizatsiya muvaffaqiyatsiz bo'lsa, mijoz manzili bo'yicha tez-tezlik cheklovi qo'llanadi. IP-cheklovlar ilova ko'rayotgan manzilga asoslanadi; unga tayanishdan oldin teskari proksi xatti-harakatlarini tekshiring. Witness hisob ma'lumotlari alohida, faqat o'qish uchun mo'ljallangan tekshiruv nuqtasi/sog'liqni tekshirish ma'lumotlari bo'lib qoladi.

### Demo kirish

`/api/demo-access` aniq boshlangan, izolyatsiyalangan sintetik demo uchun ataylab autentifikatsiyalanmagan bootstrap hisoblanadi. U alohida jarayon umrboqiyligi imkoniyatini beradi, hech qachon haqiqiy panel tokeni yoki TGWITNESS_TOKEN ustuvor tokenini bermaydi. Chiqarish va foydalanish loopback tengdosh va mezbonni, yo'naltirilgan sarlavhalarni va manba-aralash so'rovlarni talab qiladi. Qo'shimcha ish maydonchalari yoki ruxsat etilgan sessiya ushbu yo'nalishni o'chirib qo'yadi. Jonli ish maydonchalari hech qachon ushbu imkoniyatni bermaydi. Demo hisoblarni bog'lay olmaydi yoki yig'ish sozlamalarini o'zgartira olmaydi.

## Panel mazmuni va eksportlari

Panel hech qanday tashqi shriftlar, tahliliy vositalar, CDN resurslari yoki o'rnatilgan masofaviy media elementlaridan foydalanmaydi. Telegram manbasidan olingan matn HTML emas, oddiy matn sifatida kiritiladi. Yuklab olingan ilovalar binar ilovalar sifatida taqdim etiladi. JSONL eksporti asl satrlarni saqlaydi; HTML ularni qochiradi; formulaga aylanishi mumkin bo'lgan CSV hujayralari esa apostrof bilan boshlanadi.

Eksportlar autentifikatsiya va imzolash sirlarini o'z ichiga olmaydi, lekin ataylab to'plangan manba metama'lumotlari, identifikatorlar va ehtimol shaxsiy yoki nozik kontentni o'z ichiga oladi. Telegramga kirish hashlar va fayl havolalari xom manba metama'lumotlarida uchrashi mumkin.

## Saqlangan sirlar

Telegram API kreditsialari, StringSession va Ed25519 xususiy kaliti Fernet yordamida shifrlanadi. Standart bo'yicha uning kaliti shu himoyalangan ma'lumotlar papkasi ichida saqlanadi. Bu tasodifan oddiy matnning oshkor bo'lishini kamaytiradi; bu butun katalogni o'qiy oladigan hujumchiga qarshi himoya emas. TgWitness xabar mazmuni va media fayllarini **shifrlamaydi** . Diskni shifrlash va operatsion tizim ruxsatlarini cheklashdan foydalaning. Unix shaxsiy kalit fayllari 0600 rejimida yaratiladi; yangi yaratilgan ma'lumotlar kataloglari 0700 rejimidan foydalanadi. Mavjud papka ruxsatlari o'zgartirilmaydi. Windows papka ACLlarini meros qilib oladi: ularni faqat xizmat akkaunti va vakolatli administratorlarga cheklang.

### Tashqi bosh kalit

Yangi ma'lumotlar katalogi uchun TGWITNESS_VAULT_KEY_FILE tashqi tasodifiy bosh kalitni ta'minlashi mumkin. HKDF-SHA256 va alohida tasodifiy salt har bir ish maydoni uchun turli Fernet kalitini hosil qiladi. vault.external.json tiklash uchun saqlanishi kerak. Yo'qolgan yoki noto'g'ri bosh kalitlar yopilishga olib keladi. Mavjud mahalliy omborlar jimjit ko'chirilmaydi. Ijro etilayotgan jarayon kalitga kirish huquqiga ega; bu HSM izolyatsiyasi emas. Panel tanlangan rejimni xabar qiladi va xabar/media saqlovi ilova tomonidan shifrlanmaganligini aniq ko'rsatadi. To'liq tahdid modelini ko'rish uchun [ulanish, proksi-serverlar va ma'lumotlarni himoya qilish](https://phishdestroy.github.io/TgWitness/uz/docs/reference/connection/) bo'limlariga murojaat qiling.

## Proxy-lar va tarmoq yo'nalishlari

Proxy konfiguratsiyasi omborda shifrlanadi. Parollar va MTProxy sirlar API orqali qaytarilmaydi yoki dalil yozuvlariga yozilmaydi. Har bir ish maydoni o'z Telegram yo'nalishi va [IP rejimini](https://phishdestroy.github.io/TgWitness/uz/docs/reference/connection/#ip-modes) tanlaydi.

IP yashirish rejimi Telegramga to'g'ridan-to'g'ri zaxira ulanishni rad etadi va tashqi HTTP so'rovlari uchun proksi talab qiladi. Aniq tanlangan zaxira rejimi kechikishdan so'ng Telegramga to'g'ridan-to'g'ri ulanishga ruxsat beradi; tunnel/VPN rejimi esa to'g'ridan-to'g'ri yo'nalishlarni ta'minlaydi. Tunnel rejimini tanlash VPNni o'rnatmaydi yoki tekshirmaydi. Ushbu sozlamalar butun qurilma trafigini, brauzerlarni, paket menejerlarini yoki mahalliy proxy-host DNS aniqlashni nazorat qilmaydi.

MTProxy faqat Telegram trafigini uzatadi. Tashqi so'rovlar alohida SOCKS5/HTTP proksidan, ish maydonining SOCKS5/HTTP yo'nalishidan yoki ruxsat etilgan to'g'ridan-to'g'ri yo'ldan foydalanishi mumkin; ularni o'chirib qo'yish ham mumkin. Mustaqil guvoh o'z transport sozlamalariga ega. Oddiy SOCKS5/HTTP CONNECT autentifikatsiyasi o'sha proksi protokollari tomonidan shifrlanmaydi. Soxta TLS MTProxy sirlarini qo'llab-quvvatlash hali ham mavjud emas.

## Kirish va sessiya importlari

Konvertlangan .tgwitness-session fayllarida oddiy matnda avtorizatsiya sirini o'z ichiga oladi, ular omborga yuklanib saqlanmaguncha. Oflayn CLI ko'rib chiqilgan Telethon sxemalarini qabul qiladi. Panel importi shuningdek Pyrogram SQLite, zamonaviy yagona akkauntli TData ZIP va hujjatlashtirilgan JSON kirishlarni qabul qiladi. U autentifikatsiyalangan, to'rtta fayl / 8 MiB bilan cheklangan va yuklamalarni arxivni chiqarib olish yoki asl fayllarni saqlashsiz xotirada qayta ishlaydi. Normalizatsiyalangan kreditsialar faqat so'rov yuborgan autentifikatsiyalangan brauzerga qaytariladi; ular Telegramda muvaffaqiyatli ruxsat berilgach shifrlangan omborga saqlanadi. Asl fayllar va konvertatsiya qilingan fayllarni himoya qiling va bir vaqtning o'zida bir nechta mijozlarning ruxsatnoma nusxasini yaratishining oldini oling.

TData ishlovi konteyner tekshiruv yig'indilarini, mahalliy dekriptirovka xeshlarini va tuzilma uzunliklarini tasdiqlaydi. Taqdim etilgan Desktop mahalliy paroli vaqtinchalik ishlatiladi va saqlanmaydi. Ushbu chegaralangan parser har bir Desktop versiyasining mos kelishini kafolatlamaydi. QR tasvirlari mahalliy ravishda yaratiladi, qisqa muddatli Telegram kirish tokenlarini o'z ichiga oladi va hech qachon tashqi render xizmatiga yuborilmaydi. Bloklash, ish maydoni o'zgarishi, yangi kirish va yo'nalish o'zgarishlari kutayotgan QR urinishlarini bekor qiladi. Veb-sahifani qayta yuklash yoki yopish urinishni muddat tugaguncha kutayotgan holda qoldirishi mumkin. Muvaffaqiyatli QR kirish hisobni bog'lashni baribir majburiy qiladi. Oddiy API tanalari 16 KiB bilan cheklangan bo'lib qoladi; autentifikatsiyalangan import yo'li esa kodlangan JSON uchun 12 MiB gacha qabul qiladi, dekompressiyalangan faylning kichikroq limitini alohida qo'llaydi.

Kirish kodlari va Telegram ikki bosqichli tasdiqlash parollari saqlanmaydi. Telefon raqami/kod-hash holati avtorizatsiya vaqtida xotirada saqlanadi. Telegram sessiyalari hisobga kirish huquqini beradi; hech qachon ma'lumotlar katalogi, sessiya, token, xazina kaliti yoki xususiy imzo kalitini GitHubga yuklamang.

## Loglar va transport

Standart API tasdiqlash javobi o'zgartiriladi, shunda u autentifikatsiya ma'lumotlarini aks ettirmaydi. Ilova kirish logi o'chirilgan. Revers proksi sozlamang, Authorization sarlavhalari yoki so'rov tanalarini yozib olish uchun. HTTP tokenlar va kirish sirlarini oddiy matnda uzatadi: localhostdan tashqariga chiqayotganda HTTPS yoki SSH tunneli ishlating.

## Buzilmaslik chegaralari

Hash zanjiri, ma'lumotlar bazasi trigerlari va imzolar ma'lum o'zgartirishlarni aniqlaydi; ular mahalliy administratorning jurnalni qayta yozishi va qayta imzolashini oldini olmaydi. Imzolangan tekshiruv nuqtalarini va ommaviy kalit barmoq izini alohida tizimda saqlang. Dalil rejimi va masofaviy nusxa (ikkovlasi ham standart bo'yicha o'chirilgan) tekshiruv nuqtasi xeshlarini vaqt belgilash xizmatlariga va S3-ga mos saqlashga shifrlangan nusxalarni yuboradi; [dalil format](https://phishdestroy.github.io/TgWitness/uz/docs/reference/evidence/)iga qarang. Ochiqlik jurnallari, HSM bilan qo'llab-quvvatlanadigan imzolash va rasmiy zanjir bo'ylab mulkchilik sertifikati amalga oshirilmagan.

## Agar muammo borligiga shubha qilsangiz

Asl ma'lumotlar katalogini saqlang va tahlil uchun alohida nusxa ishlating. Xususiy Telegram ma'lumotlari yoki kirish ma'lumotlarini ommaviy masalaga kiritmang. Hech qanday mustaqil xavfsizlik sertifikati da'vo qilinmaydi.
