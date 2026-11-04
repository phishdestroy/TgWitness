# কি পরীক্ষা করা হয়েছে

Canonical page: https://phishdestroy.github.io/TgWitness/bn/docs/reference/verification/

লাইভ টেলিগ্রাম পরীক্ষা, স্বয়ংক্রিয় যাচাইকরণ, ব্রাউজার যাচাইকরণ এবং যা যাচাই করা যায়নি।

## Live server journal inventory · 1 November 2026

At approximately 19:15 UTC, sequential read-only SQLite `query_only` queries counted events in ten workspace databases on a running server. Collection continued during the queries, so this is not an atomic snapshot across workspaces.

| Observed across the ten workspace databases | গণুন |
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

| যাচাই করুন | What it exercised |
| --- | --- |
| [Source archive](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_source_archive.py) | Two builds with identical source bytes but changed file times produced the same ZIP and checksum. Exact archived bytes and file hashes matched; private test files stayed out. A simulated write failure left the previous archive and checksum intact. |
| [Account export recovery](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_account_export_recovery.py) | A simulated disk error on the second ZIP member left no published or partial ZIP. Resume kept every signed receipt byte-identical, produced an independently verifiable archive using the expected signing fingerprint, and retained the synthetic coverage gap as a partial result. Scale assertions guard against repeated task and receipt scans as histories grow. |
| [Minimized disclosure privacy](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_disclosure_privacy.py) | Synthetic Unicode names and aliases, nested metadata, unknown senders and media fields were checked in all three identity modes and with text omission. A masking-limit failure did not silently weaken redaction; the original signed account export stayed unchanged. |
| [Linux media decoder and OCR](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_media_worker.py) | A [Linux Docker CI check](https://github.com/phishdestroy/TgWitness/actions/runs/41341200341/job/124951395192) at commit `5a9e0814` passed generated Ogg/Opus, MP3, M4A, MP4 with video, WAV and FLAC inputs; forged-duration and secondary-file-reference controls; and 48 mutated parser fixtures (34 rejected, 14 decoded within bounds). Real Tesseract OCR ran with original bytes unchanged. The decoder and OCR ran in network-isolated containers without a Whisper model. |

The checks run in the [pull-request](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/pr-check.yml) and [full Checks](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/checks.yml) workflows. They test these failure boundaries, not every possible storage failure or whether a disclosure is automatically safe to publish. The media check does not measure speech recognition accuracy or Telegram delivery. Review each derivative before sharing.

## লাইভ টেলিগ্রাম পরীক্ষা, সম্পূর্ণ অ্যাকাউন্ট · ২৯ অক্টোবর ২০২৬

নীচের পরীক্ষায় একই অ্যাকাউন্ট চলতেই থাকল। ২৯ অক্টোবর ১২:১০ UTC-এ এর পরিধি পুরো অ্যাকাউন্টে (চ্যানেল, গ্রুপ, ব্যক্তিগত চ্যাট এবং বট) পরিবর্তন করা হয়; প্যানেল নিশ্চিতকরণের জন্য অনুরোধ করেছিল এবং স্বাক্ষরিত জার্নালে তা রেকর্ড করা হয়েছিল। ১৭:৫৯ UTC-এ জার্নালে ছিল:

| রেকর্ড করা হয়েছে, ২৭ অক্টোবর ২১:৩৬ থেকে ২৯ অক্টোবর ১৭:৫৯ ইউটিসি | গণুন |
| --- | --- |
| জার্নাল রেকর্ডসমূহ | 9,968 |
| নতুন বার্তা | 5,308 |
| পুরো অ্যাকাউন্টে স্যুইচ করার পর তাদের | 3,878 |
| মোছা | 784 |
| TgWitness বার্তাটি সংরক্ষণ করার পর সেগুলো মুছে ফেলা হয়েছিল। | 596 |
| সম্পাদনাগুলি | 41 |
| পুনঃপরীক্ষার মাধ্যমে যোগ করা বার্তাগুলি | 2,273 |
| বার্তাগুলো আর খুঁজে পাওয়া গেল না | 18 |
| ইতিহাসের স্ন্যাপশট দ্বারা সংরক্ষিত বার্তা | 242 |
| সংরক্ষিত সংযুক্তিগুলি | 247 |
| সংগ্রাহক শুরু করে | 19 |
| টেলিগ্রাম ফ্লাড অপেক্ষা করছে | 26 |

- প্যানেলের **Verify** চেক সমস্ত ৯,৯৬৮ রেকর্ডের স্বাক্ষর এবং হ্যাশ চেইন নিশ্চিত করেছে।
- বার্তাগুলো দুইটি গ্রুপ বা চ্যানেল এবং তিনটি ব্যক্তিগত চ্যাট ও বট থেকে এসেছে। একটি বার্তা বোতাম **চ্যাটস** থেকে চাপানো হয়েছিল; অনুরোধ এবং টেলিগ্রামের উত্তর জার্নালে রয়েছে।
- যখন কালেক্টর রিস্টার্টের পর অ্যাকাউন্টটি পুনরায় স্ক্যান করেছিল, তখন নতুন চ্যাটগুলো যোগ করা হয়েছিল। নতুন চ্যাটগুলোর পূর্ববর্তী বার্তা সংরক্ষণ বন্ধ ছিল (`history = 0`), তাই এখানে তা অন্তর্ভুক্ত করা হয়নি।

অন্তর্ভুক্ত নয়: প্রতিক্রিয়া, সদস্যপদ পরিবর্তন, ব্যক্তি প্রোফাইল, বার্তা পাঠানো, আমন্ত্রণের মাধ্যমে যোগদান, প্রক্সি, বিজ্ঞপ্তি, উইটনেস বট এবং একযোগে একাধিক অ্যাকাউন্ট। পাবলিক ফাইলগুলোতে শুধুমাত্র গণনা থাকে।

## পাসওয়ার্ড-সুরক্ষিত রপ্তানি libarchive দিয়ে খোলা হয়েছে · ২৯ অক্টোবর ২০২৬

রপ্তানি এনক্রিপশন কোড (WinZip AES-256, যা 7-Zip এবং WinRAR ফরম্যাট পড়ে) দ্বারা লেখা একটি আর্কাইভ Windows `tar` (bsdtar 3.6.2, libarchive) দিয়ে খোলা হয়েছিল। সঠিক পাসওয়ার্ডে এক্সট্র্যাক্ট করা ফাইলের SHA-256 মূলটির সাথে মিলল; ভুল পাসওয়ার্ডে "Incorrect passphrase" দেখিয়ে প্রত্যাখ্যাত করা হয়েছিল। 7-Zip এবং WinRAR নিজেই চালানো হয়নি।

## লাইভ টেলিগ্রাম পরীক্ষা · ২৭ থেকে ২৯ অক্টোবর ২০২৬

একটি আসল টেলিগ্রাম অ্যাকাউন্ট, বিল্ট-ইন API পেয়ার পুলের মাধ্যমে সাইন ইন করা, **২৭ অক্টোবর ২১:৩৬ UTC** থেকে **২৯ অক্টোবর ০৫:১৫ UTC পর্যন্ত** একটি সুপারগ্রুপ রেকর্ড করেছে। ওই সময়কালে কালেক্টরটি ১২ বার চালু করা হয়েছিল।

| রেকর্ড করা হয়েছে | গণুন |
| --- | --- |
| জার্নাল রেকর্ডসমূহ, যার মধ্যে হার্টবিট এবং সার্ভিস রেকর্ডসমূহ অন্তর্ভুক্ত | 2,385 |
| নতুন বার্তা | 1,291 |
| মোছা | 472 |
| TgWitness টেক্সটটি সংরক্ষণ করার পর সেগুলো মুছে ফেলা হয়েছিল। | 347 |
| সম্পাদনাগুলি | 12 |
| বন্ধ থাকা অবস্থায় মিস হওয়া বার্তাগুলো পুনরায় যাচাইকরণে যোগ করা হয়েছে। | 12 |
| সংরক্ষিত সংযুক্তিগুলি | 17 |
| সংযুক্তিগুলি ডাউনলোড হয়নি (ডাউনলোড বন্ধ, অথবা ডাউনলোডের কোনো ফাইল নেই) | 14 |
| টেলিগ্রাম ফ্লাড: পুনঃযাচাইয়ের সময় প্রতিবার ৩ সেকেন্ড করে বিরতি দেয়। | 8 |

- সকল ২,৩৮৫টি রেকর্ডের স্বাক্ষর এবং হ্যাশ চেইন জার্নালের পাবলিক কী-র বিরুদ্ধে যাচাই করা হয়।
- পুনঃশুরু করার পর কালেক্টর সংরক্ষিত আপডেট অবস্থা (`pts`) থেকে পুনরায় শুরু করে এবং Telethon পিছিয়ে থাকা মেসেজগুলো ধরতে থাকে; পুনঃপরীক্ষা তখন এখনও অনুপস্থিত মেসেজগুলো যোগ করে।
- প্রতিটি FloodWait-এ কালেক্টর অনুরোধকৃত সময় অপেক্ষা করল এবং চালিয়ে গেল।
- অ্যাকাউন্টটি সাইন ইন অবস্থায়ই ছিল, এবং একই সেশন ২৯ অক্টোবর পুনরায় সংযুক্ত হয়েছিল।

এই পরীক্ষায় অন্তর্ভুক্ত নয়: একযোগে একাধিক অ্যাকাউন্ট, প্রশাসক ভূমিকা, প্রক্সি, কয়েক ঘণ্টার বেশি সময়ের আউটেজ এবং সম্পূর্ণ [লাইভ গ্রহণ প্রক্রিয়া](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md)। পাবলিক ফাইলগুলিতে শুধুমাত্র এই গণনাগুলি রয়েছে: কোনো অ্যাকাউন্ট বা চ্যাট আইডেন্টিফায়ার, বার্তা বা শংসাপত্র নেই।

## কৃত্রিম স্থানীয় সক্ষমতা পরিমাপ

কমান্ড: `python tools/check_capacity.py --events 10000 --chats 100`

| মিটারিক | পর্যবেক্ষিত |
| --- | --- |
| ইনপুট | ১০০টি সিন্থেটিকভাবে নির্বাচিত উৎসের মধ্যে ১০,০০০টি সিন্থেটিক বার্তা ইভেন্ট |
| বার্তার পাঠ্য | ৪০০ অক্ষর; কোনো মিডিয়া বা নেটওয়ার্ক নেই |
| সেবন | ৫৩.২৭৩ সেকেন্ড; ১৮৭.৭ ইভেন্ট/সেকেন্ড |
| হ্যান্ডলার ল্যাটেন্সি | p50 4.162 ms; p95 7.784 ms; সর্বোচ্চ 129.118 ms |
| ZIP রপ্তানি | ট্র্যাসম্যালক সক্রিয় অবস্থায় ১৯.৮৬৮ সেকেন্ড |
| শীর্ষ ট্রেসকৃত পাইথন রপ্তানি বরাদ্দ | 0.51 MiB; প্রক্রিয়া RSS নয় |
| ZIP আকার | ৪,৬১০,৯৬২ বাইট |
| স্বতন্ত্র যাচাইকরণ | সমস্ত ১০,০০০টি ইভেন্ট যাচাই করা হয়েছে |

এটি এই Windows হোস্টে স্থানীয় সিরিয়াল রেকর্ডিং/রপ্তানি পথ পরিমাপ করে। এটি MTProto ডেলিভারি, সমান্তরাল অ্যাকাউন্ট, টেলিগ্রাম থ্রটলিং, মিডিয়া, দীর্ঘমেয়াদী ওয়ার্কলোড বা নিশ্চিত সংখ্যক বাস্তব চ্যাট পরিমাপ করে না। এই পরিমাপটি চূড়ান্ত অফলাইন টাইমস্ট্যাম্প টুলিং-এর আগে করা হয়েছে, যা পরিমাপকৃত মেসেজ পথ পরিবর্তন করে না।

## বাকী যোগ্যতা

সংরক্ষিত লাইভ জার্নাল প্রকৃত সংগ্রহ, সম্পাদনা, মুছে ফেলার বিজ্ঞপ্তি, সংযুক্তি, পুনঃপরীক্ষা এবং রেট-লিমিট হ্যান্ডলিং প্রতিষ্ঠা করে। এটি সম্পূর্ণ ডেলিভারি বা ভূমিকা দৃশ্যমানতা, প্রতিক্রিয়াশীল অভিনেতারা, দীর্ঘায়িত FloodWait, অ্যাকাউন্ট নিষেধাজ্ঞা এবং নেটওয়ার্ক/প্রক্রিয়া বিঘ্ন পুনরুদ্ধারের নিয়ন্ত্রিত ম্যাট্রিক্স প্রতিষ্ঠা করে না। QR-টোকেন ইস্যু সম্পূর্ণ মোবাইল QR নিশ্চিতকরণের থেকে পৃথক।

ডকার বিল্ড/রান, লিনাক্স/ম্যাকওএস ইনস্টলেশন, দীর্ঘস্থায়ী উচ্চ লোড, স্বাধীন নিরাপত্তা পর্যালোচনা, একটি প্রকৃত স্বাধীন TSA প্রতিক্রিয়া, সার্টিফিকেট বাতিলকরণ/আর্কাইভ্যাল ভ্যালিডেஷன் এবং ফরেনসিক সার্টিফিকেশন রেকর্ডকৃত যোগ্যতার বাইরে রয়েছে। সংরক্ষিত MTProto স্টেট এবং ক্যাচ-আপ বাস্তবায়িত হয়েছে; অ্যাটমিক ডুরএবল রিপ্লে এখনও প্রতিষ্ঠিত হয়নি। অ্যাডমিন-লগ সংগ্রহ, অতিরিক্ত রিয়্যাক্টর তালিকা এবং অগ্রাধিকার শর্ট পোলিং পৃথক বৈশিষ্ট্য হিসেবে রয়ে গেছে। নিয়ন্ত্রিত যোগ্যতা ম্যাট্রিক্সের জন্য [লাইভ গ্রহণ](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md) দেখুন।

স্থানীয় বিস্তারিত রসিদ এবং স্ক্রিনশটগুলো test-results/ (Git-ignored) ফোল্ডারে রয়েছে। docs/assets/ ফোল্ডারে থাকা পাবলিক স্ক্রিনশটে শুধুমাত্র কাল্পনিক প্রদর্শনী ডেটা রয়েছে।
