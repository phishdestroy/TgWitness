# اسے چلتا رکھیں

Canonical page: https://phishdestroy.github.io/TgWitness/ur/docs/server/

کلیکٹر کو چلتا اور ڈیٹا کو ری اسٹارٹس میں محفوظ رکھیں۔

## لانچ کا طریقہ منتخب کریں

مقامی: [لانچر](https://phishdestroy.github.io/TgWitness/ur/docs/start/) اور [deploy/](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md) میں سروس ٹیمپلیٹس۔ Docker، پروجیکٹ فولڈر سے:

```
docker compose up -d --build --wait
docker compose exec tgwitness cat /data/panel-token.txt
```

پینل localhost:8787 پر سنتا ہے۔ اسے مقامی طور پر یا SSH ٹنل سے کھولیں، دوسری کمانڈ کے ٹوکن کے ساتھ۔

## پورے ڈیٹا ڈائریکٹری کو برقرار رکھیں

مقامی: `data/live`۔ Docker: `tgwitness-data` والیوم۔ جرنلز، سیشنز اور کلیدیں ساتھ رہتی ہیں۔ دستخط شدہ ایکسپورٹ ثبوت ہے، بیک اپ نہیں۔

1. پہلے جمع کرنا روکیں۔
2. پوری ڈیٹا ڈائریکٹری ہوسٹ سے باہر کسی محفوظ جگہ کاپی کریں۔
3. بھروسہ کرنے سے پہلے الگ انسٹال پر بحالی آزمائیں۔

## ری اسٹارٹ کے بعد چیک کریں

ورک اسپیس اور کلید، کنکشن، ذرائع اور نئے پیغامات کی آمد جانچیں۔ TgWitness وہی پورا کرتا ہے جو Telegram کے پاس اب بھی ہے، وہ سب نہیں جو بند رہنے کے دوران ہوا۔

"healthy" کنٹینر کا مطلب ہے ویب سرور جواب دیتا ہے۔ جمع کرنا کام کر رہا ہے یا نہیں، ٹیسٹ پیغام اور گواہ بتائیں گے۔

## صرف وہی شائع کریں جو آپ کا ارادہ ہو

HTTPS، والیومز، اپ ڈیٹس اور بحالی ڈیپلائمنٹ حوالے میں ہیں۔ جو واقعی ٹیسٹ ہوا: [توثیقی ریکارڈ](https://phishdestroy.github.io/TgWitness/ur/docs/reference/verification/)۔
