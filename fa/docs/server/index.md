# Telegram · آن را در حال اجرا نگه دارید

Canonical page: https://phishdestroy.github.io/TgWitness/fa/docs/server/

جمع‌کننده را روشن و داده‌ها را در راه‌اندازی‌های مجدد امن نگه دارید.

## روش راه‌اندازی را انتخاب کنید

نصب بومی: [راه‌انداز](https://phishdestroy.github.io/TgWitness/fa/docs/start/) به‌علاوه قالب‌های سرویس در [deploy/](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md). Docker، از پوشه پروژه:

```
docker compose up -d --build --wait
docker compose exec tgwitness cat /data/panel-token.txt
```

پنل روی localhost:8787 گوش می‌دهد. آن را محلی یا از طریق تونل SSH باز کنید، با توکن فرمان دوم.

## تمام دایرکتوری داده‌ها را حفظ کنید

نصب بومی: `data/live`. Docker: حجم `tgwitness-data`. ژورنال‌ها، نشست‌ها و کلیدها باید کنار هم باشند. خروجی امضاشده شاهد است، نه پشتیبان.

1. اول جمع‌آوری را متوقف کنید.
2. کل پوشه داده را به جای امنی بیرون از میزبان کپی کنید.
3. پیش از اعتماد، بازیابی آن را روی یک نصب جداگانه امتحان کنید.

## پس از راه‌اندازی مجدد بررسی کنید

فضای کاری و کلید، اتصال، منابع و رسیدن پیام‌های جدید را بررسی کنید. TgWitness آنچه Telegram هنوز دارد را جبران می‌کند، نه هر چیزی که هنگام خاموشی رخ داده.

کانتینر «healthy» یعنی وب‌سرور پاسخ می‌دهد. اینکه جمع‌آوری کار می‌کند یا نه را پیام آزمایشی و شاهد می‌گویند.

## فقط آنچه را که قصد دارید منتشر کنید

HTTPS، حجم‌ها، به‌روزرسانی‌ها و بازیابی در مرجع استقرار هستند. آنچه واقعاً آزمایش شده: [سابقه اعتبارسنجی](https://phishdestroy.github.io/TgWitness/fa/docs/reference/verification/).
