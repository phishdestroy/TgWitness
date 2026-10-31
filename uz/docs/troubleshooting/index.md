# Nima noto'g'ri ketganini aniqlang

Canonical page: https://phishdestroy.github.io/TgWitness/uz/docs/troubleshooting/

Alomatdan boshlang. Har safar bitta qatlamni tekshiring.

## Panel token so'raydi

Ishga tushiruvchi tomonidan ko'rsatilgan mahalliy fayldan panel tokenini ishlating. Docker uchun `docker compose exec tgwitness cat /data/panel-token.txt` buyruqni ishga tushiring. Telegram kirish kodi, BotFather tokeni va faqat o'qish uchun mo'ljallangan guvoh tokeni turli maqsadlarga xizmat qiladi.

## Telegram ulanmaydi

Ulanish sozlamalarini oching va ulanishni tekshirishni ishga tushiring. Agar ommaviy proksi ishlatilsa, boshqa kirish nuqtasini sinab ko'ring va yo'nalishni aniq saqlang. Proksi turini va qo'llab-quvvatlanadigan maxfiy formatni tekshiring. Ommaviy ro'yxatni yangilash hisob yo'nalishini o'zgartirmaydi.

## Ulanish mavjud, lekin yangi xabarlar yo'q

1. Kuzatuv to'g'ri ish maydonida ishlayotganini tekshiring.
2. Manba tanlanganligini va o'sha hisobga ko'rinishini tasdiqlang.
3. Boshqariladigan guruhda noyob yangi xabar yuboring va aynan shu matnni qidiring.
4. Operatsion jurnalni uzilishlar, kechikishlar yoki Telegram xatolari uchun tekshiring.

Tarixiy snapshotlar va yangi xabar voqealari turlicha. Yangi xabarlar hosil qilmasdan jim manbani ulash mumkin. To'liqlik muhim bo'lganda nazoratli yetkazib berish testidan foydalaning.

## FloodWait yoki qayta ishga tushirgandan keyin bo'shliq

FloodWait Telegramga tanaffus kerakligini anglatadi. Ko'rsatilgan muddatni kuting va yig'ish yukini ko'rib chiqing; qayta-qayta ulanish cheklovni bekor qilmaydi. Saqlangan yangilanish holati qayta ishga tushirgandan keyin orqada qolganlarni to'ldirishga yordam beradi, lekin muddati o'tgan yangilanishlar va ba'zi uzilish oynalari cheklov bo'lib qoladi. Jurnalni to'liq deb hisoblash o'rniga bo'shliqni qayd eting.

## Bot sozlangan, lekin hech narsa joylamaydi

Witness jarayonining haqiqatan ishlayotganiga ishonch hosil qiling: bot kanalga post qilishga qodir va witness ma'lumot yig'uvchi hamda Bot API ga ulanishi mumkin. Noto'g'ri nashrlar uchun uning jurnalini tekshiring. Faqat muvaffaqiyatli collector so'rovi kanalga post qilinganini tasdiqlamaydi.

## GitHub token integratsiyasi qayerda?

**Rejalashtirilgan.** Qo'shimchalar taklif etilayotgan fork va build tasdiqlash ish jarayonini tasvirlaydi. Hozirda GitHub tokeni shakli yoki ishga tushirilgan o'rnatmaning omborga mos kelishini avtomatik tasdiqlovchi hech qanday vosita mavjud emas. [Joriy xususiyat holatini](https://phishdestroy.github.io/TgWitness/uz/docs/reference/features/) ko'ring.

Muammoni xabar qilganda versiyani, operatsion tizimni, bajarilgan bosqichlarni va xatolik matnining qizil rangda o'chirilgan nusxasini kiritish kerak. Sessiyalar, tokenlar, shaxsiy xabarlar va ma'lumotlar katalogini ommaviy muammolardan chetda saqlang.
