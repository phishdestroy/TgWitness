# Witness botini sozlang

Canonical page: https://phishdestroy.github.io/TgWitness/uz/docs/witness/

Alohida jarayon jurnalni tekshirsin va imzolangan tekshiruv nuqtalarini kanalingizga e'lon qilsin.

## Ikki mezbon, ikki imzolash kaliti

MEZBON / YIĂUVCHI**Hisob + jurnal**

Telegram sessiyasi Collector imzolash kaliti

Faqat o'qish uchun mo'ljallangan tekshiruv nuqtasi oxiri

← imzolangan javobni so'rash →

MEZBON B / GUVOH**Tasdiqlash + saqlash**

Biriktirilgan yig'uvchi barmoq izi Alohida guvoh imzolash kaliti

O'z jurnali + bot tokeni

Witness → Telegram Bot API →**Sizning kanalingiz · imzolangan TGW1 postlari**

Witness o'zi tekshiruvlarni bajaradi. Collector foydalanuvchisiga faqat o'qish huquqi berilgan. Bot nashriyoti witnessning ulanishidan va tokenidan foydalanadi; witnessga hech qanday hisob sessiyasi berilmaydi.

03 / CHECKPOINT QARORLARIIllyustrativ javoblar

Oxirgi qabul qilingan**120 yozuv**`head 9c7d…`

KEYINGI JAVOB**128 yozuv**`head a4f2…`

Qabul qilindi: hisob ortadi, imzo tasdiqlanadi va kalit mos keladi. Guvoh ushbu yangi chegarani saqlab qoladi.

Barcha javob misollari haqiqiy imzo va biriktirilgan kalitni taxmin qiladi. Bu yerda xeshlar qisqartirilgan misollar bo'lib, faqat ko'proq son butun eski prefiks o'zgarmaganligini isbotlay olmaydi; saqlangan tekshiruv nuqtalariga ega eksportni solishtiring.

## Bot va kanal tayyorlang

BotFather yordamida bot yarating va uni o'zingiz nazorat qiladigan kanalga post qilishga ruxsat bering. Guvoh uchun kompyuter yoki server tanlang. Alohida host va operator kollektor serveridagi ikkinchi jarayondan ko'ra kuchliroq mustaqillikni ta'minlaydi.

## Extras bo'limida uchta qadam

1. **Faqat o'qish huquqi bilan.** Open **Extras → Kanalga bot qo'shib**, guvoh tokenini yarating va kirish faylini saqlang. Bu tekshiruv nuqtalari va holatni o'qishga imkon beradi, suhbatlar yoki yig'uvchi boshqaruvlarini emas.
2. **Kanal va intervallar.** Kanalni va guvohdan erishiladigan kollektor manzilini kiriting. Sozlamalar faylini saqlang.
3. **Boshlash.** Witness hostida yaratilgan `witness.json`, `witness-token.txt` va `bot-token.txt` ni birga joylashtiring. O'rnatilgan loyiha muhitida quyidagi buyruqlarni ijro eting.

```
python -m tgwitness.witness run --config witness.json --check-config
python -m tgwitness.witness run --config witness.json
```

Fayllarni yuklab olish witness dasturini ishga tushirmaydi. Kanalda birinchi imzolangan post paydo bo'lishini tekshiring, so'ngra guvohning jamoat kaliti barmoq izini alohida saqlang.

## Nashr etish chastotasini tanlang

Har bir tekshiruvni e'lon qilish muntazam tashqi yozuvni yaratadi. Har besh daqiqada, bu kuniga har bir ish maydoni uchun taxminan 288 ta postga to'g'ri keladi. Kengaytirilgan sozlamalar o'zgarishlar yoki muammolar bo'lganda e'lon qilish, proksi va maxsus Bot API manzilini ham taklif etadi.

**Bot aslida nimani tasdiqlaydi?**

Guvoҳ yig'uvchidan imzolangan tekshiruv nuqtasini so'raydi, uni kutilayotgan kalitga qarshi tekshiradi va alohida imzolangan jurnalni saqlaydi. U yo'qolgan javoblar va rad etilgan javoblarni, shuningdek muvaffaqiyatli tekshiruvlarni qayd etadi. Nashr guvoҳ Telegram Bot APIga ulanib, uni ishga tushirishiga bog'liq bo'lib qoladi.

U yig'uvchining xabar bergan jurnal holatini tekshiradi. U har bir Telegram xabarini mustaqil ravishda kuzatmaydi. Buning uchun nazorat ostidagi yetkazib berish testini qo'shing.

## Dalillarni keyin tekshiring

Guvoxlik jurnalini, kanal postlarini va mustaqil saqlangan barmoq izlarini saqlang. [To'liq tekshirish protsedurasi](https://phishdestroy.github.io/TgWitness/uz/docs/reference/witness/#verify) ularni yig'uvchining imzolangan eksporti bilan solishtiradi.
