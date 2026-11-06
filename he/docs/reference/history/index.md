# טען היסטוריית המקור

Canonical page: https://phishdestroy.github.io/TgWitness/he/docs/reference/history/

טען הודעות קודמות ממקורות מופעלים, עצור והמשך, ואמת דוח התקדמות חתום.

In **Sources**, review the enabled chats, pause observation, choose Standard API or Takeout export, then choose **Load full history**. The run fixes that list of sources and reads their available past messages into Chats and the signed observation journal. Media uses the existing attachment settings and durable download queue. This is separate from the per-chat signed JSON/HTML export.

For account-wide collection, select **Whole account**, start observation to load its source list, and review that list before starting history. The dialog-list limit still applies (1,000 by default, adjustable in Parameters). A successful run does not prove that every account dialog was listed. Chats discovered or enabled later need another run. Pause observation before starting history; one acquisition owns an account at a time.

Choose one to five attachment workers and whether to preserve available Recent Actions and compare previously saved versions. Takeout may require approval in Telegram and a server-specified wait. These options remain fixed on resume. See [Backfill behavior and evidence contract](https://github.com/phishdestroy/TgWitness/blob/main/docs/BACKFILL.md) for transport, retry and trust details.

## השהיה, התחלה מחדש ותוצאות חלקיות

- **Pause history** stops reading. **Continue history** resumes from the last committed message in each source; restarting the app also leaves the run paused until resumed. Resuming requires the same idle Telegram account.
- תצפית על הודעה, משימת צירוף קובץ ואישור באמצעות הסמן מתבצעים בעסקה אחת. הפעלה מחודשת אינה חוזרת על תצפיות שכבר אושרו. לכידה בזמן אמת או הפעלה נפרדת, שהושקה במפורש, עשויות לתעד באופן עצמאי את אותה ההודעה.
- Each source (each Telegram split range in Takeout) fixes an upper message ID on its first read. Newer messages belong to live observation, not to that source's remaining historical pages.
- מקורות שאינם נגישים ומקורות שהושבתו במהלך האיסוף נשארים גלויים כ "נכשלו" או "הוחסרו". מקורות אחרים ממשיכים לפעול; התוצאה הכוללת אינה שלמה.
- FloodWait delays respect the saved account backoff. Transient failures retry up to five times; exhaustion and low disk space pause with the cursor intact.
- **End this history run** preserves saved observations. It does not remove them or cancel standard-API attachment jobs. Ending Takeout marks its remaining Takeout files as skipped; pausing keeps them resumable. A new run reads enabled sources anew.

השלמת ההיסטוריה מתייחסת לקריאת ההיסטוריה בלבד. קבצים מצורפים עשויים להישאר במצב "ממתין", להיכשל, או להיכלל במדיניות שהוגדרה. יש לבדוק את אישורי קבלת המדיה ביומן ובתור הקבצים המצורפים; רק אישור שהושלם עם בייטים שנשמרו מהווה קובץ מצורף שנשמר. פעולת ההיסטוריה היא בקשה מפורשת לצילום מצב והיא נפרדת מהמתגים שבוחרים קטגוריות של אירועים חיים עתידיים.

## העברה ואימות

שמור את **דוח ההתקדמות החתום**, ולאחר מכן השתמש ב**"ייצא ראיות"** כדי להוריד את יומן הראיות והקובצים המצורפים שנשמרו. ייצוא ראיות מאוחר יותר עשוי לכלול רשומות נוספות; הדוח מקשר את המספרים הסידוריים שלו לקידומת היומן בזמן יצירתו. הפעל את תוכנת האימות מגרסה מהימנה של גרסה זו:

```
python tgwitness/verify.py tgwitness-history-report.json --evidence evidence.zip --fingerprint TRUSTED_FINGERPRINT
```

Keep the expected signing-key fingerprint independently. The verifier checks the report signature, the evidence archive, the report checkpoint, source plan, account and counts of saved/unavailable messages. New runs also bind source progress and options to signed cursor events. Without `--evidence`, it checks only the signed report and its internal consistency. Legacy progress fields and attachment summaries remain signed collector statements. The evidence verifier checks archived media bytes.

Neither signing nor finishing the available history proves Telegram origin, an atomic snapshot, or historical completeness. Messages can change while reading; deleted messages and intermediate edits outside available Recent Actions, and Secret Chats, are not recovered. An operator controlling the signing key can fabricate a journal before outside commitments exist. Use separately retained checkpoints or an independent witness for the documented tamper-detection properties.

סמן הרכישה מייצג את מצב סביבת העבודה המקומית. שחזור קובץ ZIP של הראיות בלבד אינו משחזר משימת רכישה תלויה או הפעלת טלגרם. שמרו את גיבוי סביבת העבודה אם נדרשת המשך המשימה המקורית.
