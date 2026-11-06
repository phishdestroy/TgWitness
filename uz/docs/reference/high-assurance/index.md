# Yuqori ishonchlilikka ega joylashtirish

Canonical page: https://phishdestroy.github.io/TgWitness/uz/docs/reference/high-assurance/

Hetzner yoki Phala Cloud&#x27;da joylashgan, 24/7 yopiq server, Gateway DNS va uchinchi tomon takrorlay oladigan tekshiruvlar.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Hujjatlash](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Joylashtirish va tiklash](https://phishdestroy.github.io/TgWitness/uz/docs/reference/deployment/)

![Joylashtirish va tiklash](https://phishdestroy.github.io/TgWitness/assets/chapter-operate.svg)

Yuqori ishonchlilikka ega joylashtirish arxivni tekshirishga yig'ish muhitining mustaqil tekshiruvlarini qo'shadi. Ko'rib chiquvchi bulut provayderi va Cloudflare'da saqlangan joylashtirish va kirish yozuvlarini so'raydi, Intel TDX joylashtirishi esa yig'uvchining muhitini apparat tasdiqlash bilan to'ldiradi.

Oddiy mahalliy va Docker ishlatish o'zgarmagan. Bu yerda hech narsa ishlamaydi, agar siz uni bilan joylashtirmang `python -m tgwitness.cloud`, va collector faqat joylashtirishda sozlamalar belgilanganida mezbonini o'qiydi. `TGWITNESS_ASSURANCE`.

Oqim sxemasi · Operator → Server, kirish qoidalarsiz firewall (provayder API); Operator → Tunnel va DNS (Cloudflare API); Server, kirish qoidalarsiz firewall → Tunnel va DNS (faqat chiqish); Server, kirish qoidalarsiz firewall → Serverda yaratilgan imzolash kaliti; Verifier, faqat o&#x27;qish uchun tokenlar → Provayder logi va firewall; Verifier, faqat o&#x27;qish uchun tokenlar → Tunnel ulagich manzili va kirish; Verifier, faqat o&#x27;qish uchun tokenlar → Imzolangan /api/kafolat bayonoti; Verifier, faqat o&#x27;qish uchun tokenlar → Dalil ZIP · Operator · Verifier, faqato&#x27;qish uchun tokenlar · Server, kirish qoidalarsizfirewall · Provayder logi va firewall · Tunnel ulagich manzili vakirish · Imzolangan /api/kafolatbayonoti · Dalil ZIP · Tunnel va DNS · Serverda yaratilganimzolash kaliti · provayder API · Cloudflare API · faqat chiqish

**Diagramma matn sifatida**

1. Operator → Server, kirish qoidalarsiz firewall (provayder API)
2. Operator → Tunnel va DNS (Cloudflare API)
3. Server, kirish qoidalarsiz firewall → Tunnel va DNS (faqat chiqish)
4. Server, kirish qoidalarsiz firewall → Serverda yaratilgan imzolash kaliti
5. Verifier, faqat o&#x27;qish uchun tokenlar → Provayder logi va firewall
6. Verifier, faqat o&#x27;qish uchun tokenlar → Tunnel ulagich manzili va kirish
7. Verifier, faqat o&#x27;qish uchun tokenlar → Imzolangan /api/kafolat bayonoti
8. Verifier, faqat o&#x27;qish uchun tokenlar → Dalil ZIP

**Ushbu sahifada**

- [Verifikator tekshira oladigan narsalar](https://phishdestroy.github.io/TgWitness/uz/docs/reference/high-assurance/#what-a-verifier-can-check)
- [Provayderlar](https://phishdestroy.github.io/TgWitness/uz/docs/reference/high-assurance/#providers)
- [Phala Cloud'dagi maxfiy VM (Intel TDX)](https://phishdestroy.github.io/TgWitness/uz/docs/reference/high-assurance/#confidential-vm-on-phala-cloud-intel-tdx)
- [Boshlashdan oldin](https://phishdestroy.github.io/TgWitness/uz/docs/reference/high-assurance/#before-you-start)
- [Panelidan](https://phishdestroy.github.io/TgWitness/uz/docs/reference/high-assurance/#from-the-panel)
- [Domensiz tezkor tunnel](https://phishdestroy.github.io/TgWitness/uz/docs/reference/high-assurance/#quick-tunnel-without-a-domain)
- [Joylashtirish](https://phishdestroy.github.io/TgWitness/uz/docs/reference/high-assurance/#deploy)
- [Xatoliklarni tuzatish, joylashtirish va qulflash](https://phishdestroy.github.io/TgWitness/uz/docs/reference/high-assurance/#debug-deployment-and-lock)
- [Joylashtirishni olib tashlash](https://phishdestroy.github.io/TgWitness/uz/docs/reference/high-assurance/#remove-a-deployment)
- [Har qanday server (o'zini tasdiqlagan)](https://phishdestroy.github.io/TgWitness/uz/docs/reference/high-assurance/#any-server-self-attested)
- [Tasdiqlang](https://phishdestroy.github.io/TgWitness/uz/docs/reference/high-assurance/#verify)
- [Dalillarni topshirish bo'yicha hisobot](https://phishdestroy.github.io/TgWitness/uz/docs/reference/high-assurance/#report-for-evidence-handover)
- [Cloudflare tashqi guvoh sifatida](https://phishdestroy.github.io/TgWitness/uz/docs/reference/high-assurance/#cloudflare-as-an-outside-witness)
- [Joylashtirish natijasini o'qish](https://phishdestroy.github.io/TgWitness/uz/docs/reference/high-assurance/#reading-the-deployment-result)

## Verifikator nima tekshira oladi

| Da'vo | Qanday tekshiriladi | Tomonidan saqlangan |
| --- | --- | --- |
| Server ma'lum vaqtda provayder API orqali yaratilgan | Server obyekti va uning provayderning o'z logida yaratilishi | Provayder |
| Hech kim provayderning kirish yo'llaridan foydalanmadi | Konsol so'rovlari, tiklash, parolni tiklash, qayta qurish, ISO, tasvirlar, zaxira nusxalari logi | Provayder |
| Hech narsa unga ulanolmadi | Provayderning firewallida kirish qoidalari yo'q; SSH birinchi yuklashdan boshlab yashirilgan. | Provayder (firewall), host (SSH) |
| Panelga faqat tunnel orqali kirish mumkin | Tunnel kirishi faqat paneldagi manzilga yo'naltiriladi; ulagich server manzilidan ishlaydi | Cloudflare |
| Aynan shu dasturiy ta'minot ishlaydi | Yig'uvchining imzolangan manba daraxti hashiga joylashtirilgan commitning checkouti teng | Collector, Git bilan tekshirilgan |
| Imzo kaliti shu serverda yaratilgan | Kalit provayderning server IDsi va olgan cloud-initning xeshini ko'rsatadigan bayonotni imzolaydi | Provayderga qarshi tekshirilgan Collector |
| Jurnal o'sha kalit va serverga tegishli | Har bir jarayon dalillarda boshlanadiZIP o'sha server uchun mezbon o'lchovini o'zida saqlaydi | Dalil ZIP |

Yig'uvchi imzolangan process-start va `host.state` yozuvlarida SSH holatini, sessiyalarni, kirish tarixini va ishga tushirish ma'lumotlarini qayd etadi. Oddiy VMda bu mahalliy inventarizatsiya yozuvlari bo'lib, ko'rib chiquvchi ularni provayderning mustaqil yozuvlari bilan solishtiradi. Quyidagi Intel TDX joriy etilishi esa apparat bilan ta'minlangan o'lchovlarni ham tasdiqlaydi.

## Provayderlar

| `--provider` | Kirish ma'lumotlari | Verifikatorning faqat o'qish huquqi | Verifikator uchun provayder logi | Saqlangan |
| --- | --- | --- | --- | --- |
| `hetzner` | `HCLOUD_TOKEN` | Shu loyihaning tokenini o'qish | Server va firewall harakatlari | Resurslar mavjud bo'lsa |
| `digitalocean` | `DIGITALOCEAN_TOKEN` | Faqat o'qish uchun shaxsiy kirish tokeni | Droplet harakatlari | Droplet mavjud bo'lgan paytda |
| `linode` | `LINODE_TOKEN` | `linodes`, `firewall`, `events` faqat o'qish uchun mo'ljallangan doiralar | Hisob voqealari, firewall qoidalarining versiyalari | 90 kun |
| `vultr` | `VULTR_API_KEY` | O'qish huquqiga ega foydalanuvchi va `activity_logs` ruxsati | Hisob faoliyati logi (usul, yo'l, ijrochi) | 30 kun, audit-log obunasiga ega bo'lsa, muddati uzaytiriladi |
| `aws` | `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` | `ec2:DescribeInstances`, `ec2:DescribeSecurityGroups`, `cloudtrail:LookupEvents` | CloudTrail voqealari tarixi | 90 kun |
| `phala` | `PHALA_CLOUD_API_KEY` | Bir xil ish maydonining API kaliti | Ilova reviziyalari va CVM operatsiyalari: Docker Compose konfiguratsiyasi va muhit o'zgarishlari, qayta ishga tushirishlar, operatsion tizimni yangilashlar | Ilova mavjud bo'lsa |
| `generic` | yo'q | yo'q | yo'q: **o'zini tasdiqlagan** | – |

Har bir ish uchun maxsus loyiha, jamoa, hisob yoki kichik hisobdan foydalaning: tekshiruvchining faqat o'qish huquqi faqat shu joylashtirishni ko'rsatadi. Kirish ma'lumotlari `--provider-token-file` yoki yuqoridagi o'zgaruvchidan o'qiladi, hech qachon buyruq satridan emas. AWS uchun fayl saqlaydi `ACCESS_KEY_ID SECRET_ACCESS_KEY [SESSION_TOKEN]`; mintaqa esa `--location`.

Har bir provayderning yozuvlari ko'rsata olmaydigan narsa har bir hisobotda chop etiladi. Qisqasi: Hetzner konsol so'rovlarini qayd etadi; DigitalOcean'ning Recovery Console, Linode'ning Lish/Glish va Vultr'ning veb-konsoli shu tarzda qayd etilmaydi, shuning uchun root birinchi yuklashda qulflanadi va konsolga kirish parolni tiklash yoki yuklashni o'zgartirishni talab qiladi, bu esa qayd etiladi. Vultr instantsiyani o'qiy oladigan har qanday kalitga konsol manzilini qaytaradi; na yozuv, na hisobot uni saqlamaydi.

## Phala Cloud'dagi maxfiy virtual mashina (Intel TDX)

Bilan `--provider phala` to'plovchi dstack tomonidan boshqariladigan [Phala Cloud](https://phala.com/)'dagi Intel TDX maxfiy virtual mashinada ishlaydi. Host va Phala xodimlari uning xotirasini o'qiy olmaydi, protsessor esa mashinaning nimadan yuklanganligi haqidagi tasdig'ni imzolaydi. Tekshiruvchi Phala'ning gapiga ishonmaydi: `tgwitness.tdx` har bir tasdig'ni o'zi, hattoki belgilangan Intel SGX Root CA gacha, Intelning bekor qilish ro'yxatlari va Intelning imzolangan platforma ma'lumotlariga qarshi tekshiradi va xatolik tuzatilishi yoki ko'chirib olinishi mumkin bo'lgan mashinalarni rad etadi.

| Hisobot yozuvi | U nimani ko'rsatadi |
| --- | --- |
| `tdx_binding` | Tasdiq to'plovchining imzolangan bayonoti va ushbu so'rovning tasodifiy qiymatini o'z ichiga oladi. |
| `tdx_quote` | Intel attestatsiyani kafolatlaydi; u faqat Intel platformani yangilangan deb baholaganda o'tadi |
| `tdx_compose_hash` | RTMR3, dstack voqealar logidan qayta ijro etilganda, kollektorning hisobot bergan app-compose'ini o'lchaydi |
| `tdx_compose` | Ushbu kompozitsiya joylashtirilgan commit kodining bytema-byte nusxasi: manba fayllari hash bo'yicha biriktirilgan, ikkala rasm esa digest bo'yicha, boshqa hech qanday kod yo'q. |
| `tdx_identity` | Tasdiq joylashtirilgan ilova va instantsiya tomonidan beriladi, kalitlar Phala KMS'idan olinadi va disk shifrlangan. |
| `tdx_os` | MRTD va RTMR0-2 qiymatlari verifikator tomonidan Dstack-TEE operatsion tizimi tasviridan (Dstack-TEE tomonidan e'lon qilingan), CVM tomonidan xabar qilingan operatsion tizim tasviri xashi va VM shakli uchun QEMU tomonidan tuzilgan ACPI jadvallariga asoslanib hisoblangan qiymatlarga to'g'ri keladi: firmware, kernel, initrd, ildiz fayl tizimi xashi bilan buyruq qatori, xotira, vCPUlar va qurilmalar. Rivojlantirish tasviri muvaffaqiyatsiz bo'ladi |

Operatsion tizim tasviri (taxminan 180 MB, ulardan 21 MB saqlanadi) bir marta [Dstack-TEE/meta-dstack](https://github.com/Dstack-TEE/meta-dstack/releases) dan `dstack-images` yozuv yoniga yuklanadi; `--tdx-image FOLDER` boshqa papka yoki ochilmagan tasvirni ishlatadi, `--tdx-image none` taqqoslashni o'tkazib yuboradi. O'lchov `dstack-mr` va `qemu-acpi` Rust paketidan Dstack-TEE/dstack'dan keyin amalga oshiriladi; `tools/check_dstack_image.py` uni QEMU'ning o'z ACPI chiqishi va haqiqiy Phala Cloud apparat attestatlari yozuvi bilan solishtiradi, `--live` esa chop etilgan tasvir bilan ham solishtiradi. `--tdx-measurements` esa MRTD va RTMR0-2 ni JSON ko'rinishida solishtiradi.

Jurnalga yozilgan har bir kollektor ishga tushishi bunday tasdiqnomaga ega, shuning uchun `verify --evidence` har bir ishga tushishni va uning yuklagan OS tasvirini tekshiradi. Phala ilovasining versiyalari va CVM amallari provayder logi sifatida xizmat qiladi: joylashtirishdan keyin o'zgartirilgan Docker Compose konfiguratsiyasi hisobotda xato sifatida qayd etiladi va qayta ishga tushishlar ko'rib chiqish uchun ro'yxatlanadi.

Panelda **Extras** → **Server 24/7** bo'limida **Confidential virtual machine · Phala Cloud** ni tanlang va Phala Cloud API kalitini joylashtiring; tez tunnel Hetzner'da ishlaydi. Buyruq satridan:

```
python -m tgwitness.cloud deploy --provider phala --name case-1 --server-type tdx.small \
    --ref v0.8.0 --repository https://github.com/phishdestroy/TgWitness --quick-tunnel \
    --provider-token-file phala-key.txt
python -m tgwitness.cloud verify --record deployments/case-1/deployment.json \
    --provider-token-file phala-key.txt --cloud-init deployments/case-1/docker-compose.yaml \
    --source CHECKOUT_OF_COMMIT --fingerprint COLLECTOR_FINGERPRINT --report certificate.md
python -m tgwitness.cloud check-report --report certificate.pdf --verifier-fingerprint VERIFIER_KEY
```

`--tdx-collateral` Intel sertifikatlari va bekor qilish ro'yxatlarini Intel'dan yuklab olish o'rniga fayldan o'qiydi. Gateway DNS bu yerda mavjud emas: Phala'da chiquvchi trafik uchun provayder firewalli yo'q.

### Tasdiqlash sertifikati

Phala joylashtirish uchun `verify --report certificate.md` ham sertifikatni yozadi: a mustaqil `certificate.html` va A4 `certificate.pdf` xulosasi bilan, Intel ildizidan to'plovchi kalitigacha bo'lgan ishonch zanjiri, oddiy va yuqori kafolatli serverlar bilan solishtirish, e'lon qilingan imidjdan hisoblangan qiymatlar yonidagi o'lchovlar, har bir qism uchun kim kafolat beradi, Intel sertifikat zanjiri, har bir tekshiruv, provayder logi va tekshiruvni qanday takrorlash. JSON hisobot rasmiy yozuv bo'lib qoladi; sahifalar uni ko'rsatadi.

Hisobot `certificate.seal.json` va uning yonidagi `.tsq`/`.tsr` fayllarida imzo va vaqt shtamplari bilan raqamli muhrlangan:

| Muhr | Qo'shgan yangiliklari |
| --- | --- |
| Malakali elektron vaqt shtampi, `http://tsa.belgium.be/connect` | RFC 3161 vaqt shtampi Belgiya federal hukumatining malakali ishonch xizmat provayderi (FPS Siyosat va Qo'llab-quvvatlash, BOSA) tomonidan taqdim etilgan `certificate.json` aniq baytlariga nisbatan qo'llanadi. Ushbu birlik Belgiya Yevropa Ittifoqi ishonchli ro'yxatida malakali vaqt belgilash xizmati sifatida, maqoli berilgan holda keltirilgan; root (Belgium Root CA6) va ro'yxatdagi yozuvlar 2026-yil 20-oktabrdagi ro'yxatga muvofiq `tgwitness/tsa_roots.py` ga mahkamlangan. 910/2014-sonli Reglamentning 41-moddasiga muvofiq, bunday vaqt shtampi har bir Yevropa Ittifoqi a'zo davlatida sana va vaqt hamda ma'lumotlarning yaxlitligi bo'yicha to'g'ri deb qabul qilinadi. |
| RFC 3161 vaqt shtampi, FreeTSA | Ikkinchi, mustaqil vaqt tamg'asi |
| Verifikator imzosi | Ed25519 hashi hisobotning SHA-256 va har bir vaqt shtampini o'z ichiga olgan bayonot ustida, verifikatorning o'z kaliti (`--sign-with FOLDER`, standart `~/.tgwitness/verifier`) bilan tuziladi; PDF ham shu kalit bilan imzolangan |

`--timestamp URL` (takrorlanadigan) boshqa vakolatli organlarni tanlaydi, `--timestamp none` hech birini tanlamaydi, `--sign-with
none` muhrni imzolamasdan qoldiradi. `check-report` hisobotning xeshini, tasdiqlovchi imzosini, har bir vaqt shtampini ishonchli ildizga va uning malakali holatini, shuningdek PDF faylining imzosini tekshiradi. Yevropa Ittifoqi tashqarisidagi malakali vaqt shtampining va hisobotning butunlay huquqiy og'irligi uni qabul qiluvchi sud yoki organ zimmasidadir; muhr hisobot qachon mavjud bo'lganini va u o'zgarmaganini ko'rsatadi.

Attestatsiya Intel'ning TDX modulidagi yoki mikrokodidagi nuqsonni yoki xotira magistraliga jismoniy kirishni inkor eta olmaydi. Phala hisobidagi ilovani nazorat qiluvchi shaxs boshqa compose joylashtirishi mumkin; u yangi compose hash bilan yangi tahrir sifatida paydo bo'ladi. Mezbon mashina vaqt manbai va tarmog'ini nazorat qiladi.

Joylashtirish, `--evidence` bilan tekshirish, qayta ishga tushirishlar, operatsion tizim tasvirini solishtirish, imzo va vaqt shtamplari bilan raqamli muhrlangan sertifikat va yo'q qilish amallari Phala Cloud'da o'zida bajarilgan; qarang [, 2026-yil 4-noyabrdagi](https://phishdestroy.github.io/TgWitness/uz/docs/reference/verification/#live-phala-cloud-deployment--4-november-2026) ishga tushirish.

## Boshlashdan oldin

1. Cloudflare zonasining, uning hisob IDsi va **Cloudflare Tunnel Edit**, **Zone Read** va **DNS Edit** huquqlariga ega API tokeni, berilgan `--cloudflare-token-file` yoki `CLOUDFLARE_API_TOKEN`Verifikatsiya qiluvchi uchun: **Cloudflare Tunnel Read**, **DNS Read** va audit log uchun **Account Settings Read**. Domensiz [tezkor tunnel](https://phishdestroy.github.io/TgWitness/uz/docs/reference/high-assurance/#quick-tunnel-without-a-domain)ga bularning hech biri kerak emas.
2. Maxsus loyihaga yozish huquqiga ega provayder ma'lumotlari; `lock` xuddi shunday ishlatadi:

   - Hetzner: O'qish va yozish huquqiga ega API tokeni;
   - DigitalOcean: yozish huquqiga ega shaxsiy kirish tokeni;
   - Linode: shaxsiy kirish tokeni bilan `linodes`, `firewall` va `events` o'qish/yozish doiralariga ega;
   - Vultr: maxsus hisob yoki sub-hisobning API kaliti;
   - AWS: IAM kreditsiyalari ruxsat etilgan `ec2:DescribeVpcs`, `ec2:DescribeImages`, `ec2:CreateSecurityGroup`, `ec2:AuthorizeSecurityGroupIngress`, `ec2:RunInstances`, `ec2:CreateTags`, `ec2:DescribeInstances`, `ec2:DescribeSecurityGroupRules` va `ec2:RevokeSecurityGroupIngress`.
3. Ijro etiladigan commit. Reliz tegini bir marta uning commitiga hal qiladi `git ls-remote`; server faqat 40 belgili commitni oladi.

## Panelidan

O'zingizning kompyuteringizda **Extras → Server 24/7** ham xuddi shunday ishlaydi `deploy` Hetzner uchun uch bosqichda: Yevropa yoki Qo'shma Shtatlarni tanlang, Hetzner tokenini (O'qish va yozish) joylashtiring, so'ng server turi, oylik narxi, manzil va panel ushbu token orqali topgan versiyasini ko'rib chiqing. Siz tasdiqlamaguningizcha hech narsa yaratilmaydi. Panel har bir bosqichni quyidagicha ko'rsatadi `deploy` hisobot beradi, keyin manzil, panel tokeni va imzolash kalitining barmoq izi ko'rsatiladi. Domen bo'lmasa, serverga [tezkor tunnel](https://phishdestroy.github.io/TgWitness/uz/docs/reference/high-assurance/#quick-tunnel-without-a-domain) beriladi; **Sizning serverlaringiz → Joriy manzilni topish** qayta ishga tushirilgandan keyin uni yana tekshiradi. O'zingizning domeningiz ostida doimiy manzil uchun, **Imtiyozli · o'zingizning domeningizni** oching va Cloudflare tokenini qo'shing (tayyorlangan havola Zona o'qish, DNS tahrirlash va Cloudflare Tunnel tahrirlashni tanlaydi).

Tokenlar brauzer yorlig'idan TgWitnessgacha bo'lgan har bir so'rov bilan birga harakatlanadi va biror joyga yozilmaydi; joylashtirish yozuvi, tahrirlangan cloud-init, panel tokeni va tezkor tunnel uchun manzil kaliti `deployments/NAME` ma'lumotlar katalogi ichida. Panel buni faqat asosiy ma'murga to'g'ridan-to'g'ri loopback ulanishida taklif etadi (`127.0.0.1`, proksi yoki tunnel sarlavhalarsiz); tarmoq orqali ulanilgan panel esa uning o'rniga buyruqlarni ko'rsatadi. Versiya o'lchovi ishlayotgan panelning chiqarish tegiga (release tag) o'rnatilgan bo'lib, u GitHub API orqali aniqlanadi. Joylashuv, server turi va narxi Hetzner API'sidan olinadi: `cpx22` agar u taklif etilsa, aks holda kamida 2 GB xotiraga ega eng arzon x86 turi.

## Domensiz tezkor tunnel

`--quick-tunnel` o'rnini bosadi `--zone`, `--cloudflare-account` va `--panel-host`; Cloudflare hisob qaydnomasi yoki token ishtirok etmaydi:

```
python -m tgwitness.cloud deploy --provider hetzner --name case-2026-11 --server-type cpx22 \
    --ref 0123456789abcdef0123456789abcdef01234567 --quick-tunnel --provider-token-file hetzner.token
```

Serverda cloudflared panelga [tez tunnel](https://developers.cloudflare.com/tunnel/get-started/quick-tunnels/) ochadi: tasodifiy `https://….trycloudflare.com` manzilni har safar cloudflared yoki server qayta ishga tushirilganda o'zgartiradi. Serverdagi kichik bir xizmat har bir manzilni tasodifiy ntfy.sh mavzusiga joylaydi, uni faqat joylashtirish katalogida saqlangan kalit bilan imzolaydi (HMAC-SHA256) (`address-key.txt`), va uni har uch soatda takrorlaydi, chunki ntfy.sh postlarni 12 soat davomida saqlaydi. `deploy` **Joriy manzilni topish** faqat imzolangan postlarni qabul qiladi, shuning uchun soxtalashtirilgan post sizni va panel tokeningizni boshqasining manziliga yubora olmaydi. Mavzu yozuvda va e'lon qilingan cloud-initda mavjud: ularga ega bo'lgan har kim joriy manzilni o'qishi mumkin, u hanuzgacha panel tokenini so'raydi. Server hech qanday kiruvchi portni ochmaydi.

Verifikatorning manzil kaliti yo'q va mavzuni o'qiydigan har kim unga post yozishi mumkin. Shuning uchun collector ham manzilni o'zining Ed25519 kaliti bilan imzolab post qiladi va `verify` joylashtirish yozuvida collector kaliti bilan imzolangan eng yangi postni oladi; postlar ularning da'vo qilgan vaqtiga emas, balki ntfy.sh ularni qabul qilgan vaqtga ko'ra tartiblanadi. Ushbu o'zgarishdan oldingi kollektor hech narsani imzolamaydi va `verify` eng yangi postni oladi va `statement` tekshiruvida shuni bildiradi; soxtalashtirilgan post faqatgina ushbu tekshiruvni muvaffaqiyatsiz qilishi mumkin, chunki manzil hali ham kollektor kaliti bilan javob berishi kerak.

Nima uchun: tezkor tunnel yozuvlarini saqlamaydigan Cloudflare hisobotlari yo'qligi sababli, `verify` tunnel, konnektor va DNS tekshiruvini mavjud emas deb hisoblaydi va natija eng yaxshi holatda ham `incomplete` (Phala'da Cloud tekshiruv o'rniga o'tkaziladi: ulagich o'lchangan Docker Compose konfiguratsiyasi ichida ishlaydi); provayder yozuvlari, firewall, imzolangan bayonot, host o'lchovlari va o'rnatuvchi solishtirish odatdagidek tekshiriladi. Referens o'rnatuvchi bilan bayt solishtirish `--quick-tunnel` ni allaqachon biladigan joylashtirilgan commitni talab qiladi; 0.7.0 checkout domen o'rnatuvchini yaratadi va farqni xabar qiladi. Cloudflare tezkor tunnelar uchun ish vaqti kafolatini bermaydi, 200 ta so'rovni bir vaqtda uzatishga ruxsat beradi va Server-Sent Eventsni uzatmaydi, shuning uchun paneldagi jonli yangilanishlar (0.7.0 dan keyingi versiyalar) birinchi usul orqali yetib kelmasligi mumkin va ko'rinishni qayta yuklash talab qilinadi; bu qism sinab ko'rilmagan. Ishga tushirish zarur bo'lgan holat uchun o'zingizning domeningizdan foydalaning.

## Joriy etish

Avvalo yuboriladigan barcha narsalarni ko'ring. `plan` provayder yoki Cloudflare so'rovini yubormaydi:

```
python -m tgwitness.cloud plan --provider hetzner --name case-2026-11 --server-type cpx22 \
    --ref 0123456789abcdef0123456789abcdef01234567 --zone example.org \
    --cloudflare-account CLOUDFLARE_ACCOUNT_ID --panel-host case.example.org
```

Keyin bir xil parametrlar va kirish ma'lumotlari bilan joylashtiring:

```
python -m tgwitness.cloud deploy --provider hetzner --name case-2026-11 --server-type cpx22 \
    --ref 0123456789abcdef0123456789abcdef01234567 --zone example.org \
    --cloudflare-account CLOUDFLARE_ACCOUNT_ID --panel-host case.example.org \
    --witness-host case-witness.example.org \
    --provider-token-file hetzner.token --cloudflare-token-file cloudflare.token
```

Boshlash uchun server turlari: `cpx22` (Hetzner), `s-1vcpu-2gb` (DigitalOcean), `g6-standard-1` (Linode), `vc2-1c-2gb` (Vultr), `t3.small` (AWS). `--location` va `--image` har bir provayderning Yevropa mintaqasidagi Ubuntu 24.04 tizimini standart sifatida tanlaydi.

`--repository` URLda parol ko'rsatmasdan boshqa https Git omboridan commitni oladi (defolt `https://github.com/phishdestroy/TgWitness.git`). `deploy` ham qabul qiladi `--out` boshqa joylashtirish katalogi uchun (bo'shliganida `deployments/NAME`; allaqachon joylashtirish (deployment) mavjud bo'lgan papka rad etiladi) va `--wait`, yig'uvchining imzolangan bayonotini kutish uchun daqiqalar: 1 dan 240 gacha, standart 20, yoki 60 uchun `generic`.

Buyruq:

1. Cloudflare tunneli yaratadi, uning kirish qismi panel hostnomini panellarga yo'naltiradi va, agar berilgan bo'lsa, guvoh hostnomini `/api/witness/head` va `/api/assurance` faqat;
2. ushbu hostnomalar uchun proksi orqali CNAME yozuvlarini yaratadi, allaqachon mavjud bo'lgan nomlarni rad etadi;
3. kirish qoidalarsiz provayder firewalli va uning ortida SSH kalitisiz, zaxira nusxalarsiz, konsol agenti bo'lmagan va SSH ni yashiruvchi, rootni qulflash va o'rnatishni amalga oshiruvchi cloud-init bilan server yaratadi `cloudflared`, aynan kerakli commitni oladi, uni tekshiradi va TgWitnessni mustahkamlangan systemd xizmati sifatida ishga tushiradi;
4. yig'uvchining imzolangan bayonotini kutadi va unda aynan shu server hamda shu cloud-initning xeshini ko'rsatilganligini tekshiradi.

`deployments/case-2026-11/` so'ngra saqlaydi:

| Hujjat | Mavzular | Ulaish? |
| --- | --- | --- |
| `deployment.json` | IDlar, xeshlar, bajarilgan API chaqiruvlari (metod, yo'l, holat) va birinchi imzolangan bayonot | Ha, verifikator bilan |
| `cloud-init.redacted.yaml` | Aniq cloud-init ikkita sir o'rniga `REDACTED` | Ha |
| `panel-token.txt` | Panel tokeni | Yo'q |

Provayderning root paroli, tunnel tokeni va panel tokeni hech qachon yozilmaydi `deployment.json`. Yakunda chop etilgan kollektor barmoq izini o'zingiz nazorat qilmaydigan kanal orqali, masalan guvoh kanali yoki qabul qiluvchiga xabar orqali e'lon qiling.

Telegramga kirish uchun `https://case.example.org` panel tokeni bilan, [hisob](https://phishdestroy.github.io/TgWitness/uz/docs/reference/accounts/)yo'riqnomadagi kabi. Panel harakatlari imzolangan jurnalga yozib olinadi; ular SSH sessiyalari emas. [Guvoh](https://phishdestroy.github.io/TgWitness/uz/docs/reference/witness/) so'rov yuborishi mumkin `https://case-witness.example.org`.

SSH yo'q: agar bootstrap muvaffaqiyatsiz bo'lsa, yig'uvchi hech qachon javob bermaydi. Serverni o'chirib tashlang va qayta joylashtiring, yoki sababini aniqlash uchun debug joylashtirishdan foydalaning.

### Foydalanuvchi ma'lumotlaridagi sirlar

cloud-init ikkita sirni o'zida saqlaydi: panel tokeni va Cloudflare tunnel tokeni. Imzo kaliti ularning ichida yo'q; u serverda yaratiladi. Hetzner, DigitalOcean va Linode o'z API orqali foydalanuvchi ma'lumotlarini qaytarmaydi. Vultr esa instantsiyani o'qiy oladigan har qanday kalitga ma'lumotni qaytaradi, EC2 esa orqali `DescribeInstanceAttribute`. AWS uchun tasdiqlovchiga faqat jadvaldagi uchta harakatni bering, hech qachon `ec2:Describe*`. Vultr uchun verifikator kaliti ikkala tokenni ham o'qiy oladi deb hisoblang. Tunnel token kimgadir ikkinchi konnektorni ishga tushirishga imkon beradi: `verify` serverda bo'lmagan har qanday konnektorni aniqlaydi, va yig'uvchining bayonotlari shu tarzda soxtalashtirilmaydi, chunki har biri yangi chaqiriqni imzolaydi. `--quick-tunnel` ikkinchi sir o'rniga manzil kalitidir: uni o'qiydigan har kim paneldan qabul qilinadigan yolg'on manzilni joylashtira oladi.

Yig'uvchining ommaviy bayonotida server manzili va kirish manbalari keltirilmaydi; ular ikkalasi ham imzolangan jurnal ichida saqlanadi.

## Xatoliklarni tuzatish, joylashtirish va qulflash

`--debug-ssh-key KEY --debug-ssh-from 198.51.100.4` bitta manzil yoki kichik tarmoqdagi bitta kalit uchun SSHni saqlaydi, IPv4 uchun maksimal /24 yoki IPv6 uchun /48. `KEY` allaqachon provayderda ro'yxatdan o'tkazilgan: Hetzner loyihasidagi SSH kalitining nomi yoki IDi, DigitalOcean jamoasidagi SSH kalitining IDi yoki barmoq izi, profil SSH kalitlari root'ga qo'shilgan Linode foydalanuvchi nomi, Vultr hisobidagi SSH kalitining IDi yoki mintaqadagi EC2 kalit juftligining nomi. Ushbu variantlarga tegishli emas `generic`. Bunday joylashtirish `debug` va **hech qachon** yuqori ishonchlilik (high-assurance) darajasida hisoblanmaydi. Ishingiz tugagach, quyidagi buyruqni ijro eting `sudo tgwitness-lock` so'nggi SSH sessiyasining oxirgi buyrug'i sifatida, keyin:

```
python -m tgwitness.cloud lock --record deployments/case-2026-11/deployment.json --provider-token-file hetzner.token
```

Firewall barcha kiruvchi qoidalarni yo'qotadi. Hisobotlar keyin SSH qachon ruxsat etilgani va qachon yopilganini ko'rsatadi; o'sha oynacha ko'rinib turaveradi.

## Joylashtirishni olib tashlash

`destroy` server va uning firewall'ini, deployment'ning label'i bo'yicha topilgan holda o'chiradi, shunda yarim yo'lda muvaffaqiyatsiz bo'lgan deployment ham olib tashlanadi, keyin uning tunneliga yo'naltiruvchi DNS yozuvlari va tunnelni o'chiradi. Serverning jurnal va imzolash kaliti ham birga o'chiriladi: avvalo dalillarni eksport qiling. Yozuv qoladi, belgilangan `removed`, olib tashlash bo'yicha API chaqiruvlari bilan.

```
python -m tgwitness.cloud destroy --record deployments/case-2026-11/deployment.json --confirm case-2026-11 \
    --provider-token-file hetzner.token --cloudflare-token-file cloudflare.token
```

Hetzner uchun API orqali o'chirish amalga oshiriladi. Boshqa provayderlar uchun `destroy` hech narsani o'chirishdan oldin to'xtaydi va provayder konsolida o'chirish uchun yorliq nomini ko'rsatadi. Qo'lda o'rnatilgan server (`generic`) faqat tunnel va DNS yozuvlarini yo'qotadi. Tez tunnelni ishga tushirish uchun Cloudflare tokeni kerak emas: uning tunneli serverda tugaydi va uning postlari ntfy.sh saytida 12 soat ichida o'chadi.

## Istalgan server (o'zini tasdiqlagan)

`--provider generic` qo'lda sotib olingan yoki o'rnatilgan server uchun mo'ljallangan. `deploy` tunel va DNSni yaratadi, yozadi `install.sh` (maxfiy) va `install.redacted.sh` (e'lon qilish uchun), va kutadi. Ko'chirish `install.sh` Uni yangi o'rnatilgan Ubuntu 24.04 serveriga nusxalab oling va u yerda ishga tushiring:

```
sudo bash install.sh
```

U hostni avvalgi holatda yozib oladi (kirishlar, hisoblar, `authorized_keys`, tinglovchi soketlar, xizmatlar, rejalashtirilgan ishlar, paketlar), commitni o'rnatadi, host firewallini yoqadi, o'zini o'chirib tashlaydi, SSHni yashiradi va sessiyani yakunlaydi. Bunday server uchun hisobot eng yaxshi holatda **O'Z-O'ZINI TASDIQLANGAN**: installyerni ishga tushirgan kishi oldinroq root huquqlariga ega bo'lgan va tasdiqlovchi uchun provayder yozuvi mavjud emas. Bu hanuzgacha tushuntirilmagan serverdan yaxshiroq: inventarizatsiya, installyer xesh va har bir keyingi kirish imzolangan.

## Tasdiqlang

Verifikatorga kerak `deployment.json`, nashr etilgan o'rnatuvchi, faqat o'qish huquqli ma'lumotlar va, ideal holda, commit-ning nusxasi va dalilZIP:

```
git clone -c core.autocrlf=false https://github.com/phishdestroy/TgWitness.git checkout
git -C checkout checkout 0123456789abcdef0123456789abcdef01234567
python -m tgwitness.cloud verify --record deployment.json \
    --provider-token-file read-only.token --cloudflare-token-file cloudflare-read.token \
    --fingerprint COLLECTOR_FINGERPRINT --cloud-init cloud-init.redacted.yaml \
    --source checkout --evidence tgwitness-evidence.zip --report report.md
```

Har bir provayder va Cloudflare qiymati shu paytda tasdiqlovchi tomonidan so'raladi; yozuv faqat so'raladigan IDlarni taqdim etadi. Chiqish kodi **PASS** uchun 0, **FAIL** uchun 1 va **REVIEW**, **INCOMPLETE** yoki **SELF-ATTESTED** uchun 2 hisoblanadi. `--fingerprint` mustaqil kanal orqali kelishi kerak; aks holda kalit faqat operatorning yozuvi bilan solishtiriladi. `python verify.py` ZIP o'zi dalillarni hanuzgacha tasdiqlaydi, xuddi [Evidence](https://phishdestroy.github.io/TgWitness/uz/docs/reference/evidence/) dagi kabi.

Provayder harakatlari tasniflanadi: yaratish va yaratilganidan keyin 30 daqiqa ichida boshlanish muvaffaqiyatli; konsol, qutqarish, parolni tiklash, qayta qurish, ISO, tasvirlar, snapshotlar, zaxira nusxalari, Systems Manager, EC2 Instance Connect va firewall ochilishlari muvaffaqiyatsiz; quvvat harakatlari va kutilmagan har qanday harakat ko'rib chiqish uchun belgilangan. Noma'lum harakat hech qachon jim o'tkazilmaydi.

## Dalillarni topshirish bo'yicha hisobot

`--report report.md` Markdown hisobotini yozadi va `report.json` uning yonida:

1. natija, yig'uvchi kalit barmoq izi, joylashtirish, ta'minlovchi, commit, server, firewall, tunnel;
2. har bir tekshiruv uning holati va manbai bilan (provayder API, Cloudflare API, yig'uvchi bayonoti, dalillar jurnali);
3. provayderning har bir harakat bo'yicha bahosi va, provayder uni qayd etgan joyda, ijrochi;
4. tunelning ulanishlari, konfiguratsiyasi va audit logini saqlovchi Cloudflare nuqtalari;
5. imzolangan kollektor bayonoti;
6. hisobot nimani tasdiqlaydi va nimani tasdiqlamaydi;
7. Uni qayta yaratish uchun buyruqlar va unga berilgan har bir faylning SHA-256i.

Hisobotni topshiring, `report.json`, `deployment.json`, nashr etilgan o'rnatuvchi va dalillarniZIP. Hisobotni erta taqdim eting: provayder jurnallari cheklangan muddatgacha saqlanadi.

## Cloudflare tashqi guvoh sifatida

Bu yerda hamma narsa ixtiyoriy. Cloudflare hisobisiz ham server ishlaydi, va bugun ulardan ikkitasi ishlaydi:

| Nima | U nimani ko'rsatadi | TgWitnessda |
| --- | --- | --- |
| Tez tunnel yoki sizning domeningiz tunneli | paneldan faqat tunnel orqali erishiladi | server ustasi, yuqoriga qarang |
| drand relay `drand.cloudflare.com` | drand raundidan keyingi yozuvlar undan yangiroq: jurnal yozilgani sayin yozilgan | dalil rejimi, **Qo'shimcha guvohlar**, hisob yo'q ([format](https://phishdestroy.github.io/TgWitness/uz/docs/reference/evidence/#optional-records-in-evidence-mode-drand-and-telegram-devices)) |
| Tunnel holati bo'yicha bildirishnomalar | tunel ishlamay qolganda, elektron pochta yoki Cloudflare webhook orqali | ularni Cloudflare boshqaruv panelida sozlang |
| Gateway DNS (`--gateway-dns`, yoki ustadlikda **Cloudflare Gateway DNS**) | server so'rab topgan har bir nom, TLS orqali Cloudflare tomonidan javob berilgan; Hetzner firewall DNS-ni boshqa hech narsaga yo'naltirmaydi; Gateway siyosati javoblarni qayta yozishi mumkinmi | Hetzner, bepul Zero Trust rejasi, domensiz; `verify` fayervolni, joylashuvni, loglashni, siyosatlarni, server so'rovlarini va audit logini tekshiradi; dalil rejimi logni jurnalga nusxalaydi |
| Serverdagi Cloudflare One mijoziga ega Gateway, faqat Cloudflare'ni ruxsat etadigan chiqish devori | Server amalga oshirgan har bir ulanish, faqat DNS emas | hanuz yaratilmagan |
| Panel oldidagi kirish | kim paneldan qachon tizimga kirgan | qurilmagan: o'zingizning domeningiz kerak |
| SSH buyruqlarini loglash | debug sessiyasidagi har bir buyruq | hanuz yaratilmagan |

Logpush, u Cloudflare'ning o'z nusxasini R2'da saqlaydi, Enterprise xususiyati hisoblanadi: bepul rejada Cloudflare javob beradi `logpush is not enabled for this account`. U yerda Gateway logi 24 soat davom etadi, shuning uchun dalil rejimi uni imzolangan jurnalga nusxa ko'chiradi (**Cloudflare Gateway'ning ushbu serverning DNS so'rovlari logi**, Hisob Analitikasi O'qish huquqiga ega o'qish uchun mo'ljallangan token).

Zero Trust rejasi bo'lmasa, hisobning bitta DNS manzili bo'ladi. Cloudflare boshqa manzilni rad etganda, server mavjud manzilni baham ko'radi va uning so'rovlari manzili bo'yicha ajratiladi; o'sha filtrga ham Zero Trust PII Read huquqi kerak, va `destroy` ulashilgan joyni tark etadi. Bitta log so'rovi ko'pi bilan uch soatni qamrab oladi, shuning uchun nusxa va `verify` kunni uch soatlik oynalarda o'qiydi.

Gateway DNS tizim resolverini qamrab oladi. 443-port orqali HTTPS orqali boshqa resolverga yo'naltirilgan DNS so'rovlari va hech qayerda qidirilmagan manzillarga (masalan, Telegramning ma'lumot markazlariga) bo'lgan ulanishlar uning logida qayd etilmaydi.

Cloudflare Telegramning shifrlash ichki qismiga, Telegram hisobidagi boshqa qurilmalarga (evidence mode'ning qurilmalar ro'yxati ularni Telegram tomonidan qayd etadi) yoki provayderning gipervizoriga kira olmaydi.

## Joylashtirish natijasini o'qish

Oddiy VM uchun provayder host infratuzilmasini va mahalliy inventarizatsiyani nazorat qiladi hamda provayder yozuvlari bilan birga tekshiradi. Intel TDX uchun verifikator shuningdek apparat iqtibosi, yig'uvchi bog'lanishi, kompozitsiya va operatsion tizim o'lchovlarini ham tekshiradi. Qaysi tekshiruvlar o'tgani yoki mavjud emasligini ko'rish uchun yakka natijalarni o'qing.

Tarixiy firewall tafsilotlari provayderga bog'liq; Linode qoidalar versiyalarini saqlab qoladi. [Validatsiya yozuvi](https://phishdestroy.github.io/TgWitness/uz/docs/reference/verification/) sinovdan o'tkazilgan joylashtirishlarni va qolgan jonli tekshiruvlarni ro'yxatlaydi, hamda [tasdiqlash doirasi](https://phishdestroy.github.io/TgWitness/uz/docs/reference/evidence/#verification-scope) ushbu muhit tekshiruvlarini arxiv olish va yaxlitlik bilan bog'laydi.
