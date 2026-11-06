# खाते और सत्र प्रारूप

Canonical page: https://phishdestroy.github.io/TgWitness/hi/docs/reference/accounts/

फ़ोन, QR कोड या auth कुंजी से साइन इन करें, Telethon, Pyrogram या Telegram Desktop सत्र आयात करें, और कई खाते चलाएँ।

[टीजीविटनेस](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [दस्तावेज़ीकरण](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Getting started](https://phishdestroy.github.io/TgWitness/hi/docs/reference/quickstart/)

![Getting started](https://phishdestroy.github.io/TgWitness/assets/chapter-start.svg)

TgWitness, MTProto का उपयोग करते हुए, एक टेलीथॉन खाते से **टेलीग्राम उपयोगकर्ता खाते** (बॉट नहीं) के रूप में साइन इन करता है। प्रत्येक खाता अपने स्वयं के **कार्यक्षेत्र** (API और कमांड-लाइन टूल में जिसे *वर्कस्पेस* कहा जाता है) में रहता है, जिसमें उसका अपना सत्र, स्रोत, जर्नल और हस्ताक्षर कुंजी होती है।

सेशन फ़ाइलें, सेशन स्ट्रिंग्स और ऑथ कीज़ **खाता प्राधिकरण** हैं: जिसके पास इनमें से कोई भी हो, वह उस खाते के रूप में कार्य कर सकता है। इनमें संदेश इतिहास शामिल नहीं होता।

> [!चेतावनी] **किसी भी ऐसी चीज़ का उपयोग न करें जिसे आप खोने का जोखिम नहीं उठा सकते।** हम व्यक्तिगत या अन्यथा मूल्यवान खातों को जोड़ने, और किसी ऐसे खाते पर API ID / API हैश बनाने के खिलाफ दृढ़ता से सलाह देते हैं जिसे आप महत्व देते हैं। यह TgWitness के परीक्षण न किए जाने के बारे में नहीं है: टेलीग्राम अनिश्चित रूप से खातों को प्रतिबंधित करता है और स्थायी रूप से ब्लॉक कर देता है — अनुरोधों की उस मात्रा के लिए जिसे वह अत्यधिक मानता है, क्लाइंट या उद्देश्य की परवाह किए बिना, और बिना किसी पर्याप्त दस्तावेज़ीकरण के। कई प्रतिबंध अपरिवर्तनीय होते हैं। समर्पित खाते का उपयोग करें। सुचारू परीक्षण रन टेलीग्राम पर निर्भर करते हैं, न कि सॉफ़्टवेयर पर, और भविष्य के लिए कोई गारंटी नहीं देते हैं।

- [एक नज़र में](https://phishdestroy.github.io/TgWitness/hi/docs/reference/accounts/#at-a-glance)
- [शुरू करने से पहले: एपीआई आईडी और एपीआई हैश](https://phishdestroy.github.io/TgWitness/hi/docs/reference/accounts/#before-you-start-api-id-and-api-hash)
- [फ़ोन नंबर](https://phishdestroy.github.io/TgWitness/hi/docs/reference/accounts/#phone-number) · [क्यूआर कोड](https://phishdestroy.github.io/TgWitness/hi/docs/reference/accounts/#qr-code) · [ऑथ कुंजी + डीसी आईडी](https://phishdestroy.github.io/TgWitness/hi/docs/reference/accounts/#auth-key--dc-id)
- [खाता फ़ाइलें](https://phishdestroy.github.io/TgWitness/hi/docs/reference/accounts/#account-files): [टेलीथॉन .सेशन](https://phishdestroy.github.io/TgWitness/hi/docs/reference/accounts/#telethon-session) · [पायरोग्राम .सेशन](https://phishdestroy.github.io/TgWitness/hi/docs/reference/accounts/#pyrogram-session) · [सत्र + JSON जोड़ी](https://phishdestroy.github.io/TgWitness/hi/docs/reference/accounts/#session--json-pair) · [टीडेटा](https://phishdestroy.github.io/TgWitness/hi/docs/reference/accounts/#telegram-desktop-tdata) · [स्ट्रिंगसेशन](https://phishdestroy.github.io/TgWitness/hi/docs/reference/accounts/#telethon-stringsession) · [खाता JSON](https://phishdestroy.github.io/TgWitness/hi/docs/reference/accounts/#account-json)
- [पहचानें कि आपके पास क्या है](https://phishdestroy.github.io/TgWitness/hi/docs/reference/accounts/#identify-what-you-have) · [असमर्थित प्रारूप](https://phishdestroy.github.io/TgWitness/hi/docs/reference/accounts/#unsupported-formats)
- [कई खाते](https://phishdestroy.github.io/TgWitness/hi/docs/reference/accounts/#multiple-accounts) · [खाता फ़ाइलों को सुरक्षित रखना](https://phishdestroy.github.io/TgWitness/hi/docs/reference/accounts/#keeping-account-files-safe) · [समस्या निवारण](https://phishdestroy.github.io/TgWitness/hi/docs/reference/accounts/#troubleshooting)

## एक नज़र में

| आपके पास क्या है | खाता जोड़ें टैब | आपको इनकी भी आवश्यकता होगी |
| --- | --- | --- |
| फ़ोन नंबर और उसके लॉगिन कोड्स तक पहुँच | फ़ोन | यदि सक्षम हो तो 2FA पासवर्ड |
| दूसरे डिवाइस पर टेलीग्राम खुला है | **क्यूआर कोड** | यदि सक्षम हो तो 2FA पासवर्ड |
| `.session` फ़ाइल (टेलीथॉन या पायरोग्राम) | **फ़ाइलें** | ऐप सेटिंग्स के लिए वैकल्पिक साथी JSON |
| `.session` + `.json` समान नाम के साथ | **फ़ाइलें** (दोनों चुनें) | आमतौर पर और कुछ नहीं |
| एक टेलीग्राम डेस्कटॉप `tdata` फ़ोल्डर | **फ़ाइलें** (ZIP के रूप में) | यदि डेस्कटॉप स्थानीय पासकोड सेट किया गया हो तो वह |
| एक टेलीथॉन स्ट्रिंगसेशन (टेक्स्ट, `.txt`, `.tgwitness-session`) | **फ़ाइलें** | अलग API जोड़ी की आवश्यकता नहीं |
| `.json`, एक सत्र या ऑथ कुंजी के साथ | **फ़ाइलें** | अलग API जोड़ी की आवश्यकता नहीं |
| एक ऑथ की (512 हेक्स वर्ण) और उसका डीसी नंबर | **ऑथ कुंजी** | वैकल्पिक उपयोगकर्ता आईडी |

TgWitness फ़ाइलों को उनके नाम से नहीं, बल्कि उनकी **सामग्री** से पहचानता है। किसी फ़ाइल का नाम बदलने से वह कभी भी परिवर्तित नहीं होती।

## शुरू करने से पहले: एपीआई आईडी और एपीआई हैश

You can sign in without creating a Telegram API application. When no pair is entered, imported or already saved in the workspace, TgWitness picks a pair from its built-in pool of 50 public API pairs (`tgwitness/api_pool.py`), preferring Telegram Desktop for a fresh login and retaining a saved pair first; remaining candidates are shuffled. If Telegram refuses a pair (`API_ID_INVALID`, `API_ID_PUBLISHED_FLOOD`, `UPDATE_APP_TO_LOGIN`), the next one is tried, up to eight per sign-in; refused pairs are skipped until restart. The pair that signed in is saved with the account and reused for it. An **API ID** and **API hash** identify the application to Telegram; they do not authorize an account by themselves.

Missing connection fields use a deterministic device/OS pair from the bundled [opentele2 2.0.0 catalogs](https://github.com/DedInc/opentele2/tree/7e973bc71cd7a714ad13ac703c0895a90d36a735): Desktop `2040`, Android `6`, Android X `21724`, iOS `10840`, macOS `2834`, and Web `2496`. Android's source-build ID `4` also uses the Android catalog, as identified in [Telegram Android's BuildVars](https://github.com/DrKLO/Telegram/blob/master/TMessagesProj/src/main/java/org/telegram/messenger/BuildVars.java). Web defaults to A; an imported `K` app-version suffix or `macos` language pack selects K, and version `0.7.0` selects Webogram. Unknown application IDs keep Telethon's host defaults. Imported fields always win, including an older app version and an empty language pack. The catalog never changes the API ID/hash. Its version snapshot is reviewed explicitly, not fetched during login. A saved profile stays stable after updates.

`account.getAuthorizations` reports Telegram's saved authorization metadata; it is not an echo of each new `initConnection`. Compare it with the actual sent profile. Connecting an existing authorization does not validate its companion API hash: `initConnection` sends the API ID, while the hash is used by login requests.

After a new phone or QR authorization, TgWitness requests config, nearest DC, online status, languages (when the language pack is nonempty), app updates and terms-of-service updates, with 0.3–1.5 seconds between requests. Updating status briefly marks the account online. This sequence runs once at login completion, not on imports, reconnects or restarts. The authorization is saved first; a failed request stops the sequence without retrying or discarding the login. Results are recorded as `account.initialized`, with error names rather than response bodies. The sequence is not a guarantee against account restrictions.

For `tdesktop`, a missing `tz_offset` uses the server's local UTC offset, rounded to 900 seconds using the [opentele2 algorithm](https://github.com/DedInc/opentele2/blob/7e973bc71cd7a714ad13ac703c0895a90d36a735/crates/opentele2-core/src/fingerprint.rs) (MIT; license in `tgwitness/client_profiles.LICENSE`). It is refreshed on each connection so daylight-saving changes are reflected. An imported `tz_offset` takes precedence on every platform and is kept exactly, including zero. Other `initConnection.params` entries are retained. The HTTP sign-in form accepts the numeric timezone returned by file import; booleans, fractions and offsets outside the supported range are rejected.

Direct, SOCKS5 and HTTP CONNECT routes use Telethon's `ConnectionTcpObfuscated` (obfuscated abridged MTProto). HTTPS CONNECT retains TLS to the proxy and uses the same obfuscated transport inside the tunnel. MTProxy retains its required randomized intermediate transport and secret handling. Route switches apply the same choices. Obfuscation changes packet framing; it does not hide the account or its client metadata from Telegram or imply immunity to restrictions.

After connecting an authorized client, TgWitness checks config, nearest DC, the current authorization, the reviewed layer baseline, languages, app updates and terms-of-service updates. These diagnostics run once per client instance, before collection, and are shown under the connection details with their time. `account.connection_checked` records the result without session hashes, IPs, tokens or API hashes. They never accept terms or install updates. A request failure or FloodWait stops subsequent requests; a missing result stays unknown. Local checks can still report their results while network checks are skipped.

FloodWait diagnostics retain the failed TL method, any Takeout/range wrappers, the server-requested wait and the effective deadline in `telegram.backoff`. Connection details show the method and deadline while requests are paused. The diagnostic includes per-method client-call counters since that client was created; they count nested peer resolution separately, but do not count packets or Telethon's internal retry attempts. Current counters are also available as `collector.rpc_activity` in the status API. No request arguments, usernames, access hashes or exception text are included. The last diagnostic and full deadline survive restart. Earlier waits without a method record cannot be attributed retrospectively. See [export limits](https://github.com/phishdestroy/TgWitness/blob/main/docs/EXPORT-LIMITS.md) for the source review and the distinction between discovery and history acquisition.

`official_app=True` or `False` is Telegram's current-authorization flag. Neither value establishes whether the account is restricted, trusted or under observation. The existing evidence-mode `account.devices` snapshots remain the history of all signed-in devices; connection diagnostics retain only the current device description.

Before connection, advisory checks compare the API platform, language pack, device/OS and app-version formats, mobile system locale, and Telethon's actual schema layer against the reviewed catalog baseline. Warnings appear in the server log and account status metadata; they never replace imported values or change the schema layer. A different layer is a compatibility review signal, not proof of a broken or restricted account. These checks and `official_app` do not certify that Telegram considers the account safe from restrictions. Disconnected account status uses the saved profile instead of generating another device description.

इसके बजाय अपना स्वयं का एप्लिकेशन उपयोग करने के लिए (जिसे पंजीकृत करने वाला खाता जोखिम में है; देखें: [अंतर्निहित API पूल क्यों?](https://github.com/phishdestroy/TgWitness/blob/main/docs/PROJECT-GUIDE.md#connect-a-telegram-account))

1. [my.telegram.org](https://my.telegram.org) खोलें और अपने किसी भी फोन नंबर से साइन इन करें। कोड Telegram ऐप में आता है, SMS से नहीं।
2. **API विकास उपकरण** चुनें।
3. एक एप्लिकेशन बनाएँ: कोई भी शीर्षक और संक्षिप्त नाम (5–32 अक्षर), प्लेटफ़ॉर्म **डेस्कटॉप**। URL और विवरण खाली रह सकते हैं।
4. **ऐप का api_id** (एक संख्या) और **api_hash** (32 हेक्साडेसिमल अक्षर) कॉपी करें।

पैनल में, साइन-इन फ़ॉर्म के नीचे **API ID + हैश** खोलें। आप एक ही `api_id:api_hash` जोड़ी को **API ID** में पेस्ट कर सकते हैं और दोनों फ़ील्ड भर जाएँगे। एक जोड़ी का उपयोग आपके सभी खातों के लिए किया जा सकता है। सफल लॉगिन के बाद यह केवल उसी वर्कस्पेस में सहेजा, एन्क्रिप्ट किया जाता है और कभी भी ब्राउज़र में वापस नहीं भेजा जाता है।

तीन अलग-अलग क्रेडेंशियल शामिल हैं:

| गोपनीय | खोलता है | यह कहाँ स्थित है |
| --- | --- | --- |
| पैनल टोकन | TgWitness वेब पैनल | `panel-token.txt` डेटा निर्देशिका में, या `TGWITNESS_TOKEN` |
| एपीआई आईडी + हैश | अपने आप में कुछ नहीं; ऐप की पहचान करता है | बिल्ट-इन जोड़ी, आयातित सेटिंग्स, या my.telegram.org पर आपका अपना ऐप |
| खाता प्राधिकरण | टेलीग्राम खाता | फ़ोन/QR लॉगिन द्वारा बनाया गया या सत्र के रूप में लाया गया |

यदि टेलीग्राम तक पहुँचने के लिए प्रॉक्सी का उपयोग करना आवश्यक हो, तो पहले इसे **Account → Settings → Connection settings → Change connection route** में सेट करें।

## फ़ोन नंबर

1. खाता खोलें, फ़ोन टैब पर जाएँ, और नंबर अंतरराष्ट्रीय प्रारूप में दर्ज करें, उदाहरण के लिए `+44 7700 900123`। रिक्त स्थान और डैश स्वचालित रूप से हटा दिए जाते हैं।
2. **Continue** दबाएँ। API ID + हैश खाली रह सकते हैं।
3. Telegram द्वारा भेजा गया कोड दर्ज करें (आमतौर पर Telegram ऐप में; SMS की गारंटी नहीं)।
4. यदि खाते में दो-चरणीय सत्यापन है, तो वह पासवर्ड दर्ज करें। यह पैनल टोकन नहीं है और न ही डिवाइस पासकोड है।
5. लॉगिन के बाद प्रदर्शित खाता आईडी की जाँच करें, फिर स्रोत चुनें।

लॉगिन कोड और 2FA पासवर्ड कभी भी डिस्क पर लिखे नहीं जाते।

## क्यूआर कोड

जब खाता पहले से ही फोन या किसी अन्य कंप्यूटर पर साइन इन हो, तब इसका उपयोग करें।

1. **QR कोड** टैब → **QR कोड दिखाएँ**। API ID + हैश खाली रह सकते हैं।
2. साइन-इन किए गए डिवाइस पर: **सेटिंग्स → डिवाइस → डेस्कटॉप डिवाइस लिंक करें**, कोड स्कैन करें और पुष्टि करें।
3. यदि टेलीग्राम अनुरोध करता है तो TgWitness में 2FA पासवर्ड दर्ज करें।

QR छवि स्थानीय रूप से उत्पन्न होती है। कोड समाप्त हो जाते हैं; दोबारा प्रयास करने के लिए **'एक और QR कोड उत्पन्न करें'** पर क्लिक करें। पैनल को लॉक करने, कार्यक्षेत्र बदलने या दूसरा लॉगिन शुरू करने से लंबित कोड रद्द हो जाता है।

## ऑथ कुंजी + डीसी आईडी

एक ऑथ की हर टेलीग्राम सत्र के पीछे का कच्चा 256-बाइट प्राधिकरण है, जिसे डेटा-सेंटर नंबर **DC 1–5** के साथ, **512 हेक्साडेसिमल अक्षरों** के रूप में लिखा जाता है।

1. टैब **'Auth कुंजी**'। पूरी कुंजी पेस्ट करें; `…` वाली संक्षिप्त कुंजी काम नहीं करेगी।
2. कुंजी के साथ प्रदान किया गया DC ID चुनें।
3. वैकल्पिक रूप से **उपयोगकर्ता आईडी** दर्ज करें। यदि टेलीग्राम कोई अलग खाता रिपोर्ट करता है तो TgWitness कनेक्ट करने से इनकार कर देता है।
4. Press **Connect खाता**।

एक ऑथ की (512 वर्ण) कोई एपीआई हैश (32 वर्ण) नहीं है। उसी की को JSON के रूप में भी आयात किया जा सकता है, देखें [खाता JSON](https://phishdestroy.github.io/TgWitness/hi/docs/reference/accounts/#account-json)।

## खाता फ़ाइलें

ओपन पर जाएँ, **'खाता जोड़ें' → 'फ़ाइलें'** चुनें और **एक ही खाते की** अधिकतम **चार फ़ाइलें** (कुल **8 MiB**) चुनें, फिर **'खाता कनेक्ट करें'** दबाएँ।

The **Files**, **Auth key** and bulk-import forms show the parallel-session warning before connecting. By default imported authorizations are reused. Keep the original client closed while its key is in use here. **Files** and **Auth key** also offer **Create an independent authorization**, described below. Bulk import still uses the direct mode. Phone and interactive QR login create separate authorizations. The warning heading stays visible in the import form; its full explanation opens automatically when files or a key/session string are supplied. It can be collapsed after reading, so the file picker and connection controls remain usable on a phone.

- फ़ाइलें आपके TgWitness सर्वर की मेमोरी में ही परिवर्तित की जाती हैं। अपलोड्स संग्रहीत नहीं किए जाते, ZIP फ़ाइलें डिस्क पर एक्सट्रेक्ट नहीं की जातीं और किसी भी बाहरी सेवा से संपर्क नहीं किया जाता।
- फिर इस सत्र की जाँच टेलीग्राम के साथ की जाती है। यदि कोई फ़ाइल उपयोगकर्ता आईडी बताती है, तो उसका मिलान टेलीग्राम द्वारा रिपोर्ट किए गए खाते से होना चाहिए।
- विभिन्न खातों या विभिन्न API क्रेडेंशियल्स का वर्णन करने वाली फ़ाइलें अस्वीकार की जाती हैं, एक को चुनने के बजाय।
- **पासकोड या सत्र टेक्स्ट** में TData स्थानीय पासकोड फ़ील्ड होता है, जो **बिना साइन इन किए** स्ट्रिंगसेशन और **रीड फ़ाइलें** पेस्ट करने के लिए एक बॉक्स है (टेलिग्राम से संपर्क किए बिना फ़ॉर्म भरता है)।

### Create an independent authorization

Select **Create an independent authorization** before connecting imported files or an Auth Key. TgWitness connects the imported donor briefly, uses it to approve the new client's QR login token, and disconnects the donor immediately after approval. The new client has its own authorization key and a separately selected Desktop profile. The donor's supplied API credentials and device profile are used only for the donor connection. No existing authorization is logged out or revoked.

**Keep the donor's original client fully closed during this step.** The initial connection still uses its copied key, so this mode cannot remove that initial parallel-use risk. Once the new authorization is connected, the owner can reopen the original client and use both independently. Interactive **QR code** login lets the original client approve the login without copying or connecting its key here.

If Telegram requests 2FA, this mode uses `twoFA` from the selected JSON when present, or asks for the password. A rejected imported password returns to the password form. Passwords are not saved. The candidate key is saved encrypted in `independent_login.enc`, including changes during data-centre migration. After an interruption, select the same donor and this option to resume the saved candidate. The workspace remains reserved for that account; failed completion does not delete the new workspace. Keep its data directory and vault key. The final credentials and `account.authorized` journal record include the import method, input formats and donor API ID, without the donor key or password.

On 5 November 2026, a dedicated account passed live checks with Telethon, Pyrogram and TData donors: 2FA completion, distinct new authorization keys, concurrent access by the donor and new client, and reading a public channel. The Telethon case also resumed a saved candidate after an interruption at the password step. Each new authorization completed the six post-login initialization requests, and its signed journal verified. The original session remained usable in all four supplied formats.

Telegram's [RPC error database](https://core.telegram.org/api/errors.json) associates `FRESH_CHANGE_ADMINS_FORBIDDEN` with changing admins, `FRESH_CHANGE_PHONE_FORBIDDEN` with changing the phone number, and `FRESH_RESET_AUTHORISATION_FORBIDDEN` with revoking other sessions, changing their lifetime or registering a passkey. `SESSION_TOO_FRESH_*` and `PASSWORD_TOO_FRESH_*` concern ownership transfers and revenue or gift withdrawals. These are not collection operations; a new login does not imply a blanket 24-hour reading ban. Export can separately return `TAKEOUT_INIT_DELAY_*`. TgWitness retains server-requested pauses and does not retry token acceptance automatically or revoke sessions to work around restrictions.

### टेलीथन `.session`

|  |  |
| --- | --- |
| यह क्या है | SQLite डेटाबेस जो Telethon-आधारित उपकरण बनाते हैं, उदाहरण के लिए `my_account.session` |
| द्वारा मान्यता प्राप्त | तालिकाएँ `sessions` (`dc_id`, `server_address`, `port`, `auth_key`) और `version` = 7 या 8 |
| आवश्यकताएँ | ठीक एक अधिकृत सत्र पंक्ति; एक बंद, पूर्ण डेटाबेस |

सबसे पहले उस प्रोग्राम को बंद करें जिसने फ़ाइल बनाई है। यदि इसके बगल में `my_account.session-journal` या `my_account.session-wal` मौजूद है, तो डेटाबेस अंतिम नहीं है: मूल क्लाइंट को साफ़-सुथरे तरीके से खोलें और बंद करें। उन साइडकार फ़ाइलों को हटाने से एक टूटी हुई कॉपी रह सकती है।

### पायरोग्राम `.session`

|  |  |
| --- | --- |
| यह क्या है | SQLite डेटाबेस जो Pyrogram-आधारित उपकरण बनाते हैं |
| द्वारा मान्यता प्राप्त | `sessions` को `dc_id`, `auth_key`, `test_mode`, `user_id`, `is_bot` के साथ तालिकाबद्ध करें; `version` = 2 या 3 |
| आवश्यकताएँ | प्रोडक्शन नेटवर्क पर एक अधिकृत **उपयोगकर्ता** सत्र। बॉट और टेस्ट-डीसी सत्र अस्वीकार किए जाते हैं। |

लॉगिन के दौरान संग्रहीत उपयोगकर्ता आईडी की टेलीग्राम के साथ जांच की जाती है।

### सत्र + JSON जोड़ी

खातों को अक्सर एक ही नाम वाली दो फ़ाइलों के रूप में वितरित किया जाता है, उदाहरण के लिए `447700900123.session` और `447700900123.json`। एक साथ दोनों चुनें।

- JSON से, TgWitness `app_id`/`api_id` और `app_hash`/`api_hash` का उपयोग करता है, इसलिए आपको आमतौर पर API क्रेडेंशियल टाइप नहीं करने पड़ते।
- The connection profile uses `device_model` (alias `device`), `system_version` (alias `sdk`), `app_version`, `lang_code`, `system_lang_code` (alias `system_lang_pack`), `lang_pack` and optional `tz_offset` (seconds from UTC, -43200 to 50400). Supplied fields take priority over generated defaults and the panel/browser language. Conflicting aliases are rejected. The resolved profile is saved in the encrypted workspace credentials and reused after restart, including its app version.
- `phone`, proxy settings and device tokens are **ignored**. `twoFA` is read only when **Create an independent authorization** is selected; direct import ignores it.
- A JSON without a supported authorization field is only metadata. Add its session file or continue with phone or QR login. A JSON containing a supported session or Auth Key can authorize on its own; see [Account JSON](https://phishdestroy.github.io/TgWitness/hi/docs/reference/accounts/#account-json).

### टेलीग्राम डेस्कटॉप (TData)

TData टेलीग्राम डेस्कटॉप एप्लिकेशन का`tdata` फ़ोल्डर है (desktop.telegram.org से क्रॉस-प्लेटफ़ॉर्म ऐप)।

| सिस्टम | डिफ़ॉल्ट `tdata` स्थान |
| --- | --- |
| विंडोज | `%APPDATA%\Telegram Desktop\tdata` (पोर्टेबल टेलीग्राम: `Telegram.exe` के बगल में) |
| लिनक्स | `~/.local/share/TelegramDesktop/tdata` |
| macOS | `~/Library/Application Support/Telegram Desktop/tdata` |

इसे आयात करने के लिए:

> **Parallel session warning.** Direct TData import reuses Telegram Desktop's authorization key. Do not use that key in Desktop and TgWitness simultaneously. Telegram can invalidate the authorization with `AUTH_KEY_DUPLICATED`, leaving both copies unusable until a new login.
>
>
>
> Fully quit Desktop, including its tray process, and keep that copy closed while TgWitness uses the imported session. **Quit, do not log out or revoke the session:** revocation also invalidates the imported copy. If you need both clients running, select **Create an independent authorization** and keep Desktop closed until the new login succeeds, or sign in to TgWitness by phone or QR. A dedicated account is recommended, but does not make cloned keys safe to use in parallel.
>
>
>
> यह आयातित पर भी लागू होता है `.session` फ़ाइलें, StringSession टेक्स्ट और Auth Key HEX पर भी लागू होता है। अन्य क्लाइंट जो अपने स्वयं के स्वतंत्र रूप से बनाए गए प्राधिकरणों के साथ हैं, वे साइन इन रह सकते हैं। [Telegram का AUTH_KEY_DUPLICATED दस्तावेज़](https://core.telegram.org/api/errors#406-not-acceptable) देखें।

1. Telegram डेस्कटॉप को पूरी तरह से बंद करें।
2. `tdata` से **केवल** इन दो आइटमों वाली एक ZIP बनाएं:

   - `key_datas`
   - 16-अक्षर वाली फ़ाइल जिसका अंत `s` पर होता है, उसके बगल में, आमतौर पर `D877F783D5D3EF8Cs`

   मीडिया कैश के साथ पूरे फ़ोल्डर को ज़िप करने पर आमतौर पर सीमा (512 प्रविष्टियाँ, 32 MiB अनपैक) से अधिक हो जाता है। 3. **फ़ाइल्स** में ज़िप चुनें। यदि टेलीग्राम डेस्कटॉप का कोई **स्थानीय पासकोड** है, तो पहले उसे **पासकोड या सत्र टेक्स्ट** के तहत दर्ज करें। यह 2FA पासवर्ड नहीं है।

समर्थित: प्रति आर्काइव एक खाता, आधुनिक `key_datas`/`key_data0`/`key_data1` स्टोरेज, स्थानीय पासकोड। समर्थित नहीं: कई लॉग-इन खातों वाले फ़ोल्डर, पुराने डेस्कटॉप लेआउट, पासवर्ड-संरक्षित ज़िप्स, और अलग नेटिव macOS ऐप "Telegram for macOS"।

### टेलीथॉन स्ट्रिंगसेशन

टेक्स्ट की एक पंक्ति, जो आमतौर पर `1` से शुरू होती है और लगभग 350 वर्णों की लंबी होती है। इसे `.txt` या `.tgwitness-session` फ़ाइल (अधिकतम 4 KiB) के रूप में लोड करें, या इसे **पासकोड या सेशन टेक्स्ट** के तहत पेस्ट करें। केवल टेलीथॉन स्ट्रिंग्स स्वीकार किए जाते हैं; पायरोग्राम और TDLib स्ट्रिंग्स अलग प्रारूपों का उपयोग करते हैं।

### खाता JSON

एक JSON ऑब्जेक्ट, अधिकतम **64 KiB**, **`.json`** पर समाप्त होने वाली फ़ाइल में।

| क्षेत्र (उपनाम) | अर्थ |
| --- | --- |
| `api_id` (`app_id`) | एप्लिकेशन आईडी, एक धनात्मक संख्या |
| `api_hash` (`app_hash`) | एप्लिकेशन हैश, 32 हेक्साडेसिमल अक्षर |
| `string_session` (`session_string`, `session_str`; legacy `session`) | Telethon StringSession टेक्स्ट, फ़ाइल नाम नहीं |
| `auth_key` (`auth_key_hex`) + `dc_id` | 512-अक्षर की ऑथ कुंजी और DC 1–5 पूरा करें |
| `user_id` (`id`) | वैकल्पिक; प्राधिकरण सहेजे जाने से पहले टेलीग्राम के साथ जांचा जाता है |
| `device_model` (`device`) | Connection device description |
| `system_version` (`sdk`) | Connection OS version |
| `app_version` | Application version sent to Telegram |
| `lang_code`, `system_lang_code` (`system_lang_pack`), `lang_pack` | Client language, system language and client language pack; an empty `lang_pack` is allowed |
| `tz_offset` | Optional UTC offset in seconds, sent in `initConnection.params`; integer or decimal integer string |

If both an alias and the main name are present, they must agree. Explicit Telethon session fields take priority over a generic `session` blob in another format. If both contain recognizable Telethon sessions, they must describe the same authorization. Without an explicit field, `session` must be a valid Telethon StringSession. Examples:

```
{ "app_id": 1234567, "app_hash": "0123456789abcdef0123456789abcdef" }
```

```
{
  "api_id": 1234567,
  "api_hash": "0123456789abcdef0123456789abcdef",
  "auth_key": "REPLACE_WITH_ALL_512_HEXADECIMAL_CHARACTERS",
  "dc_id": 2,
  "user_id": 123456789
}
```

पहला उदाहरण केवल API क्रेडेंशियल भरता है; फोन या QR से साइन इन करें, या एक सत्र फ़ाइल जोड़ें। बल्क सूचियाँ (खातों की एक JSON ऐरे) स्वीकार नहीं की जाती हैं।

## पहचानें कि आपके पास क्या है

| आप देखते हैं | यह है | उपयोग करें |
| --- | --- | --- |
| `*.session`; इसे टेक्स्ट एडिटर में खोलने पर शीर्ष पर `SQLite format 3` दिखता है | टेलीथॉन या पायरोग्राम SQLite | **फ़ाइलें** (स्वचालित रूप से पता लगाई गई) |
| `tdata` नामक एक फ़ोल्डर जिसमें `key_datas` शामिल है | टेलीग्राम डेस्कटॉप टीडेटा | दो फ़ाइलों को ज़िप करें, फिर **फ़ाइलें** |
| `1` से शुरू होने वाली एक टेक्स्ट लाइन, लगभग 350 अक्षर | टेलीथॉन स्ट्रिंगसेशन | **फ़ाइलें** |
| `*.json` के साथ `app_id`/`app_hash` | सहायक मेटाडेटा | **फ़ाइलें**, इसके सत्र के साथ |
| `*.json` के साथ `auth_key` या `string_session` | खाता JSON | **फ़ाइलें** |
| 512 वर्ण `0-9a-f` | ऑथ कुंजी | **ऑथ कुंजी** |
| 32 वर्ण `0-9a-f` | एपीआई हैश | **एपीआई आईडी + हैश** |
| TDLib ऐप से `td.binlog` या `db.sqlite` | TDLib स्टोरेज | समर्थित नहीं |
| `123456789:AA…` | बॉट टोकन | समर्थित नहीं |

## असमर्थित प्रारूप

| फ़ॉर्मेट | वैकल्पिक |
| --- | --- |
| TDLib स्टोरेज (`td.binlog`) और TDLib एक्सपोर्ट्स | फ़ोन या QR से साइन इन करें |
| पायरोग्राम सत्र स्ट्रिंग्स | Pyrogram फ़ाइल `.session` का उपयोग करें, या फ़ोन/QR |
| कई लॉग-इन खातों वाला TData | Telegram Desktop में अन्य खातों से लॉग आउट करें, या प्रत्येक खाते की अपनी सत्र फ़ाइल का उपयोग करें |
| बॉट टोकन | समर्थित नहीं: TgWitness एक उपयोगकर्ता खाते के रूप में अवलोकन करता है |
| कई खातों की CSV/JSON सूचियाँ | **खाते → खातों को आयात करें** के माध्यम से समर्थित सेशन फ़ाइलें आयात करें, या अलग-अलग वर्कस्पेस में फ़ोन/QR द्वारा साइन इन करें |
| टेस्ट-डीसी या बॉट सत्र | एक प्रोडक्शन उपयोगकर्ता खाता उपयोग करें |

## कई खाते

खाता चयनकर्ता के बगल में **+** दबाएँ, या **खाता → सेटिंग्स → कनेक्शन सेटिंग्स → वर्कस्पेस** खोलें, एक लेबल दर्ज करें और साइन इन करें।

- मुख्य सहित किसी भी संख्या में वर्कस्पेस। प्रत्येक का अपना सत्र, प्रॉक्सी मार्ग, स्रोत, कैप्चर नीति, जर्नल, हस्ताक्षर कुंजी, चेकपॉइंट और एक्सपोर्ट होते हैं।
- प्रदर्शित कार्यक्षेत्र को बदलने से अन्य कार्यक्षेत्र रुके नहीं हैं।
- एक जर्नल उसे बनाने वाले खाते से बंधा रहता है। एक अलग खाते से साइन इन करने के लिए एक अन्य वर्कस्पेस की आवश्यकता होती है, और एक खाते को दो वर्कस्पेस में असाइन नहीं किया जा सकता।
- मुख्य पैनल टोकन सभी वर्कस्पेस को नियंत्रित करता है। [जारी की गई पहुँच](https://phishdestroy.github.io/TgWitness/hi/docs/reference/access/) अन्य लोगों को चयनित खातों और चैट्स तक सीमित कर सकती है, अलग-अलग अनुमतियों और सत्र सीमाओं के साथ।
- **अकाउंट्स** एक वर्कस्पेस का नाम बदलता है और एक जोड़े गए वर्कस्पेस को उसके सत्र, जर्नल, स्रोतों और साइनिंग की के साथ हटा देता है। मुख्य वर्कस्पेस को पैनल से हटाया नहीं जा सकता।

### एक साथ आयात और खाता समूह

एकाधिक खाते जोड़ने, फ़ाइलों को बेसनेम के अनुसार जोड़ी बनाने और प्रत्येक लॉगिन परिणाम को देखने के लिए **खातों → खाते आयात करें**का उपयोग करें। प्रत्येक खाते को अपना स्वयं का वर्कस्पेस मिलता है।

एक समूह संबंधित खातों को उनके सत्रों, कुंजियों या साक्ष्यों को मर्ज किए बिना एक साथ रखता है। **खातों** पर **समूह खोलने से** यह उसके पृष्ठ पर ले जाता है `/groups/<id>`:

- **खाते:** प्रत्येक सदस्य का कनेक्शन मार्ग, अवलोकन और अंतिम संदेश, साथ ही **सभी** प्रारंभ करें और **सभी को रोकें**।
- **ध्यान देने की ज़रूरत:** वे खाते जो साइन आउट किए गए हैं, अनुपलब्ध हैं या जिनमें कनेक्शन, इनटेक, स्रोत या मीडिया की समस्या है; प्रत्येक नाम उसके कार्ड की ओर ले जाता है।
- **चैट्स कई खाते देख सकते हैं:** साझा स्रोत, उन्हें देखने वाले खाते और उपलब्ध कार्यक्षेत्र-निरीक्षण अवधि (सात दिनों तक) में रुकावटें। **N खातों के साथ एक्सपोर्ट** एक चैनल या सुपरग्रुप एक्सपोर्ट को उनके बीच विभाजित करता है और एक आर्काइव पर हस्ताक्षर करता है।
- **समूह निर्यात:** प्रत्येक खाते के हस्ताक्षरित एक्सपोर्ट के साथ एक ZIP `accounts/` और `manifest.json` उनके SHA-256 और कुंजी फिंगरप्रिंट्स की सूची, मुख्य द्वारा हस्ताक्षरित कार्यक्षेत्र में `manifest.signature.json`प्रत्येक खाते के आर्काइव को उसके स्वयं के साथ सत्यापित करें `python -m tgwitness.verify` और उस खाते के विश्वसनीय फिंगरप्रिंट के साथ।

सदस्य समूह की सेटिंग्स साझा करते हैं; एक खाता अपने स्वयं के मान रख सकता है। [साझा सेटिंग्स](https://phishdestroy.github.io/TgWitness/hi/docs/reference/settings/#account-groups), [आयात और समूह गाइड](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Accounts.md#import-accounts-and-share-settings) और [MTProxy पूल डैशबोर्ड](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Proxies.md#pool-dashboard-and-custom-sources) देखें।

## साइन आउट

**खाता → टेलीग्राम से साइन आउट करें** (निरीक्षण रुका हुआ) टेलीग्राम से सत्र समाप्त करने के लिए कहता है, ताकि यह खाते की **सेटिंग्स → डिवाइस** से भी गायब हो जाए, और कार्यक्षेत्र वॉल्ट से सत्र को हटा दे। जर्नल, स्रोत, सेटिंग्स और साइनिंग कुंजी बनी रहती हैं, और जर्नल साइन-आउट को रिकॉर्ड करता है। वर्कस्पेस अभी भी उसके खाते का है: केवल वही खाता फिर से इससे जुड़ सकता है। यदि टेलीग्राम जवाब नहीं देता है, तो सत्र यहां से फिर भी हटा दिया जाता है और पैनल ऐसा ही बताता है; टेलीग्राम में **सेटिंग्स → डिवाइस** के तहत इसे समाप्त करें।

## खाता फ़ाइलों को सुरक्षित रखना

- हर `.session`, TData ZIP, StringSession, Auth Key और account JSON को एक पासवर्ड की तरह मानें। TgWitness आयातित प्राधिकरण को अपने एन्क्रिप्टेड वॉल्ट में रखता है; आप बाद में मूल फ़ाइलें हटा सकते हैं।
- एक ही प्राधिकरण को एक साथ दो प्रोग्रामों में न चलाएँ। टेलीग्राम इसे रद्द कर सकता है (`AUTH_KEY_DUPLICATED`), और दोनों प्रतियाँ काम करना बंद कर देंगी।
- समाप्त या रद्द किया गया सत्र रूपांतरण द्वारा पुनर्जीवित नहीं किया जा सकता। फिर से साइन इन करें।

## समस्या निवारण

| संदेश या लक्षण | क्या करें |
| --- | --- |
| *इस सत्र को पढ़ा नहीं जा सकता। इसके मूल क्लाइंट को बंद करें…* | SQLite फ़ाइल खुली या अधूरी है (`-journal`/`-wal` साइडकार)। मूल प्रोग्राम को साफ़-सुथरे तरीके से बंद करें और फ़ाइल को फिर से कॉपी करें। |
| *समर्थित टेलीथॉन SQLite स्कीमा: 7 और 8* / *पायरोग्राम … 2 और 3* | फ़ाइल किसी बहुत पुराने या अज्ञात लाइब्रेरी संस्करण द्वारा बनाई गई थी। इसके बजाय फोन/QR से साइन इन करें। |
| *केवल अधिकृत प्रोडक्शन उपयोगकर्ता सत्रों का ही समर्थन किया जाता है* | Pyrogram फ़ाइल किसी बॉट या परीक्षण नेटवर्क से संबंधित है। |
| *TData आर्काइव 512 प्रविष्टियों या 32 MiB से अधिक हो गया है* | केवल ZIP `key_datas` और `D877F783D5D3EF8Cs`, पूरा फ़ोल्डर नहीं। |
| *TData को डिक्रिप्ट नहीं किया जा सकता। डेस्कटॉप स्थानीय पासकोड की जाँच करें।* | **Passcode या session टेक्स्ट** में Telegram Desktop का स्थानीय पासकोड दर्ज करें। |
| *एक समय में एक TData खाते को आयात करें* | Telegram Desktop के कई खाते थे; [असमर्थित प्रारूप](https://phishdestroy.github.io/TgWitness/hi/docs/reference/accounts/#unsupported-formats) देखें। |
| *चुनी गई फ़ाइलें विभिन्न खातों या API क्रेडेंशियल्स का वर्णन करती हैं* | केवल एक खाते की फ़ाइलें चुनें। |
| *JSON में कोई समर्थित API क्रेडेंशियल या प्राधिकरण शामिल नहीं है।* | [Account JSON](https://phishdestroy.github.io/TgWitness/hi/docs/reference/accounts/#account-json) में फ़ील्ड नामों की जाँच करें। |
| *केवल API मेटाडेटा* | JSON में कोई सत्र नहीं है। `.session` फ़ाइल जोड़ें या फ़ोन/QR का उपयोग करें। |
| *Auth Key HEX में सभी 512 हेक्साडेसिमल अक्षर शामिल होने चाहिए* | कुंजी संक्षिप्त की गई है या इसमें `…` शामिल है। |
| खाता आईडी आयात किए गए खाते से मेल नहीं खाता | फ़ाइल का उपयोगकर्ता आईडी टेलीग्राम द्वारा रिपोर्ट किए गए आईडी से भिन्न है; यह फ़ाइल किसी अन्य खाते के लिए है। |
| खाता पहले से ही किसी अन्य कार्यक्षेत्र का है | खाते को दो बार जोड़ने के बजाय उस वर्कस्पेस को खोलें। |
| कनेक्टेड, लेकिन स्रोतों में चैट सूची से एक निजी समूह गायब है | सदस्यता की जाँच करें। पिकर पहले 1,000 डायलॉग्स का निरीक्षण करता है; **पैरामीटर के** अंतर्गत सीमा बढ़ाएँ। |
| प्रॉक्सी कनेक्शन विफल | रूट और आईपी मोड की जाँच करें। स्वचालित MTProxy दूसरी कार्यशील प्रविष्टि आज़माता है। Hide the address waits; Direct as a last resort कॉन्फ़िगर की गई देरी के बाद सीधे कनेक्ट कर सकता है। [राउटिंग मोड](https://phishdestroy.github.io/TgWitness/hi/docs/reference/connection/#ip-modes) देखें। |

यह भी देखें: प्रॉक्सी और एन्क्रिप्शन के लिए [कनेक्शन और सुरक्षा](https://phishdestroy.github.io/TgWitness/hi/docs/reference/connection/), और साइन-इन के बाद क्या कैप्चर किया जाता है, इसके लिए [संग्रह कैसे काम करता है](https://phishdestroy.github.io/TgWitness/hi/docs/reference/collection/)।
