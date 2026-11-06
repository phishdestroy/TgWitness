# מה נבדק

Canonical page: https://phishdestroy.github.io/TgWitness/he/docs/reference/verification/

הבדיקה החיה של טלגרם, בדיקות אוטומטיות, בדיקות דפדפן ומה שעדיין לא אומת.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [תיעוד](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Evidence and verification](https://phishdestroy.github.io/TgWitness/he/docs/reference/evidence/)

![Evidence & verification](https://phishdestroy.github.io/TgWitness/assets/chapter-evidence.svg)

**Updated 6 November 2026.** Results are tied to the revision, environment and workload recorded for each run. [Current capabilities](https://github.com/phishdestroy/TgWitness/blob/main/docs/STATUS.md) describes the available workflows; this page records what has actually been checked.

[Performance graphs](https://phishdestroy.github.io/TgWitness/docs/validation/) · [Signed English audit](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/REPORT.md) · [Downloadable measurements](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/MEASUREMENTS.csv)

| Latest evidence | תוצאה | היקף |
| --- | --- | --- |
| Release audit · 6 Nov | 1,461 core tests passed; 37 platform skips | Source `92e539af40d8`; open findings retained |
| Fresh exports · 6 Nov | 127.713 and 141.781 records/s, complete cycle | Two accounts per server; text and metadata through WARP |
| Retained archives · 6 Nov | 48 archives; 3,598,381 records verified | Existing archives checked against pinned workspace keys |
| Trusted Live · 5 Nov | Guarded CPU recording and WARP checks | Official Desktop login and native export remain unqualified |
| Phala / Intel TDX · 4 Nov | All 16 verifier checks passed on later runs | Historical deployment; no Telegram account on the CVM |

**On this page**

- [Release audit and fresh exports · 6 November 2026](https://phishdestroy.github.io/TgWitness/he/docs/reference/verification/#release-audit-and-fresh-exports--6-november-2026)
- [Trusted Live CPU Ubuntu and WARP · 5 November 2026](https://phishdestroy.github.io/TgWitness/he/docs/reference/verification/#trusted-live-cpu-ubuntu-and-warp--5-november-2026)
- [Live Phala Cloud deployment · 4 November 2026](https://phishdestroy.github.io/TgWitness/he/docs/reference/verification/#live-phala-cloud-deployment--4-november-2026)
- [Live server journal inventory · 1 November 2026](https://phishdestroy.github.io/TgWitness/he/docs/reference/verification/#live-server-journal-inventory--1-november-2026)
- [Recent offline and fault-injection checks · 1 November 2026](https://phishdestroy.github.io/TgWitness/he/docs/reference/verification/#recent-offline-and-fault-injection-checks--1-november-2026)
- [Live Telegram test, whole account · 29 October 2026](https://phishdestroy.github.io/TgWitness/he/docs/reference/verification/#live-telegram-test-whole-account--29-october-2026)
- [Password-protected export opened with libarchive · 29 October 2026](https://phishdestroy.github.io/TgWitness/he/docs/reference/verification/#password-protected-export-opened-with-libarchive--29-october-2026)
- [Live Telegram test · 27 to 29 October 2026](https://phishdestroy.github.io/TgWitness/he/docs/reference/verification/#live-telegram-test--27-to-29-october-2026)
- [Synthetic local capacity measurement](https://phishdestroy.github.io/TgWitness/he/docs/reference/verification/#synthetic-local-capacity-measurement)
- [Full-text search on one million messages · 5 November 2026](https://phishdestroy.github.io/TgWitness/he/docs/reference/verification/#full-text-search-on-one-million-messages--5-november-2026)
- [Remaining qualification](https://phishdestroy.github.io/TgWitness/he/docs/reference/verification/#remaining-qualification)

## Release audit and fresh exports · 6 November 2026

The audit used v0.9.1 at source `92e539af40d8368d198ff5e040f1d876f2c1310e`, release `92e539af40d8-83e41104669e`. Installed-package smoke checks passed on three servers. The signed report retains the state observed at that time.

[![Acquisition and complete export rates for two fresh workloads](https://phishdestroy.github.io/TgWitness/assets/performance.svg)](https://phishdestroy.github.io/TgWitness/docs/validation/)

| Workload | תיעוד | Acquisition | Complete cycle | Complete-cycle rate |
| --- | --- | --- | --- | --- |
| Server A · two accounts | 27,030 | 189.043 s | 211.647 s | 127.713 records/s |
| Server B · two accounts | 29,299 | 182.513 s | 206.650 s | 141.781 records/s |

Both exports began without resume, excluded attachments and avatars, and ended with zero duplicate or reused records. The complete cycle includes preparation, acquisition, selection, packaging and archive verification. Server A also ran a protected-chat read check. Four FloodWait events on A and three on B were respected. These observations do not establish a general throughput guarantee.

| בדוק | תוצאה | Qualification |
| --- | --- | --- |
| Core pytest | 1,461 passed | 37 platform skips |
| Browser / browser UX / evidence / site | 102 / 66 / 15 / 9 passed | These programs overlap other tests; counts are not additive |
| Capture addon | 124 passed | Three Official Web checks blocked by the required Chromium sandbox |
| API authorization | 269 routes; 538 requests passed | Missing credentials and revoked access |
| Retained archives | 48 of 48 verified | 3,598,381 records; pinned workspace keys |
| Live fleet read checks | 24 of 40 profiles passed | 16 WARP routes failed qualification; those profiles were not connected |

The [signed report](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/REPORT.md) records all open findings, including three defects in an unpublished secret-chat snapshot absent from the audited main build. The earlier [public-history qualification](https://github.com/phishdestroy/TgWitness/blob/main/docs/EXPORT-BENCHMARK-2026-11-06.md) used a different revision and workload; its rates must not be combined with this comparison.

Verify the original report using the [pinned key and verifier](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/README.md#verify-the-original-files). Its signature protects the operator's report from alteration. It is not independent attestation, proof of Telegram authorship or GDPR certification.

## Trusted Live CPU Ubuntu and WARP · 5 November 2026

The retained integration run used a CPU-only Ubuntu 24.04.5 guest (4 vCPU, 8 GiB) under QEMU inside a RunPod CPU host. The collector used `14e642a5`; verification used `02072461`. The final fixes merged in [PR #114](https://github.com/phishdestroy/TgWitness/pull/114) as `755f78f6`, whose tree matched the tested PR head. This was not a TEE.

- A real WARP Connector reported healthy; proxied HTTPS reported WARP and Gateway enabled. Three probes saw the same egress address, not a fixed-IP guarantee.
- Disconnecting WARP made the proxied request fail. Direct gateway-service HTTPS was rejected. In the recorder namespace, direct IPv4/IPv6, external DNS and Docker's embedded UDP resolver were blocked.
- A scoped read-only provider token could read health/connections and could not read the connector enrollment token. Signed provider observations included explicit unavailable samples. The witness ran on the operator's host, so this demonstrates recording and retention, not independent third-party custody.
- Official Desktop reached its unauthenticated welcome screen. Guarded keyboard input was rejected during capture. Three H.264 display segments decoded and their clock overlay was inspected. The 18-event preflight archive verified against the pinned recorder key and retained checkpoint.
- The final capture tests passed 114 cases on Windows and Linux CI, with real Chromium/FFmpeg. Five anchor tests and dependency advisory checks passed.

An initial 2 vCPU/4 GiB startup timed out under concurrent image-build load and stopped through the guard; it is not counted as success. Manual test-account login, native chat export, real hybrid comparison and Telegram-side logout remain pending. No supplied Telethon session was imported. Attachments, automatic OCR, local drand BLS verification and Trusted Live TDX attestation were not qualified.

## פריסה חיה ב-Phala Cloud · 4 בנובמבר 2026

**Historical result:** later deployments passed all 16 verifier checks, including Intel TDX and the quick tunnel. Restart evidence, signed address discovery and report timestamps were checked separately. Each test CVM was removed after its run.

| הגדרה | Recorded value |
| --- | --- |
| ספק | Phala Cloud · `tdx.small` · US-WEST-1 |
| פריסה | `--provider phala --quick-tunnel`; initially empty workspace |
| Initial collector | `df7d860c` · v0.8.1 |
| Collector with all fixes | `53a0f7e9` |
| Production guest | `dstack-0.5.12`; SSH access disabled |
| External services | ntfy.sh, GitHub and Intel PCS |
| Observed cost | Seven CVMs, about 1.9 US cents together; historical test pricing |

The sequence below separates initial failures, fixes and completed checks. No Telegram account was connected to these CVMs.

**Deployments 1–2 · provider differences and regression checks**

בשתי הפריסות הראשונות נמצאו חמישה הבדלים ביחס ל-Phala Cloud המדומה. [`tools/check_phala.py`](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_phala.py) משחזר כעת כל אחד מהם, ונכשל ללא התיקון:

| ב-Phala Cloud | לפני התיקון | תיקון |
| --- | --- | --- |
| `compose_file.name` נדרש | HTTP 422, לא נוצר דבר | תצורת ה-Docker Compose נושאת את שם ה-CVM |
| אלא אם כן ניתן שם ריק, Phala מוסיפה את סקריפט ההפעלה המוקדמת שלה ל-app-compose הנמדד (v0.0.20: התחברות ל-Docker, `docker compose pull`, סיסמת root, מפתחות SSH מ-`user_config`) | `tdx_compose` נכשל: קוד מחוץ לתצורת Docker Compose שפורסמה | קובץ ה-app-compose מגדיר את `pre_launch_script` כ-`""`; Phala משמיטה אותו |
| ללא `image`, Phala בוחרת ב-`dstack-dev-0.5.12`, גרסת הפיתוח, עם גישה ל-SSH מופעלת | `server_state` נכשל. רק רשומת אימות החומרה עברה בהצלחה בתמונה זו; רק רשומת הספק ו-`tdx_os` מציגים זאת | הפריסה מבקשת את גרסת הייצור של המהדורה הנוכחית של Phala, `dstack-0.5.12` |
| כאשר שער ה-dstack כבוי, פרטי ה-CVM לעולם אינם מקבלים `instance_id` | הפריסה ממתינה 30 דקות ונכשלת | מזהה המופע נקרא ממצב ה-CVM |
| הפעלה מחדש, עצירה והפעלה הן פעולות CVM, ולא עדכוני יישום | `provider_actions` לא ציין את הפעולות מחדש | הפעולות נקראות גם כן |

**Deployment 3 · attestation, access checks and restart evidence**

- ה-CVM הפעיל את `dstack-0.5.12` עם גישה ל-SSH כבויה. האספן פרסם את כתובתו החתומה כ- 1.5 דקות לאחר יצירתו. לאחר מכן, הפריסה העבירה את `tdx_binding`, `tdx_quote` (Intel TCB UpToDate, רשומת אימות חומרה v4, FMSPC `20a06f000000`, לא במצב ניפוי באגים, לא ניתן להעברה, תומך בנתוני אימות קריפטוגרפיים שהורדו מ-Intel), `tdx_compose_hash`, `tdx_compose` (בייט אחר בייט) ו-`tdx_identity` (מפתחות KMS).
- הלוח בכתובת trycloudflare.com השיב 401 ללא אסימון או עם אסימון שגוי, ו-200 עם אסימון הלוח.
- `verify` כאשר `--source` מוגדר לארכיון ה-GitHub של ה-commit והטביעת אצבע עברה בנפרד: שרת, `server_state`, חומת אש (ללא שער, ללא נקודת קצה ציבורית), יומן ספק, דוח, טביעת אצבע, hash מקור, אתחול וחמש בדיקות `tdx_*` עברו. Cloudflare ו- `tdx_os` לא היו זמינים, ולכן התוצאה הייתה INCOMPLETE.
- שתי הפעלות מחדש באמצעות ה-API של Phala: בכל פעם ה-CVM חזר לפעול תוך פחות משתי דקות עם אותו מפתח אספן, כתובת חתומה חדשה, והכתובת הישנה שענתה 530. `verify` דיווח על האתחול החדש ועל שתי ההפעלות מחדש כ-REVIEW. עם `--evidence` הוא אישר את חתימות היומן ואת שלושת ההפעלות, כאשר לכל אחת מהן היה רשומת אימות חומרה Intel TDX משלה מאותו CVM.
- הפקודה `destroy` הסירה רק את ה-CVM הזה. לאחר מכן, סביבת העבודה הייתה ריקה, וכתובת הלוח הפסיקה להגיב.
- בדיקת המחיר באשף הפאנל הראתה `tdx.small` במחיר של 0.058 דולר לשעה. מפתח שגוי גרר הודעה פשוטה "לא התקבל מפתח ה-API".

**Follow-up fixes · signed address discovery and OS measurements**

- ללא מפתח הכתובת, `verify` עקב אחר הפוסט האחרון והתקין בנושא הכתובת, המופיע בתצורת Docker Compose שפורסמה. פוסט מזויף אחד שלח אותו למארח שאינו קיים, ו-`statement` נכשל: זייפן לא יכול היה להתחזות לאספן, אך יכול היה לחסום אימות צד שלישי, למשך עד 12 שעות באמצעות חותמת זמן עתידית מזויפת. האספן כעת מפרסם גם את כתובתו חתומה במפתח שלו, `verify` מקבל רק פוסטים כאלה כאשר האספן מפרסם אותם, והפוסטים ממוינים לפי זמן הקבלה של ntfy.sh. [`tools/check_cloud_wizard.py`](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_cloud_wizard.py) משחזר את הפרסומים המזויפים. CVM מפעיל זאת רק מתוך commit המכיל אותה, ולכן האספן של הריצה הזו עדיין לא חתם על כתובתו ו-`verify` ציין זאת.
- `tdx_os` לא יכול היה לפעול ללא `dstack-mr`, שגרסתו הנוכחית כוללת את `measure-os` במקום את `measure --json` המוזכר בתיעוד. המאמת מחשב כעת את MRTD ו-RTMR0-2 בעצמו מהתמונה שפורסמה וממבנה ה-VM, כולל טבלאות ACPI.

**Deployment 4 · all 16 checks, report seals and restart verification**

- הפריסה הורידה את ה-`dstack-0.5.12` שפורסם פעם אחת, התאימה אותו להאש של תמונת מערכת ההפעלה ש-CVM דיווח עליה, ו-`tdx_os` עבר: MRTD, RTMR0, RTMR1 ו-RTMR2 שווים לערכים שחושבו עבור QEMU 8.2.2, 1 vCPU ו-2 GiB. אותו חישוב הניב ערך RTMR0 שונה עבור 4 GiB מוצהרים, 2 vCPUs, QEMU 9.2.1 או כרטיס רשת שני, ונכשל עבור גרעין, קושחה או שורת פקודה ששונו וכן עבור תמונת הפיתוח.
- `verify` עבר את כל 16 הבדיקות, כולל מחבר המנהרה המהירה, ולכן התוצאה הייתה "עבר". הוא כתב את תעודת ה-HTML וה-PDF, שנחתמו דיגיטלית בחתימות ובחותמות זמן עם חותמת זמן eIDAS מוסמכת מ יחידת חותמות הזמן של ממשלת בלגיה TSU 202301 (סטטוס שהוענק ברשימת האמינות של בלגיה ), חותמת זמן FreeTSA וחתימת המאמת; `check-report` אישר את כולן ואת חתימת ה-PDF.
- לאחר הפעלה מחדש, `verify --evidence` אישר שתי הפעלות, שכל אחת מהן לוותה באישור חומרה שנוצר בתוך ה-CVM וכל אחת הופעלה מה-`dstack-0.5.12` שפורסם; ההפעלה מחדש והאתחול החדש היו בדרגת REVIEW.
- `destroy` השאיר את סביבת העבודה ריקה.

**Deployment 5 · collector-signed discovery and forged-post rejection**

The collector ran from commit `53a0f7e9`, which includes the fixes above.

- האספן פרסם את כתובתו, חתומה במפתח שלו, לצד ההודעה של המפעיל עם ה-HMAC. לאחר מכן נוספו לנושא שתי הודעות מזויפות, אחת עם HMAC מאופס ואחת חתומה על ידי מפתח Ed25519 אחר, שתיהן טוענות לתאריך בשנת 2096. `verify` לקח את הכתובת החתומה על ידי מפתח האספן ועבר את כל 16 הבדיקות; החותם נשא שוב את חותמת הזמן הבלגית המוסמכת, את חותמת הזמן של FreeTSA ואת חתימת המאמת, ו-`check-report` אישר אותם.
- לאחר הפעלה מחדש, האספן פרסם את הכתובת החדשה החתומה: `verify` מצא אותה מיד, המפעיל **מצא את הכתובת הנוכחית** 27 שניות לאחר הפרסום ב-HMAC, ושניהם התעלמו מהפרסומים המזויפים. `verify --evidence` אישר שתי הפעלות שהותחלו מ-`dstack-0.5.12`.
- הפריסה הציגה את הסכום ש-Phala גובה עבור ה-CVM, כולל הדיסק: 0.06078 דולר לשעה.

### Panel wizard and remaining scope

אשף הפאנל הופעל פעמיים ב-Phala Cloud, פעם אחת דרך ממשק ה-API של המשימות ופעם אחת דרך הדפדפן עם Chromium אמיתי: בדיקת המחיר, יצירה עם ה-commit תחת **Advanced**, כל שש בדיקות האישור עברו בהצלחה, רשימת השרתים מציגה את המחיר שחויב (44.37 דולר לחודש), **Find הכתובת הנוכחית**, הורדת תצורת Docker Compose שנמדדה, והמחיקה. הדפדפן לא זיהה שגיאות בדף. בכל פעם, סביבת העבודה הייתה ריקה לאחר מכן.

Not covered: a Cloudflare domain on Phala, a Telegram account on the CVM, and the `dstack-0.6.1` image. The wizard's price before creation is Phala's compute price only, as its API names the disk price only for an existing CVM; the server list shows the billed price after creation. All prices in this section were observed on 4 November 2026.

## Live server journal inventory · 1 November 2026

At approximately 19:15 UTC, sequential read-only SQLite `query_only` queries counted events in ten workspace databases on a running server. Collection continued during the queries, so this is not an atomic snapshot across workspaces.

| Observed across the ten workspace databases | ספירה |
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

| בדוק | What it exercised |
| --- | --- |
| [Source archive](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_source_archive.py) | Two builds with identical source bytes but changed file times produced the same ZIP and checksum. Exact archived bytes and file hashes matched; private test files stayed out. A simulated write failure left the previous archive and checksum intact. |
| [Account export recovery](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_account_export_recovery.py) | A simulated disk error on the second ZIP member left no published or partial ZIP. Resume kept every signed receipt byte-identical, produced an independently verifiable archive using the expected signing fingerprint, and retained the synthetic coverage gap as a partial result. Scale assertions guard against repeated task and receipt scans as histories grow. |
| [Minimized disclosure privacy](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_disclosure_privacy.py) | Synthetic Unicode names and aliases, nested metadata, unknown senders and media fields were checked in all three identity modes and with text omission. A masking-limit failure did not silently weaken redaction; the original signed account export stayed unchanged. |
| [Linux media decoder and OCR](https://github.com/phishdestroy/TgWitness/blob/main/tools/check_media_worker.py) | A [Linux Docker CI check](https://github.com/phishdestroy/TgWitness/actions/runs/41341200341/job/124951395192) at commit `5a9e0814` passed generated Ogg/Opus, MP3, M4A, MP4 with video, WAV and FLAC inputs; forged-duration and secondary-file-reference controls; and 48 mutated parser fixtures (34 rejected, 14 decoded within bounds). Real Tesseract OCR ran with original bytes unchanged. The decoder and OCR ran in network-isolated containers without a Whisper model. |

The checks run in the [pull-request](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/pr-check.yml) and [full Checks](https://github.com/phishdestroy/TgWitness/blob/main/.github/workflows/checks.yml) workflows. They test these failure boundaries, not every possible storage failure or whether a disclosure is automatically safe to publish. The media check does not measure speech recognition accuracy or Telegram delivery. Review each derivative before sharing.

## בדיקת טלגרם בזמן אמת, חשבון שלם · 29 באוקטובר 2026

אותו חשבון המשיך לפעול לאחר הבדיקה המפורטת להלן. ב-29 באוקטובר בשעה 12:10 UTC הוחלף היקף התיעוד לכל החשבון (ערוצים, קבוצות, צ'אטים פרטיים ובוטים); הלוח ביקש אישור והיומן החתום תיעד זאת. בשעה 17:59 UTC נכלל ביומן:

| נרשם בין 27 באוקטובר בשעה 21:36 ל-29 באוקטובר בשעה 17:59 UTC | ספירה |
| --- | --- |
| רישומי היומן | 9,968 |
| הודעות חדשות | 5,308 |
| מתוכם לאחר המעבר לחשבון המלא | 3,878 |
| מחיקות | 784 |
| מתוכם נמחקו לאחר ש-TgWitness שמר את ההודעה | 596 |
| עריכות | 41 |
| הודעות שנוספו לאחר בדיקה חוזרת | 2,273 |
| הודעות שלא ניתן היה לאתר בבדיקה חוזרת | 18 |
| הודעות שנשמרו באמצעות תמונות מצב של ההיסטוריה | 242 |
| קובצים מצורפים שנשמרו | 247 |
| Collector מתחיל לפעול | 19 |
| Telegram FloodWait בהשהיה | 26 |

- בדיקת **ה-Verify** של הפאנל אימתה את החתימות ואת שרשרת ההאש של כל 9,968 הרשומות.
- ההודעות הגיעו משתי קבוצות או ערוצים, משלושה צ'אטים פרטיים ומבוטים. לחצן הודעה אחד נלחץ מתוך **הצ'אטים**; הבקשה ותשובת Telegram מופיעות ביומן.
- צ'אטים חדשים נוספו כאשר האספן סרק מחדש את החשבון לאחר הפעלה מחדש. שמירת ההודעות המוקדמות יותר של הצ'אטים החדשים הייתה כבויה (`history = 0`), ולכן היא אינה נכללת כאן.

לא נכללים: תגובות, שינויים בחברות, פרופילים אישיים, שליחת הודעות, הצטרפות באמצעות הזמנה, פרוקסי, התראות, בוט ה-Witness ושימוש במספר חשבונות בו-זמנית. הקבצים הציבוריים מכילים נתונים מספריים בלבד.

## ייצוא מוגן בסיסמה שנפתח באמצעות libarchive · 29 באוקטובר 2026

ארכיון שנכתב באמצעות קוד הצפנה לייצוא (WinZip AES-256, הפורמט ש-7-Zip ו-WinRAR קוראים) נפתח באמצעות Windows `tar` (bsdtar 3.6.2, libarchive). עם הסיסמה הנכונה, הקובץ שחולץ תאם את ה-SHA-256 המקורי; סיסמה שגויה נדחתה עם ההודעה "סיסמה שגויה". תוכנות 7-Zip ו-WinRAR עצמן לא הופעלו.

## בדיקה חיה ב-Telegram · 27 עד 29 באוקטובר 2026

חשבון Telegram אמיתי אחד, שנכנס באמצעות מאגר זוגות ה-API המובנה, תיעד קבוצת-על אחת מה**-27 באוקטובר בשעה 21:36 UTC ועד ה-29 באוקטובר בשעה 05:15 UTC**. האספן הופעל 12 פעמים בתקופה זו.

| מתועד | ספירה |
| --- | --- |
| רישומי היומן, כולל "פעימות לב" ורישומי שירות | 2,385 |
| הודעות חדשות | 1,291 |
| מחיקות | 472 |
| מתוכם נמחקו לאחר ש-TgWitness שמר את הטקסט | 347 |
| עריכות | 12 |
| הודעות שהוחמצו בזמן שהכלי היה מושבת, נוספו בבדיקה חוזרת | 12 |
| קובצים מצורפים שנשמרו | 17 |
| הקובצים המצורפים לא הורדו (הורדות כבויות, או שאין קובץ להורדה) | 14 |
| Telegram FloodWait עוצר ל-3 שניות בכל פעם במהלך בדיקות חוזרות | 8 |

- החתימות ושרשרת ההאש של כל 2,385 הרשומות מאומתות מול המפתח הציבורי של היומן.
- לאחר הפעלה מחדש, האספן ממשיך מהמצב המעודכן שנשמר (`pts`) ו-Telethon משלים את הפעולה; הבדיקה החוזרת מוסיפה אז את ההודעות שעדיין חסרות.
- בכל אירוע של FloodWait, האספן המתין את הזמן המבוקש והמשיך.
- החשבון נשאר מחובר, ואותה הפעלה התחברה מחדש ב-29 באוקטובר.

נושאים שאינם נכללים במבחן זה: מספר חשבונות בו-זמנית, תפקידי מנהל, פרוקסי, שיבושים הנמשכים יותר מכמה שעות והליך [הקבלה המלא בזמן אמת](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md). הקבצים הציבוריים מכילים רק את הנתונים הבאים: ללא מזהי חשבונות או צ'אטים, הודעות או פרטי הזדהות.

## מדידת יכולת מקומית סינתטית

פקודה: `python tools/check_capacity.py --events 10000 --chats 100`

| מדד | נצפה |
| --- | --- |
| קלט | 10,000 אירועי הודעות סינתטיות מ-100 מקורות סינתטיים נבחרים |
| טקסט ההודעה | 400 תווים; ללא מדיה או רשת |
| קליטה | 53.273 שניות; 187.7 אירועים בשנייה |
| זמן השהיה של המטפל | p50 4.162 ms; p95 7.784 ms; מקסימום 129.118 ms |
| ייצוא ZIP | 19.868 שניות עם tracemalloc מופעל |
| הקצאות ייצוא ב-Python שעברו מעקב בשיא | 0.51 MiB; לא מעבד RSS |
| גודל קובץ ZIP | 4,610,962 בתים |
| אימות עצמאי | כל 10,000 האירועים אומתו |

מדידה זו מודדת את נתיב ההקלטה/ייצוא הסדרתי המקומי במארח Windows זה. היא אינה מודדת משלוח MTProto, חשבונות מקבילים, הגבלת רוחב פס ב-Telegram, מדיה, עומס עבודה מתמשך או מספר מובטח של צ'אטים אמיתיים. המדידה קדמה לכלי חותמת הזמן הסופי במצב לא מקוון, אשר אינו משנה את נתיב ההודעות הנמדד.

## חיפוש טקסט מלא במיליון הודעות · 5 בנובמבר 2026

פקודה: `python tools/bench_fulltext.py --messages 1000000 --work <empty directory>`

יומן חתום דטרמיניסטי של 1,000,000 הודעות סינתטיות ב-200 צ'אטים (צורות מילים ברוסית, אוקראינית, אנגלית, סינית, יפנית, קישורים וכינויים) הועמד באינדקס תוך 71 שניות; האינדקס תפס 58 MiB בנוסף ליומן בגודל 1.50 GiB. חיפושים לפי התאמה מיטבית ארכו בין 9 ל-190 מילי-שניות (חציון), לעומת 2.4 עד 3.2 שניות בחיפוש הקודם לפי תת-מחרוזת . תוצאות מלאות, חומרה ומגבלות: [חיפוש טקסט מלא](https://phishdestroy.github.io/TgWitness/he/docs/reference/search/#benchmark). `tools/test_fulltext.py` מאמת גם ארכיון חתום שנוצר לפני חיפוש הטקסט המלא (`tools/fixtures/evidence-before-fulltext.zip`) באמצעות המאמת הנוכחי, וכן ארכיון נוכחי עם הארכיון של אותו ארכיון עצמו `verify.py`.

## הסתייגות נוספת

יומן החי הנשמר מתעד איסוף אמיתי, עריכות, הודעות מחיקה, קבצים מצורפים, בדיקות חוזרות וטיפול במגבלות קצב. הוא אינו מתעד מסירה ממצה או מטריצה מבוקרת של נראות תפקידים, גורמים מגיבים, FloodWait ממושך, חסימות חשבונות ו התאוששות מהפרעות ברשת/בתהליכים. הנפקת אסימון QR נותרת נפרדת מאימות QR סלולרי שהושלם.

Docker/Compose and installation checks are recorded in CI; real Phala deployment and external timestamp verification are described above. They do not establish sustained high load, a complete live platform/role matrix, independent security review, long-term archival validation or forensic certification. Saved MTProto state and catch-up are implemented; atomic lossless live replay remains unestablished. The newer backfill commits messages and cursors atomically and preserves available Recent Actions, but its synthetic coverage is distinct from live qualification. See [live acceptance](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md) for the controlled qualification matrix.

The [public audit directory](https://github.com/phishdestroy/TgWitness/blob/main/website/validation/audit/README.md) contains only the signed report and aggregate measurements. Detailed operational receipts, raw captures and account material remain private. Application screenshots in `docs/assets/` use fictional demonstration data.
