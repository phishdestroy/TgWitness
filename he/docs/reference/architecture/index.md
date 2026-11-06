# ארכיטקטורה

Canonical page: https://phishdestroy.github.io/TgWitness/he/docs/reference/architecture/

מרכיבי האספן, לוח הבקרה, היומן, העובדים וה-Witness, וכיצד הנתונים עוברים ביניהם.

תהליך Python אחד מארח את לוח הבקרה של FastAPI ומספר בלתי מוגבל של סביבות עבודה מבודדות, כשכל אחת מהן כוללת לקוח חשבון משתמש של Telethon. SQLite מכיל יומן אירועים חתום שניתן להוסיף אליו בלבד, וכן הגדרות תפעוליות הניתנות לשינוי. כספת מוצפנת מאחסנת את פרטי הזיהוי של ה-API, את ה-StringSession ואת מפתח החתימה. ה-frontend מורכב מקובצי HTML/CSS/JavaScript רגילים: אין צורך בבניית Node, ב-CDNs או בהורדות frontend בזמן ריצה.

Optional browser and AyuGram recorders run in **separate processes or containers**. The `tgwitness_capture` package owns their event format, keys, artifacts, checkpoint API, independent witness and standalone verifier. It is bundled in the main wheel and can also be installed alone from `addons/capture`, without importing the collector. The main panel's `capture_api.py` and `capture_connections.py` provide administrator-only, workspace-scoped controls under `/api/capture`; connection tokens live in the encrypted vault. No recorder or outbound request starts with the main process. Each explicit command verifies a fresh challenge against the pinned recorder key. Exports are verified before download and keep their original signature; they do not become Telegram message events. Collection sessions and proxy routes stay with each client. See the English [Independent capture guide](https://github.com/phishdestroy/TgWitness/blob/main/docs/OPTIONAL-CAPTURE.md) for deployment and trust boundaries.

| מודול | אחריות |
| --- | --- |
| collector.py | אישור, בחירת דיאלוג, עדכונים, תמונות מצב, תור מדיה, ניטור חיבור |
| interactions.py / telegram_client.py | פעולות פאנל מפורטות, קבלות חתומות, מזהי בקשות קבועים ומדיניות ניסיונות חוזרים מקומיים למשימות של שיחות חוזרות/הצטרפות |
| message_content.py | השוואת הודעות נראית לעין, ללא מטא-נתוני גישה לתעבורה |
| workers.py | יש להמתין לעובדי ייצוא הקבצים לפני ביצוע ניקוי הביטולים |
| distributed_export.py / distributed_pages.py | Concurrent chat jobs, per-account reservations, signed checkpoints and cleanup after archive verification |
| distributed_takeout.py / export_timing.py | Resumable Takeout sessions and timings for each start or resume |
| store.py | עסקאות WAL, שרשרת אירועים מסודרת, מסנני שאילתות, הגדרות תפעוליות |
| fulltext.py | אינדקס טקסט מלא נגזר (צורות מילים, BM25), המקושר לכותרת היומן החתום; לא מיוצא לעולם |
| security.py | יצירת קובץ פרטי, כספת מוצפנת, חתימה ב-Ed25519, נעילת תהליך יחיד |
| evidence.py | ייצוא יומן מלא, נגזרות, נקודות ביקורת, אימות קבצים מצורפים |
| verify.py | מאמת עצמאי, לקריאה בלבד (stdlib + קריפטוגרפיה): ארכיונים, כיסוי, יומני עדים והודעות בערוצים, קבצי פרופיל |
| app.py | API מאומת, מחזור חיים, אימות בקשות, לוח סטטי |
| profiles.py | אספני חשבונות מרובים, בקר גישה משותף, מחזור חיים לכל סביבת עבודה |
| access.py | היקף ההרשאות, בדיקות הרשאות, הגבלות IP, מגבלות על הפעלה וקונסולת מנהל |
| proxy_catalog.py | תמונות מצב של פידים ציבוריים, בדיקות העברה, מאגר פרוקסי משותף ובחירה על סמך תקינות |
| provenance.py | מדידות חתומות של זהות, קוד ותלות, המבוצעות במהלך תהליך הרכישה |
| network.py | מסלולים מאומתים לכל סביבת עבודה; סטטוס וראיות שעברו עריכה; אפשרויות העברה של Telethon |
| sessions.py | המרה למצב קריאה בלבד (offline) של סכמות SQLite של Telethon שעברו בדיקה |
| account_import.py | זיהוי ונורמליזציה בזיכרון של קבצי חשבונות נתמכים ו-JSON |
| tdata.py | קורא ZIP מודרני ומוגבל של TData, אימות בדיקת סיכום/פענוח, ללא חילוץ |
| doctor.py | בדיקות מוכנות מקומיות ללא איסוף נתונים, התחברות או התקנת חבילות תוכנה |
| download.py | הורדת ייצוא זרם מאומת עם קריאות מוגבלות וללא כתיבה על קבצים קיימים |
| monitoring.py | מדיניות אירועים מאומתת לכל סביבת עבודה וכללי קבצים מצורפים לפי סוג, המשותפים למנהלי חשבונות, סטטוס וקבלות חתומות |
| scope.py | היקף הניטור (צ'אטים נבחרים, תיקיית טלגרם, חשבון שלם), סוגי מקורות, החרגות, רמות בדיקה חוזרת |
| dossier.py | פרופילים אישיים לכל צ'אט, הנבנים על בסיס רשומות שנשמרו: עובדות עם הפניות לרשומות, SHA-256/pHash של האווטאר, חילוץ אזכורים |
| witness_api.py | אסימוני עדים לקריאה בלבד וכותרת היומן החתום שהם עשויים לאחזר |
| witness.py | תהליך עדות עצמאי: מפתח ויומן משלך, בדיקות ראש, פוסטים חתומים בערוץ, ייצוא |
| alerts.py | התראות Apprise ורשימת ההתראות של הפאנל |
| logging_config.py | רישום יומני קונסולה ואבחון שרתים מתחלף עבור הפעלות ללא חלון |
| static/ | ממשק רספונסיבי, שער גישה מקומי, מסננים, פרטים, ייצוא, הגדרת חשבון |
| demo.py | יומן סינתטי המסומן בבירור, מבודד מהאיסוף האמיתי |

מטפלי התצפית נרשמים לפני ההתחברות. האיסוף בזמן אמת מוגבל על ידי זהות הלקוח הפעיל, מצב הפעלה מפורש, מקורות מופעלים או היקף התצפית (מצבי תיקייה או חשבון שלם מוסיפים צ'אט חדש כמקור בעת העדכון הראשון שלו), ומדיניות האירועים. לקוחות שנדחו או הוחלפו אינם יכולים לתרום עדכונים בזמן אמת. תגובות גולמיות ועדכוני חברות שומרים על מגבלות הנראות. תוכן ההודעה הנכנסת ומשימת המדיה הקבועה שלה נשמרים יחד. המשימות שומרות על תיאור ה-TL המקורי וקושרות את ה-hash שלו לתצפית ההודעה החתומה. הסמנטיקה של השולח/העורך/המחיק נפרדת.

כל סביבת עבודה מקבלת חשבון אחד ויש לה ספרייה וזהות חתימה משלה. סביבת העבודה הראשית נשארת בשורש למען תאימות; סביבות עבודה נוספות נמצאות ב- profiles/<id>/. אסימון נושא אחד שולט על כל ההתקנה; סביבות העבודה אינן דיירים נפרדים לצורך אישור. נעילות תהליכים מגנות על הספריות; נעילות מסד הנתונים מסדרות את הוספת האירועים. כל תוספת נרשמת באופן סינכרוני ל-SQLite WAL במצב סינכרוני מלא (FULL). מפעילים לעדכון/מחיקה של אירועים מונעים עריכות רגילות של היישום; מנהלי מערכת הקבצים נשארים בתוך גבול האמון.

API authorization is a bearer token. Login operations are serialized and time-bounded. Account uploads use a dedicated 12 MiB encoded-body limit and an 8 MiB decoded-file limit; normal API requests retain the 16 KiB limit. Conversion runs in a worker thread, keeps uploads in memory, and returns normalized input to the authenticated browser. QR login has a per-workspace candidate, short-lived identifier, waiter task, and explicit cancellation. Only accepted authorization becomes the active client. Telegram FloodWait is returned with a Retry-After value; credentials and raw RPC error messages are not exposed in API errors. Journal exports run outside the async event loop and are serialized per workspace. They stream a stable read snapshot alongside continuing WAL writes. Chat acquisition jobs can run concurrently on separate accounts; each account remains reserved until its job stops. A paused or failed job retains its checkpoints. Successful archive verification permits cleanup of its working files, leaving the ZIP, signed plan and status. Workspace collectors share the process/event loop.

תמונות מצב היסטוריות עדכניות ועדכונים בזמן אמת עשויים לחפוף. שתיהן מהוות תצפיות נפרדות, המסומנות לפי מקור; כפילויות אינן מוסתרות באופן אוטומטי. לא מיושמת כל הסקה הנובעת מ- מזהים חסרים, טקסט שנמחק באופן מזויף, ספירת חברים בכפייה או הצטרפות אוטומטית לקבוצות. .

להסבר המיועד למפעילים, ראו [כיצד פועל תהליך האיסוף](https://phishdestroy.github.io/TgWitness/he/docs/reference/collection/) וכן [את פורמטי החשבונות והפעלות](https://phishdestroy.github.io/TgWitness/he/docs/reference/accounts/).

תצורת הרשת מאוחסנת בכספת המוצפנת. יישום מסלול סוגר לקוחות ישנים ומבטל כניסות שלא הושלמו; חיבורים מאוחרים יותר משתמשים באותו מסלול ללא גיבוי ישיר. התקנה חדשה עם מפתח חיצוני מפיקה את מפתח ה-Fernet של כל סביבת עבודה באמצעות HKDF-SHA256 מקובץ מפתח ראשי ומ-salt אקראי מאוחסן. הדבר מגן על הסודות בנפרד מספריית הנתונים, ולא על תוכן היומן/המדיה בטקסט רגיל.

הכניסה לדמו המקומי משתמשת ביכולת תהליך שנוצרה בנפרד, לעולם לא באסימון הלוח שהוגדר. ההנפקה והקבלה דורשות מצב דמו מפורש, שורש סינתטי ללא סביבות עבודה נוספות או הפעלה מורשית, עמית/מארח בלולאה חוזרת, ללא כותרות העברת פרוקסי, וללא בקשת דפדפן בין-מקורות. ממשקי ה-API החיים שומרים על אימות נושא ומסרבים לשינויים באיסוף במצב הדגמה.
