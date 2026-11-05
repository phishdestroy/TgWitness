# הודעות משתנות． שמור את מה שראית．

Canonical page: https://phishdestroy.github.io/TgWitness/he/

[קוד פתוח ／ v0.9.1](https://phishdestroy.github.io/TgWitness/he/docs/reference/changelog/)

שמרו צ＇אטים של Telegram עם כל עריכה ומחיקה， ואז מסרו תיעוד שכל אחד יכול לבדוק．

[הדגמה פתוחה](https://phishdestroy.github.io/TgWitness/demo/?lang=he)[מדריך התקנה](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=he)

נתונים מזויפים， בלי התחברות ל－Telegram．

 [איסוף באמצעות GitHub Actions （גרסה מקדימה）](https://phishdestroy.github.io/TgWitness/he/docs/capture/) [עותק חיצוני ב－S3： הגדרה ושחזור](https://phishdestroy.github.io/TgWitness/he/#s3)

הודעה， לאורך הזמן ＃0042

Northstar · מחקרמקור／הודעה בדיונית 42

1. **הודעה שנצפתה：**09：41：02

   התדרוך מתחיל ב－14：00．
2. **עריכה נשמרה**09：43：18

   התדרוך מתחיל ב－15：00．

   הגרסה הקודמת נותרה על כנה
3. **הודעת מחיקה**10：06：45

   התוכן שנאסף נשאר ביומן שלכם．

שלוש תצפיות． היסטוריה אחת． דוגמה

ההודעה נעלמת． ההיסטוריה שנשמרה נשארת．

## כל שינוי שנלכד． בדיוק במקום שבו אתה צריך אותו．

הממשק האמיתי， עם נתונים מומצאים．

TgWitness ／ צ＇אטים שנשמרוסביבת העבודה שלך לתיעוד תצפיות

![שיחות טלגרם שנשמרו בעיצוב כהה， עם עריכות והודעות שנמחקו שנלכדו ונשמרו בהקשרן](https://phishdestroy.github.io/TgWitness/assets/chats-dark.png)

01 ／ צ＇אטים שמורים נראה כמו צ＇אט רגיל， עם עריכות ומחיקות ממש ליד ההודעות．

TgWitness ／ יומןסביבת עבודה מקומית

![יומן הכולל הודעות שנצפו， עריכות， הודעות על מחיקה ואירועים שנכללו בכיסוי](https://phishdestroy.github.io/TgWitness/assets/workspace.png)

02 ／ יומן כל מה שהחשבון שלכם ראה， ניתן לחיפוש， כולל פערים．

TgWitness ／ היסטוריית עריכותסביבת עבודה מקומית

![מגירת פרטים המציגה השוואה בין הגרסה הקודמת של ההודעה שנטמעה לבין הגרסה הערוכה שלה](https://phishdestroy.github.io/TgWitness/assets/detail.png)

03 ／ היסטוריית עריכות גרסאות ישנות וחדשות זו לצד זו， שום דבר לא נדרס．

TgWitness ／ ייצוא חתוםסביבת עבודה מקומית

![ייצוא סביבת העבודה המציע קבצי ZIP， JSONL ו－CSV חתומים， וכן דוח HTML למשתמש לא מקוון](https://phishdestroy.github.io/TgWitness/assets/exports.png)

04 ／ ייצואים חתומים קחו את היומן איתכם， חתום， עם כלי האימות שלו．

עקבו אחר רשומה שנשמרה באמצעות [Case Board](https://phishdestroy.github.io/TgWitness/he/docs/case-board/)， [עיצוב הדוח](https://phishdestroy.github.io/TgWitness/he/docs/reports/) וה[עתק](https://phishdestroy.github.io/TgWitness/he/docs/handover/) [לשיתוף](https://phishdestroy.github.io/TgWitness/he/docs/handover/)． [סקרו קבוצות חשבונות](https://phishdestroy.github.io/TgWitness/he/docs/groups/) יחד．

01 ／ לכידה

### אתם בוחרים את היקף הפעילות．

כמה צ＇אטים， תיקייה או החשבון כולו． לכל חשבון יש סביבת עבודה משלו．

[השוואת מצבי איסוף](https://phishdestroy.github.io/TgWitness/he/guides/modes.html#scope)

02 ／ PRESERVE

### השינויים תורמים לסיפור．

גרסאות， מחיקות ופערים נשארים כולם ביומן．

[ראו את מטריצת האירועים](https://phishdestroy.github.io/TgWitness/he/guides/modes.html#events)

03 ／ מסירה

### תיעוד שנשמר לאורך זמן．

ZIP חתום， קבצים ודוח לא מקוון． סיסמה אופציונלית．

[ייצא ואמת את](https://phishdestroy.github.io/TgWitness/he/docs/exports/)

## שינוי של בייט אחד．
האימות יגלה זאת．

כל אירוע מקושר להאש הקודם ונושא חתימת Ed25519．

![האירועים שנלכדו מקושרים להאשים קודמים， נושאים חתימות ומועברים בייצוא הניתן לאימות．](https://phishdestroy.github.io/TgWitness/assets/evidence-chain-animated.svg)

![שינוי של רשומה שנלכדה משנה את ה－hash שלה ופוגע באמינות האימות של הרשומה המקושרת．](https://phishdestroy.github.io/TgWitness/assets/evidence-tamper-animated.svg)

![נקודת ביקורת הנשמרת בנפרד מאפשרת למקבל להשוות את היומן המיוצא עם תצפית קודמת．](https://phishdestroy.github.io/TgWitness/assets/evidence-checkpoint-animated.svg)

יש לעקוב אחר הבדיקות החל מהאש של הקובץ ועד לנקודת ביקורת שנשמרה בנפרד．

[גלו שמונה רמות ראיות](https://phishdestroy.github.io/TgWitness/he/guides/modes.html#levels)

## מוכן לעיון נוסף．

הודעות， קבצים ודוח לא מקוון בחבילה חתומה אחת．

[קראו את מודל הראיות](https://phishdestroy.github.io/TgWitness/he/docs/reference/evidence/)

tgwitness-evidence.zipחבילה חתומה

- 01

  תצפיות מקוריותרשומות JSONL ＋ טבלת CSV
- 02

  הקשר קריאדוח HTML לא מקוון ＋ מדיה משומרת
- 03

  אימות עצמאירשימת תוכן חתומה ＋ בודק עצמאי

הנמען בודק הכול מול המפתח שלכם， ונקודת ביקורת שנשמרה במקום אחר מראה ששום דבר לא נכתב מחדש מאז． [איך הבדיקות עובדות．](https://phishdestroy.github.io/TgWitness/he/docs/concepts/#layers)

## עותקים ב－S3． בדיקות חיצוניות．

יש לשמור עותקים מוצפנים ולהוסיף בדיקות עצמאיות．

כבוי כברירת מחדל

### העתק הכל לאחסון תואם S3

יומן， קבצים， נקודות ביקורת וייצואי צ＇אטים， מוצפנים לפני שהם נשלחים ל－S3．

**הגדרות אחסון ושחזור**

הצפנה בצד הלקוח

`AES-256-GCM` על המחשב שלכם． הספק רואה רק טקסט מוצפן．

העתקות מתוזמנות או ידניות

העתיקו עכשיו או כל 1 עד 1，440 דקות， ההתקדמות מוצגת בלוח．

Object Lock

בחרו ימי שמירה ומצב， והלוח בודק שזה באמת נקלט．

שחזור מאומת

שמרו את המפתח בנפרד． שחזרו בכל מקום， הקבצים יוצאים רק אחרי אימות．

![לוח בקרות מלא מחוץ לאתר： נקודת קצה， אזור， דלי， מפתחות גישה， לוח זמנים， נעילת אובייקטים ובקרות מפתחות שחזור](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)

לוח הבקרה המלא עם האפשרויות המתקדמות פתוח． לא מוצגים פרטי הזדהות לאחסון．

יומן ותקשורת`AES-256-GCM`אחסון תואם S3

[הגדר את S3 ושחזר עותק](https://phishdestroy.github.io/TgWitness/he/docs/exports/#s3)[קראו את פרטי האימות](https://phishdestroy.github.io/TgWitness/he/docs/reference/evidence/#off-site-copy-and-restore-s3)

**מפתח שחזור** שמרו אותו בנפרד， בלעדיו העותק לא קריא．

### התראות · Apprise

בעיות， שינויים בצ＇אטים וסיכום יומי לאפליקציות מסרים， לדוא＂ל או ל－webhook משלכם．

**בחרו מה לשתף** בלי טקסט ההודעות， אלא אם תפעילו אותו．

 [הגדרת יעדי ההתראות](https://phishdestroy.github.io/TgWitness/he/docs/reference/operations/#notifications)

### חותמות זמן חיצוניות

חשיפת חתימות זמן （timestamp） באמצעות RFC 3161 ו－OpenTimestamps．

**עקבו אחרי התוצאה** בדקו את תשובת ה－TSA או שדרגו את קבלת OpenTimestamps להוכחת Bitcoin．

 [בדקו את הוכחות חותמות הזמן](https://phishdestroy.github.io/TgWitness/he/docs/reference/timestamp/)

### עד עצמאי

שרת נפרד שומר את התצפיות החתומות ויכול לפרסם נקודות ביקורת מסוג `TGW1`．

**הפרידו את נקודת הייחוס** הריצו על מארח אחר， עם מפתח ויומן משלו．

 [הגדר עד](https://phishdestroy.github.io/TgWitness/he/docs/witness/)

### שחזור ופערים ניכרים

המשך לאחר הפעלה מחדש． בדיקות חוזרות ו－`coverage.json` מציגות הודעות ששוחזרו ופערים．

**סקרו את המרווח** הודעות ששוחזרו ופערים שתועדו זה לצד זה．

 [בדקו את הרצף והפערים](https://phishdestroy.github.io/TgWitness/he/guides/modes.html#continuity)

## סביבת העבודה הראשונה שלכם מתחילה כאן．

נסו קודם את ההדגמה， וחברו חשבון רזרבי כשתהיו מוכנים．
Windows， Linux， macOS או Docker．

[קרא את מדריך ההתקנה](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=he)

**פעולה אחת מיובאת， לקוח אחד פועל．**

אל תריצו TData או סשן מיובא ב－Telegram Desktop וב－TgWitness בו－זמנית， Telegram עלול לנתק את שניהם （AUTH_KEY_DUPLICATED）． צריכים את שניהם？ התחברו ל－TgWitness בנפרד בטלפון או ב－QR．

[קרא את אזהרת הייבוא של ההפעלה](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=he#session-warning)

**עיינו באתר לפני שתתחברו．**

נסו את סביבת העבודה הפיקטיבית ללא חשבון טלגרם．

[פתח את ההדגמה המקוונת →](https://phishdestroy.github.io/TgWitness/demo/?lang=he)

Windows `scripts\Demo.cmd`Linux ／ macOS `sh start.sh --demo`

**פקודות להתקנה מקומית**

שלב 01

### הורד את הקוד המקור．

[הורידו את קובץ ה－ZIP של הקוד המקור](https://github.com/phishdestroy/TgWitness/archive/refs/heads/main.zip) וחילצו אותו， או שיכפלו את המאגר：

```
git clone https://github.com/phishdestroy/TgWitness.git
cd TgWitness
```

נדרש Python 3.11 ומעלה． ב－Windows המפעיל מציע להתקין אותו．

[עיין במהדורות](https://github.com/phishdestroy/TgWitness/releases)

שלב 02

### בחרו כיצד להפעיל．

לחץ פעמיים על `Start.cmd`， או הפעל ב－PowerShell：

```
.\Start.cmd
```

רק סקרנים？ לחצו פעמיים על `scripts\Demo.cmd` כדי לצפות בהדגמה מבודדת． אין צורך להתחבר ל－Telegram．

עם Python 3.11+ ו－`venv`：

```
sh start.sh
```

כדי לפתוח את היומן הבדיוני במקום זאת， הפעל את `sh start.sh --demo`．

כאשר Docker פועל ו－Compose 2.20+ מותקן：

```
docker compose up -d --build --wait
docker compose exec tgwitness cat /data/panel-token.txt
```

הפקודה השנייה מציגה את אסימון הפאנל הפרטי שלך． שמור אותו במחשב שלך．

לאחר ההשקה， יש לפתוח את הכתובת [127.0.0.1:8787](http://127.0.0.1:8787)．

בהתקנה מקוד המקור הטוקן נמצא ב－`data/live/panel-token.txt`． צמד API משלכם מ－[my.telegram.org](https://my.telegram.org) הוא אופציונלי． [מדריך התקנה מלא ↗](https://phishdestroy.github.io/TgWitness/he/docs/reference/quickstart/)

**TgWitness 0.9.1** [מה חדש →](https://phishdestroy.github.io/TgWitness/he/docs/reference/changelog/) · [תכונות ומגבלות ידועות →](https://phishdestroy.github.io/TgWitness/he/docs/reference/features/)

## הוראות ברורות． צעד מועיל להמשך．

[עיינו במדריכים ↗](https://phishdestroy.github.io/TgWitness/he/docs/)

[### מצבים， תרחישים ורמות ראיות ארבעה מצבי איסוף． שמונה רמות אימות． מצאו את תהליך העבודה המתאים למקרה שלכם．](https://phishdestroy.github.io/TgWitness/he/guides/modes.html)

[01 ### חבר חשבון ייבוא באמצעות טלפון， QR וייבוא מפגישות נתמכות．](https://phishdestroy.github.io/TgWitness/he/docs/accounts/)[02 ### בחר פרוקסי רשימות MTProxy ציבוריות או מסלול משלך．](https://phishdestroy.github.io/TgWitness/he/docs/proxies/)[03 ### הגדרת בוט Witness נקודות ביקורת חתומות בערוץ הטלגרם שלכם．](https://phishdestroy.github.io/TgWitness/he/docs/witness/)[04 ### ייצוא ואימות שתפו את ההיסטוריה שנשמרה ובדקו את תקינותה．](https://phishdestroy.github.io/TgWitness/he/docs/exports/)

## עבוד עם הארכיון．

היסטוריה， AI עם מקורות， MCP， OCR ו－webhooks חתומים．

[גלו את תהליך העבודה](https://phishdestroy.github.io/TgWitness/he/docs/archive/)

## לפני שתתחילו．

**האם דף זה מקושר ל－Telegram？**

לא． זה דף סטטי עם דוגמאות מזויפות． האפליקציה רצה על המחשב שלכם ושם אתם מתחברים．

**האם הוא יכול לשחזר הודעות שנמחקו לפני תיעודן？**

לא． הוא שומר את מה שהחשבון שלכם ראה בזמן שרץ． תמונת מצב מאוחרת יותר לא יכולה לשחזר עריכות שהוחמצו או הודעות שנמחקו．

**האם כל היומן שלי מוצפן？**

סשנים ומפתחות כן． הודעות וקבצים לא， השתמשו בהצפנת דיסק． לייצואים אפשר להגדיר סיסמת AES－256．

**האם האתר קשור ל－Telegram？**

לא． זה פרויקט עצמאי ברישיון MIT שבנוי על Telethon． אתם מתחברים עם החשבונות שלכם．

PROJECT NOTICE ／ LICENCE

## Operator incompatibility．

**Taylor Wessing PartG mbB， German core， Hamburg office．**

This statement from the authors of TgWitness adds no condition to the MIT License， and the complete notice includes its source record．

[Read the complete notice](https://phishdestroy.github.io/TgWitness/docs/reference/notice/) [Original text](https://phishdestroy.github.io/TgWitness/NOTICE)

## תבדקו קודם． תתחילו בהגדרה כשתהיו מוכנים．

[הדגמה פתוחה](https://phishdestroy.github.io/TgWitness/demo/?lang=he)[מדריך התקנה](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=he)
