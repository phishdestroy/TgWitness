# Arxiv bilan ishlash

Canonical page: https://phishdestroy.github.io/TgWitness/uz/docs/archive/

Xabarni toping. Manbani tekshiring. Ishni tuzing.

01**Tarixni olib keling**

Yoqilgan manbalarning o'tgan xabarlarini ish maydoniga torting.

02**Manbalarga rioya qiling**

Qidiring, so'ng har bir natija ortidagi saqlangan xabarni oching.

03**Topshirishni aniq saqlang**

Tahlilingiz bitta faylda, imzolangan dalil yonida.

Yozib olingan yozuvlar, tan olingan matn va tahlilchi xulosalari alohida saqlanadi.

## Avvalgi xabarlarni yuklash

1. **Manbalar → Qamrovdagi chatlar**: yoqilgan chatlarni tekshiring, kuzatuvni boshlang.
2. **To'liq tarixni yuklash**. U manbalar ro'yxatini hozir qanday bo'lsa, shunday oladi.
3. **Tarixni to'xtatish** / **Tarixni davom ettirish** istalgan vaqtda. Qayta ishga tushirgandan keyin qo'lda davom ettiring.
4. Har bir manba natijalarini va yuklab olish navbatini tekshiring, imzolangan jarayon hisobotini eksport bilan birga saqlang.

Bu ish maydonini to'ldiradi. Bitta chatning HTML/JSON eksporti boshqa narsa. [Batafsil](https://phishdestroy.github.io/TgWitness/uz/docs/reference/history/).

## Avvalo qidiring, keyin sun'iy intellekt haqida qaror qiling

1. **Jurnal** mahalliy qidiradi, manba va vaqt bo'yicha filtrlang.
2. Ibora yoki domenni qidiring, yozuv va uning versiyalarini oching.
3. AI uchun administrator **Integratsiyalar** bo'limida provayderni sozlaydi. So'ng **Arxivdan so'rang**: chatlar va davrni tanlang, **Modelga yuborilgan ma'lumotlar**ni ko'ring va tashqariga chiqmasligi kerak bo'lganlarning belgisini olib tashlang.
4. Iqtiboslarni tekshiring, javobni hisobot sifatida saqlang, eslatmalaringizni qo'shing.

Qidiruv uchun AI shart emas. Hisobotlar o'z manbalari va tahrirlarini imzolangan jurnaldan alohida saqlaydi. [Provayderni sozlash](https://phishdestroy.github.io/TgWitness/uz/docs/reference/analysis/).

## Sizga kerakli ulanishni tanlang

| Vazifa | Ochiq | Sozlash |
| --- | --- | --- |
| AI mijoziga tanlangan chatlarni o'qishga ruxsat bering | **Integratsiyalar → MCP** | [MCP'ni o'rnating, cheklangan token yarating, ulaning](https://phishdestroy.github.io/TgWitness/uz/docs/reference/mcp/) |
| Saqlangan mediadagi matnni aniqlash | `media.saved` yozuvi → **Ilovani tan olish** | [Mahalliy Docker worker'ni sozlang](https://phishdestroy.github.io/TgWitness/uz/docs/reference/media-analysis/) |
| Voqealarni n8n yoki SIEMga yuboring | **Integratsiyalar → Chiqish webhooklari** | [Qabul qiluvchi qo'shing, HMAC'ni tekshiring, takroriy ID'larni olib tashlang](https://phishdestroy.github.io/TgWitness/uz/docs/reference/webhooks/) |

**Qaysi access token qayerga qo'yiladi?**

Panelga kirish odamlar uchun. MCP'ning o'z faqat o'qish tokenlari, webhook'larning o'z HMAC siri bor. Hech biriga Telegram sessiyasi kerak emas.

[Panelga kirishni ulashing](https://phishdestroy.github.io/TgWitness/uz/docs/access/) yoki [MCP-klientni sozlang](https://phishdestroy.github.io/TgWitness/uz/docs/reference/mcp/).

## Manbalar va xulosalarni taqdim eting

Hisobotni imzolangan ZIP yoniga qo'ying. Hisobot manbalarni sizning talqiningiz, ZIP esa qabul qiluvchi tekshiradigan narsa.

[Eksport va tekshirish](https://phishdestroy.github.io/TgWitness/uz/docs/exports/) · [To'liq tergovni bosqichma-bosqich o'tkazing](https://phishdestroy.github.io/TgWitness/uz/docs/cases/)
