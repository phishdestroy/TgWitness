# इंस्टॉल करें, सत्यापित करें और अपडेट करें

Canonical page: https://phishdestroy.github.io/TgWitness/hi/docs/reference/installation/

एक कमांड से इंस्टॉल करें, हस्ताक्षरों और हैश की जांच करें, इंस्टॉलेशन को अपडेट और हटाएँ।

[परियोजना](https://github.com/phishdestroy/TgWitness/blob/main/README.md) · [त्वरित आरंभ](https://phishdestroy.github.io/TgWitness/hi/docs/reference/quickstart/) · [तैनाती](https://phishdestroy.github.io/TgWitness/hi/docs/reference/deployment/)

## एक कमांड से इंस्टॉल करें

गाइडेड इंस्टॉलर में एक निजी पाइथन रनटाइम शामिल है। भविष्य की इंस्टॉलेशन के लिए उसी पते का उपयोग करें: प्रत्येक प्रकाशन इंस्टॉलर, हैश, हस्ताक्षर और बिल्ड जानकारी को एक साथ अपडेट करता है।

**Linux / macOS (Bash):**

```
curl -fsSL https://get.destroy.tools/install.sh | bash
```

उबंटू सर्वर पर, बैकग्राउंड सेवा इंस्टॉल करने के लिए रूट के रूप में चलाएँ। डेस्कटॉप पर, अपने सामान्य उपयोगकर्ता के रूप में चलाएँ।

**विंडोज (पावरशेल या कमांड प्रॉम्प्ट):**

```
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "irm https://get.destroy.tools/install.ps1 | iex"
```

Windows पर किसी प्रशासक की आवश्यकता नहीं है। चाइल्ड PowerShell प्रक्रिया आपके टर्मिनल को परिणाम के साथ खुला छोड़ देती है। Python और निर्भरताएँ इंस्टॉलेशन में ही रहती हैं।

उबंटू पर, **'यह कंप्यूटर**', **'अस्थायी HTTPS लिंक'** या **'अपना डोमेन'** चुनें। इंस्टॉलर पैनल का पता और एक्सेस कुंजी प्रिंट करता है। अस्थायी लिंक के लिए, उस HTTPS पते को अपने ब्राउज़र में खोलें और कुंजी दर्ज करें। रिमोट सर्वर पर स्थानीय एक्सेस के साथ, अपने कंप्यूटर से एक SSH फॉरवर्ड का उपयोग करें (`ssh -L 8787:127.0.0.1:8787 user@server`) और खोलें `http://127.0.0.1:8787`. macOS और Windows पर, स्थानीय पैनल आपके ब्राउज़र में खुलता है; इसके टर्मिनल को चालू रखें।

पैनल में टेलीग्राम में साइन इन करें और चुनें कि क्या एकत्र करना है। केवल इंस्टॉलेशन से टेलीग्राम संग्रह शुरू नहीं होता है।

## जहाँ सब कुछ चलता है

`get.destroy.tools` यह एक **Cloudflare Worker स्थिर डाउनलोड परोस रहा है** है। इसमें कोई TgWitness पैनल, टेलीग्राम सत्र या उपयोगकर्ता साक्ष्य डेटाबेस नहीं है। इसे किसी प्रोजेक्ट वीपीएस पर राउट नहीं किया गया है। एप्लिकेशन उस मशीन पर चलती है जहाँ आप कमांड निष्पादित करते हैं।

| स्थापना | कार्यक्रम | डेटा |
| --- | --- | --- |
| रूट के रूप में उबंटू | `/opt/tgwitness` | सिस्टम सेवा: `/var/lib/tgwitness-<installation ID>`; का उपयोग करें `tgwitness paths` सटीक पथ के लिए। |
| Linux / macOS उपयोगकर्ता | `~/.local/share/tgwitness` | `data/live` उस इंस्टॉलेशन के अंतर्गत। |
| विंडोज उपयोगकर्ता | `%LOCALAPPDATA%\TgWitness` | `data\live` उस इंस्टॉलेशन के अंतर्गत। |

सेट `TGWITNESS_INSTALL_DIR` दूसरा फ़ोल्डर चुनने के लिए। इंस्टॉल किए गए संस्करण और डेटा अलग होते हैं। इंस्टॉलर आपके खातों, संदेशों या कुंजियों को डाउनलोड साइट पर अपलोड नहीं करता है। Cloudflare टनल चुनने पर पैनल ट्रैफ़िक Cloudflare के माध्यम से जाता है; अपना स्वयं का डोमेन उपयोग करने पर यह आपके स्वयं के सर्वर पर निर्देशित होता है।

हर इंस्टॉलेशन में **START-HERE.html** और **START-HERE.txt** शामिल होते हैं, जिनमें स्थानीय पथ, कमांड और रिपॉजिटरी के लिंक होते हैं। चलाएँ `tgwitness guide` गाइड खोलने के लिए। Windows पर, का उपयोग करें `& "$env:LOCALAPPDATA\TgWitness\bin\tgwitness.cmd" guide` PowerShell में, PowerShell_startup.ps1 का उपयोग करें।

## चलाने से पहले सत्यापित करें

एक-लाइन कमांड अपनी प्रारंभिक स्क्रिप्ट के लिए HTTPS पर भरोसा करती है। वह स्क्रिप्ट इंस्टॉलेशन से पहले SHA-256 और एप्लिकेशन पर प्रोजेक्ट के RSA हस्ताक्षर और प्रतिबंधों की जांच करती है। आप पहले प्रारंभिक स्क्रिप्ट को डाउनलोड और सत्यापित भी कर सकते हैं।

सार्वजनिक रिलीज़ कुंजी [release-signing.pub](https://github.com/phishdestroy/TgWitness/blob/main/deploy/installer/release-signing.pub) है। इसका SHA-256 है:

```
039d98a658ccda14253e45a00335b4a68d840976d8ec18b8d4355cc7c458447d
```

आपके भरोसेमंद रिपॉजिटरी संशोधन से इस फिंगरप्रिंट को बनाए रखें। उसी डाउनलोड सर्वर से एक चेकसम असंगति का पता लगाता है; स्वतंत्र रूप से विश्वसनीय सार्वजनिक कुंजी ही एक रिलीज़ हस्ताक्षर को प्रमाणित करती है।

नीचे दिए गए सत्यापन डाउनलोड के लिए एक नई, खाली निर्देशिका का उपयोग करें।

**Linux / macOS — एक नई, खाली डाउनलोड निर्देशिका में चलाएँ** (curl और OpenSSL आवश्यक):

```
curl -fSLO https://get.destroy.tools/install.sh &&
curl -fSLO https://get.destroy.tools/install.sh.sig &&
curl -fSLO https://get.destroy.tools/release-signing.pub &&
test "$(openssl dgst -sha256 release-signing.pub | awk '{print $NF}')" = \
  '039d98a658ccda14253e45a00335b4a68d840976d8ec18b8d4355cc7c458447d' &&
openssl dgst -sha256 -verify release-signing.pub -signature install.sh.sig install.sh &&
bash install.sh
```

द `&&` यदि डाउनलोड, कुंजी फिंगरप्रिंट या हस्ताक्षर जांच विफल हो जाती है तो चेन निष्पादन से पहले रुक जाती है। यदि स्क्रिप्ट को डाउनलोड करने और उसके हस्ताक्षर के बीच प्रकाशन हो जाता है, तो दोनों को फिर से डाउनलोड करें। पुराने इंस्टॉलर अपने अपरिवर्तनीय पैकेज URL को बनाए रखते हैं।

**Windows — चलाने से पहले SHA-256 का निरीक्षण करें:**

```
Invoke-WebRequest https://get.destroy.tools/install.ps1 -OutFile install.ps1 -UseBasicParsing
Get-FileHash .\install.ps1 -Algorithm SHA256
Invoke-RestMethod https://get.destroy.tools/SHA256SUMS.txt
```

हैश की तुलना के साथ करें `install.ps1` पंक्ति। एक स्वतंत्र हस्ताक्षर जांच के लिए, OpenSSL का उपयोग करें (उदाहरण के लिए, Git Bash से) और ऊपर दी गई वही सार्वजनिक-कुंजी फिंगरप्रिंट:

```
curl -fSLO https://get.destroy.tools/install.ps1 &&
curl -fSLO https://get.destroy.tools/install.ps1.sig &&
curl -fSLO https://get.destroy.tools/release-signing.pub &&
test "$(openssl dgst -sha256 release-signing.pub | awk '{print $NF}')" = \
  '039d98a658ccda14253e45a00335b4a68d840976d8ec18b8d4355cc7c458447d' &&
openssl dgst -sha256 -verify release-signing.pub -signature install.ps1.sig install.ps1 &&
powershell.exe -NoProfile -ExecutionPolicy Bypass -File install.ps1
```

विंडोज इंस्टॉलेशन स्वयं .NET के साथ पैकेज हस्ताक्षरों को सत्यापित करता है और OpenSSL की आवश्यकता नहीं होती है। ये अलग किए गए RSA-3072 / SHA-256 हस्ताक्षर हैं, न कि Authenticode। [मैनिफेस्ट](https://get.destroy.tools/manifest.json) सॉफ्टवेयर संस्करण, सटीक Git कमिट, अपरिवर्तनीय रिलीज़ आईडी और प्रत्येक आर्टिफैक्ट के SHA-256 को रिकॉर्ड करता है। पेज संबंधित स्रोत से लिंक करता है। मैनिफेस्ट और चेकसम सूची में भी अलग किए गए हस्ताक्षर होते हैं (`manifest.json.sig` और `SHA256SUMS.txt.sig`).

## मौजूदा इंस्टॉलेशन को अपडेट करें

**एक नया प्रकाशन डाउनलोड साइट को अपडेट करता है; इंस्टॉल किए गए प्रोग्राम तब अपडेट होते हैं जब आप इंस्टॉलर को फिर से चलाते हैं।** कोई अनअटेंडेड अपडेटर या चल रहे संग्रह का स्वचालित पुनरारंभ नहीं है। वर्तमान इंस्टॉलर चैनल **पूर्वावलोकन** है; यह प्रकाशित, जाँचे गए बिल्ड का अनुसरण करता है `main`, जिसका कमिट पिछली क्रमांकित GitHub रिलीज़ से नया हो सकता है। पेज का संस्करण से आता है `pyproject.toml`; इसकी कमिट और बिल्ड आईडी एक ही प्रीव्यू संस्करण के भीतर अपडेट को अलग करती हैं।

पहले की तरह ही इंस्टॉलेशन फ़ोल्डर और OS उपयोगकर्ता का उपयोग करें। संग्रह को रोके बिना पूरी डेटा निर्देशिका का बैकअप लें; `tgwitness paths` इसकी पहचान करता है। एक हस्ताक्षरित एक्सपोर्ट एक पूर्ण इंस्टॉलेशन बैकअप नहीं है।

**उबंटू रूट इंस्टॉलेशन पर `/opt/tgwitness`:**

```
curl -fsSL https://get.destroy.tools/install.sh | TGWITNESS_INSTALL_DIR=/opt/tgwitness bash -s -- --no-start
```

सफल स्थापना के बाद:

```
/opt/tgwitness/bin/tgwitness restart
/opt/tgwitness/bin/tgwitness status
/opt/tgwitness/bin/tgwitness open
```

Linux/macOS उपयोगकर्ता इंस्टॉलेशन के लिए, इसके मूल `TGWITNESS_INSTALL_DIR` या डिफ़ॉल्ट का उपयोग करें और पहली इंस्टॉलेशन कमांड को फिर से चलाएँ। अपडेट करने से पहले किसी फॉरग्राउंड पैनल को बंद करें और बाद में उसे फिर से शुरू करें। एक कॉन्फ़िगर किए गए लिनक्स उपयोगकर्ता सेवा के लिए, इसका `tgwitness restart` कमांड चलाएँ।

**विंडोज़:** चल रहे पैनल को बंद करें, विंडोज़ इंस्टॉलेशन कमांड को फिर से चलाएँ, फिर खोलें `bin\tgwitness.cmd` एक ही इंस्टॉलेशन में। इंस्टॉलर डेटा, सत्र, एक्सेस सेटिंग्स और साइनिंग कुंजियों को बरकरार रखता है। यह लॉन्चर को केवल तभी बदलता है जब नया वातावरण अपनी जाँच पास कर ले; असफल इंस्टॉलेशन पिछले लॉन्चर को वहीं रख देता है। स्टोरेज-फ़ॉर्मेट परिवर्तनों के लिए प्री-अपग्रेड बैकअप को रखें।

## उबंटू पर दैनिक कमांड

| कमांड | परिणाम |
| --- | --- |
| `tgwitness open` | वर्तमान पैनल URL और एक्सेस कुंजी। |
| `tgwitness paths` | सटीक प्रोग्राम, डेटा और मार्गदर्शिका पथ। |
| `tgwitness guide --print` | ऑफ़लाइन संचालन निर्देश। |
| `tgwitness status` / `tgwitness logs` | उपलब्धता / सेवा लॉग। |
| `tgwitness stop` / `tgwitness start` | सेवा को रोकें / फिर से शुरू करें; डेटा बनाए रखें। |
| `tgwitness token rotate` | प्रशासक कुंजी बदलें और ब्राउज़र सत्र समाप्त करें। |
| `tgwitness tunnel off` | सार्वजनिक क्विक टनल को अक्षम करें; स्थानीय पैनल को बनाए रखें। |
| `tgwitness tunnel on` / `tgwitness tunnel restart` | एक त्वरित-टनल लिंक बनाएँ / उसका पता बदलें। |

सहकर्मी टोकन, सत्र और आईपी प्रतिबंधों के लिए [एक्सेस](https://phishdestroy.github.io/TgWitness/hi/docs/reference/access/) देखें, और GitHub-to-Cloudflare रिलीज़ वर्कफ़्लो के लिए [इंस्टॉलर प्रकाशन](https://github.com/phishdestroy/TgWitness/blob/main/deploy/installer/README.md#automatic-publication-from-github) ।

## TgWitness हटाएँ

कोई अनइंस्टॉलर नहीं है: आप पैनल को रोकते हैं और उसके फ़ोल्डरों को हटा देते हैं। डेटा फ़ोल्डर को हटाने से जर्नल, साइनिंग कुंजियाँ, टेलीग्राम सत्र और सहेजी गई फ़ाइलें हमेशा के लिए नष्ट हो जाती हैं। उससे पहले:

1. जिस चीज़ की आपको ज़रूरत है उसे एक्सपोर्ट करें (**एक्सपोर्ट्स → डाउनलोड साइन्ड ZIP**) और साइनिंग की का फिंगरप्रिंट और चेकपॉइंट्स इस मशीन से बाहर रखें। वर्कस्पेस को खुद को बनाए रखने के लिए, कलेक्शन को रोके हुए पूरे डेटा फ़ोल्डर को कॉपी करें।
2. **Extras → Server 24/7** के तहत **आपके सर्वरों** या के साथ बनाए गए सर्वरों को हटाएँ `python -m tgwitness.cloud destroy`; प्रदाता उन्हें हटाए जाने तक बिल करता है।
3. प्रत्येक खाते का सत्र Telegram में **Settings → Devices** के अंतर्गत समाप्त करें। फ़ाइलों को हटाने से Telegram की ओर से सत्र लॉग आउट नहीं होता।

**उबंटू रूट इंस्टॉलेशन।** डेटा फ़ोल्डर पर ध्यान दें, सेवा को रोकें, फिर सेवा, फ़ोल्डरों और शॉर्टकट को हटा दें:

```
/opt/tgwitness/bin/tgwitness paths
/opt/tgwitness/bin/tgwitness stop
systemctl list-unit-files 'tgwitness-*'
systemctl disable tgwitness-<ID>
rm /etc/systemd/system/tgwitness-<ID>.service
systemctl daemon-reload
rm -rf /opt/tgwitness /var/lib/tgwitness-<ID> /usr/local/bin/tgwitness
```

**Linux या macOS उपयोगकर्ता इंस्टॉलेशन।** पैनल बंद करें। एक कॉन्फ़िगर की गई Linux उपयोगकर्ता सेवा के साथ रोकी जाती है `systemctl --user disable --now tgwitness-<ID>`; इसकी इकाई है `~/.config/systemd/user/`। फिर हटाएँ `~/.local/share/tgwitness` (या आपका `TGWITNESS_INSTALL_DIR`) और `~/.local/bin/tgwitness` शॉर्टकट।

**Windows।** पैनल बंद करें और हटाएं `%LOCALAPPDATA%\TgWitness` (या आपका `TGWITNESS_INSTALL_DIR`)। इंस्टॉलर कोई सेवा, अनुसूचित कार्य या शॉर्टकट नहीं जोड़ता है।
