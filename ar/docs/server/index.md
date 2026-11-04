# حافظ على استمرار عملها

Canonical page: https://phishdestroy.github.io/TgWitness/ar/docs/server/

أبقِ المُجمِّع يعمل والبيانات آمنة عبر إعادات التشغيل.

## اختر طريقة الإطلاق

التثبيت الأصلي: [المشغّل](https://phishdestroy.github.io/TgWitness/ar/docs/start/) مع قوالب الخدمة في [deploy/](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md). Docker، من مجلد المشروع:

```
docker compose up -d --build --wait
docker compose exec tgwitness cat /data/panel-token.txt
```

تستمع اللوحة على localhost:8787. افتحها محليًا أو عبر نفق SSH، بالرمز الناتج عن الأمر الثاني.

## احتفظ بدليل البيانات بالكامل

التثبيت الأصلي: `data/live`. Docker: وحدة التخزين `tgwitness-data`. السجلات والجلسات والمفاتيح يجب أن تبقى معًا. التصدير الموقّع دليل، وليس نسخة احتياطية.

1. أوقف الجمع أولاً.
2. انسخ دليل البيانات كاملاً إلى مكان آمن خارج المضيف.
3. جرّب استعادته على تثبيت منفصل قبل أن تثق به.

## يرجى التحقق بعد إعادة التشغيل

تحقق من مساحة العمل والمفتاح والاتصال والمصادر ومن وصول رسائل جديدة. يلحق TgWitness بما لا يزال لدى Telegram، لا بكل ما حدث أثناء توقفه.

الحاوية "healthy" تعني أن خادم الويب يجيب. أما هل يعمل الجمع، فرسالة الاختبار والشاهد يخبرانك.

## انشر فقط ما تنوي نشره

HTTPS ووحدات التخزين والتحديثات والاستعادة موجودة في مرجع النشر. ما تم اختباره فعلاً: [سجل التحقق](https://phishdestroy.github.io/TgWitness/ar/docs/reference/verification/).
