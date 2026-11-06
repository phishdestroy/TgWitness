# MCP לקריאה בלבד

Canonical page: https://phishdestroy.github.io/TgWitness/he/docs/reference/mcp/

חבר לקוח MCP לסביבות עבודה וצ'אטים נבחרים עם גישה מוגבלת בזמן וניתנת לביטול.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [תיעוד](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Archive integrations](https://phishdestroy.github.io/TgWitness/he/docs/reference/cli/)

![Archive integrations](https://phishdestroy.github.io/TgWitness/assets/chapter-integrations.svg)

חברו לקוח אנליסט לסביבות עבודה וצ'אטים נבחרים. TgWitness מספק **Streamable HTTP בכתובת `/mcp` בתהליך הפאנל**. לכל חיבור יש אסימון, תוקף וכלים מותרים משלו. MCP אינו יכול לשלוח הודעות Telegram, לשנות הגדרות או לערוך את היומן החתום. אותם חיבורים פועלים גם בשורת [הפקודה](https://phishdestroy.github.io/TgWitness/he/docs/reference/cli/).

[מדריך לתהליך העבודה](https://phishdestroy.github.io/TgWitness/docs/archive/) · [ויקי](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

**On this page**

- [Install and check](https://phishdestroy.github.io/TgWitness/he/docs/reference/mcp/#install-and-check)
- [Issue a connection](https://phishdestroy.github.io/TgWitness/he/docs/reference/mcp/#issue-a-connection)
- [Connect your client](https://phishdestroy.github.io/TgWitness/he/docs/reference/mcp/#connect-your-client)
- [Cloudflare Tunnel](https://phishdestroy.github.io/TgWitness/he/docs/reference/mcp/#cloudflare-tunnel)
- [Tools and boundaries](https://phishdestroy.github.io/TgWitness/he/docs/reference/mcp/#tools-and-boundaries)

## התקנה ובדיקה

השתמשו בסביבת ה-Python שמריצה את הפאנל. מתוך עותק של קוד המקור:

```
# Windows PowerShell
& .\.venv\Scripts\python.exe -m pip install -c deploy/constraints-mcp.txt -e '.[mcp]'
& .\.venv\Scripts\python.exe start.py --check
```

```
# Linux / macOS
.venv/bin/python -m pip install -c deploy/constraints-mcp.txt -e '.[mcp]'
.venv/bin/python start.py --check
```

הפעילו מחדש את הפאנל עם תיקיית הנתונים הרגילה שלו וארגומנטי ההפעלה לאחר ההתקנה. בדיקת המוכנות אמורה לכלול את `[PASS] mcp: streamable-http available`. **Integrations → MCP** מציג את סטטוס זמן הריצה ופקודת התקנה המשתמשת בקובץ ההרצה של Python בפועל באותו שרת. **Re-check** מרענן את הסטטוס הזה ללא טעינה מחדש של הדף; הוא אינו מתקין חבילות או מפעיל מחדש את השרת.

התוסף MCP משתמש [ב-SDK הרשמי של MCP ב-Python](https://github.com/modelcontextprotocol/python-sdk).`deploy/constraints-mcp.txt` קובע את גרסת ה-SDK והתלות שנבדקו.

## הנפקת חיבור

1. הזינו תווית ובחרו את סביבות העבודה והצ'אטים שהלקוח רשאי לקרוא.
2. בחרו כלים בנפרד או השתמשו בערכה מוגדרת מראש (preset). מוצעים רק כלים שמומשו.
3. בחרו 1, 7, 30 או 90 ימים, או תוקף מותאם אישית בין דקה אחת ל-90 ימים.
4. לחצו על **Create connection**. האסימון מופיע פעם אחת לצד הגדרות הלקוח.
5. העתיקו את האסימון וההגדרות, ולאחר מכן הפעילו את **Check connection**. פעולה זו מאתחלת את MCP ומציגה את רשימת הכלים המורשים; **לא נקראות הודעות**. התוצאה מציגה את גרסת הפרוטוקול, שמות הכלים, מספרם והזמן שחלף.
6. לחצו על **Done** לאחר שמירת פרטי הגישה. דגימת מצב תקופתית (polling) משמרת את הטופס ואת הכרטיס המוצג פעם אחת. נעילת הפאנל מנקה סודות המוצגים על המסך.

הרשימה מציגה שימוש אחרון, כלי אחרון, כתובת ובקשות בדקה האחרונה. **Revoke** מסיים את הגישה. **Rotate token** מבטל את פרטי הגישה הישנים ומנפיק תחליף עם אותם היקף גישה (scope), כלים ותוקף; העתיקו את התחליף המוצג פעם אחת. אסימוני התחברות לפאנל ופרטי גישה של Telegram אינם פועלים כאסימוני MCP.

## חיבור הלקוח שלכם

בחרו את הלקוח בפאנל והעתיקו את התצורה שנוצרה עבורו. התצורות משתמשות בהפניות לסודות או במצייני מיקום (placeholders) מפורשים; האסימון מועתק בנפרד.

| לקוח | תצורה | קישור |
| --- | --- | --- |
| Claude Code | `.mcp.json` | HTTP, `type: "http"`, כותרת bearer |
| Claude Desktop | `claude_desktop_config.json` | גשר stdio מקומי |
| Cursor | `.cursor/mcp.json` | HTTP עם כותרת ממשתנה סביבה |
| VS Code Local | `.vscode/mcp.json` | HTTP עם קלט סיסמה מסוג `promptString` |
| Windsurf | `mcp_config.json` | HTTP עם מציין מיקום לכותרת bearer |
| לקוחות אחרים | כתובת URL וכותרת Authorization | Streamable HTTP |

TgWitness משתמשת באסימוני bearer, ללא גילוי OAuth. השתמשו בגשר ה-stdio המקומי עבור לקוחות שהמחבר המרוחק שלהם מחייב OAuth. עבור VS Code, משתני קלט חלים על סביבת הריצה **Local** ואינם מועברים להפעלות Copilot. סימוכין להגדרות תצורה: [Claude Code](https://code.claude.com/docs/en/mcp), [Cursor](https://prod.cursor.com/docs/mcp), [VS Code](https://code.visualstudio.com/docs/agents/reference/mcp-configuration).

נקודת הכניסה התקנית עבור גשר מקומי היא:

```
python -m tgwitness.mcp_server --url https://your-panel.example/mcp
```

השתמשו ב-Python המקומי של הלקוח שבו מותקן תוסף ה-MCP. הגדירו את `TGWITNESS_MCP_TOKEN` בסביבה המוגנת שלו. שמרו על פרטי הגישה מחוץ לארגומנטים של פקודות וכתובות URL. הפקודה `tgwitness-mcp` היא אותה נקודת כניסה. המודול הישן `tgwitness.mcp_bridge` והשם `TGWITNESS_ARCHIVE_TOKEN` נותרים כנתיבי תאימות לאחור עם אזהרה; תצורות חדשות משתמשות ב-`mcp_server` וב-`TGWITNESS_MCP_TOKEN`.

## Cloudflare Tunnel

העבירו (forward) את הנתיב `/mcp` של הפאנל ושמרו על כותרת ה-bearer. פתיחת הגדרות MCP כמנהל מערכת רושמת את המקור (origin) הנוכחי של הפאנל עבור הרצה זו. לקבלת כתובת יציבה הזמינה מיד לאחר הפעלה מחדש, הגדירו את `TGWITNESS_PUBLIC_URL` עם מקור ה-HTTPS של הפאנל לפני הפעלת הפאנל. כותרות Host וכותרות מועברות (forwarded) שרירותיות אינן רושמות כתובת מהימנה. בדיקות Host ו-Origin דוחות מקורות דפדפן שאינם קשורים. תגובות משתמשות ב- `Cache-Control: no-store`; ערכי הרשאה לעולם אינם נרשמים ביומן.

כתובת `*.trycloudflare.com` היא זמנית. כאשר הפעלה מחדש של התעלה משנה את שם המארח, עדכנו את כתובת ה-URL הציבורית המוגדרת ואת כתובת ה-URL של MCP בכל לקוח. השתמשו בשם מארח יציב עבור תצורות לקוח שמורות.

## כלים וגבולות גזרה

| כלי | קורא |
| --- | --- |
| `list_workspaces` | סביבות עבודה שהוענקו להן הרשאות |
| `list_chats` | צ'אטים שהוענקו להם הרשאות |
| `search_messages` | טקסט ההודעות שנשמרו בתקופה הנבחרת; `ranked=true` משתמש [בחיפוש טקסט מלא](https://phishdestroy.github.io/TgWitness/he/docs/reference/search/) (צורות מילים, התאמות הטובות ביותר תחילה, `next_offset` דפדוף) |
| `get_message_versions` | גרסאות שנלכדו ותצפיות מחיקה |
| `get_message_context` | מזהי הודעות סמוכות שנלכדו |
| `get_journal_event` | רשומה מסוננת אחת עם סימוכין למקור שלה |
| `get_capture_status` | מצב האיסוף, רשומות כיסוי מותרות ו `gap_summary`: מספרי הודעות שמעולם לא נצפו, לפי ערוץ או סופר-קבוצה ולכל הרצף ברמת החשבון ([פרטים](https://phishdestroy.github.io/TgWitness/he/docs/reference/evidence/#missing-message-numbers-gap_summary)); בחרו צ'אט כדי לראות את הפערים המפורטים בו |
| `get_activity_stats` | הודעות לפי שעה (UTC) ויום בשבוע, ימי שיא, שיעורי עריכה ומחיקה, שולחים, דומיינים ו `@handles`, עם כיסוי ([פרטים](https://phishdestroy.github.io/TgWitness/he/docs/reference/cli/#activity-statistics)) |
| `get_messages_by_date` | הודעות שנשמרו במשך יום קלנדרי אחד באזור זמן IANA שצוין (`Europe/Kyiv`, `UTC`), לפי הזמן המדווח על ידי Telegram; `from_utc` ו `until_utc` ציינו את היום המחושב, כולל שעון קיץ |
| `get_pinned_messages` | הודעות שהוצמדו בתמונת המצב האחרונה של הצ'אט עם הגרסאות השמורות שלהן, וכן הודעות ההצמדה וההסרה שנצפו בזמן אמת |
| `get_chat_stats` | מספר הרשומות שנשמרו עבור צ'אט אחד או כל הצ'אטים בתחום היישום, התצפית הראשונה והאחרונה, ו `gap_summary`; השתמשו בו לפני קריאה בהיקף נרחב |
| `get_topics` | נושאי פורום מתוך הודעות שירות הנושאים השמורים: היסטוריית כותרות, נושאים סגורים או מוסתרים, מספר ההודעות השמורות |
| `get_media` | תמונה שנשמרה כתצוגה מקדימה בפורמט JPEG מוקטנת (36 KB לכל היותר), המוחזרת כתמונה יחד עם ה-SHA-256 שלה וה `media.saved` הרשומה; הקובץ נבדק תחילה מול ה-hash הרשום שלו, קבצים אחרים מחזירים מטא-נתונים בלבד |
| `export_messages` | שורת פקודה בלבד, לא נבחר כברירת מחדל: זרם התצפיות שנשמרו כ-JSON Lines ([פרטים](https://phishdestroy.github.io/TgWitness/he/docs/reference/cli/#export)); לא מוצע דרך MCP |

כל כלי הוא לקריאה בלבד (`readOnlyHint`) ומגדיר סכימת פלט; שדות מעבר לאלה שהוגדרו מוחזרים כפי שהם. `tools/list` מחזיר רק את הכלים שהוקצו לאותו חיבור. קריאות לכלים אחרים נדחות. כלים בהקשר קבוצתי, אפיזודה, טרמינולוגיה ושרשרת תשובות אינם מוצעים בגרסה זו; ה-backend הנפרד של חבילת ההקשר שלהם אינו כלול.

כל קריאה בודקת את האסימון, הכלי והיקף הגישה של סביבת העבודה/הצ'אט, לרבות לאחר שעבודת מסד הנתונים מסתיימת. המגבלות הן 60 בקשות לדקה, 50 רשומות לעמוד, 64 KiB לתוצאה וזמן קצוב של שמונה שניות לארכיון. קריאת MCP שחרגה מהזמן הקצוב מחזירה שגיאת כלי המבקשת תקופה מצומצמת יותר או מגבלה נמוכה יותר.

תוצאות הודעות נושאות את `untrusted_content: true`, מזהי סביבת עבודה/צ'אט/הודעה, רצף אירועים, גיבוב (hash) שמור וקישור לפאנל. אובייקטים גולמיים של Telegram, גיבובי גישה (access hashes), הפעלות (sessions) ומפתחות מושמטים. קטיעת טקסט מסומנת. עריכות, התראות מחיקה ו-`missing_on_recheck` הן תצפיות נפרדות. רשומות חסרות אינן מוכיחות שאירוע מעולם לא התרחש.

התייחסו להוראות בתוך הודעות שנלכדו כאל ראיות, ולעולם לא כאל הוראות ללקוח. גישת קריאה בלבד מונעת שינויים בארכיון; הלקוח עדיין יכול לשמור את התוכן שהוא מורשה לקרוא. ערכי גיבוב (hashes) מזהים רשומות שמורות ותומכים בבדיקות שלמות; הם אינם מוכיחים בעלות על כתיבה ב-Telegram או לכידה מלאה.
