# Birinchi sozlash va parametrlar

Canonical page: https://phishdestroy.github.io/TgWitness/uz/docs/reference/settings/

Sozlash ustasi, maqsadlar, interfeys darajalari, ulanish yo&#x27;nalishlari va hisob guruhi bo&#x27;yicha baham ko&#x27;riladigan sozlamalar.

[Hisoblar](https://phishdestroy.github.io/TgWitness/uz/docs/reference/accounts/) · [Ulanish](https://phishdestroy.github.io/TgWitness/uz/docs/reference/connection/) · [Kirish](https://phishdestroy.github.io/TgWitness/uz/docs/reference/access/)

Yangi ish maydoni ochiladi `/first-run`: til va vaqt, interfeys darajasi, maqsad, ulanish, Telegram va suhbatlar. Har bir javob serverda o'zgargach darhol saqlanadi, shuning uchun sahifani yangilash (reload) shu bosqichni davom ettiradi. Oxirgi ekranda javoblar ro'yxati keltirilgan va ularning istalganiga qaytish imkonini beradi.

Til, IANA vaqt zonasiga, tema va daraja har bir operator va har bir ish maydoni bo'yicha saqlanadi. O'rnatilgan qiymatlar brauzer tili, qurilma vaqt zonasi, tizim mavzusi va Oddiy interfeysdir. Tilni o'zgartirish panel sessiyasini saqlab qoladi. Imzolangan jurnal vaqtlari hech qachon o'zgarmaydi.

`/settings` ustuvor yordamchi kabi bir xil yozuvlarni tahrirlaydi. Qidiruv asosiy maydonlar, parametrlar va kengaytirilgan shakllarni qamrab oladi; yashirin maydon darajani o'zgartirmasdan ochilishi mumkin. Darajalar faqat ko'rsatiladigan narsalarni o'zgartiradi: server ruxsatnomalarni mustaqil ravishda tekshiradi. To'plam sozlamalari va birinchi ulanish ish maydoni ma'muri ixtiyoridadir.

| Daraja | Maydonlar | Yon panel |
| --- | --- | --- |
| Oddiy | Faqat eng muhimlari | Bosh sahifa, Suhbatlar, O'zgarishlar, Arxivlar, Sozlamalar |
| Standart | Izohlar bilan umumiy sozlamalar | Case Board, Hisoblar va Kirishni qo'shadi |
| Mutaxassis | Barcha maydonlar, cheklovlar va texnik tafsilotlar | Manbalar, Qo'shimchalar, Arxivga so'rov, Parametrlar, Hisob, Tizim logi va Integratsiyalarni qo'shadi |

[Panel qo'llanmasi](https://phishdestroy.github.io/TgWitness/uz/docs/reference/panel/) har bir bo'limni tasvirlaydi.

## Maqsadlar

| Maqsad | Yig'ma | Fayllar | Tashqi xizmatlar | Server manzili |
| --- | --- | --- | --- | --- |
| Arxiv nusxasi | Off; **Start** eksportni ishga tushiradi | 20 MB gacha fotosuratlar | O'chirilgan | Avtomatik |
| Suhbatlarni kuzatib boring | Uzluksiz | 60 soniyagacha / 20 MBgacha fotosuratlar va videolar | Vaqt tamg'alari va muammo bildirishnomalari | Avtomatik |
| Dalillar | Uzluksiz | 1 GB gacha bo'lgan barcha fayllar | Vaqt tamg'alari, drand, bildirishnomalar | Yo'q, yashir |

Dalil sifatida off-site nusxasi, guvoh bot va kod tekshiruvi tavsiya etiladi. Saqlash va bildirishnoma manzillari avvalo manzilga muhtoj. Tashqi xizmat bilan muloqot qiluvchi funksiya Telegram tashqarisidagi so'rovlarni ruxsat etishni so'raydi; uni o'chirish vaqt tamg'alarini, bildirishnomalarni va off-site nusxasini ham o'chirishni taklif etadi.

Maqsadni o'zgartirish avvalo farqni ko'rsatadi va qo'lda kiritilgan o'zgartirishlar saqlanishi mumkin. Maqsaddan farq qiladigan maydon "**Siz tomonidan o'zgartirilgan**" deb belgilangan bo'lib, uni tiklash mumkin. Sozlamalar versiyalari boshqa yorliqda kiritilgan o'zgartirish ustidan ko'rib chiqilgan farqni qo'llanilishiga yo'l qo'ymaydi.

## Ulanish

**Automatic** avvalo ommaviy MTProxy serverlarini, keyin WARPni, so'ngra to'g'ridan-to'g'ri ulanishni sinab ko'radi; oxirgisi faqat server manzili ko'rsatilishi mumkin bo'lgan holatda ishlatiladi. Automatic va WARP hash-nazorat qilingan komponentlarni o'rnatishi va serverni Cloudflare'da ro'yxatdan o'tkazishi mumkin. WARP mavjud wgcf/wireproxy menejeri va mahalliy SOCKS5 portidan foydalanadi; tizim marshrutlash jadvali o'zgarmaydi. Tashqi xizmatlar kerak bo'lganda, Automatic MTProxy o'rniga WARPni afzal ko'radi.

Sizning o'zingizning proksingiz qabul qiladi `tg://proxy`, `socks5://`, `http://` va `https://`. HTTPS proksi sertifikati foydalanuvchi ma'lumotlari unga yuborilishidan oldin tekshiriladi.

Ulanishni tekshirish besh daqiqa davom etadi va marshrut, siyosat hamda ustama javoblariga bog'langan; ulardan birini o'zgartirish yangi tekshiruvni talab qiladi. **Tekshirmasdan davom etish** mumkin va bu Telegramga kirishni almashtirmaydi. Tanlangan marshrut fon rejimida qayta tekshiriladi, va ulanish yo'qolgach Automatic o'z zanjirini yana ishga tushiradi. Jamoat proksi javob bermasa, hisob WARP bilan qizil rangga o'tadi va qayta tekshirish harakatlari paydo bo'ladi.

## Hisob guruhlari

Guruhdagi hisoblar o'z sozlamalarini baham ko'radi. **Hisoblar → Guruhlar va umumiy sozlamalar → Umumiy sozlamalar** yoki hisobning Sozlamalar sahifasida **Guruh sozlamalari bo'limini** oching.

Guruh maqsad, saqlangan fayllar, vaqt tamg'alari, drand, muammo bildirishnomalari, ofis tashqarisidagi nusxa, Telegram tashqarisidagi so'rovlar, IP rejim, nima yozib olish, qayta tekshirish jadval, bildirishnoma qoidalari, hisobot sozlamalari, parametrlar va ulanish yo'nalishini baham ko'radi. Bildirishnoma manzillari, proksi ma'lumotlari va tizimga kirish har bir hisob uchun alohida saqlanadi, shuningdek yozib olishni boshlash va to'xtatish ham alohida hisobda amalga oshiriladi.

- Har bir a'zo guruhni kuzatadi. Sozlamalar qiymatni belgilaydi 🔗 **Guruhdan** yoki ✏️ **O'z qiymati**; **Guruh qiymatiga qaytish** uni qaytaradi.
- O'zgarish ta'sir qiladigan hisoblarni ro'yxatlaydi (**3 ta hisobdan 2 tasiga tegishli**) va o'z qiymatini almashtirishdan oldin har bir hisob bo'yicha alohida so'raydi. Belgilanmagan hisoblar o'z qiymatlarini saqlab qoladi.
- Guruh bo'lishmaydigan parametr **Ular baham ko'rilmaydi: har bir hisob o'z qiymatini alohida saqlaydi** bo'lib qoladi, siz **Ushbu qiymatni ulashing** tugmasini bosmaguningizcha.
- **Bir hisobdan sozlamalarni nusxalashda** tanlangan hisobning qiymatlari guruh sozlamalari sifatida qabul qilinadi.
- Guruhga ko'chirilgan hisobdan so'raladi: **guruh qiymatlarini olasizmi?** Aks holda u o'z qiymatlarini saqlaydi, ✏️ bilan belgilangan. Keyinchalik qo'shilgan hisoblar guruh qiymatlari bilan boshlanadi.
- Kuzatuvchi hisob IP-rejasini pauza qilinguncha saqlaydi.

Har bir o'zgarish asosiy ish maydonchasining va unga tegishli bo'lgan har bir a'zoning imzolangan jurnalida qayd etiladi. Guruhni o'chirish uning hisoblarini va ularning joriy qiymatlarini saqlab qoladi.

Guruh sahifasi `/groups/<id>` a'zolarni, e'tibor talab qiladigan masalalarni va bir nechta hisoblar ko'radigan suhbatlarni ko'rsatadi. [Hisob guruhlariga](https://phishdestroy.github.io/TgWitness/uz/docs/reference/accounts/#bulk-import-and-account-groups) qarang.

## Mavjud ish maydonchalari

Sessiya yoki ilgari yakunlangan sozlama mavjud bo'lgan ish maydoni ustuvorlik yordamchisini ko'rmaydi. Sahifa yuklanganda uning qiymatlari maqsad bilan almashtirilmaydi. Maydonni yashirish funksiyani o'chirib qo'ymaydi yoki uning qiymatini o'chirib tashlamaydi.

O'lcham va vaqt baholovi uchta tanlangan suhbatni va har biridan 20 tagacha xabarni o'qiydi. Bu faqat taxmindir: u Telegram limitlarini, ma'lum bir server tezligini yoki har bir suhbatdagi fayllarni oldindan aytib bera olmaydi.

```
python tools/test_settings_hub.py
python tools/test_group_settings.py
python tools/check_group_settings_browser.py
python tools/check_first_run.py
```
