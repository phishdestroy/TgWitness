# Arxiv bilan ishlash

Canonical page: https://phishdestroy.github.io/TgWitness/uz/docs/archive/

Xabarni toping. Manbani tekshiring. Ishni tuzing.

01**Tarixni olib keling**

Faollashtirilgan manbalaringizdan avvalgi xabarlarni ish maydoniga yuklang.

02**Manbalarga rioya qiling**

Arxivni qidiring va har bir natija ortidagi saqlangan xabarni oching.

03**Topshirishni aniq saqlang**

Tahlilingizni alohida saqlang va imzolangan dalillarni uning yoniga eksport qiling.

Yozib olingan yozuvlar, tan olingan matn va tahlilchi xulosalari alohida saqlanadi.

## Avvalgi xabarlarni yuklash

1. **Manbalar → Qamrovdagi chatlar** bo'limini oching, yoqilgan chatlarni ko'rib chiqing va kuzatuvni boshlang.
2. **To'liq tarixni yuklashni** tanlang. Jarayon o'sha paytda tanlangan manba ro'yxatidan foydalanadi.
3. Zarur bo'lganda "**Pause history"** va "**Continue history" funksiyalaridan** foydalaning. Qayta ishga tushirgandan so'ng, davom ettirishni aniq ko'rsatib amalga oshiring.
4. Har bir manba bo'yicha natija va ilovalar navbatini tekshiring. Dalillar eksporti bilan imzolangan ish jarayoni hisobotini saqlang.

Bu ish maydonini mavjud xabarlardan to'ldiradi. Sohbet bo'yicha HTML/JSON eksporti alohida amaliyotdir. [Tarix va tiklash tafsilotlari](https://phishdestroy.github.io/TgWitness/uz/docs/reference/history/).

## Avvalo qidiring, keyin sun'iy intellekt haqida qaror qiling

1. Mahalliy qidiruv uchun **Jurnal** bo'limini oching. Ish maydonini tanlang va manba hamda vaqt filtrlaridan foydalaning.
2. Iborani yoki domenni qidiring. Mos keladigan yozuvni va uning saqlangan versiyalarini oching.
3. AI tahlili uchun administrator **Integratsiyalar** bo'limida provayderni yoqadi va sozlaydi. **Arxivdan so'rang** bo'limini oching hamda chatlar va davrni tanlang. So'rovni tasdiqlashdan oldin **Modelga yuborilgan ma'lumotlar** bo'limini ko'rib chiqing va keraksiz parchalardan belgini olib tashlang.
4. Qaytarilgan manbalarni tekshiring. Javobni hisobot sifatida saqlang va o'zingizning tahriringiz yoki izohlaringizni qo'shing.

Qidiruv mahalliy tarzda, sun'iy intellektisiz amalga oshiriladi. Analitik hisobotlar manba havolalari va tahrir tarixini saqlaydi; ular imzolangan jurnalga alohida. [Provayderni sozlash va hisobotlar](https://phishdestroy.github.io/TgWitness/uz/docs/reference/analysis/).

## Sizga kerakli ulanishni tanlang

| Vazifa | Ochiq | Sozlash |
| --- | --- | --- |
| AI mijozidan tanlangan suhbatlarni o'qing | **Integratsiyalar → MCP** | [MCP extra-ni o'rnating, scoped token chiqaring va mijozni ulang](https://phishdestroy.github.io/TgWitness/uz/docs/reference/mcp/) |
| Saqlangan mediadagi matnni aniqlash | `media.saved` yozuvi → **Ilovani tan olish** | [Mahalliy Docker ishchisini va zarur til/model fayllarini sozlang](https://phishdestroy.github.io/TgWitness/uz/docs/reference/media-analysis/) |
| Voqealarni n8n yoki SIEMga yuboring | **Integratsiyalar → Chiqish webhooklari** | [Qabul qiluvchini qo'shing, HMACni tasdiqlang va voqea IDlarini takrorlanishdan tozalang](https://phishdestroy.github.io/TgWitness/uz/docs/reference/webhooks/) |

**Qaysi access token qayerga qo'yiladi?**

Panelga kirish ishini ko'rib chiqayotgan shaxslar uchun mo'ljallangan. MCP ulanishlari alohida faqat o'qish huquqiga ega arxiv tokenlarini oladi. Webhook qabul qiluvchisi o'zining HMAC siridan foydalanadi. Hech kimga Telegram sessiya fayli kerak emas.

[Panelga kirishni ulashing](https://phishdestroy.github.io/TgWitness/uz/docs/access/) yoki [MCP-klientni sozlang](https://phishdestroy.github.io/TgWitness/uz/docs/reference/mcp/).

## Manbalar va xulosalarni taqdim eting

Ko'rib chiqilgan tahliliy hisobotni imzolangan dalillar ZIP-fayli bilan birga saqlang. Hisobot sizning manbalarni qanday tushunganingizni tushuntiradi; ZIP-fayl esa qabul qiluvchiga saqlangan yozuvni mustaqil ishonchli barmoq izi va tekshirish nuqtasi bilan solishtirib tekshirish imkonini beradi.

[Eksport va tekshirish](https://phishdestroy.github.io/TgWitness/uz/docs/exports/) · [To'liq tergovni bosqichma-bosqich o'tkazing](https://phishdestroy.github.io/TgWitness/uz/docs/cases/)
