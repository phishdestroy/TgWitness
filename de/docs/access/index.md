# Einen Fall teilen

Canonical page: https://phishdestroy.github.io/TgWitness/de/docs/access/

Teilen Sie den Fall, den jemand benötigt. Behalten Sie die Kontrolle über den Rest.

01**Wählen Sie die Beweise aus**

Wählen Sie ganze Konto-Arbeitsbereiche oder einzelne aufgezeichnete Chats aus.

02**Wählen Sie die Aktionen aus**

Erteilen Sie die erforderlichen Berechtigungen zum Anzeigen, Exportieren oder für bestimmte operative Vorgänge, die die betreffende Person benötigt.

03**Legen Sie die Grenzen fest**

Erstellen Sie ein persönliches Token mit Ablaufdatum, Sitzungsbeschränkungen und optionalen IP-Einschränkungen.

Der Erfassungsumfang bestimmt, was aufgezeichnet wird. Der Zugriffsumfang bestimmt, was eine Person sehen und tun kann.

## Jemandem Zugriff gewähren

1. Melden Sie sich als Administrator an und öffnen Sie **„Access**“.
2. Geben Sie den Namen des Zugangs an und wählen Sie Arbeitsbereiche und Chats aus.
3. Behalten Sie **die Option „Anzeigen“** für einen Prüfer bei. Fügen Sie **die Option „Exportieren“** hinzu, falls dieser die Aufzeichnungen herunterladen soll.
4. Legen Sie die Einschränkungen fest und klicken Sie anschließend auf **„Zugriff erstellen**“.
5. Kopieren Sie das einmalig angezeigte Token. Senden Sie es privat zusammen mit der Panel-Adresse.
6. Bitte überprüfen Sie die zulässige Ansicht in einer separaten Browsersitzung, bevor Sie die Seite weitergeben.

## Beginnen Sie mit der Aufgabe, die sie zu erledigen haben

| Person | Zugriff | Ergebnis |
| --- | --- | --- |
| Rezensent | Ausgewählte Chats; nur zur Ansicht | Lesen Sie die erfasste Unterhaltung, ohne die Datensammlung zu verändern. |
| Analyst | Ausgewählte Chats; anzeigen und exportieren | Prüfen und laden Sie die für den Fall erforderlichen Aufzeichnungen herunter. |
| Betreiber | Ausgewählte vollständige Arbeitsbereiche; Quellen und Sammlung | Verwalten Sie die erfassten Daten und starten oder stoppen Sie die Erfassungsmodule. |

Hierbei handelt es sich um von Ihnen gewählte Konfigurationen, nicht um festgelegte Rollen. Kontoweite Einstellungen und vollständige Protokoll-Exporte bleiben für den auf Chats beschränkten Zugriff gesperrt, selbst wenn eine andere Berechtigung aktiviert ist. Der Zugriff auf den gesamten Arbeitsbereich umfasst auch zukünftige Konten.

## Sie können Ihre Meinung jederzeit ändern

Bearbeiten Sie die Zugriffsrechte, um festzulegen, welche Aktionen bei nachfolgenden Anfragen möglich sind. Beenden Sie eine einzelne Sitzung oder widerrufen Sie den gesamten Zugriff, um alle Sitzungen zu beenden. Bereits heruntergeladene Dateien können nicht zurückgerufen werden. Das Beenden einer Panel-Sitzung stoppt die Erfassung nicht.

**Sitzungs- und IP-Beschränkungen**

Begrenzen Sie die Anzahl paralleler Sitzungen und erfolgreicher Anmeldungen, legen Sie ein absolutes Enddatum fest, erlauben Sie bestimmte IP-Adressen oder Subnetze oder binden Sie den Zugriff an die Adresse der ersten Anmeldung. Das Ablaufen einer Sitzung wird anhand von Inaktivität gemessen; das Abrufen eines geöffneten Fensters gilt als Aktivität. Überprüfen Sie die von der Anwendung angezeigte Client-Adresse, wenn diese hinter einem Proxy oder Tunnel ausgeführt wird.

**Der Hauptschlüssel und das Aktivitätsprotokoll**

Der Administrator verwahrt das Token für das Hauptfenster. Mit einem erteilten Zugriffsrecht ist es nicht möglich, die Zugriffsrechte anderer Personen zu verwalten oder die Administratorkonsole zu öffnen. Die Konsole zeigt die Aktivitäten des aktuellen Prozesses über alle Arbeitsbereiche hinweg an; signierte Zugriffsprotokolle speichern Berechtigungs- und Sitzungsereignisse ohne Tokens. Die Arbeitsbereiche teilen sich den Host-Prozess und isolieren die Daten nicht vom Serveradministrator.

Verwenden Sie die [vollständige Berechtigungsreferenz](https://phishdestroy.github.io/TgWitness/de/docs/reference/access/) für alle sieben Berechtigungen, Sitzungsregeln und die Administratorgrenzen.
