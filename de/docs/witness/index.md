# Einen Witness-Bot einrichten

Canonical page: https://phishdestroy.github.io/TgWitness/de/docs/witness/

Ein separater Prozess prüft Ihr Journal und veröffentlicht signierte Prüfpunkte in einem Kanal.

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

Erstellen Sie einen Bot mit BotFather und lassen Sie ihn in Ihrem Kanal posten. Betreiben Sie den Zeugen woanders: ein anderer Host, idealerweise von jemand anderem betrieben, ist viel mehr wert als ein zweiter Prozess neben dem Collector.

## Drei Schritte unter „Extras“

1. **Nur-Lese-Zugriff.** **Extras → Unabhängiger Zeuge**, Token erstellen, Datei speichern. Es liest Prüfpunkte und Zustand, sonst nichts.
2. **Kanal und Intervall.** Telegram-Kanal oder Discord-Webhook, dazu eine Collector-Adresse, die der Zeuge erreicht. Einstellungsdatei speichern.
3. **Starten.** Legen Sie `witness.json`, `witness-token.txt` und `bot-token.txt` zusammen auf den Zeugen-Host und führen Sie aus:

```
python -m tgwitness.witness run --config witness.json --check-config
python -m tgwitness.witness run --config witness.json
```

Warten Sie auf den ersten signierten Beitrag im Kanal und speichern Sie dann den Fingerabdruck des Zeugen an einem sicheren Ort.

Lieber Discord? Speichern Sie die Webhook-URL als `discord-webhook.txt`. Ein Zeuge postet an einen Ort; lange Prüfungen kommen auf Discord als Datei.

## Wählen Sie aus, wie oft Sie Beiträge veröffentlichen möchten

Jede Prüfung zu posten ergibt eine stetige externe Aufzeichnung: alle fünf Minuten sind das etwa 288 Beiträge pro Tag und Arbeitsbereich. Erweiterte Einstellungen können nur bei Änderungen oder Problemen posten, einen Proxy oder eine eigene Bot API nutzen.

**Was bestätigt der Bot tatsächlich?**

Er fragt den Collector nach einem signierten Prüfpunkt, prüft ihn gegen den erwarteten Schlüssel und führt ein eigenes signiertes Journal, einschließlich verpasster und abgelehnter Antworten.

Er prüft den Journalzustand, beobachtet Telegram aber nicht selbst. Dafür machen Sie einen kontrollierten Zustelltest.

## Überprüfen Sie die Beweise später

Bewahren Sie das Zeugen-Journal, die Beiträge und die Fingerabdrücke auf. [So prüfen Sie sie](https://phishdestroy.github.io/TgWitness/de/docs/reference/witness/#verify) gegen den Export des Collectors.
