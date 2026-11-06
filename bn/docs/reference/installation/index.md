# ইনস্টল, যাচাই এবং আপডেট

Canonical page: https://phishdestroy.github.io/TgWitness/bn/docs/reference/installation/

একটি কমান্ডে ইনস্টল করুন, স্বাক্ষর ও হ্যাশ যাচাই করুন, ইনস্টলেশন আপডেট ও অপসারণ করুন।

[টিজিউইটনেস](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [ডকুমেন্টেশন](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Getting started](https://phishdestroy.github.io/TgWitness/bn/docs/reference/quickstart/)

![Getting started](https://phishdestroy.github.io/TgWitness/assets/chapter-start.svg)

[প্রকল্প](https://github.com/phishdestroy/TgWitness/blob/main/README.md) · [দ্রুত শুরু](https://phishdestroy.github.io/TgWitness/bn/docs/reference/quickstart/) · [নিয়োগ](https://phishdestroy.github.io/TgWitness/bn/docs/reference/deployment/)

**On this page**

- [Install with one command](https://phishdestroy.github.io/TgWitness/bn/docs/reference/installation/#install-with-one-command)
- [Where everything runs](https://phishdestroy.github.io/TgWitness/bn/docs/reference/installation/#where-everything-runs)
- [Full-text search settings](https://phishdestroy.github.io/TgWitness/bn/docs/reference/installation/#full-text-search-settings)
- [Command-line access](https://phishdestroy.github.io/TgWitness/bn/docs/reference/installation/#command-line-access)
- [Verify before running](https://phishdestroy.github.io/TgWitness/bn/docs/reference/installation/#verify-before-running)
- [Update an existing installation](https://phishdestroy.github.io/TgWitness/bn/docs/reference/installation/#update-an-existing-installation)
- [Everyday commands on Ubuntu](https://phishdestroy.github.io/TgWitness/bn/docs/reference/installation/#everyday-commands-on-ubuntu)
- [Remove TgWitness](https://phishdestroy.github.io/TgWitness/bn/docs/reference/installation/#remove-tgwitness)

## একটি কমান্ডে ইনস্টল করুন

গাইডেড ইনস্টলারটিতে একটি ব্যক্তিগত পাইথন রানটাইম অন্তর্ভুক্ত রয়েছে। ভবিষ্যতের ইনস্টলেশনের জন্য একই ঠিকানা ব্যবহার করুন: প্রতিটি প্রকাশনা ইনস্টলার, হ্যাশ, স্বাক্ষর এবং বিল্ড তথ্য একসঙ্গে আপডেট করে।

**লিনাক্স / ম্যাকওএস (ব্যাশ):**

```
curl -fsSL https://get.destroy.tools/install.sh | bash
```

উবুন্টু সার্ভারে, ব্যাকগ্রাউন্ড সার্ভিস ইনস্টল করতে রুট হিসেবে চালান। ডেস্কটপে, আপনার সাধারণ ব্যবহারকারী হিসেবে চালান।

**উইন্ডোজ (পাওয়ারশেল বা কমান্ড প্রম্পট):**

```
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "irm https://get.destroy.tools/install.ps1 | iex"
```

Windows-এ কোনো প্রশাসকের প্রয়োজন নেই। child PowerShell প্রক্রিয়াটি ফলাফলসহ আপনার টার্মিনাল খোলা রাখে। Python এবং নির্ভরতা ইনস্টলেশনেই থাকে।

উবুন্টুতে, **This computer**, **Temporary HTTPS link** বা **Own domain** নির্বাচন করুন। ইনস্টলার প্যানেল ঠিকানা এবং অ্যাক্সেস কী মুদ্রণ করে। একটি অস্থায়ী লিঙ্কের জন্য, সেই HTTPS ঠিকানাটি আপনার ব্রাউজারে খুলুন এবং কীটি প্রবেশ করান। রিমোট সার্ভারে লোকাল অ্যাক্সেসের জন্য, আপনার কম্পিউটার থেকে একটি SSH ফরওয়ার্ড ব্যবহার করুন (`ssh -L 8787:127.0.0.1:8787 user@server`) এবং খুলুন `http://127.0.0.1:8787`. macOS এবং Windows-এ, লোকাল প্যানেল আপনার ব্রাউজারে খুলে; এর টার্মিনাল চালু রাখুন।

প্যানেলের Telegram-এ সাইন ইন করুন এবং সংগ্রহ করতে যা চান তা নির্বাচন করুন। ইনস্টলেশন করলেই Telegram সংগ্রহ শুরু হয় না।

## যেখানে সবকিছু চলে

`get.destroy.tools` এটি একটি **Cloudflare Worker স্ট্যাটিক ডাউনলোড পরিবেশন করছে**। এতে কোনো TgWitness প্যানেল, টেলিগ্রাম সেশন বা ব্যবহারকারী প্রমাণের ডাটাবেস নেই। এটি কোনো প্রকল্প VPS-এ রাউট করা হয় না। অ্যাপ্লিকেশনটি সেই মেশিনে চলে যেখানে আপনি কমান্ডটি চালান।

| ইনস্টলেশন | প্রোগ্রাম | ডেটা |
| --- | --- | --- |
| রুট হিসেবে উবুন্টু | `/opt/tgwitness` | সিস্টেম সার্ভিস: `/var/lib/tgwitness-<installation ID>`; ব্যবহার করুন `tgwitness paths` নির্দিষ্ট পথের জন্য। |
| লিনাক্স/ম্যাকওএস ব্যবহারকারী | `~/.local/share/tgwitness` | `data/live` সেই ইনস্টলেশনের অধীনে। |
| উইন্ডোজ ব্যবহারকারী | `%LOCALAPPDATA%\TgWitness` | `data\live` সেই ইনস্টলেশনের অধীনে। |

সেট `TGWITNESS_INSTALL_DIR` অন্য কোনো ফোল্ডার নির্বাচন করতে। ইনস্টলকৃত সংস্করণ এবং ডেটা পৃথক। ইনস্টলার আপনার অ্যাকাউন্ট, বার্তা বা কী-গুলো ডাউনলোড সাইটে আপলোড করে না। Cloudflare টানেল নির্বাচন করলে প্যানেল ট্র্যাফিক Cloudflare-এর মাধ্যমে প্রেরণ করে; আপনার নিজস্ব ডোমেইন ব্যবহার করলে তা আপনার নিজ সার্ভারে নির্দেশ করে।

প্রতিটি ইনস্টলেশনে **START-HERE.html** এবং **START-HERE.txt** অন্তর্ভুক্ত থাকে, যাতে স্থানীয় পথ, কমান্ড এবং রিপোজিটরির লিঙ্ক থাকে। চালান `tgwitness guide` গাইড খুলতে। Windows-এ, ব্যবহার করুন `& "$env:LOCALAPPDATA\TgWitness\bin\tgwitness.cmd" guide` PowerShell-এ ব্যবহার করুন।

## পূর্ণ-পাঠ অনুসন্ধান সেটিংস

[পূর্ণ-পাঠ অনুসন্ধান](https://phishdestroy.github.io/TgWitness/bn/docs/reference/search/) (প্রিভিউ) কোনো সেটআপ ছাড়াই ব্যবহারযোগ্য। আপডেটের পর এর সূচি পটভূমিতে তৈরি হয়।

| ভেরিয়েবল বা কমান্ড | প্রভাব |
| --- | --- |
| `TGWITNESS_FULLTEXT=disk` | ডিফল্ট: সূচি রাখা হয় `search/fulltext.sqlite3` প্রতিটি ওয়ার্কস্পেসের |
| `TGWITNESS_FULLTEXT=memory` | কোনও সূচীপত্র ফাইল নেই; প্রতিবার শুরুতেই সূচীপত্র পুনর্নির্মাণ করা হয়। |
| `TGWITNESS_FULLTEXT=off` | কোনো সূচী নেই; শুধুমাত্র সঠিক-পাঠ অনুসন্ধান |
| `tgwitness index status` | প্রতিটি ওয়ার্কস্পেসের অবস্থা সূচিবদ্ধ করুন |
| `tgwitness stop`, `tgwitness index rebuild`, `tgwitness start` | স্বাক্ষরিত জার্নাল থেকে প্রতিটি সূচিপত্র পুনর্নির্মাণ করুন |

**Journal → Filters → Search index**-এ প্রশাসকের পছন্দ সেই ওয়ার্কস্পেসের জন্য ভেরিয়েবলকে ওভাররাইড করে। কমান্ডগুলো সেগুলো চালানোর ইনস্টলেশনের ডেটা ডিরেক্টরি খুঁজে বের করে; অন্যত্র, যোগ করুন `--data-dir` পথ থেকে `tgwitness paths`. সম্পূর্ণ ইউক্রেনীয় অভিধান (GPL-3.0 ডেটা) পেতে, ইনস্টল করুন `pymorphy3-dicts-uk` ইনস্টলেশনের Python পরিবেশে ইনস্টল করুন।

## কমান্ড-লাইন অ্যাক্সেস

[কমান্ড লাইন](https://phishdestroy.github.io/TgWitness/bn/docs/reference/cli/) (প্রিভিউ) স্ক্রিপ্ট এবং এজেন্টদের জন্য আর্কাইভ পড়ে।

| ভেরিয়েবল | প্রভাব |
| --- | --- |
| `TGWITNESS_URL` | প্যানেলের ঠিকানা জন্য `tgwitness search`, `context`, `messages`, `stats` এবং `export`; ডিফল্ট `http://127.0.0.1:8787` যখন একটি টোকেন সেট করা হয় |
| `TGWITNESS_MCP_TOKEN` | **Integrations → MCP** থেকে সংযোগ টোকেন সংরক্ষণ করুন, যা MCP ক্লায়েন্টদের সাথে শেয়ার করা হয়েছে; `--token-file` তার পরিবর্তে এটি একটি ফাইল থেকে পড়ে |
| `TGWITNESS_DATA` | কোনো না থাকলে সরাসরি ডেটা ডিরেক্টরি পড়ুন `--data-dir`, URL বা টোকেন দেওয়া না হলে সরাসরি পড়া হবে |

## চালানোর আগে যাচাই করুন

এক-লাইনের কমান্ডটি তার প্রাথমিক স্ক্রিপ্টের জন্য HTTPS-কে বিশ্বাস করে। সেই স্ক্রিপ্টটি ইনস্টলেশনের আগে SHA-256 এবং অ্যাপ্লিকেশন ও কন্টেইনমেন্টের প্রকল্পের RSA স্বাক্ষর পরীক্ষা করে। আপনি প্রথমে প্রাথমিক স্ক্রিপ্টটি ডাউনলোড করে যাচাই করতে পারেন।

পাবলিক রিলিজ কী হলো [release-signing.pub](https://github.com/phishdestroy/TgWitness/blob/main/deploy/installer/release-signing.pub)। এর SHA-256 হলো:

```
039d98a658ccda14253e45a00335b4a68d840976d8ec18b8d4355cc7c458447d
```

আপনি বিশ্বাস করেন এমন একটি রিপোজিটরি সংস্করণ থেকে এই ফিঙ্গারপ্রিন্ট সংরক্ষণ করুন। একই ডাউনলোড সার্ভার থেকে নেওয়া একটি চেকসাম অমিল সনাক্ত করে; স্বাধীনভাবে বিশ্বাসযোগ্য পাবলিক কী-ই রিলিজ স্বাক্ষরকে প্রমাণীকরণ করে।

নিচের যাচাইকরণ ডাউনলোডের জন্য একটি নতুন, খালি ডিরেক্টরি ব্যবহার করুন।

**Linux / macOS — একটি নতুন, ফাঁকা ডাউনলোড ডিরেক্টরিতে চালান** (curl এবং OpenSSL প্রয়োজন):

```
curl -fSLO https://get.destroy.tools/install.sh &&
curl -fSLO https://get.destroy.tools/install.sh.sig &&
curl -fSLO https://get.destroy.tools/release-signing.pub &&
test "$(openssl dgst -sha256 release-signing.pub | awk '{print $NF}')" = \
  '039d98a658ccda14253e45a00335b4a68d840976d8ec18b8d4355cc7c458447d' &&
openssl dgst -sha256 -verify release-signing.pub -signature install.sh.sig install.sh &&
bash install.sh
```

The `&&` চেইন এক্সিকিউশনের আগে থেমে যায় যদি ডাউনলোড, কী ফিঙ্গারপ্রিন্ট বা স্বাক্ষর যাচাই ব্যর্থ হয়। যদি স্ক্রিপ্ট ডাউনলোড এবং তার স্বাক্ষর যাচাইয়ের মধ্যে প্রকাশ ঘটে, তাহলে উভয়ই আবার ডাউনলোড করুন। পুরনো ইনস্টলারগুলো তাদের অপরিবর্তনীয় প্যাকেজ URLগুলো ধরে রাখে।

**Windows — চালানোর আগে SHA-256 পরিদর্শন করুন:**

```
Invoke-WebRequest https://get.destroy.tools/install.ps1 -OutFile install.ps1 -UseBasicParsing
Get-FileHash .\install.ps1 -Algorithm SHA256
Invoke-RestMethod https://get.destroy.tools/SHA256SUMS.txt
```

হ্যাশটি সাথে তুলনা করুন `install.ps1` রেখা। একটি স্বাধীন স্বাক্ষর যাচাইয়ের জন্য, OpenSSL ব্যবহার করুন (উদাহরণস্বরূপ, Git Bash থেকে) এবং উপরের একই পাবলিক-কী ফিঙ্গারপ্রিন্ট:

```
curl -fSLO https://get.destroy.tools/install.ps1 &&
curl -fSLO https://get.destroy.tools/install.ps1.sig &&
curl -fSLO https://get.destroy.tools/release-signing.pub &&
test "$(openssl dgst -sha256 release-signing.pub | awk '{print $NF}')" = \
  '039d98a658ccda14253e45a00335b4a68d840976d8ec18b8d4355cc7c458447d' &&
openssl dgst -sha256 -verify release-signing.pub -signature install.ps1.sig install.ps1 &&
powershell.exe -NoProfile -ExecutionPolicy Bypass -File install.ps1
```

Windows ইনস্টলেশন নিজেই .NET দিয়ে প্যাকেজ স্বাক্ষর যাচাই করে এবং OpenSSL প্রয়োজন হয় না। এগুলো বিচ্ছিন্ন RSA-3072 / SHA-256 স্বাক্ষর, Authenticode নয়। [ম্যানিফেস্ট](https://get.destroy.tools/manifest.json) সফটওয়্যার সংস্করণ, সঠিক Git commit, অপরিবর্তনীয় রিলিজ আইডি এবং প্রতিটি আর্টিফ্যাক্টের SHA-256 রেকর্ড করে। পৃষ্ঠাটি সংশ্লিষ্ট সোর্সের লিঙ্ক দেয়। ম্যানিফেস্ট এবং চেকসাম তালিকাতেও বিচ্ছিন্ন স্বাক্ষর রয়েছে (`manifest.json.sig` এবং `SHA256SUMS.txt.sig`).

## বিদ্যমান ইনস্টলেশন আপডেট করুন

**একটি নতুন প্রকাশনা ডাউনলোড সাইট আপডেট করে; ইনস্টল করা প্রোগ্রামগুলো আপডেট হয় যখন আপনি ইনস্টলারটি আবার চালান।** কোনো আনঅ্যাটেন্ডেড আপডেটার নেই বা চলমান সংগ্রহের স্বয়ংক্রিয় পুনঃসূচনা নেই। বর্তমান ইনস্টলার চ্যানেলটি **প্রিভিউ**; এটি প্রকাশিত, যাচাইকৃত বিল্ডগুলো অনুসরণ করে `main`, যার commit শেষ সংখ্যাযুক্ত GitHub রিলিজের তুলনায় নতুন হতে পারে। পৃষ্ঠার সংস্করণ আসে `pyproject.toml`; এর commit এবং build ID একই প্রিভিউ সংস্করণের মধ্যে আপডেটগুলোকে পৃথক করে।

Publication is automatic after that exact commit passes the application and security checks and the signed package passes Ubuntu service and Windows PowerShell installation tests. While checks are running, or if they fail, the same commands continue to install the previous checked build. The build manifest shows which commit is currently available; the version number alone may stay the same between preview updates.

আগের মতো একই ইনস্টলেশন ফোল্ডার এবং OS ব্যবহারকারী ব্যবহার করুন। সংগ্রহ বন্ধ রেখে সম্পূর্ণ ডেটা ডিরেক্টরি ব্যাকআপ করুন; `tgwitness paths` এটি সনাক্ত করে। একটি স্বাক্ষরিত এক্সপোর্ট সম্পূর্ণ ইনস্টলেশন ব্যাকআপ নয়।

**উবুন্টু রুট ইনস্টলেশন at `/opt/tgwitness`:**

```
curl -fsSL https://get.destroy.tools/install.sh | TGWITNESS_INSTALL_DIR=/opt/tgwitness bash -s -- --no-start
```

সফল ইনস্টলেশনের পর:

```
/opt/tgwitness/bin/tgwitness restart
/opt/tgwitness/bin/tgwitness status
/opt/tgwitness/bin/tgwitness open
```

Linux/macOS ব্যবহারকারীর ইনস্টলেশনের জন্য, এর মূল `TGWITNESS_INSTALL_DIR` অথবা ডিফল্ট ব্যবহার করে প্রথম ইনস্টলেশন কমান্ডটি আবার চালান। আপডেট করার আগে একটি ফোরগ্রাউন্ড প্যানেল বন্ধ করুন এবং পরে এটি আবার চালু করুন। কনফিগার করা Linux ব্যবহারকারী সার্ভিসের জন্য, এর `tgwitness restart` কমান্ড চালান।

**Windows:** চলমান প্যানেলটি বন্ধ করুন, Windows ইনস্টলেশন কমান্ডটি আবার চালান, তারপর খুলুন `bin\tgwitness.cmd` একই ইনস্টলেশনে। ইনস্টলার ডেটা, সেশন, অ্যাক্সেস সেটিংস এবং স্বাক্ষর কী সংরক্ষণ করে। এটি শুধুমাত্র নতুন পরিবেশ তার যাচাইকরণ পাস করার পর লঞ্চার পরিবর্তন করে; ব্যর্থ ইনস্টলেশন পূর্বের লঞ্চারই রেখে দেয়। স্টোরেজ-ফরম্যাট পরিবর্তনের জন্য প্রি-আপগ্রেড ব্যাকআপ সংরক্ষণ করুন।

## উবুন্টুতে দৈনন্দিন কমান্ডসমূহ

| কমান্ড | ফলাফল |
| --- | --- |
| `tgwitness open` | বর্তমান প্যানেল URL এবং অ্যাক্সেস কী। |
| `tgwitness paths` | নির্দিষ্ট প্রোগ্রাম, ডেটা এবং গাইড পথ। |
| `tgwitness guide --print` | অফলাইনে পরিচালনার নির্দেশনা। |
| `tgwitness status` / `tgwitness logs` | উপলব্ধতা / সেবা লগ। |
| `tgwitness stop` / `tgwitness start` | সেবা বন্ধ/পুনরায় চালু করুন; ডেটা সংরক্ষণ করুন। |
| `tgwitness token rotate` | প্রশাসক কী প্রতিস্থাপন করুন এবং ব্রাউজার সেশনগুলো বন্ধ করুন। |
| `tgwitness tunnel off` | পাবলিক কুইক টানেল নিষ্ক্রিয় করুন; স্থানীয় প্যানেল রাখুন। |
| `tgwitness tunnel on` / `tgwitness tunnel restart` | দ্রুত-টানেল লিঙ্ক তৈরি করুন / এর ঠিকানা প্রতিস্থাপন করুন। |

সহকর্মী টোকেন, সেশন এবং আইপি সীমাবদ্ধতার জন্য [Access](https://phishdestroy.github.io/TgWitness/bn/docs/reference/access/) দেখুন, এবং GitHub-to-Cloudflare রিলিজ ওয়ার্কফ্লো-এর জন্য [ইনস্টলার প্রকাশ](https://github.com/phishdestroy/TgWitness/blob/main/deploy/installer/README.md#automatic-publication-from-github) ।

## TgWitness সরান

কোনও আনইনস্টলার নেই: আপনি প্যানেলটি বন্ধ করে এর ফোল্ডারগুলো মুছে ফেলুন। ডেটা ফোল্ডার মুছে ফেলার ফলে জার্নাল, স্বাক্ষর কী, টেলিগ্রাম সেশন এবং সংরক্ষিত ফাইলগুলো চিরতরে মুছে যাবে। তার আগে:

1. আপনার প্রয়োজনীয় অংশ রপ্তানি করুন (**Exports → Download signed ZIP**) এবং স্বাক্ষর কী-এর ফিঙ্গারপ্রিন্ট ও চেকপয়েন্টগুলো এই মেশিনের বাইরে সংরক্ষণ করুন। ওয়ার্কস্পেস নিজেই রাখতে, সংগ্রহ বন্ধ রেখে পুরো ডেটা ফোল্ডারটি কপি করুন।
2. **আপনার সার্ভারসমূহের** অধীনে **Extras → Server 24/7** থেকে বা দিয়ে তৈরি সার্ভারগুলো মুছে ফেলুন `python -m tgwitness.cloud destroy`; প্রদানকারী সেগুলি মুছে ফেলা পর্যন্ত বিল করে।
3. প্রতিটি অ্যাকাউন্টের সেশন Telegram-এর **Settings → Devices**-এ গিয়ে শেষ করুন। ফাইলগুলো মুছে ফেলা Telegram-এর দিক থেকে সেশন লগআউট করে না।

**উবুন্টু রুট ইনস্টলেশন।** ডেটা ফোল্ডারটি লক্ষ্য করুন, সার্ভিসটি থামান, তারপর সার্ভিস, ফোল্ডারগুলো এবং শর্টকাটটি মুছে ফেলুন:

```
/opt/tgwitness/bin/tgwitness paths
/opt/tgwitness/bin/tgwitness stop
systemctl list-unit-files 'tgwitness-*'
systemctl disable tgwitness-<ID>
rm /etc/systemd/system/tgwitness-<ID>.service
systemctl daemon-reload
rm -rf /opt/tgwitness /var/lib/tgwitness-<ID> /usr/local/bin/tgwitness
```

**লিনাক্স বা ম্যাকওএস ব্যবহারকারীর ইনস্টলেশন।** প্যানেলটি বন্ধ করুন। একটি কনফিগার করা লিনাক্স ব্যবহারকারী পরিষেবা বন্ধ করা হয় `systemctl --user disable --now tgwitness-<ID>`; এর ইউনিট হল `~/.config/systemd/user/`। তারপর মুছে ফেলুন `~/.local/share/tgwitness` (অথবা আপনার `TGWITNESS_INSTALL_DIR`) এবং `~/.local/bin/tgwitness` শর্টকাট।

**Windows.** প্যানেলটি বন্ধ করুন এবং মুছে ফেলুন `%LOCALAPPDATA%\TgWitness` (অথবা আপনার `TGWITNESS_INSTALL_DIR`)। ইনস্টলার কোনো সার্ভিস, নির্ধারিত টাস্ক বা শর্টকাট যোগ করে না।
