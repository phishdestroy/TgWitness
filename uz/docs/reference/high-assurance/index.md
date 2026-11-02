# Yuqori ishonchlilikka ega joylashtirish

Canonical page: https://phishdestroy.github.io/TgWitness/uz/docs/reference/high-assurance/

Hetzner yoki Phala Cloud&#x27;da joylashgan, 24/7 yopiq server, Gateway DNS va uchinchi tomon takrorlay oladigan tekshiruvlar.

Imzolangan jurnal yozuvlar imzolangandan **keyin** o'zgartirilmaganligini isbotlaydi. Jiddiy holatlarda keyingi savol shuki, ma'lumotlar imzolanishidan **oldin** kimdir uni o'zgartirganmi: kollektorni kim ishga tushirgan, qaysi mashinada va unga kimdir kirganmi. Ushbu ixtiyoriy rejim kollektorni shunday joylashtiradiki, uchinchi tomon operatorning gapiga emas, bulut provayderi va Cloudflare saqlagan yozuvlarga tayanib tekshiruv o'tkazishi mumkin.

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

Mehmon o'lchovlari (SSH tinglovchilari va jarayonlar, joriy sessiyalar, kirishlar `wtmp`, yuklash) kollektorning o'zi tomonidan hisobot qilinadi va har bir jarayon boshlanishida hamda `host.state` yozuvlariga har safar o'zgarganda imzo qo'yiladi. Serverdagi root ularni soxtalashtirishi mumkin; ular provayder va Cloudflare yozuvlarini almashtirish o'rniga ularni qo'llab-quvvatlaydi.

## Provayderlar

| `--provider` | Kirish ma'lumotlari | Verifikatorning faqat o'qish huquqi | Verifikator uchun provayder logi | Saqlangan |
| --- | --- | --- | --- | --- |
| `hetzner` | `HCLOUD_TOKEN` | Shu loyihaning tokenini o'qish | Server va firewall harakatlari | Resurslar mavjud bo'lsa |
| `digitalocean` | `DIGITALOCEAN_TOKEN` | Faqat o'qish uchun shaxsiy kirish tokeni | Droplet harakatlari | Droplet mavjud bo'lgan paytda |
| `linode` | `LINODE_TOKEN` | `linodes`, `firewall`, `events` faqat o'qish uchun mo'ljallangan doiralar | Hisob voqealari, firewall qoidalarining versiyalari | 90 kun |
| `vultr` | `VULTR_API_KEY` | O'qish huquqiga ega foydalanuvchi va `activity_logs` ruxsati | Hisob faoliyati logi (usul, yo'l, ijrochi) | 30 kun, audit-log obunasiga ega bo'lsa, muddati uzaytiriladi |
| `aws` | `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` | `ec2:DescribeInstances`, `ec2:DescribeSecurityGroups`, `cloudtrail:LookupEvents` | CloudTrail voqealari tarixi | 90 kun |
| `phala` | `PHALA_CLOUD_API_KEY` | Bir xil ish maydonining API kaliti | Ilova versiyalari: kompozitsiya va muhit o'zgarishlari, qayta ishga tushirishlar, operatsion tizim yangilanishlari | Ilova mavjud bo'lsa |
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
| `tdx_os` | Bilan `--tdx-measurements`, MRTD va RTMR0-2 dstack OS tasviridan hisoblangan qiymatlarga teng (`dstack-mr measure --json`) |

Kollektorning jurnalda qayd etilgan har bir ishga tushishi bunday tasdiqnomaga ega, shuning uchun `verify --evidence` har bir boshlanishni tekshiradi. Phala'ning ilova o'zgartirishlari ro'yxati provayder logi vazifasini bajaradi: agar joylashtirishdan keyin kompozitsiya o'zgarsa, hisobot muvaffaqiyatsiz bo'ladi.

Panelda **Extras** → **Server 24/7** bo'limida **Confidential virtual machine · Phala Cloud** ni tanlang va Phala Cloud API kalitini joylashtiring; tez tunnel Hetzner'da ishlaydi. Buyruq satridan:

```
python -m tgwitness.cloud deploy --provider phala --name case-1 --server-type tdx.small \
    --ref v0.8.0 --repository https://github.com/phishdestroy/TgWitness --quick-tunnel \
    --provider-token-file phala-key.txt
python -m tgwitness.cloud verify --record deployments/case-1/deployment.json \
    --provider-token-file phala-key.txt --cloud-init deployments/case-1/docker-compose.yaml \
    --source CHECKOUT_OF_COMMIT --tdx-measurements dstack-mr.json
```

`--tdx-collateral` Intel sertifikatlari va bekor qilish ro'yxatlarini Intel'dan yuklab olish o'rniga fayldan o'qiydi. Gateway DNS bu yerda mavjud emas: Phala'da chiquvchi trafik uchun provayder firewalli yo'q.

Attestatsiya Intel'ning TDX modulidagi yoki mikrokodidagi nuqsonni yoki xotira magistraliga jismoniy kirishni inkor eta olmaydi. Phala hisobidagi ilovani nazorat qiluvchi shaxs boshqa compose joylashtirishi mumkin; u yangi compose hash bilan yangi tahrir sifatida paydo bo'ladi. Mezbon mashina vaqt manbai va tarmog'ini nazorat qiladi.

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

Nima uchun: Cloudflare hisobingiz bo'lmasa, tezkor tunnel yozuvlarini saqlamaydi, shuning uchun `verify` tunnel, ulanuvchi va DNS tekshiruvini mavjud emas deb hisoblaydi va natija eng yaxshi holatda `incomplete`; provayder yozuvlari, firewall, imzolangan bayonot, host o'lchovlari va o'rnatuvchi solishtirish odatdagidek tekshiriladi. Referens o'rnatuvchi bilan baytlar solishtirish uchun allaqachon nimani bilishini biladigan joylashtirilgan commit kerak `--quick-tunnel`; 0.7.0 versiyasini yuklab olish domen o'rnatuvchini yaratadi va farqni xabar qiladi. Cloudflare tezkor tunnel'larga ish vaqti kafolatini bermaydi, 200 ta so'rovni bir vaqtda uzatishga ruxsat beradi va Server-Sent Events'ni uzatmaydi, shuning uchun panelning jonli yangilanishlari (0.7.0 dan keyingi versiyalar) birinchi urinishda kelmasligi mumkin va sahifani qayta yuklash kerak bo'ladi; bu qism sinab ko'rilmagan. Ish berilishi kerak bo'lgan holat uchun o'zingizning domeningizdan foydalaning.

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

2026-yil 1-noyabrda Gateway DNS haqiqiy Hetzner Cloud va bepul Cloudflare hisobiga qarshi ishga tushirildi: Hetzner chiqish qoidalarini qabul qildi, server v0.7.0 versiyasini o'rnatdi va har bir so'rov TLS orqali Gateway orqali amalga oshirildi, tezkor tunnel shu firewall orqali ishladi va `verify` serverning 19 ta nomini Cloudflare'dan qayta o'qidi (Ubuntu va Hetzner oynalari, GitHub, PyPI, NTP, tunnel, ntfy.sh). Panel sakkizta oynada 36 ta so'rovni jurnalga nusxa ko'chirdi va `verify.py` ularni bo'shliqlarsiz qisqartirdi; `destroy` server va firewall o'chirib tashlandi va umumiy joy qoldirildi.

## Bu nima tasdiqlamaydi

- Provayder va uning xodimlari gipervizor, disklar va tarmoqni boshqaradi.
- Mehmon o'lchovlari kollektor tomonidan o'z-o'zini hisobot qiladi.
- Avvalgi firewall qoida mazmuni har bir provayder logida mavjud emas; faqat Linode qoida versiyalarini saqlaydi.
- Bu xabar haqiqiyligi haqida hech qanday yangilik keltirmaydi; qarang [Dalil](https://phishdestroy.github.io/TgWitness/uz/docs/reference/evidence/).

## Bu yerda sinovdan o'tkazilgan

Joylashtirish, qulflash va tekshirish mantiqi ularning e'lon qilingan API ma'lumotlariga asoslanib yaratilgan simulyatsiya qilingan Hetzner, DigitalOcean, Linode, Vultr, EC2/CloudTrail va Cloudflare APIlariga qarshi avtomatlashtirilgan testlar hamda AWS'ning e'lon qilingan misollariga muvofiq AWS so'rovlarini imzolash orqali qamrab olinadi. `tools/check_cloud_wizard.py` panelning server ustasini ham xuddi shunday ishga tushiradi: domen bilan va tezkor tunnel orqali. `tools/check_tdx.py` dcap-qvl va dstack'dan olingan haqiqiy Intel TDX tasdiqnomalarini Intel'ning ildiz sertifikatigacha tekshiradi (manbalar [tools/tdx/README.md](https://github.com/phishdestroy/TgWitness/blob/main/tools/tdx/README.md)'da); `tools/check_phala.py`simulyatsiya qilingan Phala Cloudga qarshi deploy, verify, journal, destroy va panel wizardni ishga tushiradi, uning attestatlari Intel uslubidagi soxta PKIdan olinadi. Phala yo'li hali Phala Cloudda sinab ko'rilmagan.

2026-yil 1-noyabrda tezkor tunnel yo'li real **Hetzner Cloud** (Nürnberg, `cpx22`, TgWitness v0.7.0), real ntfy.sh va GitHub, paneldan va koddan:

- narxni tekshirish, so'ngra panel tugmalari orqali yaratish: server 13 soniyadan so'ng ishga tushadi, taxminan ikki daqiqadan so'ng instantsiya va o'rnatuvchi hashlariga mos keladigan imzolangan bayonot;
- serverning o'z paneli trycloudflare.com manzili orqali ochilib, panel tokenini qabul qiladi; token bo'lmasa 401 javob beradi;
- Hetzner API orqali qayta ishga tushirilgach, server yangi imzolangan manzilni joyladi, **joriy manzilni** topdi, eski manzil javob berishni to'xtatdi, imzolash kaliti o'zgarmadi; ntfy.sh mavzusiga imzolanmagan post e'tiborsiz qoldirildi;
- `verify` Hetzner API ga qarshi: server, kiruvchi qoidalarisiz firewall, bayonot, bog'lash, mehmondo'st o'lchovlari, yuklash va v0.7.0 versiyasini yuklab olishning manba xeshidan o'tdi; Cloudflare tekshiruvlari yuqorida ta'riflanganidek mavjud emas edi; o'rnatuvchi v0.7.0 versiyasidagidan farq qilardi va bu versiyaning kodi tomonidan yaratilganiga baytma-bayt mos kelardi;
- paneldan o'chirish aynan joylashtirish belgilagan server va firewallni olib tashladi; bir xil loyihadagi boshqa serverlar va firewalllar o'zgarmagan holda qoldi.

Hali haqiqiy hisoblarga qarshi ishga tushirilmagan: o'zingizning domeningiz ostida joylashtirish (Cloudflare tunneli va DNS), boshqa provayderlar, xatoliklarni tuzatish bo'yicha joylashtirish va `lock`, bunday serverda Telegram akkaunti, va keyingi versiyalarning jonli yangilanishlari tezkor tunnel orqali. Har bir provayderda birinchi joylashtirishni tekshiring orqali `plan`, xatoliklarni tuzatish uchun joylashtirish va `verify` ishonishdan oldin, debug-deployment va har bir provayderda birinchi joylashtirishni tekshiring.
