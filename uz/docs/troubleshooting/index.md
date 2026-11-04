# Nima noto'g'ri ketganini aniqlang

Canonical page: https://phishdestroy.github.io/TgWitness/uz/docs/troubleshooting/

Alomatdan boshlang, bir vaqtda bitta narsani tekshiring.

## Panel token so'raydi

U ishga tushirgich chop etgan fayldagi panel tokenini so'raydi. Docker: `docker compose exec tgwitness cat /data/panel-token.txt`. Telegram kodi emas, bot tokeni emas, guvoh tokeni ham emas.

## Telegram ulanmaydi

Ulanish tekshiruvini ishga tushiring. Ochiq proksida boshqasini tanlang va saqlang. Proksi turi va sir formatini tekshiring. Ro'yxatlarni yangilash marshrutni o'z-o'zidan almashtirmaydi.

## Ulanish mavjud, lekin yangi xabarlar yo'q

1. Kuzatuv to'g'ri ish maydonida ishlayaptimi?
2. Manba tanlanganmi va o'sha hisobga ko'rinadimi?
3. Sinov guruhingizda noyob xabar yuboring va uni qidiring.
4. Jurnalda uzilishlar yoki Telegram xatolarini qidiring.

Jim chatda shunchaki yangi narsa yo'q. To'liqlik muhim bo'lsa, nazorat ostidagi yetkazish sinovini o'tkazing.

## FloodWait yoki qayta ishga tushirgandan keyin bo'shliq

FloodWait Telegram'ning "sekinroq" deyishi. U o'tguncha kuting va yukni kamaytiring, qayta ulanish yordam bermaydi. Qayta ishga tushirgandan keyin TgWitness Telegram'da hali bor narsani to'ldiradi; qolgani bo'shliq, uni yozib qo'ying.

## Bot sozlangan, lekin hech narsa joylamaydi

Guvoh ishlayaptimi, bot kanalga post qila oladimi, u kollektor va Bot API'ga yeta oladimi? Uning jurnalida muvaffaqiyatsiz postlarni qidiring. Kollektor tomonidagi so'rov post chiqqanini bildirmaydi.

## GitHub token integratsiyasi qayerda?

**Rejalashtirilgan.** Qo'shimchalar taklif etilayotgan fork va build tasdiqlash ish jarayonini tasvirlaydi. Hozirda GitHub tokeni shakli yoki ishga tushirilgan o'rnatmaning omborga mos kelishini avtomatik tasdiqlovchi hech qanday vosita mavjud emas. [Joriy xususiyat holatini](https://phishdestroy.github.io/TgWitness/uz/docs/reference/features/) ko'ring.

Xato haqida xabar beryapsizmi? Versiya, OT, qadamlar va shaxsiy ma'lumotlari olib tashlangan xato. Hech qachon sessiyalar, tokenlar, shaxsiy xabarlar yoki ma'lumotlar katalogini ommaviy issue'ga qo'ymang.
