# Telegram · המשך להפעיל את האתר

Canonical page: https://phishdestroy.github.io/TgWitness/he/docs/server/

השאירו את האוסף פועל ואת הנתונים בטוחים לאורך הפעלות מחדש.

## בחר שיטת השקה

התקנה מקומית: [המפעיל](https://phishdestroy.github.io/TgWitness/he/docs/start/) ועוד תבניות שירות ב-[deploy/](https://github.com/phishdestroy/TgWitness/blob/main/deploy/README.md). Docker, מתיקיית הפרויקט:

```
docker compose up -d --build --wait
docker compose exec tgwitness cat /data/panel-token.txt
```

הלוח מאזין ב-localhost:8787. פתחו אותו מקומית או דרך מנהרת SSH, עם הטוקן מהפקודה השנייה.

## יש לשמור את ספריית הנתונים במלואה

התקנה מקומית: `data/live`. Docker: הכרך `tgwitness-data`. יומנים, סשנים ומפתחות שייכים יחד. ייצוא חתום הוא ראיה, לא גיבוי.

1. עצרו קודם את האיסוף.
2. העתיקו את כל תיקיית הנתונים למקום בטוח, מחוץ למארח.
3. נסו לשחזר אותה בהתקנה נפרדת לפני שאתם סומכים עליה.

## יש לבדוק לאחר הפעלה מחדש

בדקו את סביבת העבודה והמפתח, החיבור, המקורות ושהודעות חדשות נכנסות. TgWitness משלים את מה שעדיין יש ל-Telegram, לא את כל מה שקרה בזמן שהיה כבוי.

קונטיינר "healthy" אומר ששרת הווב עונה. אם האיסוף עובד, הודעת בדיקה והעד יגידו.

## פרסם רק את מה שאתה מתכוון לפרסם

HTTPS, כרכים, עדכונים ושחזור נמצאים במדריך הפריסה. מה שבאמת נבדק: [רישום האימות](https://phishdestroy.github.io/TgWitness/he/docs/reference/verification/).
