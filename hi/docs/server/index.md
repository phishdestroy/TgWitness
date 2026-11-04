# इसे चालू रखें

Canonical page: https://phishdestroy.github.io/TgWitness/hi/docs/server/

कलेक्टर चलता रखें और डेटा रीस्टार्ट के दौरान सुरक्षित रखें।

## लॉन्च विधि चुनें

नेटिव: [लॉन्चर](https://phishdestroy.github.io/TgWitness/hi/docs/start/) और [deploy/](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md) में सर्विस टेम्पलेट। Docker, प्रोजेक्ट फ़ोल्डर से:

```
docker compose up -d --build --wait
docker compose exec tgwitness cat /data/panel-token.txt
```

पैनल localhost:8787 पर सुनता है। इसे स्थानीय रूप से या SSH टनल से खोलें, दूसरी कमांड के टोकन के साथ।

## पूरे डेटा निर्देशिका को रखें

नेटिव: `data/live`। Docker: `tgwitness-data` वॉल्यूम। जर्नल, सेशन और कुंजियाँ साथ रहनी चाहिए। हस्ताक्षरित एक्सपोर्ट साक्ष्य है, बैकअप नहीं।

1. पहले संग्रह रोकें।
2. पूरी डेटा डायरेक्टरी होस्ट से बाहर किसी सुरक्षित जगह कॉपी करें।
3. भरोसा करने से पहले अलग इंस्टॉल पर पुनर्स्थापना आज़माएँ।

## पुनरारंभ के बाद जाँचें

वर्कस्पेस और कुंजी, कनेक्शन, स्रोत और नए संदेशों का आना जाँचें। TgWitness वही पूरा करता है जो Telegram के पास अब भी है, वह सब नहीं जो बंद रहने के दौरान हुआ।

"healthy" कंटेनर का मतलब है वेब सर्वर जवाब देता है। संग्रह काम कर रहा है या नहीं, टेस्ट संदेश और गवाह बताएँगे।

## केवल वही प्रकाशित करें जो आपका इरादा हो

HTTPS, वॉल्यूम, अपडेट और पुनर्स्थापना डिप्लॉयमेंट संदर्भ में हैं। जो सच में टेस्ट हुआ: [सत्यापन रिकॉर्ड](https://phishdestroy.github.io/TgWitness/hi/docs/reference/verification/)।
