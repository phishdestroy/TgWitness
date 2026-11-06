# Telegram · Yashirin suhbatlar: amalga oshirish va demo

Canonical page: https://phishdestroy.github.io/TgWitness/uz/docs/reference/secret-chats/

Alohida Maxfiy Suhbat implementatsiyasini tushunib oling, badiiy interfeysni sinab ko'ring va qoldirilgan nuqsonlarni ko'rib chiqing.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Hujjatlash](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md)

**Holati tekshirilgan 6 Noyabr 2026:** alohida Secret Chat amalga oshirilishi ishlab chiqilmoqda. U e'lon qilingan `main` da `3d23e52b647b`. Oddiy yig'uvchi va Takeout eksporti Maxfiy suhbatlarni yig'maydi. Interaktiv veb-sayt ssenariysi soxta ma'lumotlar bilan interfeysni namoyish etadi; u Telegram muloqotini yoqmaydi.

## Ijro etish joyi

`0e60f88e` qo'shildi **Manbalar → Pseudo-maxfiy** mahalliy rivojlantirish filialida `fix/panel-routes-sessions`. Tekshirilgan snapshot `bb8788fb685c`. Uning amalga oshirilishi `tgwitness/secret_chats.py`, ilova yo'llari, `tgwitness/static/views/secret-chats.js` va maxsus testlarni o'z ichiga oladi.

Ushbu filialdagi ixtiyoriy `secret-chats` qo'shimchasi [KiaroSama/Telethon-Secret-Chat](https://github.com/KiaroSama/Telethon-Secret-Chat) ni `d87bf037b90060383c7b704d8a06ebb98c621c6f` ga bog'laydi. Kutubxona mavjud Telethon ruxsatnomasi asosida Telegramning end-to-end chat protokolini amalga oshiradi. Faqatgina ushbu kutubxonani o'rnatish `main` ga yetishmayotgan integratsiyani qo'shmaydi.

## Rivojlantirish interfeysi nima qiladi

| Harakat | Qayd etilgan xatti-harakatlar |
| --- | --- |
| Foydalanuvchi nomi yoki foydalanuvchi ID bo'yicha suhbatni boshlang | So'rov yuboring; boshqa ishtirokchi uni qabul qilishi kerak. |
| Kiruvchi so'rovni qabul qiling | TgWitness o'sha suhbat uchun qabul qiluvchi nuqta bo'ladi. Avtomatik qabul qilish alohida sozlama bo'lib, standartda o'chirilgan. |
| Xabar yuborish yoki qabul qilish | Chiqish yoki kirish `secret_chat.message` yozuvini qo'shing va uni mavzuda ko'rsating. |
| Ilovani qabul qiling | Uni dekript qiling, baytlarini SHA-256 bo'yicha saqlang va `secret_chat.file` ni qayd eting. |
| Timer yoki o'chirish bildirishnomasini qabul qiling | Ogohlantirishni qayd eting va oldin saqlangan kontentni saqlab qoling. |
| Suhbatni ko'rib chiqing | Xabarlar, fayllar, bildirishnomalar va asosiy vizualizatsiyani ko'rsating. Ochiq yorliq har to'rt soniyada yangilanadi. |

Integratsiyani o'z ichiga olgan rivojlantirish versiyasida operator tanlangan hisob uchun modulni yoqadi va uni ulaydi. Boshlash, qabul qilish va yuborish uchun o'zaro aloqada bo'lish ruxsati hamda hisobning faqat o'qish uchun himoyasi o'chirilgan bo'lishi talab etiladi. Boshqa ishtirokchi yangi chiquvchi suhbatni qabul qilishi kerak. Ushbu nazorat elementlari yuqoridagi reviziyadagi e'lon qilingan ilovada mavjud emas.

Faqat ushbu TgWitness sessiyasi tomonidan yaratilgan yoki qabul qilingan suhbatlar qamrab olinadi. Telefonidagi mavjud Yashirin Suhbatlar shu qurilmada qoladi. Sessiyani import qilish ularning alohida shifrlash kalitlarini taqdim etmaydi. Yashirin suhbat kalit materiallari va hisoblagichlar ish maydoni seyfida saqlanadi; saqlangan xabarlar va dekriptlangan fayllar odatiy ish maydoni saqlash himoyalariga bo'ysunadi.

## Veb-sayt namoyishi

Veb-saytning "**Try Secret Chat**" ssenariysi badiiy suhbatni ochadi. U o'quvchiga so'rov yuborish, uning qabul qilinishini simulyatsiya qilish, namunaviy xabar yuborish, skriptlangan javob va faylni qabul qilish hamda taymer va o'chirish bildirishnomasini ko'rib chiqish imkonini beradi. Kiruvchi so'rov ham qabul qilinishi mumkin. Boshqaruv elementlari simulyatsiya qilingan tengdosh harakatlarini aniq belgilaydi.

Ushbu ssenariy brauzer xotirasida ishlaydi. Qayta tiklash yoki qayta yuklash uni tozalaydi. U tizimga kira olmaydi, Telegram bilan bog'lanmaydi, haqiqiy shifrlash kalitlarini yaratmaydi yoki imzolangan namunalarni yuklab olishni o'zgartirmaydi. Uning ko'rsatilgan xabarlari imzolangan dalil emas. Ssenariy mo'ljallangan o'zaro ta'sirni namoyish etadi; u rivojlantirish amalga oshirilganligi tayyorligini tasdiqlamaydi.

## Tekshiruvlar va hal qilinmagan nuqsonlar

Mavjud beshta test shifrlangan kalit saqlanuvchanligi, hayotiy tsikli va xabar yozuvlari, kiruvchi qabul qilish siyosati, faqat o'qish uchun yuborish va ilova eksportini qamrab oladi. Ular 6-noyabr ko'rigida belgilangan kutubxona bilan muvaffaqiyatli o'tkazildi. Qo'shimcha uchta sintetik tekshiruv shu snapshotda nuqsonlarni qayta ishlab chiqdi:

| Topilma | Oqibat |
| --- | --- |
| Yopilish`read_only`ni chetlab o'tadi | Yopiq yo'l o'zaro ta'sirlar bloklanishi kerak bo'lgan hollarda masofaviy harakatni bajarishi mumkin. |
| Takrorlarni aniqlash faqat so500t yangi yozuvlarni tekshiradi | Eskirgan qayta ijro qayta ishga tushirgandan so'ng nusxa yaratishi mumkin. |
| Muvaffaqiyatsiz ilova yuklab olish uning kutib turgan yozuvini o'chirib tashlaydi | Vaqtinchalik xato qayta urinish ishni yo'qotishga olib keladi. |

Bu ochiq nuqsonlar bo'lib, ular [nashr qilingan auditori](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/REPORT.md)da ham qayd etilgan. Besh muvaffaqiyatli test ushbu xatoliklarni qamrab olmaydi. Ko'rib chiqish sintetik ish maydonchalari va Telegram operatsiyalarining soxta nusxalaridan foydalangan; u jonli qo'l siqishni takrorlamagan yoki ishlab chiqarishga joriy etishni tasdiqlamagan.
