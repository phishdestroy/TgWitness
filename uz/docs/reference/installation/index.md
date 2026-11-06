# O&#x27;rnatish, tekshirish va yangilash

Canonical page: https://phishdestroy.github.io/TgWitness/uz/docs/reference/installation/

Bir buyruq bilan o&#x27;rnatish, imzo va xeshlarni tekshirish, o&#x27;rnatmani yangilash va o&#x27;chirish.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Hujjatlash](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Boshlash](https://phishdestroy.github.io/TgWitness/uz/docs/reference/quickstart/)

![Boshlash](https://phishdestroy.github.io/TgWitness/assets/chapter-start.svg)

[Loyiha](https://github.com/phishdestroy/TgWitness/blob/main/README.md) · [Tez boshlash](https://phishdestroy.github.io/TgWitness/uz/docs/reference/quickstart/) · [Joylashtirish](https://phishdestroy.github.io/TgWitness/uz/docs/reference/deployment/)

**Ushbu sahifada**

- [Bir buyruq bilan o'rnating](https://phishdestroy.github.io/TgWitness/uz/docs/reference/installation/#install-with-one-command)
- [Har narsa ishlaydigan joy](https://phishdestroy.github.io/TgWitness/uz/docs/reference/installation/#where-everything-runs)
- [To'liq matnli qidiruv sozlamalari](https://phishdestroy.github.io/TgWitness/uz/docs/reference/installation/#full-text-search-settings)
- [Komanda satri orqali kirish](https://phishdestroy.github.io/TgWitness/uz/docs/reference/installation/#command-line-access)
- [Ijro etishdan oldin tekshirish](https://phishdestroy.github.io/TgWitness/uz/docs/reference/installation/#verify-before-running)
- [Mavjud o'rnatishni yangilash](https://phishdestroy.github.io/TgWitness/uz/docs/reference/installation/#update-an-existing-installation)
- [Ubuntudagi kundalik buyruqlar](https://phishdestroy.github.io/TgWitness/uz/docs/reference/installation/#everyday-commands-on-ubuntu)
- [TgWitness so'zini olib tashlang](https://phishdestroy.github.io/TgWitness/uz/docs/reference/installation/#remove-tgwitness)

## Bir buyruq bilan o'rnating

Yo'naltirilgan o'rnatuvchi shaxsiy Python ijro muhitini o'z ichiga oladi. Keyingi o'rnatishlar uchun ham shu manzilni ishlating: har bir nashr o'rnatuvchi, xeshlar, imzo va kompilyatsiya ma'lumotlarini birgalikda yangilaydi.

**Linux / macOS (Bash):**

```
curl -fsSL https://get.destroy.tools/install.sh | bash
```

Ubuntu serverida fon xizmatini o'rnatish uchun root sifatida ishga tushiring. Stol usti kompyuterda esa oddiy foydalanuvchi sifatida ishga tushiring.

**Windows (PowerShell yoki Command Prompt):**

```
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "irm https://get.destroy.tools/install.ps1 | iex"
```

Windowsda administrator kerak emas. Farzand PowerShell jarayoni natija bilan terminalingizni ochiq qoldiradi. Python va unga bog'liq paketlar o'rnatishda qoladi.

Ubuntuda "**Ushbu kompyuter**", "**Vaqtinchalik HTTPS havolasi**" yoki "**O'z domeni**" ni tanlang. O'rnatuvchi panel manzili va kirish kalitini chop etadi. Vaqtinchalik havola uchun shu HTTPS manzilini brauzeringizda oching va kalitni kiriting. Masofaviy serverda mahalliy kirishni ta'minlash uchun kompyuteringizdan SSH orqali yo'naltirishdan foydalaning (`ssh -L 8787:127.0.0.1:8787 user@server`) va oching `http://127.0.0.1:8787`. macOS va Windowsda mahalliy panel brauzeringizda ochiladi; uning terminalini ishga tushgan holda saqlang.

Panelda Telegramga kiring va nimani yig'ishni tanlang. Faqatgina o'rnatish Telegram ma'lumotlarini yig'ishni boshlamaydi.

## Hammasi ishlaydigan joy

`get.destroy.tools` **statik yuklamalarni taqdim etuvchi Cloudflare Worker**'dir. Unda TgWitness paneli, Telegram sessiyasi yoki foydalanuvchi dalillari ma'lumotlar bazasi yo'q. U loyiha VPSiga yo'naltirilmagan. Ilova buyruqni ijro qilayotgan mashinada ishlaydi.

| O'rnatish | Dastur | Ma'lumotlar |
| --- | --- | --- |
| Ubuntu root sifatida | `/opt/tgwitness` | Tizim xizmati: `/var/lib/tgwitness-<installation ID>`; foydalaning `tgwitness paths` aniq yo'l uchun |
| Linux / macOS foydalanuvchisi | `~/.local/share/tgwitness` | `data/live` o'sha o'rnatish ostida. |
| Windows foydalanuvchisi | `%LOCALAPPDATA%\TgWitness` | `data\live` o'sha o'rnatish ostida. |

Sozlash `TGWITNESS_INSTALL_DIR` boshqa papkani tanlash uchun. O'rnatilgan versiyalar va ma'lumotlar alohida. O'rnatuvchi dastur sizning hisoblaringizni, xabarlaringizni yoki kalitlaringizni yuklab olish saytiga yuklamaydi. Cloudflare tunneli tanlanganda panel trafigi Cloudflare orqali yo'naltiriladi; o'zingizning domeningizdan foydalanganda esa u o'zingizning serveringizga yo'naltiriladi.

Har bir o'rnatishga mahalliy yo'llar, buyruqlar va omborga havolalar bilan **START-HERE.html** va **START-HERE.txt** fayllari kiradi. `tgwitness guide` qo'llanmani ochish uchun. Windowsda esa `& "$env:LOCALAPPDATA\TgWitness\bin\tgwitness.cmd" guide` PowerShell'da ishlating.

## To'liq matnli qidiruv sozlamalari

[To'liq matnli qidiruv](https://phishdestroy.github.io/TgWitness/uz/docs/reference/search/) (oldindan ko'rish) hech qanday sozlashni talab qilmaydi. Uning indeksi yangilanishdan so'ng fon rejimida yaratiladi.

| O'zgaruvchi yoki buyruq | Ta'sir |
| --- | --- |
| `TGWITNESS_FULLTEXT=disk` | Standart: indeks saqlanadi `search/fulltext.sqlite3` har bir ish maydonining |
| `TGWITNESS_FULLTEXT=memory` | Indeks fayli yo'q; indeks har boshlanishda qayta tuziladi |
| `TGWITNESS_FULLTEXT=off` | Indeks yo'q; faqat aniq matn bo'yicha qidiruv |
| `tgwitness index status` | Har bir ish maydonining holatini indekslash |
| `tgwitness stop`, `tgwitness index rebuild`, `tgwitness start` | Imzolangan jurnalning har bir indeksini qayta tuzing |

Administratorning **Journal → Filters → Search index** bo'limidagi tanlovi shu ish maydoni uchun o'zgaruvchini ustun qo'yadi. Buyruqlar ularni ishga tushirayotgan o'rnatmaning ma'lumotlar katalogini topadi; boshqa joylarda qo'shing `--data-dir` yo'ldan `tgwitness paths`. To'liq ukraincha lug'at (GPL-3.0 ma'lumotlari) uchun o'rnating `pymorphy3-dicts-uk` o'rnatishning Python muhitida o'rnatiladi.

## Komanda satri orqali kirish

[Komanda satri](https://phishdestroy.github.io/TgWitness/uz/docs/reference/cli/) (oldindan ko'rinish) skriptlar va agentlar uchun arxivni o'qiydi.

| O'zgaruvchi | Ta'sir |
| --- | --- |
| `TGWITNESS_URL` | Panel manzili uchun `tgwitness search`, `context`, `messages`, `stats` va `export`; standart `http://127.0.0.1:8787` token o'rnatilganda |
| `TGWITNESS_MCP_TOKEN` | **Integratsiyalar → MCP** bo'limidan MCP mijozlari bilan baham ko'rilgan ulanish tokenini arxivlang; `--token-file` uning o'rniga fayldan o'qiydi |
| `TGWITNESS_DATA` | Ma'lumotlar katalogi hech qanday bo'lmaganda to'g'ridan-to'g'ri o'qiladi `--data-dir`, URL yoki token ko'rsatilmagan taqdirda to'g'ridan-to'g'ri o'qiladi |

## Ijro etishdan oldin tekshiring

Bir qatorli buyruq dastlabki skript uchun HTTPS ga ishonadi. Ushbu skript o'rnatishdan oldin ilovadagi SHA-256 va loyihaning RSA imzolarini tekshiradi. Shuningdek, avval dastlabki skriptni yuklab olib, uni tekshirishingiz mumkin.

Jamoat chiqarish kaliti [release-signing.pub](https://github.com/phishdestroy/TgWitness/blob/main/deploy/installer/release-signing.pub). Uning SHA-256 esa:

```
039d98a658ccda14253e45a00335b4a68d840976d8ec18b8d4355cc7c458447d
```

Ishonadigan omborning reviziyasidan ushbu barmoq izini saqlang. Xuddi shu yuklab olish serveridan olingan tekshirish summasi nomuvofiqlikni aniqlaydi; mustaqil ravishda ishonchli deb tan olingan jamoat kaliti esa chiqarilgan imzoni autentifikatsiya qiladi.

Quyidagi tasdiqlash yuklab olishlari uchun yangi, bo'sh papka ishlating.

**Linux / macOS — yangi, bo'sh yuklab olish katalogida ishga tushiring** (curl va OpenSSL talab etiladi):

```
curl -fSLO https://get.destroy.tools/install.sh &&
curl -fSLO https://get.destroy.tools/install.sh.sig &&
curl -fSLO https://get.destroy.tools/release-signing.pub &&
test "$(openssl dgst -sha256 release-signing.pub | awk '{print $NF}')" = \
  '039d98a658ccda14253e45a00335b4a68d840976d8ec18b8d4355cc7c458447d' &&
openssl dgst -sha256 -verify release-signing.pub -signature install.sh.sig install.sh &&
bash install.sh
```

The `&&` Zanjir yuklash, kalit izi yoki imzo tekshiruvi muvaffaqiyatsiz bo'lsa, ijro etilishdan oldin to'xtaydi. Agar skriptni yuklab olish va uning imzosi o'rtasida nashr qilinsa, ikkalasini yana yuklab oling. Eski o'rnatgichlar o'zgarmas paket URL-manzillarini saqlab qoladi.

**Windows — ishga tushirishdan oldin SHA-256 ni tekshiring:**

```
Invoke-WebRequest https://get.destroy.tools/install.ps1 -OutFile install.ps1 -UseBasicParsing
Get-FileHash .\install.ps1 -Algorithm SHA256
Invoke-RestMethod https://get.destroy.tools/SHA256SUMS.txt
```

Hashni bilan solishtiring `install.ps1` qator bilan solishtiring. Mustaqil imzo tekshiruvi uchun OpenSSL (masalan, Git Bash orqali) va yuqoridagi xuddi shu jamoat kaliti barmoq izini ishlating:

```
curl -fSLO https://get.destroy.tools/install.ps1 &&
curl -fSLO https://get.destroy.tools/install.ps1.sig &&
curl -fSLO https://get.destroy.tools/release-signing.pub &&
test "$(openssl dgst -sha256 release-signing.pub | awk '{print $NF}')" = \
  '039d98a658ccda14253e45a00335b4a68d840976d8ec18b8d4355cc7c458447d' &&
openssl dgst -sha256 -verify release-signing.pub -signature install.ps1.sig install.ps1 &&
powershell.exe -NoProfile -ExecutionPolicy Bypass -File install.ps1
```

Windows o'rnatilishi o'zi .NET yordamida paket imzolarini tekshiradi va OpenSSL talab etilmaydi. Bu Authenticode emas, balki alohida RSA-3072 / SHA-256 imzolaridir. [Manifest](https://get.destroy.tools/manifest.json) dasturiy ta'minot versiyasini, aniq Git commitini, o'zgarmas reliz ID-sini va har bir artefaktning SHA-256-ni qayd etadi. Sahifa tegishli manbaga havola qiladi. Manifest va tekshiruv yig'indisi ro'yxatida ham alohida imzolar mavjud (`manifest.json.sig` va `SHA256SUMS.txt.sig`).

## Mavjud o'rnatishni yangilash

**Yangi nashr yuklab olish saytini yangilaydi; o'rnatilgan dasturlar installyerni yana ishga tushirganingizda yangilanadi.** Nazoratsiz yangilovchi yoki ishlayotgan to'plamni avtomatik qayta ishga tushirish mavjud emas. Joriy installyer kanali **ko'rgazmali**; u e'lon qilingan, tekshirilgan build-larni kuzatadi `main`, uning commit-i oxirgi raqamli GitHub relizidan yangiroq bo'lishi mumkin. Sahifaning versiyasi _____ dan olinadi. `pyproject.toml`; uning commit va build IDlari bir xil preview versiyasi ichidagi yangilanishlarni ajratib ko'rsatadi.

Ushbu aniq commit ilova va xavfsizlik tekshiruvlaridan o'tib, imzolangan paket Ubuntu xizmati va Windows PowerShell o'rnatish testlaridan muvaffaqiyatli o'tgach, nashr avtomatik amalga oshiriladi. Tekshiruvlar davom etayotgan paytda yoki ular muvaffaqiyatsiz tugasa, xuddi shu buyruqlar avvalgi tekshirilgan buildni o'rnatishni davom ettiradi. Build manifesti hozir qaysi commit mavjudligini ko'rsatadi; preview yangilanishlari orasida faqat versiya raqami o'zgarmasligi mumkin.

Avvalgidek o'rnatish papkasi va operatsion tizim foydalanuvchisini ishlating. To'plam to'xtatilgan holda to'liq ma'lumotlar katalogini zaxiralang; `tgwitness paths` uni aniqlaydi. Imzolangan eksport to'liq o'rnatish zaxira nusxasi emas.

**Ubuntu root o'rnatilishi `/opt/tgwitness`:**

```
curl -fsSL https://get.destroy.tools/install.sh | TGWITNESS_INSTALL_DIR=/opt/tgwitness bash -s -- --no-start
```

Muvaffaqiyatli o'rnatilgandan so'ng:

```
/opt/tgwitness/bin/tgwitness restart
/opt/tgwitness/bin/tgwitness status
/opt/tgwitness/bin/tgwitness open
```

Linux/macOS foydalanuvchisi uchun o'rnatishda uning asl `TGWITNESS_INSTALL_DIR` yoki tavsiya etilgan parametrni tanlab, birinchi o'rnatish buyrug'ini yana ishga tushiring. Yangilashdan oldin oldingi panelni yoping va yangilagandan so'ng uni qayta ishga tushiring. Sozlangan Linux foydalanuvchi xizmati uchun uning `tgwitness restart` buyrug'ini ishga tushiring.

**Windows:** ishlayotgan panelni yoping, Windows o'rnatish buyrug'ini yana ishga tushiring, so'ngra oching `bin\tgwitness.cmd` shu o'rnatishda. O'rnatuvchi ma'lumotlarni, sessiyalarni, kirish sozlamalarini va imzolash kalitlarini saqlab qoladi. U ishga tushiruvchini faqat yangi muhit o'z tekshiruvlaridan muvaffaqiyatli o'tgach almashtiradi; muvaffaqiyatsiz o'rnatish avvalgi ishga tushiruvchini o'z o'rnida qoldiradi. Saqlash formatidagi o'zgarishlar uchun yangilashdan oldingi zaxira nusxasini saqlang.

## Ubuntudagi kundalik buyruqlar

| Buyruq | Natija |
| --- | --- |
| `tgwitness open` | Joriy panel URL manzili va kirish kaliti. |
| `tgwitness paths` | Aniq dastur, ma'lumotlar va yo'riqnomalar yo'llari. |
| `tgwitness guide --print` | Oflayn ishlash bo'yicha ko'rsatmalar. |
| `tgwitness status` / `tgwitness logs` | Mavjudlik / xizmat jurnallari. |
| `tgwitness stop` / `tgwitness start` | Xizmatni to'xtatish / davom ettirish; ma'lumotlarni saqlash. |
| `tgwitness token rotate` | Administrator kalitini almashtiring va brauzer sessiyalarini yakunlang. |
| `tgwitness tunnel off` | Jamoat tezkor tunnelini o'chirib qo'ying; mahalliy panelni saqlang. |
| `tgwitness tunnel on` / `tgwitness tunnel restart` | Tezkor tunnel havolasini yarating / uning manzilini o'zgartiring. |

Hamkasb tokenlari, sessiyalar va IP-cheklovlar uchun [Access bo'lim](https://phishdestroy.github.io/TgWitness/uz/docs/reference/access/) iga hamda GitHub-dan Cloudflare-ga chiqarish ish jarayoni uchun [o'rnatgichni nashr qilishga](https://github.com/phishdestroy/TgWitness/blob/main/deploy/installer/README.md#automatic-publication-from-github) qarang.

## TgWitnessni olib tashlang

O'chirish dasturi yo'q: paneldan chiqib, uning papkalarini o'chirib tashlaysiz. Ma'lumotlar papkasini o'chirib tashlash jurnallarni, imzolash kalitlarini, Telegram sessiyalarini va saqlangan fayllarni qaytarib bo'lmas darajada yo'q qiladi. Buni amalga oshirishdan oldin:

1. Sizga kerak bo'lgan narsalarni eksport qiling (**Eksportlar → Imzolangan ZIPni yuklab olish**) va imzolash kalitining barmoq izi hamda tekshiruv nuqtalarini ushbu mashinadan tashqarida saqlang. Ish maydonini saqlab qo'yish uchun to'plam to'xtatilgan holda butun ma'lumotlar papkasini nusxalang.
2. **Extras → Server 24/7** bo'limida, **Your servers** yoki bilan yaratilgan serverlarni o'chirib tashlang `python -m tgwitness.cloud destroy`; provayder ular o'chirilguncha to'lov oladi.
3. Har bir hisobingiz sessiyasini Telegramda **Sozlamalar → Qurilmalar** bo'limida yakunlang. Fayllarni o'chirish Telegram tomonidan sessiyani chiqarib yuborishni anglatmaydi.

**Ubuntu root o'rnatilishi.** Ma'lumotlar papkasiga e'tibor bering, xizmatni to'xtating, so'ngra xizmatni, papkalarni va tezkor yo'lni o'chirib tashlang:

```
/opt/tgwitness/bin/tgwitness paths
/opt/tgwitness/bin/tgwitness stop
systemctl list-unit-files 'tgwitness-*'
systemctl disable tgwitness-<ID>
rm /etc/systemd/system/tgwitness-<ID>.service
systemctl daemon-reload
rm -rf /opt/tgwitness /var/lib/tgwitness-<ID> /usr/local/bin/tgwitness
```

**Linux yoki macOS foydalanuvchisi uchun o'rnatish.** Panelni yoping. Sozlangan Linux foydalanuvchi xizmati to'xtatiladi `systemctl --user disable --now tgwitness-<ID>`; uning bo'limi `~/.config/systemd/user/`. Keyin o'chirib tashlang `~/.local/share/tgwitness` (yoki sizning `TGWITNESS_INSTALL_DIR`) va `~/.local/bin/tgwitness` qo'lma-qo'lma yo'riqnomasini o'chirib tashlang.

**Windows.** Panelni yoping va o'chirib tashlang `%LOCALAPPDATA%\TgWitness` (yoki sizning `TGWITNESS_INSTALL_DIR`). O'rnatuvchi hech qanday xizmat, rejalashtirilgan vazifa yoki tezkor yo'riqnoma qo'shmaydi.
