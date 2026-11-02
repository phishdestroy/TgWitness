# Anleitung zum Panel

Canonical page: https://phishdestroy.github.io/TgWitness/de/docs/reference/panel/

Alle Bildschirme des Panels: Chats, Tagebuch, Quellen, Exporte, Extras, Schutzmodi und die Code-Prüfung.

[Erste Einrichtung und Einstellungen](https://phishdestroy.github.io/TgWitness/de/docs/reference/settings/) · [Konten](https://phishdestroy.github.io/TgWitness/de/docs/reference/accounts/) · [Exportieren und verifizieren](https://phishdestroy.github.io/TgWitness/de/docs/reference/evidence/) · [Fallberichte](https://phishdestroy.github.io/TgWitness/de/docs/reference/case-reports/)

Was die einzelnen Bildschirme bewirken, was sie in das signierte Protokoll schreiben und wo sich die ausführliche Anleitung befindet. Das Fenster zeigt jeweils einen Arbeitsbereich an: ein Telegram-Konto mit eigenen Quellen, einem eigenen Protokoll und einem eigenen Signaturschlüssel. Mit dem Auswahlfeld oben in der Seitenleiste kann man zwischen den Arbeitsbereichen wechseln. Die Adresse enthält den Arbeitsbereich (`?ws=…`); solange die Adresse, der Auswähler und das geladene Konto nicht übereinstimmen, bleiben Aktionen gesperrt.

## Finden Sie sich zurecht

Die täglichen Bereiche befinden sich oben in der Seitenleiste, **„Konten“** ist unter **„Arbeitsbereich“** zu finden, und alles andere ist unter **„Weitere Tools & Einstellungen“** zu finden. Der Schalter **für die Oberflächenebene** in der oberen Leiste legt fest, wie viele Bereiche angezeigt werden:

| Ebene | Abschnitte in der Seitenleiste |
| --- | --- |
| Einfach | Startseite, Chats, Änderungen, Archive und Einstellungen |
| Standard | Außerdem Case Board, Konten und Zugriff |
| Experte | Außerdem: Quellen, Extras, „Das Archiv befragen“, Parameter, Konto, Systemprotokoll und Integrationen |

Einfache Aufrufe: „Hier starten“, „Journal“ und „Exporte“, **„Startseite**“, **„Änderungen“** und **„Archive**“. Eine Stufe blendet lediglich Abschnitte aus. Eine ausgeblendete Funktion bleibt weiterhin aktiv, und der Server überprüft jede Berechtigung eigenständig. Stufe, Sprache, Design und Zeitzone werden pro Benutzer und Arbeitsbereich gespeichert; siehe [Einstellungen](https://phishdestroy.github.io/TgWitness/de/docs/reference/settings/).

Die obere Leiste enthält außerdem:

- **Zu einem Abschnitt springen** (Strg+K oder ⌘K auf einem Mac): Finden Sie einen Chat, einen Parameter oder einen Tagebucheintrag durch `#number`. Mit den Pfeiltasten navigieren, mit Enter öffnen, mit Esc schließen.
- **Benachrichtigungen**: Probleme und Änderungen im Chat, die aus dem Journal abgeleitet wurden. **Mit „Alle als gelesen markieren“** wird der Zähler zurückgesetzt, und **„Benachrichtigungsregeln“** öffnet die Regeln. Die Zustellung an Telegram, Discord oder per E-Mail wird unter [„Extras → Benachrichtigungen“](https://phishdestroy.github.io/TgWitness/de/docs/reference/panel/#notifications) eingerichtet.
- Die Verbindungsanzeige für diesen Arbeitsbereich. **Der „Collector Health“-Status** unter der oberen Leiste unterteilt diesen in die Telegram-Verbindung, die Ereignisaufnahme, die Quellen und die Anhangswarteschlange.
- **„Lock**“: Schließt das Fenster in diesem Browser. Die Sammlung läuft auf dem Server weiter.
- Der Schutzmodus neben der Versionsnummer; siehe [Schutzmodi](https://phishdestroy.github.io/TgWitness/de/docs/reference/panel/#protection-modes).

Der Demo-Arbeitsbereich enthält fiktive Nachrichten und stellt niemals eine Verbindung zu Telegram her. Aktionen, die einen echten Arbeitsbereich verändern würden, werden dort abgelehnt.

## Hier beginnen

Wählen Sie eine Aufgabe aus. **Mit „Mein Konto exportieren“** werden die Inhalte heruntergeladen, auf die das Konto derzeit Zugriff hat. **„Einer Untersuchung folgen“** protokolliert neue Nachrichten, beobachtete Bearbeitungen und Löschbenachrichtigungen aus den von Ihnen ausgewählten Chats. Die Einrichtungskarte zeigt die drei Schritte: Konto verbinden, Quellen auswählen, Beobachtung starten. Die Zielfrage bleibt auf dieser Seite stehen, bis Sie sie beantworten oder überspringen. Ein neuer Arbeitsbereich öffnet stattdessen die [erste Einrichtung](https://phishdestroy.github.io/TgWitness/de/docs/reference/settings/).

## Chats

Gespeicherte Unterhaltungen, standardmäßig schreibgeschützt.

- Durchsuche die Liste nach Namen oder ID. **Mit „Auswählen“** kannst du beobachtete Chats hinzufügen oder entfernen. **„Telegram-Link öffnen**“ akzeptiert einen Benutzernamen oder einen Einladungslink und speichert eine Vorschau im Journal. **„Beitreten / Öffnen und beobachten**“ tritt dem Chat bei und fügt ihn deinen Quellen hinzu; das Öffnen eines Bots sendet diesen `/start`.
- Die Chat-Kopfzeile zählt die Nachrichten **gelöscht, Text beibehalten**, **vor dem Speichern gelöscht** und **Bei erneuter Überprüfung nicht gefunden**. Die Chat-Liste und die Benachrichtigungen verwenden dieselben Definitionen. Eine gelöschte Nachricht ist rot und behält ihren gespeicherten Text bei; eine bearbeitete Nachricht behält jede gespeicherte Version bei. Jede Löschung gibt an, was bekannt ist: wann sie gesehen wurde, dass Telegram nicht meldet, wer sie gelöscht hat, oder dass nur die Benachrichtigung angekommen ist.
- **Der Ladeverlauf** zeigt die letzten 100, 250 oder 500 Nachrichten in dieser Ansicht und im Journal an. Um alle aktivierten Quellen zu laden, wählen Sie [„Quellen“ → „Vollständiger Verlauf](https://phishdestroy.github.io/TgWitness/de/docs/reference/panel/#sources)“.
- Mit **„Chat exportieren“** wird der gesamte sichtbare Verlauf als signierte `chat.json` und `chat.html`. Mehrere verbundene Konten können sich die Arbeit teilen: Jedes lädt seinen eigenen Bereich von Nachrichtennummern herunter und signiert seinen Teil, und das Konto, das den Export startet, signiert das Archiv. Siehe [„Einen Chat exportieren](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Chat-Export.md)“.
- **Unter „Personen“** werden alle Personen aufgelistet, deren Nachrichten in diesem Chat gespeichert sind. Personenprofile sind standardmäßig deaktiviert, da es sich um personenbezogene Daten Dritter handelt. Sind sie für einen Chat aktiviert, zeigt ein Profil den Namen und den Verlauf der Benutzernamen, Telegram-Flags, Avatar-Hashes, Aktivitäten, wer wem antwortet, andere beobachtete Chats sowie erwähnte Wallets, Telefonnummern, Benutzernamen und Links an. Jede Angabe verweist auf den entsprechenden Datensatz. **Beim Exportieren von Profilen** wird eine signierte Datei gespeichert, optional in einem passwortgeschützten ZIP; beim Deaktivieren der Profile wird die Profildatei gelöscht. Siehe [Personenprofile](https://phishdestroy.github.io/TgWitness/de/docs/reference/evidence/#people-profiles).
- **Profil jetzt speichern** erstellt einen Schnappschuss des Chats oder des Bot-Profils: Beschreibung, Mitglieder, Einladungslink, Bot-Befehle.

### Schreibgeschützt, Senden und Geheimnisse

Zwei Schalter oberhalb der Nachrichten schützen das Konto und den Leser:

- **Der schreibgeschützte Modus** ist aktiviert, wenn ein Chat geöffnet wird. Deaktivieren Sie diese Option, um Nachrichten zu senden oder Bot-Schaltflächen anzuklicken. Bei jeder Aktion wird gefragt: **„Als @Konto senden?**“ oder **„Diese Bot-Schaltfläche als @Konto anklicken?**“, um Sie darauf hinzuweisen, dass Chat-Teilnehmer dies sehen und dass die Aktion in das signierte Protokoll aufgenommen wird. **Die Option „In diesem Chat 10 Minuten lang nicht erneut fragen“** überspringt die Frage für eine Weile. Das Senden ist für das Ziel **„Beweismaterial für einen Fall**“ deaktiviert, sowohl im Bedienfeld als auch in der API.
- **„Mask Secrets“** verbirgt alles, was wie ein Passwort, ein Anmeldecode, ein API-Schlüssel oder Hash, ein Bot-Token, eine Sitzungs-String, ein privater Schlüssel, ein JWT oder eine Zahlungskartennummer aussieht (Kartennummern werden anhand der Luhn-Summe überprüft). **Mit „Show“** wird ein Wert angezeigt; die Anzeige wird im Journal protokolliert. Auch das Deaktivieren der Maskierung für diesen Browser wird protokolliert. Es ändert sich lediglich die Anzeige: Die ursprünglichen Datensätze und alle Exporte behalten den vollständigen Text bei.

## Protokoll

Alle vom Arbeitsbereich signierten Aufzeichnungen, sortiert nach dem neuesten Datum zuerst.

- **Die Übersicht** zählt die beobachteten Nachrichten, aufgezeichneten Bearbeitungen, Löschmeldungen und ausgewählte Quellen.
- **Ereigniszeitleiste** filtert nach Ereignistyp (alle, Bearbeitungen, Löschungen, Reaktionen, Mitgliedschaft, Berichterstattung), nach Text und nach Quelle. **Frühere Ereignisse laden** blättert zurück.
- Öffnen Sie einen Datensatz, um dessen Details, Hash und Nutzdaten anzuzeigen. **Der Link zu diesem Datensatz** ist eine Adresse, über die derselbe Datensatz geöffnet wird. Mögliche vertrauliche Informationen werden in dieser Vorschau maskiert; bei Exporten bleibt das Original erhalten.
- Das Protokoll ist schreibgeschützt: Im Bedienfeld kann kein Datensatz bearbeitet oder gelöscht werden. Überprüfen Sie dies unter **„Exporte“ → „Protokoll überprüfen“** oder `python -m tgwitness.verify`; siehe [„Exportieren und Überprüfen](https://phishdestroy.github.io/TgWitness/de/docs/reference/evidence/)“.

## Quellen

Welche Unterhaltungen dieser Arbeitsbereich aufzeichnet und welche Inhalte daraus gespeichert werden. Änderungen gelten für zukünftige Aktivitäten; gespeicherte Aufzeichnungen bleiben erhalten.

**„Chatliste aktualisieren“** liest die Chats und Ordner des Kontos aus. Es werden keine Nachrichten heruntergeladen.

### Geltungsbereich

- **Was dieses Konto aufzeichnet** : **Ausgewählte Chats** (nur die Chats, die Sie hinzufügen), **Telegram-Ordner** (einer der Ordner des Kontos, einschließlich der Chats, die später hinzugefügt werden) oder **Gesamter Beitrag** (jeder Chat sowie jeder neue Chat, jede neue Gruppe, jeder neue private Chat oder jeder neue Bot, sobald er erscheint). **Untersuchungsmodus** ist für ein dediziertes Konto vorgesehen: Es zeichnet alles auf, was das Konto sieht, seine eigenen Nachrichten und Tastendrücke, und speichert das Profil jedes neuen Chats sowie die zuvor sichtbaren Nachrichten sofort. Das [Spezieller Leitfaden für Konten](https://phishdestroy.github.io/TgWitness/docs/dedicated-account/) erklärt, warum du niemals dein Hauptkonto verwenden solltest.
- **Quellentypen** beschränken den Ordner- und den Gesamtkonto-Modus auf Kanäle, Gruppen, private Chats und Bots. **„Eigene Aktionen“** fügt die eigenen Nachrichten, Bearbeitungen und Tastenanschläge bei Antworten des Kontos hinzu.
- **Wenn ein neuer Chat oder Bot erscheint**: Speichere dessen Profil und bis zu der gewählten Anzahl seiner zuletzt sichtbaren Nachrichten.

Einschränkungen: Geheime Chats werden niemals an TgWitness übermittelt. Es wird nichts aufgezeichnet, solange TgWitness nicht läuft; nach einem Neustart holt es nur das nach, was Telegram noch zurückgibt, und der Bericht zeigt die Lücke an. Chats, die über das Limit der Chat-Liste hinausgehen (1.000 Dialoge, sofern nicht in den Parametern geändert), werden hinzugefügt, sobald sie das nächste Mal aktiv werden. Inline-Bot-Schaltflächen, die in einer anderen App gedrückt werden, sind unsichtbar; die Antwort des Bots wird jedoch aufgezeichnet.

### Betroffene Chats

Filtern Sie nach Status (**Aktiviert**, **Pausiert**, **Priorität**, **Ausgeschlossen**, **Unbestätigter Zugriff**, **Ignoriert**) und Typ und führen Sie dann Aktionen für eine Auswahl durch: aktivieren, pausieren, Priorität setzen oder entfernen, aus dem Umfang ausschließen oder entfernen. Das Status-Symbol zeigt nur den Status an; Aktionen befinden sich im Menü jeder Zeile mit einer Beschreibung ihrer Funktion. Das Pausieren und Ausschließen erfordert eine Bestätigung, auch bei Massenaktionen. Beim Entfernen einer Quelle wird nach deren Namen gefragt und die zugehörigen Personenprofile gelöscht; die gespeicherten Einträge verbleiben im Journal.

Eine Quelle, die nicht in der Chat-Liste des Kontos angezeigt wird, ist **Empfang von Updates, die nicht in der Chat-Liste erscheinen**, während weiterhin Aufzeichnungen eingehen; andernfalls **Zugriff unbestätigt**. **Verfügbare Chats** fügt Chats mit **Ausgewählte hinzufügen** oder **Alle Treffer hinzufügen** hinzu.

### Vollständiger Verlauf

Lädt den verfügbaren Verlauf jeder aktivierten Quelle in „Chats“ und das Journal. Der Fortschritt bleibt nach einem Neustart erhalten; Anhänge richten sich nach Ihren Medieneinstellungen. Siehe [Quellenverlauf](https://phishdestroy.github.io/TgWitness/de/docs/reference/history/).

### Aufzeichnung

- **Wählen Sie aus, welche Änderungen beibehalten werden sollen**: neue Nachrichten, Bearbeitungen, Löschbenachrichtigungen, sichtbare Reaktionen, Beitritte und Austritte. Eine Voreinstellung ändert das Formular; **mit „Aufzeichnungseinstellungen speichern“** wird sie übernommen. Das erneute Aktivieren einer Kategorie stellt verpasste Ereignisse nicht wieder her.
- **Medien nach Möglichkeit sichern**: Anhänge bis zu einer bestimmten Dateigröße herunterladen, pro Typ zwischen 1 und 2.000 MiB festlegen und die Videolänge in Sekunden begrenzen (0 bedeutet keine Begrenzung). Jeder Download-Versuch wird mit einem Ergebnis protokolliert.
- **Überprüfung**: Prioritätschats alle paar Minuten, andere Chats selten, damit das Konto die „FloodWait“-Grenzen von Telegram nicht überschreitet. Mit „0“ wird eine Gruppe deaktiviert. Markieren Sie Prioritätschats in der Liste mit dem Stern; die Anzahl der Chats pro Durchlauf und die Pause zwischen den Chats finden Sie unter „Parameter“. Siehe [Sammlung](https://phishdestroy.github.io/TgWitness/de/docs/reference/collection/).

## Exporte

**Unter „Downloads“** werden Dateien vorbereitet; unter **„Build-Bericht“** wird festgelegt, wie die Berichte aussehen sollen.

| Was | Verwenden Sie es für | Anleitung |
| --- | --- | --- |
| Kontoexport | Ein aktueller Überblick darüber, was das Konto derzeit lesen kann | [Kontoexport](https://phishdestroy.github.io/TgWitness/de/docs/reference/account-export/) |
| Kopie teilen | Eine vereinfachte Version eines fertigen Kontoexports | [Offenlegung](https://phishdestroy.github.io/TgWitness/de/docs/reference/account-export/#prepare-a-disclosure-for-a-lawyer-or-another-recipient) |
| Signiert ZIP | Journal, Bericht, Anhänge und Verifizierungstools innerhalb einer festen Journalgrenze | [Exportieren und überprüfen](https://phishdestroy.github.io/TgWitness/de/docs/reference/evidence/) |
| Bericht im HTML-, PDF- und JSON-Format | Ein versiegelter, lesbarer Bericht | [Fallberichte](https://phishdestroy.github.io/TgWitness/de/docs/reference/case-reports/) |
| JSONL, CSV | Originalaufzeichnungen mit Signaturen; eine formelsichere Tabellenkalkulation | [Exportieren und überprüfen](https://phishdestroy.github.io/TgWitness/de/docs/reference/evidence/) |
| Auszug aus der Übergabe | Nur die Chats, Zeiträume und Personen, die ein Empfänger benötigt | [Beweismittel](https://phishdestroy.github.io/TgWitness/de/docs/reference/evidence/#investigation-handoff) |
| Chat-Export | Ein Chat als signierte Datei `chat.json` und `chat.html` | [Einen Chat exportieren](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Chat-Export.md) |

- **Die Verschlüsselung der oben genannten Downloads mit einem Passwort** (mindestens 12 Zeichen) speichert eine AES-256-Datei ZIP, die mit 7-Zip oder WinRAR geöffnet werden kann. Die darin enthaltene signierte Datei bleibt unverändert. Das Passwort wird nicht gespeichert.
- **Vorbereitete Exporte** speichern bis zu 20 Dateien mit einer Gesamtgröße von bis zu 2 GiB sowie die aktuellste Datei für wiederholte Downloads, jeweils mit einem SHA-256. Die Vorbereitung einer Datei stellt keine Zustellung dar.
- Wenn der Browser den Speicherdialog ablehnt, weicht das Panel auf einen normalen Download aus.
- **Ihre Signaturidentität** zeigt den Schlüssel-Fingerabdruck an. **Checkpoint speichern** und **Signierte Ausführungsbestätigung herunterladen** liefern Ihnen Aufzeichnungen, die Sie außerhalb des Collectors aufbewahren können. **Anfrage für Zeitstempel vorbereiten** erstellt eine RFC-3161-Anfrage, ohne einen Dienst zu kontaktieren.

## Einstellungen, Konten und Verbindung

- **Einstellungen**: Ziel, Verbindung, Aufzeichnungsumfang und Benutzeroberfläche. Siehe [„Erste Einrichtung und Einstellungen](https://phishdestroy.github.io/TgWitness/de/docs/reference/settings/)“.
- **Konten**: Jeder Arbeitsbereich mit seinem Status, seinen Quellen, Ereignissen und der Anhangswarteschlange. Filtern nach **„Erfordert Aufmerksamkeit“**, **„Wird gesammelt“**, **„Offline“ oder „Pausiert“** oder **„Nicht verbunden“**, eine Auswahl pausieren oder fortsetzen, Kontodateien in großen Mengen importieren und Gruppen verwalten. Siehe [Konten](https://phishdestroy.github.io/TgWitness/de/docs/reference/accounts/).
- **Konto**: Anmeldung und Verbindungsroute dieses Kontos. Direkt, ein WireGuard- Profil, Ihr eigener Proxy, der öffentliche MTProto-Pool oder WARP; bereiten Sie eine Route vor, prüfen Sie sie und wenden Sie sie dann auf dieses Konto, eine Gruppe oder alle Konten an. Siehe [„Verbindung“ und „](https://phishdestroy.github.io/TgWitness/de/docs/reference/connection/)[Proxys](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Proxies.md)“.

## Extras

Optional: Ein Konto und Quellen reichen aus, um mit dem Sammeln zu beginnen. Nur die von Ihnen gewählte Option öffnet ihre Einstellungen, und es wird nichts automatisch verbunden. Die Karte **„Schutzstufe“** oben zeigt den [Schutzmodus](https://phishdestroy.github.io/TgWitness/de/docs/reference/panel/#protection-modes) an.

| Karte | Was es bietet | Anleitung |
| --- | --- | --- |
| Speicher & Speicherplatz | Backups, das Verschieben älterer Dateien in Ihre Cloud, eine Beweiskopie, die nicht gelöscht werden kann | [Speicher](https://phishdestroy.github.io/TgWitness/de/docs/reference/storage/) |
| Ziel & Schutzstufe | Empfohlene Einstellungen für Ihr Ziel und zwei Skalen | [unten](https://phishdestroy.github.io/TgWitness/de/docs/reference/panel/#goal-and-protection-level) |
| Benachrichtigungen | Probleme, geänderte Nachrichten und eine tägliche Zusammenfassung; dein eigener Kontrollbot | [unten](https://phishdestroy.github.io/TgWitness/de/docs/reference/panel/#notifications) |
| Beweismaterial & Backups | Zeitstempel, weitere Zeugen und eine verschlüsselte externe Kopie | [unten](https://phishdestroy.github.io/TgWitness/de/docs/reference/panel/#evidence-and-backups) |
| Server rund um die Uhr | Ein Cloud-Server ohne SSH, der über das Panel erstellt und gelöscht wird | [Hohe Sicherheit](https://phishdestroy.github.io/TgWitness/de/docs/reference/high-assurance/#from-the-panel) |
| Unabhängiger Zeuge | Signierte Checks, die in Ihrem Telegram-Kanal oder auf Discord veröffentlicht werden | [Witness](https://phishdestroy.github.io/TgWitness/de/docs/reference/witness/) |
| Code-Prüfung | Vergleicht das laufende Programm mit einem öffentlichen GitHub-Commit | [unten](https://phishdestroy.github.io/TgWitness/de/docs/reference/panel/#code-check) |

### Ziel und Schutzstufe

Vier Fragen:

1. **Wozu dient es? Als** persönliches Protokoll, für Ermittlungen oder als Beweismaterial für einen Fall.
2. **Wie viel möchten Sie beobachten?** Einige Chats (bis zu etwa 50), viele Chats (bis zu etwa 500) oder ganze Konten. Dadurch wird die Obergrenze für die Chat-Liste auf 1.000, 3.000 oder 20.000 festgelegt.
3. **Fotos und Dateien?** Nur Text, Fotos und kurze Medien (Fotos 20 MB, Videos 100 MB) oder alles (Videos und Dokumente mit jeweils bis zu 1 GB). Bei der Option „Alles“ mit ganzen Konten bleiben zudem 4 GiB Speicherplatz frei.
4. **Wo läuft es? Auf** diesem Computer oder auf einem Server, der ständig in Betrieb ist.

Der Vorschlag listet unabhängige Zeitstempel, „drand“ und die Geräteliste von Telegram auf, jeweils mit einer Zeile dazu, was hinzugefügt wird. Zeitstempel werden alle 60, 30 oder 10 Minuten für eine persönliche Aufzeichnung, eine Untersuchung oder Beweismittel gesetzt; „drand“ und die Geräteliste benötigen Zeitstempel. **Anwenden** ändert nur diese, die Anhangsrichtlinie und die beiden oben genannten Parameter. Jede Änderung ist ein Journaleintrag, dazu `setup.applied`. Benachrichtigungen, eine externe Kopie, ein Server, Gateway-DNS, die Codeüberprüfung und ein Zeuge werden als nächste Schritte mit eigenen Formularen angeboten.

Zwei Skalen werden anhand der festgelegten Werte berechnet, nicht anhand des Ziels:

| Umfang | Punkte |
| --- | --- |
| Glaubwürdigkeit | Signiertes Journal 1, Zeitstempel 3, drand 1, Geräteliste 1, Code-Prüfung, die übereinstimmt 1, Witness-Abfrage 1, beglaubigter Server 2, Gateway-DNS-Protokoll 1 |
| Zuverlässigkeit | Ständig aktiver Server 3, externe Kopie 3, Object Lock 1, Problembenachrichtigungen 1 |

**Maximal** 80 % Lesezugriffe, 50 % **hoch**, 25 % **mittel**, darunter **grundlegend**. Die Zuverlässigkeit berücksichtigt derzeit einen stets aktiven Server gemäß der Antwort auf Frage 4, bevor ein Server überprüft wird.

### Benachrichtigungen

Benachrichtigungen werden über Apprise an Telegram, Discord, Slack, ntfy, E-Mail, Matrix und über 100 weitere Dienste gesendet. Wählen Sie einen Dienst aus, füllen Sie ein oder zwei Felder aus und senden Sie einen Test, oder fügen Sie Apprise-Adressen direkt ein.

- **Probleme**: Festplatte fast voll, Konto abgemeldet, Fehler beim Erfassen, Kopieren oder beim Zeitstempel. Auf einem abgeschotteten Server stellen ein offener SSH-Port oder eine Anmeldung ebenfalls ein Problem dar.
- **Änderungen**: gelöschte, bearbeitete und fehlende Nachrichten in beobachteten Chats, zusammengefasst in einer Benachrichtigung pro Überprüfung (jede Minute, sofern in den Parametern nicht anders festgelegt).
- **Abgeschlossene Aufgaben**: Verlauf, Exporte und Sicherungskopien.
- **Tägliche Zusammenfassung** zur gewählten Uhrzeit (Serverzeit).

Benachrichtigungen enthalten Chat-Namen und Anzahlangaben. Nachrichtenauszüge sind standardmäßig deaktiviert; wenn sie aktiviert sind, verlässt der Nachrichtentext diesen Rechner.

**Dein Operator-Bot** ist ein eigener Bot von @BotFather, der `/status` und `/stats`und optional `/pause`, `/resume` und `/copy`. Nur die aufgeführten Chats und Telegram-Benutzer-IDs können ihn nutzen; der Gesprächstext verbleibt im Arbeitsbereich. Verwenden Sie einen separaten Bot, wenn eine andere Anwendung dessen Befehle bereits empfängt. Siehe [Benachrichtigungen](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Notifications.md) und [Operator-Bot](https://phishdestroy.github.io/TgWitness/de/docs/reference/storage/#operator-bot-and-completion-notices).

### Beweismaterial und Backups

- **Unabhängige Zeitstempel** sendet nur das SHA-256 jedes signierten Checkpoints an RFC 3161- Autoritäten und OpenTimestamps-Kalender, alle 5 bis 1.440 Minuten. **Jetzt verankern** führt einen Durchlauf durch. Siehe [Zeitstempel](https://phishdestroy.github.io/TgWitness/de/docs/reference/timestamp/).
- **Weitere Zeugen**, die jeweils deaktiviert sind, bis sie ausgewählt werden: die neueste „drand“-Runde, Telegrams Liste der angemeldeten Geräte ohne IP-Adressen und das Protokoll der Cloudflare Gateway-DNS-Abfragen des Servers . Siehe [optionale Aufzeichnungen](https://phishdestroy.github.io/TgWitness/de/docs/reference/evidence/#optional-records-in-evidence-mode-drand-and-telegram-devices).
- **Die verschlüsselte Sicherung** kopiert das Journal, die Dateien, die Checkpoints und die Chat-Exporte in einen S3-kompatiblen Speicher (Wasabi, Amazon S3, Backblaze B2, Cloudflare R2, MinIO). Alles wird zunächst auf diesem Rechner verschlüsselt. **Laden Sie den Verschlüsselungsschlüssel herunter** und bewahren Sie ihn getrennt auf: Ohne ihn kann die Kopie nicht gelesen werden. „Object Lock“ im Governance- oder Compliance-Modus verhindert das Löschen von Objekten für eine festgelegte Anzahl von Tagen. Siehe [externe Kopie](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Off-site-Copy.md).

### Code-Prüfung

Prüft, ob das installierte Programm mit einer veröffentlichten Version übereinstimmt.

1. Geben Sie ein GitHub-Repository (das offizielle ist bereits eingetragen) sowie ein Tag, einen Branch oder einen Commit ein.
2. **Jetzt prüfen** fragt über die Route dieses Arbeitsbereichs für externe Anfragen die GitHub-API ab, um die Dateiliste dieses Commits abzurufen. Es vergleicht die Git-Blob-ID jeder gemessenen Programmdatei mit dem Commit. Ein Windows-Checkout mit konvertierten Zeilenenden passt weiterhin.
3. Das Ergebnis listet geänderte, zusätzliche und fehlende Dateien auf (jeweils bis zu 50) und wird als ein `source.checked` Protokoll.

Das Ergebnis gilt nur so lange als aktuell, wie die ausgeführten Programmdateien unverändert bleiben: Überprüfen Sie dies nach einem Update erneut. Es wird kein Token benötigt und es funktionieren nur öffentliche Repositorys; Chats und Anmeldedaten werden nicht hochgeladen. Eine Übereinstimmung identifiziert den Code auf der Festplatte. Es handelt sich nicht um eine Hardware-Attestierung; dazu siehe [Phala Cloud](https://phishdestroy.github.io/TgWitness/de/docs/reference/high-assurance/#confidential-vm-on-phala-cloud-intel-tdx).

## Schutzmodi

Der Umschalter neben der Versionsnummer zeigt den gewählten Modus an und wie viele der 18 Schutzebenen aktiv sind, zum Beispiel `🟠 Witnessed 9/18`. **Das Ändern des Modus** unter **„Extras“ → „Schutzstufe“** öffnet die Auswahl. Ein Modus beschreibt ein Ziel und listet auf, was noch fehlt; Aufzeichnung, Signierung und gespeicherte Einstellungen sind in jedem Modus identisch.

| Modus | Für | Fügt hinzu |
| --- | --- | --- |
| 🟢 Einfach | Einen Chat beobachten und eine Kopie aufbewahren | Chats, das Tagebuch und Chat-Exporte; die Signierung läuft im Hintergrund |
| 🟡 Signiert | Meldungen an eine Plattform, einen Host oder eine Missbrauchsstelle | Signiertes Archiv, Journalprüfung, Checkpoints, Übergabeauszug |
| 🟠 Beglaubigt | Fälle, in denen jemand behaupten könnte, der Datensatz sei verändert worden | Ein unabhängiger Zeuge, der signierte Journal-Köpfe veröffentlicht |
| 🔴 Gerichtsfähig | Beweismaterial für einen Anwalt, die Polizei oder ein Gericht | Zeitstempel, eine verschlüsselte externe Kopie, Falldetails in Berichten |
| 🟣 Von GitHub verifiziert | Aufzeichnungen, deren Software jeder überprüfen können muss | Code-Prüfung und Erfassung von GitHub Actions |
| ⚫ Mossad | Fälle mit hohem Einsatz gegen einen finanzstarken Gegner | Ein abgeschotteter 24/7-Server, eine versteckte IP-Adresse, alle 18 Ebenen |

Die Ebenen: jeder Datensatz wird signiert und verkettet; eine signierte Ausführungsbestätigung; Anhänge, die mit SHA-256 gespeichert werden; signierte Checkpoints; Nachprüfungen; Problemwarnungen; schreibgeschützter Witness-Zugriff; ein Witness, der planmäßig überprüft; RFC-3161-Zeitstempel; OpenTimestamps-Nachweise; ein verifizierter aktueller Zeitstempel; eine verschlüsselte externe Kopie; Fall-Details in Berichten; eine Code-Übereinstimmungsprüfung ; Telegram sieht die IP-Adresse dieses Geräts niemals; externe Anfragen über einen Proxy; Object Lock auf der Kopie; ein versiegelter Server mit Anbieterdaten. Eine deaktivierte Ebene verfügt über **„Einrichten“**, wodurch das entsprechende Formular geöffnet wird. Die Auswahl eines niedrigeren Modus erfordert eine Bestätigung und löscht nichts.

## Weitere Tools

- **Das Archiv abfragen**: Gespeicherte Beobachtungen durchsuchen, die Quellen prüfen und dann entscheiden, ob sie an ein KI-Modell gesendet werden sollen. Siehe [Archivanalyse](https://phishdestroy.github.io/TgWitness/de/docs/reference/analysis/) sowie [lokale OCR und Transkription](https://phishdestroy.github.io/TgWitness/de/docs/reference/media-analysis/).
- **Parameter**: Begrenzungen und Tempo der Datenerfassung, erneute Überprüfungen, Downloads, Profile, Benachrichtigungen und Exporte. Suche nach Namen, Anzeige von **„Nur geänderte** Werte“ und Vorbereitung der Standardeinstellungen als Entwurf mit **„Standardeinstellungen wiederherstellen…“.** Mit**„Parameter speichern“** werden die Werte ab der nächsten Verwendung übernommen, und jede Änderung wird in einem Protokoll vermerkt.
- **Zugriff**: separate Tokens für Prüfer, Analysten und Betreiber, beschränkt auf ausgewählte Arbeitsbereiche, Chats und Berechtigungen. Siehe [„Zugriff](https://phishdestroy.github.io/TgWitness/de/docs/reference/access/)“.
- **Systemprotokoll** : Was dieser Prozess seit seinem Start getan hat (Verbindungen, Proxy-Änderungen, Anmeldungen, Ablehnungen, Einstellungsänderungen), wobei die IP-Adressen verborgen bleiben. **„Follow new lines“** sorgt dafür, dass die neueste Zeile im Blickfeld bleibt. Nachrichten verbleiben ausschließlich im Journal.
- **Integrationen**: der KI-Anbieter, [schreibgeschützte MCP-Verbindungen](https://phishdestroy.github.io/TgWitness/de/docs/reference/mcp/) und [signierte Webhooks](https://phishdestroy.github.io/TgWitness/de/docs/reference/webhooks/).
- **Case Board**: private Teamnotizen, Lesezeichen und Ausschnitte neben den Beweismitteln. Siehe [Case Board](https://phishdestroy.github.io/TgWitness/de/docs/reference/case-board/).
- **GitHub Actions-Erfassung** unter „Exports“: ein aus Ihrem Fork erfasster Chat. Siehe [„Sealed Capture](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md)“.
