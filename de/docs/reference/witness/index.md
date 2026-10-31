# Unabhängiger Zeuge

Canonical page: https://phishdestroy.github.io/TgWitness/de/docs/reference/witness/

Führen Sie „Witness“ mit einem eigenen Schlüssel und Bot aus, veröffentlichen Sie signierte Checkpoints in einem Kanal und vergleichen Sie die Exporte damit.

[Einrichtung des Bots und des Proxys auf Russisch](https://github.com/phishdestroy/TgWitness/blob/main/docs/ru/WITNESS.md).

Ein Collector signiert sein eigenes Protokoll; daher könnte jeder, der die Kontrolle über den Collector und dessen Schlüssel hat, grundsätzlich das Protokoll umschreiben oder kürzen und es erneut signieren. Ein „Witness“ macht dies nachweisbar. Es handelt sich um einen separaten Prozess – einen weiteren Container oder besser gesagt einen Server, der von einer anderen Person betrieben wird –, der alle paar Minuten den signierten Protokollkopf des Collectors abruft, das Gesehene mit seinem eigenen Schlüssel signiert, es in seinem eigenen Protokoll speichert und es in einem Telegram-Kanal veröffentlicht.

Ablaufdiagramm · Collector → Witness (Signierter Prüfpunkt: Anzahl der Einträge + Head-Hash); Witness → Witness-Protokoll, eigener Schlüssel; Witness → Telegram-Kanal (Signierter Beitrag über den eigenen Bot); Beweismaterial-ZIP → verify.py; Witness-Protokoll, eigener Schlüssel → verify.py; Telegram-Kanal → verify.py (Export über Telegram Desktop oder die Seite „t.me/s“) · Collector · Witness · Witness-Protokoll, eigenerSchlüssel · Telegram-Kanal · Beweismaterial-ZIP · verify.py · Signierter Prüfpunkt: Anzahl · der Einträge + Head-Hash · Signierter Beitrag über den · eigenen Bot · Export über Telegram Desktop · oder die Seite „t.me/s“

**Diagramm als Text**

1. Collector → Witness (Signierter Prüfpunkt: Anzahl der Einträge + Head-Hash)
2. Witness → Witness-Protokoll, eigener Schlüssel
3. Witness → Telegram-Kanal (Signierter Beitrag über den eigenen Bot)
4. Beweismaterial-ZIP → verify.py
5. Witness-Protokoll, eigener Schlüssel → verify.py
6. Telegram-Kanal → verify.py (Export über Telegram Desktop oder die Seite „t.me/s“)

## Was TgWitness bietet – und was nicht

| Der Zeuge hat | Der Zeuge hat niemals |
| --- | --- |
| Ein schreibgeschütztes **Witness-Token** für einen Arbeitsbereich | Die Telegram-Sitzung oder die API-Zugangsdaten des Erfassers |
| Eigener Ed25519-Schlüssel und eigenes Protokoll | Der Speicher des Collectors, der Signaturschlüssel oder das Panel-Token |
| Ein eigenes Telegram-Bot-Token | Inhalt der Nachricht: Der Kopf besteht aus einer Datensatzanzahl und einem Hash |

Das Token wird auf der **„Witness**“-Seite des Panels erstellt, einmalig angezeigt und ausschließlich als SHA-256 gespeichert. Es öffnet genau einen Endpunkt, `GET /api/witness/head`, der einen frisch signierten Checkpoint sowie signierte, inhaltsfreie Erfassungszähler und den Betriebszustand zurückgibt. Es kann weder das Panel öffnen noch Nachrichteninhalte lesen oder Einstellungen ändern, und das Panel-Token wird dort nicht akzeptiert. Ein Token kann auf derselben Seite widerrufen werden. Der Collector protokolliert, wann ein neuer Witness-Schlüssel mit der Überprüfung beginnt (`witness.seen`), und zeigt die letzte Überprüfung pro Token an; ein Witness, der innerhalb von 2,5 Intervallen keine Überprüfung durchgeführt hat, wird als überfällig markiert.

Neue Zeugen senden bei jeder Abfrage eine zufällige Herausforderung; die Erfassungsanweisung gibt diese unter der Signatur des Sammlers wieder. Zähler sind an den genauen Kontrollpunkt gebunden und werden in signierte Zeugenbeiträge aufgenommen. Ältere Kopfzeilen werden vom eigenständigen Zeugen weiterhin akzeptiert. Das Wachstum des Protokolls allein wird niemals als neue Nachricht gezählt.

## Was überprüft und aufgezeichnet wird

In jedem Intervall (standardmäßig alle 10 Minuten) führt TgWitness folgende Schritte durch:

1. ruft den Header selbst ab (der Collector kann ihn weder übertragen noch überspringen);
2. überprüft die Signatur des Erfassers, den festgesteckten Erfassungsschlüssel (`--collector-fingerprint`, oder den zuerst angezeigten Schlüssel), einen nicht abnehmenden Zählwert und einen unveränderten Kopf bei einem unveränderten Zählwert;
3. fügt seinem eigenen Protokoll einen signierten Datensatz hinzu: `witness.anchor` mit dem Status `ok`, `key_changed`, `rollback` (weniger Datensätze als zuvor), `fork` (gleiche Länge, anderer Kopf) oder `invalid` (die Antwort hat die Überprüfung nicht bestanden) oder `witness.no_response`, wenn der Kollektor nicht geantwortet hat;
4. Das Ergebnis wird signiert im Kanal veröffentlicht, einschließlich der Meldung „keine Antwort“, solange TgWitness läuft und die Bot-API erreichen kann. Die Beitrags-ID wird aufgezeichnet (`witness.posted`), ebenso wie ein fehlgeschlagener Beitrag (`witness.post_failed`).

Ein Eintrag sieht wie folgt aus; die letzte Zeile enthält die signierte Erklärung:

```
TgWitness witness #42 · journal head
Collector 3fa9c2d1e0b4a7f6: 18234 records
Head 9b1f…c07e
2026-10-28T19:40:00.123+00:00
TGW1.eyJhdCI6…<statement>.<signature>
```

## Ein Witness ausführen

Sie benötigen einen Telegram-Bot (erstellen Sie einen mit @BotFather), einen Kanal, in dem dieser Bot als Administrator fungiert, sowie die Adresse des Collectors, die für den Zeugen erreichbar ist – über HTTPS außerhalb eines privaten Netzwerks (siehe das HTTPS-Profil im Abschnitt [„Bereitstellung“](https://phishdestroy.github.io/TgWitness/de/docs/reference/deployment/)).

Öffnen Sie **„Extras“ → „Ein Bot in Ihrem Kanal“ → „Bot** im Panel **einrichten** “. In drei Schritten legen Sie den schreibgeschützten Zugriff, Ihren Kanal und das Intervall fest und starten anschließend den Witness. Die Veröffentlichungsrichtlinien, ein optionaler HTTP/SOCKS5-Proxy sowie eine benutzerdefinierte Bot-API-Adresse finden Sie unter **„Erweiterte Einstellungen** “. Das Formular lädt „`witness.json` “ herunter, wobei der Collector-Schlüssel dieses Arbeitsbereichs fest zugeordnet ist. Laden Sie das neu erstellte schreibgeschützte Token mit **„Zugriffsdatei speichern** als `witness-token.txt` “ herunter; legen Sie es zusammen mit einem auf dem Witness-Host erstellten `bot-token.txt` neben dieser JSON-Datei ab. Der Collector erhält niemals das Bot-Token. Durch das Herunterladen wird weder ein Dienst gestartet noch eine Nachricht veröffentlicht. Es wird kein gehosteter Projekt-Witness implizit registriert.

```
python -m tgwitness.witness run --config witness.json --check-config
python -m tgwitness.witness run --config witness.json
python -m tgwitness.witness fingerprint --config witness.json
```

Der erste Befehl überprüft Konfigurations- und Geheimdateien ohne Netzwerkanfragen oder Schlüsselerstellung. Pfade in JSON sind relativ zu dieser Datei; CLI-/Umgebungspfade sind relativ zum Arbeitsverzeichnis. Bewahren Sie den Fingerabdruck des Witness außerhalb seines Hosts auf. Der „Last-Poll“-Indikator des Collectors bestätigt lediglich eine Anfrage; die Veröffentlichung wird von Proof gemeldet oder im Witness-Protokoll und im Kanal überprüft.

Wenn sich das Panel hinter einem SSH-Tunnel befindet, stellen Sie nur den begrenzten Witness-Endpunkt auf einem separaten HTTPS-Hostnamen gemäß [diesem Caddy-Beispiel](https://github.com/phishdestroy/TgWitness/blob/main/deploy/Caddyfile.witness.example) bereit. Der Standard-Arbeitsbereich verwendet dann „`https://witness.example.org`“, andere Arbeitsbereiche verwenden „ `https://witness.example.org/profiles/ID`“. Token sind weiterhin erforderlich; das Panel und seine anderen API-Routen werden von diesem virtuellen Host nicht weitergeleitet.

Wählen Sie „`all`“ für regelmäßig veröffentlichte Checkpoints. Ein Fünf-Minuten-Intervall entspricht etwa 288 Einträgen pro Arbeitsbereich pro Tag. „`changes`“ und „`problems`“ lassen bewusst einige Überprüfungen unveröffentlicht. MTProxy ist für den Telegram-Client des Erfassers vorgesehen. Witness-HTTP-Abfragen und die HTTPS-Bot-API von Telegram verwenden ihre eigene direkte/HTTP/SOCKS5-Route ([Bot-API](https://core.telegram.org/bots/api)).

**Neben dem Collector, mit Docker** (derselbe Host – unabhängiger Prozess und Schlüssel, jedoch derselbe Betreiber): Geben Sie die Werte in „`.env`“ ein und starten Sie das Profil.

```
TGWITNESS_WITNESS_TOKEN=tgww_...
TGWITNESS_WITNESS_BOT_TOKEN=123456:ABC...
TGWITNESS_WITNESS_CHANNEL=@your_witness_channel
# another workspace: TGWITNESS_WITNESS_COLLECTOR=http://tgwitness:8787/profiles/<workspace ID>

docker compose --profile witness up -d
docker compose logs witness     # prints the witness key fingerprint
```

Verwenden Sie bei der Veröffentlichung eines Bildes den Code `docker compose --project-directory . -f deploy/compose/compose.image.yaml --profile witness up -d`.

**Auf dem Server einer anderen Person** (einem echten unabhängigen Zeugen): Kopieren Sie das Repository dorthin, legen Sie `TGWITNESS_WITNESS_COLLECTOR=https://your-collector.example.org` sowie die drei oben genannten Werte in `.env` fest, dann

```
docker compose --project-directory . -f deploy/compose/compose.witness.yaml up -d
```

oder ohne Docker:

```
python -m tgwitness.witness run --collector https://your-collector.example.org \
    --token-file witness-token.txt --bot-token-file bot-token.txt --channel @your_witness_channel
```

### Optionen

| Option | Umfeld | Standard | Bedeutung |
| --- | --- | --- | --- |
| `--interval` | `TGWITNESS_WITNESS_INTERVAL` | 10 | Intervalle zwischen den Überprüfungen: 1–1.440 |
| `--timeout` | `_TIMEOUT` | 30 | Wartezeit für den Collector und die Bot-API: 5–600 Sekunden |
| `--post` | `_POST` | `all` | `all`: alles in Ordnung; `changes`: ein neuer Ansatz oder ein Problem; `problems`: ausschließlich Probleme und fehlende Antworten |
| `--title` | `_TITLE` | `TgWitness witness` | Die ersten Wörter jedes Kanalbeitrags |
| `--collector-fingerprint` | `_COLLECTOR_FINGERPRINT` | – | Speichern Sie den Collector-Schlüssel, anstatt der ersten Antwort zu vertrauen |
| `--proxy` | `_PROXY` | direkt | `socks5://host:port` oder `http://host:port` |
| `--bot-api` | `_BOT_API` | `https://api.telegram.org` | Adresse der Bot-API, z. B. eines lokalen Bot-API-Servers |
| `--data-dir` | `_DATA` | `witness-data` | Witness-Schlüssel und Protokoll |
| `--config` | `_CONFIG` | – | JSON-Datei mit einer der oben genannten Optionen |

Die Sammeladresse, die Token und der Kanal stammen von `--collector`, `--token` oder `--token-file`, `--bot-token` oder `--bot-token-file` und `--channel` oder `_COLLECTOR`, `_TOKEN`, `_TOKEN_FILE`, `_BOT_TOKEN`, `_BOT_TOKEN_FILE` und `_CHANNEL`, wodurch vertrauliche Informationen aus der Prozessliste herausgehalten werden.

Eine Konfigurationsdatei verwendet Optionsnamen mit Unterstrichen sowie „`texts`“, wodurch die Wörter der Kanalbeiträge ersetzt werden:

```
{"collector": "https://your-collector.example.org", "token_file": "witness-token.txt",
 "bot_token_file": "bot-token.txt", "channel": "@your_witness_channel",
 "interval": 5, "timeout": 30, "post": "changes", "title": "Partner witness",
 "texts": {"ok": "journal head", "no_response": "no answer from the collector", "records": "records"}}
```

`texts`-Schlüssel: `ok`, `key_changed`, `rollback`, `fork`, `invalid`, `no_response`, `collector`, `records`, `head`. Die Befehlszeile hat Vorrang vor der Umgebung, die Umgebung vor der Datei. Unbekannte Optionen oder Textschlüssel führen dazu, dass der Witness mit einer Meldung angehalten wird, anstatt ignoriert zu werden. Der Wortlaut hat keinerlei Einfluss auf die Verifizierung: verify.py überprüft das signierte Token am Ende jedes Beitrags. Bei `--post changes` oder `problems` befinden sich Prüfungen, die nicht gepostet wurden, weiterhin im Zeugenjournal, und `verify.py` listet sie als „nie gepostet“ auf; der Startdatensatz benennt die Richtlinie. Jede Prüfung erscheint weiterhin im Journal, sodass weniger Posts weniger unabhängige Telegramm-Zeiten bedeuten, nicht jedoch weniger Prüfungen.

Auch ohne Kanal führt „Witness“ weiterhin sein Protokoll. Bewahren Sie den Fingerabdruck des „Witness“-Schlüssels (`python -m tgwitness.witness fingerprint`) an einem anderen Ort auf.

## Überprüfen

Auf der Seite des Zeugen: Exportieren Sie das Protokoll:

```
python -m tgwitness.witness export --out witness.zip
# Docker (add -f deploy/compose/compose.witness.yaml on a witness server):
docker compose exec witness python -m tgwitness.witness export --out /witness/witness.zip
docker compose cp witness:/witness/witness.zip .
```

Anschließend können Sie an jedem beliebigen Ort mit der signierten ZIP-Datei des Collectors und dem aus Telegram Desktop exportierten Kanal (*Chat-Verlauf exportieren* → JSON ergibt `result.json` ) oder dessen öffentlicher `https://t.me/s/…` -Seite:

```
python verify.py tgwitness-evidence.zip --fingerprint COLLECTOR_SHA256 \
    --witness witness.zip --witness-fingerprint WITNESS_SHA256 --channel result.json
```

`verify.py` überprüft das Zeugenprotokoll (Kette und Signaturen) und stellt anschließend sicher, dass **jeder „Head“, den der Zeuge gesehen hat**, **Teil des exportierten Protokolls ist**: Der Eintrag an dieser Stelle muss genau diesen Hash aufweisen. Ein „Head“, der nicht übereinstimmt, führt zum Scheitern der Überprüfung – das Protokoll wurde verändert, nachdem der Zeuge es gesehen hat. Es meldet außerdem nach dem Export gesehene Header, vom Zeugen aufgezeichnete Anomalien, fehlgeschlagene Antworten, Zeiträume, deren übereinstimmende Checkpoints in diesem Export vorhanden sind („Bezeugt von X bis Y“) sowie Lücken. Spätere Checkpoints verlängern diese Zeiträume nicht. Das Ergebnis umfasst die Nummer des zuletzt übereinstimmenden Datensatzes und die Anzahl der nachfolgenden Datensätze ohne passenden Checkpoint. Es zählen nur Antworten, die mit dem eigenen Schlüssel des Exports signiert wurden: Ein Export, der mit einem Schlüssel signiert wurde, den der Zeuge nie gesehen hat, wird als nicht bezeugt gemeldet, und ohne `--fingerprint` bleibt dessen Unterzeichner ungebunden. Bei „`--channel`“ muss jeder signierte Beitrag Datensatz für Datensatz mit dem Zeugen-Journal übereinstimmen: Geänderte Beiträge bestehen die Überprüfung nicht, fehlende Beiträge werden aufgelistet. Ein Datum in einem bereitgestellten Telegram-JSON-Export ist bearbeitbare Metadaten, die außerhalb des signierten Zeugen-Tokens liegen. Die Übereinstimmung mit dem Token authentifiziert nicht das Veröffentlichungsdatum; das Ergebnis gibt ausdrücklich an, dass keine Überprüfung des Veröffentlichungszeitpunkts durchgeführt wurde.

### Eine beglaubigte Exportgrenze ist erforderlich

Für eine Übergabe, die eine beglaubigte Abschlussaufzeichnung enthalten muss, fügen Sie bitte „`--require-witness`“ hinzu:

```
python verify.py tgwitness-evidence.zip --fingerprint COLLECTOR_SHA256 \
    --witness witness.zip --witness-fingerprint WITNESS_SHA256 --require-witness
```

Hierfür sind der unabhängig gespeicherte „Witness“-Fingerabdruck und ein übereinstimmender Checkpoint genau am Ende dieses Exports erforderlich. Ein Checkpoint, der nur ein früheres Präfix abdeckt, ist unzureichend. Unterbrechen Sie die Erfassung, lassen Sie den Zeugen den Endzustand beobachten und führen Sie den Export durch, bevor weitere Einträge in das Protokoll erfolgen; sollte sich das Protokoll ändern, speichern Sie einen weiteren Checkpoint und exportieren Sie diesen Zustand. Ein späterer Prüfpunkt allein kann den endgültigen Hash eines kürzeren Exports nicht verifizieren. Wenn zusätzlich „`--channel`“ angegeben wird, führen fehlende angegebene Beiträge oder ein leerer Übereinstimmungssatz zum Scheitern dieser strengen Prüfung. Ohne dieses Kennzeichen melden gewöhnliche Integritätsprüfungen weiterhin nicht beglaubigte Datensätze, ohne ein ansonsten intaktes Archiv zurückzuweisen.

Das Kennzeichen gewährleistet die Übereinstimmung mit den bereitgestellten, angehefteten Zeugenprotokollen. Der Betreiber muss weiterhin die Unabhängigkeit des Zeugen nachweisen und dessen Aufzeichnungen separat aufbewahren. Es bestätigt weder die Richtigkeit der Nachrichten noch die Vollständigkeit der Erfassung oder eine unabhängig gemessene Laufzeit.

Ein „Witness“ zeigt, was der Collector zu den jeweiligen Zeitpunkten gemeldet hat und dass spätere Exporte damit übereinstimmen. Er zeigt nicht, dass der Collector alles aufgezeichnet hat, was Telegram übermittelt hat, oder dass der Inhalt der Nachrichten wahr ist. Ein „Witness“, der vom selben Betreiber auf demselben Rechner ausgeführt wird, ist weniger aussagekräftig als einer, der von einer anderen Person ausgeführt wird.

Eine erhöhte Anzahl allein kann die Kontinuität im Online-Modus („Append-Only“) nicht nachweisen: Beim Offline-Vergleich muss jeder gespeicherte Präfix-Hash mit dem vollständigen Collector-Export abgeglichen werden. Ausfallzeiten von Witness und fehlgeschlagene Veröffentlichungen führen zu Zeiträumen ohne externe Verankerungen. Fehlende Beiträge können anhand eines aufbewahrten Witness-Protokolls gemeldet werden; weder ein Kanal noch ein Server, der vom selben Betreiber kontrolliert wird, stellt ein unveränderliches Archiv eines Dritten dar.
