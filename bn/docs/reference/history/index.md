# লোড সোর্সের ইতিহাস

Canonical page: https://phishdestroy.github.io/TgWitness/bn/docs/reference/history/

সক্রিয় উৎস থেকে পূর্ববর্তী বার্তাগুলো লোড করুন, বিরতি দিন এবং পুনরায় শুরু করুন, এবং স্বাক্ষরিত অগ্রগতি প্রতিবেদন যাচাই করুন।

[টিজিউইটনেস](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [ডকুমেন্টেশন](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [সংগ্রহ](https://github.com/phishdestroy/TgWitness/blob/main/docs/COLLECTION-MODES.md)

![Collection](https://phishdestroy.github.io/TgWitness/assets/chapter-collect.svg)

In **Sources**, review the enabled chats, pause observation, choose Standard API or Takeout export, then choose **Load full history**. The run fixes that list of sources and reads their available past messages into Chats and the signed observation journal. Media uses the existing attachment settings and durable download queue. This is separate from the per-chat signed JSON/HTML export.

For account-wide collection, select **Whole account**, start observation to load its source list, and review that list before starting history. The dialog-list limit still applies (1,000 by default, adjustable in Parameters). A successful run does not prove that every account dialog was listed. Chats discovered or enabled later need another run. Pause observation before starting history; one acquisition owns an account at a time.

Choose one to five attachment workers and whether to preserve available Recent Actions and compare previously saved versions. Takeout may require approval in Telegram and a server-specified wait. These options remain fixed on resume. See [Backfill behavior and evidence contract](https://github.com/phishdestroy/TgWitness/blob/main/docs/BACKFILL.md) for transport, retry and trust details.

## থামানো, পুনরায় শুরু এবং আংশিক ফলাফল

- **Pause history** stops reading. **Continue history** resumes from the last committed message in each source; restarting the app also leaves the run paused until resumed. Resuming requires the same idle Telegram account.
- বার্তা পর্যবেক্ষণ, সংযুক্ত কাজ এবং কার্সর কমিট একটি লেনদেনে সম্পন্ন হয়। পুনরায় চালানো একটি রান ইতিমধ্যেই কমিট করা পর্যবেক্ষণগুলো পুনরাবৃত্তি করে না। লাইভ ক্যাপচার বা একটি পৃথক, স্পষ্টভাবে শুরু করা রান স্বাধীনভাবে একই বার্তা পর্যবেক্ষণ করতে পারে।
- Each source (each Telegram split range in Takeout) fixes an upper message ID on its first read. Newer messages belong to live observation, not to that source's remaining historical pages.
- অপ্রাপ্তব্ধ উত্স এবং অধিগ্রহণের সময় নিষ্ক্রিয় করা উত্সগুলো ব্যর্থ বা এড়িয়ে যাওয়া হিসেবে দৃশ্যমান থাকে। অন্যান্য উত্সগুলো চালিয়ে যায়; সামগ্রিক ফলাফল অসম্পূর্ণ।
- FloodWait delays respect the saved account backoff. Transient failures retry up to five times; exhaustion and low disk space pause with the cursor intact.
- **End this history run** preserves saved observations. It does not remove them or cancel standard-API attachment jobs. Ending Takeout marks its remaining Takeout files as skipped; pausing keeps them resumable. A new run reads enabled sources anew.

ইতিহাস সম্পন্ন হলে তা শুধুমাত্র পড়ার জন্য ইতিহাস হিসেবে সংরক্ষিত হয়। সংযুক্তিগুলি পেন্ডিং থাকতে পারে, ব্যর্থ হতে পারে, অথবা কনফিগার করা নীতি অনুযায়ী বাদ পড়তে পারে। জার্নাল এবং সংযুক্তি সারিতে মিডিয়া রসিদগুলি পরীক্ষা করুন; সংরক্ষিত বাইটসহ একটি সম্পন্ন রসিদই একটি সংরক্ষিত সংযুক্তি গঠন করে। ইতিহাস অপারেশন একটি স্পষ্ট স্ন্যাপশট অনুরোধ এবং এটি ভবিষ্যতের লাইভ ইভেন্টের বিভাগ নির্বাচনকারী সুইচগুলি থেকে পৃথক।

## স্থানান্তর করুন এবং যাচাই করুন

**স্বাক্ষরিত অগ্রগতি প্রতিবেদন**টি সংরক্ষণ করুন, তারপর জার্নাল এবং সংরক্ষিত সংযুক্তিগুলি ডাউনলোড করতে **'প্রমাণ রপ্তানি'** ব্যবহার করুন। পরবর্তী কোনো প্রমাণ রপ্তানিতে অতিরিক্ত রেকর্ড থাকতে পারে; প্রতিবেদনটি তৈরি হওয়ার সময় জার্নাল প্রিফিক্সের সাথে এর কাউন্টারগুলো আবদ্ধ করে। এই সংস্করণের একটি বিশ্বস্ত চেকআউট থেকে যাচাইকারী চালান:

```
python tgwitness/verify.py tgwitness-history-report.json --evidence evidence.zip --fingerprint TRUSTED_FINGERPRINT
```

Keep the expected signing-key fingerprint independently. The verifier checks the report signature, the evidence archive, the report checkpoint, source plan, account and counts of saved/unavailable messages. New runs also bind source progress and options to signed cursor events. Without `--evidence`, it checks only the signed report and its internal consistency. Legacy progress fields and attachment summaries remain signed collector statements. The evidence verifier checks archived media bytes.

Neither signing nor finishing the available history proves Telegram origin, an atomic snapshot, or historical completeness. Messages can change while reading; deleted messages and intermediate edits outside available Recent Actions, and Secret Chats, are not recovered. An operator controlling the signing key can fabricate a journal before outside commitments exist. Use separately retained checkpoints or an independent witness for the documented tamper-detection properties.

অধিগ্রহণ কার্সর স্থানীয় ওয়ার্কস্পেসের অবস্থা। শুধুমাত্র প্রমাণের ZIP পুনরুদ্ধার করলে ঝুলন্ত অধিগ্রহণ কাজ বা টেলিগ্রাম সেশন পুনরুদ্ধার হয় না। যদি মূল কাজের ধারাবাহিকতা প্রয়োজন হয়, তাহলে ওয়ার্কস্পেস ব্যাকআপ রাখুন।
