# सुरक्षा और डेटा प्रबंधन

Canonical page: https://phishdestroy.github.io/TgWitness/hi/docs/reference/security/

थ्रेट मॉडल, एक्सेस मॉडल, रेस्ट में सिक्रेट्स, नेटवर्क एक्सपोजर, सेशन इम्पोर्ट्स और भेद्यता की रिपोर्ट कैसे करें।

[टीजीविटनेस](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [दस्तावेज़ीकरण](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Deployment and recovery](https://phishdestroy.github.io/TgWitness/hi/docs/reference/deployment/)

![Deployment & recovery](https://phishdestroy.github.io/TgWitness/assets/chapter-operate.svg)

This page describes access, storage and network protection in a local or server workspace. For collection on a GitHub runner or in an Intel TDX confidential VM, see the [verification modes](https://phishdestroy.github.io/TgWitness/hi/docs/reference/evidence/#verification-scope), which add checks of the collection environment. Account connections, notifications, timestamps, off-site copies and witnesses have their own routing settings.

| क्षेत्र | संक्षेप में |
| --- | --- |
| पहुँच | प्रशासक कुंजी और खातों/चैट्स तक सीमित पहुँच, सात अनुमतियाँ और रद्द की जा सकने वाली सत्र; डिफ़ॉल्ट रूप से लोकलहोस्ट |
| विश्राम में रहस्य | सत्र, एपीआई जोड़ी, हस्ताक्षर कुंजी और प्रॉक्सी सेटिंग्स Fernet के साथ एन्क्रिप्ट की जाती हैं |
| संदेश और मीडिया | अनएन्क्रिप्टेड संग्रहीत: डिस्क एन्क्रिप्शन और सख्त अनुमतियों का उपयोग करें |
| अखंडता | हर रिकॉर्ड पर SHA-256 हैश चेन और Ed25519 हस्ताक्षर |
| स्थानीय विश्वास सीमा | The host administrator controls the workspace and its signing key; independent checkpoints retain an earlier journal boundary |

कमजोरियों की रिपोर्टों के लिए, [सुरक्षा नीति](https://github.com/phishdestroy/TgWitness/blob/main/.github/SECURITY.md) देखें।

**On this page**

- [Access model](https://phishdestroy.github.io/TgWitness/hi/docs/reference/security/#access-model)
- [Panel content and exports](https://phishdestroy.github.io/TgWitness/hi/docs/reference/security/#panel-content-and-exports)
- [Secrets at rest](https://phishdestroy.github.io/TgWitness/hi/docs/reference/security/#secrets-at-rest)
- [Proxies and network routes](https://phishdestroy.github.io/TgWitness/hi/docs/reference/security/#proxies-and-network-routes)
- [Sign-in and session imports](https://phishdestroy.github.io/TgWitness/hi/docs/reference/security/#sign-in-and-session-imports)
- [Logs and transport](https://phishdestroy.github.io/TgWitness/hi/docs/reference/security/#logs-and-transport)
- [Integrity limits](https://phishdestroy.github.io/TgWitness/hi/docs/reference/security/#integrity-limits)
- [If you suspect a problem](https://phishdestroy.github.io/TgWitness/hi/docs/reference/security/#if-you-suspect-a-problem)

## पहुँच मॉडल

मुख्य पैनल टोकन पूर्ण नियंत्रण प्रदान करता है। अन्य लोग अपनी स्वयं की [सीमित पहुँच](https://phishdestroy.github.io/TgWitness/hi/docs/reference/access/) प्राप्त कर सकते हैं: चुने हुए वर्कस्पेस और चैट, अनुमतियाँ, समाप्ति, आईपी प्रतिबंध, साइन-इन सीमाएँ और रद्द की जा सकने वाली सत्र। चैट-सीमित पहुँच पूरे वर्कस्पेस के संचालन नहीं कर सकती, भले ही उनकी अनुमति टिक की गई हो। वर्कस्पेस एक प्रक्रिया साझा करते हैं और होस्ट प्रशासक से डेटा को अलग नहीं करते हैं।

पैनल डिफ़ॉल्ट रूप से लोकलहोस्ट पर सुनता है। ब्राउज़र साइन-इन एक सत्र क्रेडेंशियल के लिए एक्सेस टोकन का आदान-प्रदान करता है; ब्राउज़र इसे एक बेयरर टोकन के रूप में भेजता है। इसे प्रमाणीकरण कुकी के बजाय sessionStorage में रखा जाता है। लॉक/साइन-आउट ब्राउज़र सत्र को साफ़ कर देता है। ब्राउज़र बंद करने या सत्र समाप्त करने से संग्रह रुकता नहीं है।

जारी किए गए टोकन और सत्र क्रेडेंशियल एन्क्रिप्टेड वॉल्ट में हैश के रूप में रखे जाते हैं। रद्दीकरण संबंधित सत्रों को समाप्त कर देता है; अनुमति परिवर्तन बाद के अनुरोधों को प्रभावित करते हैं। डाउनलोड की गई फ़ाइलों को वापस नहीं लिया जा सकता। प्रशासक अपने स्वयं के ब्राउज़र सत्रों को भी सीमित कर सकते हैं, लेकिन मुख्य पैनल टोकन का सीधे उपयोग करने वाली स्क्रिप्ट्स पूरी पहुंच बनाए रखती हैं और उन ब्राउज़र-सत्र सीमाओं को बायपास कर देती हैं।

विफल प्रमाणीकरण क्लाइंट पते द्वारा दर-सीमित है। आईपी प्रतिबंध एप्लिकेशन द्वारा देखे गए पते का उपयोग करते हैं; इस पर भरोसा करने से पहले रिवर्स-प्रॉक्सी व्यवहार की जाँच करें। विटनेस क्रेडेंशियल अलग, केवल-पठन योग्य चेकपॉइंट/स्वास्थ्य क्रेडेंशियल होते हैं।

### डेमो एक्सेस

`/api/demo-access` एक स्पष्ट रूप से शुरू किए गए, अलग-थलग सिंथेटिक डेमो के लिए जानबूझकर बिना प्रमाणीकरण वाला बूटस्ट्रैप है। यह एक अलग प्रोसेस-लाइफटाइम क्षमता जारी करता है, कभी भी वास्तविक पैनल टोकन या TGWITNESS_TOKEN ओवरराइड नहीं। जारी करने और उपयोग करने के लिए एक लूपबैक पीयर और होस्ट की आवश्यकता होती है, कोई फॉरवर्डेड हेडर नहीं, और कोई क्रॉस-ओरिजिन अनुरोध नहीं। अतिरिक्त वर्कस्पेस या एक अधिकृत सत्र इस पथ को अक्षम कर देते हैं। लाइव वर्कस्पेस कभी भी इस क्षमता को जारी नहीं करते हैं। यह डेमो खातों को नहीं जोड़ सकता है या संग्रह सेटिंग्स को नहीं बदल सकता है।

## पैनल सामग्री और निर्यात

पैनल कोई बाहरी फ़ॉन्ट, एनालिटिक्स, CDN संसाधन, या एम्बेडेड रिमोट मीडिया का उपयोग नहीं करता है। टेलीग्राम-स्रोत पाठ को HTML के रूप में नहीं, बल्कि साधारण पाठ के रूप में डाला जाता है। डाउनलोड की गई अटैचमेंट्स को बाइनरी अटैचमेंट के रूप में परोसा जाता है। JSONL एक्सपोर्ट मूल स्ट्रिंग्स को संरक्षित करते हैं; HTML उन्हें एस्केप कर देता है; CSV सेल जिनके फ़ॉर्मूला बन सकते हैं, उनके सामने एक अपॉस्ट्रॉफ़ी लगा दी जाती है।

एक्सपोर्ट्स में प्रमाणीकरण और हस्ताक्षर रहस्य शामिल नहीं होते हैं, लेकिन जानबूझकर एकत्रित स्रोत मेटाडेटा, पहचानकर्ता, और संभवतः व्यक्तिगत या संवेदनशील सामग्री शामिल होती है। टेलीग्राम एक्सेस हैश और फ़ाइल संदर्भ कच्चे स्रोत मेटाडेटा में आ सकते हैं।

## विश्राम में रहस्य

Telegram API credentials, the session and signing key are encrypted with Fernet. For local messages and media, encryption is provided by the host's disk or volume; the workspace stores ordinary files. Exports can use a password-protected AES-256 ZIP, and off-site copies use AES-256-GCM.

The vault key defaults to the protected data directory. Use an external master-key file below to store it separately. On Unix, new private-key files use mode 0600 and new data directories use 0700; on Windows, set the directory ACL for the service account and authorized administrators. Existing directory permissions are retained.

### बाहरी मास्टर कुंजी

For a new data directory, TGWITNESS_VAULT_KEY_FILE can supply an external random master key. HKDF-SHA256 and a separate random salt derive a different Fernet key for each workspace. vault.external.json must be retained for recovery. Missing or wrong master keys fail closed. Existing local vaults are not silently migrated. The panel displays the selected key-storage mode. Disk encryption protects the local message and media files in either mode; see [connection and data protection](https://phishdestroy.github.io/TgWitness/hi/docs/reference/connection/) for setup details.

## प्रॉक्सी और नेटवर्क मार्ग

प्रॉक्सी कॉन्फ़िगरेशन वॉल्ट में एन्क्रिप्ट किया गया है। पासवर्ड और MTProxy सीक्रेट्स API द्वारा लौटाए नहीं जाते हैं या साक्ष्य रिकॉर्ड में लिखे नहीं जाते हैं। प्रत्येक वर्कस्पेस अपना टेलीग्राम रूट और एक [IP मोड](https://phishdestroy.github.io/TgWitness/hi/docs/reference/connection/#ip-modes) चुनता है।

**पता छिपाएँ** सीधे टेलीग्राम फॉलबैक को अस्वीकार करता है और बाहरी HTTP अनुरोधों के लिए एक प्रॉक्सी की आवश्यकता होती है। स्पष्ट रूप से चयनित फॉलबैक मोड इसकी देरी के बाद सीधे टेलीग्राम एक्सेस की अनुमति देता है; टनल/VPN मोड सीधे मार्गों की अनुमति देता है। टनल मोड चुनने से कोई VPN स्थापित या सत्यापित नहीं होता है। ये सेटिंग्स सभी मशीन ट्रैफ़िक, ब्राउज़र, पैकेज मैनेजर या स्थानीय प्रॉक्सी-होस्ट DNS समाधान को नियंत्रित नहीं करती हैं।

MTProxy केवल टेलीग्राम ट्रैफ़िक ले जाता है। बाहरी अनुरोध एक अलग SOCKS5/HTTP प्रॉक्सी, वर्कस्पेस के SOCKS5/HTTP रूट, या एक अनुमत सीधे रूट का उपयोग कर सकते हैं; इन्हें अक्षम भी किया जा सकता है। स्वतंत्र गवाह की अपनी ट्रांसपोर्ट सेटिंग्स होती हैं। साधारण SOCKS5/HTTP CONNECT प्रमाणीकरण स्वयं उन प्रॉक्सी प्रोटोकॉल द्वारा एन्क्रिप्ट नहीं किया जाता है। नकली TLS MTProxy रहस्य समर्थित नहीं हैं।

## साइन-इन और सत्र आयात

कन्वर्ट की गई .tgwitness-session फ़ाइलों में एक प्लेनटेक्स्ट ऑथराइज़ेशन सीक्रेट तब तक रहता है जब तक कि उन्हें वॉल्ट में लोड और स्टोर न किया जाए। ऑफ़लाइन CLI समीक्षा किए गए टेलीथॉन स्कीमा को स्वीकार करता है। पैनल आयात अतिरिक्त रूप से पायरोग्राम SQLite, आधुनिक एकल-खाते वाला TData ZIP, और प्रलेखित JSON इनपुट स्वीकार करता है। यह प्रमाणीकृत है, चार फ़ाइलों / 8 MiB तक सीमित है, और मूल फ़ाइलों को निकालने या सहेजने के बिना मेमोरी में अपलोड को संसाधित करता है। सामान्यीकृत क्रेडेंशियल केवल अनुरोध करने वाले प्रमाणीकृत ब्राउज़र को ही लौटाए जाते हैं; सफल टेलीग्राम प्राधिकरण के बाद उन्हें एन्क्रिप्टेड वॉल्ट में सहेजा जाता है। मूल और परिवर्तित फ़ाइलों की सुरक्षा करें, और एक प्राधिकरण को क्लोन करने वाले समवर्ती क्लाइंट्स से बचें।

TData प्रोसेसिंग कंटेनर चेक्सम, स्थानीय डिक्रिप्शन हैश, और संरचना की लंबाई को सत्यापित करती है। प्रदान किया गया डेस्कटॉप स्थानीय पासकोड अस्थायी रूप से उपयोग किया जाता है और संग्रहीत नहीं किया जाता है। यह सीमित पार्सर यह स्थापित नहीं करता है कि हर डेस्कटॉप संस्करण संगत है। क्यूआर छवियाँ स्थानीय रूप से उत्पन्न होती हैं, इनमें अल्पकालिक टेलीग्राम लॉगिन टोकन होते हैं, और इन्हें कभी भी किसी बाहरी रेंडरिंग सेवा पर नहीं भेजा जाता है। लॉक, वर्कस्पेस स्विच, नया लॉगिन, और मार्ग परिवर्तन लंबित क्यूआर प्रयासों को रद्द कर देते हैं। एक टैब को रीलोड/बंद करने से कोई प्रयास समाप्ति तक लंबित रह सकता है। एक सफल क्यूआर लॉगिन फिर भी खाते को बांधता है। साधारण एपीआई बॉडी 16 KiB तक सीमित रहती हैं; प्रमाणीकृत आयात मार्ग एन्कोडेड JSON के 12 MiB तक स्वीकार करता है, और अलग से छोटी डिकोडेड-फ़ाइल सीमा को लागू करता है।

लॉगिन कोड और टेलीग्राम दो-चरणीय सत्यापन पासवर्ड संग्रहीत नहीं किए जाते हैं। फोन नंबर/कोड-हैश की स्थिति प्राधिकरण के दौरान मेमोरी में रखी जाती है। टेलीग्राम सत्र खाते तक पहुंच प्रदान करते हैं; कभी भी GitHub पर कोई डेटा निर्देशिका, सत्र, टोकन, वॉल्ट कुंजी, या निजी हस्ताक्षर कुंजी अपलोड न करें।

## लॉग और परिवहन

डिफ़ॉल्ट एपीआई सत्यापन प्रतिक्रिया को बदला जाता है ताकि यह क्रेडेंशियल मानों को दोहराए नहीं। एप्लिकेशन एक्सेस लॉगिंग अक्षम है। प्राधिकरण हेडर या अनुरोध बॉडी को लॉग करने के लिए रिवर्स प्रॉक्सी कॉन्फ़िगर न करें। HTTP, टोकन और लॉगिन सीक्रेट को प्लेनटेक्स्ट में ले जाता है: जब भी लोकलहोस्ट से बाहर जा रहे हों तो HTTPS या SSH टनल का उपयोग करें।

## अखंडता सीमाएँ

Local verification checks record signatures, the hash chain, attachments and the export manifest. The administrator holds the local signing key and can create another signed journal; an independently retained checkpoint detects replacement of the prefix it covers. Keep the key fingerprint and checkpoints with the recipient or an independent witness.

For independently checked collection, choose [GitHub Actions capture](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md) or [Intel TDX deployment](https://phishdestroy.github.io/TgWitness/hi/docs/reference/high-assurance/#confidential-vm-on-phala-cloud-intel-tdx). Their verifiers check workflow provenance or hardware measurements in addition to archive integrity. Optional timestamps and encrypted off-site copies provide time anchors and recoverable copies; the [evidence format](https://phishdestroy.github.io/TgWitness/hi/docs/reference/evidence/#verification-scope) describes the checks for each mode.

## यदि आपको कोई समस्या संदेह हो

Preserve the original data directory and use a separate copy for analysis. Report the affected version, operation and reproducible steps through the [security policy](https://github.com/phishdestroy/TgWitness/blob/main/.github/SECURITY.md), keeping account data and credentials private.
