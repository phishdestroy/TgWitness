# क्या परीक्षण किया गया है

Canonical page: https://phishdestroy.github.io/TgWitness/hi/docs/reference/verification/

लाइव टेलीग्राम परीक्षण, स्वचालित जांचें, ब्राउज़र जांचें और जो अप्रमाणित रह जाता है।

## लाइव फला क्लाउड परिनियोजन · 4 नवंबर 2026

`--provider phala --quick-tunnel` को वास्तविक **Phala Cloud** (`tdx.small`, क्षेत्र US-WEST-1) पर एक खाली वर्कस्पेस की Phala Cloud API कुंजी, वास्तविक ntfy.sh, GitHub और Intel PCS के साथ चलाया गया। CVM ने commit `df7d860c` (v0.8.1) इंस्टॉल किया; deploy, verify और destroy नीचे दिए गए फिक्स के साथ कमांड लाइन से चले। सात CVM की कुल लागत लगभग 1.9 अमेरिकी सेंट आई।

पहली दो डिप्लॉयमेंट्स में सिम्युलेटेड Phala क्लाउड से पाँच अंतर पाए गए। [`tools/check_phala.py`](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_phala.py) अब प्रत्येक को फिर से उत्पन्न करता है, और इसकी फिक्स के बिना विफल हो जाता है:

| Phala Cloud पर | ठीक करने से पहले | ठीक करें |
| --- | --- | --- |
| `compose_file.name` आवश्यक है | HTTP 422, कुछ भी नहीं बनाया गया | Docker Compose कॉन्फ़िगरेशन CVM नाम वहन करता है |
| जब तक एक खाली स्क्रिप्ट नहीं दी जाती, Phala मापे गए ऐप-कंपोज़ में अपनी खुद की प्री-लॉन्च स्क्रिप्ट जोड़ता है (v0.0.20: Docker लॉगिन, `docker compose pull`, रूट पासवर्ड, `user_config` से SSH कुंजियाँ) | `tdx_compose` विफल हो जाता है: प्रकाशित Docker Compose कॉन्फ़िगरेशन के बाहर का कोड | ऐप-कंपोज़ `pre_launch_script` को `""` पर सेट करता है; फिर Phala इसे छोड़ देता है |
| `image` के बिना Phala, `dstack-dev-0.5.12`, डेवलपमेंट बिल्ड, को चुनता है, जिसमें SSH एक्सेस सक्षम है। | `server_state` विफल हो जाता है। केवल हार्डवेयर प्रमाणीकरण रिकॉर्ड ही इस छवि पर पास हुआ; केवल प्रदाता रिकॉर्ड और `tdx_os` ही इसे दिखाते हैं। | डिप्लॉयमेंट Phala की वर्तमान रिलीज़, `dstack-0.5.12` के प्रोडक्शन बिल्ड के लिए पूछता है। |
| dstack गेटवे बंद होने पर, CVM विवरण को कभी भी `instance_id` नहीं मिलता है। | डिप्लॉय 30 मिनट तक प्रतीक्षा करता है और विफल हो जाता है | इंस्टेंस आईडी सीवीएम की स्थिति से पढ़ी जाती है। |
| रीस्टार्ट, स्टॉप और स्टार्ट सीवीएम ऑपरेशन हैं, न कि एप्लिकेशन संशोधन। | `provider_actions` ने रीस्टार्ट्स को सूचीबद्ध नहीं किया। | ऑपरेशन भी पढ़े जाते हैं |

तीसरी तैनाती:

- CVM ने SSH एक्सेस बंद करके `dstack-0.5.12` चलाया। कलेक्टर ने अपनी साइन की हुई पता-पंक्ति बनाने के लगभग 1.5 मिनट बाद पोस्ट की। इसके बाद Deploy ने `tdx_binding`, `tdx_quote` (Intel TCB UpToDate, हार्डवेयर अटेस्टेशन रिकॉर्ड v4, FMSPC `20a06f000000`, डिबग मोड में नहीं, माइग्रेटेबल नहीं, Intel से प्राप्त क्रिप्टोग्राफिक सत्यापन डेटा का समर्थन करता है), `tdx_compose_hash`, `tdx_compose` (बाइट-दर-बाइट) और `tdx_identity` (KMS कुंजियाँ)।
- trycloudflare.com पते पर पैनल ने टोकन के बिना या गलत टोकन के साथ 401 का उत्तर दिया, और पैनल टोकन के साथ 200 का।
- `verify` के साथ `--source` को कमिट के GitHub आर्काइव पर सेट किया गया और फिंगरप्रिंट अलग से दिया गया: सर्वर, `server_state`, फ़ायरवॉल (कोई गेटवे नहीं, कोई सार्वजनिक एंडपॉइंट नहीं), प्रोवाइडर लॉग, स्टेटमेंट, फिंगरप्रिंट, सोर्स हैश, बूट और पाँच `tdx_*` जांचें पास हुईं। Cloudflare और `tdx_os` अनुपलब्ध थे, इसलिए परिणाम अधूरा था।
- Phala की API के माध्यम से दो बार रीस्टार्ट: हर बार CVM दो मिनट से भी कम समय में उसी कलेक्टर की, एक नए साइन किए गए एड्रेस, और पुराने वाले के 530 का जवाब देने के साथ वापस आ गया। `verify` ने नए बूट और दोनों रीस्टार्ट को REVIEW के रूप में रिपोर्ट किया। `--evidence` के साथ इसने जर्नल हस्ताक्षरों और तीन स्टार्ट्स की पुष्टि की, प्रत्येक में उसी CVM से अपना स्वयं का Intel TDX हार्डवेयर अटेस्टेशन रिकॉर्ड था।
- `destroy` ने केवल उसी CVM को हटा दिया। उसके बाद वर्कस्पेस खाली हो गया, और पैनल का पता जवाब देना बंद कर दिया।
- पैनल विज़ार्ड की कीमत की जाँच में `tdx.small` को $0.058 प्रति घंटा पढ़ा गया। एक गलत कुंजी पर एक साधारण "एपीआई कुंजी स्वीकार नहीं की गई" संदेश मिला।

दो और निष्कर्ष, जिन्हें बाद में ठीक किया गया:

- पते की कुंजी के बिना, `verify` ने पते के विषय पर सबसे नए सही ढंग से बने पोस्ट का अनुसरण किया, जो प्रकाशित Docker Compose कॉन्फ़िगरेशन में मुद्रित होता है। एक जाली पोस्ट ने इसे एक ऐसे होस्ट पर भेज दिया जो मौजूद नहीं है, और `statement` विफल हो गया: एक जालसाज़ कलेक्टर के रूप में नहीं चल सकता था, लेकिन ब्लॉक कर सकता था तीसरे पक्ष के सत्यापन को, एक जाली भविष्य के टाइमस्टैम्प के साथ 12 घंटे तक ब्लॉक कर सकता है। कलेक्टर अब अपने पते को अपनी ही कुंजी से हस्ताक्षरित करके पोस्ट भी करता है, `verify` केवल तभी ऐसी पोस्ट स्वीकार करता है जब कलेक्टर उन्हें करता है, और पोस्ट ntfy.sh के प्राप्ति समय के अनुसार क्रमबद्ध होते हैं। [`tools/check_cloud_wizard.py`](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_cloud_wizard.py) जाली पोस्ट्स को फिर से चलाता है। एक CVM इसे केवल उसी कमिट से चलाता है जिसमें यह मौजूद है, इसलिए इस रन के कलेक्टर ने अभी तक अपने एड्रेस पर साइन नहीं किया था और `verify` ने ऐसा ही कहा।
- `tdx_os`, `dstack-mr` के बिना नहीं चल सकता, जिसका वर्तमान संस्करण दस्तावेज़ीकरण में नामित `measure --json` के बजाय `measure-os` है। सत्यापनकर्ता अब प्रकाशित इमेज और VM के आकार, जिसमें ACPI तालिकाएँ शामिल हैं, से स्वयं MRTD और RTMR0-2 की गणना करता है।

चौथी तैनाती, इनके साथ:

- Deploy ने एक बार प्रकाशित `dstack-0.5.12` को डाउनलोड किया, इसे CVM द्वारा रिपोर्ट किए गए OS इमेज हैश से मिलाया, और `tdx_os` पास हो गया: MRTD, RTMR0, RTMR1 और RTMR2 QEMU के लिए गणना किए गए मानों के बराबर हैं 8.2.2, 1 vCPU और 2 GiB। उसी गणना ने दावा किए गए 4 GiB, 2 vCPUs, QEMU 9.2.1 या दूसरे नेटवर्क कार्ड के लिए एक अलग RTMR0 दिया, और बदले हुए कर्नेल, फर्मवेयर या कमांड लाइन और डेवलपमेंट इमेज के लिए यह विफल हो गया।
- `verify` ने अपनी 16 जाँचों में से हर एक को पास किया, जिसमें क्विक टनल का कनेक्टर भी शामिल था, इसलिए परिणाम PASS था। इसने HTML और PDF प्रमाणपत्र लिखा, जिसे बेल्जियम सरकार की टाइम-स्टैम्पिंग यूनिट TSU 202301 (बेल्जियम की विश्वसनीय सूची में अनुमोदित दर्जा) से एक योग्य eIDAS टाइम स्टैम्प, एक FreeTSA टाइम स्टैम्प और सत्यापनकर्ता के हस्ताक्षर के साथ डिजिटल रूप से सील किया गया था; `check-report` ने उन सभी और PDF के हस्ताक्षर की पुष्टि की।
- एक रीस्टार्ट के बाद, `verify --evidence` ने दो स्टार्ट की पुष्टि की, प्रत्येक के साथ CVM के अंदर उत्पन्न एक हार्डवेयर अटेस्टेशन था और प्रत्येक प्रकाशित `dstack-0.5.12` से बूट किया गया था; रीस्टार्ट और नया बूट REVIEW थे।
- `destroy` ने वर्कस्पेस को खाली छोड़ दिया।

पाँचवीं डिप्लॉयमेंट ने commit `53a0f7e9` से कलेक्टर चलाया, जिसमें उपरोक्त सभी शामिल हैं:

- कलेक्टर ने ऑपरेटर की HMAC पोस्ट के बगल में, अपनी खुद की कुंजी से हस्ताक्षरित अपना पता पोस्ट किया। फिर विषय में दो जाली पोस्ट जोड़े गए, एक शून्य HMAC के साथ और एक दूसरे Ed25519 कुंजी से हस्ताक्षरित, दोनों में 2096 के वर्ष का दावा किया गया था। `verify` ने कलेक्टर कुंजी द्वारा हस्ताक्षरित पते को लिया और सभी 16 जांचों में उत्तीर्ण हुआ; सील में फिर से योग्य बेल्जियम टाइमस्टैम्प, FreeTSA का टाइमस्टैम्प और सत्यापनकर्ता का हस्ताक्षर था, और `check-report` ने उन्हें पुष्टि किया।
- पुनः आरंभ होने के बाद कलेक्टर ने हस्ताक्षर सहित नया पता प्रकाशित किया। `verify` ने उसे तुरंत खोज लिया; ऑपरेटर के **वर्तमान पता खोजें** विकल्प ने HMAC पोस्ट से 27 सेकंड बाद उसे पाया। दोनों ने जाली पोस्ट को अनदेखा किया। `verify --evidence` ने पुष्टि की कि दो आरंभ `dstack-0.5.12` से बूट हुए थे।
- डिप्लॉय ने यह प्रिंट किया कि फला CVM को क्या बिल करता है, जिसमें डिस्क शामिल है: $0.06078 प्रति घंटा।

पैनल विज़ार्ड Phala Cloud पर दो बार चला, एक बार इसकी जॉब API के माध्यम से और एक बार एक वास्तविक Chromium के साथ ब्राउज़र के माध्यम से: कीमत की जाँच, **Advanced** के तहत कमिट के साथ निर्माण, सभी छह प्रमाणीकरण जाँचें पास हुईं, सर्वर सूची में बिल की गई कीमत (प्रति माह 44.37 USD) दिखाना, **वर्तमान पता खोजें**, मापी गई Docker Compose कॉन्फ़िगरेशन डाउनलोड, और हटाना। ब्राउज़र में कोई पेज त्रुटि नहीं देखी गई। हर बार बाद में वर्कस्पेस खाली था।

इसमें शामिल नहीं है: Phala पर एक Cloudflare डोमेन, CVM पर एक Telegram खाता, और `dstack-0.6.1` इमेज। विज़ार्ड की कीमत बनाने से पहले केवल Phala की कंप्यूट कीमत है, क्योंकि इसकी API मौजूदा CVM के लिए केवल डिस्क कीमत बताती है; सर्वर सूची बनाने के बाद बिल की गई कीमत दिखाती है।

## Live server journal inventory · 1 November 2026

At approximately 19:15 UTC, sequential read-only SQLite `query_only` queries counted events in ten workspace databases on a running server. Collection continued during the queries, so this is not an atomic snapshot across workspaces.

| Observed across the ten workspace databases | गिनती |
| --- | --- |
| Workspaces with at least one `message.new` event | 8 |
| Journal records, including operational events | 1,610,818 |
| `message.new` events | 900,232 |
| `message.edited` events | 80,683 |
| `message.deleted` events | 400,536 |
| `message.recovered` events | 53,403 |
| `message.snapshot` events | 2,183 |
| `media.saved` events | 50,418 |
| `media.failed` events | 5,575 |
| `coverage.gap` events | 11 |
| Database bytes, excluding WAL files and media | 7,909,003,264 |

These are **event counts**, not unique messages, people or media files. The same message can appear in more than one workspace, and an edit or deletion can produce another journal event. `media.failed` counts historical failure events, not the current media queue. The queries did **not** newly verify signatures and the full hash chain of all 1,610,818 records, measure delivery or throughput, or establish that every Telegram event was captured. No message content, account or chat IDs, workspace labels, credentials or private files are published here.

At this review, the separately configured public monitor covered three sources: one capture response was OK and two reported `no_response`. That monitor is not a ten-workspace health summary. `no_response` means the observer could not obtain a response at that check; it does not establish message loss. The smaller 29 October test below has its own explicit signature and hash-chain verification.

## Recent offline and fault-injection checks · 1 November 2026

These checks use fictional data and local files; they add regression evidence for the current source, not another live Telegram delivery measurement:

| जाँचें | What it exercised |
| --- | --- |
| [Source archive](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_source_archive.py) | Two builds with identical source bytes but changed file times produced the same ZIP and checksum. Exact archived bytes and file hashes matched; private test files stayed out. A simulated write failure left the previous archive and checksum intact. |
| [Account export recovery](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_account_export_recovery.py) | A simulated disk error on the second ZIP member left no published or partial ZIP. Resume kept every signed receipt byte-identical, produced an independently verifiable archive using the expected signing fingerprint, and retained the synthetic coverage gap as a partial result. Scale assertions guard against repeated task and receipt scans as histories grow. |
| [Minimized disclosure privacy](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_disclosure_privacy.py) | Synthetic Unicode names and aliases, nested metadata, unknown senders and media fields were checked in all three identity modes and with text omission. A masking-limit failure did not silently weaken redaction; the original signed account export stayed unchanged. |
| [Linux media decoder and OCR](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_media_worker.py) | A [Linux Docker CI check](https://github.com/phishdestroy/TgWitness/actions/runs/41341200341/job/124951395192) at commit `5a9e0814` passed generated Ogg/Opus, MP3, M4A, MP4 with video, WAV and FLAC inputs; forged-duration and secondary-file-reference controls; and 48 mutated parser fixtures (34 rejected, 14 decoded within bounds). Real Tesseract OCR ran with original bytes unchanged. The decoder and OCR ran in network-isolated containers without a Whisper model. |

The checks run in the [pull-request](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/pr-check.yml) and [full Checks](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/checks.yml) workflows. They test these failure boundaries, not every possible storage failure or whether a disclosure is automatically safe to publish. The media check does not measure speech recognition accuracy or Telegram delivery. Review each derivative before sharing.

## लाइव टेलीग्राम परीक्षण, पूरा खाता · 29 अक्टूबर 2026

नीचे दिए गए परीक्षण के बाद वही खाता चलता रहा। 29 अक्टूबर को 12:10 UTC पर इसके दायरे को पूरे खाते (चैनल, समूह, निजी चैट और बॉट) में बदल दिया गया; पैनल ने पुष्टि के लिए कहा और हस्ताक्षरित जर्नल ने इसे दर्ज किया। 17:59 UTC तक जर्नल में दर्ज था:

| रिकॉर्ड किया गया, 27 अक्टूबर 21:36 से 29 अक्टूबर 17:59 UTC तक | गिनती |
| --- | --- |
| जर्नल रिकॉर्ड | 9,968 |
| नए संदेश | 5,308 |
| पूरे खाते में स्विच करने के बाद उनमें से | 3,878 |
| हटाई गई वस्तुएँ | 784 |
| उन्हें TgWitness द्वारा संदेश सहेजने के बाद हटा दिया गया | 596 |
| संपादन | 41 |
| पुनः जाँच द्वारा जोड़े गए संदेश | 2,273 |
| वे संदेश जिन्हें रीचेक अब और नहीं ढूंढ सकता | 18 |
| इतिहास स्नैपशॉट्स द्वारा सहेजे गए संदेश | 242 |
| सहेजे गए अटैचमेंट | 247 |
| कलेक्टर शुरू होता है | 19 |
| Telegram FloodWait विराम | 26 |

- पैनल के **Verify** चेक ने सभी 9,968 रिकॉर्ड्स के हस्ताक्षर और हैश चेन की पुष्टि की।
- संदेश 2 समूहों या चैनलों और 3 निजी चैट और बॉट्स से आए थे। चैट्स से एक संदेश बटन दबाया गया था; अनुरोध और टेलीग्राम का उत्तर जर्नल में हैं।
- जब कलेक्टर ने रीस्टार्ट पर खाते को फिर से स्कैन किया, तब नई चैट्स जोड़ी गईं। नई चैट्स के पुराने संदेशों को सहेजना बंद (`history = 0`) था, इसलिए यह यहाँ शामिल नहीं है।

इसमें शामिल नहीं है: प्रतिक्रियाएं, सदस्यता परिवर्तन, लोगों के प्रोफाइल, संदेश भेजना, निमंत्रण द्वारा जुड़ना, प्रॉक्सी, सूचनाएं, विटनेस बॉट और एक साथ कई खाते। सार्वजनिक फ़ाइलों में केवल गिनती होती है।

## पासवर्ड-संरक्षित निर्यात libarchive के साथ खोला गया · 29 अक्टूबर 2026

एक्सपोर्ट एन्क्रिप्शन कोड (WinZip AES-256, वह प्रारूप जिसे 7-Zip और WinRAR पढ़ते हैं) द्वारा लिखे गए एक आर्काइव को Windows `tar` (bsdtar 3.6.2, libarchive) से खोला गया। सही पासवर्ड के साथ निकाली गई फ़ाइल का मूल SHA-256 से मिलान हुआ; गलत पासवर्ड देने पर "Incorrect passphrase" (गलत पासफ़्रेज़) की त्रुटि दिखाई गई। 7-Zip और WinRAR को स्वयं नहीं चलाया गया।

## लाइव टेलीग्राम परीक्षण · 27 से 29 अक्टूबर 2026

एक असली टेलीग्राम खाते ने, जो बिल्ट-इन एपीआई जोड़ी पूल के माध्यम से साइन इन किया हुआ था, **27 अक्टूबर 21:36 UTC**से**29 अक्टूबर 05:15 UTC तक** एक सुपरग्रुप को रिकॉर्ड किया। उस अवधि में कलेक्टर को 12 बार शुरू किया गया था।

| रिकॉर्ड किया गया | गिनती |
| --- | --- |
| जर्नल रिकॉर्ड, जिसमें हार्टबीट्स और सेवा रिकॉर्ड शामिल हैं | 2,385 |
| नए संदेश | 1,291 |
| हटाई गई वस्तुएँ | 472 |
| उन्हें TgWitness द्वारा टेक्स्ट सहेजने के बाद हटा दिया गया | 347 |
| संपादन | 12 |
| रुकने के दौरान छूटे संदेश, रीचेक द्वारा जोड़े गए | 12 |
| सहेजे गए अटैचमेंट | 17 |
| संलग्नक डाउनलोड नहीं हुए (डाउनलोड बंद हैं, या डाउनलोड करने के लिए कोई फ़ाइल नहीं है) | 14 |
| Telegram FloodWait पुनः जाँच के दौरान प्रत्येक बार 3 सेकंड के लिए विराम लेता है | 8 |

- सभी 2,385 रिकॉर्डों के हस्ताक्षर और हैश श्रृंखला जर्नल की सार्वजनिक कुंजी के विरुद्ध सत्यापित होती हैं।
- रीस्टार्ट के बाद कलेक्टर सहेजे गए अपडेट स्टेट (`pts`) से फिर से शुरू होता है और Telethon catch up करता है; फिर रीचेक उन संदेशों को जोड़ता है जो अभी भी गायब हैं।
- हर फ्लडवॉइट पर कलेक्टर ने अनुरोधित समय तक प्रतीक्षा की और जारी रखा।
- खाता साइन इन ही रहा, और वही सत्र 29 अक्टूबर को फिर से जुड़ गया।

इस परीक्षण में शामिल नहीं हैं: एक साथ कई खाते, प्रशासक भूमिकाएँ, प्रॉक्सी, कुछ घंटों से अधिक समय तक चलने वाली रुकावटें और पूरी [लाइव स्वीकृति प्रक्रिया](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md)। सार्वजनिक फ़ाइलों में केवल ये गिनती शामिल हैं: कोई खाता या चैट पहचानकर्ता, संदेश या क्रेडेंशियल नहीं।

## कृत्रिम स्थानीय क्षमता मापन

कमांड: `python tools/check_capacity.py --events 10000 --chats 100`

| मेट्रिक | निरीक्षित |
| --- | --- |
| इनपुट | 100 कृत्रिम रूप से चयनित स्रोतों में 10,000 सिंथेटिक संदेश घटनाएँ |
| संदेश का पाठ | 400 वर्ण; कोई मीडिया या नेटवर्क नहीं |
| इनजेस्टन | 53.273 सेकंड; 187.7 घटनाएँ/सेकंड |
| हैंडलर विलंबता | p50 4.162 ms; p95 7.784 ms; अधिकतम 129.118 ms |
| ZIP निर्यात | ट्रेसमैलोक सक्षम होने पर 19.868 सेकंड |
| पीक ट्रेस किए गए पाइथन एक्सपोर्ट आवंटन | 0.51 MiB; RSS प्रक्रिया नहीं |
| ZIP आकार | 4,610,962 बाइट्स |
| स्वतंत्र सत्यापन | सभी 10,000 घटनाएँ सत्यापित |

यह इस विंडोज़ होस्ट पर स्थानीय सीरियल रिकॉर्डिंग/एक्सपोर्ट पथ को मापता है। यह MTProto डिलीवरी, एक साथ चलने वाले खातों, टेलीग्राम थ्रॉटलिंग, मीडिया, एक लंबे समय तक चलने वाले वर्कलोड, या वास्तविक चैट की एक गारंटीकृत संख्या को मापता नहीं है। यह मापन अंतिम ऑफ़लाइन टाइमस्टैम्प टूलिंग से पहले का है, जो मापे गए संदेश पथ को नहीं बदलता है।

## शेष योग्यता

रखे गए लाइव जर्नल में वास्तविक संग्रह, संपादन, हटाने की सूचनाएं, संलग्नक, पुनः जाँच और दर-सीमा प्रबंधन दर्ज होता है। यह व्यापक डिलीवरी या भूमिका दृश्यता, प्रतिक्रिया करने वालों, लंबे समय तक चलने वाले फ्लडवेट (FloodWait), खाते पर प्रतिबंध और नेटवर्क/प्रक्रिया में रुकावट से उबरने के नियंत्रित मैट्रिक्स को स्थापित नहीं करता है। QR-टोकन जारी करना पूरी हुई मोबाइल QR पुष्टि से अलग रहता है।

Docker बिल्ड/रन, लिनक्स/मैकओएस इंस्टॉलेशन, निरंतर उच्च लोड, स्वतंत्र सुरक्षा समीक्षा, एक वास्तविक स्वतंत्र TSA प्रतिक्रिया, प्रमाणपत्र रद्दीकरण/संग्रहण सत्यापन और फोरेंसिक प्रमाणन रिकॉर्ड की गई योग्यता के बाहर बने रहते हैं। सहेजा गया MTProto स्टेट और कैच-अप लागू किए गए हैं; एटॉमिक ड्यूरबल रिप्ले अभी स्थापित नहीं है। एडमिन-लॉग संग्रह, अतिरिक्त रिएक्टर सूचियाँ और प्राथमिकता शॉर्ट पोलिंग अलग-अलग सुविधाएँ बनी हुई हैं। नियंत्रित योग्यता मैट्रिक्स के लिए [लाइव स्वीकृति](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md) देखें।

स्थानीय विस्तृत रसीदें और स्क्रीनशॉट test-results/ (Git-ignored) में हैं। docs/assets/ में सार्वजनिक स्क्रीनशॉट में केवल काल्पनिक प्रदर्शन डेटा है।
