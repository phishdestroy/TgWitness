# התחלה מהירה

Canonical page: https://phishdestroy.github.io/TgWitness/he/docs/reference/quickstart/

כל הדרכים להתקנה והפעלה של TgWitness: חבילת Windows, Python, Docker והדגמה סינתטית, כולל בדיקות ראשוניות.

**אנגלית** · [Русский](https://github.com/phishdestroy/TgWitness/blob/main/docs/ru/QUICKSTART.md) · [אוקראינית](https://github.com/phishdestroy/TgWitness/blob/main/docs/uk/QUICKSTART.md) · [Español](https://github.com/phishdestroy/TgWitness/blob/main/docs/es/QUICKSTART.md) · [פורטוגזית (ברזיל)](https://github.com/phishdestroy/TgWitness/blob/main/docs/pt/QUICKSTART.md) · [Türkçe](https://github.com/phishdestroy/TgWitness/blob/main/docs/tr/QUICKSTART.md) · [العربية](https://github.com/phishdestroy/TgWitness/blob/main/docs/ar/QUICKSTART.md) · [فارسی](https://github.com/phishdestroy/TgWitness/blob/main/docs/fa/QUICKSTART.md) · [אורדו](https://github.com/phishdestroy/TgWitness/blob/main/docs/ur/QUICKSTART.md) · [हिन्दी](https://github.com/phishdestroy/TgWitness/blob/main/docs/hi/QUICKSTART.md) · [באסהה אינדונזיה](https://github.com/phishdestroy/TgWitness/blob/main/docs/id/QUICKSTART.md) · [Tiếng Việt](https://github.com/phishdestroy/TgWitness/blob/main/docs/vi/QUICKSTART.md) · [סינית פשוטה](https://github.com/phishdestroy/TgWitness/blob/main/docs/zh/QUICKSTART.md)

TgWitness הוא יישום עצמאי לניטור קבוצות וערוצים ב-Telegram שאליהם יש לחשבונותיכם גישה. הוא פועל באופן מקומי עם ספריית נתונים משלו.

זו הפעם הראשונה שאתם מבקרים [באתר? התנסו בהדגמה](https://phishdestroy.github.io/TgWitness/he/docs/reference/quickstart/#explore-the-interface) לפני שתחברו חשבון. [בחרו במדריך](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) בנושא פרוקסי, עדים, ייצוא או הגדרת שרת.

## התקנה והפעלה

[איסוף באמצעות GitHub Actions (גרסה מקדימה)](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md)

בחרו בשיטה אחת. קבצים להורדה ניידת יהיו זמינים לאחר פרסום גרסת השחרור:

| מארח | אין צורך בהתקנה | מהמקור: Python 3.11+ | Docker: Engine/Desktop עם Compose 2.20+ |
| --- | --- | --- | --- |
| Windows | חלץ את `TgWitness-<version>-windows-amd64-portable.zip` מ-GitHub Releases, לחץ פעמיים על `TgWitness.cmd` | לחץ פעמיים על `Start.cmd` | לחץ פעמיים על `scripts\Docker.cmd` |
| Linux / macOS | — | `sh start.sh` | `sh scripts/docker-start.sh` |

לשיטות ההרצה מקוד המקור, [הורידו וחלצו את ענף ה-`main` הנוכחי](https://github.com/phishdestroy/TgWitness/archive/refs/heads/main.zip) או שכפלו (clone) את המאגר:

```
git clone https://github.com/phishdestroy/TgWitness.git
cd TgWitness
```

הקובץ `Start.cmd` מציע להתקין את Python 3.12 עבור משתמש ה-Windows שלכם אם לא נמצאה התקנת Python מתאימה (באמצעות winget, או תוכנית ההתקנה החתומה מ-python.org). הקובץ `start.sh` מדפיס את פקודת ההתקנה המדויקת עבור הפצת ה-Linux או ה-macOS שלכם אם Python חסר. ההפעלה הראשונה מקוד המקור יוצרת סביבת `.venv` ומתקינה את התלויות באופן אוטומטי.

Docker בונה את היישום ומפעיל אותו ברקע; אין צורך ב-Python במחשב המארח. הפקודות `scripts\Docker.cmd` ו-`scripts/docker-start.sh` מדפיסות את כתובת הפאנל ואת האסימון כאשר הקונטיינר פועל כראוי. פקודות ה-Docker המקבילות בכל מחשב מארח נתמך הן:

```
docker compose up -d --build --wait
docker compose exec tgwitness cat /data/panel-token.txt
```

פתחו את **http://127.0.0.1:8787**. השתמשו באסימון שהודפס על ידי עוזר ה-Docker או בפקודת ה-Docker השנייה, או קראו את **הקובץ data/live/panel-token.txt** להתקנה ניידת או מהמקור. המשיכו ב" **חבר את Telegram**" להלן. התקנות מקוריות והתקנות Docker משתמשות באחסון נפרד; הפעלת Docker אינה מייבאת יומן מקורי קיים.

במקרה של שרת, [הפריסה](https://phishdestroy.github.io/TgWitness/he/docs/reference/deployment/) כוללת HTTPS אוטומטי, הפעלה מחדש, תמונות שפורסמו, עדכונים וגיבויים.

## גלו את הממשק

1. הפעל **את הקובץ TgWitness-Demo.cmd** בחבילה הניידת, את הקובץ **scripts\Demo.cmd** בתיקיית המקור של Windows, או את הפקודה `sh start.sh --demo` ב-Linux/macOS. הפעלה מהמקור יוצרת תחילה את הקובץ `.venv` ומתקינה את התלויות.
2. **http://127.0.0.1:8787** פתוח.
3. הדגמה המקומית פותחת את יומן הדוגמה באופן אוטומטי. אין צורך בהעתקת אסימון (token) לצורך גישה מקומית ישירה.

ההודעות בהדגמה הן פיקטיביות. מצב ההדגמה אינו מאפשר חיבור לחשבון Telegram אמיתי.

## התחבר ל-Telegram

> [!אזהרה] **אל תשתמשו בשום דבר שאינכם יכולים להרשות לעצמכם לאבד.** אנו ממליצים בחום להימנע מחיבור חשבונות אישיים או בעלי ערך, וכן מיצירת מזהה API / hash בחשבון שחשוב לכם. Telegram חוסמת חשבונות באופן בלתי צפוי ולעתים קרובות לצמיתות, ללא תלות בלקוח. הפעלה חלקה של הבדיקה תלויה ב-Telegram, לא ב-TgWitness, ואינה מבטיחה דבר להמשך.

1. אם ההדגמה המקורית פועלת, עצרו אותה והפעילו **את Start.cmd** או `sh start.sh`. אחרת, המשיכו להפעיל את ההתקנה החיה שהושקה לעיל.
2. השתמש באסימון הפאנל המתאים לשיטת ההתקנה שלך כדי לפתוח את הפאנל.
3. אם אתם זקוקים לפרוקסי, שמרו אותו תחת **חשבון → הגדרות → הגדרות חיבור → שינוי נתיב החיבור**.
4. ב**"חשבון**", הזן את מספר הטלפון שלך ולחץ על **"המשך**", בחר **"קוד QR" → "הצג קוד QR**", או בחר קבצים ולחץ על **"חבר חשבון"**. **מזהה API + Hash** הם אופציונליים: סביבת העבודה משתמשת בזוג השמור או המיובא שלה, או בזוג פעיל מהמאגר המובנה. כדי להשתמש באפליקציה משלך, הדבק זוג אחד של `API ID:API Hash` בשדה "מזהה API". לקבלת מפתח אישור מלא, בחר "**מפתח אישור**", הדבק את כל 512 התווים ההקסדצימליים ובחר את מזהה ה-DC שסופק. מזהה המשתמש הוא אופציונלי ומסומן אם הוזן.
5. השלם את שיטת הכניסה שבחרת: טלפון/קוד/2FA, אישור מאפליקציית Telegram מחוברת עבור QR, או ייבוא של הפעלה מאושרת נתמכת.
6. בדקו את מזהה החשבון המוצג. **מקורות** פתוחים: הצ'אטים שלכם נטענים אוטומטית; הוסיפו את הקבוצות שלכם.
7. תחת "**בחר אילו שינויים לשמור**", בחר קטגוריות אירועים או את ההגדרה המוגדרת מראש " **הודעות, עריכות ומחיקות**", ולאחר מכן שמור את הגדרות הניטור.
8. בחר את הגדרות הקבצים המצורפים בנפרד, ולאחר מכן לחץ על "**התחל תצפית"**.

פרטי הזדהות ה-API מזהים את היישום שלכם; הם אינם מאשרים חשבון כשלעצמם. קבוצות פרטיות אינן זקוקות לשם משתמש ציבורי, אך על חשבונכם להיות בעל גישה.

עבור חשבונות קיימים, עיינו ב[פורמטים של חשבונות וסשנים](https://phishdestroy.github.io/TgWitness/he/docs/reference/accounts/): הפאנל מקבל Telethon StringSession, קובצי SQLite של Telethon/Pyrogram, קובץ ZIP של TData לחשבון יחיד וקובץ JSON נתמך של חשבון. בחרו סשן ואת קובץ ה-JSON הנלווה שלו יחד, ולחצו על **חבר חשבון**. התחברות באמצעות QR זמינה גם היא עם אותן הגדרות API אופציונליות. סשנים של TDLib, סשנים של בוטים ורשימות מלאי חשבונות בפורמט CSV/JSON אינם נתמכים.

עבור מספר חשבונות, השתמשו ב-**חשבונות → ייבוא חשבונות** ובחרו את קובצי הסשן הנתמכים שלהם. קובצי JSON נלווים משויכים לפי שם הקובץ הבסיסי (basename); כל חשבון מיובא מקבל סביבת עבודה משלו. עיינו ב[ייבוא מרוכז וקבוצות חשבונות](https://phishdestroy.github.io/TgWitness/he/docs/reference/accounts/#bulk-import-and-account-groups).

כדי להוסיף חשבון נוסף, לחץ על **+** ליד בורר החשבונות או פתח **חשבון → הגדרות → הגדרות חיבור → סביבות עבודה**, או השתמש ב**"חשבונות"**. לסביבות העבודה יש הפעלות, יומנים, מפתחות, מקורות ותורים נפרדים. מעבר בין תצוגות משאיר את שאר האספנים פועלים. לא ניתן להקצות את אותו חשבון טלגרם לשתי סביבות עבודה בהתקנה זו. אין מספר קבוע של סביבות עבודה; הן חולקות תהליך אחד, ולכן הקיבולת תלויה במחשב.

אסימון הפאנל החי מגן על הגישה לאישורי ה-Telegram ולחומר השמור שלכם; הוא נפרד מפרטי הזיהוי של ה-API של Telegram. רק הדגמה מקומית שהופעלה במפורש, והגישה אליה היא ישירה, זוכה לרישום אוטומטי. הדגמה מרחוק או באמצעות פרוקסי עדיין משתמשת ב- `data/demo/panel-token.txt`.

## סקירה וייצוא

- **יומן:** חיפוש וסינון תצפיות לפי מקור וסוג אירוע.
- בחר אירוע כדי לבחון את התיעוד המקורי שלו, את מקורו ואת הגרסאות השמורות.
- פרטי העריכה מציגים את התוכן הזמין לפני ואחרי העריכה. פרטי המחיקה מציגים את התוכן האחרון שנלכד, אם קיים; גורם לא ידוע נותר לא ידוע.
- **ייצוא:** ZIP חתום, JSONL, CSV ו-HTML לא מקוון.
- **ייצוא צ'אט מלא** (מקורות → ייצוא צ'אט מלא): הורדת כל ההיסטוריה הגלויה של צ'אט אחד כחבילה חתומה ב-`chat.json` (בסגנון ייצוא טלגרם) ו-`chat.html` קריא. צ'אטים פרטיים פועלים כאשר החשבון הוא חבר. זוהי תמונת מצב עדכנית, ולא שחזור של הודעות שנמחקו או נערכו בעבר. אמתו עותק באמצעות `python verify.py chat-export.zip --fingerprint TRUSTED_SHA256`.
- **נקודת ביקורת:** יש לשמור על גבולות היומן החתום מחוץ לאספן.
- **הורדת קבלה חתומה על הפעלה:** שמירת תיעוד התוכנית/הגרסה של האספן.
- **הכנת בקשה לחותמת זמן:** הכן בקשה לא מקוונת לרשות חותמת זמן; פעל לפי ההוראות [ב-TIMESTAMP.md](https://phishdestroy.github.io/TgWitness/he/docs/reference/timestamp/) כדי לקבל את התשובה ולאמת אותה.
- **אימות היומן:** בדקו את חתימות האירועים וקישורי השרשרת. ייצוא בפורמט ZIP בודק גם קבצי מדיה.

דפדפנים נתמכים שומרים ייצוא בנפח גדול ישירות לקובץ נבחר. דפדפנים אחרים מאחסנים במאגר זמני לכל היותר 128 MiB. בזמן שהשרת פועל, ממשק ה-CLI הזורם תומך בהורדות גדולות יותר ללא אחסון כל התגובה במאגר הזמני:

```
python -m tgwitness.download --token-file data/live/panel-token.txt --out evidence.zip
```

לסביבת עבודה נוספת, הוסף את `--profile ID` באמצעות **'ייצוא' → 'מזהה סביבת עבודה**'. לשרת מרוחק, הוסף את `--url https://your-server`. מגבלת ההעברה המוגדרת כברירת מחדל היא 5 GiB; `--max-mib` משנה אותו. לתוכן ZIP חתום יש מגבלת אימות נפרדת של 4 GiB ללא דחיסה כברירת מחדל (**Parameters** מעלה אותה; אמת ארכיונים כאלה באמצעות `verify.py --max-gib N`). אמת את הארכיון באמצעות עותק מהימן של תוכנת האימות ו טביעת אצבע/נקודת ביקורת של המפתח, שנשמרו באופן עצמאי.

## בדוק את ההתקנה

```
python start.py --setup-only
python start.py --check
python start.py --check --json
```

`--check` בודק תלות מקומיות, תמיכה בחתימה, אחסון, תצורת מפתחות ו כתובת ההאזנה. הוא אינו מתקין דבר ואינו מתחבר ל-Telegram. יציאה עמוסה עשויה להעיד על כך שמקרה נוסף פועל. השתמש ב-`--port` אחר או הפסק אותו תחילה.

תוכנת ההפעלה מותקנת ב-`.venv`. פקודות עזר של `python -m tgwitness...` חייבות להשתמש ב-`.venv\Scripts\python.exe` ב-Windows או ב-`.venv/bin/python` ב-Linux/macOS, אלא אם כן סביבה זו כבר מופעלת.

## פעילויות, הגנה ותפעול

קובץ Telethon SQLite סגור ועקבי (`.session`) ניתן להמרה באופן מקומי באמצעות `python -m tgwitness.sessions account.session --out account.tgwitness-session`, ולאחר מכן לטעון אותו ב-Account. ייבוא קבצים ישיר וכניסה באמצעות QR זמינים גם הם. ראו את [הקובץ CONNECTION-SECURITY.md](https://phishdestroy.github.io/TgWitness/he/docs/reference/connection/) לקבלת פורמטים לכניסה, SOCKS5, HTTP CONNECT, MTProxy ומפתחות ראשיים חיצוניים.

**השהיית התצפית** מפסיקה את האיסוף. **נעילה** רק סוגרת את הגישה לדפדפן. סגירת לשונית משאירה את תהליך האיסוף פועל. עצירת התהליך מפסיקה את האיסוף; תמונת מצב של ההיסטוריה אינה יכולה לשחזר את כל העריכות או המחיקות שהוחמצו. ראו [כיצד פועל האיסוף](https://phishdestroy.github.io/TgWitness/he/docs/reference/collection/) בהקשר של מדיניות אירועים, תורי קבצים מצורפים, בידוד חשבונות והתנהגות בעת הפעלה מחדש.

הפעלות וסודות מוצפנים. תוכן ההודעות, קבצי המדיה והייצואים דורשים דיסק או אמצעי אחסון מוצפן. החתימות מאמתות את תקינות הנתונים ביחס למפתח מהימן; הן אינן מאמתות את מקורן ב-Telegram ואינן מונעות זיוף על ידי מפעיל השולט במאגר ובמפתח שלו.

קראו [את הקובץ OPERATIONS.md](https://phishdestroy.github.io/TgWitness/he/docs/reference/operations/) בנושא גיבוי/שחזור, [את הקובץ DEPLOYMENT.md](https://phishdestroy.github.io/TgWitness/he/docs/reference/deployment/) בנושא אירוח, ואת [deploy/](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md) לדוגמאות לשימוש בשירות. הלוח המותקן כולל גם מדריך התקנה במצב לא מקוון בכתובת `/guide.html`.

האימות בפועל והמגבלות הקיימות מתועדים בקבצים [VERIFICATION.md](https://phishdestroy.github.io/TgWitness/he/docs/reference/verification/) [ו-READINESS.md](https://github.com/phishdestroy/TgWitness/blob/main/docs/internal/READINESS.md).
