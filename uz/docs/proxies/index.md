# Telegram · Proxy tanlang

Canonical page: https://phishdestroy.github.io/TgWitness/uz/docs/proxies/

Hisobni onlayn saqlang va server IP'sini ko'rsatishi mumkinmi yoki yo'qmi, o'zingiz hal qiling.

## Avvalo IP rejimini tanlang

01**Manishani yashirish**

Faqat proksi. Hech biri ishlamasa, kutadi.

02**Oxirgi chora sifatida to'g'ridan-to'g'ri**

Kechikishdan keyin to'g'ridan-to'g'ri ulanadi, biror proksi ishlashi bilan unga qaytadi.

03**Tunnel yoki VPN ortidagi server**

To'g'ridan-to'g'ri ulanish mumkin. U siz uchun VPN'ni sozlamaydi va tekshirmaydi.

Yo'l ulanishni tanlaydi. IP rejimi to'g'ridan-to'g'ri ulanishga ruxsat berilishini aniqlaydi.

## Pool marshrutni saqlab tursin

1. **Hisob → Sozlamalar → Ulanish sozlamalari**.
2. IP rejimini va **Avtomatik MTProxy**ni yoki qat'iy marshrutni tanlang.
3. Saqlang, **Telegram ulanishini sinash** (kirishdan oldin ham ishlaydi).
4. Yig'ishni boshlang va o'zingizga sinov xabari yuboring.

Yangi ish maydonlari avtomatik MTProxy va **Manzilni yashirish** bilan boshlanadi. Pul to'rtta ochiq ro'yxatni oladi, serverlarni tekshiradi, yaxshilarini saqlaydi va o'liklarini almashtiradi.

## O'zingizning proksingizdan foydalaning

SOCKS5, HTTP CONNECT, Telegram proksi havolasi yoki operator katalogi. Almashtirishdan oldin kuzatuvni to'xtating. Fake TLS sirlari (`ee`…) ishlamaydi.

**Aylantirish, ulashish va qayta urinish sozlamalari**

**Parametrlar → Avtomatik MTProxy**: xato chegaralari, tanaffuslar, aylanish, har bir proksiga hisoblar. Cheklov 1 hisob ulashish o'rniga kutishini bildiradi. Turli proksilar baribir bitta chiqish IP'sini bo'lishishi mumkin.

## Telegramni tashqi so'rovlardan ajratish

MTProxy faqat Telegram'ni tashiydi. Vaqt belgilari, bildirishnomalar, nusxalar va kod tekshiruvlari alohida SOCKS5/HTTP proksi, hisobning SOCKS5/HTTP marshruti yoki rejim ruxsat bersa to'g'ridan-to'g'ri o'tadi. Yoki ularni o'chiring.

`TGWITNESS_PROXY_FEED_PROXY` ro'yxatlarni yuklab olish marshrutini belgilaydi. [Guvoh](https://phishdestroy.github.io/TgWitness/uz/docs/witness/)ning o'z sozlamalari bor. Bularning hech biri brauzeringiz yoki tizim tarmog'ingizga tegmaydi.

Batafsil: [rejimlar va standart qiymatlar](https://phishdestroy.github.io/TgWitness/uz/docs/reference/connection/#ip-modes), [marshrutlarni kim o'zgartira oladi](https://phishdestroy.github.io/TgWitness/uz/docs/access/).
