# स्रोत इतिहास लोड करें

Canonical page: https://phishdestroy.github.io/TgWitness/hi/docs/reference/history/

सक्षम स्रोतों से पिछले संदेश लोड करें, विराम और फिर से शुरू करें, और एक हस्ताक्षरित प्रगति रिपोर्ट सत्यापित करें।

In **Sources**, review the enabled chats, pause observation, choose Standard API or Takeout export, then choose **Load full history**. The run fixes that list of sources and reads their available past messages into Chats and the signed observation journal. Media uses the existing attachment settings and durable download queue. This is separate from the per-chat signed JSON/HTML export.

For account-wide collection, select **Whole account**, start observation to load its source list, and review that list before starting history. The dialog-list limit still applies (1,000 by default, adjustable in Parameters). A successful run does not prove that every account dialog was listed. Chats discovered or enabled later need another run. Pause observation before starting history; one acquisition owns an account at a time.

Choose one to five attachment workers and whether to preserve available Recent Actions and compare previously saved versions. Takeout may require approval in Telegram and a server-specified wait. These options remain fixed on resume. See [Backfill behavior and evidence contract](https://github.com/phishdestroy/TgWitness/blob/main/docs/BACKFILL.md) for transport, retry and trust details.

## विराम, पुनरारंभ और आंशिक परिणाम

- **Pause history** stops reading. **Continue history** resumes from the last committed message in each source; restarting the app also leaves the run paused until resumed. Resuming requires the same idle Telegram account.
- संदेश अवलोकन, अटैचमेंट जॉब और कर्सर कमिट एक ही लेनदेन में। एक फिर से शुरू किया गया रन अपने पहले से कमिट किए गए अवलोकनों को दोहराता नहीं है। लाइव कैप्चर या एक अलग, स्पष्ट रूप से शुरू किया गया रन स्वतंत्र रूप से उसी संदेश का अवलोकन कर सकता है।
- Each source (each Telegram split range in Takeout) fixes an upper message ID on its first read. Newer messages belong to live observation, not to that source's remaining historical pages.
- पहुँच से बाहर के स्रोत और अधिग्रहण के दौरान अक्षम किए गए स्रोत 'असफल' या 'छूटा हुआ' के रूप में दिखाई देते रहते हैं। अन्य स्रोत जारी रहते हैं; कुल परिणाम अधूरा रहता है।
- FloodWait delays respect the saved account backoff. Transient failures retry up to five times; exhaustion and low disk space pause with the cursor intact.
- **End this history run** preserves saved observations. It does not remove them or cancel standard-API attachment jobs. Ending Takeout marks its remaining Takeout files as skipped; pausing keeps them resumable. A new run reads enabled sources anew.

इतिहास पूर्ण होने का अर्थ केवल इतिहास पढ़ना है। अटैचमेंट लंबित रह सकते हैं, विफल हो सकते हैं, या कॉन्फ़िगर की गई नीति द्वारा बाहर रखा जा सकते हैं। जर्नल और अटैचमेंट कतार में मीडिया रसीदों की जाँच करें; केवल संरक्षित बाइट्स वाली एक पूरी हुई रसीद ही एक सहेजा गया अटैचमेंट बनाती है। इतिहास संचालन एक स्पष्ट स्नैपशॉट अनुरोध है और यह भविष्य के लाइव घटनाओं की श्रेणियों का चयन करने वाले स्विच से अलग है।

## स्थानांतरित करें और सत्यापित करें

**हस्ताक्षरित प्रगति रिपोर्ट** सहेजें, फिर जर्नल और सहेजी गई अटैचमेंट डाउनलोड करने के लिए **'सबूत निर्यात करें'** का उपयोग करें। बाद के सबूत निर्यात में अतिरिक्त रिकॉर्ड शामिल हो सकते हैं; रिपोर्ट अपने काउंटर को उस समय जर्नल उपसर्ग से बांधती है जब इसे बनाया गया था। इस संस्करण के एक विश्वसनीय चेकआउट से वेरिफायर चलाएँ:

```
python tgwitness/verify.py tgwitness-history-report.json --evidence evidence.zip --fingerprint TRUSTED_FINGERPRINT
```

Keep the expected signing-key fingerprint independently. The verifier checks the report signature, the evidence archive, the report checkpoint, source plan, account and counts of saved/unavailable messages. New runs also bind source progress and options to signed cursor events. Without `--evidence`, it checks only the signed report and its internal consistency. Legacy progress fields and attachment summaries remain signed collector statements. The evidence verifier checks archived media bytes.

Neither signing nor finishing the available history proves Telegram origin, an atomic snapshot, or historical completeness. Messages can change while reading; deleted messages and intermediate edits outside available Recent Actions, and Secret Chats, are not recovered. An operator controlling the signing key can fabricate a journal before outside commitments exist. Use separately retained checkpoints or an independent witness for the documented tamper-detection properties.

अधिग्रहण कर्सर स्थानीय कार्यक्षेत्र की स्थिति है। केवल साक्ष्य ZIP को पुनर्स्थापित करने से लंबित अधिग्रहण कार्य या टेलीग्राम सत्र पुनर्स्थापित नहीं होता है। यदि मूल कार्य को जारी रखने की आवश्यकता हो तो कार्यक्षेत्र का बैकअप रखें।
