# Arxiv tahlili

Canonical page: https://phishdestroy.github.io/TgWitness/uz/docs/reference/analysis/

Saqlangan xabarlarni qidiring, sun'iy intellekt kirimlarini ko'rib chiqing va manba havolalari bilan analitik hisobotlarni saqlang.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Hujjatlash](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Tergov](https://phishdestroy.github.io/TgWitness/uz/docs/reference/investigation/)

![Tergov](https://phishdestroy.github.io/TgWitness/assets/chapter-investigate.svg)

[Ish jarayoni bo'yicha qo'llanma](https://phishdestroy.github.io/TgWitness/docs/archive/) · [Wiki](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

AI ishtirokisiz mahalliy qidiruv uchun **Journal-**dan foydalaning; [to'liq matnli qidiruv](https://phishdestroy.github.io/TgWitness/uz/docs/reference/search/) (oldindan ko'rish) so'z shakllari, iboralar, domenlar va @foydalanuvchi nomlarini mos keltiradi. **Ask arxivi** uchun avvalo **Integrations** bo'limida provayderni yoqib, sozlang. Ish maydoni tanlovchisi hisobni, forma esa suhbatlar va kuzatuv davrini tanlaydi. Ma'lumotlarni tiklash mahalliy tarzda ishlaydi. Aniq ibora yoki domen qidiruvni toraytiradi; xabar ID saqlangan versiyalarni so'raydi. Parçalarni ko'rib chiqing va ularning jurnal yozuvlari yoki kontekstini oching. Vektor ma'lumotlar bazasi yoki avtomatik Telegram harakati mavjud emas.

## Provayderlar va rozilik

Har bir ish maydonida sun'iy intellekt o'chirilgan holda boshlanadi. Faqat asosiy administrator model, endpoint, shifrlangan API kaliti, kontekst/chiqish chegaralari, timeout va kunlik so'rov byudjetini sozlay oladi. Kalit hech qachon brauzerga qaytarilmaydi. Joriy kalitni saqlab qolish uchun kalit maydonini bo'sh qoldiring yoki uni aniqlik bilan o'chirib tashlang.

Ollama o'zining hujjatlashtirilgan [`/api/chat` manzilidan](https://docs.ollama.com/api/chat) jonli efirda bo'lmagan JSON chiqish bilan foydalanadi. Uning standart manzili TgWitness serverida `http://127.0.0.1:11434`. Operator uni `TGWITNESS_AI_LOCAL_ENDPOINT` orqali o'zgartirishi mumkin; bu model nazoratidagi manzil emas. Tanlangan modelni o'zingiz o'rnating. TgWitness uni avtomatik yuklamaydi.

Mos keluvchi provayder `/v1` bilan tugaydigan asosiy URL manzilni va [Chat Completions protokoli](https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create): `messages`, JSON javob rejimi, `max_completion_tokens` va `choices[0].message.content` ni kutadi. Ushbu maydonlarga ega bo'lmagan xizmatlar qo'llab-quvvatlanmaydi. Ulanishni sinash sintetik matn yuboradi va so'rov byudjetiga qo'shiladi.

Har bir so'rov ish maydonining sozlangan tashqi yo'lidan foydalanadi. Bloklangan yo'l yoki faqat Telegram MTProxy xato hisoblanadi; to'g'ridan-to'g'ri qayta urinish mavjud emas. Ataylab sozlangan mahalliy Ollama manzili xususiy manzilga ruxsat beradi. Loopback AI manzili ish maydonining To'g'ridan-to'g'ri tashqi yo'lidan foydalanishni talab qiladi; proxy yo'llari uzatishdan oldin rad etiladi. Boshqa xususiy xizmatlar uchun mavjud server darajasidagi xususiy manzilga ruxsat berish qoidasi amal qiladi. Ko'rinish manzil va tashqi yo'lni, zarur bo'lganda proxy mezbonini ham ko'rsatadi. Ushbu yo'lni o'zgartirish yangi ko'rinishni talab qiladi.

Generatsiyadan oldin **modelga yuborilgan ma'lumot** so'rovni ko'rsatadi: savol, tekshirilgan parchalar, voqea turlari, kuzatuv vaqtlari va qamrov markerlari. Telegram sessiyalari, xom maydonlar, provayder kalitlari, ilova baytlari va to'liq jurnal ushbu kontekstga kirmaydi. Istalmagan manbalarni belgilashni bekor qiling, so'ng qayta ishlashni aniq tasdiqlang. Tashqi provayderlar taqdim etilgan kontentni o'z siyosatlari doirasida saqlab qolishlari mumkin. Mahalliy ijro degani maqsad nuqtasi mahalliy ekanligini anglatadi; bu mustaqil sozlangan xizmatning xatti-harakatlariga oid kafolat emas.

Butun dunyo bo'ylab bir vaqtning o'zida ko'pi bilan ikki ta provayder so'rovi va har bir ish maydoni bo'yicha bittadan so'rov bo'lishi mumkin. Ko'rinish o'n daqiqadan so'ng amal qilmay qoladi va bitta javob hosil qilishi mumkin. Provayder tomonidan xabar qilingan token sonlari ko'rsatiladi; xarajatlar baholovi faqat kirish va chiqish tariflari sozlanganida paydo bo'ladi. Muvaffaqiyatsiz urinishlar ham kunlik so'rov byudjetini sarf qiladi. Avtomatik qayta urinishlar qo'shimcha byudjet sarflamaydi.

## Manbalar va cheklovlar

Ma'lumotni tiklash to'liq tugagach, [to'liq matn ind](https://phishdestroy.github.io/TgWitness/uz/docs/reference/search/#ask-the-archive-and-mcp)eksidan foydalanadi: tanlangan suhbatlar bo'ylab so'z shakllari bilan eng yaxshi mosliklar. Yaqinda bo'lgan o'zgarishlar yoki bir xabarning versiyalari haqidagi savollar va indeks tuzilayotgan paytdagi qidiruvlar eng yangi yozuvlarning chegaralangan leksikal qidiruvidan foydalanadi. Oldindan ko'rish usulni nomlaydi. Ma'lumotni tiklash 24 tagacha manbani qaytaradi; uzun matnlar mos kelgan joyda qisqartiriladi. Kesilgan parchalar va to'liq bo'lmagan natija to'plamlari belgilab qo'yiladi. Davr **kuzatuv vaqti** ga ishora qiladi, Telegram tarixi to'liq degan da'vo emas. Ish maydoni bo'ylab qamrov voqealari suhbat doirasidagi kirishdan yashiriladi. Yo'qolgan ma'lumotlar mavjud arxivda topilmagan deb ta'riflanadi.

Model hech qanday vositalarni olmaydi. Uning manba IDlari tanlangan yozuvlarga nisbatan aniqlanadi, xeshlar qayta tekshiriladi va iqtibos keltirilgan satrlar shu yozuvlarda mavjud bo'lishi kerak. Noma'lum identifikatorlar, o'zgartirilgan iqtibos belgilari va manbasi ko'rsatilmagan da'volar javobni rad etadi. Ilova havolalar yaratadi; model tomonidan yaratilgan URL manzillar manba sifatida qabul qilinmaydi. Ushbu tekshiruvlar manbaning mavjudligini va iqtibosning aniqligini tasdiqlaydi, xulosaning to'g'riligini emas. Xulosalarga tayanishdan oldin ularni yozuvlarga muvofiq ko'rib chiqing.

## Hisobotlar

Ko'rib chiqilgan javobni alohida tahliliy hisobot sifatida saqlang. U model xulosasi, kuzatilgan xronologiya, olingan havolalar va foydalanuvchi nomlari, tahrirlash/o'chirish yozuvlari, qamrov chegaralari va manba voqealari xeshlarini o'z ichiga oladi. Provayder, model, maqsad nuqtasi, vaqt va so'rov-shablon versiyasi ham unga biriktiriladi. Hech qanday identifikatorlar avtomatik ravishda birlashtirilmaydi.

Tahlilchi tahrirlari va eslatmalari model xulosasidan alohida saqlanadi. Hisobotlar shifrlangan hosil fayllarda, imzolangan voqealar oqimidan tashqaridagi indeks bilan saqlanadi; asl voqealar va media o'zgarmaydi. Faqat egasi yoki ma'muri hisobotni ochishi mumkin va manbaa kirish huquqi qayta tekshiriladi. Yuklab olish uchun shuningdek eksport ruxsati talab etiladi. 1-versiya hisobotlarni imzolamaydi va model xulosalarini tekshirilgan dalil deb hisoblamaydi. Cheklovlar: har bir ish maydoni uchun 100 ta hisobot va har bir hisobot uchun 100 ta tahlilchi tahrirlari.

Qo'lda OCR va transkriptlar uchun [media ishlov berish bo'limiga](https://phishdestroy.github.io/TgWitness/uz/docs/reference/media-analysis/) qarang. Klientga kirish uchun [MCP bo'limiga](https://phishdestroy.github.io/TgWitness/uz/docs/reference/mcp/) qarang.
