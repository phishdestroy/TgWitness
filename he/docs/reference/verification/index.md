# מה נבדק

Canonical page: https://phishdestroy.github.io/TgWitness/he/docs/reference/verification/

הבדיקה החיה של טלגרם, בדיקות אוטומטיות, בדיקות דפדפן ומה שעדיין לא אומת.

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

## הסתייגות נוספת

יומן החי הנשמר מתעד איסוף אמיתי, עריכות, הודעות מחיקה, קבצים מצורפים, בדיקות חוזרות וטיפול במגבלות קצב. הוא אינו מתעד מסירה ממצה או מטריצה מבוקרת של נראות תפקידים, גורמים מגיבים, FloodWait ממושך, חסימות חשבונות ו התאוששות מהפרעות ברשת/בתהליכים. הנפקת אסימון QR נותרת נפרדת מאימות QR סלולרי שהושלם.

הרכבה/הפעלה ב-Docker, התקנה ב-Linux/macOS, עומס גבוה מתמשך, בדיקת אבטחה עצמאית, תגובה עצמאית אמיתית ל-TSA, אימות ביטול/ארכיון תעודות ו הסמכה פורנזית נותרים מחוץ לתחום ההסמכה המתועד. מצב MTProto שמור והשלמת פערים מיושמים; השמעה חוזרת אטומית ועמידה נותרה בלתי מבוססת. איסוף יומני מנהל, רשימות ריאקטורים נוספות וסקר קצר בעדיפות נשארים תכונות נפרדות. ראו [קבלה בזמן אמת](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/LIVE_ACCEPTANCE.md) עבור מטריצת ההסמכה המבוקרת.

קבלות וצילומי מסך מקומיים ומפורטים נמצאים בתיקייה test-results/ (מוחרגים ב-Git). צילומי המסך הציבוריים בתיקייה docs/assets/ מכילים אך ורק נתוני הדגמה פיקטיביים.
