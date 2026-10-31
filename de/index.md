# Nachrichten ändern sich. Bewahren Sie fest, was Sie gesehen haben.

Canonical page: https://phishdestroy.github.io/TgWitness/de/

[Open Source / v0.7.0](https://phishdestroy.github.io/TgWitness/de/docs/reference/changelog/)

Telegram-Nachrichten erfassen, deren Änderungen dokumentieren und einen signierten Datensatz exportieren.

[Demo öffnen:](https://phishdestroy.github.io/TgWitness/demo/?lang=de)[Einrichtungsanleitung](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=de)

Die Demo verwendet fiktive Daten. Eine Anmeldung bei Telegram ist nicht erforderlich.

 [Erfassung mit GitHub Actions (Vorschau)](https://phishdestroy.github.io/TgWitness/de/docs/capture/) [S3-Offsite-Kopie: Einrichtung und Wiederherstellung](https://phishdestroy.github.io/TgWitness/de/#s3)

EINE NACHRICHT DURCH DIE ZEIT #0042

Northstar · ForschungFiktive Quelle / Nachricht 42

1. **Beobachtete Nachricht:**09:41:02

   Die Einweisung beginnt bei 14:00.
2. **Bearbeitung beibehalten**09:43:18

   Die Einweisung beginnt bei 15:00.

   Vorherige Version beibehalten
3. **Löschhinweis**10:06:45

   Die erfassten Inhalte verbleiben in Ihrem Protokoll.

Drei Beobachtungen. Eine Geschichte. BEISPIEL

Die Nachricht verschwindet. Der aufgezeichnete Verlauf bleibt erhalten.

## Jede erfasste Änderung. Genau dort, wo Sie sie benötigen.

Sehen Sie sich die Benutzeroberfläche mit fiktiven Demonstrationsdaten an.

TgWitness / Gespeicherte ChatsIHR ARBEITSBEREICH FÜR BEOBACHTUNGEN

![Gespeicherte Telegram-Konversationen im „Dark Theme“, wobei erfasste Bearbeitungen und gelöschte Nachrichten im Kontext erhalten bleiben](https://phishdestroy.github.io/TgWitness/assets/chats-dark.png)

01 / Gespeicherte Chats Eine vertraute Konversationsansicht, in der neben den Nachrichten auch erfasste Bearbeitungen und Löschhinweise angezeigt werden.

TgWitness / ProtokollLOKALER ARBEITSBEREICH

![Protokoll mit erfassten Nachrichten, Bearbeitungen, Löschmeldungen und erfassten Ereignissen](https://phishdestroy.github.io/TgWitness/assets/workspace.png)

02 / Protokoll: Eine durchsuchbare Zeitleiste der von Ihrem Konto erfassten Ereignisse, einschließlich Unterbrechungen.

TgWitness / BearbeitungsverlaufLOKALER ARBEITSBEREICH

![Detailansicht, in der die erfasste ursprüngliche und die bearbeitete Version einer Nachricht miteinander verglichen werden](https://phishdestroy.github.io/TgWitness/assets/detail.png)

03 / Bearbeitungshistorie: Vergleichen Sie erfasste Versionen, ohne die frühere Aufzeichnung zu überschreiben.

TgWitness / Signierte ExporteLOKALER ARBEITSBEREICH

![Exportfunktion für den Arbeitsbereich mit signierten Dateien im ZIP-, JSONL- und CSV-Format sowie einem Offline-HTML-Bericht](https://phishdestroy.github.io/TgWitness/assets/exports.png)

04 / Signierte Exporte Nehmen Sie das Protokoll mit – inklusive eines Manifests und eines unabhängigen Prüfers.

01 / ERFASSUNG

### Sie bestimmen den Umfang.

Ausgewählte Chats, ein Telegram-Ordner oder das gesamte Konto. Ein separater Arbeitsbereich für jedes Konto.

[Vergleichen Sie die Erfassungsmodi:](https://phishdestroy.github.io/TgWitness/de/guides/modes.html#scope)

02 / PRESERVE

### Änderungen tragen zur Geschichte bei.

Erfasste Versionen, Löschhinweise und Beobachtungslücken verbleiben im Protokoll.

[Siehe die Ereignismatrix](https://phishdestroy.github.io/TgWitness/de/guides/modes.html#events)

03 / ÜBERGABE

### Eine Aufzeichnung, die weitergereicht wird.

Signierte ZIP-Datei, erhaltene Dateien und ein Offline-Bericht. Optionaler Passwortschutz.

[exportieren und verifizieren](https://phishdestroy.github.io/TgWitness/de/docs/exports/)

## Ändern Sie ein Byte. Die Blockchain informiert Sie darüber.

Jedes Ereignis ist mit dem vorherigen Hash verknüpft und trägt eine Ed25519-Signatur.

![Erfasste Ereignisse sind mit früheren Hashes verknüpft, tragen Signaturen und werden in einem überprüfbaren Export bereitgestellt.](https://phishdestroy.github.io/TgWitness/assets/evidence-chain-animated.svg)

![Das Ändern eines erfassten Datensatzes verändert dessen Hash-Wert und macht die Überprüfung des verknüpften Datensatzes unmöglich.](https://phishdestroy.github.io/TgWitness/assets/evidence-tamper-animated.svg)

![Ein separat gespeicherter Kontrollpunkt ermöglicht es dem Empfänger, das exportierte Protokoll mit einer früheren Beobachtung zu vergleichen.](https://phishdestroy.github.io/TgWitness/assets/evidence-checkpoint-animated.svg)

Erfahren Sie, was die einzelnen Verifizierungsmechanismen leisten und wo ihre Grenzen liegen.

[Entdecken Sie acht Beweisstufen:](https://phishdestroy.github.io/TgWitness/de/guides/modes.html#levels)

## Bereit für eine zweite Überprüfung.

Übergeben Sie Beobachtungen, Dateien und einen Offline-HTML-Bericht in einem signierten Paket.

[Lesen Sie das Beweismodell](https://phishdestroy.github.io/TgWitness/de/docs/reference/evidence/)

tgwitness-evidence.zipSIGNED BUNDLE

- 01

  Ursprüngliche BeobachtungenJSONL-Datensätze + CSV-Tabelle
- 02

  Lesbarer KontextOffline-HTML-Bericht + erhaltene Medien
- 03

  Unabhängige ÜberprüfungSigniertes Manifest + eigenständiger Verifizierer

Signaturen erkennen Manipulationen im Vergleich zu einem vertrauenswürdigen Schlüssel. Sie beweisen weder die Herkunft aus Telegram noch garantieren sie eine vollständige Erfassung. Der Inhalt des Protokolls und die Medien erfordern eine von Ihnen bereitgestellte verschlüsselte Speicherung.

## S3-Kopien. Externe Überprüfungen.

Bewahren Sie verschlüsselte Kopien auf und führen Sie unabhängige Überprüfungen durch.

Standardmäßig deaktiviert

### Kopieren Sie alles in einen S3-kompatiblen Speicher

Protokoll, Dateien, zeitgestempelte Kontrollpunkte und Chat-Exporte – verschlüsselt vor dem Hochladen auf AWS S3 oder einen kompatiblen Speicher.

**Speichereinstellungen und Wiederherstellung**

Clientseitige Verschlüsselung

`AES-256-GCM` verschlüsselt Objekte auf diesem Rechner. Der Anbieter erhält verschlüsselte Objekte.

Geplante oder manuelle Kopien

Jetzt kopieren oder ein Intervall zwischen 1 und 1.440 Minuten auswählen. Überprüfen Sie den Fortschritt im Bedienfeld.

Object Lock

Wählen Sie die Aufbewahrungsdauer in Tagen und einen Modus aus, sofern der Speicherbereich dies unterstützt. Das Bedienfeld zeigt an, ob die Aufbewahrung für ein hochgeladenes Objekt bestätigt wurde.

Verifizierte Wiederherstellung

Laden Sie den Verschlüsselungsschlüssel herunter und bewahren Sie ihn separat auf. Stellen Sie die Daten auf einem anderen Rechner wieder her; die Dateien werden erst nach Überprüfung veröffentlicht.

![Vollständiges Off-Site-Kopier-Panel: Endpunkt, Region, Bucket, Zugriffsschlüssel, Zeitplan, „Object Lock“- und Wiederherstellungsschlüssel-Steuerelemente](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)

Das vollständige Bedienfeld mit erweiterten Optionen ist aufgeklappt. Es werden keine Anmeldedaten für den Speicher angezeigt.

Zeitschrift und Medien`AES-256-GCM`S3-kompatibler Speicher

[S3 konfigurieren und eine Kopie wiederherstellen:](https://phishdestroy.github.io/TgWitness/de/docs/exports/#s3)[Lesen Sie die Details zur Verifizierung unter](https://phishdestroy.github.io/TgWitness/de/docs/reference/evidence/#off-site-copy-and-restore-s3)

**Funktionsumfang:** Das Tool **führt** ohne den exportierten Entschlüsselungsschlüssel keine Wiederherstellung **durch** und ersetzt keinen unabhängigen Zeugen.

### Benachrichtigungen · Apprise

Problembenachrichtigungen, Änderungen im Chat und tägliche Zusammenfassungen über Apprise: per Messenger, E-Mail oder über Ihren eigenen JSON-Webhook.

**Funktionsumfang:** Der Text der Nachrichten wird nicht gesendet, es sei denn, Sie aktivieren die Anzeige von Auszügen.

 [Benachrichtigungsempfänger konfigurieren](https://phishdestroy.github.io/TgWitness/de/docs/reference/operations/#notifications)

### Externe Zeitstempel

Zeitstempel-Checkpoint-Hashes gemäß RFC 3161 und OpenTimestamps.

**Gilt nicht**: Eine ausstehende Kalenderbestätigung wird nicht als bestätigter Bitcoin-Zeitstempel behandelt.

 [Überprüfen Sie die Zeitstempel-Nachweise unter](https://phishdestroy.github.io/TgWitness/de/docs/reference/timestamp/)

### Unabhängiger Zeuge

Ein separater Host speichert die signierten Beobachtungen und kann „`TGW1`“-Checkpoints veröffentlichen.

**Dies ist nicht der Fall**: Es werden zwei Arbeitsbereiche auf einem Collector-Host nicht zu unabhängigen Zeugen gemacht.

 [Richten Sie ein Witness-Konto ein:](https://phishdestroy.github.io/TgWitness/de/docs/witness/)

### Wiederherstellung und erkennbare Lücken

Fortsetzung nach Neustart. Nachprüfungen und „`coverage.json`“ zeigen wiederhergestellte Nachrichten und Lücken an.

**Was** das Tool **nicht leistet:** Es rekonstruiert nicht jede versäumte Bearbeitung oder verschwundene Nachricht.

 [Überprüfen Sie Kontinuität und Lücken](https://phishdestroy.github.io/TgWitness/de/guides/modes.html#continuity)

## Hier beginnt Ihr erster Arbeitsbereich.

Sehen Sie sich zunächst die Demo an. Verbinden Sie ein eigenes Konto, sobald Sie bereit sind. Windows, Linux, macOS oder Docker.

[Lesen Sie die Einrichtungsanleitung](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=de)

**Eine importierte Sitzung, ein laufender Client.**

Führen Sie einen importierten TData-/Sitzungsschlüssel nicht gleichzeitig in Telegram Desktop und TgWitness aus. Telegram kann die gemeinsame Autorisierung ungültig machen (AUTH_KEY_DUPLICATED). Für die parallele Nutzung erstellen Sie bitte einen separaten TgWitness-Zugang per Telefon oder QR-Code.

[Lesen Sie die Warnung zum Import von Sitzungen](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=de#session-warning)

**Werfen Sie einen Blick darauf, bevor Sie eine Verbindung herstellen.**

Probieren Sie den fiktiven Arbeitsbereich ohne Telegram-Konto aus.

[Online-Demo öffnen →](https://phishdestroy.github.io/TgWitness/demo/?lang=de)

Windows `scripts\Demo.cmd`Linux / macOS `sh start.sh --demo`

**Befehle zur lokalen Installation**

SCHRITT 01

### Hier finden Sie den Quellcode.

[Laden Sie die ZIP-Datei mit dem Quellcode herunter](https://github.com/phishdestroy/TgWitness/archive/refs/heads/main.zip) und entpacken Sie sie, oder klonen Sie das Repository:

```
git clone https://github.com/phishdestroy/TgWitness.git
cd TgWitness
```

Für den Start des Programms ist Python 3.11+ erforderlich. Der Windows-Launcher bietet eine Installation an, falls Python nicht vorhanden ist.

[Veröffentlichungen durchsuchen](https://github.com/phishdestroy/TgWitness/releases)

Kein Python unter Windows? [Laden Sie das portable Paket herunter](https://github.com/phishdestroy/TgWitness/releases/download/v0.7.0/TgWitness-0.7.0-windows-amd64-portable.zip), entpacken Sie es und doppelklicken Sie auf „`TgWitness.cmd`“.

SCHRITT 02

### Wählen Sie die Ausführungsart.

Doppelklicken Sie auf „`Start.cmd`“ oder führen Sie den Befehl in PowerShell aus:

```
.\Start.cmd
```

Sie möchten sich nur umsehen? Doppelklicken Sie auf „`scripts\Demo.cmd`“, um eine isolierte Demo aufzurufen. Eine Telegram-Anmeldung ist nicht erforderlich.

Verfügbar mit Python 3.11+ und „`venv`“:

```
sh start.sh
```

Um stattdessen das fiktive Protokoll zu öffnen, führen Sie bitte den Befehl „`sh start.sh --demo`“ aus.

Bei laufendem Docker und installierter Compose-Version 2.20+:

```
docker compose up -d --build --wait
docker compose exec tgwitness cat /data/panel-token.txt
```

Der zweite Befehl zeigt Ihr privates Panel-Token an. Bewahren Sie es auf Ihrem Rechner auf.

Öffnen Sie nach dem Start [127.0.0.1:8787](http://127.0.0.1:8787).

Bei der Installation aus dem Quellcode lautet das Token „`data/live/panel-token.txt`“. Für die Telegram-Anmeldung können Sie die integrierten API-Einstellungen oder Ihr eigenes Schlüsselpaar von [my.telegram.org](https://my.telegram.org) verwenden. [Vollständige Einrichtungsanleitung ↗](https://phishdestroy.github.io/TgWitness/de/docs/reference/quickstart/)

**TgWitness 0.7.0** [Was gibt’s Neues →](https://phishdestroy.github.io/TgWitness/de/docs/reference/changelog/) · [Funktionen und bekannte Einschränkungen →](https://phishdestroy.github.io/TgWitness/de/docs/reference/features/)

## Klare Anweisungen. Ein nützlicher nächster Schritt.

[Entdecken Sie die Anleitungen ↗](https://phishdestroy.github.io/TgWitness/de/docs/)

[### Modi, Szenarien und Beweisstufen Vier Erfassungsmodi. Acht Verifizierungsstufen. Finden Sie den passenden Arbeitsablauf für Ihren Fall.](https://phishdestroy.github.io/TgWitness/de/guides/modes.html)

[01 ### Ein Konto verbinden Import von Telefon-, QR- und unterstützten Sitzungsdaten.](https://phishdestroy.github.io/TgWitness/de/docs/accounts/)[02 ### Wählen Sie einen Proxy Öffentliche MTProxy-Listen oder Ihre eigene Route.](https://phishdestroy.github.io/TgWitness/de/docs/proxies/)[03 ### Einen Witness-Bot einrichten Signierte Kontrollpunkte in Ihrem Telegram-Kanal.](https://phishdestroy.github.io/TgWitness/de/docs/witness/)[04 ### Exportieren und verifizieren Teilen Sie den erfassten Verlauf und überprüfen Sie dessen Integrität.](https://phishdestroy.github.io/TgWitness/de/docs/exports/)

## Das Archiv bearbeiten.

Verlauf laden, KI-Quellen überprüfen, einen MCP-Client verbinden, gespeicherte Medien erkennen und signierte Webhooks senden.

Verfügbar über die aktuelle Quelle. Die portable Vorschauversion 0.7.0 ist älter als diese Tools.

[Entdecken Sie den Arbeitsablauf](https://phishdestroy.github.io/TgWitness/de/docs/archive/)

## Bevor Sie beginnen.

**Ist diese Seite mit Telegram verknüpft?**

Nein. Dies ist eine statische Projektseite mit fiktiven Beispielen und Screenshots. Die eigentliche Anwendung läuft auf Ihrem Computer oder Server; die Anmeldung erfolgt dort.

**Kann es Nachrichten wiederherstellen, die vor der Erfassung gelöscht wurden?**

Nein. TgWitness speichert die Inhalte, die Ihr Konto während der Erfassungsphase erfasst hat. Ein späterer Verlaufs-Snapshot kann versäumte Bearbeitungen oder gelöschte Nachrichten nicht rekonstruieren.

**Ist mein gesamtes Protokoll verschlüsselt?**

Anmeldedaten und Signaturschlüssel werden in einem verschlüsselten Tresor gespeichert. Lokale Nachrichten und Anhänge erfordern eine verschlüsselte Festplatte oder ein verschlüsseltes Volume. Für Exporte kann optional ein passwortgeschütztes ZIP-Archiv mit AES-256-Verschlüsselung verwendet werden.

**Steht dies in Verbindung mit Telegram?**

Nein. TgWitness ist ein unabhängiges Projekt, das auf Telethon basiert und unter der MIT-Lizenz vertrieben wird. Sie autorisieren Ihre eigenen Konten mithilfe der integrierten API-Einstellungen oder Ihres eigenen API-Paares.

PROJECT NOTICE / LICENCE

## Operator incompatibility.

**Taylor Wessing PartG mbB — German core, Hamburg office.**

Our statement as the authors of TgWitness. It adds no condition to the MIT License. Read the complete notice and its source record.

[Read the complete notice](https://phishdestroy.github.io/TgWitness/docs/reference/notice/) [Original text](https://phishdestroy.github.io/TgWitness/NOTICE)

## Entdecken Sie zunächst die Funktionen. Richten Sie das Tool ein, wenn Sie bereit sind.

[Demo öffnen:](https://phishdestroy.github.io/TgWitness/demo/?lang=de)[Einrichtungsanleitung](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=de)
