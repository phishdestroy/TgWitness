# Tez boshlash

Canonical page: https://phishdestroy.github.io/TgWitness/uz/docs/reference/quickstart/

TgWitness-ni o'rnatish va ishga tushirishning barcha usullari: Windows paketi, Python, Docker va sintetik demo, dastlabki tekshiruvlar bilan.

**Inglizcha** · [Rus tili](https://github.com/phishdestroy/TgWitness/blob/main/docs/ru/QUICKSTART.md) · [Ukrain tili](https://github.com/phishdestroy/TgWitness/blob/main/docs/uk/QUICKSTART.md) · [Ispancha](https://github.com/phishdestroy/TgWitness/blob/main/docs/es/QUICKSTART.md) · [Portugalscha (Braziliya)](https://github.com/phishdestroy/TgWitness/blob/main/docs/pt/QUICKSTART.md) · [Turkcha](https://github.com/phishdestroy/TgWitness/blob/main/docs/tr/QUICKSTART.md) · [Arab tili](https://github.com/phishdestroy/TgWitness/blob/main/docs/ar/QUICKSTART.md) · [Farsi](https://github.com/phishdestroy/TgWitness/blob/main/docs/fa/QUICKSTART.md) · [O'rdu](https://github.com/phishdestroy/TgWitness/blob/main/docs/ur/QUICKSTART.md) · [hindicha](https://github.com/phishdestroy/TgWitness/blob/main/docs/hi/QUICKSTART.md) · [Indoneziya tili](https://github.com/phishdestroy/TgWitness/blob/main/docs/id/QUICKSTART.md) · [Vyetnam tili](https://github.com/phishdestroy/TgWitness/blob/main/docs/vi/QUICKSTART.md) · [Xoʻllashma xitoycha](https://github.com/phishdestroy/TgWitness/blob/main/docs/zh/QUICKSTART.md)

TgWitness – bu mustaqil dastur bo'lib, u sizning hisoblaringiz kira oladigan Telegram guruhlari va kanallarini kuzatadi. U mahalliy tarzda, o'z ma'lumotlar katalogi bilan ishlaydi.

**Birinchi marta tashrif buyurayapsizmi?** Hisobni ulashdan oldin [demo bilan tanishing](https://phishdestroy.github.io/TgWitness/uz/docs/reference/quickstart/#explore-the-interface). Proxylar, guvohlar, eksportlar yoki server sozlamalari bo'yicha [qo'llanma tanlang](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md).

## O'rnatish va ishga tushirish

[GitHub Actions orqali yig‘ish (dastlabki versiya)](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md)

Bir usulni tanlang. Portativ yuklamalar chiqarilgan versiya e'lon qilingach mavjud bo'ladi:

| Mehmondo'st | Hech narsa o'rnatilmagan | Manba: Python 3.11+ | Docker: Engine/Desktop, Compose 2.20+ bilan |
| --- | --- | --- | --- |
| Windows | `TgWitness-<version>-windows-amd64-portable.zip`ni GitHub Releases'dan yuklab oling, `TgWitness.cmd` ustiga ikki marta bosing | `Start.cmd` ustiga ikki marta bosing | `scripts\Docker.cmd` ustiga ikki marta bosing |
| Linux / macOS | — | `sh start.sh` | `sh scripts/docker-start.sh` |

Manba kod usullari uchun GitHub Releases'dan manba ZIP faylini yuklab oling va arxivdan chiqarib oling yoki omborni klonlang. Agar mos Python topilmasa (winget yoki imzolangan python.org o'rnatuvchisi), `Start.cmd` Windows foydalanuvchingiz uchun Python 3.12 o'rnatishni taklif etadi. `start.sh` Python yo'q bo'lsa, Linux distributivi yoki macOS uchun aniq o'rnatish buyrug'ini chiqaradi. Birinchi manba ishga tushirilganda `.venv` yaratiladi va bog'liqliklar avtomatik o'rnatiladi.

Docker ilovani kompilyatsiya qilib, uni fon rejimida ishga tushiradi; host Python keraksiz. `scripts\Docker.cmd` va `scripts/docker-start.sh` konteyner sog'lom holatda bo'lganda panel manzili va tokenni chop etadi. Har bir qo'llab-quvvatlanadigan hostdagi ekvivalent Docker buyruqlari quyidagilardan iborat:

```
docker compose up -d --build --wait
docker compose exec tgwitness cat /data/panel-token.txt
```

http://127.0.0.1:8787 saytini oching. Docker yordamchisi yoki ikkinchi Docker buyrug'i tomonidan chop etilgan tokenni ishlating yoki portativ yoki manba o'rnatilmasida **data/live/panel-token.txt faylini** o'qing. Qolgan qismni quyidagi "**Telegramga ulanish**" bo'limida davom ettiring. Native va Docker o'rnatmalari alohida saqlashdan foydalanadi; Docker-ni ishga tushirish mavjud native jurnalni import qilmaydi.

Server uchun [joylashtirish](https://phishdestroy.github.io/TgWitness/uz/docs/reference/deployment/) avtomatik HTTPS, qayta ishga tushirish, e'lon qilingan tasvirlar, yangilanishlar va zaxira nusxalarini o'z ichiga oladi.

## Interfeysni o'rganing

1. Portativ paketdagi **TgWitness-Demo.cmd** , Windows manba papkasidagi **scripts\Demo.cmd** yoki Linux/macOS'da `sh start.sh --demo` ni ishga tushiring. Manba kodni ishga tushirish avvalo `.venv` ni yaratadi va zarur kutubxonalarni o'rnatadi.
2. **http://127.0.0.1:8787 saytini** oching.
3. Mahalliy demo namunaviy jurnalni avtomatik ochadi. To'g'ridan-to'g'ri mahalliy kirish uchun token nusxasini ko'chirish shart emas.

Demo xabarlari badiiydir. Demo rejimi haqiqiy Telegram hisobiga ulanmaydi.

## Telegramga ulanish

> [!OGOHLANTIRISH] **Yo'qotishga qodir bo'lmagan narsalardan foydalanmang.** Shaxsiy yoki qimmatli hisoblarni ulashni va qadrlaydigan hisobingizda API ID / xesh yaratishni qat'iyan tavsiya qilmaymiz. Telegram mijozdan qat'i nazar, hisoblarni oldindan aytib bo'lmaydigan va ko'pincha doimiy ravishda taqiqlaydi. Sinovning muammosiz o'tishi Telegramga bog'liq, TgWitnessga emas, va keyingi holatlar uchun hech qanday kafolat bermaydi.

1. Agar mahalliy demo ishlamoqda bo'lsa, uni to'xtating va **Start.cmd** yoki `sh start.sh` faylini ishga tushiring. Aks holda, yuqorida jonli o'rnatishni ishga tushirgan holda qoldiring.
2. Paneldan foydalanish usulingiz uchun tokenni ishlatib panelni oching.
3. Agar proksi kerak bo'lsa, uni **Hisob → Sozlamalar → Ulanish sozlamalari → Ulanish yo'nalishini o'zgartirish** bo'limida saqlang.
4. **Hisob** bo'limida telefon raqamingizni kiriting va **Davom etish tugmasini** bosing, **QR kod → QR kodni ko'rsatishni** tanlang yoki fayllarni tanlab **Hisobni bog'lash**tugmasini bosing. **API ID + Hash** ixtiyoriy: ish maydoni saqlangan yoki import qilingan juftlikni, yoki o'rnatilgan bazadagi ishlaydigan juftlikni ishlatadi. O'zingizning ilovangizdan foydalanish uchun bitta `API ID:API Hash` juftligini API ID ga joylashtiring. To'liq avtorizatsiya kaliti uchun **Auth kalitini** tanlang, barcha 512 geksadesimal belgini joylashtiring va taqdim etilgan DC ID ni tanlang. Foydalanuvchi ID ixtiyoriy bo'lib, kiritilganda tekshiriladi.
5. Tanlangan kirish usulingizni yakunlang: telefon/kod/2FA, QR uchun kirishga kirgan Telegram ilovasidan tasdiq yoki qo'llab-quvvatlanadigan ruxsat berilgan sessiyani import qilish.
6. Ko'rsatilgan hisob IDni tekshiring. Ochiq **manbalar**: suhbatlaringiz avtomatik yuklanadi; guruhlaringizni qo'shing.
7. **Qaysi o'zgarishlarni saqlashni tanlash** bo'limida voqea toifalarini yoki " **Xabarlar, tahrirlar va o'chirishlar**" oldindan belgilangan sozlamasini tanlang, so'ngra monitoring sozlamalarini saqlang.
8. Ilovalar sozlamalarini alohida tanlang, so'ngra **Kuzatuvni boshlash** tugmasini bosing.

API ma'lumotlari sizning ilovangizni aniqlaydi; ular o'zlari hech qanday hisobni ruxsat etmaydi. Xususiy guruhlarga ommaviy foydalanuvchi nomi kerak emas, lekin sizning hisobingizda kirish huquqi bo'lishi kerak.

Mavjud hisoblar uchun [hisoblar va sessiya formatlariga](https://phishdestroy.github.io/TgWitness/uz/docs/reference/accounts/) qarang: panel Telethon StringSession, Telethon/Pyrogram SQLite, yagona hisobli TData ZIP va qo'llab-quvvatlanadigan hisob JSON formatlarini qabul qiladi. Sessiyani va uning hamroh JSON faylini birgalikda tanlang, **"Hisobni ulash"** tugmasini bosing. QR orqali kirish ham xuddi shu ixtiyoriy API sozlamalari bilan mavjud. TDLib, botlar va ommaviy hisob ro'yxatlari qo'llab-quvvatlanmaydi.

Yana bir akkaunt qo'shish uchun akkaunt tanlovchisining yonidagi **+** tugmasini bosing yoki **Akkaunt → Sozlamalar → Ulanish sozlamalari → Ish maydonchalari bo'limini** oching, yoki **Akkauntlar bo'lim**idan foydalaning. Ish maydonchalari alohida sessiyalarga, jurnalarga, kalitlarga, manbalarga va navbatlarga ega. Ko'rinishlarni almashtirish boshqa yig'uvchilarni ishlashda davom ettiradi. Ushbu o'rnatishda bir xil Telegram akkaunti ikki ish maydonchasiga tayinlanishi mumkin emas. Ish maydonlarining doimiy soni yo'q; ular bitta jarayonni baham ko'radi, shuning uchun sig'im mashinaga bog'liq.

Jonli panel tokeni Telegram ruxsatnomalaringiz va saqlangan materiallarga kirishni himoya qiladi; u Telegram API ma'lumotlaridan alohida. Faqat aniq boshlangan va to'g'ridan-to'g'ri ulanilgan mahalliy demo avtomatik kirish huquqiga ega. Masofaviy/proxy orqali ulanadigan demo hanuzgacha `data/demo/panel-token.txt` ni ishlatadi.

## Ko'rib chiqish va eksport qilish

- **Jurnal:** kuzatuvlarni manba va hodisa turiga ko'ra qidirish va filtrlash.
- Voqeani tanlang va uning asl yozuvini, atributsiyasini hamda saqlangan versiyalarini ko'rib chiqing.
- Tahrirlash tafsilotlari mavjud bo'lgan oldingi/keyingi kontentni ko'rsatadi. O'chirish tafsilotlari mavjud bo'lsa, oxirgi qayd etilgan kontentni ko'rsatadi; noma'lum aktor noma'lum bo'lib qoladi.
- **Eksportlar:** imzolangan ZIP, JSONL, CSV va oflayn HTML.
- **To'liq suhbat eksporti** (Manbalar → To'liq suhbat eksporti): bitta suhbatning butun ko'rinadigan tarixini imzolangan paket sifatida `chat.json` bilan (Telegram-eksport uslubida) va o'qiladigan `chat.html` bilan yuklab oling. Xususiy suhbatlar hisob suhbat a'zosi bo'lganida ishlaydi. Bu hozirgi snapshot bo'lib, o'chirilgan yoki ilgari tahrirlangan xabarlarning rekonstruksiyasi emas. `python verify.py chat-export.zip --fingerprint TRUSTED_SHA256` yordamida nusxani tasdiqlang.
- **Save checkpoint:** imzolangan jurnal chegarasini to'plovchidan tashqarida saqlang.
- **Imzolangan ishga tushirish kvitansiyasini yuklab oling:** to'plovchining dastur/versiya yozuvini saqlang.
- **Vaqt tamg'asi so'rovini tayyorlang:** vaqt tamg'asi vakolat organi uchun oflayn so'rov tayyorlang; Javobni olish va tekshirish uchun [TIMESTAMP.md hujjatiga](https://phishdestroy.github.io/TgWitness/uz/docs/reference/timestamp/) amal qiling.
- **Jurnalni tekshirish:** voqea imzolarini va zanjir bog'lanmalarini tekshirish. ZIP eksporti media fayllarni ham tekshiradi.

Qo'llab-quvvatlanadigan brauzerlar katta eksportlarni to'g'ridan-to'g'ri tanlangan faylga saqlaydi. Boshqa brauzerlar eng ko'pi bilan 128 MiB buferlaydi. Server ishlayotgan paytda, oqimli CLI butun javobni buferlamasdan kattaroq yuklab olishlarni qo'llab-quvvatlaydi:

```
python -m tgwitness.download --token-file data/live/panel-token.txt --out evidence.zip
```

Boshqa ish maydoni uchun **Exports → Workspace ID** orqali `--profile ID` ni qo'shing. Masofaviy server uchun `--url https://your-server` ni qo'shing. Standart uzatish limiti 5 GiB; `--max-mib` uni o'zgartiradi. Imzolangan ZIP kontentining standart bo'yicha alohida 4 GiB siqilmagan tekshirish limiti mavjud (**Parameters** uni oshiradi; bunday arxivlarni `verify.py --max-gib N` yordamida tekshiring). Arxivni ishonchli tekshiruvchi nusxasi va mustaqil saqlangan kalit izi/nazorat nuqtasi yordamida tekshiring.

## O'rnatishni tekshiring

```
python start.py --setup-only
python start.py --check
python start.py --check --json
```

`--check` mahalliy bog'liqliklarni, imzolashni qo'llab-quvvatlashni, saqlash joyini, kalit sozlamalarini va tinglash manzilini tekshiradi. U hech narsa o'rnatmaydi va Telegramga ulanmaydi. Band port boshqa bir nusxa ishlamoqda degani bo'lishi mumkin. Boshqa `--port` dan foydalaning yoki avval uni to'xtating.

Ishga tushiruvchi dastur `.venv` ga o'rnatiladi. Yordamchi `python -m tgwitness...` buyruqlari Windowsda `.venv\Scripts\python.exe`, Linux/macOSda esa `.venv/bin/python` ni ishlatishi kerak, agar bu muhit allaqachon faollashtirilmagan bo'lsa.

## Sessiyalar, himoya va ishlash

Yopiq, izchil Telethon SQLite `.session` faylini mahalliy tarzda `python -m tgwitness.sessions account.session --out account.tgwitness-session` bilan konvertatsiya qilish va keyin Hisobga yuklash mumkin. To'g'ridan-to'g'ri fayl importi va QR orqali kirish ham mavjud. Kirish formatlari, SOCKS5, HTTP CONNECT, MTProxy va tashqi bosh kalitlar uchun [CONNECTION-SECURITY.md hujjatiga](https://phishdestroy.github.io/TgWitness/uz/docs/reference/connection/) qarang.

**To'xtatish kuzatuvni** to'xtatadi. **Quqitish** faqat brauzer orqali kirishni yopadi. Vozkani yopish yig'ish jarayonini ishga tushgan holda qoldiradi. Jarayonni to'xtatish yig'ishni uzib qo'yadi; tarixning snapshoti barcha o'tkazib yuborilgan tahrirlar yoki o'chirishlarni qayta tiklay olmaydi. Voqea siyosatlari, ilova navbatlari, hisobni izolyatsiya qilish va qayta ishga tushirish xatti-harakatlari bo'yicha [yig'ish qanday ishlashini](https://phishdestroy.github.io/TgWitness/uz/docs/reference/collection/) ko'ring.

Sessiyalar va sirlar shifrlanadi. Xabarlar mazmuni, media va eksportlar shifrlangan disk yoki hajmni talab qiladi. Imzolar ishonchli kalitga nisbatan yaxlitlikni ta'minlaydi; ular Telegram kelib chiqishini aniqlamaydi yoki yig'uvchi va uning kalitini nazorat qiluvchi operator tomonidan soxtalashtirishni oldini olmaydi.

Zaxira nusxa olish va tiklash uchun [OPERATIONS.md](https://phishdestroy.github.io/TgWitness/uz/docs/reference/operations/), hosting uchun [DEPLOYMENT.md](https://phishdestroy.github.io/TgWitness/uz/docs/reference/deployment/) hamda xizmat misollari uchun [deploy/](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md) fayllarini o'qing. O'rnatilgan panelda shuningdek `/guide.html` manzilida oflayn sozlash bo'yicha qo'llanma mavjud.

Haqiqiy tasdiqlash va qolgan cheklovlar [VERIFICATION.md](https://phishdestroy.github.io/TgWitness/uz/docs/reference/verification/) hamda [READINESS.md](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/READINESS.md) fayllarida qayd etilgan.
