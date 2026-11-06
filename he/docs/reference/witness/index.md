# Telegram · עד עצמאי

Canonical page: https://phishdestroy.github.io/TgWitness/he/docs/reference/witness/

הפעל את Witness עם מפתח ובוט משלו, פרסם נקודות ביקורת חתומות בערוץ ובדוק את הייצוא מולן.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [תיעוד](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [ראיות ואימות](https://phishdestroy.github.io/TgWitness/he/docs/reference/evidence/)

![ראיות ואימות](https://phishdestroy.github.io/TgWitness/assets/chapter-evidence.svg)

[ייצוא ואימות](https://phishdestroy.github.io/TgWitness/he/docs/reference/evidence/) · [אמינות גבוהה](https://phishdestroy.github.io/TgWitness/he/docs/reference/high-assurance/) · [מדריך לפאנלים](https://phishdestroy.github.io/TgWitness/he/docs/reference/panel/#extras)

עדה שומרת נקודות ביקורת חתומות בנפרד מהאוסף. היא בודקת את חתימת האוסף ואת רציפות היומן, חותמת על התוצאה באמצעות המפתח שלה, ו מפרסמת אותה בערוץ Telegram. יש להריץ אותה בשרת נפרד עם גישה לקריאה בלבד ל נקודת הקצה של העדה של האוסף.

תרשים זרימה · אספן → עד (נקודת ביקורת חתומה: מספר הרשומות + חתימת ה-hash של הכותרת); עד → יומן Witness, מפתח פרטי; עד → ערוץ טלגרם (הודעה חתומה באמצעות הבוט של האתר); קובץ ZIP של הראיות → verify.py; יומן Witness, מפתח פרטי → verify.py; ערוץ טלגרם → verify.py (ייצוא מ-Telegram Desktop או דף "t.me/s") · אספן · עד · יומן Witness, מפתח פרטי · ערוץ טלגרם · קובץ ZIP של הראיות · verify.py · נקודת ביקורת חתומה: מספר · הרשומות + חתימת ה-hash של · הכותרת · הודעה חתומה באמצעות הבוט של · האתר · ייצוא מ-Telegram Desktop או · דף "t.me/s"

**תרשים כטקסט**

1. אספן → עד (נקודת ביקורת חתומה: מספר הרשומות + חתימת ה-hash של הכותרת)
2. עד → יומן Witness, מפתח פרטי
3. עד → ערוץ טלגרם (הודעה חתומה באמצעות הבוט של האתר)
4. קובץ ZIP של הראיות → verify.py
5. יומן Witness, מפתח פרטי → verify.py
6. ערוץ טלגרם → verify.py (ייצוא מ-Telegram Desktop או דף "t.me/s")

**בעמוד זה**

- [מה ה-Witness מקבל, ומה הוא לא מקבל](https://phishdestroy.github.io/TgWitness/he/docs/reference/witness/#what-the-witness-gets-and-what-it-does-not)
- [מה הוא בודק ומתעד](https://phishdestroy.github.io/TgWitness/he/docs/reference/witness/#what-it-checks-and-records)
- [הפעל עד](https://phishdestroy.github.io/TgWitness/he/docs/reference/witness/#run-a-witness)
- [דף הוכחה ציבורי למספר סביבות עבודה](https://phishdestroy.github.io/TgWitness/he/docs/reference/witness/#public-proof-page-for-several-workspaces)
- [אמת](https://phishdestroy.github.io/TgWitness/he/docs/reference/witness/#verify)

## מה ה-TgWitness מספק, ומה הוא אינו מספק

| ל-TgWitness יש | העד מעולם לא |
| --- | --- |
| **אסימון עדות** לקריאה בלבד עבור סביבת עבודה אחת | פרטי ההתחברות של האספן ל-Telegram או פרטי הזיהוי ל-API |
| מפתח Ed25519 ויומן משלו | כספת האספן, מפתח החתימה או אסימון הפאנל |
| אסימון בוט טלגרם משלו | תוכן ההודעה: בראש ההודעה מופיע מספר הרשומות ו-hash |

האסימון נוצר **ב-Extras → Independent witness**, מוצג פעם אחת ונשמר רק כ- SHA-256. הוא פותח נקודת קצה אחת בלבד, `GET /api/witness/head`, המחזירה נקודת ביקורת חתומה טרייה, בנוסף למונים חתומים של אוספים נטולי תוכן ולמצב תפעולי. היא אינה יכולה לפתוח את הלוח, לקרוא תוכן הודעות או לשנות הגדרות, ו אסימון הלוח אינו מתקבל שם. ניתן לבטל אסימון באותו דף. האספן מתעד מתי מפתח עד חדש מתחיל לבדוק (`witness.seen`) ומציג את הבדיקה האחרונה לכל אסימון; עד שלא ביצע בדיקה תוך 2.5 מרווחים מסומן כאיחור.

עדים חדשים שולחים אתגר אקראי בכל סקר; הצהרת הלכידה חוזרת עליו תחת חתימת האספן. מונים קשורים לנקודת הבדיקה המדויקת ונכללים בפוסטים חתומים של העדים. כותרות ישנות ממשיכות להתקבל על ידי העד העצמאי. צמיחת היומן כשלעצמה לעולם אינה נספרת כהודעה חדשה.

## מה הוא בודק ומתעד

בכל פרק זמן (10 דקות כברירת מחדל) ה-Witness:

1. מביא את הראש עצמו (האספן אינו יכול לדחוף או לדלג עליו);
2. מאמת את חתימת האספן, את מפתח האספן המוצמד (`--collector-fingerprint`, או המפתח הראשון שנראה), ספירה שאינה פוחתת וראש שלא השתנה בספירה שלא השתנתה. הוכחות הכללה ועקביות של מרקל מאמתות כי יומן הולך וגדל מרחיב את נקודת הבדיקה שנשמרה. לאחר שהוכחות הרציפות שימשו, הסרתן נדחית;
3. מוסיף רשומה חתומה ליומן שלו: `witness.anchor` עם הסטטוס `ok`, `key_changed`, `rollback` (פחות רשומות מבעבר), `fork` (אותו אורך, כותרת שונה ) או `invalid` (התשובה נכשלה באימות), או `witness.no_response` כאשר האספן לא ענה;
4. מפרסם את התוצאה בערוץ, חתומה, כולל "אין תשובה" כל עוד ה-Witness פועל ומסוגל לגשת ל-Bot API. מזהה הפרסום נרשם (`witness.posted`), כמו גם פרסום שנכשל (`witness.post_failed`).

פוסט נראה כך; השורה האחרונה מכילה את ההצהרה החתומה:

```
TgWitness witness #42 · journal head
Collector 3fa9c2d1e0b4a7f6: 18234 records
Head 9b1f…c07e
2026-10-28T19:40:00.123+00:00
TGW1.eyJhdCI6…<statement>.<signature>
```

## הפעל את Witness

נדרש בוט של טלגרם (ניתן ליצור אחד באמצעות @BotFather), ערוץ שבו הבוט משמש כמנהל, וכתובת האספן הנגישה לעד — באמצעות HTTPS מחוץ לרשת פרטית (ראו את פרופיל ה-HTTPS בפרק [הפריסה](https://phishdestroy.github.io/TgWitness/he/docs/reference/deployment/)).

פתחו **את 'תוספות' → 'עד עצמאי' → 'הגדר'** בלוח הבקרה. שלושת השלבים כוללים גישה לקריאה בלבד, הערוץ והמרווח שלכם, ולאחר מכן הפעלת העד. מדיניות הפרסום, פרוקסי HTTP/SOCKS5 אופציונלי וכתובת API מותאמת אישית לבוט נמצאים תחת **'הגדרות מתקדמות**'. הטופס מוריד `witness.json` עם מפתח האספן של סביבת העבודה הזו מוצמד אליו. הורידו את האסימון לקריאה בלבד שנוצר זה עתה באמצעות **'שמור קובץ גישה** כ-' `witness-token.txt`; שמור אותו ואת `bot-token.txt`נוצר במארח העד לצד קובץ ה-JSON הזה. האספן לעולם אינו מקבל את אסימון הבוט. ההורדה אינה מפעילה שירות ואינה מפרסמת הודעה. אף עד של פרויקט מאוחסן אינו נרשם באופן מרומז.

```
python -m tgwitness.witness run --config witness.json --check-config
python -m tgwitness.witness run --config witness.json
python -m tgwitness.witness fingerprint --config witness.json
```

הפקודה הראשונה בודקת קבצי תצורה וקבצים סודיים ללא בקשות רשת או יצירת מפתח. הנתיבים ב-JSON הם יחסית לאותו קובץ; נתיבי CLI/סביבה הם יחסית לספריית העבודה. שמור את טביעת האצבע של ה-witness מחוץ למארח שלו. מחוון הסקר האחרון של האספן מאשר בקשה בלבד; הפרסום מדווח על ידי Proof או נבדק ביומן ה-witness ובערוץ.

אם הפאנל נמצא מאחורי מנהרת SSH, יש לחשוף רק את נקודת הקצה המוגדרת של Witness על שם מארח HTTPS נפרד, כפי שמוצג [בדוגמה זו של Caddy](https://github.com/phishdestroy/TgWitness/blob/main/deploy/Caddyfile.witness.example). סביבת העבודה המוגדרת כברירת מחדל משתמשת ב-`https://witness.example.org`, וסביבות עבודה אחרות משתמשות ב- `https://witness.example.org/profiles/ID`. עדיין נדרשים אסימונים; הפאנל ו נתיבי ה-API האחרים שלו אינם מועברים על ידי אותו מארח וירטואלי.

בחרו ב-`all` לקבלת נקודות ביקורת המתפרסמות באופן קבוע. מרווח של חמש דקות פירושו כ-288 פרסומים לכל סביבת עבודה ביום. `changes`/`problems` משאירים בכוונה חלק מהבדיקות ללא פרסום. MTProxy מיועד ללקוח Telegram של האספן. סקרי HTTP של Witness ו-HTTPS של Telegram Bot API משתמשים במסלול ישיר/HTTP/SOCKS5 משלהם ([Bot API](https://core.telegram.org/bots/api)).

**ליד האספן, עם Docker** (אותו מארח — תהליך ומפתח עצמאיים, אך אותו מפעיל): הזן את הערכים ב-`.env` והפעל את הפרופיל.

```
TGWITNESS_WITNESS_TOKEN=tgww_...
TGWITNESS_WITNESS_BOT_TOKEN=123456:ABC...
TGWITNESS_WITNESS_CHANNEL=@your_witness_channel
# another workspace: TGWITNESS_WITNESS_COLLECTOR=http://tgwitness:8787/profiles/<workspace ID>

docker compose --profile witness up -d
docker compose logs witness     # prints the witness key fingerprint
```

בשימוש בתמונה שפורסמה יש לציין את `docker compose --project-directory . -f deploy/compose/compose.image.yaml --profile witness up -d`.

**בשרת של מישהו אחר** (עד עצמאי אמיתי): העתיקו את המאגר לשם, הגדירו `TGWITNESS_WITNESS_COLLECTOR=https://your-collector.example.org` בתוספת שלושת הערכים שלעיל ב-`.env`, ואז

```
docker compose --project-directory . -f deploy/compose/compose.witness.yaml up -d
```

או ללא Docker:

```
python -m tgwitness.witness run --collector https://your-collector.example.org \
    --token-file witness-token.txt --bot-token-file bot-token.txt --channel @your_witness_channel
```

### פרסם ב-Discord

עד יכול לפרסם בערוץ Discord במקום ב-Telegram. ב-Discord, פתחו **"ערוך ערוץ" → "אינטגרציות" → "Webhooks**", צרו Webhook והעתיקו את כתובת ה-URL שלו. בלוח הבקרה, בחרו **"Webhook של Discord · הערוץ שלכם**" בשלב 2. במארח העד, שמרו את כתובת ה-URL כ `discord-webhook.txt` ליד `witness.json`; הוא לעולם לא מגיע אל האספן.

```
python -m tgwitness.witness run --collector https://your-collector.example.org \
    --token-file witness-token.txt --discord-webhook-file discord-webhook.txt
```

ל-Witness יש מפרסם אחד: ערוץ Telegram או Webhook של Discord, אך לא שניהם. פוסטים נושאים את אותה הצהרה חתומה ואינם יכולים לשלוח התראות לאף אחד. פוסט שאורכו עולה על המגבלה של Discord (2,000 תווים) מוחלף בשורה קצרה עם הצ'ק המלא המצורף כקובץ `witness-check.txt`. כל מזהה פוסט נרשם כ `witness.posted`. `verify.py --channel`קורא רק ייצוא של ערוצי טלגרם, ולכן עבור Discord יש לשמור את יומן העד: הוא מכיל כל בדיקה.

### אפשרויות

| אפשרות | סביבה | ברירת מחדל | משמעות |
| --- | --- | --- | --- |
| `--interval` | `TGWITNESS_WITNESS_INTERVAL` | 10 | מרווחי זמן בין בדיקות: 1–1440 |
| `--timeout` | `_TIMEOUT` | 30 | שניות המתנה לאספן ול-Bot API: 5–600 |
| `--post` | `_POST` | `all` | `all`: כל הבדיקות; `changes`: נושא חדש או בעיה; `problems`: רק בעיות ותשובות חסרות |
| `--title` | `_TITLE` | `TgWitness witness` | המילים הראשונות בכל פוסט בערוץ |
| `--collector-fingerprint` | `_COLLECTOR_FINGERPRINT` | – | יש להציג את מפתח האספן במקום להסתמך על התשובה הראשונה |
| `--proxy` | `_PROXY` | ישיר | `socks5://host:port` או `http://host:port` |
| `--bot-api` | `_BOT_API` | `https://api.telegram.org` | כתובת ה-API של הבוט, למשל שרת API מקומי של הבוט |
| `--data-dir` | `_DATA` | `witness-data` | מפתח Witness ויומן |
| `--config` | `_CONFIG` | – | קובץ JSON עם אחת מהאפשרויות שלעיל |

כתובת האספן, האסימונים והערוץ מגיעים מ `--collector`, `--token` או `--token-file`, `--bot-token` או `--bot-token-file`, `--discord-webhook-file` ו `--channel`, או `_COLLECTOR`, `_TOKEN`, `_TOKEN_FILE`, `_BOT_TOKEN`, `_BOT_TOKEN_FILE`, `_DISCORD_WEBHOOK_FILE` ו `_CHANNEL`, מה שמונע מסודות להופיע ברשימת התהליכים.

קובץ התצורה משתמש בשמות האפשרויות עם קווים תחתונים, בתוספת `texts`, המחליף את המילים בהודעות הערוץ:

```
{"collector": "https://your-collector.example.org", "token_file": "witness-token.txt",
 "bot_token_file": "bot-token.txt", "channel": "@your_witness_channel",
 "interval": 5, "timeout": 30, "post": "changes", "title": "Partner witness",
 "texts": {"ok": "journal head", "no_response": "no answer from the collector", "records": "records"}}
```

מפתחות `texts`: `ok`, `key_changed`, `rollback`, `fork`, `invalid`, `no_response`, `collector`, `records`, `head`. שורת הפקודה גוברת על הסביבה, והסביבה גוברת על הקובץ. אפשרויות או מפתחות טקסט לא מוכרים עוצרים את התוכנה עם הודעה במקום להתעלם מהם. הניסוח לעולם אינו משפיע על האימות: verify.py בודק את האסימון החתום בסוף כל פרסום. ב-`--post changes` או ב-`problems`, בדיקות שלא פורסמו עדיין נמצאות ב יומן העדים, ו-`verify.py` מפרט אותן כלא פורסמו מעולם; רשומת הפתיחה מציינת את המדיניות. כל בדיקה עדיין מופיעה ביומן, ולכן פחות פרסומים משמעותם פחות פעמים עצמאיות ב-Telegram, ולא פחות בדיקות.

גם ללא ערוץ, ה-Witness ממשיך לנהל את היומן שלו. שמרו את טביעת האצבע של מפתח ה-Witness (`python -m tgwitness.witness fingerprint`) במקום אחר.

## דף הוכחה ציבורי למספר סביבות עבודה

`python -m tgwitness.proof` TgWitness תומך בעד 32 סביבות עבודה בו-זמנית ומציג דף לקריאה בלבד המכיל את הבדיקה החתומה האחרונה של כל אחת מהן. כל סביבת עבודה מקבלת מפתח Witness משלה ו יומן בתיקיית הנתונים, וכן מפתח אספן מוצמד; פרסום בערוץ Telegram הוא אופציונלי עבור כל סביבת עבודה. התחל מ- [proof.config.example](https://github.com/phishdestroy/TgWitness/blob/main/deploy/proof.config.example):

| תחום | משמעות |
| --- | --- |
| `title` | כותרת הדף, 1–100 תווים |
| `data_dir` | מפתחות ויומנים של Witness, ביחס לקובץ; ברירת מחדל `proof-data` |
| `interval`, `timeout` | דקות בין בדיקות (1–1440, ברירת מחדל 5); שניות להמתנה (5–600, ברירת מחדל 20) |
| `workspaces[].id`, `label` | כינוי קצר באותיות קטנות והשם המוצג |
| `workspaces[].collector` | כתובת ה-Collector; סביבות עבודה אחרות מסתיימות ב- `/profiles/<workspace ID>` |
| `workspaces[].collector_fingerprint` | נדרש, שונה עבור כל סביבת עבודה |
| `workspaces[].token_file` | קובץ עם אסימון העד לקריאה בלבד של סביבת העבודה הזו |
| `workspaces[].channel`, `bot_token_file` | אופציונלי, בשילוב: פרסום כל בדיקה בערוץ |
| `workspaces[].proxy`, `bot_api` | מסלול אופציונלי וכתובת ה-API של הבוט |

```
python -m tgwitness.proof --config proof.json --check-config
python -m tgwitness.proof --config proof.json --host 127.0.0.1 --port 8790
```

הפקודה הראשונה מאמתת את הקובץ ואת קבצי האסימונים מבלי לפתוח חיבור. הדף מגיב רק לפקודות GET ו-HEAD:

- `/` מציג את כל סביבות העבודה; סביבת עבודה שלא נבדקה במשך 2.5 מחזורים מסומנת כ"מיושנת".
- `/api/proof` מחזיר את אותו התוכן כמו JSON.
- `/api/proof/<id>` מוריד את ההצהרה החתומה העדכנית ביותר (`tgwitness-public-proof-v1`): מספר התיעוד של העד וה-hash, סטטוס, מפתח האספן המוצמד, נקודת ביקורת, מונה האיסוף והאם פרסום הערוץ הצליח, חתום על ידי מפתח העד של סביבת העבודה הזו.
- `/healthz` מציג שגיאה 503 כאשר הצג של סביבת העבודה הפסיק לפעול.

הקצו לדף שם מארח משלו, כמו [ב-Caddyfile.proof.example](https://github.com/phishdestroy/TgWitness/blob/main/deploy/Caddyfile.proof.example). לצורך אימות, ייצאו את יומן העדים של סביבת העבודה `python -m tgwitness.witness export --data-dir proof-data/<id> --out witness.zip` והשתמש בו כמתואר להלן.

## אמת

מצד ה-Witness, ייצוא היומן:

```
python -m tgwitness.witness export --out witness.zip
# Docker (add -f deploy/compose/compose.witness.yaml on a witness server):
docker compose exec witness python -m tgwitness.witness export --out /witness/witness.zip
docker compose cp witness:/witness/witness.zip .
```

לאחר מכן, מכל מקום, באמצעות קובץ ה-ZIP החתום של האספן והערוץ שיוצא מ-Telegram Desktop (*ייצוא היסטוריית צ'אט* → JSON נותן `result.json` ) או דף ה-`https://t.me/s/…` הציבורי שלו:

```
python verify.py tgwitness-evidence.zip --fingerprint COLLECTOR_SHA256 \
    --witness witness.zip --witness-fingerprint WITNESS_SHA256 --channel result.json
```

`verify.py` בודק את יומן העד (השרשרת והחתימות), ולאחר מכן מוודא **שכל כותרת שה עד ראה היא חלק מהיומן שיוצא**: לרישום באותו מספר חייב להיות בדיוק אותו חשיש. כותרת שאינה תואמת נכשלת באימות — היומן שונה לאחר שהעד ראה אותו. הוא מדווח גם על כותרות שנראו לאחר הייצוא, חריגות שהעד תיעד, תשובות שנכשלו, תקופות שנקודות הבדיקה התואמות שלהן קיימות בייצוא זה ("הועד מ-X עד Y") ופערים. נקודות בדיקה מאוחרות יותר אינן מאריכות תקופות אלה. התוצאה כוללת את מספר הרישום האחרון שהתאים ואת מספר הרישומים הבאים שאינם כוללים נקודת ביקורת תואמת. רק תשובות שנחתמו על ידי המפתח של הייצוא עצמו נספרות: ייצוא שנחתם על ידי מפתח שהעד מעולם לא ראה מדווח כלא מאומת, ובלי `--fingerprint` החותם שלו נשאר לא מאובטח. בשיטת ה-`--channel`, כל פוסט חתום חייב להתאים ליומן העד רשומה אחר רשומה: פוסטים ששונו נכשלים באימות, ופוסטים חסרים מפורטים ברשימה. תאריך ב- ייצוא JSON של Telegram שסופק הוא מטא-נתונים הניתנים לעריכה, מחוץ לאסימון העד החתום. התאמת האסימון אינה מאמתת את תאריך הפרסום; התוצאה מדווחת במפורש כי לא בוצע אימות של זמן הפרסום.

### נדרש גבול ייצוא מאומת

לצורך העברה שחייבת לכלול תיעוד סופי בנוכחות עדים, הוסף את `--require-witness`:

```
python verify.py tgwitness-evidence.zip --fingerprint COLLECTOR_SHA256 \
    --witness witness.zip --witness-fingerprint WITNESS_SHA256 --require-witness
```

לשם כך נדרשת טביעת אצבע של עד שנשמרה באופן עצמאי ונקודת ביקורת תואמת בדיוק בסוף הייצוא הזה. נקודת ביקורת המכסה רק קידומת מוקדמת יותר אינה מספיקה. יש להשהות את האיסוף, לאפשר לעד לבחון את המצב הסופי, ולייצא לפני כתיבות נוספות ביומן; אם היומן משתנה, יש לשמור נקודת ביקורת נוספת ו לייצא את המצב הזה. נקודת ביקורת מאוחרת יותר לבדה אינה יכולה לאמת את ה-hash הסופי של ייצוא קצר יותר. כאשר מסופק גם הדגל `--channel`, פוסטים נטענים חסרים או קבוצת התאמות ריקה נכשלים בבדיקה הקפדנית הזו. ללא הדגל, בדיקות תקינות רגילות עדיין מדווחות על רשומות שלא עברו אימות מבלי לדחות ארכיון שלם בכל שאר המובנים.

יש לשמור את יומן העד ואת המפתח המוצמד אליו בנפרד. בדיקות מקוונות מאמתות את הרציפות בין נקודות הבדיקה; אימות לא מקוון משווה כל נקודת בדיקה שנשמרה עם הייצוא. כותרות ישנות ללא הוכחות רציפות שומרות על ההשוואה הלא מקוונת ומדווחות ללא אימות רציפות מקוון. הדוח מפרט את זמן ההשבתה של העד ואת הפרסומים שנכשלו לפי מרווחי זמן.

### חותמות יומיות ולוחות שנה של חותמות זמן שאינם זמינים

ה-witness חותם את גבול היומן של היום הקודם לפי UTC ושולח את ה-hash של אותו חותם חתום ל-OpenTimestamps. הגשה ללוח השנה היא ראיה בהמתנה; רק התחייבויות ביטקוין שנבדקו באופן עצמאי מקבלות אישור במאמת.

אם כל לוחות השנה נכשלים, החותם החתום והניסיון הכושל נשארים ב יומן. תהליך התחזוקה השעתי מנסה שוב את אותו הרישום המקורי, כולל לאחר הפעלה מחדש או שינוי תאריך. הוא סורק לכל היותר חותמות 32, מגיש לכל היותר שתי הגשות חסרות ומקדיש לכל היותר 60 שניות לניסיונות חוזרים בכל מחזור. סמן קבוע עובר בין החותמות הישנות יותר. הגשות שנשמרו עוקבות אחר נתיב שדרוג ההוכחה הקיים.

ניסיון חוזר אינו כותב מחדש את החותם, אינו משנה את התאריך המקורי שלו ואינו טוען כי הלוח קיבל אותו מוקדם יותר. התחייבות מאוחרת יותר של ביטקוין נותרת אישור חיצוני מאוחר יותר. הוכחות חסרות נותרות ב-`none`; הוכחות בהמתנה נותרות ב-`pending` עד שהמאמת בודק אותן באופן עצמאי.
