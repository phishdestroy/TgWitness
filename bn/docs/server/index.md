# এটি চালু রাখুন

Canonical page: https://phishdestroy.github.io/TgWitness/bn/docs/server/

কালেক্টর চালু রাখুন এবং রিস্টার্টের মধ্যেও ডেটা নিরাপদ রাখুন।

## একটি লঞ্চ পদ্ধতি নির্বাচন করুন

নেটিভ: [লঞ্চার](https://phishdestroy.github.io/TgWitness/bn/docs/start/) ও [deploy/](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md)-এ সার্ভিস টেমপ্লেট। Docker, প্রকল্প ফোল্ডার থেকে:

```
docker compose up -d --build --wait
docker compose exec tgwitness cat /data/panel-token.txt
```

প্যানেল localhost:8787-এ শোনে। স্থানীয়ভাবে বা SSH টানেল দিয়ে খুলুন, দ্বিতীয় কমান্ডের টোকেন দিয়ে।

## পুরো ডেটা ডিরেক্টরিটি রাখুন

নেটিভ: `data/live`। Docker: `tgwitness-data` ভলিউম। জার্নাল, সেশন ও কী একসাথে থাকা উচিত। স্বাক্ষরিত এক্সপোর্ট প্রমাণ, ব্যাকআপ নয়।

1. আগে সংগ্রহ থামান।
2. পুরো ডেটা ডিরেক্টরি হোস্টের বাইরে নিরাপদ কোথাও কপি করুন।
3. বিশ্বাস করার আগে আলাদা ইনস্টলে পুনরুদ্ধার চেষ্টা করুন।

## পুনরায় চালু করার পর পরীক্ষা করুন

ওয়ার্কস্পেস ও কী, সংযোগ, উৎস এবং নতুন বার্তা আসছে কিনা দেখুন। TgWitness পূরণ করে যা Telegram-এর কাছে এখনো আছে, বন্ধ থাকার সময় ঘটা সব কিছু নয়।

"healthy" কন্টেইনার মানে ওয়েব সার্ভার উত্তর দেয়। সংগ্রহ কাজ করছে কিনা, টেস্ট বার্তা ও সাক্ষী বলবে।

## আপনি যা প্রকাশ করতে চান শুধুমাত্র সেটাই প্রকাশ করুন।

HTTPS, ভলিউম, আপডেট ও পুনরুদ্ধার ডিপ্লয়মেন্ট রেফারেন্সে আছে। যা সত্যিই পরীক্ষা করা হয়েছে: [যাচাইয়ের রেকর্ড](https://phishdestroy.github.io/TgWitness/bn/docs/reference/verification/)।
