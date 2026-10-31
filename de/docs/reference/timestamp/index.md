# Zeitstempel

Canonical page: https://phishdestroy.github.io/TgWitness/de/docs/reference/timestamp/

RFC 3161-Zeitstempel für signierte Checkpoints: Was wird an die Behörde gesendet und wie wird eine Antwort verifiziert?

TgWitness erstellt RFC-3161-Anfragen und überprüft die Antworten der Zeitstempel-Behörde (TSA). Bei diesem manuellen Verfahren wird weder eine TSA ausgewählt noch werden Daten übermittelt; der Beweismodus erledigt beides nach einem Zeitplan ([Beweisformat](https://phishdestroy.github.io/TgWitness/de/docs/reference/evidence/#rfc-3161-preparation-and-response-verification-02)). Eine vorbereitete Anfrage stellt **noch keinen Zeitstempel-Nachweis** dar.

## Was die Beweise belegen

Ablaufdiagramm · Beobachtungen zu Konten → SHA-256-Kette und Ed25519-Signaturen; SHA-256-Kette und Ed25519-Signaturen → Signierter Kontrollpunkt; Signierter Kontrollpunkt → Exakter Byte-Hash und zufälliger Nonce; Exakter Byte-Hash und zufälliger Nonce → RFC 3161-Anfrage; RFC 3161-Anfrage → Unabhängige TSA; Unabhängige TSA → Signierte Antwort der TSA; Signierter Kontrollpunkt → Daten, Nonce und explizite CA-Vertrauenswürdigkeit überprüfen; Signierte Antwort der TSA → Daten, Nonce und explizite CA-Vertrauenswürdigkeit überprüfen · Beobachtungen zuKonten · SHA-256-Kette undEd25519-Signaturen · SignierterKontrollpunkt · Exakter Byte-Hash undzufälliger Nonce · RFC 3161-Anfrage · Unabhängige TSA · Signierte Antwort derTSA · Daten, Nonce undexpliziteCA-Vertrauenswürdigkeit überprüfen

**Diagramm als Text**

1. Beobachtungen zu Konten → SHA-256-Kette und Ed25519-Signaturen
2. SHA-256-Kette und Ed25519-Signaturen → Signierter Kontrollpunkt
3. Signierter Kontrollpunkt → Exakter Byte-Hash und zufälliger Nonce
4. Exakter Byte-Hash und zufälliger Nonce → RFC 3161-Anfrage
5. RFC 3161-Anfrage → Unabhängige TSA
6. Unabhängige TSA → Signierte Antwort der TSA
7. Signierter Kontrollpunkt → Daten, Nonce und explizite CA-Vertrauenswürdigkeit überprüfen
8. Signierte Antwort der TSA → Daten, Nonce und explizite CA-Vertrauenswürdigkeit überprüfen

Die Signatur des Erfassers verknüpft die Datensätze mit seinem Schlüssel. Eine vertrauenswürdige TSA-Antwort kann nachweisen, dass ein bestimmter Kontrollpunkt zum von der TSA angegebenen Zeitpunkt existierte. Der Kontrollpunkt kann dann das Protokollpräfix verknüpfen. Dies belegt jedoch weder den Zeitpunkt jeder einzelnen Telegram-Aktion noch die Richtigkeit der erfassten Inhalte.

## Vorgehensweise

1. Bewahren Sie den Fingerabdruck des Sammelschlüssels über einen separaten vertrauenswürdigen Kanal auf. Ein Schlüssel, der ausschließlich aus der untersuchten ZIP-Datei stammt, reicht nicht aus, um den Sammler zu identifizieren.
2. Laden Sie unter **„Exporte“ → „Zeitstempelanfrage vorbereiten“** die ZIP-Datei mit der Anfrage für den ausgewählten Arbeitsbereich herunter. Entpacken Sie die Dateien „`checkpoint.json`“, „`timestamp.tsq`“, „`SHA256SUMS`“ und „`README.txt`“. Ändern Sie die Checkpoint-Bytes nicht.
3. Wählen Sie ein für die Untersuchung geeignetes TSA aus. Senden Sie „`timestamp.tsq`“ gemäß der dokumentierten Methode, zusammen mit „`application/timestamp-query`“ für einen HTTP-Dienst. Speichern Sie die ursprüngliche binäre Antwort als „`timestamp.tsr`“ sowie den Endpunkt, den Abrufzeitpunkt und das Ergebnis der Anfrage. Die Anfrage enthält einen Hash und einen Nonce anstelle von Nachrichten; die Netzwerk-Metadaten geben die Anfrage dennoch preis.
4. Beziehen Sie das vertrauenswürdige Stammzertifikat unabhängig von der Antwort sowie alle erforderlichen Zwischenzertifikate. Ein Zertifikat in der Antwort wird nicht allein dadurch vertrauenswürdig, dass es dort enthalten ist.
5. Überprüfen Sie anhand einer vertrauenswürdigen TgWitness-Installation Folgendes:

```
python -m tgwitness.anchor verify --checkpoint checkpoint.json --request timestamp.tsq --response timestamp.tsr --ca trusted-tsa-root.pem
```

Fügen Sie bei Bedarf `--intermediates tsa-intermediates.pem` oder `--openssl /path/to/openssl` hinzu. OpenSSL muss `ts` unterstützen. Unter Windows durchsucht der Verifizierer zudem die Standard-Git- Installation. OpenSSL 3.5.9 wurde lokal mit einer synthetischen CA/TSA getestet.

1. Exportieren Sie nach dem Checkpoint ein signiertes Protokoll als ZIP-Datei, sodass es dieses Präfix enthält. Überprüfen Sie dies anhand des unabhängig bekannten Fingerabdrucks:

```
python tgwitness/verify.py evidence.zip --fingerprint TRUSTED_SHA256 --checkpoint checkpoint.json
```

1. Bewahren Sie die ZIP-Datei, den Checkpoint, die Anfrage, die Antwort, die Zertifikatskette, die Verifizierungsergebnisse sowie die Übergabeprotokolle außerhalb des Collectors auf. Wiederholen Sie die Verifizierung bei Erhalt.

So erstellen Sie eine Anfrage anhand eines gespeicherten Checkpoints:

```
python -m tgwitness.anchor prepare checkpoint.json --out timestamp-request.zip
```

Bei der Aufbereitung wird das JSON-Format kanonisiert und der entsprechende Checkpoint in das Archiv aufgenommen. Verwenden Sie die **Checkpoint-Bytes aus diesem Archiv** für die TSA-Verifizierung, auch wenn die Eingabedatei abweichende Leerzeichen enthielt.

## Grenzen der Verifizierbarkeit

| Überprüfen | Aktuelles Verhalten |
| --- | --- |
| Daten | Der SHA-256-Hash der exakten Checkpoint-Bytes muss mit der Antwort übereinstimmen. |
| Anfrage | Mit „`--request`“ werden die ursprüngliche Abfrage und der Nonce verifiziert |
| TSA-Signatur | OpenSSL überprüft die Signatur und die Signaturkette bis hin zur explizit angegebenen Zertifizierungsstelle (CA). |
| Signatur des Erfassers | Unabhängig verifiziert durch den Protokollprüfer mit einem festgesteckten Schlüssel |
| Widerruf | Kein automatischer Abruf von OCSP/CRL |
| Langfristige Gültigkeit | Keine Archivvalidierung nach Ablauf des Zertifikats |
| Geplante Einreichung | Beweismodus, standardmäßig deaktiviert |

`--request` ist technisch gesehen optional, doch wird durch dessen Weglassen die Überprüfung des ursprünglichen Nonce verhindert. Für diesen vollständigen Vorgang muss das Ergebnis `request_checked` wahr sein. Die Zertifikatsüberprüfung erfolgt gemäß den Regeln und der Überprüfungsdauer des installierten OpenSSL. Die langfristige Aufbewahrung erfordert eine separate Richtlinie für Zertifikate und Widerrufsnachweise.

Eine gültige kryptografische Signatur ist nicht automatisch ein qualifizierter Zeitstempel oder eine Feststellung der rechtlichen Zulässigkeit. Sollte ein Betreiber Beobachtungen vor dem Zeitstempeln gefälscht haben, verankert die TSA diese Bytes; sie bestätigt jedoch nicht deren Wahrheitsgehalt.

## Übergabeprotokoll

Erfassen Sie die Fall-ID, den Absender und den Empfänger, den UTC-Zeitpunkt der Übertragung und deren Quelle, den Zweck, Dateinamen/SHA-256-Werte, den Fingerabdruck des Erfassers, den Sequenzbereich, bekannte Lücken, die Version des Verifizierers und das Verifizierungsergebnis. Signieren Sie diese Aufzeichnung und bewahren Sie sie unabhängig im Rahmen der Prozesse Ihrer Organisation auf. Ein System zur Aufbewahrung von Aufzeichnungen durch mehrere Benutzer ist in TgWitness nicht implementiert.

Während der Entwicklung wurde keine unabhängige Live-TSA kontaktiert. Bei lokalen Tests wird eine synthetische CA/TSA erstellt, um die Kompatibilität sowie die Ablehnung geänderter Daten, Nonces oder CAs zu überprüfen.
