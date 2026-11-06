# Telegram · Öffentliches Showcase

Canonical page: https://phishdestroy.github.io/TgWitness/de/docs/reference/showcase/

Veröffentlichen Sie gespeicherte Nachrichten ausgewählter öffentlicher Kanäle und signierte Momentaufnahmen über zeitlich begrenzte, widerrufbare Links.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Dokumentation](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Bereitstellung und Wiederherstellung](https://phishdestroy.github.io/TgWitness/de/docs/reference/deployment/)

![Bereitstellung und Wiederherstellung](https://phishdestroy.github.io/TgWitness/assets/chapter-operate.svg)

**„Zugriff → Öffentliches Showcase“** erstellt eine separate, schreibgeschützte Seite unter Verwendung des bestehenden Access-Token-Systems. Es liest die gespeicherten Beobachtungen der Installation aus. Es startet keinen Kollektor, meldet sich nicht bei Telegram an und richtet keinen Kanal für einen Besucher ein.

## Eine Seite veröffentlichen

1. Speichern Sie für jeden öffentlichen Kanal, den Sie anzeigen möchten, ein Quellprofil. Ein Kanal muss in seinem zuletzt gespeicherten Profil einen öffentlichen Benutzernamen haben; Gruppen und private Chats kommen nicht in Frage.
2. Offener **Zugriff → Öffentlicher Showcase** (oder `/showcase-manage.html`) als Administrator.
3. Wählen Sie Kanäle aus bis zu 16 Arbeitsbereichen aus, geben Sie den Titel der öffentlichen Seite ein und wählen Sie eine Gültigkeitsdauer des Links von 1, 7 oder 30 Tagen. Interne Arbeitsbereichsbezeichnungen werden nicht veröffentlicht. Es können bis zu 64 Kanäle einbezogen werden.
4. Überprüfen Sie den Text der ausgewählten Kanäle vor der Veröffentlichung und klicken Sie anschließend auf **„Vorschau der ausgewählten Datensätze**“. Die Vorschau verwendet dieselbe serverseitige Projektion wie die Besucherseite.
5. Klicken Sie auf **„Showcase-Link erstellen**“. Kopieren Sie den Link, solange er sichtbar ist. Öffnen Sie ihn in einem separaten Browser, um die Seite des Empfängers zu überprüfen, bevor Sie ihn weiterleiten.

Der Link enthält ein Zugriffstoken im URL-Fragment. Die Seite entfernt das Fragment vor dem Absenden von API-Anfragen und tauscht es gegen eine Browsersitzung aus. Jeder, der den Link besitzt, kann das ausgewählte Material bis zum Ablauf oder zur Widerrufung öffnen. Neue Links erlauben 100 gleichzeitige Sitzungen, die jeweils höchstens eine Stunde dauern. Bestehende Zugriffskontrollen können über die Grant-API auch Adressbeschränkungen und Anmeldebegrenzungen durchsetzen. Der normale Prüferzugriff ist ein anderer Modus und umfasst weiterhin die ursprünglich zugelassenen Nachrichten und Dateien.

## Was Besucher sehen

| Sichtbar | Privat gehalten |
| --- | --- |
| Ausgewählte Titel öffentlicher Kanäle, Benutzernamen und Daten der Profilbeobachtung | Kontoidentitäten, interne Arbeitsbereichsbezeichnungen und nicht ausgewählte Quellen |
| Erfasster Text und jede gespeicherte Bearbeitung | Strukturierte Absender-IDs, Namen, Benutzernamen, Telefonnummern und Profilwerte |
| Löschmeldungen mit dem zuvor gespeicherten Text, sofern verfügbar | Anhänge, Avatare, Miniaturansichten, Dateinamen und Originaldaten |
| Markierungen, die anzeigen, dass ein Autor/Profil oder ein Anhang erfasst wurde | Metadaten zu Weiterleitungen und Antworten, Netzwerkwege, IP-Adressen und Anmeldedaten |
| Ereignisanzahlen für ausgewählte Kanäle, aktuelle Sammlungsschalter, Heartbeat- und Checkpoint-Intervall | Steuerelemente für die Datenerfassung und gängige APIs zum Export von Beweismaterial |
| Signatur-Fingerabdruck, Journal-Checkpoint und Konsistenznachweis | Signaturschlüssel und Telegram-Sitzungen |

**Der Text öffentlicher Nachrichten wird nicht automatisch anonymisiert.** Ein Name, eine Erwähnung, eine Telefonnummer oder ein Link, die in der Nachricht enthalten sind, bleiben Teil dieses Textes. `Redacted`Dies gilt für die strukturierten Autoren-/Profilfelder. Überprüfen Sie den tatsächlich ausgewählten Inhalt vor der Veröffentlichung, einschließlich beibehaltener Bearbeitungen und Löschungen.

Die Berechtigung spiegelt das **zuletzt gespeicherte Quellprofil** wider, nicht eine Live-Abfrage bei Telegram. Wenn ein nachfolgendes Profil keinen öffentlichen Kanal-Benutzernamen mehr enthält, schließen neue Anfragen den Kanal aus. Aktualisieren Sie die Quellprofile, wenn sich die öffentliche Sichtbarkeit ändert. Leser haben möglicherweise bereits Material gespeichert, das sie zuvor erhalten haben.

Die ursprünglichen signierten Datensätze bleiben unverändert. Die angezeigte Projektion wird separat signiert und enthält Hashes, die auf die ursprünglichen Datensätze verweisen. Eine Projektionssignatur authentifiziert die angezeigte Aussage; es handelt sich nicht um die Signatur des ursprünglichen Ereignisses über redigierte Bytes.

## Signaturen und Kontinuität prüfen

Erweitern Sie **„Fingerabdruck & signierter Checkpoint“** und laden Sie einen Snapshot herunter. Nach einer Seitenaktualisierung enthält der Download den vorherigen Browser-Snapshot und einen Merkle- Konsistenznachweis zwischen deren Journalgrenzen. Die automatische Aktualisierung erfolgt einmal pro Minute, solange die Seite sichtbar ist und ihre erste Seite mit Beobachtungen anzeigt.

Nachdem Sie TgWitness installiert haben, überprüfen Sie die heruntergeladene Datei offline:

```
python -m tgwitness.showcase_verify showcase.json --fingerprint TRUSTED_COLLECTOR_SHA256
```

Der Fingerabdruck muss von einer separat vertrauenswürdigen Referenz stammen. Um einen Vergleich mit einem von Ihnen selbst gespeicherten Snapshot durchzuführen, verwenden Sie `--previous earlier.json`; dies überschreibt den vorherigen Snapshot, der im Download enthalten ist. Der aktuelle Nachweis muss an dieser gespeicherten Grenze beginnen. Authentifizierte Clients können diesen Nachweis mit `GET /api/showcase/{workspace_id}?challenge=<32-hex-random>&from_count=<retained-count>`. Ein kürzeres Journal gibt einen HTTP-409-Fehler zurück, anstatt die Grenze stillschweigend zurückzusetzen.

Der signierte Checkpoint wird für das **gesamte Collector-Journal** festgeschrieben, einschließlich seiner Datensatzanzahl und des undurchsichtigen Head-Hash. Die angezeigten Nachrichtenzahlen gelten nur für die ausgewählten öffentlichen Kanäle. Die Seite listet niemals den Inhalt des anderen Journals auf. Es handelt sich um Ereigniszahlen, nicht um die Anzahl eindeutiger Nachrichten. Die Einstellungen beschreiben die aktuelle Konfiguration, nicht jedes frühere Aufzeichnungsintervall.

Die Signatur- und Konsistenzprüfung kann Änderungen im Verhältnis zu einer festgelegten Grenze erkennen. Sie führt keine unabhängige Neuzählung der signierten Zähler durch, bescheinigt nicht die Telegram-Herkunft, weist keine lückenlose Erfassung nach und ersetzt keinen unabhängigen Zeugen. Verwenden Sie für diese Überprüfung den [Evidenzprüfer](https://github.com/phishdestroy/TgWitness/blob/main/docs/TRUST.md), [den unabhängigen Zeugen](https://phishdestroy.github.io/TgWitness/de/docs/reference/witness/) und [den in Testmaßstab erstellten Datensatz](https://phishdestroy.github.io/TgWitness/de/docs/reference/verification/). Synthetische Installationen sind sichtbar als „synthetisch“ gekennzeichnet.

## Seite widerrufen oder hosten

Verwenden Sie **„Revoke“** im Showcase-Manager oder im bestehenden Abschnitt **„Zugriff“,** um den Link zu schließen und alle zugehörigen Sitzungen zu beenden. Der Besucher löscht angezeigte Datensätze, sobald eine Anfrage feststellt, dass der Zugriff beendet wurde. Ablaufdatum und Berechtigungen werden bei jeder Anfrage überprüft. Showcase-Berechtigungen können nicht direkt in einen gewöhnlichen Panel-Zugriff umgewandelt werden; erstellen Sie eine neue Berechtigung, um den Modus zu ändern.

Die Seite wird über die bestehende HTTPS-Adresse der Installation bereitgestellt. Das Veröffentlichen eines Links öffnet keinen neuen Port, erstellt keinen Tunnel und ändert keine DNS-Einstellungen. Der HTML-Code und die API bleiben auf der Installation des Nutzers. Ein Besucher der Demo kann mit diesem Zugriff die üblichen APIs für Nachrichten, Profile, Medien, Export oder Verwaltung nicht nutzen.
