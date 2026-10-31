# עד עצמאי

Canonical page: https://phishdestroy.github.io/TgWitness/he/docs/reference/witness/

הפעל את Witness עם מפתח ובוט משלו, פרסם נקודות ביקורת חתומות בערוץ ובדוק את הייצוא מולן.

[הגדרת הבוט והפרוקסי ברוסית](https://github.com/phishdestroy/TgWitness/blob/main/docs/ru/WITNESS.md).

אוסף הנתונים חותם על היומן שלו עצמו, ולכן מי ששולט באוסף הנתונים ובמפתח שלו יכול, בעיקרון, לשכתב או לקצר את היומן ולחתום עליו שוב. "Witness" מאפשר לזהות זאת. זהו תהליך נפרד — מיכל נוסף, או ליתר דיוק שרת שמישהו אחר מפעיל — אשר כל כמה דקות משיג את ראש היומן החתום של האספן, חותם על מה ש ראה באמצעות המפתח שלו, שומר זאת ביומן משלו ומפרסם זאת בערוץ טלגרם.

תרשים זרימה · Collector → Witness (נקודת ביקורת חתומה: מספר הרשומות + חתימת ה-hash של הכותרת); Witness → יומן Witness, מפתח פרטי; Witness → ערוץ טלגרם (הודעה חתומה באמצעות הבוט של האתר); קובץ ZIP של הראיות → verify.py; יומן Witness, מפתח פרטי → verify.py; ערוץ טלגרם → verify.py (ייצוא מ-Telegram Desktop או דף "t.me/s") · Collector · Witness · יומן Witness, מפתח פרטי · ערוץ טלגרם · קובץ ZIP של הראיות · verify.py · נקודת ביקורת חתומה: מספר · הרשומות + חתימת ה-hash של · הכותרת · הודעה חתומה באמצעות הבוט של · האתר · ייצוא מ-Telegram Desktop או · דף "t.me/s"

**תרשים כטקסט**

1. Collector → Witness (נקודת ביקורת חתומה: מספר הרשומות + חתימת ה-hash של הכותרת)
2. Witness → יומן Witness, מפתח פרטי
3. Witness → ערוץ טלגרם (הודעה חתומה באמצעות הבוט של האתר)
4. קובץ ZIP של הראיות → verify.py
5. יומן Witness, מפתח פרטי → verify.py
6. ערוץ טלגרם → verify.py (ייצוא מ-Telegram Desktop או דף "t.me/s")

## מה ה-TgWitness מספק, ומה הוא אינו מספק

| ל-TgWitness יש | העד מעולם לא |
| --- | --- |
| **אסימון עדות** לקריאה בלבד עבור סביבת עבודה אחת | פרטי ההתחברות של האספן ל-Telegram או פרטי הזיהוי ל-API |
| מפתח Ed25519 ויומן משלו | כספת האספן, מפתח החתימה או אסימון הפאנל |
| אסימון בוט טלגרם משלו | תוכן ההודעה: בראש ההודעה מופיע מספר הרשומות ו-hash |

האסימון נוצר בדף **ה-Witness** של הפאנל, מוצג פעם אחת ונשמר רק כ- SHA-256. הוא פותח נקודת קצה אחת בדיוק, `GET /api/witness/head`, המחזירה נקודת ביקורת חתומה טרייה, בנוסף למונים חתומים של איסוף ללא תוכן ולמצב תפעולי. הוא אינו יכול לפתוח את הפאנל, לקרוא תוכן הודעות או לשנות הגדרות, ו אסימון הפאנל אינו מתקבל שם. ניתן לבטל אסימון באותו דף. האספן מתעד מתי מפתח עד חדש מתחיל לבדוק (`witness.seen`) ומציג את הבדיקה האחרונה לכל אסימון; עד שלא נבדק תוך 2.5 מרווחי זמן מסומן כאיחור.

עדים חדשים שולחים אתגר אקראי בכל סקר; הצהרת הלכידה חוזרת עליו תחת חתימת האספן. מונים קשורים לנקודת הבדיקה המדויקת ונכללים בפוסטים חתומים של העדים. כותרות ישנות ממשיכות להתקבל על ידי העד העצמאי. צמיחת היומן כשלעצמה לעולם אינה נספרת כהודעה חדשה.

## מה הוא בודק ומתעד

בכל פרק זמן (10 דקות כברירת מחדל) ה-Witness:

1. מביא את הראש עצמו (האספן אינו יכול לדחוף או לדלג עליו);
2. מאמת את חתימת האספן, את מפתח האספן המוצמד (`--collector-fingerprint`, או המפתח הראשון שנראה), ספירה שאינה פוחתת וראש שלא השתנה בספירה שלא השתנתה;
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

פתח **תוספות → בוט בערוץ שלך → הגדר בוט** בלוח הבקרה. שלושה שלבים מכסים גישה לקריאה בלבד, הערוץ שלך והמרווח, ולאחר מכן הפעלת ה-Witness. מדיניות פרסום, פרוקסי HTTP/SOCKS5 אופציונלי וכתובת API מותאמת אישית לבוט נמצאים תחת **הגדרות מתקדמות** . הטופס מוריד את `witness.json` עם מפתח האספן של סביבת העבודה הזו מוצמד. הורידו את האסימון לקריאה בלבד שנוצר זה עתה באמצעות **'שמור קובץ גישה** כ-`witness-token.txt` '; שימו אותו ואת `bot-token.txt` שנוצר במארח ה-Witness לצד קובץ ה-JSON הזה. האספן לעולם אינו מקבל את אסימון הבוט. ההורדה אינה מפעילה שירות ואינה מפרסמת הודעה. אף עד לפרויקט מאוחסן אינו נרשם באופן מרומז.

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

כתובת האספן, האסימונים והערוץ מקורם ב-`--collector`, `--token` או `--token-file`, `--bot-token` או `--bot-token-file` ו-`--channel`, או `_COLLECTOR`, `_TOKEN`, `_TOKEN_FILE`, `_BOT_TOKEN`, `_BOT_TOKEN_FILE` ו-`_CHANNEL`, מה שמאפשר לשמור על סודיות מחוץ לרשימת התהליכים.

קובץ התצורה משתמש בשמות האפשרויות עם קווים תחתונים, בתוספת `texts`, המחליף את המילים בהודעות הערוץ:

```
{"collector": "https://your-collector.example.org", "token_file": "witness-token.txt",
 "bot_token_file": "bot-token.txt", "channel": "@your_witness_channel",
 "interval": 5, "timeout": 30, "post": "changes", "title": "Partner witness",
 "texts": {"ok": "journal head", "no_response": "no answer from the collector", "records": "records"}}
```

מפתחות `texts`: `ok`, `key_changed`, `rollback`, `fork`, `invalid`, `no_response`, `collector`, `records`, `head`. שורת הפקודה גוברת על הסביבה, והסביבה גוברת על הקובץ. אפשרויות או מפתחות טקסט לא מוכרים עוצרים את התוכנה עם הודעה במקום להתעלם מהם. הניסוח לעולם אינו משפיע על האימות: verify.py בודק את האסימון החתום בסוף כל פרסום. ב-`--post changes` או ב-`problems`, בדיקות שלא פורסמו עדיין נמצאות ב יומן העדים, ו-`verify.py` מפרט אותן כלא פורסמו מעולם; רשומת הפתיחה מציינת את המדיניות. כל בדיקה עדיין מופיעה ביומן, ולכן פחות פרסומים משמעותם פחות פעמים עצמאיות ב-Telegram, ולא פחות בדיקות.

גם ללא ערוץ, ה-Witness ממשיך לנהל את היומן שלו. שמרו את טביעת האצבע של מפתח ה-Witness (`python -m tgwitness.witness fingerprint`) במקום אחר.

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

הסימון מבטיח עקביות עם רישומי העדים המסופקים והמוצמדים. על המפעיל להמשיך ולוודא את עצמאותו של העד ולשמור את הרישומים בנפרד. הסימון אינו קובע את אמיתות ההודעות, את שלמות האוסף או את משך הזמן שנמדד באופן עצמאי.

"עדות" מציגה את מה שהאספן דיווח באותם רגעים, וכי ייצוא מאוחר יותר תואם לכך. היא אינה מראה שהאספן תיעד את כל מה ש-Telegram העביר, או שתוכן ההודעות הוא אמת. "עדות" המופעלת על ידי אותו מפעיל על אותה מכונה היא חלשה יותר מזו המופעלת על ידי אדם אחר.

עלייה במספר בלבד אינה יכולה להוכיח רציפות של "הוספה בלבד" ברשת: ההשוואה במצב לא מקוון חייבת להתאים כל חתימת hash של קידומת שנשמרה מול הייצוא המלא של האספן. זמן השבתה של Witness וכישלונות בפרסום מותירים פרקי זמן ללא נקודות ייחוס חיצוניות. ניתן לדווח על פוסטים חסרים בהשוואה ליומן Witness שנשמר; לא ערוץ ולא שרת הנשלטים על ידי אותו מפעיל מהווים ארכיון צד שלישי בלתי ניתן לשינוי.
