# אבטחה וטיפול בנתונים

Canonical page: https://phishdestroy.github.io/TgWitness/he/docs/reference/security/

מודל איומים, מודל גישה, מידע סודי במאגר, חשיפה ברשת, ייבוא הפעלות וכיצד לדווח על פגיעות אבטחה.

This page describes access，storage and network protection in a local or server workspace． For collection on a GitHub runner or in an Intel TDX confidential VM，see the [verification modes](https://phishdestroy.github.io/TgWitness/he/docs/reference/evidence/#verification-scope)，which add checks of the collection environment． Account connections，notifications，timestamps，off-site copies and witnesses have their own routing settings．

| תחום | בקיצור |
| --- | --- |
| גישה | מפתח מנהל בתוספת גישה מוגבלת לחשבונות/צ'אטים, שבע רמות הרשאה ומפגשים הניתנים לביטול; localhost כברירת מחדל |
| סודות במנוחה | ההגדרות של ההפעלה, זוג ה-API, מפתח החתימה והגדרות ה-proxy מוצפנות באמצעות Fernet |
| הודעות ומדיה | מאוחסן ללא הצפנה: יש להשתמש בהצפנת דיסק ובהגבלות גישה קפדניות |
| יושרה | שרשרת חשיש SHA-256 וחתימת Ed25519 על כל רשומה |
| Local trust boundary | The host administrator controls the workspace and its signing key；independent checkpoints retain an earlier journal boundary |

לדיווחים על פגיעויות, ראו את [מדיניות האבטחה](https://github.com/phishdestroy/TgWitness/blob/main/.github/SECURITY.md).

## מודל גישה

אסימון הפאנל הראשי מעניק שליטה מלאה. משתמשים אחרים יכולים לקבל [גישה מוגבלת](https://phishdestroy.github.io/TgWitness/he/docs/reference/access/): סביבות עבודה וצ'אטים נבחרים, הרשאות, תוקף, הגבלות IP, מגבלות כניסה ומפגשים הניתנים לביטול. גישה המוגבלת לצ'אט אינה מאפשרת לבצע פעולות בכל סביבת העבודה, גם אם ההרשאה מסומנת. סביבות העבודה חולקות תהליך ואינן מבודדות את הנתונים מהמנהל המארח.

כברירת מחדל, הפאנל מאזין ב-localhost. כניסה דרך הדפדפן מחליפה אסימון גישה בתעודת זהות של הפעלה; הדפדפן שולח אותה כאסימון נושא. היא נשמרת ב-sessionStorage ולא בעוגיית אימות. נעילה/יציאה מוחקת את הפעלת הדפדפן. סגירת הדפדפן או סיום הפעלה אינם עוצרים את האיסוף.

אסימונים שהונפקו ואישורי גישה למפגשים נשמרים כ-hashes בכספת המוצפנת. ביטול האסימון מסיים את המפגשים הקשורים אליו; שינויים בהרשאות משפיעים על בקשות עתידיות. לא ניתן לבטל קבצים שהורדו. המנהל יכול להגביל גם את מפגשי הדפדפן שלו עצמו, אך סקריפטים המשתמשים ישירות באסימון של לוח הבקרה הראשי שומרים על גישה מלאה ועוקפים את מגבלות מפגשי הדפדפן הללו.

אימות כושל מוגבל לפי קצב לפי כתובת הלקוח. הגבלות ה-IP משתמשות בכתובת שנראית על ידי היישום; יש לבדוק את התנהגות ה-reverse-proxy לפני שמסתמכים עליה. אמצעי הזיהוי של Witness נשארים נפרדים, כנקודת ביקורת לקריאה בלבד או כאמצעי זיהוי לבדיקת תקינות.

### גישה לדמו

`/api/demo-access` הוא בוטסטראפ שלא אומת בכוונה, המיועד להדגמה סינתטית מבודדת שהופעלה במפורש. הוא מנפיק יכולת נפרדת לתקופת חיי התהליך, לעולם לא את אסימון הפאנל האמיתי או עקיפת TGWITNESS_TOKEN. ההנפקה והשימוש דורשים עמית לולאה אחורית (loopback) ומארח, ללא כותרות מועברות וללא בקשות בין-מקורות. סביבות עבודה נוספות או הפעלה מורשית מבטלות נתיב זה. סביבות עבודה פעילות לעולם אינן מנפיקות את היכולת. ההדגמה אינה יכולה לחבר חשבונות או לשנות הגדרות איסוף.

## תוכן הלוח וייצוא נתונים

הפאנל אינו משתמש בגופנים חיצוניים, בניתוח נתונים, במשאבי CDN או במדיה מרוחקת משובצת. טקסט שמקורו ב-Telegram מוחדר כטקסט, ולא כ-HTML. קבצים מצורפים שהורדו מוצגים כקבצים בינאריים. ייצוא בפורמט JSONL משמר את המחרוזות המקוריות; HTML מבצע החלפה של תווים; לתאי CSV שעלולים להפוך לנוסחאות מתווסף קידומת של גרש.

הייצוא אינו כולל סודות אימות וחתימה, אך מכיל במכוון מטא-נתוני מקור שנאספו, מזהים, וייתכן שגם תוכן אישי או רגיש. במטא-נתוני המקור הגולמיים עשויים להופיע חשישים של גישה ל-Telegram והפניות לקבצים.

## סודות במנוחה

Telegram API credentials，the session and signing key are encrypted with Fernet． For local messages and media，encryption is provided by the host's disk or volume； the workspace stores ordinary files．Exports can use a password-protected AES-256 ZIP， and off-site copies use AES-256-GCM．

The vault key defaults to the protected data directory．Use an external master-key file below to store it separately．On Unix，new private-key files use mode 0600 and new data directories use 0700；on Windows，set the directory ACL for the service account and authorized administrators．Existing directory permissions are retained．

### מפתח ראשי חיצוני

For a new data directory, TGWITNESS_VAULT_KEY_FILE can supply an external random master key. HKDF-SHA256 and a separate random salt derive a different Fernet key for each workspace. vault.external.json must be retained for recovery. Missing or wrong master keys fail closed. Existing local vaults are not silently migrated. The panel displays the selected key-storage mode．Disk encryption protects the local message and media files in either mode；see [connection and data protection](https://phishdestroy.github.io/TgWitness/he/docs/reference/connection/) for setup details．

## פרוקסי ונתיבי רשת

תצורת ה-Proxy מוצפנת בכספת. סיסמאות וסודות MTProxy אינם מוחזרים על ידי ה-API ואינם נכתבים ברשומות הראיות. כל סביבת עבודה בוחרת את נתיב ה-Telegram שלה ואת [מצב ה-IP](https://phishdestroy.github.io/TgWitness/he/docs/reference/connection/#ip-modes).

**הסתרת הכתובת** מונעת שימוש ישיר ב-Telegram כגיבוי ודורשת פרוקסי עבור בקשות HTTP חיצוניות. מצב הגיבוי שנבחר במפורש מאפשר גישה ישירה ל-Telegram לאחר עיכוב; מצב מנהרה/VPN מאפשר נתיבים ישירים. בחירת מצב המנהרה אינה מתקינה או מאמתת VPN. הגדרות אלה אינן שולטות בכל התעבורה של המחשב, בדפדפנים, במנהלי החבילות או בפתרון ה-DNS של מארח הפרוקסי המקומי.

MTProxy מעביר רק תעבורת טלגרם. בקשות חיצוניות יכולות להשתמש ב- פרוקסי SOCKS5/HTTP נפרד, בנתיב SOCKS5/HTTP של סביבת העבודה, או בנתיב ישיר מותר; ניתן גם להשבית אותן. ל-Witness העצמאי יש הגדרות העברה משלו. אימות SOCKS5/HTTP CONNECT רגיל אינו מוצפן על ידי פרוטוקולי הפרוקסי עצמם. סודות TLS מזויפים של MTProxy אינם נתמכים.

## כניסה וייבוא נתוני הפעלה

קבצי .tgwitness-session שהומרו מכילים סוד אימות בטקסט רגיל עד לטעונם ואחסונם בכספת. ממשק ה-CLI המקוון מקבל סכמות Telethon שנבדקו. ייבוא הפאנל מקבל בנוסף Pyrogram SQLite, ZIP של TData מודרני לחשבון יחיד, וקבצי JSON מתועדים. הוא מאומת, מוגבל לארבעה קבצים / 8 MiB, ומעבד העלאות בזיכרון ללא חילוץ ארכיונים או שמירת קבצים מקוריים. אישורי הכניסה המנורמלים מוחזרים רק לדפדפן המאושר המבקש; הם נשמרים בכספת המוצפנת לאחר אימות מוצלח ב-Telegram. יש להגן על הקבצים המקוריים והקבצים שהומרו, ולמנוע מלקוחות מקבילים לשכפל אישור.

עיבוד הנתונים מאמת סכומי ביקורת של קונטיינרים, חשישים של פענוח מקומי ואורכי מבנה. קוד גישה מקומי לשולחן העבודה שסופק משמש באופן זמני ואינו נשמר. מנתח תחבירי מוגבל זה אינו קובע שכל גרסת שולחן עבודה תואמת. תמונות QR נוצרות באופן מקומי, מכילות אסימוני כניסה לטלגרם בעלי תוקף קצר, ו לעולם אינן נשלחות לשירות עיבוד חיצוני. נעילה, מעבר בין סביבות עבודה, כניסה חדשה, ושינויי מסלול מבטלים ניסיונות QR הממתינים לאישור. טעינה מחדש/סגירת כרטיסייה עלולה להשאיר ניסיון הממתין לאישור עד לפקיעת תוקפו. כניסה מוצלחת באמצעות QR עדיין מחייבת קישור חשבון. גופי API רגילים נשארים מוגבלים ל-16 KiB; מסלול הייבוא המאומת מקבל עד 12 MiB של JSON מקודד, תוך אכיפה נפרדת של המגבלה הקטנה יותר על קובץ מפוענח.

קודי כניסה וסיסמאות לאימות דו-שלבי ב-Telegram אינם נשמרים. מצב מספר הטלפון/ה-hash של הקוד נשמר בזיכרון במהלך תהליך האימות. הפעלות ב-Telegram מעניקות גישה לחשבון; לעולם אל תעלו ספריית נתונים, הפעלה, אסימון, מפתח כספת או מפתח חתימה פרטי ל-GitHub.

## יומנים והעברה

תגובת אימות ה-API המוגדרת כברירת מחדל הוחלפה כך שלא תחזור על ערכי האישורים. רישום הגישה ליישום מושבת. אין להגדיר פרוקסי הפוך כדי לרשום כותרות אימות או גופי בקשות. פרוטוקול HTTP מעביר אסימונים ופרטי התחברות בטקסט גלוי: יש להשתמש ב-HTTPS או במנהרת SSH בכל פעם שיוצאים מ-localhost.

## מגבלות שלמות

Local verification checks record signatures，the hash chain，attachments and the export manifest． The administrator holds the local signing key and can create another signed journal； an independently retained checkpoint detects replacement of the prefix it covers． Keep the key fingerprint and checkpoints with the recipient or an independent witness．

For independently checked collection，choose [GitHub Actions capture](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md) or [Intel TDX deployment](https://phishdestroy.github.io/TgWitness/he/docs/reference/high-assurance/#confidential-vm-on-phala-cloud-intel-tdx)． Their verifiers check workflow provenance or hardware measurements in addition to archive integrity． Optional timestamps and encrypted off-site copies provide time anchors and recoverable copies； the [evidence format](https://phishdestroy.github.io/TgWitness/he/docs/reference/evidence/#verification-scope) describes the checks for each mode．

## אם אתם חושדים בבעיה

Preserve the original data directory and use a separate copy for analysis． Report the affected version，operation and reproducible steps through the [security policy](https://github.com/phishdestroy/TgWitness/blob/main/.github/SECURITY.md)，keeping account data and credentials private．
