# Einen Witness-Bot einrichten

Canonical page: https://phishdestroy.github.io/TgWitness/de/docs/witness/

Lassen Sie das Protokoll von einem separaten Prozess überprüfen und signierte Prüfpunkte in Ihrem Kanal veröffentlichen.

## Zwei Hosts, zwei Signaturschlüssel

HOST A / COLLECTOR**Konto + Protokoll**

Signaturschlüssel des Telegram-Session-Collectors

Endpunkt für schreibgeschützte Checkpoints

← Signierte Antwort anfordern →

HOST B / WITNESS**Überprüfen + aufbewahren**

Festgelegter Fingerabdruck des Erfassers; separater Signaturschlüssel des Zeugen

Eigenes Protokoll + Bot-Token

Witness → Telegram-Bot-API →**Ihr Kanal · signierte TGW1-Beiträge**

Der „Witness“ führt die Überprüfungen selbst durch. Der Zugriff des „Collectors“ ist schreibgeschützt. Die Veröffentlichung durch den Bot erfolgt über die Verbindung und das Token des „Witness“; dem „Witness“ wird keine Kontositzung zugewiesen.

03 / CHECKPOINT-ENTSCHEIDUNGENBeispielantworten

ZULETZT AKZEPTIERT**120 Einträge**`head 9c7d…`

NÄCHSTE ANTWORT**128 Einträge**`head a4f2…`

Akzeptiert: Die Zählung steigt, die Signatur wird verifiziert und der Schlüssel stimmt überein. Der Witness behält diese neue Grenze bei.

Alle Antwortbeispiele setzen eine gültige Signatur und den festgesteckten Schlüssel voraus. Die hier angegebenen Hashes dienen lediglich der Veranschaulichung. Eine höhere Anzahl allein kann nicht beweisen, dass das gesamte alte Präfix unverändert ist; vergleichen Sie einen Export mit beibehaltenen Kontrollpunkten.

## Bereiten Sie einen Bot und einen Kanal vor

Erstellen Sie mit BotFather einen Bot und erlauben Sie ihm, in einem von Ihnen kontrollierten Kanal zu posten. Wählen Sie einen Computer oder Server für den Witness aus. Ein separater Host und Betreiber gewährleisten eine größere Unabhängigkeit als ein zweiter Prozess auf dem Server des Erfassers.

## Drei Schritte unter „Extras“

1. **Nur-Lese-Zugriff.** Öffnen Sie **„Extras“ → „Ein Bot in Ihrem Kanal“**, erstellen Sie ein Witness-Token und speichern Sie die Zugriffsdatei. Damit können Sie Checkpoints und den Systemzustand einsehen, jedoch keine Unterhaltungen oder Steuerelemente des Collectors.
2. **Kanal und Intervall.** Geben Sie den Kanal und eine vom Witness erreichbare Sammleradresse ein. Speichern Sie die Einstellungsdatei.
3. **Start.** Fügen Sie „`witness.json`“, „`witness-token.txt`“ und ein auf dem Witness-Host erstelltes „`bot-token.txt`“ zusammen ein. Führen Sie die folgenden Befehle in der installierten Projektumgebung aus.

```
python -m tgwitness.witness run --config witness.json --check-config
python -m tgwitness.witness run --config witness.json
```

Das Herunterladen der Dateien löst den Witness nicht aus. Vergewissern Sie sich, dass der erste signierte Beitrag im Kanal erscheint, und speichern Sie anschließend den Fingerabdruck des öffentlichen Schlüssels des Witness separat.

## Wählen Sie aus, wie oft Sie Beiträge veröffentlichen möchten

Die Veröffentlichung jeder Überprüfung erzeugt einen regelmäßigen externen Datensatz. Bei Intervallen von fünf Minuten sind das etwa 288 Beiträge pro Arbeitsbereich und Tag. Die erweiterten Einstellungen bieten zudem die Veröffentlichung bei Änderungen oder Problemen, einen Proxy sowie eine benutzerdefinierte Bot-API-Adresse.

**Was bestätigt der Bot tatsächlich?**

Der „Witness“ fordert vom „Collector“ einen signierten Checkpoint an, vergleicht diesen mit dem erwarteten Schlüssel und führt ein separates, signiertes Protokoll. Es erfasst sowohl fehlende Antworten und abgelehnte Antworten als auch erfolgreiche Überprüfungen. Die Veröffentlichung hängt weiterhin davon ab, dass der „Witness“ läuft und die Bot-API von Telegram erreicht.

Es überprüft den vom Collector gemeldeten Protokollstatus. Es überwacht nicht jede Telegram-Nachricht eigenständig. Fügen Sie hierfür den Test zur kontrollierten Zustellung hinzu.

## Überprüfen Sie die Beweise später

Bewahren Sie das Zeugenprotokoll, die Kanalbeiträge und die unabhängig gespeicherten Fingerabdrücke auf. Im [Rahmen des vollständigen Verifizierungsverfahrens](https://phishdestroy.github.io/TgWitness/de/docs/reference/witness/#verify) werden diese mit dem signierten Export des Erfassers abgeglichen.
