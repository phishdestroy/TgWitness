# Joriy etish

Canonical page: https://phishdestroy.github.io/TgWitness/uz/docs/reference/deployment/

TgWitness-ni Windows, Linux, macOS yoki Docker-da xizmat sifatida, HTTPS orqali, zaxira nusxalari va yangilanishlari bilan ishga tushiring.

**Inglizcha** · [Rus tili](https://github.com/phishdestroy/TgWitness/blob/main/docs/ru/DEPLOYMENT.md) · [Ukrain tili](https://github.com/phishdestroy/TgWitness/blob/main/docs/uk/DEPLOYMENT.md) · [Ispancha](https://github.com/phishdestroy/TgWitness/blob/main/docs/es/DEPLOYMENT.md) · [Portugalscha (Braziliya)](https://github.com/phishdestroy/TgWitness/blob/main/docs/pt/DEPLOYMENT.md) · [Turkcha](https://github.com/phishdestroy/TgWitness/blob/main/docs/tr/DEPLOYMENT.md) · [Arab tili](https://github.com/phishdestroy/TgWitness/blob/main/docs/ar/DEPLOYMENT.md) · [Farsi](https://github.com/phishdestroy/TgWitness/blob/main/docs/fa/DEPLOYMENT.md) · [O'rdu](https://github.com/phishdestroy/TgWitness/blob/main/docs/ur/DEPLOYMENT.md) · [hindicha](https://github.com/phishdestroy/TgWitness/blob/main/docs/hi/DEPLOYMENT.md) · [Indoneziya tili](https://github.com/phishdestroy/TgWitness/blob/main/docs/id/DEPLOYMENT.md) · [Vyetnam tili](https://github.com/phishdestroy/TgWitness/blob/main/docs/vi/DEPLOYMENT.md) · [Xoʻllashma xitoycha](https://github.com/phishdestroy/TgWitness/blob/main/docs/zh/DEPLOYMENT.md)

## O'rnatishni tanlang

Portativ paket uchun GitHub Releases'dan `TgWitness-<version>-windows-amd64-portable.zip`-ni chiqarib oling. Boshqa usullar uchun manba ZIP-faylni yuklab olib oching yoki omborni klonlang, so'ng loyiha katalogidan quyidagi buyruqni ijro eting:

| O'rnatish | Boshlash | Orqa fonda ishlaydimi? |
| --- | --- | --- |
| Windows uchun portativ paket | `TgWitness.cmd` | Yo'q; oynani ochiq holda saqlang. |
| Windows uchun mahalliy | `Start.cmd` | Yo'q; fon rejimida ishlatish uchun ixtiyoriy logon vazifasidan foydalaning. |
| Linux/macOS uchun mahalliy | `sh start.sh` | Yo'q; fon rejimida ishlatish uchun systemd/launchd dan foydalaning. |
| Har qanday qo'llab-quvvatlanadigan mezbon kompyuterda Docker | `docker compose up -d --build --wait` | Ha, Docker daemon ishlayotgan paytda. |
| Windows uchun Docker yordamchisi | `scripts\Docker.cmd` | Ha; yordamchi veb-server sog'lig'ini kutadi. |
| Linux/macOS uchun Docker yordamchisi | `sh scripts/docker-start.sh` | Ha; yordamchi veb-server sog'lig'ini kutadi. |

Uchinchi tomon tekshira oladigan bulutli server uchun — provayder API orqali yaratilgan, SSHsiz, faqat Cloudflare Tunnel orqali erishiladigan — [yuqori ishonchlilikka ega joylashtirishni](https://github.com/phishdestroy/TgWitness/blob/main/docs/HIGH-ASSURANCE.md) ko'ring.

Native startup maxfiy `.venv`ni yaratadi va bog'langan bog'liqliklarni o'rnatadi. Docker ularni host Pythonni talab qilmay, image ichida quradi. Birinchi marta o'rnatish uchun Internetga ulanish zarur. Python 3.11+ topilmasa, `Start.cmd` hozirgi Windows foydalanuvchisi uchun Python 3.12 ni o'rnatishdan oldin so'raydi (winget orqali, aks holda Python Software Foundation imzosi tekshirilgach python.org installyeridan); u hech qachon administrator huquqlarini so'ramaydi. Docker va OS xizmatlari oldindan talab qilinadi.

Mahalliy va ko'chma o'rnatishlar papkalarida `data/live` dan foydalanadi. Docker `tgwitness-data` nomli hajmni `/data` da ishlatadi. To'liq ma'lumotlar katalogini ataylab ko'chirib o'tmaguningizcha, ular alohida o'rnatishlar hisoblanadi. Yangi Docker konteyneri mahalliy hisoblarni avtomatik ravishda aniqlaydi deb kutmang.

## O'rnatish talablari

Mahalliy o'rnatish uchun Python 3.11 yoki undan keyingi versiya, `venv` va `ensurepip`, birinchi bog'liqlikni o'rnatish uchun Internetga ulanish hamda `.venv` uchun yozish huquqiga ega loyiha papkasi kerak. Ilovaga kiritilgan panel uchun Node.js yoki frontend qurilmasi talab qilinmaydi. Launcher-ni odatdagi operatsion tizim akkauntingizdan ishga tushiring; TgWitness uchun administrator/root huquqlari zarur emas.

- **Windows:** `Start.cmd` avval `py -3`, keyin `python`, so'ngra foydalanuvchi uchun belgilangan va Program Files o'rnatish papkalarini tekshiradi va 3.11-versiya yoki undan keyingi versiyani talab qiladi. Agar hech biri ishlamasa, u yuqorida tasvirlangan avtomatik foydalanuvchi o'rnatilishini taklif etadi. `py -3 start.py` ham ishlaydi. Portativ paketga umuman Python kerak emas.
- **Linux:** `start.sh` `python3.13`, `python3.12`, `python3.11`, `python3` va `python` ni sinab ko'radi va mos keladigan dastur topilmaganda apt, dnf, pacman, zypper, apk yoki Homebrew uchun o'rnatish buyrug'ini chiqaradi. Debian/Ubuntu tizimlarida tanlangan interpretatorga mos `python3-venv` paketini o'rnatish talab qilinishi mumkin. Tarqatishning eski asosiy Python'i Python 3.11+ bilan almashtirilishi yoki to'ldirilishi kerak.
- **macOS:** joriy Python 3.11+ tarqatmasini o'rnating; operatsion tizim taqdim etgan interpretator talabga javob beradi deb hisoblamang. Loyiha katalogidan `python3 start.py`-dan foydalaning.
- **Docker:** Docker Engine/Desktop-ni Compose v2.20 yoki undan yangiroq versiyasi bilan ishlating. Docker Desktop Windowsda Linux konteynerlaridan foydalanishi kerak. Konteyner o'zining Python bog'liqliklarini o'rnatadi; hostda alohida Python o'rnatilishiga ehtiyoj yo'q.

Ma'lumotlar katalogi uchun doimiy mahalliy saqlashdan foydalaning. Xabarlar, media, WAL o'sishi, eksport va zaxira nusxalari asosida sig'imni rejalashtiring; har bir ish yukiga mo'ljallangan universal minimal disk/RAM spetsifikatsiyasi mavjud emas. CPU arxitekturalari va Python versiyalari mos keladigan qaramlik gildiraksiz bo'lsa, qo'shimcha kompilyatsiya vositalari va ularning alohida malaka sinovlarini talab qilishi mumkin. "Portativ" universal operatsion tizim yoki apparat qo'llab-quvvatlanishini anglatmaydi.

Windows 11/Python 3.12 mahalliy tarzda tasdiqlangan. Linux/macOS/konteyner ta'riflari va CI taqdim etilgan, ammo ushbu rivojlantirish muhitida ishga tushirilmagan. Aniq doirani ko'rish uchun [VERIFICATION.md](https://phishdestroy.github.io/TgWitness/uz/docs/reference/verification/) hujjatiga murojaat qiling.

## Mahalliy kompyuter

Windowsda `Start.cmd`, Linux/macOSda esa `sh start.sh` dan foydalaning. `scripts\Setup.cmd` yoki `sh start.sh --setup-only` muhitni tayyorlaydi. Launcher birinchi marta ishlatilganda zarur kutubxonalarni o'rnatadi; keyingi ishga tushirishlarda muhit qayta ishlatiladi. Sozlash va Telegram xabarlarini yig'ish uchun internetga ulanish talab etiladi, ammo mavjud yozuvlarni ko'rib chiqish va eksport yaratish oflayn rejimda amalga oshiriladi.

`python start.py --check`-ni sozlamalardan so'ng ishga tushiring, kollektorni ishga tushirmay turib mahalliy bog'liqliklarni, Ed25519, saqlash joyini, kalit konfiguratsiyasini va tinglash manzilini tekshirish uchun. Tuzilgan chiqish uchun `--json` dan foydalaning. Mo'ljallangan `--data-dir`, `--host` va `--port` ni uzating. Tekshiruv paketlarni o'rnatmaydi, jurnal yaratmaydi yoki Telegramga ulanmaydi; bu yaxlitlik yoki qamrov kvalifikatsiyasi emas. Startup alohida mavjud jurnallarni tekshiradi. `python start.py --help` ham o'rnatishni oldini oladi.

Imkoniyatlar:

start.py-dan foydalangandan so'ng, Windowsda `.venv\Scripts\python.exe`, Linux/macOSda esa `.venv/bin/python` yordamchi buyruqlarini ishga tushiring yoki avval shu muhitni yoqing. Quyidagi `python -m ...` misollari muhit faol deb hisoblaydi.

```
python -m tgwitness --data-dir /path/to/private/data --host 127.0.0.1 --port 8787
```

Atrof-muhit o'zgaruvchilari: TGWITNESS_DATA, TGWITNESS_HOST, TGWITNESS_PORT, TGWITNESS_TOKEN. TGWITNESS_VAULT_KEY_FILE yangi o'rnatish uchun tashqi kalit rejimini tanlaydi; quyida ko'ring. TGWITNESS_TOKEN, agar ko'rsatilsa, kamida 24 belgidan iborat bo'lishi kerak; kriptografik jihatdan tasodifiy qiymatdan foydalaning. U bo'lmasa, ilova panel-token.txt faylida 256 bitli tasodifiy token yaratadi. Atrof-muhit sozlamalari ustunligi ushbu faylni qayta yozmaydi. Kirish ma'lumotlarini aylantirish uchun ilovani qayta ishga tushiring.

Aynan bitta jarayon ma'lumotlar katalogiga egalik qilishi mumkin. Platformalararo operatsion tizim fayl qulfi tasodifiy bir vaqtda yozuv qilishni oldini oladi. Bitta Uvicorn ishchisini ishlating. Panel istalgan sonli ish maydonlarini boshqarishi mumkin, qo'shimcha ish maydoni kataloglari profiles/<id>/ ostida joylashadi. Alohida xizmat instantsiyalari uchun alohida kataloglar va portlardan foydalaning. SQLite WAL fayllari tarmoq fayl tizimida emas, balki mahalliy doimiy saqlash joyida bo'lishi kerak. Bir xajmni nusxa ko'chirishlar (replika) o'rtasida ulashingiz mumkin emas.

## Windows uchun portativ paket

Har bir GitHub Release `TgWitness-<version>-windows-amd64-portable.zip` va uning `.sha256` versiyalarini o'z ichiga oladi. U python.org saytidan olingan rasmiy embeddable Python 3.12 ijro muhitini (checksum `tools/build_portable.py` da qayd etilgan), TgWitness va uning qayd etilgan bog'liqliklarini, shuningdek uchta ishga tushiruvchini o'z ichiga oladi:

| Hujjat | Maqsad |
| --- | --- |
| `TgWitness.cmd` | Panelni ishga tushiring; qo'shimcha parametrlar uzatiladi, masalan`TgWitness.cmd --port 8790` |
| `TgWitness-Demo.cmd` | `data\demo`da sintetik demo-ni ishga tushiring |
| `TgWitness-Check.cmd` | Boshlashni boshlamadan tayyorgarlik tekshiruvini ishga tushiring |

Butun arxivni yozish mumkin bo'lgan papkaga, masalan `Documents\TgWitness` ga chiqarib oling; uni ZIP ichida yoki Program Files katalogidan ishga tushirmang. Ijro vaqti alohida modul yo'lidan foydalanadi, shuning uchun boshqa Python o'rnatmalari va `PYTHONPATH` unga ta'sir qilmaydi. Ma'lumotlar paketning `data` papkasida saqlanadi. Yangilash uchun TgWitness-ni to'xtating, yangi versiyani yangi papkaga chiqarib oling va `data` papkasini nusxalab o'tkazing.

Uni 64-bit Windowsda Python 3.12 bilan o'zingiz quring:

```
python tools/build_portable.py
```

Quruvchi ijro vaqtidagi tekshiruv summasini tasdiqlaydi, cheklangan bog'liqliklarni paketga o'rnatadi, o'rnatilgan interpretator bilan tayyorgarlik tekshiruvini ishga tushiradi va ZIP hamda tekshiruv summasini`dist/` ga yozadi.

## Kontener

```
docker compose up -d --build --wait
```

Bu /data uchun nomlangan doimiy hajm yaratadi. Veb-port 127.0.0.1:8787 ga bog'lanadi. Jarayon UID 10001 sifatida, imtiyozlari cheklangan, faqat o'qish uchun mo'ljallangan root fayl tizimi va yozish mumkin bo'lgan /data hamda /tmp bilan ishlaydi. `--wait` javob qaytarishdan oldin veb-server holatini tekshiradi; u Telegram avtorizatsiyasi yoki yetkazib berishni o'rnatmaydi. Taqdim etilgan yordamchi dasturlar kompilyatsiyadan so'ng 180 soniyalik tayyorlik timeoutidan foydalanadi. Dastlabki bog'liqliklarni yuklab olish buni ham oshib ketishi mumkin.

Ikkala asosiy Compose fayllari ham `tgwitness` loyiha nomidan foydalanadi, shuning uchun yangi chiqarilishni boshqa katalogga chiqarish yangi ma'lumot hajmini jimjit tanlamaydi. Ushbu loyiha uchun faqat bitta joylashtirishni faol saqlang. Mustaqil o'rnatishlar uchun noyob `docker compose -p NAME ...` va boshqa host portidan foydalaning hamda yangilanishlarda ikkalasini ham saqlang. Boshqa loyiha nomidan foydalangan eski joylashtirish uchun uning asl nomini `-p` bilan ishlatishni davom ettiring; `docker compose ls` mavjud loyihalarni ro'yxatlaydi.

`deploy/env.example` ni `.env` ga nusxa ko'chiring va `TGWITNESS_PORT` ni boshqa loopback portidan foydalanish uchun o'zgartiring. Masalan, `TGWITNESS_PORT=8788` panelni `http://127.0.0.1:8788` da ochadi; konteyner esa hanuz 8787 portda tinglaydi. `.env` Git tomonidan e'tiborsiz qoldirilgan.

Boshlang'ich tokenni oling:

```
docker compose exec tgwitness cat /data/panel-token.txt
```

Foydali buyruqlar:

```
docker compose ps
docker compose logs --tail 100 -f
docker compose stop
docker compose up -d --wait
```

`restart: unless-stopped` qulash yoki Docker daemon qayta ishga tushgach kollektorni qayta ishga tushiradi. Linux serverida, odatda `sudo systemctl enable --now docker` bo'lgan distribyutivingizning xizmat menejeri orqali tizim yuklanganda Docker ni yoqishni yoqish. Windows/macOS da Docker Desktop ning tizimga kirishda avtomatik ishga tushirish sozlamasini yoqish. Kompyuterdan chiqish, uxlatish yoki to'xtatilgan Docker daemon yig'ishni to'xtatishi mumkin. Aniq to'xtatilgan konteyner uni qayta ishga tushirmaguningizcha to'xtagan holda qoladi.

Misol konfiguratsiyasida /tmp hajmi 512 MiB bilan cheklangan. Eksport qurilishi o'rniga har bir ish maydonining doimiy /data bo'limidagi `temporary-exports/`dan foydalanadi. Simultane eksportlar, jurnal/WAL o'sishi, media va zaxira nusxalar uchun u yerdagi joyni ajratib qo'ying. Ishga tushiruvchi deploy/constraints.txt faylidan foydalanib, malakali ijro muhitiga bog'liqlik versiyalarini mahkamlaydi. Docker va yuqori ishonchlilikka ega serverlar deploy/requirements.lock va deploy/build.lock fayllaridan pip --require-hashes yordamida o'rnatiladi: har bir paket fayli commitda qayd etilgan SHA-256 bilan mos kelishi kerak, shuning uchun PyPI yoki uning oynasida almashtirilgan fayl o'rnatilmaydi. Python asosiy tasviri va operatsion tizim paketlari hanuzgacha mustaqil chiqarish malakasini talab qiladi.

Jurnal va kalitlarni yo'q qilmoqchi bo'lmasangiz, docker compose down -v ni ishlatmang. Kontener sog'ligi hisobotlari Telegram xabarlarini muvaffaqiyatli qabul qilishni emas, veb-server mavjudligini ko'rsatadi. Panelning yig'uvchisining holatini, yurak urishini, xatolarini va qamrov voqealarini tekshiring.

### Mustaqil guvoh profili

Ixtiyoriy `witness` xizmati [mustaqil guvoh](https://phishdestroy.github.io/TgWitness/uz/docs/reference/witness/)ni o'z konteynerida, o'z kaliti va jurnaliga ega holda `witness-data` hajmida ishga tushiradi va yig'uvchi uchun faqat o'qish huquqiga ega guvoh tokenini taqdim etadi. Tokenni panelning **Witness** sahifasida yarating, uni bot tokeni va kanal bilan `.env` ga qo'shing, so'ng profilni ishga tushiring:

```
docker compose --profile witness up -d          # deploy/compose/compose.image.yaml: same flag
docker compose logs witness                     # witness key fingerprint
```

Xizmat Compose tarmog'idagi `http://tgwitness:8787` manzildagi yig'uvchiga ulanadi (`TGWITNESS_WITNESS_COLLECTOR` ustun keladi, masalan, boshqa ish maydoni uchun `/profiles/<workspace ID>` ). Alohida serverda, boshqa birov tomonidan boshqariladigan guvoh uchun `deploy/compose/compose.witness.yaml` manzilini ishlating va `TGWITNESS_WITNESS_COLLECTOR` ni yig'uvchining HTTPS manziliga o'rnating; o'sha faylda faqat guvoh bo'ladi.

## Nashr qilingan rasmni o'rnating

Bu muvaffaqiyatli [reliz jarayoni](https://phishdestroy.github.io/TgWitness/uz/docs/reference/deployment/#automated-github-releases) va ommaviy GHCR paket konfiguratsiyasidan so'ng mavjud bo'ladi. Repozitoriy egasi/nomi ushbu manba daraxtiga qattiq kiritilmagan. Ushbu reliz jarayoni xulosasida ko'rsatilgan tasvirni ishlating.

`deploy/env.example` nusxasini `.env` ga nusxalang. `TGWITNESS_IMAGE` ni e'lon qilingan versiyaga, **kichik harfli** ombor yo'lidan foydalangan holda o'rnating, masalan:

```
TGWITNESS_IMAGE=ghcr.io/your-owner/your-repository:0.7.0
TGWITNESS_PORT=8787
```

`compose.yaml` o'rniga, ushbu faylni mustaqil ravishda ishga tushiring:

```
docker compose --project-directory . -f deploy/compose/compose.image.yaml pull
docker compose --project-directory . -f deploy/compose/compose.image.yaml up -d --wait
docker compose --project-directory . -f deploy/compose/compose.image.yaml exec tgwitness cat /data/panel-token.txt
```

Hostda manba kodini kompilyatsiya qilish, Python yoki kompilyator o'rnatilishi shart emas. Reliz jarayoni Linux AMD64 va ARM64 konteynerlarini, jumladan Docker Desktop'ning Linux virtual mashinasi (VM)ni qo'llab-quvvatlaydi. Jarayon tavsifidan versiya tegini yoki `ghcr.io/owner/repository@sha256:...` ni ishlating. `latest` tegini ko'chirish yoki ilovani nazoratsiz yangilash sozlanmagan. Image va manba variantlari loyiha nomlari mos kelganda bir xil ma'lumot hajmini ishlatadi.

## Serverda avtomatik HTTPS

Docker bilan ishlaydigan server, nazorat qiladigan domeningiz va doimiy mahalliy saqlash joyidan foydalaning. Domenda A/AAAA yozuvlarini serverga yo'naltiring; IPv6 unga yetib kelganda AAAA yozuvini nashr eting. Kiruvchi TCP 80 va 443 portlarini hamda sertifikat chiqarish uchun chiquvchi DNS/HTTPS trafigini ruxsat eting. Boshqa xizmatlar ushbu portlarni allaqachon egallab olmagan bo'lishi kerak.

`deploy/env.example` ni `.env` ga nusxa ko'chiring va sxema yoki yo'l ko'rsatmasdan host nomini belgilang:

```
TGWITNESS_DOMAIN=watch.your-domain.org
```

HTTPS ustki qatlami bilan manba kompilyatsiyasini ishga tushiring:

```
docker compose -f compose.yaml -f deploy/compose/compose.https.yaml up -d --build --wait
docker compose -f compose.yaml -f deploy/compose/compose.https.yaml exec tgwitness cat /data/panel-token.txt
```

```
docker compose --project-directory . -f deploy/compose/compose.image.yaml -f deploy/compose/compose.https.yaml up -d --wait
```

E'lon qilingan rasm uchun o'rniga birinchi fayl sifatida `deploy/compose/compose.image.yaml` ni ishlating. Keyingi holat, loglar, yangilash va to'xtatish buyruqlari uchun ikkala `-f` argumentini saqlang.

Caddy sertifikatni oladi va yangilaydi, HTTP-ni HTTPS-ga yo'naltiradi va so'rovlarni xususiy Compose tarmog'idagi yig'uvchiga uzatadi. Sertifikat holatiga o'zining doimiy hajmi biriktirilgan. Yig'uvchining to'g'ridan-to'g'ri host porti faqat loopback uchun mo'ljallangan bo'lib qoladi. Taqdim etilgan Caddy konfiguratsiyasi kirish jurnalini yuritishni yoqmaydi.

`https://watch.your-domain.org`ni oching va panel tokenini kiriting. Tayyorlik holatini aniqlash sertifikat berilganini yoki tashqi ulanish imkoniyatini tasdiqlamaydi. Agar HTTPS tayyor bo'lmasa, DNS, firewall qoidalarini tekshiring va:

```
docker compose -f compose.yaml -f deploy/compose/compose.https.yaml logs --tail 100 caddy
```

Taqdim etilgan Caddy tasviri uning `2-alpine` tegiga ega. Pulling o'sha tasvirni yangilaydi; agar sizga infratuzilma versiyalarini barqaror saqlash kerak bo'lsa, joylashtirishingizda sinovdan o'tgan digestni pin qiling.

## Yangilanishlar va zaxira nusxalari

Yangilanishlar davomida Compose loyiha nomini va ma'lumot hajmini saqlab qolish. Avvalo, to'plovchini to'xtating va to'liq zaxira nusxasini yarating. Standart manbaga asoslangan joylashtirish uchun:

```
docker compose stop
docker compose cp tgwitness:/data ../tgwitness-backup-before-update
```

Har safar ombor tashqarisida yangi zaxira manzilini ishlating va uni hisobga kirish materiali sifatida himoya qiling. Misol yo'li ko'rsatmali; shaxsiy zaxira joyingizdan foydalaning. Yashirin fayllar, barcha ish maydonchalari, kalitlar, jurnal va media hamda butun papkani nusxalang. Agar sozlangan bo'lsa, tashqi omborning bosh kalitini alohida zaxiralang. Dalil ZIP fayli tiklanadigan ilova zaxira nusxasi emas. HTTPS uchun, agar uning sertifikat/hisob holatini saqlash zarur bo'lsa, Caddy hajmlari ham saqlansin.

Manbaani ishga tushirish uchun yangi reliz fayllarini oling va quyidagi buyruqni ijro eting:

```
docker compose up -d --build --wait
```

Image deploy uchun `TGWITNESS_IMAGE` ni xohlagan versiyaga o'zgartiring, so'ngra quyidagi buyruqni ishga tushiring:

```
docker compose --project-directory . -f deploy/compose/compose.image.yaml pull
docker compose --project-directory . -f deploy/compose/compose.image.yaml up -d --wait
```

Oldingi stop/copy buyruqlari uchun ham o'rnatishingizning Compose fayllaridan foydalaning. `.env`, maxsus konfiguratsiya va loyiha nomini o'zgarmas qoldiring. `down` nomlangan hajmlarni saqlaydi; **`down -v` ularni o'chiradi**. `.venv` ni operatsion tizimlar yoki Python versiyalari o'rtasida nusxalamaslikka harakat qiling. Mahalliy yangilanishlar uchun TgWitness ni to'xtating, uning to'liq ma'lumotlar katalogining zaxira nusxasini oling, manba fayllarini almashtiring va ishga tushirishdan oldin `python start.py --setup-only` ni ishga tushiring.

Yangilanishdan so'ng panelga kirish, hisob identifikatori, kuzatuv holati va qamrovni tekshiring. Qayta ishga tushirish o'tkazib yuborilgan Telegram yangilanishlarini tiklamaydi. Agar kelajakdagi versiya saqlash formatlarini o'zgartirsa, rollback uchun oldingi yangilanishdan oldingi zaxira nusxasi talab qilinishi mumkin.

## Avtomatlashtirilgan GitHub relizlari

[Chiqarish ish](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/release.yml) jarayoni ushbu loyiha GitHub omboriga Actions yoqilgan holda joylashtirilgach ishlashga tayyor bo'ladi. U GitHub Release **e'lon** qilinganda, jumladan prerelease ham, ishga tushadi. Faqat loyihalar (drafts) yoki tag push qilish paketlarni e'lon qilmaydi.

1. Paket versiyasi va o'zgarishlar jurnalini sozlang, so'ngra `v` tegiga ega chiqarilishni nashr eting qo'shimcha ravishda aniq `pyproject.toml` versiyasini, masalan `v0.7.0`.
2. Jarayon tegni tasdiqlaydi va Windows/Linux/macOS uchun umumiy Python, hisob-import/QR brauzer, manba paket va Docker tekshiruvlarini ishga tushiradi. Shuningdek, barcha uch operatsion tizimda Python 3.12 yordamida yangi mahalliy o'rnatish ham sinovdan o'tkaziladi.
3. Ushbu tekshiruvlar muvaffaqiyatli o'tkazilgach, u QEMU ostida ARM64 imidjini smoke-test qiladi, AMD64/ARM64 imidjlarini `ghcr.io/<lowercase-owner>/<lowercase-repository>:<version>` ga joylaydi va manba ZIP-faylini, checksum hamda Python wheel-ni relizga ilova qiladi. Alohida Windows vazifasi esa portativ ZIP-faylni yaratib, uning checksumini ham ilova qiladi.
4. Birinchi nashrdan so'ng, GHCR paket sozlamalarini oching va agar anonim rasm yuklab olish mo'ljallangan bo'lsa, ko'rinishni **Public** (Ommaviy) ga o'rnating. Faqat ommaviy manba ombori ommaviy konteyner paketini kafolatlamaydi. Tashkilot siyosati paket nashr etilishiga ruxsat berishi kerak. Ish jarayoni `GITHUB_TOKEN` ni ishlatadi; omborda hech qanday registr paroli yoki VPS ma'lumotlari bo'lmasligi kerak.

Uzoqdan ish jarayonining muvaffaqiyati ushbu mahalliy tayyorgarlik bilan aniqlanmagan. ARM64 emulyatsiyasi — bu dastlabki tekshiruv bo'lib, u asl apparat yoki jonli Telegram uchun malaka emas. Bu chiqarilishni paketlashni avtomatlashtiradi; serverni ishga tushirish uchun hanuzgacha Compose buyrug'i va uning domen/mehmon oldindan shartlari talab etiladi. Mavjud serverlar chiqarilish e'lon qilinganda jimjit yangilanmaydi yoki qayta ishga tushirilmaydi.

## Masofaviy server

Xizmatni loopback manziliga bog'lab qo'ying va SSH tunneli ishlating yoki HTTPSni teskari proxyda yakunlang. Asosiy Compose fayli faqat mahalliy; ixtiyoriy `deploy/compose/compose.https.yaml` ustki qatlami sozlangan domen uchun Caddy'ni ta'minlaydi. URL manzillari va proxy jurnallarida bearer tokenini ko'rsatmang. Revers-proxy so'rov hajmi va ulanish tezligini cheklashi kerak. Oddiy HTTP-ni Internetga ochiq qoldirmang.

[deploy/](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md) katalogida systemd, Windows logon vazifasi, macOS foydalanuvchi agenti va Caddy uchun misollar keltirilgan. Ularni o'rnatishdan oldin yo'llarini ko'rib chiqing va moslashtiring. Ular shablonlar bo'lib taqdim etilgan, mahalliy ijro etiladigan platforma kvalifikatsiyalari emas. Oddiy ishga tushiruvchi orqali hech qanday fon xizmati yoki vazifa ro'yxatga olinmaydi.

Windowsda oynasiz `pythonw.exe` ishga tushirilganda, diagnostika ma'lumotlari `logs/server.log` ning ma'lumotlar katalogida (har bir fayl uchun 5 MiB, ikkita aylantirilgan zaxira nusxa) saqlanadi. Konsolda ishga tushirishlar konsol yozuvlarini saqlab qoladi. HTTP kirish yozuvlari ikkala rejimda ham o'chirilgan. Loglarni ma'lumotlar katalogi bilan himoya qiling va ulashishdan oldin tekshirib chiqing.

## Qayta boshlash va bo'shliqlar

So'nggi so'ralgan kuzatuv holati saqlanadi. Agar kuzatuv faol bo'lsa, dastur ishga tushirilganda ulang'ichni qayta ulashga va tanlangan manbalarni tiklashga harakat qiladi. Qo'lda pauza qilish bu niyatni bekor qiladi. Muvaffaqiyatsiz qayta ishga tushirish qayd etilib, panelda ko'rsatiladi.

StringSession avtorizatsiyani saqlab qoladi, lekin Telethonning doimiy yangilanish/obyekt holatini emas. Dialog oynalari ishga tushirilganda qayta yuklanadi. Telegram/Telethon ish vaqtida ba'zi transport uzilishlarini tiklashi mumkin, ammo TgWitness jarayonni qayta ishga tushirgandan keyin doimiy qayta ijro etishni kafolatlamaydi. Har bir ishga tushirishda avvalgi jurnal sarlavhasi va oflayn chegarasi qayd etiladi. Monitor har 10 soniyada ulanishni tekshiradi va har daqiqada yurak urishi yozuvini qo'shadi (**Parametrlar → Jonlilik yozuvini har safar qayd etish**). Qisqa uzilishlar e'tibordan chetda qolishi mumkin; ulangan transport to'liq yangilanish yetkazib berilishini kafolatlamaydi. Snapshotlar aniq joriy-tarixiy kuzatuvlar bo'lib, hech qachon bo'shliqlarni to'ldirmaydi.

Media navbati har bir ish maydonining SQLite ma'lumotlar bazasida saqlanadi. Xabar va uning ishi atomik tarzda yakunlanadi. To'xtab qolgan ishlar ish boshlanganda qayta urinish uchun tiklanadi. Har bir yuklab olish uchun 120 soniyalik asosiy timeout va hajmiga qarab 256 KiB/s tezlikda hisoblanadigan qo'shimcha vaqt, shuningdek har bir ilova turi uchun 1–2 000 MiB limit mavjud; timeout, tezlik va qayta urinishlar **Parametrlar** bo'limida sozlanadi. Yig'uvchi hajmi noma'lum bo'lgan fayllarni o'tkazib yuboradi. To'xtatish navbatdagi ishlarni saqlab qoladi. Qayta urinish dastlab kuzatilgan fayl tasvirini (file descriptor) ishlatadi, keyinchalik tahrirlangan xabarning eng so'nggi versiyasini emas. Vaqtinchalik xatoliklar cheklangan urinishlarga ega; media FloodWait pauzalari qayta ishga tushirishdan keyin ham saqlanadi. Media tiklash Telegram yangilanishlarini tiklashdan alohida bo'lib, yo'qolgan fayllarni qayta yaratolmaydi.

## Zaxira, tiklash va sig'im

**Butun ma'lumotlar katalog**ini, jumladan vault.key, signing.enc, credentials.enc, SQLite ma'lumotlar bazasi/WAL fayllari, media, token, tekshiruv nuqtalari va barcha profil/kichik kataloglarni nusxalashdan oldin jarayonni to'xtating. Maqsadli xizmat to'xtatilgan paytda to'liq nusxani tiklang. Yo'qolgan vault kalitlari yoki signing-key nomuvofiqligi ishga tushirishni muvaffaqiyatsiz yakunlaydi; majburiy kirish uchun kalitlarni qayta yaratmang.

Maxfiy zaxira nusxalarini shifrlangan va kirish nazoratli holda saqlang. Dalil ZIP-fayllari ko'chma: ular ilova zaxira nusxalari yoki Telegram sessiyasi zaxira nusxalari emas, balki artefaktlarni ko'rib chiqish uchun mo'ljallangan. Avtomatik saqlash yoki o'chirish mavjud emas. Barcha xabarlar, xom metadata, media, vaqtinchalik eksportlar va zaxira nusxalari uchun disk maydonini rejalashtiring.

Butun jurnalni yuklash o'rniga boshlang'ich tekshiruv va eksport oqim yozuvlarini ishga tushiradi. Eksport o'qish snapshotini mahkamlaydi, shu bilan birga yangi WAL yozuvlari davom etishi mumkin; uzoq davom etadigan eksportlar WAL sahifalarini saqlab qolishi mumkin, shuning uchun disk sig'imi hali ham muhim. ZIP-lar 4 GiB bilan cheklangan siqilmagan holda, mustaqil tekshiruvchining standartiga mos kelishi uchun; **Parametrlar → Eng katta imzolangan ZIP** limitni oshiradi va bunday arxivlar `verify.py --max-gib N` bilan tekshiriladi. Boshqa formatlarda voqealar soni bo'yicha cheklov yo'q. Qo'llab-quvvatlanadigan brauzerlar javob bo'laklarini foydalanuvchi tanlagan faylga oqimlaydi. Boshqa brauzerlar eng ko'pi bilan 128 MiB buferlaydi va kattaroq uzatmalarni autentifikatsiyalangan CLI ga yo'naltiradi:

```
python -m tgwitness.download --token-file data/live/panel-token.txt --out evidence.zip
```

Boshqa ish maydoni uchun **Exports → Workspace ID** bo'limidan `--profile ID`, masofaviy server uchun `--format zip|jsonl|csv|html` va `--url https://your-server` yoki 5 GiB uzatish limitini o'zgartirish uchun `--max-mib` ni ishlating. Oddiy HTTP faqat loopback uchun ruxsat etiladi. Tokenlar sarlavhalarda uzatiladi, yo'naltirishlar rad etiladi, mavjud fayllar ustidan yozib tashlanmaydi va to'liq bo'lmagan yuklamalar yakuniy fayllar sifatida e'lon qilinmaydi. Agar TGWITNESS_TOKEN hosil qilingan tokenni bekor qilsa, alohida himoyalangan va o'sha faol qiymatni o'z ichiga olgan fayldan foydalaning: panel-token.txt ustun qo'yish orqali yozib tashlanmaydi. Buyruqning SHA-256 qiymati faqat uzatish tekshiruv yig'indisi hisoblanadi; imzolangan ZIP faylni mustaqil ravishda tekshiring.

Server eksport fayllari har bir ish maydonining maxfiy `temporary-exports/` papkasida qoladi. Muvaffaqiyatli javoblar o'z fayllarini tozalaydi. To'xtab qolgan eksportlar keyingi ish maydoni ishga tushirilganda, uning eksklyuziv instantsiya qulfi ushlab turilgan holda olib tashlanadi. Ushbu katalog saqlash tahdidi/sig'im modelining bir qismi hisoblanadi; shifrlangan ma'lumot hajmini ishlating. Ishlab chiqarish miqyosidagi ko'p gigabaytli uzatmalar hanuzgacha maqsad tizimingizda malaka talab qiladi.

Panel navbatga qo'yilgan/muvaffaqiyatsiz bo'lgan media, eng qadimgi kutayotgan media, bo'sh disk, Telegram so'rovlari to'xtatib turilgan vaqtlar hamda kirish tasdiqlanmagan manbalarni ko'rsatadi. Ushbu diagnostika vositalari to'liq oxirigacha yetkazib berish monitoringi emas. Ish maydonchalari jarayonni baham ko'radi; shovqinli hisob boshqalarga ham ta'sir qilishi mumkin. Alohida ishchi jarayonlar, saqlash muddati/aylantirish, barqaror yangilanishlarni tiklash va to'liq joriy etishni tasdiqlash saqlanib qoladi. Panelga cheklangan kirish huquqi [kirish va ruxsatnomalar](https://phishdestroy.github.io/TgWitness/uz/docs/reference/access/) hujjatlarida qayd etilgan; mustaqil tekshiruv nuqtalari [guvoh](https://phishdestroy.github.io/TgWitness/uz/docs/reference/witness/)qo'llanmasida ko'rib chiqilgan.

## Ulanish va himoya variantlari

Ulanish yo'nalishlari har bir ish maydoni uchun alohida bo'lib, avtorizatsiyadan oldin sozlanishi kerak. SOCKS5/HTTP CONNECT pinlangan python-socks bog'liqligidan foydalanadi. MTProxy Telethonning eksperimental tasodifiy o'rta transportidan foydalanadi; Fake TLS ee sirlarini qo'llab-quvvatlamaydi. To'g'ridan-to'g'ri zaxira rejim tanlangan [IP](https://phishdestroy.github.io/TgWitness/uz/docs/reference/connection/#ip-modes)rejimiga bog'liq: IP ni yashirish (Hide IP) buni rad etadi; aniq zaxira rejimi kechikishdan so'ng bunga ruxsat beradi. Tunnel/VPN rejimi to'g'ridan-to'g'ri yo'nalishlarga ruxsat beradi, lekin VPN yaratmaydi. Bu butun tizim bo'ylab tarmoq siyosati emas.

Yangi o'rnatishlar uchun TGWITNESS_VAULT_KEY_FILE alohida himoyalangan tasodifiy master-kalit faylga yo'naltiriladi. Uni konteynerda /data tashqarisida faqat o'qish uchun o'rnatish kerak. Har bir ish maydoni va master kalit uchun public vault.external.json tuz metama'lumotlarini alohida saqlang. Mavjud mahalliy omborlar rejalashtirilgan migratsiyani talab qiladi; ushbu o'zgaruvchini sozlash ularni jimjit konvertatsiya qilmaydi. Xabar/media saqlash va eksportlar ilova tomonidan shifrlanmaydi. Zarur bo'lganda shifrlangan hajmlar va yetarli shaxsiy vaqtinchalik saqlashdan foydalaning.

Batafsil protseduralar: [ulanish/xavfsizlik](https://phishdestroy.github.io/TgWitness/uz/docs/reference/connection/) va [ishlash rejimlari](https://phishdestroy.github.io/TgWitness/uz/docs/reference/operations/).
