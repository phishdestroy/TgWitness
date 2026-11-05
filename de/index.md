# Nachrichten ändern sich． Bewahren Sie fest， was Sie gesehen haben．

Canonical page: https://phishdestroy.github.io/TgWitness/de/

[Open Source ／ v0.9.1](https://phishdestroy.github.io/TgWitness/de/docs/reference/changelog/)

Speichern Sie Telegram－Chats mit jeder Bearbeitung und Löschung und geben Sie einen Datensatz weiter， den jeder prüfen kann．

[Demo öffnen：](https://phishdestroy.github.io/TgWitness/demo/?lang=de)[Einrichtungsanleitung](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=de)

Erfundene Daten， keine Telegram－Anmeldung．

 [Erfassung mit GitHub Actions （Vorschau）](https://phishdestroy.github.io/TgWitness/de/docs/capture/) [S3－Offsite－Kopie： Einrichtung und Wiederherstellung](https://phishdestroy.github.io/TgWitness/de/#s3)

EINE NACHRICHT DURCH DIE ZEIT ＃0042

Northstar · ForschungFiktive Quelle ／ Nachricht 42

1. **Beobachtete Nachricht：**09：41：02

   Die Einweisung beginnt bei 14：00．
2. **Bearbeitung beibehalten**09：43：18

   Die Einweisung beginnt bei 15：00．

   Vorherige Version beibehalten
3. **Löschhinweis**10：06：45

   Die erfassten Inhalte verbleiben in Ihrem Protokoll．

Drei Beobachtungen． Eine Geschichte． BEISPIEL

Die Nachricht verschwindet． Der aufgezeichnete Verlauf bleibt erhalten．

## Jede erfasste Änderung． Genau dort， wo Sie sie benötigen．

Die echte Oberfläche， mit erfundenen Daten．

TgWitness ／ Gespeicherte ChatsIHR ARBEITSBEREICH FÜR BEOBACHTUNGEN

![Gespeicherte Telegram－Konversationen im „Dark Theme＂， wobei erfasste Bearbeitungen und gelöschte Nachrichten im Kontext erhalten bleiben](https://phishdestroy.github.io/TgWitness/assets/chats-dark.png)

01 ／ Gespeicherte Chats Sieht aus wie ein normaler Chat， Bearbeitungen und Löschungen stehen direkt neben den Nachrichten．

TgWitness ／ ProtokollLOKALER ARBEITSBEREICH

![Protokoll mit erfassten Nachrichten， Bearbeitungen， Löschmeldungen und erfassten Ereignissen](https://phishdestroy.github.io/TgWitness/assets/workspace.png)

02 ／ Journal Alles， was Ihr Konto gesehen hat， durchsuchbar， Lücken inklusive．

TgWitness ／ BearbeitungsverlaufLOKALER ARBEITSBEREICH

![Detailansicht， in der die erfasste ursprüngliche und die bearbeitete Version einer Nachricht miteinander verglichen werden](https://phishdestroy.github.io/TgWitness/assets/detail.png)

03 ／ Bearbeitungsverlauf Alte und neue Version nebeneinander， nichts wird überschrieben．

TgWitness ／ Signierte ExporteLOKALER ARBEITSBEREICH

![Exportfunktion für den Arbeitsbereich mit signierten Dateien im ZIP－， JSONL－ und CSV－Format sowie einem Offline－HTML－Bericht](https://phishdestroy.github.io/TgWitness/assets/exports.png)

04 ／ Signierte Exporte Nehmen Sie das Journal mit， signiert und mit eigenem Prüfprogramm．

Verfolgen Sie einen gespeicherten Datensatz über [das Case Board](https://phishdestroy.github.io/TgWitness/de/docs/case-board/)， [die Berichtsgestaltung](https://phishdestroy.github.io/TgWitness/de/docs/reports/) und eine [Kopie zur Weitergabe](https://phishdestroy.github.io/TgWitness/de/docs/handover/)． [Überprüfen Sie Kontengruppen](https://phishdestroy.github.io/TgWitness/de/docs/groups/) gemeinsam．

01 ／ ERFASSUNG

### Sie bestimmen den Umfang．

Ein paar Chats， ein Ordner oder das ganze Konto． Jedes Konto bekommt seinen eigenen Arbeitsbereich．

[Vergleichen Sie die Erfassungsmodi：](https://phishdestroy.github.io/TgWitness/de/guides/modes.html#scope)

02 ／ PRESERVE

### Änderungen tragen zur Geschichte bei．

Versionen， Löschungen und Lücken bleiben alle im Journal．

[Siehe die Ereignismatrix](https://phishdestroy.github.io/TgWitness/de/guides/modes.html#events)

03 ／ ÜBERGABE

### Eine Aufzeichnung， die weitergereicht wird．

Signiertes ZIP， Dateien und ein Offline－Bericht． Passwort optional．

[exportieren und verifizieren](https://phishdestroy.github.io/TgWitness/de/docs/exports/)

## Ändern Sie ein Byte．
Die Überprüfung zeigt es Ihnen an．

Jedes Ereignis ist mit dem vorherigen Hash verknüpft und trägt eine Ed25519－Signatur．

![Erfasste Ereignisse sind mit früheren Hashes verknüpft， tragen Signaturen und werden in einem überprüfbaren Export bereitgestellt．](https://phishdestroy.github.io/TgWitness/assets/evidence-chain-animated.svg)

![Das Ändern eines erfassten Datensatzes verändert dessen Hash－Wert und macht die Überprüfung des verknüpften Datensatzes unmöglich．](https://phishdestroy.github.io/TgWitness/assets/evidence-tamper-animated.svg)

![Ein separat gespeicherter Kontrollpunkt ermöglicht es dem Empfänger， das exportierte Protokoll mit einer früheren Beobachtung zu vergleichen．](https://phishdestroy.github.io/TgWitness/assets/evidence-checkpoint-animated.svg)

Befolgen Sie die Prüfungen vom Datei－Hash bis zu einem separat gespeicherten Checkpoint．

[Entdecken Sie acht Beweisstufen：](https://phishdestroy.github.io/TgWitness/de/guides/modes.html#levels)

## Bereit für eine zweite Überprüfung．

Nachrichten， Dateien und ein Offline－Bericht in einem signierten Paket．

[Lesen Sie das Beweismodell](https://phishdestroy.github.io/TgWitness/de/docs/reference/evidence/)

tgwitness-evidence.zipSIGNED BUNDLE

- 01

  Ursprüngliche BeobachtungenJSONL－Datensätze ＋ CSV－Tabelle
- 02

  Lesbarer KontextOffline－HTML－Bericht ＋ erhaltene Medien
- 03

  Unabhängige ÜberprüfungSigniertes Manifest ＋ eigenständiger Verifizierer

Der Empfänger prüft alles gegen Ihren Schlüssel， und ein anderswo gespeicherter Prüfpunkt zeigt， dass seitdem nichts umgeschrieben wurde． [So funktionieren die Prüfungen．](https://phishdestroy.github.io/TgWitness/de/docs/concepts/#layers)

## S3－Kopien． Externe Überprüfungen．

Bewahren Sie verschlüsselte Kopien auf und führen Sie unabhängige Überprüfungen durch．

Standardmäßig deaktiviert

### Kopieren Sie alles in einen S3－kompatiblen Speicher

Journal， Dateien， Prüfpunkte und Chat－Exporte， verschlüsselt， bevor sie zu S3 gehen．

**Speichereinstellungen und Wiederherstellung**

Clientseitige Verschlüsselung

`AES-256-GCM` auf Ihrem Rechner． Der Anbieter sieht nur Chiffretext．

Geplante oder manuelle Kopien

Jetzt kopieren oder alle 1 bis 1.440 Minuten， Fortschritt im Panel．

Object Lock

Wählen Sie Aufbewahrungstage und Modus， das Panel prüft， ob es wirklich greift．

Verifizierte Wiederherstellung

Bewahren Sie den Schlüssel getrennt auf． Wiederherstellen geht überall， Dateien kommen erst nach der Prüfung heraus．

![Vollständiges Off－Site－Kopier－Panel： Endpunkt， Region， Bucket， Zugriffsschlüssel， Zeitplan， „Object Lock＂－ und Wiederherstellungsschlüssel－Steuerelemente](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)

Das vollständige Bedienfeld mit erweiterten Optionen ist aufgeklappt． Es werden keine Anmeldedaten für den Speicher angezeigt．

Zeitschrift und Medien`AES-256-GCM`S3－kompatibler Speicher

[S3 konfigurieren und eine Kopie wiederherstellen：](https://phishdestroy.github.io/TgWitness/de/docs/exports/#s3)[Lesen Sie die Details zur Verifizierung unter](https://phishdestroy.github.io/TgWitness/de/docs/reference/evidence/#off-site-copy-and-restore-s3)

**Wiederherstellungsschlüssel** Getrennt aufbewahren， ohne ihn ist die Kopie unlesbar．

### Benachrichtigungen · Apprise

Probleme， Chat－Änderungen und eine tägliche Zusammenfassung an Messenger， E－Mail oder Ihren eigenen Webhook．

**Wählen Sie， was geteilt wird** Kein Nachrichtentext， solange Sie ihn nicht einschalten．

 [Benachrichtigungsempfänger konfigurieren](https://phishdestroy.github.io/TgWitness/de/docs/reference/operations/#notifications)

### Externe Zeitstempel

Zeitstempel－Checkpoint－Hashes gemäß RFC 3161 und OpenTimestamps．

**Ergebnis verfolgen** Prüfen Sie die TSA－Antwort oder rüsten Sie die OpenTimestamps－Quittung zu einem Bitcoin－Beweis auf．

 [Überprüfen Sie die Zeitstempel－Nachweise unter](https://phishdestroy.github.io/TgWitness/de/docs/reference/timestamp/)

### Unabhängiger Zeuge

Ein separater Host speichert die signierten Beobachtungen und kann „`TGW1`＂－Checkpoints veröffentlichen．

**Referenz trennen** Auf einem anderen Host betreiben， mit eigenem Schlüssel und Journal．

 [Richten Sie ein Witness－Konto ein：](https://phishdestroy.github.io/TgWitness/de/docs/witness/)

### Wiederherstellung und erkennbare Lücken

Fortsetzung nach Neustart． Nachprüfungen und „`coverage.json`＂ zeigen wiederhergestellte Nachrichten und Lücken an．

**Zeitraum prüfen** Wiederhergestellte Nachrichten und erfasste Lücken nebeneinander．

 [Überprüfen Sie Kontinuität und Lücken](https://phishdestroy.github.io/TgWitness/de/guides/modes.html#continuity)

## Hier beginnt Ihr erster Arbeitsbereich．

Probieren Sie zuerst die Demo und verbinden Sie ein Ersatzkonto， wenn Sie so weit sind．
Windows， Linux， macOS oder Docker．

[Lesen Sie die Einrichtungsanleitung](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=de)

**Eine importierte Sitzung， ein laufender Client．**

Nutzen Sie importierte TData oder eine Sitzung nicht gleichzeitig in Telegram Desktop und TgWitness： Telegram kann beide sperren （AUTH_KEY_DUPLICATED）． Brauchen Sie beides？ Melden Sie sich in TgWitness separat per Telefon oder QR an．

[Lesen Sie die Warnung zum Import von Sitzungen](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=de#session-warning)

**Werfen Sie einen Blick darauf， bevor Sie eine Verbindung herstellen．**

Probieren Sie den fiktiven Arbeitsbereich ohne Telegram－Konto aus．

[Online－Demo öffnen →](https://phishdestroy.github.io/TgWitness/demo/?lang=de)

Windows `scripts\Demo.cmd`Linux ／ macOS `sh start.sh --demo`

**Befehle zur lokalen Installation**

SCHRITT 01

### Hier finden Sie den Quellcode．

[Laden Sie die ZIP－Datei mit dem Quellcode herunter](https://github.com/phishdestroy/TgWitness/archive/refs/heads/main.zip) und entpacken Sie sie， oder klonen Sie das Repository：

```
git clone https://github.com/phishdestroy/TgWitness.git
cd TgWitness
```

Braucht Python 3.11+． Unter Windows bietet der Starter die Installation an．

[Veröffentlichungen durchsuchen](https://github.com/phishdestroy/TgWitness/releases)

SCHRITT 02

### Wählen Sie die Ausführungsart．

Doppelklicken Sie auf „`Start.cmd`＂ oder führen Sie den Befehl in PowerShell aus：

```
.\Start.cmd
```

Sie möchten sich nur umsehen？ Doppelklicken Sie auf „`scripts\Demo.cmd`＂， um eine isolierte Demo aufzurufen． Eine Telegram－Anmeldung ist nicht erforderlich．

Verfügbar mit Python 3.11+ und „`venv`＂：

```
sh start.sh
```

Um stattdessen das fiktive Protokoll zu öffnen， führen Sie bitte den Befehl „`sh start.sh --demo`＂ aus．

Bei laufendem Docker und installierter Compose－Version 2.20+：

```
docker compose up -d --build --wait
docker compose exec tgwitness cat /data/panel-token.txt
```

Der zweite Befehl zeigt Ihr privates Panel－Token an． Bewahren Sie es auf Ihrem Rechner auf．

Öffnen Sie nach dem Start [127.0.0.1:8787](http://127.0.0.1:8787)．

Bei Installation aus dem Quellcode liegt das Token in `data/live/panel-token.txt`． Ein eigenes API－Paar von [my.telegram.org](https://my.telegram.org) ist optional． [Vollständige Anleitung ↗](https://phishdestroy.github.io/TgWitness/de/docs/reference/quickstart/)

**TgWitness 0.9.1** [Was gibt＇s Neues →](https://phishdestroy.github.io/TgWitness/de/docs/reference/changelog/) · [Funktionen und bekannte Einschränkungen →](https://phishdestroy.github.io/TgWitness/de/docs/reference/features/)

## Klare Anweisungen． Ein nützlicher nächster Schritt．

[Entdecken Sie die Anleitungen ↗](https://phishdestroy.github.io/TgWitness/de/docs/)

[### Modi， Szenarien und Beweisstufen Vier Erfassungsmodi． Acht Verifizierungsstufen． Finden Sie den passenden Arbeitsablauf für Ihren Fall．](https://phishdestroy.github.io/TgWitness/de/guides/modes.html)

[01 ### Ein Konto verbinden Import von Telefon－， QR－ und unterstützten Sitzungsdaten．](https://phishdestroy.github.io/TgWitness/de/docs/accounts/)[02 ### Wählen Sie einen Proxy Öffentliche MTProxy－Listen oder Ihre eigene Route．](https://phishdestroy.github.io/TgWitness/de/docs/proxies/)[03 ### Einen Witness－Bot einrichten Signierte Kontrollpunkte in Ihrem Telegram－Kanal．](https://phishdestroy.github.io/TgWitness/de/docs/witness/)[04 ### Exportieren und verifizieren Teilen Sie den erfassten Verlauf und überprüfen Sie dessen Integrität．](https://phishdestroy.github.io/TgWitness/de/docs/exports/)

## Das Archiv bearbeiten．

Verlauf， KI mit Quellen， MCP， OCR und signierte Webhooks．

[Entdecken Sie den Arbeitsablauf](https://phishdestroy.github.io/TgWitness/de/docs/archive/)

## Bevor Sie beginnen．

**Ist diese Seite mit Telegram verknüpft？**

Nein． Das ist eine statische Seite mit erfundenen Beispielen． Die App läuft auf Ihrem eigenen Rechner， dort melden Sie sich an．

**Kann es Nachrichten wiederherstellen， die vor der Erfassung gelöscht wurden？**

Nein． Sie hält fest， was Ihr Konto gesehen hat， solange sie lief． Ein späterer Snapshot kann verpasste Bearbeitungen oder gelöschte Nachrichten nicht rekonstruieren．

**Ist mein gesamtes Protokoll verschlüsselt？**

Sitzungen und Schlüssel schon． Nachrichten und Dateien nicht， nutzen Sie Festplattenverschlüsselung． Exporte können ein AES－256－Passwort bekommen．

**Steht dies in Verbindung mit Telegram？**

Nein． Es ist ein unabhängiges MIT－lizenziertes Projekt auf Basis von Telethon． Sie melden sich mit Ihren eigenen Konten an．

PROJECT NOTICE ／ LICENCE

## Operator incompatibility．

**Taylor Wessing PartG mbB， German core， Hamburg office．**

This statement from the authors of TgWitness adds no condition to the MIT License， and the complete notice includes its source record．

[Read the complete notice](https://phishdestroy.github.io/TgWitness/docs/reference/notice/) [Original text](https://phishdestroy.github.io/TgWitness/NOTICE)

## Entdecken Sie zunächst die Funktionen． Richten Sie das Tool ein， wenn Sie bereit sind．

[Demo öffnen：](https://phishdestroy.github.io/TgWitness/demo/?lang=de)[Einrichtungsanleitung](https://phishdestroy.github.io/TgWitness/demo/guide.html?lang=de)
