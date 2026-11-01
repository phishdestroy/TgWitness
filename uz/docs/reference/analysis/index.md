# Arxiv tahlili

Canonical page: https://phishdestroy.github.io/TgWitness/uz/docs/reference/analysis/

Saqlangan xabarlarni qidiring, sun'iy intellekt kirimlarini ko'rib chiqing va manba havolalari bilan analitik hisobotlarni saqlang.

[Ish jarayoni bo'yicha qo'llanma](https://phishdestroy.github.io/TgWitness/docs/archive/) · [Wiki](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

AIsiz mahalliy qidiruv uchun **Jurnal** bo'limidan foydalaning. **Arxivdan so'rang** funksiyasidan foydalanish uchun avval **Integratsiyalar** bo'limida provayderni yoqing va sozlang. Ish maydoni tanlovchisi hisobni tanlaydi; forma chatlar va kuzatuv davrini tanlaydi. Ma'lumotlarni izlab topish mahalliy tarzda bajariladi. Aniq ibora yoki domen izlash doirasini toraytiradi; xabar ID esa saqlangan versiyalarni so'raydi. Parchalarni ko'rib chiqing va ularning jurnal yozuvlari yoki kontekstini oching. Vektor ma'lumotlar bazasi ham, Telegramda avtomatik amallar ham yo'q.

## Provayderlar va rozilik

Har bir ish maydonida sun'iy intellekt o'chirilgan holda boshlanadi. Faqat asosiy administrator model, endpoint, shifrlangan API kaliti, kontekst/chiqish chegaralari, timeout va kunlik so'rov byudjetini sozlay oladi. Kalit hech qachon brauzerga qaytarilmaydi. Joriy kalitni saqlab qolish uchun kalit maydonini bo'sh qoldiring yoki uni aniqlik bilan o'chirib tashlang.

Ollama o'zining hujjatlashtirilgan [`/api/chat` manzilidan](https://docs.ollama.com/api/chat) jonli efirda bo'lmagan JSON chiqish bilan foydalanadi. Uning standart manzili TgWitness serverida `http://127.0.0.1:11434`. Operator uni `TGWITNESS_AI_LOCAL_ENDPOINT` orqali o'zgartirishi mumkin; bu model nazoratidagi manzil emas. Tanlangan modelni o'zingiz o'rnating. TgWitness uni avtomatik yuklamaydi.

Mos keluvchi provayder `/v1` bilan tugaydigan asosiy URL manzilni va [Chat Completions protokoli](https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create): `messages`, JSON javob rejimi, `max_completion_tokens` va `choices[0].message.content` ni kutadi. Ushbu maydonlarga ega bo'lmagan xizmatlar qo'llab-quvvatlanmaydi. Ulanishni sinash sintetik matn yuboradi va so'rov byudjetiga qo'shiladi.

Har bir so'rov ish maydonining sozlangan tashqi yo'lidan foydalanadi. Bloklangan yo'l yoki faqat Telegram MTProxy xato hisoblanadi; to'g'ridan-to'g'ri qayta urinish mavjud emas. Ataylab sozlangan mahalliy Ollama manzili tanlangan yo'ldan foydalangan holda shaxsiy manzilga ruxsat beradi. Boshqa shaxsiy xizmatlar uchun mavjud server darajasidagi shaxsiy manzilga ulanishni tanlash qoidasi amal qiladi. Panel haqiqiy sozlangan yakuniy nuqtani ko'rsatadi.

Generatsiyadan oldin **modelga yuborilgan ma'lumot** so'rovni ko'rsatadi: savol, tekshirilgan parchalar, voqea turlari, kuzatuv vaqtlari va qamrov markerlari. Telegram sessiyalari, xom maydonlar, provayder kalitlari, ilova baytlari va to'liq jurnal ushbu kontekstga kirmaydi. Istalmagan manbalarni belgilashni bekor qiling, so'ng qayta ishlashni aniq tasdiqlang. Tashqi provayderlar taqdim etilgan kontentni o'z siyosatlari doirasida saqlab qolishlari mumkin. Mahalliy ijro degani maqsad nuqtasi mahalliy ekanligini anglatadi; bu mustaqil sozlangan xizmatning xatti-harakatlariga oid kafolat emas.

Butun dunyo bo'ylab bir vaqtning o'zida ko'pi bilan ikki ta provayder so'rovi va har bir ish maydoni bo'yicha bittadan so'rov bo'lishi mumkin. Ko'rinish o'n daqiqadan so'ng amal qilmay qoladi va bitta javob hosil qilishi mumkin. Provayder tomonidan xabar qilingan token sonlari ko'rsatiladi; xarajatlar baholovi faqat kirish va chiqish tariflari sozlanganida paydo bo'ladi. Muvaffaqiyatsiz urinishlar ham kunlik so'rov byudjetini sarf qiladi. Avtomatik qayta urinishlar qo'shimcha byudjet sarflamaydi.

## Manbalar va cheklovlar

Qidirish saqlangan xabar matnini chegaralangan lug'aviy qidiruv yordamida tekshiradi. U 24 tagacha manbani qaytaradi va qisqartirilgan parchalar yoki to'liq bo'lmagan natijalar to'plamini belgilaydi. Bu davr **kuzatuv vaqt**ini anglatadi, Telegram tarixi to'liq ekanligini da'vo qilmaydi. Ish maydoni bo'ylab qamrov voqealari suhbat doirasidagi kirishdan yashiriladi. Yo'qolgan ma'lumotlar mavjud arxivda topilmaganligi bilan tavsiflanadi.

Model hech qanday vositalarni olmaydi. Uning manba IDlari tanlangan yozuvlarga nisbatan aniqlanadi, xeshlar qayta tekshiriladi va iqtibos keltirilgan satrlar shu yozuvlarda mavjud bo'lishi kerak. Noma'lum identifikatorlar, o'zgartirilgan iqtibos belgilari va manbasi ko'rsatilmagan da'volar javobni rad etadi. Ilova havolalar yaratadi; model tomonidan yaratilgan URL manzillar manba sifatida qabul qilinmaydi. Ushbu tekshiruvlar manbaning mavjudligini va iqtibosning aniqligini tasdiqlaydi, xulosaning to'g'riligini emas. Xulosalarga tayanishdan oldin ularni yozuvlarga muvofiq ko'rib chiqing.

## Hisobotlar

Ko'rib chiqilgan javobni alohida tahliliy hisobot sifatida saqlang. U model xulosasi, kuzatilgan xronologiya, olingan havolalar va foydalanuvchi nomlari, tahrirlash/o'chirish yozuvlari, qamrov chegaralari va manba voqealari xeshlarini o'z ichiga oladi. Provayder, model, maqsad nuqtasi, vaqt va so'rov-shablon versiyasi ham unga biriktiriladi. Hech qanday identifikatorlar avtomatik ravishda birlashtirilmaydi.

Tahlilchi tahrirlari va eslatmalari model xulosasidan alohida saqlanadi. Hisobotlar shifrlangan hosil fayllarda, imzolangan voqealar oqimidan tashqaridagi indeks bilan saqlanadi; asl voqealar va media o'zgarmaydi. Faqat egasi yoki ma'muri hisobotni ochishi mumkin va manbaa kirish huquqi qayta tekshiriladi. Yuklab olish uchun shuningdek eksport ruxsati talab etiladi. 1-versiya hisobotlarni imzolamaydi va model xulosalarini tekshirilgan dalil deb hisoblamaydi. Cheklovlar: har bir ish maydoni uchun 100 ta hisobot va har bir hisobot uchun 100 ta tahlilchi tahrirlari.

Qo'lda OCR va transkriptlar uchun [media ishlov berish bo'limiga](https://phishdestroy.github.io/TgWitness/uz/docs/reference/media-analysis/) qarang. Klientga kirish uchun [MCP bo'limiga](https://phishdestroy.github.io/TgWitness/uz/docs/reference/mcp/) qarang.
