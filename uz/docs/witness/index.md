# Witness botini sozlang

Canonical page: https://phishdestroy.github.io/TgWitness/uz/docs/witness/

Alohida jarayon jurnalingizni tekshiradi va imzolangan nazorat nuqtalarini kanalga joylaydi.

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

BotFather bilan bot yarating va unga kanalingizda post qilishga ruxsat bering. Guvohni boshqa joyda ishga tushiring: boshqa xost, iloji bo'lsa boshqa kishi boshqaradigan, kollektor yonidagi ikkinchi jarayondan ancha qimmatli.

## Extras bo'limida uchta qadam

1. **Faqat o'qish uchun kirish.** **Qo'shimchalar → Mustaqil guvoh**, token yarating, faylni saqlang. U faqat nazorat nuqtalari va holatni o'qiydi.
2. **Kanal va interval.** Telegram kanali yoki Discord webhook'i, shuningdek guvoh yeta oladigan kollektor manzili. Sozlamalar faylini saqlang.
3. **Ishga tushirish.** `witness.json`, `witness-token.txt` va `bot-token.txt` ni guvoh xostiga birga joylashtiring va ishga tushiring:

```
python -m tgwitness.witness run --config witness.json --check-config
python -m tgwitness.witness run --config witness.json
```

Kanalda birinchi imzolangan post chiqishini kuting, so'ng guvoh barmoq izini xavfsiz joyda saqlang.

Uning o'rniga Discord? Webhook URL'ini `discord-webhook.txt` sifatida saqlang. Bitta guvoh bitta joyga post qiladi; uzun tekshiruvlar Discord'ga fayl sifatida keladi.

## Nashr etish chastotasini tanlang

Har bir tekshiruvni post qilish muntazam tashqi yozuv beradi: har besh daqiqada bu har bir ish maydoni uchun kuniga taxminan 288 ta post. Kengaytirilgan sozlamalar faqat o'zgarish yoki muammo bo'lganda post qilishi, proksi yoki maxsus Bot API ishlatishi mumkin.

**Bot aslida nimani tasdiqlaydi?**

U kollektordan imzolangan nazorat nuqtasini so'raydi, uni kutilgan kalit bilan tekshiradi va o'z imzolangan jurnalini, o'tkazib yuborilgan va rad etilgan javoblar bilan birga, saqlaydi.

U jurnal holatini tekshiradi, Telegram'ning o'zini kuzatmaydi. Buning uchun nazorat ostidagi yetkazish sinovini o'tkazing.

## Dalillarni keyin tekshiring

Guvoh jurnali, postlar va barmoq izlarini saqlang. Kollektor eksportiga nisbatan [ularni qanday tekshirish](https://phishdestroy.github.io/TgWitness/uz/docs/reference/witness/#verify).
