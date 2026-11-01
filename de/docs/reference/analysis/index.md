# Archivanalyse

Canonical page: https://phishdestroy.github.io/TgWitness/de/docs/reference/analysis/

Durchsuchen Sie gespeicherte Nachrichten, überprüfen Sie KI-Eingaben und erstellen Sie Analyseberichte mit Quellenangaben.

[Anleitung zum Arbeitsablauf](https://phishdestroy.github.io/TgWitness/docs/archive/) · [Wiki](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

Verwenden Sie **Journal** für die lokale Suche ohne KI. Für **Fragen Sie das Archiv** aktivieren und konfigurieren Sie zunächst einen Anbieter unter **Integrationen**. Über die Arbeitsbereichsauswahl wird das Konto ausgewählt; über das Formular werden Chats und der Beobachtungszeitraum festgelegt. Die Suche nach relevanten Inhalten erfolgt lokal. Eine exakte Phrase oder Domain grenzt die Suche ein; eine Nachrichten-ID fordert gespeicherte Versionen an. Überprüfen Sie die Auszüge und öffnen Sie die zugehörigen Journaleinträge oder den Kontext. Es gibt keine Vektordatenbank und keine automatischen Telegram-Aktionen.

## Anbieter und Einwilligung

Die KI ist in jedem Arbeitsbereich standardmäßig deaktiviert. Nur der Hauptadministrator kann das Modell, den Endpunkt, den verschlüsselten API-Schlüssel, Kontext-/Ausgabebegrenzungen, das Timeout und das tägliche Anfrage-Kontingent konfigurieren. Der Schlüssel wird niemals an den Browser zurückgegeben. Lassen Sie das Schlüsselfeld leer, um den aktuellen Schlüssel beizubehalten, oder entfernen Sie ihn explizit.

Ollama verwendet seinen dokumentierten [`/api/chat`-Endpunkt](https://docs.ollama.com/api/chat) mit nicht-streamingbasierter JSON-Ausgabe. Die Standardadresse lautet `http://127.0.0.1:11434` auf dem TgWitness-Server. Der Betreiber kann sie mithilfe von `TGWITNESS_AI_LOCAL_ENDPOINT` ändern; hierbei handelt es sich nicht um eine modellgesteuerte Adresse. Installieren Sie das ausgewählte Modell selbst. TgWitness lädt es nicht automatisch herunter.

Der kompatible Anbieter erwartet eine Basis-URL, die auf `/v1` endet, sowie das [„Chat Completions“-Protokoll](https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create): `messages`, JSON-Antwortmodus, `max_completion_tokens` und `choices[0].message.content`. Dienste, bei denen diese Felder fehlen, werden nicht unterstützt. Bei Verbindungstests wird synthetischer Text gesendet, der auf das Anfragekontingent angerechnet wird.

Jede Anfrage nutzt die im Arbeitsbereich konfigurierte externe Route. Eine blockierte Route oder ein ausschließlich für Telegram bestimmter MTProxy führt zu einem Fehler; es erfolgt kein direkter Wiederholungsversuch. Eine bewusst konfigurierte lokale Ollama-Adresse ermöglicht ein privates Ziel, wobei weiterhin die gewählte Route genutzt wird. Für andere private Dienste gilt die bestehende Opt-in-Möglichkeit für private Ziele auf Serverebene. Das Panel zeigt den tatsächlich konfigurierten Endpunkt an.

Vor der Generierung zeigen **die an das Modell gesendeten Daten** die Anfrage an: Frage, markierte Auszüge, Ereignistypen, Beobachtungszeitpunkte und Abdeckungsmarker. Telegram- Sitzungen, Rohdatenfelder, Anbieterschlüssel, Anhangsbytes und das vollständige Protokoll sind nicht Teil dieses Kontexts. Deaktivieren Sie unerwünschte Quellen und stimmen Sie anschließend der Verarbeitung ausdrücklich zu. Externe Anbieter können übermittelte Inhalte gemäß ihren eigenen Richtlinien aufbewahren. Lokale Ausführung bedeutet, dass der Endpunkt lokal ist; dies ist keine Garantie für das Verhalten eines unabhängig konfigurierten Dienstes.

Weltweit sind höchstens zwei gleichzeitige Anfragen an den Anbieter zulässig, eine pro Arbeitsbereich. Eine Vorschau läuft nach zehn Minuten ab und kann eine Antwort generieren. Die vom Anbieter gemeldeten Token-Zahlen werden angezeigt; eine Kostenschätzung erscheint erst, wenn sowohl Eingangs- als auch Ausgangstarife konfiguriert wurden. Fehlgeschlagene Versuche verbrauchen ebenfalls das tägliche Anfragedatenvolumen. Automatische Wiederholungsversuche verbrauchen kein zusätzliches Datenvolumen.

## Quellen und Einschränkungen

Die Abfrage untersucht den gespeicherten Nachrichtentext mit einer begrenzten lexikalischen Suche. Sie liefert bis zu 24 Quellen und kennzeichnet abgeschnittene Auszüge oder unvollständige Ergebnismengen. Der Zeitraum bezieht sich auf **den Beobachtungszeitraum** und stellt keine Behauptung dar, dass der Telegram-Verlauf vollständig ist. Ereignisse, die den gesamten Arbeitsbereich betreffen, werden beim Zugriff auf Chat-Ebene zurückgehalten. Fehlende Daten werden als im verfügbaren Archiv nicht gefunden beschrieben.

Das Modell erhält keine Hilfsmittel. Seine Quell-IDs werden anhand der ausgewählten Datensätze abgeglichen, Hashwerte werden erneut überprüft, und zitierte Zeichenfolgen müssen in diesen Datensätzen vorkommen. Unbekannte IDs, geänderte Zitate und nicht zitierte Behauptungen führen zur Ablehnung der Antwort. Die Anwendung erstellt Links; vom Modell generierte URLs werden nicht als Quellenangaben verwendet. Diese Prüfungen stellen die Existenz der Quelle und die Genauigkeit der Zitate fest, nicht die Richtigkeit einer Schlussfolgerung. Überprüfen Sie Schlussfolgerungen anhand der Datensätze, bevor Sie sich auf sie verlassen.

## Berichte

Speichern Sie eine geprüfte Antwort als separaten Analysebericht. Dieser enthält die Modellzusammenfassung, die beobachtete Chronologie, extrahierte Links und Handles, Bearbeitungs-/Löschprotokolle, Erfassungsgrenzen sowie Hash-Werte der Quellereignisse. Der Anbieter, das Modell, der Endpunkt, die Uhrzeit und die Version der Prompt-Vorlage werden ebenfalls angegeben. Es werden keine Identitäten automatisch zusammengeführt.

Änderungen und Notizen der Analysten werden getrennt von der Modellzusammenfassung gespeichert. Berichte befinden sich in verschlüsselten abgeleiteten Dateien, mit einem Index außerhalb des signierten Ereignisstroms; die ursprünglichen Ereignisse und Medien bleiben unverändert. Nur der Eigentümer oder Administrator kann einen Bericht öffnen, und der Zugriff auf die Quelle wird erneut überprüft. Für den Download ist zudem eine Exportberechtigung erforderlich. Version 1 signiert keine Berichte und impliziert nicht, dass die Schlussfolgerungen des Modells verifizierte Beweise sind. Beschränkungen: 100 Berichte pro Arbeitsbereich und 100 Analystenüberarbeitungen pro Bericht.

Informationen zu manueller OCR und Transkripten finden Sie unter [„Medienverarbeitung](https://phishdestroy.github.io/TgWitness/de/docs/reference/media-analysis/)“. Informationen zum Kundenzugang finden Sie unter [„MCP](https://phishdestroy.github.io/TgWitness/de/docs/reference/mcp/)“.
