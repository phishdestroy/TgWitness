# פריסה ברמת אבטחה גבוהה

Canonical page: https://phishdestroy.github.io/TgWitness/he/docs/reference/high-assurance/

שרת מאובטח הפועל 24/7 ב-Hetzner או ב-Phala Cloud, Gateway DNS ובדיקות שצד שלישי יכול לחזור עליהן.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [תיעוד](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [פריסה ושחזור](https://phishdestroy.github.io/TgWitness/he/docs/reference/deployment/)

![פריסה ושחזור](https://phishdestroy.github.io/TgWitness/assets/chapter-operate.svg)

פריסה ברמת אמינות גבוהה מוסיפה בדיקות עצמאיות של סביבת האיסוף לאימות הארכיון. הבודק בודק את רשומות הפריסה והגישה המוחזקות בידי ספק הענן ו-Cloudflare, ופריסת Intel TDX מוסיפה אימות חומרה של סביבת האספן.

השימוש הרגיל בסביבה מקומית וב-Docker נותר ללא שינוי. שום דבר כאן לא פועל אלא אם כן אתם מבצעים פריסה באמצעות `python -m tgwitness.cloud`, והאספן קורא את המארח שלו רק כאשר הפריסה מוגדרת `TGWITNESS_ASSURANCE`.

תרשים זרימה · מפעיל → שרת, חומת אש ללא כללי כניסה (API של הספק); מפעיל → מנהרה ו-DNS (ממשק ה-API של Cloudflare); שרת, חומת אש ללא כללי כניסה → מנהרה ו-DNS (יוצא בלבד); שרת, חומת אש ללא כללי כניסה → מפתח חתימה שנוצר בשרת; Verifier, אסימונים לקריאה בלבד → יומן ספק וחומת אש; Verifier, אסימונים לקריאה בלבד → כתובת מחבר המנהרה וכניסה; Verifier, אסימונים לקריאה בלבד → הצהרת /api/assurance חתומה; Verifier, אסימונים לקריאה בלבד → קובץ ZIP של הראיות · מפעיל · Verifier, אסימונים לקריאהבלבד · שרת, חומת אש ללא כלליכניסה · יומן ספק וחומת אש · כתובת מחבר המנהרה וכניסה · הצהרת /api/assurance חתומה · קובץ ZIP של הראיות · מנהרה ו-DNS · מפתח חתימה שנוצר בשרת · API של הספק · ממשק ה-API של Cloudflare · יוצא בלבד

**תרשים כטקסט**

1. מפעיל → שרת, חומת אש ללא כללי כניסה (API של הספק)
2. מפעיל → מנהרה ו-DNS (ממשק ה-API של Cloudflare)
3. שרת, חומת אש ללא כללי כניסה → מנהרה ו-DNS (יוצא בלבד)
4. שרת, חומת אש ללא כללי כניסה → מפתח חתימה שנוצר בשרת
5. Verifier, אסימונים לקריאה בלבד → יומן ספק וחומת אש
6. Verifier, אסימונים לקריאה בלבד → כתובת מחבר המנהרה וכניסה
7. Verifier, אסימונים לקריאה בלבד → הצהרת /api/assurance חתומה
8. Verifier, אסימונים לקריאה בלבד → קובץ ZIP של הראיות

**בעמוד זה**

- [מה יכול בודק לבדוק](https://phishdestroy.github.io/TgWitness/he/docs/reference/high-assurance/#what-a-verifier-can-check)
- [ספקים](https://phishdestroy.github.io/TgWitness/he/docs/reference/high-assurance/#providers)
- [מכונה וירטואלית חסויה ב-Phala Cloud (Intel TDX)](https://phishdestroy.github.io/TgWitness/he/docs/reference/high-assurance/#confidential-vm-on-phala-cloud-intel-tdx)
- [לפני שתתחילו](https://phishdestroy.github.io/TgWitness/he/docs/reference/high-assurance/#before-you-start)
- [מהלוח](https://phishdestroy.github.io/TgWitness/he/docs/reference/high-assurance/#from-the-panel)
- [מנהרה מהירה ללא דומיין](https://phishdestroy.github.io/TgWitness/he/docs/reference/high-assurance/#quick-tunnel-without-a-domain)
- [פריסה](https://phishdestroy.github.io/TgWitness/he/docs/reference/high-assurance/#deploy)
- [פריסת ניפוי באגים ונעילה](https://phishdestroy.github.io/TgWitness/he/docs/reference/high-assurance/#debug-deployment-and-lock)
- [הסרת פריסה](https://phishdestroy.github.io/TgWitness/he/docs/reference/high-assurance/#remove-a-deployment)
- [כל שרת (בעל אישור עצמי)](https://phishdestroy.github.io/TgWitness/he/docs/reference/high-assurance/#any-server-self-attested)
- [אמת](https://phishdestroy.github.io/TgWitness/he/docs/reference/high-assurance/#verify)
- [דוח למסירת ראיות](https://phishdestroy.github.io/TgWitness/he/docs/reference/high-assurance/#report-for-evidence-handover)
- [Cloudflare כעד חיצוני](https://phishdestroy.github.io/TgWitness/he/docs/reference/high-assurance/#cloudflare-as-an-outside-witness)
- [קריאת תוצאות הפריסה](https://phishdestroy.github.io/TgWitness/he/docs/reference/high-assurance/#reading-the-deployment-result)

## מה יכול בודק לבדוק

| טענה | כיצד מתבצע הבדיקה | מתוחזק על ידי |
| --- | --- | --- |
| השרת נוצר באמצעות ה-API של הספק במועד ידוע | אובייקט השרת ויצירתו ביומן של הספק עצמו | ספק |
| אף אחד לא השתמש בנתיבי הגישה של הספק | יומן בקשות קונסולה, חילוץ, איפוס סיסמה, בנייה מחדש, ISO, תמונות, גיבויים | ספק |
| שום דבר לא הצליח להתחבר אליו | בחומת האש של הספק אין כללים לכניסה; SSH מוסתר החל מהאתחול הראשון | ספק (חומת אש), מארח (SSH) |
| ניתן לגשת ללוח זה אך ורק דרך המנהרה | הכניסה למנהרה מועברת אל הלוח בלבד; המחבר פועל מכתובת השרת | Cloudflare |
| התוכנה הזו בדיוק פועלת | ה-hash החתום של עץ המקור של האספן שווה ל-checkout של ה-commit שהוטמע | Collector, נבדק מול Git |
| מפתח החתימה נוצר בשרת זה | המפתח חותם על הצהרה המציינת את מזהה השרת של הספק ואת ה-hash של ה-cloud-init שקיבל | Collector, נבדק מול הספק |
| היומן שייך למפתח ולשרת הזה | כל תהליך שמתחיל בראיות ZIP נושא את מדידת המארח עבור אותו שרת | ראיות ZIP |

האספן מתעד את מצב ה-SSH, הפעלות, היסטוריית הכניסות ומידע האתחול ברשומות חתומות של 'process-start' ו-`host.state`. במכונה וירטואלית רגילה מדובר ברשומות מלאי מקומיות, שהבוחן משווה לרשומות העצמאיות של הספק. פריסת Intel TDX המוצגת להלן מאמתת בנוסף מדידות הנתמכות בחומרה.

## ספקים

| `--provider` | אישורים | גישה לקריאה בלבד של ה-Verifier | יומן הספק עבור המאמת | נשמר עבור |
| --- | --- | --- | --- | --- |
| `hetzner` | `HCLOUD_TOKEN` | אסימון קריאה של אותו פרויקט | פעולות שרת וחומת אש | כל עוד המשאבים קיימים |
| `digitalocean` | `DIGITALOCEAN_TOKEN` | אסימון גישה אישי לקריאה בלבד | פעולות Droplet | כל עוד ה-Droplet קיים |
| `linode` | `LINODE_TOKEN` | `linodes`, `firewall`, `events` היקפים לקריאה בלבד | אירועי חשבון, גרסאות של כללי חומת האש | 90 ימים |
| `vultr` | `VULTR_API_KEY` | משתמש בעל גישת קריאה והרשאה `activity_logs` הרשאה | יומן פעילות החשבון (שיטה, נתיב, מבצע) | 30 ימים, ואף יותר עם מנוי ל-audit-log |
| `aws` | `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` | `ec2:DescribeInstances`, `ec2:DescribeSecurityGroups`, `cloudtrail:LookupEvents` | היסטוריית האירועים של CloudTrail | 90 ימים |
| `phala` | `PHALA_CLOUD_API_KEY` | מפתח API של אותו סביבת עבודה | עדכוני יישומים ופעולות CVM: שינויים בתצורת Docker Compose ובסביבה, הפעלות מחדש, שדרוגי מערכת הפעלה | כל עוד האפליקציה קיימת |
| `generic` | אין | אין | אין: **מאומת עצמית** | – |

השתמשו בפרויקט, צוות, חשבון או חשבון משנה ייעודיים לכל תיק: הגישה לקריאה בלבד של המאמת תציג אז רק פריסה זו. פרטי ההזדהות נקראים `--provider-token-file` או מהמשתנה שלעיל, לעולם לא משורת הפקודה. עבור AWS, הקובץ מכיל `ACCESS_KEY_ID SECRET_ACCESS_KEY [SESSION_TOKEN]`; האזור הוא `--location`.

מה שהרישומים של כל ספק אינם יכולים להציג מודפס בכל דוח. בקיצור: Hetzner מתעד בקשות לקונסולה; קונסולת השחזור של DigitalOcean, Lish/Glish של Linode והקונסולה האינטרנטית של Vultr אינן מתועדות ככאלה, ולכן הגישה ל-root נעולה בעת האתחול הראשון וכניסה לקונסולה תדרוש איפוס סיסמה או שינוי באתחול, אשר מתועדים. Vultr מחזירה את כתובת הקונסולה לכל מפתח שיכול לקרוא את המופע; לא התיעוד ולא הדוח מאחסנים אותה.

## מכונה וירטואלית סודית ב-Phala Cloud (Intel TDX)

כאשר `--provider phala` האספן פועל במכונה וירטואלית חסויה מסוג Intel TDX ב- [Phala Cloud](https://phala.com/), המנוהלת על ידי dstack. המארח וצוות Phala אינם יכולים לקרוא את הזיכרון שלו, והמעבד חותם על אישור המציין מה הותקן במכונה. המאמת אינו סומך על דברי Phala: `tgwitness.tdx` הוא בודק בעצמו כל אישור, עד ל-Intel SGX Root CA המוצמד, מול רשימות הביטול של Intel ונתוני הפלטפורמה החתומים של Intel, ומסרב למכונות שניתן לאתר בהן באגים או להעבירן.

| הזנת דוח | מה הוא מציג |
| --- | --- |
| `tdx_binding` | האישור מכסה את ההצהרה החתומה של האספן ואת הערך האקראי של בקשה זו |
| `tdx_quote` | אינטל מאשרת את האישור; הוא ניתן רק כאשר אינטל מעריכה שהפלטפורמה מעודכנת |
| `tdx_compose_hash` | RTMR3, המופעל מחדש מתוך יומן האירועים של dstack, מודד את פעולות כתיבת ההודעות באפליקציה שעליהן מדווח האספן |
| `tdx_compose` | קוד זה, בייט אחר בייט, הוא הקוד שהקוד של ה-commit שהוטמע בונה: קבצי מקור המוצמדים לפי hash, שתי התמונות לפי digest, ללא קוד אחר |
| `tdx_identity` | האישור מגיע מהיישום ומהמופע שהוטמעו, עם מפתחות מ-KMS של Phala ודיסק מוצפן |
| `tdx_os` | MRTD ו-RTMR0-2 שווים לערכים שהמאמת מחשב מתמונת מערכת ההפעלה dstack ש-Dstack-TEE מפרסמת, הנמצאת באמצעות ה-hash של תמונת מערכת ההפעלה ש-CVM מדווחת, ומטבלאות ה-ACPI ש-QEMU בונה עבור תצורת ה-VM: קושחה, קרנל, initrd, שורת פקודה עם ה-hash של מערכת הקבצים השורשית, זיכרון, vCPUs והתקנים. תמונת פיתוח נכשלת |

תמונת מערכת ההפעלה (כ-180 MB, מתוכם נשמרים 21 MB) מורידה פעם אחת מ- [Dstack-TEE/meta-dstack](https://github.com/Dstack-TEE/meta-dstack/releases) אל `dstack-images` לצד התיעוד; `--tdx-image FOLDER` משתמש בתיקייה אחרת או בתמונה שלא נפרקה, `--tdx-image none` מדלג על ההשוואה. המדידה מתבצעת על ידי `dstack-mr` וחבילת ה-Rust `qemu-acpi` מ-Dstack-TEE/dstack; `tools/check_dstack_image.py` בודק אותה מול פלט ה-ACPI של QEMU עצמו ומול רשומת אימות חומרה אמיתית של Phala Cloud, ו-`--live` בודק אותה גם מול התמונה שפורסמה. `--tdx-measurements` עדיין משווה בין MRTD ו-RTMR0-2, המוצגים במקום זאת בפורמט JSON.

כל הפעלה של האספן המתועדת ביומן נושאת אישור כזה, ולכן `verify --evidence` בודק כל הפעלה ואת תמונת מערכת ההפעלה שאותה היא אתחלה. גרסאות היישום של Phala והפעולות של ה-CVM משמשות כיומן הספק: תצורת Docker Compose ששונתה לאחר הפריסה גורמת לכישלון הדוח, וההפעלות מחדש מפורטות לבדיקה.

בלוח הבקרה, בחר "**מכונה וירטואלית חסויה · Phala Cloud"** תחת "**תוספות** " → "**שרת 24/7** " והדבק מפתח API של Phala Cloud; המנהרה המהירה פועלת כמו ב-Hetzner. משורת הפקודה:

```
python -m tgwitness.cloud deploy --provider phala --name case-1 --server-type tdx.small \
    --ref v0.8.0 --repository https://github.com/phishdestroy/TgWitness --quick-tunnel \
    --provider-token-file phala-key.txt
python -m tgwitness.cloud verify --record deployments/case-1/deployment.json \
    --provider-token-file phala-key.txt --cloud-init deployments/case-1/docker-compose.yaml \
    --source CHECKOUT_OF_COMMIT --fingerprint COLLECTOR_FINGERPRINT --report certificate.md
python -m tgwitness.cloud check-report --report certificate.pdf --verifier-fingerprint VERIFIER_KEY
```

`--tdx-collateral` קורא את האישורים ורשימות הביטול של Intel מקובץ במקום להוריד אותם מ-Intel. שירות ה-DNS של השער אינו זמין כאן: ל-Phala אין חומת אש של ספק לתעבורה יוצאת.

### תעודת אימות

בפריסת Phala, `verify --report certificate.md` כותב גם את האישור: `certificate.html` עצמאי ו-`certificate.pdf` בגודל A4 עם המסקנה, שרשרת האמון מהשורש של Intel למפתח האספן, השוואה בין שרתים רגילים לשרתים בעלי אבטחה גבוהה, המדידות לצד הערכים שחושבו מהתמונה שפורסמה, מי מעיד על כל חלק, שרשרת האישורים של Intel, כל בדיקה, יומן הספק, וכיצד לחזור על האימות. דוח ה-JSON נותר התיעוד המוסמך; הדפים מציגים אותו.

הדוח חתום דיגיטלית בחתימות ובחותמות זמן, בקובץ `certificate.seal.json` ובקובצי `.tsq`/`.tsr` הנמצאים לצדו:

| חותם | מה זה מוסיף |
| --- | --- |
| חותמת זמן אלקטרונית מאושרת, `http://tsa.belgium.be/connect` | חותמת זמן RFC 3161 על הבתים המדויקים של `certificate.json` מספק שירותי האמון המוסמך של הממשלה הפדרלית הבלגית (FPS Policy and Support, BOSA). היחידה הזו מופיעה כשירות חתימת זמן מוסמך, עם סטטוס "מוענק", ברשימת האמון של האיחוד האירופי בבלגיה; השורש (Belgium Root CA6) והרשומות ברשימה, נכון לרשימה שפורסמה ב-20 באוקטובר 2026, מוצמדים ב-`tgwitness/tsa_roots.py`. על פי תקנה (האיחוד האירופי) מס' 910/2014, סעיף 41, חותמת זמן כזו נחשבת מדויקת מבחינת התאריך והשעה, וכן מבחינת תקינות הנתונים, בכל מדינה חברה באיחוד האירופי |
| חותמת זמן RFC 3161, FreeTSA | חותמת זמן שנייה, בלתי תלויה |
| חתימת המאמת | Ed25519 על הצהרה המציינת את ה-SHA-256 של הדוח ואת כל חותמות הזמן, באמצעות המפתח של המאמת עצמו (`--sign-with FOLDER`, ברירת מחדל `~/.tgwitness/verifier`); קובץ ה-PDF נושא חתימה מאותו מפתח |

`--timestamp URL` (ניתן לשחזור) בוחר רשויות אחרות, `--timestamp none` לא בוחר אף רשות, `--sign-with
none` משאיר את החותם ללא חתימה. `check-report` בודק את ה-hash של הדוח, את חתימת המאמת, כל חותמת זמן ביחס לשורש מהימן ואת מעמדו המוסמך, וכן את חתימת ה-PDF. המשקל המשפטי של חותמת זמן מוסמכת מחוץ לאיחוד האירופי, ושל הדוח בכללותו, נתון לשיקול דעתו של בית המשפט או הרשות המקבלת אותו; החותם מראה מתי הדוח היה קיים וכי הוא לא שונה.

אישור אינו יכול לשלול פגם במודול ה-TDX או במיקרוקוד של Intel, או גישה פיזית לאוטובוס הזיכרון. מי ששולט ביישום בחשבון של Phala יכול לפרוס קומפוזיציה נוספת; היא מופיעה כגרסה חדשה עם חתימת קומפוזיציה חדשה. המארח שולט במקור הזמן של המחשב וברשת.

הפריסה, האימות באמצעות `--evidence`, ההפעלות מחדש, השוואת תמונת מערכת ההפעלה, האישור החתום דיגיטלית עם חתימות וחותמות זמן, ו השמדה בוצעו על גבי Phala Cloud עצמה; ראו [– הריצה מ-4 בנובמבר 2026,](https://phishdestroy.github.io/TgWitness/he/docs/reference/verification/#live-phala-cloud-deployment--4-november-2026).

## לפני שתתחילו

1. אזור Cloudflare, מזהה החשבון שלו ואסימון API עם **עריכת Cloudflare Tunnel**, **אזור קריאה** ו-**עריכת DNS**, הניתנים באמצעות `--cloudflare-token-file` או `CLOUDFLARE_API_TOKEN`. עבור המאמת: **קריאה ב-Cloudflare Tunnel**, **קריאת DNS**, ועבור יומן הביקורת, **הגדרות חשבון – קריאה**. ללא דומיין, [מנהרה מהירה](https://phishdestroy.github.io/TgWitness/he/docs/reference/high-assurance/#quick-tunnel-without-a-domain) אינו זקוק לשום דבר מזה.
2. פרטי הזדהות של ספק עם גישה לכתיבה לפרויקט ייעודי; `lock` משתמש באותו הדבר:

   - Hetzner: אסימון API עם הרשאות קריאה וכתיבה;
   - DigitalOcean: אסימון גישה אישי עם הרשאת כתיבה;
   - Linode: אסימון גישה אישי עם `linodes`, `firewall` ו `events` היקפי קריאה/כתיבה;
   - Vultr: מפתח API של חשבון ייעודי או חשבון משנה;
   - AWS: אישורי IAM מותרים `ec2:DescribeVpcs`, `ec2:DescribeImages`, `ec2:CreateSecurityGroup`, `ec2:AuthorizeSecurityGroupIngress`, `ec2:RunInstances`, `ec2:CreateTags`, `ec2:DescribeInstances`, `ec2:DescribeSecurityGroupRules` ו- `ec2:RevokeSecurityGroupIngress`.
3. הקומיט שיש להריץ. תגית שחרור מפורשת פעם אחת לקומיט שלה באמצעות `git ls-remote`; השרת מקבל תמיד רק את ה-commit בן 40 התווים.

## מהלוח

במחשב האישי שלכם, תפריט **Extras → Server 24/7** מפעיל את אותו `deploy` עבור Hetzner בשלושה שלבים: בחרו באירופה או בארצות הברית, הדביקו אסימון Hetzner (קריאה וכתיבה), ואז בדקו את סוג השרת, המחיר החודשי, הכתובת והגרסה שהלוח מצא באמצעות האסימון הזה. שום דבר לא נוצר לפני שתאשרו. הלוח מציג כל שלב כפי `deploy` כפי שהוא מדווח עליה, ולאחר מכן את הכתובת, אסימון הפאנל וטביעת האצבע של מפתח החתימה. ללא דומיין, השרת מקבל [מנהרה מהירה](https://phishdestroy.github.io/TgWitness/he/docs/reference/high-assurance/#quick-tunnel-without-a-domain) ; **השרתים שלך → מצא את הכתובת הנוכחית** מחפש אותה שוב לאחר הפעלה מחדש. עבור כתובת קבועה תחת הדומיין שלך, פתח **'אופציונלי' · הדומיין שלך** והוסף אסימון Cloudflare (הקישור המוכן בוחר 'קריאת אזור' , 'עריכת DNS' ו'עריכת מנהרת Cloudflare').

האסימונים מועברים עם כל בקשה מכרטיסיית הדפדפן אל TgWitness באותו מחשב ואינם נשמרים בשום מקום; תיעוד הפריסה, קובץ cloud-init שעבר עריכה, אסימון הפאנל ו, במקרה של מנהרה מהירה, מפתח הכתובת נשמרים `deployments/NAME` בתוך ספריית הנתונים. הלוח מציע זאת רק למנהל הראשי בחיבור לולאה חוזרת ישיר (`127.0.0.1`, ללא כותרות פרוקסי או מנהרה); לוח נגיש דרך הרשת מציג את הפקודות במקום זאת. ברירת המחדל של הגרסה היא תג השחרור של הלוח הפועל, המתורגם באמצעות API של GitHub. המיקום, סוג השרת והמחיר מגיעים מ-API של Hetzner: `cpx22` במקומות שבהם הוא מוצע, אחרת סוג ה-x86 הזול ביותר עם לפחות 2 GB של זיכרון.

## מנהרה מהירה ללא דומיין

`--quick-tunnel` מחליף `--zone`, `--cloudflare-account` ו `--panel-host`; אין צורך בחשבון או בטוקן של Cloudflare: ;

```
python -m tgwitness.cloud deploy --provider hetzner --name case-2026-11 --server-type cpx22 \
    --ref 0123456789abcdef0123456789abcdef01234567 --quick-tunnel --provider-token-file hetzner.token
```

בשרת, cloudflared פותח [מנהרה מהירה](https://developers.cloudflare.com/tunnel/get-started/quick-tunnels/) אל לוח הבקרה: כתובת אקראית `https://….trycloudflare.com` המתחלף בכל פעם ש-cloudflared או השרת מופעלים מחדש. שירות קטן בשרת מפרסם כל כתובת בנושא אקראי ב-ntfy.sh , חתום (HMAC-SHA256) במפתח שנמצא רק בספריית הפריסה (`address-key.txt`), וחוזר על כך כל שלוש שעות מכיוון ש-ntfy.sh שומר את ההודעות למשך 12. `deploy` ו-**Find the current address** מקבלים רק פרסומים חתומים, כך שפרסום מזויף לא יכול לשלוח אותך, ואת אסימון הפאנל שלך, לכתובת של מישהו אחר. הנושא נמצא ברשומה וב- cloud-init שפורסם: מי שיש לו אותם יכול לקרוא את הכתובת הנוכחית, שעדיין מבקשת את אסימון הפאנל. השרת לא שומר על יציאה נכנסת בשום מקרה.

למאמת אין מפתח כתובת, וכל מי שקורא את הנושא יכול לפרסם בו. לכן האספן מפרסם גם את הכתובת עצמה, חתומה במפתח Ed25519 משלו, ו-`verify` לוקח את ההודעה החדשה ביותר החתומה במפתח האספן ברשומת הפריסה; ההודעות מסודרות לפי הזמן שבו ntfy.sh קיבל אותן, ולא לפי הזמן שהן טוענות. אספן מלפני שינוי זה אינו חותם על דבר, ו- `verify` לוקח אז את ההודעה החדשה ביותר ומציין זאת בבדיקת `statement`; הודעה מזויפת יכולה רק לגרום לכישלון הבדיקה, שכן הכתובת עדיין חייבת לענות עם מפתח האספן.

מה זה עולה: אף חשבון Cloudflare אינו שומר תיעוד של מנהרה מהירה, ולכן `verify` מדווח כי המנהרה, המחבר ובדיקת ה-DNS אינם זמינים והתוצאה היא, במקרה הטוב, `incomplete` (בענן Phala Cloud הבדיקה עוברת במקום זאת: המחבר פועל בתוך תצורת Docker Compose הנמדדת); הרשומות של הספק, חומת האש, ההצהרה החתומה, מדידות המארח והשוואת המתקין נבדקות כרגיל. השוואת הבתים עם מתקין הייחוס דורשת commit פרוס שכבר מכיר את `--quick-tunnel`; צ'ק-אאוט של גרסה 0.7.0 בונה את מתקין הדומיין ומדווח על ההבדל. Cloudflare אינה מעניקה למנהרות המהירות כל אחריות לזמן פעילות, מאפשרת 200 בקשות בזמן אמת ואינה מעבירה אירועים הנשלחים מהשרת (Server-Sent Events), ולכן העדכונים החיים של הלוח (גרסאות לאחר 0.7.0) עלולים שלא להגיע דרך מנהרה כזו, ויש צורך לטעון מחדש את התצוגה; חלק זה טרם נבדק. במקרה שצריך לעמוד בדרישות, השתמשו בדומיין משלכם.

## פריסה

בדקו תחילה את כל מה שיישלח. `plan` אינו מבצע בקשות לספק או ל-Cloudflare:

```
python -m tgwitness.cloud plan --provider hetzner --name case-2026-11 --server-type cpx22 \
    --ref 0123456789abcdef0123456789abcdef01234567 --zone example.org \
    --cloudflare-account CLOUDFLARE_ACCOUNT_ID --panel-host case.example.org
```

לאחר מכן, בצעו פריסה עם אותן אפשרויות ואותם פרטי הזדהות:

```
python -m tgwitness.cloud deploy --provider hetzner --name case-2026-11 --server-type cpx22 \
    --ref 0123456789abcdef0123456789abcdef01234567 --zone example.org \
    --cloudflare-account CLOUDFLARE_ACCOUNT_ID --panel-host case.example.org \
    --witness-host case-witness.example.org \
    --provider-token-file hetzner.token --cloudflare-token-file cloudflare.token
```

סוגי שרתים להתחלה: `cpx22` (Hetzner), `s-1vcpu-2gb` (DigitalOcean), `g6-standard-1` (Linode), `vc2-1c-2gb` (Vultr), `t3.small` (AWS). `--location` וב `--image` כברירת מחדל, Ubuntu 24.04 של כל ספק באזור אירופי.

`--repository` מקבל את ה-commit ממאגר Git אחר ב-https, ללא פרטי הזדהות ב- URL (כברירת מחדל `https://github.com/phishdestroy/TgWitness.git`). `deploy` מקבל גם `--out` לספריית פריסה אחרת (ברירת מחדל `deployments/NAME`; ספרייה שכבר מכילה פריסה נדחית) ו `--wait`, מספר הדקות שיש להמתין להצהרה החתומה של האספן: 1 עד 240, ברירת מחדל 20, או 60 עבור `generic`.

הפקודה:

1. יוצר מנהרה של Cloudflare שהכניסה שלה מעבירה את שם המארח של הלוח אל הלוח, ואם ניתן, את שם המארח של ה-witness אל `/api/witness/head` ו `/api/assurance` בלבד;
2. יוצר רשומות CNAME באמצעות פרוקסי עבור שמות המארחים הללו, תוך דחיית שמות שכבר קיימים;
3. יוצר חומת אש של ספק ללא כללי כניסה, ומאחוריה שרת ללא מפתח SSH, ללא גיבויים, ללא סוכן קונסולה, ו-cloud-init שמסתיר את ה-SSH, נועל את ה-root, מתקין `cloudflared`, מוריד בדיוק את ה-commit, בודק אותו ומפעיל את TgWitness כ שירות systemd מחוזק;
4. ממתין להצהרה החתומה של האספן ובודק שהיא מציינת את השרת הזה ואת ה-hash של ה-cloud-init הזה.

`deployments/case-2026-11/` ואז מכיל:

| קובץ | תוכן העניינים | לשתף? |
| --- | --- | --- |
| `deployment.json` | מזהים, חתימות hash, קריאות ה-API שבוצעו (שיטה, נתיב, סטטוס) וההצהרה החתומה הראשונה | כן, באמצעות המאמת |
| `cloud-init.redacted.yaml` | ה-cloud-init המדויק, כאשר שני הסודות שלו הוחלפו ב- `REDACTED` | כן |
| `panel-token.txt` | אסימון הפאנל | לא |

סיסמת השורש של הספק, אסימון המנהרה ואסימון הפאנל לעולם אינם נכתבים `deployment.json`. פרסם את טביעת האצבע של האספן המופיעה בסוף דרך ערוץ שאינך שולט בו לבד, למשל ערוץ עדים או הודעה לנמען.

היכנסו ל-Telegram בכתובת `https://case.example.org` באמצעות אסימון הפאנל, כפי שמוסבר [במדריך לחשבון](https://phishdestroy.github.io/TgWitness/he/docs/reference/accounts/). פעולות הפאנל נרשמות ביומן החתום; הן אינן הפעלות SSH. [עד](https://phishdestroy.github.io/TgWitness/he/docs/reference/witness/) יכול לבצע סקר `https://case-witness.example.org`.

אין SSH: אם תהליך האתחול נכשל, האספן לעולם לא יגיב. מחקו את השרת ו הפעילו אותו מחדש, או השתמשו בפריסה לאיתור באגים כדי לאתר את הגורם.

### סודות בנתוני המשתמש

ה-cloud-init נושא שני סודות: אסימון הפאנל ואסימון המנהרה של Cloudflare. מפתח החתימה אינו נכלל ביניהם; הוא נוצר בשרת. Hetzner, DigitalOcean ו-Linode אינם מחזירים נתוני משתמש דרך ה-API שלהם. Vultr מחזיר אותם לכל מפתח שיכול לקרוא את האינסטנס, ו-EC2 דרך `DescribeInstanceAttribute`. עבור AWS, יש לתת למאמת רק את שלושת הפעולות המופיעות בטבלה, לעולם לא `ec2:Describe*`. עבור Vultr, יש להניח שמפתח המאמת יכול לקרוא את שני האסימונים. אסימון מנהרה מאפשר למישהו להפעיל מחבר שני: `verify` מדווח על כל מחבר שאינו נמצא בשרת, ולא ניתן לזייף את ההצהרות של האספן בדרך זו, מכיוון שכל אחת מהן חותמת על אתגר חדש. עם `--quick-tunnel` הסוד השני הוא מפתח הכתובת: מי שקורא אותו יכול לפרסם כתובת כוזבת שהפאנל יקבל.

בהצהרה הפומבית של האספן לא מוזכרים כתובת השרת ומקורות הכניסות; שניהם נשארים ביומן החתום.

## איתור באגים בפריסה ונעילה

`--debug-ssh-key KEY --debug-ssh-from 198.51.100.4` שומר SSH עבור מפתח אחד מכתובת אחת או מרשת קטנה, לכל היותר /24 עבור IPv4 או /48 עבור IPv6. `KEY` כבר רשום אצל הספק: השם או המזהה של מפתח SSH בפרויקט Hetzner, המזהה או טביעת האצבע של מפתח SSH בצוות DigitalOcean, שם משתמש ב-Linode שמפתחות ה-SSH בפרופיל שלו מתווספים ל-root, המזהה של מפתח SSH בחשבון Vultr, או השם של זוג מפתחות EC2 באזור. אפשרויות אלה אינן חלות על `generic`. פריסה כזו נרשמת כ `debug` ול**עולם לא** מדווחת כ בעלת אבטחה גבוהה. בסיום, הפעל `sudo tgwitness-lock` כפקודה האחרונה של הפעלת ה-SSH האחרונה, ולאחר מכן:

```
python -m tgwitness.cloud lock --record deployments/case-2026-11/deployment.json --provider-token-file hetzner.token
```

חומת האש מאבדת כל כלל נכנס. לאחר מכן, הדוחות מראים מתי הותר שימוש ב-SSH ומתי הוא נסגר; חלון זה נשאר גלוי.

## הסרת פריסה

`destroy` מחיקת השרת וחומת האש שלו, הנמצאים לפי תווית הפריסה, כך ש פריסה שנכשלה באמצע התהליך תוסר גם היא, ולאחר מכן רשומות ה-DNS שמפנות אל המנהרה, והמנהרה עצמה. יומן השרת ומפתח החתימה נמחקים יחד איתו: יש לייצא את הראיות תחילה. התיעוד נשאר, מסומן `removed`, עם קריאות ה-API של ההסרה.

```
python -m tgwitness.cloud destroy --record deployments/case-2026-11/deployment.json --confirm case-2026-11 \
    --provider-token-file hetzner.token --cloudflare-token-file cloudflare.token
```

הסרה באמצעות ה-API מיושמת עבור Hetzner. עבור ספקים אחרים `destroy` עוצר לפני מחיקת כל דבר ומציין את התווית למחיקה בקונסולת הספק. שרת המותקן ידנית (`generic`) מאבד רק את רשומות המנהרה וה-DNS שלו. פריסת מנהרה מהירה אינה דורשת אסימון Cloudflare: המנהרה שלה מסתיימת בשרת, וההודעות שלה פוקעות מ-ntfy.sh תוך 12 שעות.

## כל שרת (בעל אימות עצמי)

`--provider generic` מיועד לשרת שנרכש או הותקן באופן ידני. `deploy` יוצר את המנהרה ואת ה-DNS, כותב `install.sh` (פרטי) ו `install.redacted.sh` (לפרסום), וממתין. העתיקו `install.sh` לשרת Ubuntu 24.04 שהותקן זה עתה והפעל אותו שם:

```
sudo bash install.sh
```

הוא מתעד את המארח כפי שהיה (כניסות, חשבונות, `authorized_keys`, שקעי האזנה, שירותים, משימות מתוזמנות, חבילות), מתקין את ה-commit, מפעיל את חומת האש של המארח, מוחק את עצמו, מסווה את ה-SSH ומסיים את ההפעלה. הדוח עבור שרת כזה הוא, במקרה הטוב, **"מאומת עצמית"**: מי שהריץ את תוכנית ההתקנה החזיק בזכויות root לפני כן, ואין תיעוד של הספק זמין למאמת. זה עדיין עדיף על שרת בלתי מוסבר: המלאי, ה-hash של תוכנית ההתקנה וכל כניסה מאוחרת יותר חתומים.

## אמת

המאמת זקוק `deployment.json`, את תוכנת ההתקנה שפורסמה, פרטי התחברות לקריאה בלבד, ו, באופן אידיאלי, צ'ק-אאוט של הקומיט וראיה ZIP:

```
git clone -c core.autocrlf=false https://github.com/phishdestroy/TgWitness.git checkout
git -C checkout checkout 0123456789abcdef0123456789abcdef01234567
python -m tgwitness.cloud verify --record deployment.json \
    --provider-token-file read-only.token --cloudflare-token-file cloudflare-read.token \
    --fingerprint COLLECTOR_FINGERPRINT --cloud-init cloud-init.redacted.yaml \
    --source checkout --evidence tgwitness-evidence.zip --report report.md
```

כל ספק וערך של Cloudflare מתבקשים על ידי המאמת באותו הרגע; הרישום מספק רק את המזהים שעליהם יש לשאול. קוד היציאה הוא 0 עבור **PASS**, 1 עבור **FAIL** ו-2 עבור **REVIEW**, **INCOMPLETE** או **SELF-ATTESTED**. `--fingerprint` צריך להגיע מערוץ עצמאי; בלעדיו, המפתח מושווה רק לרישום של המפעיל. `python verify.py` עדיין מאמת את הראיות ZIP בעצמו, כפי שמופיע בסעיף ["ראיות"](https://phishdestroy.github.io/TgWitness/he/docs/reference/evidence/).

פעולות הספק מסווגות: יצירה והפעלה תוך 30 דקות מרגע היצירה עוברות; קונסולה, חילוץ, איפוס סיסמה, בנייה מחדש, ISO, תמונות, תמונות מצב, גיבויים, מנהל מערכות, חיבור EC2 Instance Connect ופתיחת חומות אש נכשלות; פעולות חשמל וכל דבר בלתי צפוי מסומנים לבדיקה. פעולה לא ידועה לעולם לא עוברת בשקט.

## דוח להעברת ראיות

`--report report.md` כותב את הדוח ב-Markdown ו `report.json` לידו:

1. תוצאה, טביעת אצבע של מפתח האספן, פריסה, ספק, התחייבות, שרת, חומת אש, מנהרה;
2. כל בדיקה עם הסטטוס והמקור שלה (API של הספק, API של Cloudflare, דוח האספן, יומן הראיות);
3. יומן הספק עם הערכת כל פעולה, ובמקרים שבהם הספק מתעד זאת – גם זהות המבצע;
4. נקודות הקצה של Cloudflare המכילות את חיבורי המנהרה, התצורה ויומן הביקורת;
5. הצהרת האספן החתומה;
6. מה הדוח קובע ומה לא;
7. פקודות לשחזור התהליך, וה-SHA-256 של כל קובץ שניתן לו.

העבר את הדוח, `report.json`, `deployment.json`, את תוכנת ההתקנה שפורסמה ואת הראיות ZIP. הכינו את הדוח בהקדם: יומני הספק נשמרים לתקופות מוגבלות.

## Cloudflare כעד חיצוני

הכל כאן הוא אופציונלי. גם ללא חשבון Cloudflare השרת עדיין פועל, ושניים מהאלה פועלים כיום:

| מה | מה הוא מציג | ב-TgWitness |
| --- | --- | --- |
| מנהרה מהירה או מנהרה של הדומיין שלכם | ניתן לגשת ללוח רק דרך המנהרה | אשף השרת, ראו לעיל |
| drand relay `drand.cloudflare.com` | הרשומות לאחר סיבוב drand חדשות יותר ממנה: היומן נכתב תוך כדי התקדמות | מצב ראיות, **עדים נוספים**, ללא חשבון ([פורמט](https://phishdestroy.github.io/TgWitness/he/docs/reference/evidence/#optional-records-in-evidence-mode-drand-and-telegram-devices)) |
| התראות על תקינות המנהרה | כאשר המנהרה הייתה מושבתת, באמצעות דוא"ל או Webhook מ-Cloudflare | הגדר אותם בלוח הבקרה של Cloudflare |
| Gateway DNS (`--gateway-dns`, או **Cloudflare Gateway DNS** באשף) | כל שם שהשרת חיפש, נענה על ידי Cloudflare באמצעות TLS; חומת האש של Hetzner מונעת מ-DNS להגיע לכל דבר אחר; האם מדיניות השער יכולה לשנות את התשובות | Hetzner, תוכנית Zero Trust חינמית, ללא דומיין; `verify` בודק את חומת האש, המיקום, הרישום, המדיניות, שאילתות השרת ויומן הביקורת; מצב הראיות מעתיק את היומן אל היומן |
| שער עם לקוח Cloudflare One בשרת, חומת אש יוצאת המאפשרת רק את Cloudflare | כל חיבור שהשרת ביצע, לא רק DNS | עדיין לא נבנה |
| גישה מול הפאנל | מי התחבר לפאנל ומתי | לא נבנה: דורש דומיין משלך |
| רישום פקודות SSH | כל פקודה בסשן ניפוי באגים | עדיין לא נבנה |

Logpush, אשר ישמור עותק של Cloudflare ב-R2, הוא תכונה של תוכנית Enterprise: בתוכנית החינמית Cloudflare עונה `logpush is not enabled for this account`. יומן ה-Gateway נשמר שם למשך 24 שעות, ולכן מצב הראיות מעתיק אותו ליומן החתום (**יומן ה-Cloudflare Gateway של שאילתות ה-DNS של שרת זה**, אסימון לקריאה בלבד עם 'קריאת ניתוח חשבונות').

ללא תוכנית Zero Trust, לחשבון יש מיקום DNS אחד. כאשר Cloudflare דוחה מיקום אחר, השרת משתף את המיקום הקיים, והשאילתות שלו מובחנות לפי כתובתו; מסנן זה זקוק גם ל-Zero Trust PII Read, ו `destroy` מה שמותיר מיקום משותף. שאילתת יומן אחת משתרעת לכל היותר על פני שלוש שעות, ולכן הקריאה וה `verify` לקריאה של היום בחלונות של שלוש שעות.

Gateway DNS מכסה את מפתרון השמות של המערכת. DNS over HTTPS ביציאה 443 למפתרון שמות אחר, ו חיבורים לכתובת שלא נבדקה בשום מקום (למשל, מרכזי הנתונים של Telegram), אינם מופיעים ביומן שלה.

Cloudflare אינה יכולה לראות את תוכן ההצפנה של Telegram, מכשירים אחרים בחשבון Telegram (רשימת המכשירים במצב הראיות מתעדת אותם מצד Telegram) או את ההיפר-ויזור של הספק.

## קריאת תוצאות הפריסה

במקרה של מכונה וירטואלית רגילה, הספק שולט בתשתית המארחת, והמלאי המקומי נבדק לצד רשומות הספק. עבור Intel TDX, המאמת בודק בנוסף את ציטוט החומרה, קישור האספן, ה-compose ומדידות מערכת ההפעלה. קראו את התוצאות הבודדות כדי לראות אילו בדיקות עברו או לא היו זמינות.

פרטי חומת האש ההיסטוריים תלויים בספק; Linode שומר את גרסאות הכללים. [רשומת האימות](https://phishdestroy.github.io/TgWitness/he/docs/reference/verification/) מפרטת פריסות שנבדקו ובדיקות פעילות שנותרו, ו-[היקף האימות](https://phishdestroy.github.io/TgWitness/he/docs/reference/evidence/#verification-scope) מקשר בין בדיקות סביבה אלה לרכישת ארכיונים ולשלמותם.
