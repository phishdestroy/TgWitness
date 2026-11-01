# Beweise und Vertrauen

Canonical page: https://phishdestroy.github.io/TgWitness/de/docs/reference/evidence-trust/

Was Exporte, Videos, Webarchive und signierte Datensätze belegen können und wie das Erfassungsgerät ihre Zuverlässigkeit beeinflusst.

Ein Export, ein Screenshot oder eine Aufzeichnung kann ein nützliches Beweismittel sein. Seine Zuverlässigkeit hängt davon ab, wie es erfasst, aufbewahrt und bestätigt wurde. **Ein gültiger Hash oder eine Signatur überprüft das gespeicherte Material; er belegt nicht eigenständig, dass das Erfassungsgerät den wahrheitsgemäßen Quellinhalt empfangen hat.** Diese Abgrenzung gilt auch für TgWitness.

Dieser Leitfaden trennt die technische Überprüfung von der rechtlichen Bewertung. Die Produktdokumentation und die nachstehenden rechtlichen Bestimmungen wurden am 1. November 2026 überprüft; der Hunchly-Vergleich beschreibt die veröffentlichte Dokumentation und stellt keine neue Produktprüfung dar.

## Wo Vertrauen ins Spiel kommt

Ablaufdiagramm · Telegram-Konto und -Dienst → Client, Browser und Betriebssystem; Client, Browser und Betriebssystem → Export, Video- oder Seitenaufzeichnung; Export, Video- oder Seitenaufzeichnung → Hashes und Signaturen des Erfassers; Hashes und Signaturen des Erfassers → Von einer unabhängigen Partei gespeicherter Hash · Telegram-Konto und-Dienst · Client, Browser undBetriebssystem · Export, Video- oderSeitenaufzeichnung · Hashes und Signaturendes Erfassers · Von einer unabhängigenPartei gespeicherterHash

**Diagramm als Text**

1. Telegram-Konto und -Dienst → Client, Browser und Betriebssystem
2. Client, Browser und Betriebssystem → Export, Video- oder Seitenaufzeichnung
3. Export, Video- oder Seitenaufzeichnung → Hashes und Signaturen des Erfassers
4. Hashes und Signaturen des Erfassers → Von einer unabhängigen Partei gespeicherter Hash

Das hier zugrunde liegende Bedrohungsmodell geht davon aus, dass ein Angreifer oder Betreiber die Erfassungsumgebung verändern kann, bevor die Beweismittel gesichert werden. Es handelt sich hierbei um eine bedingte Analyse und nicht um die Behauptung, dass ein bestimmtes Gerät oder Produkt kompromittiert wurde.

Ein offizieller Client und eine verschlüsselte Verbindung tragen zum Schutz der normalen Nutzung bei. Sie machen das umgebende Betriebssystem, den Browser oder die Anzeige jedoch nicht unabhängig vertrauenswürdig. Wenn Inhalte nach der Entschlüsselung, aber vor der Erfassung ersetzt werden, kann der Exporteur sie korrekt speichern und der Unterzeichner sie korrekt signieren. Für keinen der beiden Vorgänge ist ein defekter Hash-Algorithmus oder eine gefälschte Signatur erforderlich.

Ein auf demselben Gerät aufgenommenes Video kann dieselbe ersetzte Darstellung aufzeichnen. Eine separate Kamera kann bestätigen, was auf dem Display angezeigt wurde, aber das Display allein beglaubigt nicht, was Telegram bereitgestellt hat. Ebenso können übereinstimmende HTML-, JSON-, Screenshots und Browser-Protokolle aus einer kontrollierten Umgebung denselben Fehler aufweisen. Ihre Übereinstimmung ist ein nützlicher Kontext; sie stellt jedoch nicht automatisch eine unabhängige Bestätigung dar.

## Was jede Form von Beweismaterial beiträgt

| Material | Nützlicher Beitrag | Offene Frage |
| --- | --- | --- |
| Telegram-Desktop-Export | Lesbare oder maschinenlesbare Unterhaltungen und ausgewählte Medien | Wer hatte die Kontrolle über die Client- und Exportdateien, und was war verfügbar bzw. ausgeschlossen? |
| Screenshot oder Bildschirmaufzeichnung | Sichtbarer Kontext, Abfolge von Aktionen und Darstellung | Spiegelt die Darstellung die Quelle originalgetreu wider, und was geschah außerhalb der Aufzeichnung? |
| Lokales Webarchiv, einschließlich MHTML | Seiteninhalt und zugehörige Ressourcen zur späteren Überprüfung | Was hat der Browser dem Archiver bereitgestellt, und wer hat diesen Browser gesteuert? |
| Vom Sammler signiertes Archiv | Änderungen an signierten Bytes können relativ zu einem vertrauenswürdigen Schlüssel und einer beibehaltenen Referenz erkannt werden | Wer hatte vor der Signierung die Kontrolle über den Signaturschlüssel und die Eingabe? |
| Unabhängig beibehaltener Kontrollpunkt oder verifizierter Zeitstempel | Ein beibehaltener Hash oder Checkpoint zum Vergleich mit einer späteren Einreichung | Welche Bytes und welche Grenzen werden abgedeckt, und was bescheinigt die unabhängige Partei tatsächlich? |

Telegram dokumentiert seinen Desktop-Export als Offline-HTML-/JSON-Kopie und seine Takeout-API als Möglichkeit, ausgewählte Kontodaten abzurufen. Diese Beschreibungen enthalten keine Telegram-Signatur für das endgültige exportierte Archiv, die ein Empfänger überprüfen könnte. Unsere Schlussfolgerung beschränkt sich auf diese dokumentierten Exportmechanismen; sie ist keine Behauptung, dass Telegram-Beweismittel keinen rechtlichen Wert haben.[Telegram-Desktop-Export](https://telegram.org/blog/export-and-more),[Takeout-API](https://core.telegram.org/api/takeout).

Die gleiche Unterscheidung gilt für Hintergrundanfragen, Cache-Einträge und Netzwerkprotokolle. Sie können Unstimmigkeiten aufdecken und dazu beitragen, eine Erfassung zu untermauern. Ihre Komplexität allein sagt nichts darüber aus, wer sie erstellt hat. Ein unabhängig betriebenes Archiv oder ein separat beschaffter Dienstdatensatz stellt eine weitere Quelle zum Vergleich dar, vorbehaltlich seiner eigenen Beschränkungen hinsichtlich Erfassung und Aufbewahrung.

## Hunchly veranschaulicht dieselbe Grenze

Die Dokumentation von Hunchly beschreibt die SHA-256-Hash-Erzeugung von MHTML-Erfassungen, Fotos und Anhängen mit unabhängiger Hash-Überprüfung. Sie erklärt auch, warum eine veränderte Datei, die mit einem neu berechneten Hash versehen ist, diesen Vergleich bestehen kann, und verweist auf Signaturen und Quellenbestätigung als zusätzliche Prüfungen.[Hunchly: Hash-Erzeugung für Inhalte, Fotos und Anhänge](https://support.maltego.com/support/solutions/articles/15000061289-content-photo-and-attachment-hashing).

Der veröffentlichte *„Evidence Guide“*, Version 1.0 vom 17. Oktober 2018, beschreibt lokal generierte GPG-Schlüssel und Signaturen für MHTML-Erfassungen. Er identifiziert ausdrücklich den Zugriff auf den lokalen privaten Schlüssel als Möglichkeit, modifiziertes Material erneut zu signieren. Dies ist eine dokumentierte Vertrauensbeschränkung, kein Hinweis auf einen nicht offengelegten aktuellen Exploit. Der Leitfaden besagt außerdem, dass Chrome die MHTML-Erfassung durchführt. Würde man Hunchly so beschreiben, dass es sich ausschließlich auf die Reputation eines Ermittlers stützt, würden diese technischen Kontrollmechanismen außer Acht gelassen.[Hunchly-Beweisleitfaden, Abschnitte 2–4](https://hunch.ly/resources/Hunchly%20Evidence%20Guide.pdf).

Ob mit einem bestimmten Produkt gesammeltes Material in einem Fall zugelassen wurde, hängt von der jeweiligen Entscheidung und den Umständen ab. Wir erheben hier keinen Anspruch darauf, wie häufig Gerichte Hunchly oder TgWitness akzeptieren, oder darauf, dass eines der beiden Produkte eine allgemeine gerichtliche Zulassung besitzt.

## Was TgWitness hinzufügt und wo sein Schutz endet

TgWitness zeichnet Beobachtungen in einem signierten, verlinkten Protokoll auf und stellt Exporte bereit, die ein Empfänger überprüfen kann. Gespeicherte Kontrollpunkte, Zeitstempel und ein separater Zeuge bieten Prüfern Referenzen, die über die aktuellen Dateien des Erfassers hinausgehen. Sie helfen dabei, Änderungen an zuvor festgehaltenen Datensätzen aufzudecken. Abdeckungsaufzeichnungen und explizite Erfassungsergebnisse helfen dabei zu erklären, was erfasst wurde und was nicht.[Beweismittelformat und -übergabe](https://phishdestroy.github.io/TgWitness/de/docs/reference/evidence/), [Erfassungsumfang](https://phishdestroy.github.io/TgWitness/de/docs/reference/collection/).

Der Zeitpunkt einer möglichen Ersetzung ist von Bedeutung:

1. **Nach der Signierung, ohne Zugriff auf den Signaturschlüssel:** Das Ändern eines signierten Datensatzes oder einer an das Manifest gebundenen Datei führt zum Scheitern der Verifizierung durch einen vertrauenswürdigen Prüfer und Schlüssel.
2. **Mit dem Sammler-Schlüssel gilt nach dem Beibehalten eines unabhängigen Prüfpunkts Folgendes:** Ein Ersatzprotokoll kann gültige neue Signaturen enthalten, aber ein geändertes Präfix scheitert beim Vergleich mit diesem früheren Prüfpunkt. Ein Prüfpunkt, der nur auf demselben kontrollierten Gerät aufbewahrt wird, kann zusammen mit dem Protokoll ersetzt werden. Datensätze jenseits der beibehaltenen Grenze erfordern eine eigene Erfassung.
3. **Bevor ein einen Beobachtungsvorgang abdeckender Checkpoint unabhängig gesichert wird:**können falsche Eingaben erfolgreich signiert und verankert werden, einschließlich neuer Datensätze, die nach einem früheren Checkpoint angehängt wurden. Der resultierende Checkpoint oder Zeitstempel deckt diese falschen Datensätze weiterhin ab; er belegt jedoch nicht deren Richtigkeit.

Ein TgWitness-Zeuge empfängt die signierten Checkpoints des Sammlers; er liest nicht eigenständig die zugrunde liegende Telegram-Konversation. Sein Schlüssel und seine gespeicherten Datensätze müssen separat als vertrauenswürdig eingestuft werden. Wenn das gesamte übermittelte Journal beglaubigt werden muss, verwenden Sie das[Übergabeverfahren, das die endgültige Exportgrenze erfordert](https://phishdestroy.github.io/TgWitness/de/docs/reference/witness/#require-a-witnessed-export-boundary). Ein gewöhnlicher Integritätsdurchlauf kann dennoch einen nicht beglaubigten Endabschnitt melden.

Eine verifizierte RFC-3161-Antwort kann belegen, dass ein Checkpoint zum von der Behörde angegebenen Zeitpunkt existierte. Sie belegt nicht, wann eine Telegram-Nachricht gesendet wurde oder ob ihr Inhalt wahr war. Eine vorbereitete Anfrage oder eine beigefügte Antwortdatei allein reicht nicht aus. Bei der Überprüfung eines Exports mit `tgwitness.verify` erfordert die Überprüfung der enthaltenen TSA-Signaturen eine explizit vertrauenswürdige Zertifizierungsstelle über `--tsa-ca`. OpenTimestamps-Belegungen erfordern eine unabhängige `ots verify`, gegebenenfalls mit Nachweisen zur Aktualisierung. [Zeitstempelverfahren](https://phishdestroy.github.io/TgWitness/de/docs/reference/timestamp/), [RFC 3161](https://www.rfc-editor.org/rfc/rfc3161.html).

[Bei der Erfassung in GitHub Actions](https://github.com/phishdestroy/TgWitness/blob/main/docs/SEALED-ACTIONS.md) sammelt ein temporär gehosteter Runner die Nachrichten. Die Attestation bindet das Archiv an einen genehmigten Workflow. Dieser Modus vertraut weiterhin auf GitHub, die genehmigte Software und deren Abhängigkeiten, den Helfer/Browser und den Tunnel. Es handelt sich nicht um vertrauliche Hardware, eine Telegram-Signatur oder einen Nachweis, dass niemand auf den Host zugegriffen hat. Eine lokal signierte Ausführungsbestätigung ist ebenfalls eine selbst gemeldete Messung, keine Hardware-Attestation.

## Die rechtliche Tragweite hängt von der Grundlage ab

Vier Fragen sollten klar voneinander getrennt bleiben: ob das Element das ist, was es zu sein vorgibt, ob die übermittelten Bytes mit dem gespeicherten Datensatz übereinstimmen, ob der Inhalt die behaupteten Tatsachen stützt und ob geltende Vorschriften seine Verwendung zulassen. Eine kryptografische Prüfung deckt nur einen Teil dieser Grundlage ab.

In US-Bundesverfahren sieht Regel 901 Möglichkeiten zur Beglaubigung von Beweismitteln vor, einschließlich der Aussage sachkundiger Zeugen und von Beweisen über einen Prozess oder ein System. Die Regeln 902(13) und 902(14) sehen Beglaubigungswege für bestimmte elektronische Aufzeichnungen und Kopien vor, verbunden mit verfahrensrechtlichen Anforderungen. In den Erläuterungen des Ausschusses wird die Beglaubigung von Fragen wie Hörensagen, Relevanz und Zuordnung unterschieden. Eine Software-Signatur allein stellt nicht die dort beschriebene Beglaubigung durch eine qualifizierte Person dar.[Bundesbeweisregel 901](https://www.law.cornell.edu/rules/fre/rule_901),[Bundesbeweisregel 902](https://www.law.cornell.edu/rules/fre/rule_902).

Soweit das kanadische Beweisgesetz (Evidence Act) Anwendung findet, regelt § 31.1 die Beglaubigung von elektronischen Dokumenten. § 31.2 verknüpft die Regel des besten Beweismittels mit der Systemintegrität oder einer anwendbaren Vermutung; § 31.3 legt die Umstände für eine Vermutung der Integrität fest. Hierbei handelt es sich um definierte Beweisvoraussetzungen, nicht um eine pauschale Vermutung, dass jeder lizenzierte Ermittler oder jedes kommerzielle Produkt unfehlbar ist. [Kanadisches Beweisgesetz, 31.1](https://laws-lois.justice.gc.ca/eng/acts/C-5/section-31.1.html),[31.2](https://laws-lois.justice.gc.ca/eng/acts/C-5/section-31.2.html),[31.3](https://laws-lois.justice.gc.ca/eng/acts/C-5/section-31.3.html).

Diese Beispiele stellen keine Feststellung zur Zulässigkeit in einer anderen Gerichtsbarkeit oder einem bestimmten Fall dar. Die technischen Prüfungen sollten konsequent auf Material angewendet werden, das eine Behauptung stützt oder in Frage stellt. Dieser Leitfaden erhebt keinen Anspruch darauf, dass Beweismittel der Anklage im Allgemeinen leichter zuzulassen sind als Beweismittel der Verteidigung.

## Erstellen Sie eine Dokumentation, die von einer anderen Person bewertet werden kann

- Beschreiben Sie das Konto, das Erfassungsgerät, den Betreiber, die Softwareversion, die Zugriffsrechte, den ausgewählten Umfang und den Erfassungszeitraum. Erfassen Sie Unterbrechungen und mögliche Kompromittierungen, anstatt eine erfolgreiche Signaturprüfung als Test für ein einwandfreies Gerät zu betrachten.
- Behalten Sie die ursprünglichen Pakete bei und dokumentieren Sie Übertragungen, Hashes und den Zeitstempel. Bewahren Sie den Schlüssel-Fingerabdruck und die Checkpoints über einen separat vertrauenswürdigen Kanal auf. Überprüfen Sie die tatsächliche Abdeckung durch Zeugen oder Zeitstempel, bevor Sie diese in einem Bericht beschreiben.
- Suchen Sie nach einer der Behauptung angemessenen unabhängigen Bestätigung: Aufzeichnungen eines anderen Teilnehmers, eine unabhängige Erfassung oder rechtmäßig erlangte Dienstaufzeichnungen. Erläutern Sie deren Unabhängigkeit und Einschränkungen; eine Übereinstimmung zwischen Kopien reicht für sich allein nicht aus.
- Behalten Sie den relevanten Kontext bei. Kennzeichnen Sie ausgelassene Dateien, nicht verfügbare Verlaufsdaten und Schwärzungen. Erstellen Sie bei Bedarf eine [separate, minimierte Offenlegung](https://github.com/phishdestroy/TgWitness/blob/main/docs/ACCOUNT-EXPORT.md#prepare-a-disclosure-for-a-lawyer-or-another-recipient)und beschreiben Sie deren Umwandlungen, ohne sie als vollständiges Original darzustellen.
- Geben Sie dem Empfänger Anweisungen zur Überprüfung sowie das für diese Überprüfungen erforderliche Material. Halten Sie Beobachtungen, technische Feststellungen und die Schlussfolgerungen des Analysten klar voneinander unterscheidbar.

Geben Sie für eine bestimmte Übergabe den Archiv-Hash, den vertrauenswürdigen Schlüssel, das Verifizierungsergebnis sowie die genaue, extern abgedeckte Grenze an. Beschreiben Sie die Authentizität der Quelle, die Zuweisung zum Konto, die Vollständigkeit und die rechtlichen Schlussfolgerungen separat. Dies liefert dem nächsten Prüfer konkrete Aussagen, die er untersuchen kann.
