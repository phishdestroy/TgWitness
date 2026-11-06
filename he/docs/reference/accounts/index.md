# חשבונות ופורמטים של הפעלות

Canonical page: https://phishdestroy.github.io/TgWitness/he/docs/reference/accounts/

התחברו באמצעות טלפון, קוד QR או מפתח אימות, ייבאו הפעלות מ-Telethon, Pyrogram או Telegram Desktop, והפעילו מספר חשבונות.

TgWitness מתחבר כחשבון **משתמש טלגרם** (לא כבוט) באמצעות MTProto, תוך שימוש ב- Telethon. כל חשבון פועל בס**ביבת** עבודה משלו (המכונה "*סביבת עבודה*" ב- API ובכלי שורת הפקודה) עם הפעלה, מקורות, יומן ומפתח חתימה משלו.

קובצי הפעלה, מחרוזות הפעלה ומפתחות אימות (Auth Keys) הם **אישורי גישה לחשבון**: מי שמחזיק באחד מהם יכול לפעול בשם אותו חשבון. הם אינם מכילים היסטוריית הודעות.

> [!אזהרה] **אל תשתמשו בשום דבר שאינכם יכולים להרשות לעצמכם לאבד.** אנו ממליצים בחום להימנע מחיבור חשבונות אישיים או בעלי ערך אחר, וכן מיצירת מזהה API / חתימת API על חשבון שחשוב לכם. זה לא קשור לכך ש-TgWitness לא נבדק: טלגרם מגביל ו חוסם חשבונות לצמיתות באופן בלתי צפוי — כאשר נפח הבקשות נחשב בעיניו כמופרז, ללא תלות בלקוח או במטרה, וללא תיעוד הולם. חסימות רבות הן בלתי הפיכות. השתמשו בחשבונות ייעודיים. תפקוד חלק של הבדיקות תלוי ב-Telegram, ולא בתוכנה, ואינו מבטיח דבר לעתיד.

- [במבט חטוף](https://phishdestroy.github.io/TgWitness/he/docs/reference/accounts/#at-a-glance)
- [לפני שתתחילו: מזהה API ו-hash של API](https://phishdestroy.github.io/TgWitness/he/docs/reference/accounts/#before-you-start-api-id-and-api-hash)
- [מספר טלפון](https://phishdestroy.github.io/TgWitness/he/docs/reference/accounts/#phone-number) · [קוד QR](https://phishdestroy.github.io/TgWitness/he/docs/reference/accounts/#qr-code) · [מפתח אימות + מזהה DC](https://phishdestroy.github.io/TgWitness/he/docs/reference/accounts/#auth-key--dc-id)
- [קובצי חשבונות](https://phishdestroy.github.io/TgWitness/he/docs/reference/accounts/#account-files): [Telethon .session](https://phishdestroy.github.io/TgWitness/he/docs/reference/accounts/#telethon-session) · [Pyrogram .session](https://phishdestroy.github.io/TgWitness/he/docs/reference/accounts/#pyrogram-session) · [צמד של סשן + JSON](https://phishdestroy.github.io/TgWitness/he/docs/reference/accounts/#session--json-pair) · [TData](https://phishdestroy.github.io/TgWitness/he/docs/reference/accounts/#telegram-desktop-tdata) · [StringSession](https://phishdestroy.github.io/TgWitness/he/docs/reference/accounts/#telethon-stringsession) · [קובץ JSON של החשבון](https://phishdestroy.github.io/TgWitness/he/docs/reference/accounts/#account-json)
- [זהו את מה שיש ברשותכם](https://phishdestroy.github.io/TgWitness/he/docs/reference/accounts/#identify-what-you-have) · [פורמטים שאינם נתמכים](https://phishdestroy.github.io/TgWitness/he/docs/reference/accounts/#unsupported-formats)
- [חשבונות מרובים](https://phishdestroy.github.io/TgWitness/he/docs/reference/accounts/#multiple-accounts) · [שמירה על אבטחת קבצי החשבונות](https://phishdestroy.github.io/TgWitness/he/docs/reference/accounts/#keeping-account-files-safe) · [פתרון בעיות](https://phishdestroy.github.io/TgWitness/he/docs/reference/accounts/#troubleshooting)

## במבט חטוף

| מה יש לך | כרטיסייה ב"**הוסף חשבון"** | כמו כן, תזדקקו ל: |
| --- | --- | --- |
| מספר הטלפון וגישה לקודי הכניסה | **טלפון** | סיסמת 2FA, אם האפשרות מופעלת |
| Telegram פתוח במכשיר אחר | **קוד QR** | סיסמת 2FA, אם האפשרות מופעלת |
| קובץ `.session` (Telethon או Pyrogram) | **קבצים** | קובץ JSON נלווה אופציונלי להגדרות האפליקציה |
| `.session` + `.json` עם אותו שם | **קבצים** (בחר בשניהם) | בדרך כלל אין דבר נוסף |
| תיקיית `tdata` ב-Telegram Desktop | **קבצים** (בפורמט ZIP) | קוד הגישה המקומי של שולחן העבודה, אם הוגדר כזה |
| StringSession של Telethon (טקסט, `.txt`, `.tgwitness-session`) | **קבצים** | אין צורך בזוג API נפרד |
| `.json` עם מפתח הפעלה או מפתח אימות | **קבצים** | אין צורך בזוג API נפרד |
| מפתח אימות (512 תווים הקסדצימליים) ומספר ה-DC שלו | **מפתח אימות** | מזהה משתמש אופציונלי |

TgWitness מזהה קבצים לפי **תוכנם**, ולא לפי שמותיהם. שינוי שם של קובץ לעולם אינו מוביל להמרתו.

## לפני שתתחילו: מזהה API ו-hash של API

You can sign in without creating a Telegram API application. When no pair is entered, imported or already saved in the workspace, TgWitness picks a pair from its built-in pool of 50 public API pairs (`tgwitness/api_pool.py`), preferring Telegram Desktop for a fresh login and retaining a saved pair first; remaining candidates are shuffled. If Telegram refuses a pair (`API_ID_INVALID`, `API_ID_PUBLISHED_FLOOD`, `UPDATE_APP_TO_LOGIN`), the next one is tried, up to eight per sign-in; refused pairs are skipped until restart. The pair that signed in is saved with the account and reused for it. An **API ID** and **API hash** identify the application to Telegram; they do not authorize an account by themselves.

Missing connection fields use a deterministic device/OS pair from the bundled [opentele2 2.0.0 catalogs](https://github.com/DedInc/opentele2/tree/7e973bc71cd7a714ad13ac703c0895a90d36a735): Desktop `2040`, Android `6`, Android X `21724`, iOS `10840`, macOS `2834`, and Web `2496`. Android's source-build ID `4` also uses the Android catalog, as identified in [Telegram Android's BuildVars](https://github.com/DrKLO/Telegram/blob/master/TMessagesProj/src/main/java/org/telegram/messenger/BuildVars.java). Web defaults to A; an imported `K` app-version suffix or `macos` language pack selects K, and version `0.7.0` selects Webogram. Unknown application IDs keep Telethon's host defaults. Imported fields always win, including an older app version and an empty language pack. The catalog never changes the API ID/hash. Its version snapshot is reviewed explicitly, not fetched during login. A saved profile stays stable after updates.

`account.getAuthorizations` reports Telegram's saved authorization metadata; it is not an echo of each new `initConnection`. Compare it with the actual sent profile. Connecting an existing authorization does not validate its companion API hash: `initConnection` sends the API ID, while the hash is used by login requests.

After a new phone or QR authorization, TgWitness requests config, nearest DC, online status, languages (when the language pack is nonempty), app updates and terms-of-service updates, with 0.3–1.5 seconds between requests. Updating status briefly marks the account online. This sequence runs once at login completion, not on imports, reconnects or restarts. The authorization is saved first; a failed request stops the sequence without retrying or discarding the login. Results are recorded as `account.initialized`, with error names rather than response bodies. The sequence is not a guarantee against account restrictions.

For `tdesktop`, a missing `tz_offset` uses the server's local UTC offset, rounded to 900 seconds using the [opentele2 algorithm](https://github.com/DedInc/opentele2/blob/7e973bc71cd7a714ad13ac703c0895a90d36a735/crates/opentele2-core/src/fingerprint.rs) (MIT; license in `tgwitness/client_profiles.LICENSE`). It is refreshed on each connection so daylight-saving changes are reflected. An imported `tz_offset` takes precedence on every platform and is kept exactly, including zero. Other `initConnection.params` entries are retained. The HTTP sign-in form accepts the numeric timezone returned by file import; booleans, fractions and offsets outside the supported range are rejected.

Direct, SOCKS5 and HTTP CONNECT routes use Telethon's `ConnectionTcpObfuscated` (obfuscated abridged MTProto). HTTPS CONNECT retains TLS to the proxy and uses the same obfuscated transport inside the tunnel. MTProxy retains its required randomized intermediate transport and secret handling. Route switches apply the same choices. Obfuscation changes packet framing; it does not hide the account or its client metadata from Telegram or imply immunity to restrictions.

After connecting an authorized client, TgWitness checks config, nearest DC, the current authorization, the reviewed layer baseline, languages, app updates and terms-of-service updates. These diagnostics run once per client instance, before collection, and are shown under the connection details with their time. `account.connection_checked` records the result without session hashes, IPs, tokens or API hashes. They never accept terms or install updates. A request failure or FloodWait stops subsequent requests; a missing result stays unknown. Local checks can still report their results while network checks are skipped.

FloodWait diagnostics retain the failed TL method, any Takeout/range wrappers, the server-requested wait and the effective deadline in `telegram.backoff`. Connection details show the method and deadline while requests are paused. The diagnostic includes per-method client-call counters since that client was created; they count nested peer resolution separately, but do not count packets or Telethon's internal retry attempts. Current counters are also available as `collector.rpc_activity` in the status API. No request arguments, usernames, access hashes or exception text are included. The last diagnostic and full deadline survive restart. Earlier waits without a method record cannot be attributed retrospectively. See [export limits](https://github.com/phishdestroy/TgWitness/blob/main/docs/EXPORT-LIMITS.md) for the source review and the distinction between discovery and history acquisition.

`official_app=True` or `False` is Telegram's current-authorization flag. Neither value establishes whether the account is restricted, trusted or under observation. The existing evidence-mode `account.devices` snapshots remain the history of all signed-in devices; connection diagnostics retain only the current device description.

Before connection, advisory checks compare the API platform, language pack, device/OS and app-version formats, mobile system locale, and Telethon's actual schema layer against the reviewed catalog baseline. Warnings appear in the server log and account status metadata; they never replace imported values or change the schema layer. A different layer is a compatibility review signal, not proof of a broken or restricted account. These checks and `official_app` do not certify that Telegram considers the account safe from restrictions. Disconnected account status uses the saved profile instead of generating another device description.

כדי להשתמש במקום זאת ביישום משלכם (החשבון שרושם אותו הוא זה שנמצא בסיכון; ראו " [מדוע מאגר API מובנה?](https://github.com/phishdestroy/TgWitness/blob/main/docs/PROJECT-GUIDE.md#connect-a-telegram-account)"):

1. פתחו את [my.telegram.org](https://my.telegram.org) והתחברו באמצעות כל מספר טלפון שבבעלותכם. הקוד יגיע לאפליקציית טלגרם, ולא באמצעות SMS.
2. בחרו **כלי פיתוח API**.
3. יצירת יישום: כל כותרת ושם קצר (5–32 אותיות), פלטפורמה: **שולחן עבודה**. ניתן להשאיר את שדה ה-URL והתיאור ריקים.
4. העתיקו **את ה-api_id של האפליקציה** (מספר) ואת **ה-api_hash של האפליקציה** (32 תווים הקסדצימליים).

בלוח הבקרה, תחת טופס הכניסה, מופיעים **שדות "מזהה API" ו-"Hash"**. ניתן להדביק זוג `api_id:api_hash` יחיד בשדה "**מזהה API**" ושני השדות יתמלאו. ניתן להשתמש בזוג אחד לכל החשבונות שלכם. לאחר כניסה מוצלחת, הנתונים נשמרים, מוצפנים, במרחב העבודה הספציפי הזה בלבד, ואינם נשלחים חזרה לדפדפן.

מדובר בשלושה אישורים שונים:

| סודי | נפתח | היכן ניתן למצוא אותו |
| --- | --- | --- |
| אסימון פאנל | לוח הבקרה המקוון של TgWitness | `panel-token.txt` בספריית הנתונים, או `TGWITNESS_TOKEN` |
| מזהה API + hash | אין כאן מידע בפני עצמו; מזהה את האפליקציה | זוג מובנה, הגדרות מיובאות או האפליקציה שלכם ב-my.telegram.org |
| אימות חשבון | חשבון הטלגרם | נוצר באמצעות כניסה בטלפון/QR או יובא כפעילות |

אם יש צורך לגשת ל-Telegram דרך פרוקסי, יש להגדיר זאת תחילה תחת **חשבון → הגדרות → הגדרות חיבור → שינוי נתיב החיבור**.

## מספר טלפון

1. פתחו **את החשבון**, עברו לכרטיסייה **"טלפון**" והזינו את המספר בפורמט בינלאומי, לדוגמה `+44 7700 900123`. רווחים וקווים מפרידים מוסרים באופן אוטומטי.
2. לחץ על "**המשך**". שדות "מזהה API" ו-"Hash" יכולים להישאר ריקים.
3. הזן את הקוד ש-Telegram שולח (בדרך כלל לאפליקציית Telegram; אין ערובה לקבלת ה-SMS).
4. אם לחשבון יש אימות דו-שלבי, הזן את הסיסמה הזו. זו אינה אסימון הפאנל ואינה קוד הגישה למכשיר.
5. בדקו את מזהה החשבון המופיע לאחר הכניסה, ולאחר מכן בחרו מקורות.

קודי הכניסה והסיסמה ל-2FA לעולם אינם נשמרים בדיסק.

## קוד QR

יש להשתמש בכך כאשר החשבון כבר מחובר בטלפון או במחשב אחר.

1. לשונית **"קוד QR**" → **הצג קוד QR**. שדות "מזהה API" ו-"Hash" יכולים להישאר ריקים.
2. במכשיר שבו אתה מחובר: **הגדרות → מכשירים → קישור למכשיר שולחני**, סרוק את הקוד ואשר.
3. הזן את סיסמת ה-2FA ב-TgWitness אם Telegram מבקש זאת.

תמונת ה-QR נוצרת באופן מקומי. לקודים יש תוקף; לחץ על "**צור קוד QR נוסף"** כדי לנסות שוב. נעילת הלוח, מעבר לסביבת עבודה אחרת או התחלת כניסה נוספת מבטלת קוד בהמתנה.

## מפתח אימות + מזהה DC

מפתח אימות (Auth Key) הוא מפתח האימות הגולמי בן 256 בתים העומד בבסיס כל הפעלה של טלגרם, הכתוב **כ-512 תווים הקסדצימליים**, יחד עם מספר מרכז הנתונים **DC 1–5**.

1. **מפתח אימות** Tab. הדביקו את המפתח המלא; מפתח מקוצר המכיל את `…` לא יפעל.
2. בחר את מזהה ה-DC שסופק עם המפתח.
3. ניתן להזין את **מזהה המשתמש (User ID**). במקרה כזה, TgWitness יסרב להתחבר אם Telegram מדווח על חשבון שונה.
4. **חשבון** Press **Connect**.

מפתח אימות (512 תווים) אינו חתימת API (32 תווים). ניתן גם לייבא את אותו המפתח כקובץ JSON; ראו [JSON של החשבון](https://phishdestroy.github.io/TgWitness/he/docs/reference/accounts/#account-json).

## קובצי חשבונות

פתח את **"הוסף חשבון" →**"**קבצים**" ובחר עד **ארבעה קבצים השייכים לחשבון אחד**, בהיקף כולל של **8 MiB**, ולאחר מכן לחץ על "**חבר חשבון**".

The **Files**, **Auth key** and bulk-import forms show the parallel-session warning before connecting. By default imported authorizations are reused. Keep the original client closed while its key is in use here. **Files** and **Auth key** also offer **Create an independent authorization**, described below. Bulk import still uses the direct mode. Phone and interactive QR login create separate authorizations. The warning heading stays visible in the import form; its full explanation opens automatically when files or a key/session string are supplied. It can be collapsed after reading, so the file picker and connection controls remain usable on a phone.

- הקבצים מומרים **בזיכרון** בשרת ה-TgWitness שלכם. הקבצים המועלים אינם נשמרים, קבצי ZIP אינם נפרקים לדיסק ואין יצירת קשר עם שירות חיצוני כלשהו.
- הפעילות שהתקבלה נבדקת לאחר מכן מול טלגרם. אם קובץ מציין מזהה משתמש, עליו להתאים לחשבון שטלגרם מדווח עליו.
- קובצים המתארים חשבונות שונים או פרטי הזדהות שונים ל-API נדחים במקום לבחור באחד מהם.
- שדה **"Passcode" או "session text"** מכיל את שדה הסיסמה המקומית של TData, תיבה להדבקת StringSession **וקריאת קבצים ללא צורך בהתחברות** (ממלא את הטופס מבלי ליצור קשר עם Telegram).

### Create an independent authorization

Select **Create an independent authorization** before connecting imported files or an Auth Key. TgWitness connects the imported donor briefly, uses it to approve the new client's QR login token, and disconnects the donor immediately after approval. The new client has its own authorization key and a separately selected Desktop profile. The donor's supplied API credentials and device profile are used only for the donor connection. No existing authorization is logged out or revoked.

**Keep the donor's original client fully closed during this step.** The initial connection still uses its copied key, so this mode cannot remove that initial parallel-use risk. Once the new authorization is connected, the owner can reopen the original client and use both independently. Interactive **QR code** login lets the original client approve the login without copying or connecting its key here.

If Telegram requests 2FA, this mode uses `twoFA` from the selected JSON when present, or asks for the password. A rejected imported password returns to the password form. Passwords are not saved. The candidate key is saved encrypted in `independent_login.enc`, including changes during data-centre migration. After an interruption, select the same donor and this option to resume the saved candidate. The workspace remains reserved for that account; failed completion does not delete the new workspace. Keep its data directory and vault key. The final credentials and `account.authorized` journal record include the import method, input formats and donor API ID, without the donor key or password.

On 5 November 2026, a dedicated account passed live checks with Telethon, Pyrogram and TData donors: 2FA completion, distinct new authorization keys, concurrent access by the donor and new client, and reading a public channel. The Telethon case also resumed a saved candidate after an interruption at the password step. Each new authorization completed the six post-login initialization requests, and its signed journal verified. The original session remained usable in all four supplied formats.

Telegram's [RPC error database](https://core.telegram.org/api/errors.json) associates `FRESH_CHANGE_ADMINS_FORBIDDEN` with changing admins, `FRESH_CHANGE_PHONE_FORBIDDEN` with changing the phone number, and `FRESH_RESET_AUTHORISATION_FORBIDDEN` with revoking other sessions, changing their lifetime or registering a passkey. `SESSION_TOO_FRESH_*` and `PASSWORD_TOO_FRESH_*` concern ownership transfers and revenue or gift withdrawals. These are not collection operations; a new login does not imply a blanket 24-hour reading ban. Export can separately return `TAKEOUT_INIT_DELAY_*`. TgWitness retains server-requested pauses and does not retry token acceptance automatically or revoke sessions to work around restrictions.

### Telethon `.session`

|  |  |
| --- | --- |
| מה זה | מסד הנתונים SQLite שהכלים המבוססים על Telethon יוצרים, לדוגמה `my_account.session` |
| מוכר על ידי | טבלאות `sessions` (יחד עם `dc_id`, `server_address`, `port`, `auth_key`) ו-`version` = 7 או 8 |
| דרישות | שורה אחת בדיוק של הפעלה מורשית; מסד נתונים סגור ומלא |

סגור תחילה את התוכנית שיצרה את הקובץ. אם `my_account.session-journal` או `my_account.session-wal` קיימים לצדו, מסד הנתונים אינו סופי: פתח ו סגור את הלקוח המקורי כהלכה. מחיקת קבצי ה-sidecar הללו עלולה להשאיר עותק פגום.

### Pyrogram `.session`

|  |  |
| --- | --- |
| מה זה | כלי מבוססי Pyrogram ליצירת מסד נתונים SQLite |
| מוכר על ידי | טבלה `sessions` עם `dc_id`, `auth_key`, `test_mode`, `user_id`, `is_bot`; `version` = 2 או 3 |
| דרישות | הפעלה אחת **של משתמש** מורשה ברשת הייצור. הפעלות של בוטים ו-DC לבדיקה נדחות |

מזהה המשתמש המאוחסן נבדק מול טלגרם במהלך הכניסה.

### צמד של סשן + JSON

לעתים קרובות, החשבונות מופצים כשני קבצים בעלי אותו שם, לדוגמה `447700900123.session` ו-`447700900123.json`. יש לבחור **בשניהם** בבת אחת.

- מתוך קובץ ה-JSON, TgWitness משתמש ב-`app_id`/`api_id` וב-`app_hash`/`api_hash`, כך שבדרך כלל אין צורך להזין פרטי הזדהות ל-API.
- The connection profile uses `device_model` (alias `device`), `system_version` (alias `sdk`), `app_version`, `lang_code`, `system_lang_code` (alias `system_lang_pack`), `lang_pack` and optional `tz_offset` (seconds from UTC, -43200 to 50400). Supplied fields take priority over generated defaults and the panel/browser language. Conflicting aliases are rejected. The resolved profile is saved in the encrypted workspace credentials and reused after restart, including its app version.
- `phone`, proxy settings and device tokens are **ignored**. `twoFA` is read only when **Create an independent authorization** is selected; direct import ignores it.
- A JSON without a supported authorization field is only metadata. Add its session file or continue with phone or QR login. A JSON containing a supported session or Auth Key can authorize on its own; see [Account JSON](https://phishdestroy.github.io/TgWitness/he/docs/reference/accounts/#account-json).

### Telegram Desktop (TData)

TData היא התיקייה `tdata` של יישום Telegram Desktop (האפליקציה הרב-פלטפורמית מ-desktop.telegram.org).

| מערכת | מיקום ברירת המחדל של `tdata` |
| --- | --- |
| Windows | `%APPDATA%\Telegram Desktop\tdata` (Telegram נייד: ליד `Telegram.exe`) |
| לינוקס | `~/.local/share/TelegramDesktop/tdata` |
| macOS | `~/Library/Application Support/Telegram Desktop/tdata` |

כדי לייבא אותו:

> **Parallel session warning.** Direct TData import reuses Telegram Desktop's authorization key. Do not use that key in Desktop and TgWitness simultaneously. Telegram can invalidate the authorization with `AUTH_KEY_DUPLICATED`, leaving both copies unusable until a new login.
>
>
>
> Fully quit Desktop, including its tray process, and keep that copy closed while TgWitness uses the imported session. **Quit, do not log out or revoke the session:** revocation also invalidates the imported copy. If you need both clients running, select **Create an independent authorization** and keep Desktop closed until the new login succeeds, or sign in to TgWitness by phone or QR. A dedicated account is recommended, but does not make cloned keys safe to use in parallel.
>
>
>
> זה חל גם על קבצי `.session` מיובאים, טקסט StringSession ומפתח אימות HEX. לקוחות אחרים בעלי אישורים שנוצרו באופן עצמאי יכולים להישאר מחוברים. ראו [את התיעוד של Telegram בנושא AUTH_KEY_DUPLICATED](https://core.telegram.org/api/errors#406-not-acceptable).

1. סגור את Telegram Desktop לחלוטין.
2. צרו קובץ ZIP המכיל **רק** את שני הפריטים הבאים מ-`tdata`:

   - `key_datas`
   - הקובץ בן 16 התווים המסתיים ב-`s` שלצדו, בדרך כלל `D877F783D5D3EF8Cs`

   דחיסת התיקייה כולה עם מטמון המדיה שלה חורגת בדרך כלל מהמגבלות (512 רשומות, 32 MiB לאחר הפריקה). 3. בחרו את קובץ ה-ZIP ב**"קובצים**". אם ל-Telegram Desktop יש **קוד גישה מקומי**, הזינו אותו תחילה בשדה **"קוד גישה" או "טקסט הפעלה"**. זהו לא סיסמת ה-2FA.

נתמך: חשבון אחד לכל ארכיון, אחסון מודרני מסוג `key_datas`/`key_data0`/`key_data1`, קוד גישה מקומי. לא נתמך: תיקיות עם מספר חשבונות מחוברים, פריסות שולחן עבודה ישנות יותר, קובצי ZIP המוגנים בסיסמה, והאפליקציה המקורית הנפרדת של macOS "Telegram for macOS".

### Telethon StringSession

שורת טקסט אחת, המתחילה בדרך כלל ב-`1` ואורכה כ-350 תווים. טען אותה כקובץ `.txt` או `.tgwitness-session` (בגודל של עד 4 KiB), או הדבק אותה תחת **"קוד גישה" או "טקסט הפעלה**". מתקבלות רק מחרוזות Telethon; מחרוזות Pyrogram ו-TDLib משתמשות בפורמטים שונים.

### קובץ JSON של החשבון

אובייקט JSON אחד, בגודל של עד **64 KiB**, בקובץ שמסתיים ב-**`.json`**.

| שדה (כינויים) | משמעות |
| --- | --- |
| `api_id` (`app_id`) | מזהה היישום, מספר חיובי |
| `api_hash` (`app_hash`) | ה-hash של היישום, 32 תווים הקסדצימליים |
| `string_session` (`session_string`, `session_str`; legacy `session`) | טקסט של Telethon StringSession, לא שם קובץ |
| `auth_key` (`auth_key_hex`) + `dc_id` | מפתח אימות מלא בן 512 תווים ו-DC 1–5 |
| `user_id` (`id`) | אופציונלי; נבדק מול טלגרם לפני שמירת ההרשאה |
| `device_model` (`device`) | Connection device description |
| `system_version` (`sdk`) | Connection OS version |
| `app_version` | Application version sent to Telegram |
| `lang_code`, `system_lang_code` (`system_lang_pack`), `lang_pack` | Client language, system language and client language pack; an empty `lang_pack` is allowed |
| `tz_offset` | Optional UTC offset in seconds, sent in `initConnection.params`; integer or decimal integer string |

If both an alias and the main name are present, they must agree. Explicit Telethon session fields take priority over a generic `session` blob in another format. If both contain recognizable Telethon sessions, they must describe the same authorization. Without an explicit field, `session` must be a valid Telethon StringSession. Examples:

```
{ "app_id": 1234567, "app_hash": "0123456789abcdef0123456789abcdef" }
```

```
{
  "api_id": 1234567,
  "api_hash": "0123456789abcdef0123456789abcdef",
  "auth_key": "REPLACE_WITH_ALL_512_HEXADECIMAL_CHARACTERS",
  "dc_id": 2,
  "user_id": 123456789
}
```

בדוגמה הראשונה יש למלא רק את פרטי הזיהוי של ה-API; התחברו באמצעות טלפון או QR, או הוסיפו קובץ הפעלה. רשימות מרוכזות (מערך JSON של חשבונות) אינן מתקבלות.

## זהו את מה שיש ברשותכם

| אתה רואה | זהו | שימוש |
| --- | --- | --- |
| `*.session`; פתיחתו בעורך טקסט מציגה את `SQLite format 3` בראש העמוד | Telethon או Pyrogram SQLite | **קבצים** (שזוהו באופן אוטומטי) |
| תיקייה בשם `tdata` המכילה את `key_datas` | Telegram Desktop TData | דחיסת שני קבצים ב-ZIP, ולאחר מכן **'קבצים'** |
| שורה אחת של טקסט המתחילה ב-`1`, כ-350 תווים | Telethon StringSession | **קבצים** |
| `*.json` עם `app_id`/`app_hash` | מטא-נתונים נלווים | **קובצים**, יחד עם ההפעלה שלהם |
| `*.json` עם `auth_key` או `string_session` | קובץ JSON של החשבון | **קבצים** |
| 512 תווים `0-9a-f` | מפתח אימות | **מפתח אימות** |
| 32 תווים `0-9a-f` | ה-hash של ה-API | **מזהה API + Hash** |
| `td.binlog` או `db.sqlite` מאפליקציית TDLib | אחסון TDLib | לא נתמך |
| `123456789:AA…` | אסימון בוט | לא נתמך |

## פורמטים שאינם נתמכים

| פורמט | חלופה |
| --- | --- |
| אחסון TDLib (`td.binlog`) וייצוא TDLib | התחבר באמצעות טלפון או QR |
| **מחרוזות** הפעלה של Pyrogram | השתמשו בקובץ Pyrogram `.session`, או בטלפון/QR |
| TData עם מספר חשבונות מחוברים | התנתק מהחשבונות האחרים ב-Telegram Desktop, או השתמש בקובץ ההפעלה של כל חשבון בנפרד |
| אסימוני בוט | לא נתמך: TgWitness פועל כחשבון משתמש |
| רשימות CSV/JSON של חשבונות רבים | ייבאו קובצי סשן נתמכים דרך **חשבונות → ייבוא חשבונות**, או התחברו באמצעות טלפון/QR בסביבות עבודה נפרדות |
| Test-DC או הפעלות בוט | יש להשתמש בחשבון משתמש פעיל |

## חשבונות מרובים

לחץ על **+** ליד בורר החשבונות, או פתח **חשבון → הגדרות → הגדרות חיבור → סביבות עבודה**, הזן תווית ו התחבר.

- מספר בלתי מוגבל של סביבות עבודה, כולל הסביבה הראשית. לכל אחת מהן יש הפעלה משלה, מסלול פרוקסי , מקורות, מדיניות לכידה, יומן, מפתח חתימה, נקודות ביקורת וייצוא.
- החלפת סביבת העבודה המוצגת אינה מעכבת את האחרות.
- יומן נשאר מקושר לחשבון שיצר אותו. התחברות מחשבון אחר מחייבת סביבת עבודה נפרדת, ולא ניתן להקצות חשבון אחד לשתי סביבות עבודה.
- אסימון הלוח הראשי שולט בכל סביבות העבודה. [הגישה שהוענקה](https://phishdestroy.github.io/TgWitness/he/docs/reference/access/) יכולה להגביל משתמשים אחרים לחשבונות וצ'אטים נבחרים, עם הרשאות נפרדות ומגבלות על משך ההפעלה.
- **החשבון** משנה את שם סביבת העבודה ומוחק סביבת עבודה שנוספה, יחד עם ההפעלה, היומן, המקורות ומפתח החתימה שלה. לא ניתן למחוק את סביבת העבודה הראשית מהלוח.

### ייבוא מרובה וקבוצות חשבונות

השתמשו **ב-Accounts → Import accounts** כדי להוסיף מספר חשבונות, להתאים קבצים לפי שם בסיס ולראות את תוצאות הכניסה לכל חשבון. לכל חשבון יש סביבת עבודה משלו.

קבוצה מאגדת חשבונות קשורים מבלי למזג את הפעילויות, המפתחות או הראיות שלהם. לחיצה על "**קבוצה פתוחה"** תחת "**חשבונות"** מובילה לדף שלה בכתובת `/groups/<id>`:

- **חשבונות:** מסלול החיבור של כל חבר, תצפית והודעה אחרונה, עם "**התחל הכל"** ו-**"השהה הכל**".
- **דורש תשומת לב:** חשבונות שהתחברו החוצה, אינם זמינים או שיש בהם בעיה בחיבור, בקליטה, במקור או במדיה; כל שם מוביל לכרטיס שלו.
- **בצ'אטים של מספר חשבונות ניתן לראות:** מקורות משותפים, החשבונות העוקבים אחריהם ו הפרעות בתקופת התצפית על סביבת העבודה הזמינה (עד שבעה ימים). **ייצוא עם N חשבונות** מחלק את הייצוא של ערוץ או סופר-קבוצה ביניהם וחותם על ארכיון אחד.
- **ייצוא קבוצה:** תמונה אחת ZIP עם הייצוא החתום של כל חשבון תחת `accounts/` ו `manifest.json` ורשימה של טביעות האצבעות של ה-SHA-256 והמפתח, חתומות על ידי סביבת העבודה הראשית ב `manifest.signature.json`. יש לאמת כל ארכיון חשבון בנפרד באמצעות `python -m tgwitness.verify` ובאמצעות טביעת האצבע המהימנה של אותו חשבון.

חברי הקבוצה חולקים את הגדרות הקבוצה; חשבון יכול לשמור על הערכים שלו. ראו [הגדרות משותפות](https://phishdestroy.github.io/TgWitness/he/docs/reference/settings/#account-groups), [המדריך לייבוא ולקבוצות](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Accounts.md#import-accounts-and-share-settings) [ולוח המחוונים של מאגר ה-MTProxy](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Proxies.md#pool-dashboard-and-custom-sources).

## התנתק

**חשבון → יציאה מ-Telegram** (עם השעיית המעקב) מבקש מ-Telegram לסיים את הפעילות, כך שהיא נעלמת גם מהגדרות החשבון **→ מכשירים**, ומסירה את הפעילות מכספת סביבת העבודה. היומן, המקורות, ההגדרות ומפתח החתימה נשארים, ו היומן מתעד את היציאה. סביבת העבודה עדיין שייכת לחשבון שלה: רק אותו חשבון יכול להתחבר אליה שוב. אם טלגרם לא מגיבה, ההפעלה עדיין מוסרת מכאן והלוח מציין זאת; יש לסיים אותה בטלגרם תחת **'הגדרות' → 'מכשירים**'.

## שמירה על אבטחת קבצי החשבונות

- התייחסו לכל `.session`, TData ZIP, StringSession, מפתח אימות (Auth Key) ו-JSON של חשבון כאל סיסמה. TgWitness שומר את האישור המיובא בכספת המוצפנת שלו; תוכלו להסיר את הקבצים המקוריים לאחר מכן.
- אין להפעיל את אותה הרשאה בשתי תוכנות בו-זמנית. Telegram עלולה לבטל אותה (`AUTH_KEY_DUPLICATED`), ושתי הגרסאות יפסיקו לפעול.
- לא ניתן להחיות הפעלה שפג תוקפה או שבוטלה באמצעות המרה. התחבר שוב.

## פתרון בעיות

| הודעה או סימפטום | מה לעשות |
| --- | --- |
| *לא ניתן לקרוא את ההפעלה הזו. סגור את הלקוח המקורי שלה…* | קובץ ה-SQLite פתוח או לא גמור (קובץ נלווה מסוג `-journal`/`-wal`). סגור את התוכנית המקורית כהלכה והעתק את הקובץ שוב. |
| *סכמות SQLite נתמכות ב-Telethon: 7 ו-8* / *Pyrogram … 2 ו-3* | הקובץ נוצר בגרסת ספרייה ישנה מאוד או לא ידועה. התחבר במקום זאת באמצעות טלפון/QR. |
| *נתמכות רק הפעלות משתמשים מורשות* | קובץ ה-Pyrogram שייך לבוט או לרשת הבדיקה. |
| *ארכיון TData עולה על 512 רשומות או 32 MiB* | יש לדחוס ב-ZIP רק את הקבצים `key_datas` ו-`D877F783D5D3EF8Cs`, ולא את התיקייה כולה. |
| *לא ניתן לפענח את TData. בדוק את קוד הגישה המקומי של שולחן העבודה* | הזן את קוד הגישה המקומי של Telegram Desktop בשדה "**קוד גישה" או "טקסט הפעלה**". |
| *ייבא חשבון TData אחד בכל פעם* | ל-Telegram Desktop היו מספר חשבונות; ראו "[פורמטים שאינם נתמכים](https://phishdestroy.github.io/TgWitness/he/docs/reference/accounts/#unsupported-formats)". |
| *קובצים נבחרים מתארים חשבונות שונים או פרטי הזדהות ל-API* | בחירת קבצים מחשבון אחד בלבד. |
| *קובץ ה-JSON אינו מכיל פרטי הזדהות או הרשאות API נתמכים* | בדקו את שמות השדות בקובץ [ה-JSON של החשבון](https://phishdestroy.github.io/TgWitness/he/docs/reference/accounts/#account-json). |
| *מטא-נתוני API בלבד* | ל-JSON אין סשן. הוסף את הקובץ `.session` או השתמש בטלפון/QR. |
| *מפתח האישור (Auth Key HEX) חייב להכיל את כל 512 התווים ההקסדצימליים* | המפתח קטוע או מכיל את האותיות `…`. |
| מזהה החשבון אינו תואם לחשבון שיובא | מזהה המשתמש בקובץ שונה מזה ש-Telegram מדווח עליו; הקובץ מיועד לחשבון אחר. |
| החשבון כבר שייך לסביבת עבודה אחרת | פתח את סביבת העבודה הזו במקום להוסיף את החשבון פעמיים. |
| קשור, אך חסרה קבוצה פרטית מרשימת הצ'אטים תחת "**מקורות"** | בדוק את החברות. הבוחר בודק את 1,000 השיחות הראשונות; הגדל את המגבלה תחת **"פרמטרים"**. |
| החיבור באמצעות פרוקסי נכשל | בדקו את מצב הניתוב וה-IP. ניסיון אוטומטי MTProxy מנסה כניסה אחרת שעובדת. "הסתר את כתובת ההמתנה"; "ישיר" (Direct) כפתרון אחרון יכול להתחבר ישירות לאחר העיכוב שהוגדר. ראו [מצבי ניתוב](https://phishdestroy.github.io/TgWitness/he/docs/reference/connection/#ip-modes). |

ראו גם: [חיבור ואבטחה](https://phishdestroy.github.io/TgWitness/he/docs/reference/connection/) עבור פרוקסי והצפנה, [וכיצד מתבצע האיסוף](https://phishdestroy.github.io/TgWitness/he/docs/reference/collection/) של הנתונים הנלכדים לאחר הכניסה למערכת.
