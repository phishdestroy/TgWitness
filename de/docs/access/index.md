# Einen Fall teilen

Canonical page: https://phishdestroy.github.io/TgWitness/de/docs/access/

Teilen Sie den Fall, den jemand benötigt. Behalten Sie die Kontrolle über den Rest.

01**Wählen Sie die Beweise aus**

Ganze Arbeitsbereiche oder einzelne Chats.

02**Wählen Sie die Aktionen aus**

Ansehen, exportieren oder nur die nötigen Aktionen.

03**Legen Sie die Grenzen fest**

Ein persönliches Token mit Ablaufdatum, Sitzungslimits und IP-Regeln, wenn Sie wollen.

Der Erfassungsumfang bestimmt, was aufgezeichnet wird. Der Zugriffsumfang bestimmt, was eine Person sehen und tun kann.

## Jemandem Zugriff gewähren

1. Als Admin **Zugriff** öffnen.
2. Benennen, Arbeitsbereiche und Chats wählen.
3. Ein Prüfer braucht nur **Ansehen**. Für Downloads **Exportieren** hinzufügen.
4. Legen Sie die Einschränkungen fest und klicken Sie anschließend auf **„Zugriff erstellen**“.
5. Token kopieren (wird einmal angezeigt) und privat mit der Panel-Adresse schicken.
6. Prüfen Sie vorher in einer separaten Browser-Sitzung, was die Person sehen wird.

## Beginnen Sie mit der Aufgabe, die sie zu erledigen haben

| Person | Zugriff | Ergebnis |
| --- | --- | --- |
| Rezensent | Ausgewählte Chats; nur zur Ansicht | Liest den Chat, kann nichts ändern. |
| Analyst | Ausgewählte Chats; anzeigen und exportieren | Liest und lädt herunter, was der Fall braucht. |
| Betreiber | Ausgewählte vollständige Arbeitsbereiche; Quellen und Sammlung | Entscheidet, was beobachtet wird, startet und stoppt Collectoren. |

Das sind nur Beispiele, keine festen Rollen. Auf Chats beschränkter Zugriff bekommt nie Kontoeinstellungen oder vollständige Journal-Exporte. Zugriff auf alle Arbeitsbereiche schließt später hinzugefügte Konten ein.

## Sie können Ihre Meinung jederzeit ändern

Zugriff jederzeit bearbeiten, es gilt ab der nächsten Anfrage. Eine Sitzung beenden oder alles widerrufen. Bereits heruntergeladene Dateien sind weg. Die Erfassung läuft weiter.

**Sitzungs- und IP-Beschränkungen**

Parallele Sitzungen und Anmeldungen begrenzen, ein Enddatum setzen, IPs oder Subnetze erlauben oder an die IP der ersten Anmeldung binden. Der Ablauf zählt Inaktivität, ein offenes Panel gilt als aktiv. Hinter einem Proxy prüfen, welche Client-IP die App sieht.

**Der Hauptschlüssel und das Aktivitätsprotokoll**

Das Haupttoken bleibt beim Admin. Vergebener Zugriff kann weder fremden Zugriff verwalten noch die Admin-Konsole öffnen. Zugriffsänderungen und Sitzungen werden ins Journal signiert, ohne Tokens. Der Server-Admin sieht weiterhin alles.

Alle sieben Berechtigungen und Sitzungsregeln: [Zugriffsreferenz](https://phishdestroy.github.io/TgWitness/de/docs/reference/access/).
