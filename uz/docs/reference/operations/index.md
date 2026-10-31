# Ish jarayonlari va operatsiyalar

Canonical page: https://phishdestroy.github.io/TgWitness/uz/docs/reference/operations/

Panelning kundalik ishlashi: rejimlar, monitoring kategoriyalari, parametrlar, bildirishnomalar, eksportlar, zaxira nusxasi va sig'im.

Birinchi ulanishingiz uchun [akkauntlar va sessiya formatlaridan](https://phishdestroy.github.io/TgWitness/uz/docs/reference/accounts/) foydalaning. Saqlangan versiyalar, voqea siyosatlari va bo'shliqlar haqida tushuntirish uchun [yig'ish qanday ishlashini](https://phishdestroy.github.io/TgWitness/uz/docs/reference/collection/) ko'ring. Ushbu qo'llanma kundalik ish faoliyati va tiklashni qamrab oladi.

## Operator ish jarayoni

Oqim sxemasi · Saqlash va kalitni himoya qilishni tanlang → O'z tokeni bilan panelni oching; O'z tokeni bilan panelni oching → Ish maydonini tanlang; Ish maydonini tanlang → To'g'ridan-to'g'ri yoki proxy yo'nalishini sozlang; To'g'ridan-to'g'ri yoki proxy yo'nalishini sozlang → Telefon raqamini kiriting yoki fayllarni / QRni tanlang; Telefon raqamini kiriting yoki fayllarni / QRni tanlang → Hisob identifikatsiyasini tekshiring va kirish mumkin bo'lgan guruhlarni tanlang; Hisob identifikatsiyasini tekshiring va kirish mumkin bo'lgan guruhlarni tanlang → Voqea va ilovalar siyosatini saqlang, so'ng kuzatuvni boshlang; Voqea va ilovalar siyosatini saqlang, so'ng kuzatuvni boshlang → Xatolar, kirish, navbatlar va diskni monitoring qiling; Xatolar, kirish, navbatlar va diskni monitoring qiling → Mustaqil tekshiruv nuqtalarini saqlab qolish; Mustaqil tekshiruv nuqtalarini saqlab qolish → Materialni eksport qiling va tekshiring · Saqlash va kalitnihimoya qilishnitanlang · O'z tokeni bilanpanelni oching · Ish maydonini tanlang · To'g'ridan-to'g'riyoki proxyyo'nalishini sozlang · Telefon raqaminikiriting yokifayllarni / QRnitanlang · Hisobidentifikatsiyasinitekshiring va kirishmumkin bo'lganguruhlarni tanlang · Voqea va ilovalarsiyosatini saqlang,so'ng kuzatuvniboshlang · Xatolar, kirish,navbatlar va disknimonitoring qiling · Mustaqil tekshiruvnuqtalarini saqlabqolish · Materialni eksportqiling va tekshiring

**Diagramma matn sifatida**

1. Saqlash va kalitni himoya qilishni tanlang → O'z tokeni bilan panelni oching
2. O'z tokeni bilan panelni oching → Ish maydonini tanlang
3. Ish maydonini tanlang → To'g'ridan-to'g'ri yoki proxy yo'nalishini sozlang
4. To'g'ridan-to'g'ri yoki proxy yo'nalishini sozlang → Telefon raqamini kiriting yoki fayllarni / QRni tanlang
5. Telefon raqamini kiriting yoki fayllarni / QRni tanlang → Hisob identifikatsiyasini tekshiring va kirish mumkin bo'lgan guruhlarni tanlang
6. Hisob identifikatsiyasini tekshiring va kirish mumkin bo'lgan guruhlarni tanlang → Voqea va ilovalar siyosatini saqlang, so'ng kuzatuvni boshlang
7. Voqea va ilovalar siyosatini saqlang, so'ng kuzatuvni boshlang → Xatolar, kirish, navbatlar va diskni monitoring qiling
8. Xatolar, kirish, navbatlar va diskni monitoring qiling → Mustaqil tekshiruv nuqtalarini saqlab qolish
9. Mustaqil tekshiruv nuqtalarini saqlab qolish → Materialni eksport qiling va tekshiring

Avtorizatsiya, transport ulanishi, guruhga kirish va yetkazib berish to'liqligi turli xususiyatlardir. Yashil ulanish holati barcha voqealar qayd etilganini anglatmaydi.

## Asosiy kalitni ulashmasdan ishni ulashing

Ochiq **kirish** tahlilchi yoki ko'rib chiquvchiga o'z tokenini berish imkonini beradi. Ular ochishi mumkin bo'lgan hisoblar va suhbatlarni tanlang, so'ngra ko'rish, eksport qilish yoki operativ harakatlarni amalga oshirishga ruxsat bering. Yig'ishni boshlaydigan/to'xtatadigan operatorga butun ish maydoni bo'yicha kirish huquqi kerak; ko'rib chiquvchi esa bitta suhbat bilan cheklanishi mumkin. Sessiya cheklovlari, amal qilish muddati va IP-manzil qoidalari Telegram hisobini avtorizatsiya qilishdan alohida. [Kirish huquqlari va ruxsatnomalarni](https://phishdestroy.github.io/TgWitness/uz/docs/reference/access/) ko'ring.

**Open sessions** ulanishni yakunlash yoki uning barcha sessiyalariga kirishni bekor qilish uchun ishlatiladi. Administrator konsoli ish maydonlari bo'ylab joriy jarayon faoliyatini birlashtiradi. Sessiyani yopish ma'lumotlarni yig'ishni davom ettiradi.

## Ijro rejimlari

| Rejim | Harakat | Xulq-atvor |
| --- | --- | --- |
| Demo | scripts\Demo.cmd yoki `--demo` | Sintetik ma'lumot; haqiqiy akkauntlar o'rtasidagi bog'lanishlar o'chirib qo'yilgan |
| Kuzatuv | Kuzatuvni boshlang | Tanlangan manbalar uchun yetkazilgan yangilanishlarni qayd eting |
| Tarixning tezkor ko'rinishi | Manbalar → tarixning snapshoti | Joriy 500 tagacha xabar; barcha avvalgi o'zgarishlarni qayta tiklash yo'q |
| Tanaffus | Kuzatuvni to'xtatish | To'plashni to'xtating, ma'lumotlar va navbatdagi ishlarni saqlab qolgan holda |
| Ko'rib chiqish/topshirish | Eksportlar | ZIP, JSONL/CSV/HTML, tekshiruv nuqtasi, jarayon kvitasi va vaqt tamg'asi so'rovi |
| Bir nechta hisoblar | Ish maydonchalari yoki yuqoridagi **+** tugmasi | Bir jarayonda istalgan sonli alohida ish maydonchalari |

Mahalliy demo kirish qo'lda token kiritmasdan avtomatik ochiladi. U izolyatsiyalangan sintetik demo uchun to'g'ridan-to'g'ri loopback-kirishga haqiqiy bo'lgan, jarayon umrboqiyligi imkoniyatidan foydalanadi; asosiy panel tokeni oshkor etilmaydi. Haqiqiy ish maydonchalari va masofaviy yoki proksi orqali demo kirish token autentifikatsiyasini saqlab qoladi. Demo kirish Telegramga ruxsat bermaydi.

## Monitoring toifalari

![Har bir hisob uchun monitoring sozlamalari sun'iy manba ma'lumotlari bilan](https://phishdestroy.github.io/TgWitness/assets/sources.png)

**Manbalar → Yozib olish sozlamalari → Qaysi o'zgarishlarni saqlashni tanlash** bo'limida yangi xabarlar, tahrirlar, o'chirish bildirishnomalari, reaktsiya yangilanishlari va a'zolik voqealarini alohida tanlang. Standart sozlama barcha toifalarni saqlaydi. "**Xabarlar, tahrirlar va o'chirishlar**" esa alohida reaktsiya/a'zo yangilanishlarini o'chirib, asl kontekstni saqlaydi. **Ko'rinadigan barcha faoliyat** beshtasini ham tiklaydi. Oldindan sozlamalar shaklni o'zgartiradi; qo'llash uchun **Monitoring sozlamalarini saqlash tugmasini** bosing.

Saqlangan siyosat shu ish maydonidagi barcha tanlangan manbalarga tatbiq etiladi. Boshqa ish maydonchalari o'z sozlamalarini saqlab qoladi. Har bir haqiqiy o'zgarish imzolangan oldingi/keyingi qiymatlarni qayd etadi; joriy siyosat jarayon kvitansiyalari va kuzatuv boshlanishi yozuvlariga ham kiritilgan. Toifani o'chirish oldingi kuzatuvlarni o'chirib tashlamaydi. Uni qayta yoqish o'tkazib yuborilgan o'zgarishlarni qaytarib bermaydi. Ushbu versiyada guruh bo'yicha kategoriyani ustuvor qilish imkoniyati mavjud emas.

Avvalgi kontent muhim bo'lganda yangi xabarlarni yoqib qo'ying: o'chirish bildirishnomasi hech qachon qayd etilmagan matnni qaytarib berolmaydi. Operatsion/qamrov yozuvlari va boshqa guruh xizmat voqealari har doim saqlanadi. Aniq tarix snopshotlari jonli-kategoriya tanlovidan alohida bo'lib, xizmat xabarlari ham bo'lishi mumkin. Ushbu kalitlar aks holda qayd etilgan Telegram ob'ektiga kiritilgan reaktsiya/a'zo metama'lumotlarini o'chirib tashlamaydi.

Tarix snappoti to'xtatilganda ilovalarni navbatga qo'yishi mumkin. Ularni qayta ishlash uchun kuzatuvni boshlang. Navbatga qo'yilgan bo'lish yuklab olingan degani emas. Mavjud bo'lmagan asl fayl yangi tahrirlangan versiya bilan almashtirilmaydi; natijalar alohida qayd etiladi.

**Lock** brauzerga kirishni va maxfiy maydonlarni tozalaydi, lekin yig'ishni ishga tushgan holda qoldiradi. Vozkechishni yopish ham jarayonni ishga tushgan holda qoldiradi. Python jarayonini yoki xizmatini to'xtatish brauzer holatidan qat'i nazar yig'ishni to'xtatadi.

Qo'shimcha ish maydonini o'chirish uning yig'uvchisini to'xtatadi va mahalliy ma'lumotlarini o'chirib tashlaydi. Agar qulflangan fayl yoki fayl tizimi xatosi o'chirishni to'xtatsa, panel xatolikni bildiradi va ish maydonini mavjud emas (`DeletionPending`) deb ko'rsatadi. Uning fayllarini ushlab turgan dasturlarni yoping va **O'chirishni** qayta sinab ko'ring. TgWitness-ni qayta ishga tushirish ushbu ish maydonini to'xtatilgan holda qoldiradi va uning qisman o'chirilgan jurnali yoki kalitlarini qayta yaratmaydi. Muvaffaqiyatli o'chirish faqat katalog o'chirib tashlangandan keyin qayd etiladi; alohida eksport qilingan yoki zaxiralangan nusxalar o'z saqlash siyosatiga bo'ysunadi.

## Bildirishnomalar

Ochiq **manbalar → Bildirishnomalar → Ogohlantirishlar va kunlik xulosa**. TgWitness ogohlantirishlarni Matrix, Telegram, Discord, Slack, ntfy, elektron pochta va boshqa qo'llab-quvvatlanadigan xizmatlarga yuborish uchun Apprise-dan foydalanadi. Bir ish maydoniga bir nechta manzillarni qo'shishingiz mumkin.

1. Har bir satrga bitta Apprise manzil URL-ni kiriting. Xizmatingiz uchun [xizmat katalogi va URL formatlaridan](https://appriseit.com/services/) foydalaning.
2. **Xabar yuborishni** yoqing, so'ng muammo bildirishnomalarini, kuzatilayotgan suhbatlardagi o'zgarishlarni va kunlik xulosani tanlang. Xulosa soati server vaqtiga asoslanadi.
3. Agar o'chirib tashlangan va tahrirlangan xabarlardan saqlangan matnni bildirishnomalarda ko'rsatishni istasangiz, **"Qisqa parchalarni kiritish"**ni yoqing.
4. **Bildirishnomalarni saqlash tugmasini** bosing, so'ngra yetkazilishini tekshirish uchun **test yuboring**.

O'zingizning qabul qiluvchingiz uchun Apprise'ning [JSON webhook'idan](https://appriseit.com/services/json/) foydalaning. Masalan, `jsons://notify.example.org/tgwitness` JSON'ni HTTPS orqali shu manzilga yuboradi. Bu badiiy misol; uni o'zingizning manzilingiz bilan almashtiring.

Manzillar va sozlamalar tanlangan ish maydoniga tegishli. Ogohlantirishlar uning kuzatilayotgan manbalarini, jumladan yangi qo'shilgan suhbatlarni ham qamrab oladi. Yuqori panelidagi qo'ng'iroq ham so'nggi muammolar va suhbat o'zgarishlarini ro'yxatlaydi.

Demo rejimida bildirishnoma boshqaruvlari ko'rinadi, ammo yuborish funksiyasi o'chirilgan. Haqiqiy ish muhitida yetkazib berishni sozlang. Bildirishnomalar o'sha ish muhitining Direct, SOCKS5 yoki HTTP yo'nalishidan foydalanadi; MTProxy ularni yetkazib bera olmaydi. SMTP kabi HTTP bo'lmagan manzillar to'g'ridan-to'g'ri yo'nalishni talab qiladi.

## Panel tartibi

![Sun'iy ma'lumotlardan foydalangan holda ulanish ish maydoni](https://phishdestroy.github.io/TgWitness/assets/connection.png)

**Jurnal** kuzatuvlar, qidiruv va filtrlarni ko'rsatadi. Tahrir ushlangan versiyalarni ochadi; o'chirish mavjud bo'lsa, oldingi kontentni ochadi. Noma'lum atribut aniq ko'rsatiladi. Hisoblar **Umumiy ko'rinish** bo'limida mavjud; olish tafsilotlari mahalliy qo'llanmada qoladi.

Tahrirlangan xabarning versiyalarini **Matndagi o‘zgarishlar** yoki **Yonma-yon** yordamida solishtirish uchun uni oching; **Xom ma’lumotlar** saqlangan maydonlarni ko‘rsatadi. Yashirin havolalar va bot tugmalaridagi o‘zgarishlar alohida ko‘rinadi. Saqlangan rasm, audio yoki videolarni ko‘zdan kechirish uchun biriktirma ko‘rinishini oching; yuklab olish tugmasi saqlangan asl nusxadan foydalanish imkonini beradi.

**Live** yozuvlar kelib tushishi bilan jurnal va chatlarni yangilab boradi. Ko‘rib chiqish vaqtida uni pauza qiling yoki tayyor bo‘lganingizda yangi hodisalar tugmasidan foydalaning; ma’lumotlarni yig‘ish davom etaveradi. **Ctrl/Cmd+K** panel amallarini topadi va jurnal bo‘ylab qidiradi.

**Manbalar** kuzatuv doirasini (tanlangan suhbatlar, Telegram papkasi yoki butun akun), har qanday turdagi mavjud suhbatlarni, ustuvor yulduzchali tanlangan manbalarni, ilova va qayta tekshirish sozlamalari hamda tarix snopshotlarini o'z ichiga oladi. Xususiy manbalar dialog/ID orqali tanlanadi, ommaviy havola yo'q. Kirish holati eng so'nggi tekshiruvni tasvirlaydi, doimiy ruxsatnomalarni emas.

Manbalarni filtrlang, ularning katakchalarini belgilang, so‘ngra ularni birgalikda yoqing, pauza qiling yoki ustuvor sifatida belgilang. Mavjud chatlar ro‘yxatida **Tanlanganlarni qo‘shish** sizning tanlovingizdan foydalanadi; **Barcha mos natijalarni qo‘shish** esa joriy qidiruv va tur filtridan foydalanadi.

**Suhbatlar →** Saqlangan xabarlari bo'lgan barcha **odamlarni** ro'yxatlaydi; suhbat uchun odam profillari yoqilganda, ustiga bosish shu shaxsning profilini jurnal yozuvlari havolalari bilan ochadi.

**Witness** o'qish uchun mo'ljallangan witness tokenlarini yaratadi, har bir witness oxirgi marta qachon tekshirilganini ko'rsatadi va bittasini ([mustaqil witness](https://phishdestroy.github.io/TgWitness/uz/docs/reference/witness/)) ishga tushirish uchun buyruqlar hamda parametrlarni taqdim etadi.

**Parametrlar** ish maydonining boshqa sahifada ko'rsatilmagan barcha chegaralari va tezligini belgilaydi: qancha dialog o'qilgani, suhbatlar ro'yxati qanchalik tez-tez qayta o'qilishi, yurak urishi va tekshirish nuqtalari oralig'i, ishga tushirish buferi, qayta tekshirishlar so'rovlarini qanday tarqatishi (birinchi kechikish, suhbatlar per pass, suhbatlar orasidagi tanaffus, tiklangan va qayta so'ralgan xabarlar), disk rezervi, yuklab olishlarning vaqt chegaralari va qayta urinishlari, odamlar profillarida qidiriladigan narsalar (shu jumladan sizning o'zingizning odatiy ifodalaringiz), bildirishnomalarning hajmi va tezligi, snapshot, ZIP va brauzerdan yuklab olish limitlari, hamda Telegram klientining vaqt chegaralari va qayta urinishlari. Har bir maydon o'z diapazonini va standart qiymatini ko'rsatadi; o'zgartirilgan maydonlar belgilanadi va ularni bittadan yoki barchasini birgalikda tiklash mumkin. Har bir o'zgarish `parameters.changed` sifatida, oldingi va keyingi qiymatlar bilan qayd etiladi, va kuzatuv boshlanishi yozuvlari amalda bo'lgan qiymatlarni belgilaydi. Qiymatlar keyingi marta ishlatilganda kuchga kiradi; klient vaqt chegaralari va qayta urinishlar esa keyingi ulanishdan boshlab amal qiladi. Qayta tekshirish oraliklarini, ilova turlari va hajmlari, dalillar hamda tashqi nusxa olish oraliklarini o'z sahifalarida ko'rish mumkin bo'lib, ular faqat oldindan belgilangan qiymatlar bilan cheklanmay, o'z diapazonidagi istalgan qiymatni qabul qiladi.

Yuqori panelidagi qo'ng'iroq kuzatilgan suhbatlardagi so'nggi muammolar va o'zgarishlarni ko'rsatadi; o'qilmagan xabarlar o'qilgan deb belgilanmaguncha hisoblanadi. O'zgarishlar har bir suhbat va soat bo'yicha guruhlanadi ("12 tasi o'chirilgan, 1 tasi tahrirlangan, 0 tasi topilmagan"), va tizimdan chiqish yoki disk to'la kabi muammolar, suhbatlar qanchalik band bo'lmasin, ro'yxatda qoladi.

**Hisob** telefon raqami maydonidan boshlanadi. **Davom ettirish** to'g'ridan-to'g'ri kod kiritishga olib boradi, API ma'lumotlarini faqat ular yetishmayotganida so'raydi. QR va fayl importi alohida yorliqlar. Saqlangan API ma'lumotlari faqat o'z ish maydonida qayta ishlatiladi. Kirish ekrani yon panel, statistika yoki sozlash paragraflariga ega emas. **Sozlamalar** ikonkasi API, proksi, saqlash va qo'shimcha hisoblar boshqaruvini ochadi. Yangi o'rnatishlar shu yerdan boshlanadi; manba tanlanmagan ulangan hisoblar **"Suhbatlarni tanlash**" bo'limidan boshlanadi. Yo'nalishni o'zgartirish kuzatuvni to'xtatishni talab qiladi va yakunlanmagan tizimga kirishni bekor qiladi. Mavjud jurnalni sukut bo'yicha boshqa Telegram hisobiga bog'lash mumkin emas.

**Eksport** jurnalning yaxlitligini tekshiradi va ko'chma fayllarni yaratadi. Uning ish maydoni ID'si yuklab olish CLI'ga uzatilishi mumkin. Har bir eksport to'liq jurnal prefiksini belgilaydi; keyingi voqealar keyingi eksportga kiritiladi. Qidiruv filtrlari paket doirasini o'zgartirmaydi. Imzolash va qamrov bo'yicha batafsil ma'lumot **Tekshiruv va cheklovlar** bo'limida keltirilgan.

Panel Collector **holati** bo'limida yuklanish holatini, navbatga qo'yilgan/muvaffaqiyatsiz bo'lgan media fayllarni, eng qadimgi kutayotgan media faylni, bo'sh disk joyini, so'rov to'xtatishlarini va tasdiqlanmagan kirish huquqiga ega manbalarni ko'rsatadi. Ushbu ma'lumotlar dastlab siqilgan va Hisob sahifasida yashirilgan. Sozlash kartasi keyingi bosqichni ko'rsatadi: hisobni ulash, manbalarni tanlash yoki kuzatuvni boshlash. Hisoblar ro'yxati yuklanish vaqtidagi snapshot; tanlangan ish maydoni muntazam ravishda yangilanadi. Bu ko'p jarayonli SLA monitori emas.

Foydalanuvchi interfeysi manba kontenti uchun mahalliy resurslar va matnni renderlashdan foydalanadi. Stol usti va tor Chromium maketlari sinovdan o'tkazilgan. Bu to'liq kirish imkoniyati sertifikati emas; ekran o'qiydigan dastur va inson foydalanuvchiligi baholash alohida ish bo'lib qoladi.

## Joylashtirish muhitlari

| Muhit | O'rnatish | Verifikatsiya holati |
| --- | --- | --- |
| Windows PC/server | Python 3.11+, scripts\Setup.cmd/Start.cmd, shaxsiy ma'lumotlar katalogi | Windows/Python 3.12 da mahalliy tekshirildi |
| Linux server/VPS | Python virtual muhiti, maxsus xizmat foydalanuvchisi, HTTPS/SSH | Kod, CI va systemd misoli keltirilgan; ushbu hostda ijro etilmagan |
| macOS | Python virtual muhit (venv), old plandagi jarayon yoki foydalanuvchi agenti | launchd misoli keltirilgan; alohida o'rnatishni tekshirish zarur |
| Docker/Compose | Doimiy hajm, bitta ishchi | Ta'rif va CI ish vaqti tekshiruvi taqdim etilgan; Docker mahalliyda mavjud emas |
| Telefon brauzeri | Ishlayotgan serverdagi himoyalangan paneldan ulaning | Toraytirilgan Chromium maketi sinovdan o'tkazildi; to'plovchi iOS/Androidda ishlamaydi |

Ko'chma bo'lish – majburiy bulut xizmati yoki frontend qurilmasini talab qilmaslikni anglatadi. Har bir maqsad hanuz mos Python/kripto bog'liqliklarga, mahalliy disk va tarmoqqa kirish huquqiga ega bo'lishi kerak. Qarang: [DEPLOYMENT.md](https://phishdestroy.github.io/TgWitness/uz/docs/reference/deployment/) va [xizmat shablonlari](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md).

Ish maydonchalari CPU, xotira va voqealar tsiklini baham ko'radi. Jarayonlarni izolyatsiya qilish uchun alohida instantsiyalar, portlar, ma'lumotlar kataloglari va hisob ma'lumotlari ruxsatnomalaridan foydalaning. Alohida instantsiyalar bo'yicha yagona boshqaruv paneli mavjud emas. Bir nechta ishchi dasturini bitta ma'lumotlar bazasiga yo'naltirmang.

## Yozuvlarni tekshirish va eksport qilish

Tayyor muhitni ishga tushirishdan oldin `python start.py --check` ni ishga tushiring. Mashina o'qiy oladigan tekshiruvlar uchun `--json` ni qo'shing yoki mo'ljallangan `--data-dir`, `--host` va `--port` ni o'tkazing. Komanda Telegramga kirish yoki jurnal yaratishni talab qilmay, oldindan bajarilishi kerak bo'lgan shartlarni tekshiradi. U jurnalni tasdiqlamaydi yoki ma'lumotlarni ushlashga tayyorligini isbotlamaydi; jurnalni tasdiqlash dastur ishga tushirilganda bajariladi. Band port oddiygina mavjud instantsiya bo'lishi mumkin.

File System Access API-ni qo'llab-quvvatlaydigan brauzerlar eksportlarni yozib bo'ladigan oqim orqali saqlaydi. Boshqa brauzerlar esa buferga ko'pi bilan 128 MiB ma'lumotni joylaydi. Katta hajmdagi eksportlar yoki fayl oqimini qo'llab-quvvatlamaydigan brauzerlar uchun streaming CLI-dan foydalaning:

```
python -m tgwitness.download --token-file data/live/panel-token.txt --out evidence.zip
```

Bolalik ish maydoni uchun Exports bo'limidan `--profile ID` ni qo'shing. Masofaviy kirish uchun `--url https://server` ni ishlating. Oddiy HTTP faqat loopback manzillari uchun qabul qilinadi. Token fayldan o'qilib, sarlavhada yuboriladi, chop etilmaydi yoki URLga kiritilmaydi. Yo'naltirishlar rad etiladi. Mavjud manzillar ustiga yozilmaydi. Muvaffaqiyatsiz transferlar o'zlarining vaqtinchalik qism faylini o'chirib tashlaydi. Xabar qilingan SHA-256 transfer tekshiruv yig'indisi hisoblanadi; imzolangan ZIP-ni alohida ishonchli barmoq izi/nazorat nuqtasi yordamida tekshiring.

## Zaxira, tiklash va uzilishlar

1. Kuzatuvni to'xtating va jarayonni toza to'xtating.
2. Butun ma'lumotlar katalogini nusxalash: ma'lumotlar bazalari, mavjud bo'lsa WAL/SHM, media, `credentials.enc`, `signing.enc`, `network.enc`, xazina kalitlari/metamalg'olari, token, nazorat nuqtalari va har bir `profiles/` katalogi.
3. Tashqi kalit rejimida bosh kalitni alohida saqlang va har bir `vault.external.json`ni saqlab qo'ying. Yangi kalit yaratish eski sirlarni tiklashga imkon bermaydi.
4. Maqsad to'xtatilgan paytda tiklang; asl kalitni sozlang, kirishni cheklang va davom ettirishdan oldin yaxlitlikni tekshiring.
5. To'xtash vaqtini va tasdiqlash natijalarini qayd eting. Tarixning snapshoti uzilish davomida hech qanday o'chirish bo'lmagani haqida dalil bo'la olmaydi.

Dalil ZIP-fayllari sessiyalar/maxfiy kalitlarni o'z ichiga olmaydi va to'liq xizmat zaxira nusxalari emas. To'rt narsa boshqacha tarzda himoyalanadi:

| Nima | Himoya |
| --- | --- |
| Parolsiz (defolt) fayllarni eksport qiling | Shifrlanmagan. Imzolangan, shuning uchun o'zgartirishlar aniqlanadi, lekin faylni saqlaydigan har kim uni o'qishi mumkin. |
| Parol bilan fayllarni eksport qiling | Agar parol o'rnatilsa, tayyor eksport o'zgarmas holda 7-Zip va WinRAR ochadigan WinZip AES-256 ZIP arxiviga joylanadi; parol saqlanmaydi ([dalillar bilan ishlash](https://phishdestroy.github.io/TgWitness/uz/docs/reference/evidence/)) |
| Jurnal ma'lumotlar bazasi va diskka saqlangan ilovalar | TgWitness tomonidan shifrlanmagan; shifrlangan disk yoki hajmdan foydalaning |
| Telegram sessiyalari va imzolash kalitlari | Ma'lumotlar katalogida shifrlangan (`credentials.enc`, `signing.enc`, `network.enc`) |

To'liq xizmat zaxira nusxasi — bu yuqorida tasvirlangan to'xtatilgan ma'lumotlar katalogi bo'lib, eksport emas. Har ikkala holat uchun himoyalangan saqlash joyidan va aniq o'tkazish mexanizmidan foydalaning. Vaqtinchalik server eksportlari har bir ish maydonining `temporary-exports/` katalogida saqlanadi; yakunlangan javoblar tozalanadi, va uzilgan eksport fayllari keyingi ishga tushirishda, o'sha ish maydoni instantsiya qulfi ushlab turilgan paytda o'chiriladi.

Ulanish tiklangan voqea oraliq o'zgarishlarning tiklanishini kafolatlamaydi. Doimiy media ishlar va Telegram yangilanish pozitsiyasi qayta ishga tushirishdan keyin saqlanib qoladi; [dalil formatiga](https://phishdestroy.github.io/TgWitness/uz/docs/reference/evidence/#durable-collection-and-process-receipts-02) qarang.

## Quvvat va saqlash muddati

Standart cheklovlar, barchasi **Parametrlar** bo'limida o'zgartirilishi mumkin: birinchi 1 000 dialog, har bir snapshot uchun 500 xabar, siqilmagan imzolangan ZIP kontenti uchun 4 GiB (katta arxivlar uchun `verify.py --max-gib N` kerak) va brauzer uchun 128 MiB zaxira. Ilovalar **Manbalar → Ilovalar** bo'limida har bir tur uchun 1–2 000 MiB joy egallaydi. Yuklab olish CLI bo'yicha 5 GiB o'tkaziladi. Mavjud disk hajmi pastroq limit bo'lishi mumkin. Jurnal, media, WAL, vaqtinchalik eksportlar va zaxira nusxalar uchun joy ajrating. Eksportlar Compose'ning 512 MiB hajmli `/tmp` o'rniga ma'lumot hajmidan foydalanadi.

Faqat guruhlarni sanash o'rniga sekuntiga sodir bo'ladigan voqealar soni, navbatning yoshi, media baytlari va disk kechikishini o'lchang. Sintetik mahalliy benchmarklar Telegram xabarlarining yetkazilishini kafolatlamaydi. Avtomatik saqlash va o'chirish mavjud emas. Jurnal oxirini o'chirish uning saqlangan tekshirish nuqtalari bilan bog'liqligini bekor qiladi.

Ustuvor qayta tekshirishlar allaqachon mavjud: yulduzchali manbalar standart bo'yicha har 15 daqiqada, boshqalar esa har 6 soatda qayta tekshiriladi ([qayta tekshirish bosqichlariga](https://phishdestroy.github.io/TgWitness/uz/docs/reference/collection/#recheck-tiers) qarang). Parol bilan himoyalangan eksportlar yuqorida ta'riflanganidek mavjud. Telegram/proxy jonli qabul qilish, bardoshli qayta ijro etish, admin-log va reaksiya so'rovnomalari, izolyatsiyalangan ishchilar, mahalliy jurnal va media shifrlashi hamda mustaqil ko'rib chiqish alohida ish bo'lib qoladi. Cheklangan kirish huquqi [access va permissions](https://phishdestroy.github.io/TgWitness/uz/docs/reference/access/) hujjatlarida bayon etilgan. [READINESS.md](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/READINESS.md), [LIVE_ACCEPTANCE.md](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md) va [VERIFICATION.md](https://phishdestroy.github.io/TgWitness/uz/docs/reference/verification/) hujjatlariga qarang.
