# התקנה, אימות ועדכון

Canonical page: https://phishdestroy.github.io/TgWitness/he/docs/reference/installation/

התקן בפקודה אחת, בדוק חתימות ו-hash, עדכן והסר את ההתקנה.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [תיעוד](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [התחלת עבודה](https://phishdestroy.github.io/TgWitness/he/docs/reference/quickstart/)

![התחלת עבודה](https://phishdestroy.github.io/TgWitness/assets/chapter-start.svg)

[פרויקט](https://github.com/phishdestroy/TgWitness/blob/main/README.md) · [התחלה מהירה](https://phishdestroy.github.io/TgWitness/he/docs/reference/quickstart/) · [פריסה](https://phishdestroy.github.io/TgWitness/he/docs/reference/deployment/)

**בעמוד זה**

- [התקנה בפקודה אחת](https://phishdestroy.github.io/TgWitness/he/docs/reference/installation/#install-with-one-command)
- [המקום שבו הכל פועל](https://phishdestroy.github.io/TgWitness/he/docs/reference/installation/#where-everything-runs)
- [הגדרות חיפוש בטקסט מלא](https://phishdestroy.github.io/TgWitness/he/docs/reference/installation/#full-text-search-settings)
- [גישה משורת הפקודה](https://phishdestroy.github.io/TgWitness/he/docs/reference/installation/#command-line-access)
- [אמת לפני ההפעלה](https://phishdestroy.github.io/TgWitness/he/docs/reference/installation/#verify-before-running)
- [עדכון התקנה קיימת](https://phishdestroy.github.io/TgWitness/he/docs/reference/installation/#update-an-existing-installation)
- [פקודות יומיומיות ב-Ubuntu](https://phishdestroy.github.io/TgWitness/he/docs/reference/installation/#everyday-commands-on-ubuntu)
- [הסר TgWitness](https://phishdestroy.github.io/TgWitness/he/docs/reference/installation/#remove-tgwitness)

## התקנה בפקודה אחת

מתקין מודרך כולל סביבת ריצה פרטית של Python. השתמש באותה כתובת עבור התקנות עתידיות: כל פרסום מעדכן את המתקין, את ה-hash, את החתימות ואת פרטי הבנייה יחד.

**לינוקס / macOS (Bash):**

```
curl -fsSL https://get.destroy.tools/install.sh | bash
```

בשרת Ubuntu, הפעל כמשתמש root כדי להתקין שירות ברקע. במחשב שולחני, הפעל כמשתמש רגיל.

**Windows (PowerShell או שורת הפקודה):**

```
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "irm https://get.destroy.tools/install.ps1 | iex"
```

אין צורך במנהל מערכת ב-Windows. תהליך ה-PowerShell המשני משאיר את הטרמינל פתוח עם התוצאה. Python והתלויות נשארים בהתקנה.

ב-Ubuntu, בחרו ב-"**מחשב זה**", **"קישור HTTPS זמני**" או "**דומיין משלי**". תוכנית ההתקנה מציגה את כתובת הפאנל ומפתח הגישה. לקבלת קישור זמני, פתחו את כתובת ה-HTTPS בדפדפן והזינו את המפתח. בגישה מקומית לשרת מרוחק, השתמשו בהעברת SSH מהמחשב שלכם (`ssh -L 8787:127.0.0.1:8787 user@server`) ופתחו `http://127.0.0.1:8787`. ב-macOS וב-Windows, הפאנל המקומי נפתח בדפדפן שלכם; השאירו את הטרמינל שלו פועל.

היכנסו ל-Telegram בלוח הבקרה ובחרו מה לאסוף. ההתקנה לבדה אינה מפעילה את איסוף הנתונים מ-Telegram.

## המקום שבו הכל פועל

`get.destroy.tools` זהו **Cloudflare Worker שמספק הורדות סטטיות**. אין בו לוח TgWitness, מושב Telegram או מסד נתונים של ראיות משתמשים. הוא אינו מנותב ל-VPS של הפרויקט. היישום פועל על המחשב שבו אתה מבצע את הפקודה.

| התקנה | תוכנית | נתונים |
| --- | --- | --- |
| אובונטו כמשתמש root | `/opt/tgwitness` | שירות מערכת: `/var/lib/tgwitness-<installation ID>`; השתמש `tgwitness paths` לנתיב המדויק. |
| משתמש Linux / macOS | `~/.local/share/tgwitness` | `data/live` במסגרת אותה התקנה. |
| משתמש Windows | `%LOCALAPPDATA%\TgWitness` | `data\live` במסגרת אותה התקנה. |

הגדר `TGWITNESS_INSTALL_DIR` כדי לבחור תיקייה אחרת. הגרסאות המותקנות והנתונים נפרדים. תוכנת ההתקנה אינה מעלה את החשבונות, ההודעות או המפתחות שלכם לאתר ההורדות. בחירת מנהרת Cloudflare מעבירה את תעבורת הפאנל דרך Cloudflare; שימוש בדומיין משלכם מפנה לשרת שלכם.

כל התקנה כוללת את **START-HERE.html** ו-**START-HERE.txt**, עם נתיבים מקומיים, פקודות וקישורים למאגר. הפעל `tgwitness guide` כדי לפתוח את המדריך. ב-Windows, השתמש `& "$env:LOCALAPPDATA\TgWitness\bin\tgwitness.cmd" guide` ב-PowerShell.

## הגדרות חיפוש בטקסט מלא

[חיפוש טקסט מלא](https://phishdestroy.github.io/TgWitness/he/docs/reference/search/) (תצוגה מקדימה) אינו דורש הגדרה. האינדקס שלו נבנה ברקע לאחר עדכון.

| משתנה או פקודה | השפעה |
| --- | --- |
| `TGWITNESS_FULLTEXT=disk` | ברירת מחדל: האינדקס נשמר ב- `search/fulltext.sqlite3` של כל סביבת עבודה |
| `TGWITNESS_FULLTEXT=memory` | אין קובץ אינדקס; האינדקס נבנה מחדש בכל הפעלה |
| `TGWITNESS_FULLTEXT=off` | אין אינדקס; חיפוש לפי טקסט מדויק בלבד |
| `tgwitness index status` | מצב האינדקס של כל סביבת עבודה |
| `tgwitness stop`, `tgwitness index rebuild`, `tgwitness start` | בנו מחדש את כל האינדקסים מתוך היומן החתום |

הבחירה של המנהל ב-**Journal → Filters → Search index** גוברת על המשתנה עבור סביבת העבודה הזו. פקודות מוצאות את ספריית הנתונים של ההתקנה שמפעילה אותן; במקומות אחרים, הוסיפו `--data-dir` את הנתיב מ- `tgwitness paths`. לקבלת מילון אוקראיני מלא (נתוני GPL-3.0), התקן `pymorphy3-dicts-uk` בסביבת Python של ההתקנה.

## גישה דרך שורת הפקודה

[שורת](https://phishdestroy.github.io/TgWitness/he/docs/reference/cli/) [הפקודה](https://phishdestroy.github.io/TgWitness/he/docs/reference/cli/) (תצוגה מקדימה) סורקת את הארכיון בחיפוש אחר סקריפטים וסוכנים.

| משתנה | השפעה |
| --- | --- |
| `TGWITNESS_URL` | כתובת הפאנל עבור `tgwitness search`, `context`, `messages`, `stats` ו- `export`; ברירת מחדל `http://127.0.0.1:8787` כאשר מוגדר אסימון |
| `TGWITNESS_MCP_TOKEN` | ארכיון אסימון החיבור מ-**Integrations → MCP**, המשותף עם לקוחות MCP; `--token-file` קורא אותו מקובץ במקום זאת |
| `TGWITNESS_DATA` | יש לקרוא את ספריית הנתונים ישירות כאשר לא `--data-dir`, כתובת URL או אסימון |

## יש לוודא לפני ההפעלה

הפקודה בת שורה אחת סומכת על HTTPS עבור הסקריפט הראשוני שלה. סקריפט זה בודק את SHA-256 ואת חתימת ה-RSA של הפרויקט על היישום והמגבלות לפני ההתקנה. ניתן גם להוריד ולאמת את הסקריפט הראשוני תחילה.

מפתח הפרסום הציבורי הוא [release-signing.pub](https://github.com/phishdestroy/TgWitness/blob/main/deploy/installer/release-signing.pub). ה-SHA-256 שלו הוא:

```
039d98a658ccda14253e45a00335b4a68d840976d8ec18b8d4355cc7c458447d
```

שמור את טביעת האצבע הזו מגרסה של המאגר שאתה סומך עליה. בדיקת סיכום (checksum) מ אותו שרת הורדות מזהה אי-התאמה; המפתח הציבורי המהימן באופן עצמאי הוא זה שמאמת את חתימת הגרסה.

השתמשו בתיקייה חדשה וריקה להורדות האימות המפורטות להלן.

**Linux / macOS — יש להריץ בספריית הורדות חדשה וריקה** (נדרשים curl ו-OpenSSL):

```
curl -fSLO https://get.destroy.tools/install.sh &&
curl -fSLO https://get.destroy.tools/install.sh.sig &&
curl -fSLO https://get.destroy.tools/release-signing.pub &&
test "$(openssl dgst -sha256 release-signing.pub | awk '{print $NF}')" = \
  '039d98a658ccda14253e45a00335b4a68d840976d8ec18b8d4355cc7c458447d' &&
openssl dgst -sha256 -verify release-signing.pub -signature install.sh.sig install.sh &&
bash install.sh
```

ה `&&` השרשרת נעצרת לפני הביצוע אם ההורדה, טביעת האצבע של המפתח או בדיקת החתימה נכשלות. אם מתבצע פרסום בין הורדת הסקריפט לחתימתו, יש להוריד את שניהם שוב. מתקינים ישנים שומרים על כתובות ה-URL הבלתי משתנות של החבילות שלהם.

**Windows — בדקו את ה-SHA-256 לפני ההפעלה:**

```
Invoke-WebRequest https://get.destroy.tools/install.ps1 -OutFile install.ps1 -UseBasicParsing
Get-FileHash .\install.ps1 -Algorithm SHA256
Invoke-RestMethod https://get.destroy.tools/SHA256SUMS.txt
```

השוו את ה-hash עם `install.ps1` . לבדיקת חתימה עצמאית, השתמשו ב-OpenSSL (למשל, מ-Git Bash) ובטביעת האצבע של המפתח הציבורי המופיעה לעיל:

```
curl -fSLO https://get.destroy.tools/install.ps1 &&
curl -fSLO https://get.destroy.tools/install.ps1.sig &&
curl -fSLO https://get.destroy.tools/release-signing.pub &&
test "$(openssl dgst -sha256 release-signing.pub | awk '{print $NF}')" = \
  '039d98a658ccda14253e45a00335b4a68d840976d8ec18b8d4355cc7c458447d' &&
openssl dgst -sha256 -verify release-signing.pub -signature install.ps1.sig install.ps1 &&
powershell.exe -NoProfile -ExecutionPolicy Bypass -File install.ps1
```

מערכת ההפעלה Windows עצמה מאמתת את חתימות החבילות באמצעות .NET ואינה זקוקה ל-OpenSSL. מדובר בחתימות RSA-3072 / SHA-256 מנותקות, ולא ב-Authenticode. [המניפסט](https://get.destroy.tools/manifest.json) מתעד את גרסת התוכנה, ה-commit המדויק ב-Git, מזהה הגרסה הבלתי משתנה (immutable release ID) ואת ה-SHA-256 של כל ארטפקט. הדף מקשר למקור המתאים. גם למניפסט ולרשימת בדיקת הסיכום יש חתימות מנותקות (`manifest.json.sig` ו- `SHA256SUMS.txt.sig`).

## עדכון התקנה קיימת

**פרסום חדש מעדכן את אתר ההורדות; תוכניות מותקנות מתעדכנות כאשר מפעילים את תוכנית ההתקנה שוב.** אין מתקן עדכונים אוטומטי או הפעלה מחדש אוטומטית של אוסף פועל. ערוץ ההתקנה הנוכחי הוא ערוץ **תצוגה מקדימה**; הוא עוקב אחר גרסאות שפורסמו ונבדקו מ `main`, שה-commit שלהן עשוי להיות חדש יותר מהמהדורה האחרונה המספרית ב-GitHub. גרסת הדף נובעת `pyproject.toml`; ה-commit ומזהה ה-build שלה מבחינים בין עדכונים בתוך אותה גרסת תצוגה מקדימה.

הפרסום מתבצע באופן אוטומטי לאחר שה-commit הספציפי עובר את בדיקות היישום וה אבטחה, והחבילה החתומה עוברת את בדיקות השירות של Ubuntu ואת בדיקות ההתקנה של Windows PowerShell. בזמן שהבדיקות פועלות, או אם הן נכשלות, אותן פקודות ממשיכות להתקין את ה-build שנבדק קודם לכן. מניפסט ה-build מציג איזה commit זמין כרגע; מספר הגרסה לבדו עשוי להישאר זהה בין עדכוני התצוגה המקדימה.

השתמש באותה תיקיית התקנה ובאותו משתמש מערכת הפעלה כמו קודם. גבה את ספריית הנתונים המלאה כשהאיסוף מופסק; `tgwitness paths` זה מזהה אותה. ייצוא חתום אינו גיבוי התקנה מלא.

**התקנת root ב-Ubuntu בכתובת `/opt/tgwitness`:**

```
curl -fsSL https://get.destroy.tools/install.sh | TGWITNESS_INSTALL_DIR=/opt/tgwitness bash -s -- --no-start
```

לאחר התקנה מוצלחת:

```
/opt/tgwitness/bin/tgwitness restart
/opt/tgwitness/bin/tgwitness status
/opt/tgwitness/bin/tgwitness open
```

להתקנה על ידי משתמש לינוקס/macOS, השתמש ב `TGWITNESS_INSTALL_DIR` או את ברירת המחדל והפעילו שוב את פקודת ההתקנה הראשונה. סגרו את הפאנל הקדמי לפני העדכון והפעילו אותו מחדש לאחר מכן. עבור שירות Linux שהוגדר , הפעילו את `tgwitness restart` הפקודה שלו.

**Windows:** סגור את החלונית הפועלת, הפעל שוב את פקודת ההתקנה של Windows, ואז פתח `bin\tgwitness.cmd` באותה התקנה. תוכנית ההתקנה שומרת נתונים, הפעלות, הגדרות גישה ומפתחות חתימה. היא מחליפה את תוכנת ההפעלה רק לאחר שהסביבה החדשה עוברת את הבדיקות; התקנה שנכשלה משאירה את תוכנת ההפעלה הקודמת במקומה. שמרו את הגיבוי מלפני השדרוג למקרה של שינויים בפורמט האחסון.

## פקודות יומיומיות ב-Ubuntu

| פקודה | תוצאה |
| --- | --- |
| `tgwitness open` | כתובת ה-URL הנוכחית של הפאנל ומפתח הגישה. |
| `tgwitness paths` | נתיבי תוכנה, נתונים ומדריכים מדויקים. |
| `tgwitness guide --print` | הוראות הפעלה במצב לא מקוון. |
| `tgwitness status` / `tgwitness logs` | זמינות / יומני שירות. |
| `tgwitness stop` / `tgwitness start` | עצור/המשך את השירות; שמור את הנתונים. |
| `tgwitness token rotate` | החלף את מפתח המנהל וסיים את הפעלות הדפדפן. |
| `tgwitness tunnel off` | השבת את המנהרה המהירה הציבורית; השאר את הפאנל המקומי. |
| `tgwitness tunnel on` / `tgwitness tunnel restart` | יצירת קישור למנהרה מהירה / החלפת כתובתה. |

ראו ["גישה"](https://phishdestroy.github.io/TgWitness/he/docs/reference/access/) לקבלת מידע על אסימוני עמיתים, הפעלות והגבלות IP, וכן "[פרסום מתקין"](https://github.com/phishdestroy/TgWitness/blob/main/deploy/installer/README.md#automatic-publication-from-github) לקבלת מידע על תהליך העבודה של שחרור גרסאות מ-GitHub ל-Cloudflare.

## הסר TgWitness

אין תוכנת הסרה: יש לעצור את הפאנל ולמחוק את התיקיות שלו. מחיקת תיקיית הנתונים ממחיקה לצמיתות יומנים, מפתחות חתימה, הפעלות טלגרם וקבצים שנשמרו. לפני כן:

1. ייצא את מה שאתה צריך (**ייצוא → הורד ZIP חתום**) ושמור את טביעת האצבע של מפתח החתימה ואת נקודות הבקרה מחוץ למחשב זה. כדי לשמור את סביבת העבודה עצמה, העתק את כל תיקיית הנתונים לאחר הפסקת האיסוף.
2. מחק שרתים שנוצרו תחת "**Extras" → "Server 24/7"** מתוך "**Your servers"** או באמצעות `python -m tgwitness.cloud destroy`; הספק מחייב עבורם עד למחיקתם.
3. יש לסיים את הפעלת כל חשבון ב-Telegram תחת **"הגדרות" → "מכשירים"**. מחיקת הקבצים אינה מבטלת את ההתחברות מצד Telegram.

**התקנה ברמת השורש ב-Ubuntu.** שימו לב לתיקיית הנתונים, עצרו את השירות, ולאחר מכן הסירו את השירות, את התיקיות ואת קיצור הדרך:

```
/opt/tgwitness/bin/tgwitness paths
/opt/tgwitness/bin/tgwitness stop
systemctl list-unit-files 'tgwitness-*'
systemctl disable tgwitness-<ID>
rm /etc/systemd/system/tgwitness-<ID>.service
systemctl daemon-reload
rm -rf /opt/tgwitness /var/lib/tgwitness-<ID> /usr/local/bin/tgwitness
```

**התקנה למשתמשי לינוקס או macOS.** סגור את החלונית. שירות משתמש לינוקס שהוגדר מופסק באמצעות `systemctl --user disable --now tgwitness-<ID>`; היחידה שלו נמצאת ב- `~/.config/systemd/user/`. לאחר מכן, מחקו `~/.local/share/tgwitness` (או `TGWITNESS_INSTALL_DIR`) ואת `~/.local/bin/tgwitness` קיצור הדרך.

**Windows.** סגור את החלונית ומחק `%LOCALAPPDATA%\TgWitness` (או את `TGWITNESS_INSTALL_DIR`). תוכנית ההתקנה אינה מוסיפה שירות, משימה מתוזמנת או קיצור דרך.
