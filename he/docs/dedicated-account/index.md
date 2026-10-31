# השתמשו בחשבון נפרד. לעולם לא בחשבון הראשי שלכם.

Canonical page: https://phishdestroy.github.io/TgWitness/he/docs/dedicated-account/

קראו לפני שתחברו חשבון

העצה שלנו שלא להשתמש בחשבון הראשי שלכם אינה בדיחה. זו המציאות.

חשבון ראשי

- ה-hash של האפליקציה שלכם: 99% יצאו מהחשבון
- השעיות רק בגלל רמת אמון נמוכה הן תופעה שכיחה
- השימוש בו הוא רעיון ממש טיפשי

חשבון נוסף בזוגות ציבוריים

- יותר ממיליון חשבונות נרשמו באמצעות זוגות אלה
- הצמדים פעילים כבר יותר מ-5 שנים
- אף אחד לא יכול לראות שום דבר ששייך לכם דרכם

01

## למה לא החשבון הראשי שלך?

זהו מידע מדויק. אנו יודעים בדיוק היכן טמונות המלכודות של בעיות אלה.

1. ### ה-hash של האפליקציה שלכם: 99% יצאו מהחשבון

   כניסה ל-my.telegram.org מחשבון שאין לכם גישה אליו, כדי להשיג hash של האפליקציה, ולאחר מכן כל בקשה באמצעות ה-hash הזה, פירושה סיכוי של 99% שהחשבון יצא מהמערכת. אתם יכולים לבדוק זאת.
2. ### השעיות רק בגלל רמת אמון נמוכה הן תופעה שכיחה

   חשבונות נחסמים פשוט משום ש-Telegram אינה סומכת עליהם, ואיסורים מסוג זה מתרחשים לעתים קרובות. גם את זה תוכלו לבדוק. השימוש בחשבון שלכם הוא רעיון ממש טיפשי.
3. ### ניתן לבטל מפתחות הפעלה שהועתקו

   הפעלה בו-זמנית של מפתח TData/session מיובא ב-Telegram Desktop וב-TgWitness עלולה לגרום לשגיאת `AUTH_KEY_DUPLICATED`. Telegram מבטל את האישור הזה, ולכן שתי העותקים זקוקים לכניסה מחדש. חשבון ייעודי אינו מונע זאת.

   סגרו לחלוטין את הלקוח המקורי והשאירו אותו סגור בזמן השימוש בהפעלה המיובאת שלו. לשימוש מקביל, התחברו ל-TgWitness באמצעות טלפון או QR כדי ליצור אישור נפרד; לקוחות אחרים בעלי אישור נפרד יכולים להישאר מחוברים.

   [קראו את אזהרת ייבוא ההפעלה](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=he#session-warning)

תיעוד Telegram

- [שגיאות יציאה: AUTH_KEY_UNREGISTERED, SESSION_REVOKED](https://core.telegram.org/api/errors)
- [יצירת חתימת האפליקציה שלכם: קבלת ה-api_id](https://core.telegram.org/api/obtaining_api_id)

02

## מדוע TgWitness פועל באמצעות זוגות של חתימת האש (hash) ו-ID של האפליקציה הציבורית

זו הסיבה שבנינו את TgWitness על זוגות hash/app ID של אפליקציות ציבוריות. לפי ההיגיון שלנו, הסיכוי לחסימות נמוך יותר איתם: יותר ממיליון חשבונות טלגרם נרשמו באמצעות זוגות אלה, ותוכניות רבות ושונות פועלות דרכם. לפי ההיגיון שלנו, זה עדיף על עבודה ישירה עם חתימת האפליקציה האישית: זוגות אלה קיימים בוודאות כבר יותר מחמש שנים.

### זוג חדש משלכם

נוצר ב-my.telegram.org מהחשבון.

- כ-99% מהחשבונות יצאו מהמערכת
- יישום אחד חדש, חשבון אחד

### זוגות ציבוריים של המאגר

אותם זוגות המשמשים תוכניות רבות.

- יותר ממיליון חשבונות רשומים
- תוכניות רבות ושונות
- עובד בתחום מזה 5 שנים ויותר

### מדוע אף אחד לא יכול לראות דבר מכם באמצעות זוגות אלה

- #### הצמד הוא שם, לא מפתח

  Telegram מבקש את מזהה ה-API ואת ה-hash של ה-API כאשר תוכנית מתחברת וכאשר היא מבקשת קוד כניסה. הם מזהים את היישום ואינם מעניקים גישה לשום חשבון; בתיעוד של Telethon מצוין שזוג אחד עובד עם כל מספר טלפון.
- #### מפתח ההפעלה שלכם לעולם אינו עוזב את השרת שלכם

  הכניסה יוצרת מפתח אישור באמצעות חילופי Diffie–Hellman בין ה-TgWitness שלכם ל-Telegram; המפתח עצמו לעולם אינו נשלח. תיעוד Telegram: לאחר האישור, המפתח נקשר למשתמש, וכל קריאה עם מפתח זה פועלת בשם אותו משתמש. לתוכניות אחרות עם אותו זוג מפתחות יש מפתחות משלהן והן אינן יכולות להשתמש במפתח שלכם.
- #### התעבורה מוצפנת באמצעות המפתח שלכם

  כל בקשה ותשובה מוצפנות באמצעות מפתח האישור של ההפעלה, ולא באמצעות ה-hash של ה-API. ידיעת ה-hash של ה-API אינה מאפשרת לפענח דבר.
- #### בעל הזוג אינו רואה דבר

  ל-Telegram אין שיטה המפרטת חשבונות, הפעלות או הודעות לפי מזהה API. בעל זוג חשבונות רואה רק את הגדרות האפליקציה שלו ב-my.telegram.org.
- #### רק החשבון שלכם רואה באיזו אפליקציה מדובר

  ההגדרות → מכשירים בחשבון שלכם מפרטות את שם האפליקציה ומזהה ה-API של כל הפעלה, את המכשיר, כתובת ה-IP והתאריכים. אף אחד אחר אינו מקבל רשימה זו.

תיעוד Telegram

- [אישור משתמש: המפתח הופך למשתמש](https://core.telegram.org/api/auth)
- [auth.sendCode: api_id, api_hash](https://core.telegram.org/method/auth.sendCode)
- [initConnection](https://core.telegram.org/method/initConnection)
- [יצירת מפתח אישור](https://core.telegram.org/mtproto/auth_key)
- [הצפנת MTProto](https://core.telegram.org/mtproto/description)
- [account.getAuthorizations](https://core.telegram.org/method/account.getAuthorizations)
- [מה מכיל תיעוד הפעלה](https://core.telegram.org/constructor/authorization)
- [קבלת api_id](https://core.telegram.org/api/obtaining_api_id)
- [קוד המקור הפתוח של אפליקציות Telegram](https://telegram.org/apps#source-code)

ספריות ודיונים

- [Telethon: כניסה](https://docs.telethon.dev/en/stable/basic/signing-in.html)
- [opentele: ממשקי API של האפליקציה הרשמית](https://opentele.readthedocs.io/en/latest/documentation/authorization/api/)
- [opentele: TelegramClient](https://opentele.readthedocs.io/en/latest/documentation/telethon/telegramclient/)
- [Stack Overflow: האם יש לשמור את ה-api_hash בסוד?](https://stackoverflow.com/questions/49490818/should-telegram-api-hash-be-kept-secret)

### אותם זוגות בתוכניות אחרות 7

צמדי האפליקציות הרשמיות של טלגרם (Telegram) הם ציבוריים ומשולבים בתוכניות וספריות עצמאיות רבות:

- [opentelePython · src/api.py](https://github.com/anmv/opentele/blob/4df17bd8c443d6452afc5a2d29ec7922fad1a5c3/src/api.py#L575)

  - Desktop 2040
  - Android 6
  - Telegram X 21724
  - iOS 10840
  - macOS 2834
  - Web 2496
- [opentele2Rust · opentele2-core/src/api.rs](https://github.com/DedInc/opentele2/blob/7e973bc71cd7a714ad13ac703c0895a90d36a735/crates/opentele2-core/src/api.rs#L641)

  - Desktop 2040
  - Android 6
  - Telegram X 21724
  - iOS 10840
  - macOS 2834
  - Web 2496
- [GrampoPython · Grampo/ut/api.py](https://github.com/abbas-bachari/Grampo/blob/00aa662d853c4ac2180432371c5e0d9444bbfe9e/Grampo/ut/api.py#L526)

  - Desktop 2040
  - Android 6
  - Telegram X 21724
  - iOS 10840
  - macOS 2834
  - Web 2496
- [tgmanagePython · api/schemas/api_app.py](https://github.com/xdsnich/tgmanage/blob/f67c46be0ab234bd04526a8663d3936bd98a8597/api/schemas/api_app.py#L47)

  - Android 6
  - iOS 8
  - Desktop 2040
  - macOS 2834
  - Telegram X 21724
  - Web K 2496
- [LyChatBotTDLib · helpers/tdlib/index.js](https://github.com/LyoSU/LyChatBot/blob/fac0ae5d5f2cddb8a26312014f51c0f6f40ec191/helpers/tdlib/index.js#L11)

  - macOS 2834
- [hsadasdPython · config.py](https://github.com/herobrinovaleksandr-png/hsadasd/blob/6842c74895038c16e219324fcd07dbe8153f37f0/config.py#L68)

  - Desktop 2040
  - Desktop 17349
  - Telegram X 21724
  - macOS 2834
  - iOS 10840
  - Web 2496
  - +4
- [blb.teamblb.team/threads/…294](https://blb.team/threads/app-hash-app-id-ofitsial-nykh-kliyentov.294/)

  - Android 4 · 5 · 6
  - iOS 8
  - Desktop 2040
  - Desktop 17349
  - macOS 2834
  - Telegram X 21724

  רשימת זוגות האפליקציות הרשמיות בפורום, שפורסמה לצורך רישום חשבונות

03

## דרכים ליצירת חשבון נוסף

חשבון Telegram זקוק למספר טלפון לקבלת קוד הכניסה. בחרו בהתאם למשך הזמן שהחשבון אמור להיות פעיל.

- הבחירה הטובה ביותר

  ### SIM מראש או eSIM

  ********

  אחרון

  כל עוד אתם דואגים למלא את החשבון

  שימו לב

  האמין ביותר: Telegram מקבל בצורה הטובה ביותר מספרי טלפון ניידים אמיתיים. מספר שהמפעיל מחזיר מועבר למישהו אחר.
- ### אפליקציית מספרים וירטואליים

  ********

  אחרון

  בעוד שהאפליקציה שומרת על המספר

  שימו לב

  Telegram עשויה לדחות מספר וירטואלי, לא לשלוח את הקוד או להגביל את החשבון החדש באופן מיידי; אפליקציות מסוימות מחזירות מספרים שאינם בשימוש.
- ### השכרת מספרים

  ********

  אחרון

  תקופת ההשכרה

  שימו לב

  כאשר זה מסתיים, המספר עובר ללקוח הבא.
- ### הפעלה חד-פעמית

  ********

  אחרון

  קוד אחד

  שימו לב

  המספר חוזר למאגר באופן מיידי, לעתים קרובות עם היסטוריה של בעלים קודמים. הגדירו את סיסמת הענן לפני כל דבר אחר.

מי שיחזיק במספר בהמשך יוכל לבקש קוד כניסה. סיסמת ענן (אימות דו-שלבי) מונעת ממנו להתחבר; בלעדיה, החשבון שייך לבעלים הבא של המספר.

תיעוד Telegram

- [שאלות נפוצות בנושא ספאם: מספרי טלפון וירטואליים ובעלים קודמים](https://telegram.org/faq_spam)
- [אימות דו-שלבי](https://core.telegram.org/api/srp)

### מספרי +888 מושכרים (Fragment)

ישנם זירות מסחר ושירותים המציעים השכרה זמנית של מספרי +888 הרשמיים של טלגרם מ-Fragment.

מחיר משוער: 20 דולר ארה"ב ליום.

- ניתן לרשום חשבון ישירות ב-Telegram Web או ב-Telegram Desktop.
- ניתן למחוק חשבונות במספר זה וליצור חשבונות חדשים.
- חשבונות אלה נתונים בדרך כלל לפחות בדיקות למניעת הונאה, אך הם אינם מעניקים חסינות או זכויות מיוחדות.

המספר אינו שייך לכם. לאחר תום תקופת ההשכרה, הבעלים יכול לדרוש אותו בחזרה. הגדירו סיסמת ענן מיד ואל תתייחסו לחשבון כאל חשבון לטווח ארוך.

החזקת מספר ה-+888 בעצמכם או שימוש בכרטיס SIM מראש תשלום הנמצא בשליטתכם נותרת האפשרות האמינה ביותר.

### חשבונות מוכנים משווקים מקוונים

בכמה פלטפורמות מסחר (למשל G2G או Z2U) נמכרים חשבונות Telegram מוכנים — חדשים, ותיקים או עם קבצי הפעלה.

- [G2G: רשימות חשבונות טלגרם](https://www.g2g.com/uk/categories/telegram-accounts)
- [Z2U: רשימות חשבונות טלגרם](https://www.z2u.com/telegram/accounts-5-15140)

לעולם אל תשתמשו בחשבון הראשי שלכם! חשבון ייעודי שנוצר בדרך זו עדיין בטוח יותר מאשר להזין את חשבון הטלגרם הראשי שלכם ל-TgWitness.

#### אזהרות לפני הרכישה

- פעולה זו מהווה הפרה של תנאי השימוש של טלגרם.
- חשבונות רבים נרשמו בהמוניהם (רישום אוטומטי) או שההיסטוריה שלהם אינה ידועה.
- ייתכן שעדיין יש למוכרים מסוימים גישה לשחזור.
- חשבונות משווקים כאלה נחסמים או מוגבלים לעתים קרובות בהמשך.
- הימנעו מאתרי מסחר המוכרים בגלוי תוכנות גניבה, כלי פישינג או חשבונות שנגנבו בבירור.
- רכישת חשבון — אפילו כזה המפורסם כ"רישום אוטומטי" — מפלטפורמות המוכרות בגלוי כלי פישינג, תוכנות גניבה, הפעלות גנובות או חשבונות, מהווה הפרה לא רק של תנאי השימוש של טלגרם, אלא גם של החוקים ברוב המדינות. דבר זה עלול לפסול את הראיות שלכם בהמשך. בחרו בזהירות.

#### אם אתם משתמשים באפשרות זו

1. התייחסו לחשבון כאל חשבון חד-פעמי.
2. סיום כל הפעילויות האחרות, הגדרת סיסמת ענן ושינוי שיטות השחזור באופן מיידי.
3. השתמש ב-2–3 חשבונות מספקים שונים או בחשבונות שרשמת בעצמך.

**Premium, מחיקה והעיכוב של שבעה ימים**

אם לחשבון יש מנוי Premium, מי שיש לו גישה למספר הטלפון לא יוכל למחוק את החשבון באופן מיידי. תקבל הודעה ויהיו לך שבעה ימים לפני המחיקה.

זה חשוב מכיוון שהחקירה שלך תלויה בחשבון: יש לך זמן להכין תחליף.

**חשבונות חדשים ופרטי הזדהות ל-API**

אם תשיגו ותשתמשו ב-api_id/api_hash משלכם מחשבון חדש שרשמתם בעצמכם באמצעות מספר משירות SMS, החשבון ינותק מהמערכת בבקשת ה-API הראשונה או באישור ההפעלה הראשון. קחו זאת בחשבון בעת תכנון חקירה.

04

## יצירת החשבון

ממספר ועד הצ'אט הראשון שנרשם.

1. ### קבלו מספר

   כרטיס SIM מראש תשלום או eSIM כאשר החשבון צריך להיות פעיל לאורך זמן; כרטיס שכור או הפעלה חד-פעמית למשימה קצרה. השירותים מפורטים להלן.
2. ### הירשמו בנפרד מהחשבון הראשי שלכם

   הירשמו באפליקציית Telegram הרשמית במכשיר נפרד, באמולטור או בפרופיל טלפון, ולא לצד החשבון הראשי שלכם.
3. ### נעלו אותו באמצעות סיסמת ענן

   הגדירו מיד סיסמת ענן וכתובת דוא"ל לשחזור שאינן בשימוש בשום מקום אחר.
4. ### סגרו את הגדרות הפרטיות

   מספר טלפון **"אף אחד**", "מצא אותי לפי המספר שלי", "**אנשי הקשר שלי**", "נראה לאחרונה", "תמונות פרופיל" ו"ביוגרפיה" – **"אף אחד**" או "**אנשי הקשר שלי**"; כבו את סנכרון אנשי הקשר.
5. ### יש למנוע את השמדתו העצמית

   הגדירו את השמדת החשבון העצמית לתקופה הארוכה ביותר, כך ש-TgWitness שהופסק לא יעלה לכם בחשבון.
6. ### הקפידו על פרופיל ניטרלי

   אין להשתמש בשמות, תמונות, שמות משתמש או ביוגרפיות מחשבונות אחרים שלכם, ואין להשתמש באנשי קשר אישיים.
7. ### תנו לזה להתחמם

   הצטרפו בתחילה לכמה צ'אטים ביום. חשבונות חדשים שממהרים מוגבלים תחילה.
8. ### אל תשתפו דבר עם בוטים

   לעולם אל תלחצו על "שתף מספר טלפון" או "שתף מיקום" עבור בוט. פתחו קישורים ומיני-אפליקציות דרך VPN או פרוקסי באותו מכשיר.
9. ### חברו אותו ל-TgWitness

   בסביבת העבודה של האפליקציה, התחברו דרך **'חשבון' → 'קוד QR**', ולאחר מכן לחצו על **'מקורות' → 'מצב חקירה**'. האפליקציה היא המקום שבו אתם פועלים, ו-TgWitness הוא התיעוד.

תיעוד Telegram

- [אימות דו-שלבי](https://core.telegram.org/api/srp)
- [הגדרות פרטיות](https://core.telegram.org/api/privacy)
- [השמדה עצמית של חשבון](https://core.telegram.org/method/account.setAccountTTL)

05

## מספר שירותים

אפשרויות להתחלה. מדינות, מחירים והאם Telegram מאפשרת שינוי מספר משתנים לעתים קרובות; יש לבדוק לפני התשלום.

### SIM מראש תשלום ו-eSIM 11

- [SMARTYsmarty.co.uk](https://smarty.co.uk)

  - UK
  - SIM
- [VOXIvoxi.co.uk](https://www.voxi.co.uk)

  - UK
  - SIM
- [iD Mobileidmobile.co.uk](https://www.idmobile.co.uk)

  - UK
  - SIM
- [Threethree.co.uk](https://www.three.co.uk)

  - UK
  - SIM
- [Asda Mobilemobile.asda.com](https://mobile.asda.com)

  - UK
  - SIM
- [Ultra Mobileultramobile.com](https://www.ultramobile.com)

  - US
  - תשלום מראש

  תוכנית PayGo, זולה מאוד
- [US Mobileusmobile.com](https://www.usmobile.com)

  - US
  - תשלום מראש
- [Mint Mobilemintmobile.com](https://www.mintmobile.com)

  - US
  - תשלום מראש
- [Tracfonetracfone.com](https://www.tracfone.com)

  - US
  - תשלום מראש
- [eSIM Plusesimplus.me](https://esimplus.me)

  - eSIM
- [Numero eSIMnumeroesim.com](https://numeroesim.com)

  - eSIM

### אפליקציות למספרי טלפון וירטואליים 20

- [Google Voicevoice.google.com](https://voice.google.com)

  - US

  בארה"ב בלבד; ההרשמה דורשת מספר טלפון אמריקאי
- [TextNowtextnow.com](https://www.textnow.com)

  - US
  - CA

  המספר יוחזר אם לא תשתמש בו
- [TextFreetextfree.us](https://www.textfree.us)

  - US
- [2ndLine2ndline.co](https://www.2ndline.co)

  - US
  - CA
- [Talkatonetalkatone.com](https://www.talkatone.com)

  - US
- [TextMego-text.me](https://go-text.me)

  - US
  - CA
  - מדינות אחרות
- [textPlustextplus.com](https://textplus.com)

  [Google Play](https://play.google.com/store/apps/details?id=com.gogii.textplus)
- [FreeToneGoogle Play](https://play.google.com/store/apps/details?id=com.textmeinc.freetone)

  - US

  [TextMe Up · textmeup.com](https://www.textmeup.com)
- [Nextplusnextplus.me](https://nextplus.me)

  - US
- [Dingtonedingtone.me](https://www.dingtone.me)

  - US
  - CA
- [Burnerburnerapp.com](https://www.burnerapp.com)

  - US
  - CA
  - בתשלום

  עם תקופת ניסיון
- [Hushedhushed.com](https://hushed.com)

  - מדינות רבות
  - בתשלום

  זול
- [Sidelinesideline.com](https://www.sideline.com)

  - US
- [MySudomysudo.com](https://mysudo.com)

  - US
  - CA
  - UK
- [2NumberGoogle Play](https://play.google.com/store/apps/details?id=com.bpmobile.second.phone)

  [App Store](https://apps.apple.com/app/id1216135390)
- [SLYNUMBERslynumber.com](https://slynumber.com)

  [Google Play](https://play.google.com/store/apps/details?id=com.dev.slynumber)
- [Phonerphonerapp.com](https://phonerapp.com)
- [Onoffonoff.app](https://www.onoff.app)

  - EU

  מספרי טלפון ניידים אירופיים באפליקציה
- [Sonetelsonetel.com](https://sonetel.com)

  - מדינות רבות
  - מספר חינם
- [Zadarmazadarma.com](https://zadarma.com)

  - מדינות רבות

  מספרים וירטואליים

### מספר השכרות והפעלות: 12

השכרה שומרת על מספר במשך שבועות או חודשים. הפעלה חד-פעמית מספקת קוד יחיד: הגדירו את סיסמת הענן מיד לאחר ההרשמה.

- [OnlineSimonlinesim.io](https://onlinesim.io)

  - השכרה
  - הפעלות
- [SMSPVAsmspva.com](https://smspva.com)

  - השכרה
  - הפעלות
- [5SIM5sim.net](https://5sim.net)

  - השכרה
  - הפעלות
- [SMSPoolsmspool.net](https://www.smspool.net)

  - השכרה
  - חד-פעמי
- [VAK-SMSvak-sms.com](https://vak-sms.com)

  - השכרה
  - הפעלות
- [TextVerifiedtextverified.com](https://www.textverified.com)

  - השכרה
  - הפעלות
- [JuicySMSjuicysms.com](https://juicysms.com)

  - השכרה
  - הפעלות
- [365SMS365sms.org](https://365sms.org)

  - השכרה
  - הפעלות
- [SIMSMSsimsms.org](https://simsms.org)

  - השכרה
  - הפעלות
- [GrizzlySMSgrizzlysms.com](https://grizzlysms.com)

  - חד-פעמי
- [SMS-MANsms-man.com](https://sms-man.com)

  - חד-פעמי
- [Tiger SMStiger-sms.com](https://tiger-sms.com)

  - חד-פעמי
