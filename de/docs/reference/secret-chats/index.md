# Telegram · Geheime Chats: Implementierung und Demo

Canonical page: https://phishdestroy.github.io/TgWitness/de/docs/reference/secret-chats/

Machen Sie sich mit der separaten Secret Chat-Implementierung vertraut, probieren Sie die fiktive Benutzeroberfläche aus und überprüfen Sie noch offene Fehler.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Dokumentation](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md)

**Status geprüft am 6. November 2026:** Eine separate Implementierung für Secret Chats befindet sich in der Entwicklung. Sie wurde noch nicht in den veröffentlichten `main`-Zweig unter `3d23e52b647b` integriert. Der normale Collector und der Takeout-Export erfassen keine Secret Chats. Das interaktive Website-Szenario demonstriert die Benutzeroberfläche anhand fiktiver Daten; es ermöglicht keine Telegram-Kommunikation.

## Wo sich die Implementierung befindet

Commit `0e60f88e` hat **Sources → Pseudo-secret** im lokalen Entwicklungszweig `fix/panel-routes-sessions` hinzugefügt. Der überprüfte Snapshot ist `bb8788fb685c`. Die Implementierung umfasst `tgwitness/secret_chats.py`, Anwendungsrouten, `tgwitness/static/views/secret-chats.js` und spezielle Tests.

Das optionale `secret-chats`-Extra in diesem Zweig verwendet [KiaroSama/Telethon-Secret-Chat](https://github.com/KiaroSama/Telethon-Secret-Chat), das an `d87bf037b90060383c7b704d8a06ebb98c621c6f` angeheftet ist. Die Bibliothek implementiert das End-to-End-Chat-Protokoll von Telegram auf Basis der bestehenden Telethon-Autorisierung des Kontos. Die Installation dieser Bibliothek allein fügt die fehlende Integration zu `main` nicht hinzu.

## Funktionen der Entwicklungsschnittstelle

| Maßnahme | Aufgezeichnetes Verhalten |
| --- | --- |
| Starte einen Chat anhand des Benutzernamens oder der Benutzer-ID | Senden Sie eine Anfrage; der andere Teilnehmer muss diese annehmen. |
| Eine eingehende Anfrage annehmen | TgWitness wird zum empfangenden Endpunkt für diesen Chat. Die automatische Annahme ist eine separate Einstellung, die standardmäßig deaktiviert ist. |
| Eine Nachricht senden oder empfangen | Füge einen ausgehenden oder eingehenden `secret_chat.message`-Eintrag hinzu und zeige ihn im Thread an. |
| Anhang empfangen | Entschlüsseln Sie diese, speichern Sie die Bytes nach SHA-256 und protokollieren Sie `secret_chat.file`. |
| Erhalten Sie eine Zeitangabe oder eine Löschbenachrichtigung | Halten Sie den Hinweis fest und bewahren Sie zuvor erfasste Inhalte auf. |
| Überprüfen Sie die Unterhaltung | Zeige Nachrichten, Dateien, Hinweise und die Schlüsselvisualisierung an. Die geöffnete Registerkarte wird alle vier Sekunden aktualisiert. |

In einer Entwicklungsversion, die die Integration enthält, aktiviert der Betreiber das Modul für das ausgewählte Konto und verbindet es. Das Starten, Akzeptieren und Senden erfordern die Berechtigung zur Interaktion sowie die Deaktivierung des Lese-Schutzes des Kontos. Der andere Teilnehmer muss einen neuen ausgehenden Chat akzeptieren. Diese Steuerelemente sind in der veröffentlichten Anwendung in der oben genannten Version nicht vorhanden.

Es werden nur Chats berücksichtigt, die von dieser TgWitness-Sitzung erstellt oder akzeptiert wurden. Bestehende geheime Chats auf einem Smartphone verbleiben auf diesem Gerät. Ein Sitzungsimport liefert keine separaten Verschlüsselungsschlüssel dafür. Schlüsselmaterial und Zähler für geheime Chats werden im Workspace-Tresor gespeichert; gespeicherte Nachrichten und entschlüsselte Dateien unterliegen den üblichen Sicherheitsvorkehrungen für den Workspace-Speicher.

## Demonstration auf der Website

Das Szenario „**Try Secret Chat**“ auf der Website eröffnet eine fiktive Unterhaltung. Es ermöglicht dem Leser, eine Anfrage zu starten, deren Annahme zu simulieren, eine Beispielnachricht zu senden, eine vorgefertigte Antwort und eine Datei zu erhalten sowie einen Timer und einen Löschhinweis zu überprüfen. Eine eingehende Anfrage kann ebenfalls angenommen werden. Die Steuerelemente kennzeichnen simulierte Aktionen des Gegenübers explizit.

Dieses Szenario läuft im Browser-Speicher. Durch Zurücksetzen oder Neuladen wird es gelöscht. Es erfolgt keine Anmeldung, kein Kontakt zu Telegram, keine Erstellung echter Verschlüsselungsschlüssel und keine Änderung der signierten Beispiel-Downloads. Die angezeigten Nachrichten stellen keine signierten Beweise dar. Das Szenario veranschaulicht die beabsichtigte Interaktion; es bescheinigt nicht, dass die Entwicklungsimplementierung fertiggestellt ist.

## Prüfungen und noch bestehende Mängel

Die fünf bestehenden Tests decken die Persistenz verschlüsselter Schlüssel, den Lebenszyklus und Nachrichtenaufzeichnungen sowie die Richtlinie zur Annahme eingehender Nachrichten, das schreibgeschützte Senden und den Export von Anhängen ab. Sie wurden bei der Überprüfung am 6. November anhand der festgesteckten Bibliothek erfolgreich bestanden. Drei zusätzliche synthetische Prüfungen reproduzierten Fehler im selben Snapshot:

| Ergebnis | Folge |
| --- | --- |
| Schließung umgeht `read_only` | Der Close-Pfad kann eine Remote-Aktion ausführen, wenn Interaktionen blockiert werden sollen. |
| Die Duplikatsuche durchsucht nur die jüngsten Datensätze v500. | Eine ältere Wiedergabe kann nach einem Neustart ein Duplikat erzeugen. |
| Ein fehlgeschlagener Download eines Anhangs löscht dessen ausstehenden Eintrag | Ein vorübergehender Fehler führt zum Verlust des Wiederholungsauftrags. |

Es handelt sich um offene Fehler, die auch im veröffentlichten Audit  dokumentiert sind. Fünf bestandene Tests decken diese Fehler nicht ab. Die Überprüfung erfolgte anhand synthetischer Arbeitsbereiche und simulierter Telegram- Vorgänge; ein Live-Handshake wurde nicht wiederholt und die Eignung für den produktiven Einsatz nicht geprüft.
