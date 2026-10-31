# Ausgehende Webhooks

Canonical page: https://phishdestroy.github.io/TgWitness/de/docs/reference/webhooks/

Sendet definierte Ereignisse mit HMAC-Signaturen, Wiederholungsversuchen und Zustellstatus an HTTPS-Empfänger.

**Aktueller Hauptpunkt:** Verwenden Sie einen Source-Checkout; die portable Vorschauversion 0.7.0 stammt aus einer Zeit vor der Einführung dieser Funktion.

[Anleitung zum Arbeitsablauf](https://phishdestroy.github.io/TgWitness/docs/archive/) · [Wiki](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

Öffnen Sie **„Integrationen“ → „Ausgehende Webhooks“** im ausgewählten Arbeitsbereich. Fügen Sie einen HTTPS-Empfänger hinzu, wählen Sie „Collector/Media/Export“-Ereignisse aus und wählen Sie optional Chats für neue Beobachtungen und Änderungen aus. Der Nachrichtentext ist standardmäßig deaktiviert. Durch das Aktivieren von Auszügen werden den Ereignissen zu Nachrichtenänderungen maximal 1.000 Zeichen hinzugefügt; Telegram-Rohdatenfelder und Anmeldedaten werden niemals gesendet.

Kopieren Sie den HMAC-Schlüssel einmalig in die geschützte Konfiguration des Empfängers. Er wird im Tresor von TgWitness verschlüsselt und kann nicht über das Panel abgerufen werden. Löschen Sie ein Ziel und erstellen Sie es neu, um es zu rotieren. **Senden Sie synthetische**Testwarteschlangen einen Test ohne Chat-Inhalt; aktualisieren Sie den Zustellstatus, um das Ergebnis zu sehen.

Die Bereitstellung erweitert den bestehenden Benachrichtigungskreislauf neben Apprise. Sie nutzt die externe Route des Arbeitsbereichs und bestehende Einschränkungen für private Ziele. Es findet keine direkte Ausweich- oder Weiterleitung statt. URLs dürfen keine Anmeldedaten, Abfragezeichenfolgen oder Fragmente enthalten; private Adressen erfordern die Netzwerk-Zustimmung auf Serverebene, keine Einstellung, die ein Panel-Benutzer umgehen kann.

## Nutzdaten und Signatur

Schema: [`tgwitness.webhook/1`](https://github.com/phishdestroy/TgWitness/blob/main/integrations/webhook.schema.json). Jede Nutzlast enthält `event_id`, `timestamp`, `workspace`, `type`, `synthetic` und Zähler. Protokollbasierte Ereignisse enthalten ihre Reihenfolge und ihren Hashwert. Der Abschluss eines vollständigen Exports und synthetische Tests sind Übermittlungsereignisse ohne erfundenen Verweis auf ein signiertes Protokoll. Telegram-Löschbenachrichtigungen und `missing_on_recheck` bleiben eigenständige Typen.

Der Header „`X-TgWitness-Signature`“ lautet „`t=UNIX_SECONDS,v1=HEX_HMAC_SHA256`“. Berechnen Sie den HMAC über die exakten Bytes „`timestamp + "." + raw_request_body`“, wobei das angezeigte Geheimnis als UTF-8-Bytes verwendet wird. Vergleichen Sie die Signaturen in konstanter Zeit, bevor Sie den Textkörper analysieren oder darauf reagieren. Verwerfen Sie Zeitstempel, die mehr als fünf Minuten von Ihrer Uhr abweichen. Der Zeitstempel wird bei jedem Zustellversuch aktualisiert.

Verwenden Sie „`event_id`“ als Idempotenzschlüssel in einem dauerhaften Speicher mit einer atomaren Eindeutigkeitsbeschränkung vor Nebenwirkungen. Eine gültige Signatur allein verhindert nicht, dass eine kürzlich erfolgte Anfrage erneut abgespielt wird. Bewahren Sie verarbeitete IDs mindestens für die gesamte Wiederholungsdauer auf; bewahren Sie sie länger auf, wenn der Empfänger gespeicherte Ereignisse erneut verarbeiten kann.

## Wiederholungsversuche

Übermittlungen werden dauerhaft vor HTTP-Anfragen in eine Warteschlange gestellt. Es wird die „At-Least-Once“-Semantik verwendet: Eine verlorene Bestätigung oder ein Neustart kann dazu führen, dass ein Ereignis erneut mit derselben ID übermittelt wird. Es gibt acht Versuche mit exponentiellem Backoff, beginnend bei 15 Sekunden und begrenzt auf eine Stunde. Für einen Erfolg ist eine 2xx-Antwort erforderlich. Abgebrochene Aufträge hinterlassen einen sichtbaren Fehler; eine Zustellung ist nach Ablauf der Wiederholungsversuche nicht mehr garantiert.

Die Warteschlange fasst 1.000 Zustellungen. Ist sie voll, wird das Scannen der Protokollereignisse unterbrochen und fortgesetzt, sobald wieder Speicherplatz verfügbar ist. Ein vollständiger Export, der nicht in die Warteschlange gestellt werden kann, löst einen sichtbaren Warteschlangenfehler aus. Pro Benachrichtigungsdurchlauf werden bis zu fünf Zustellversuche unternommen, und die letzten 100 Versuchsdatensätze werden gespeichert. Durch das Entfernen eines Ziels werden auch dessen ausstehende Zustellungen entfernt.

## n8n-Beispiel

Importieren Sie [den Beispiel-Workflow](https://github.com/phishdestroy/TgWitness/blob/main/integrations/n8n-tgwitness.json). Er ist inaktiv und enthält keine vertraulichen Daten oder nachgelagerte Aktionen. Legen Sie „`TGWITNESS_WEBHOOK_SECRET`“ in der n8n-Worker-Umgebung fest, gewähren Sie dieser Umgebung Zugriff und aktivieren Sie die integrierte Funktion „`crypto`“ für den Code-Knoten. Das Beispiel nutzt die Option „raw-body“ des Webhook-Knotens, überprüft Signatur und Aktualität und bestätigt validierte Ereignisse. Dies entspricht der [dokumentierten Implementierung](https://github.com/n8n-io/n8n/blob/master/packages/nodes-base/nodes/Webhook/Webhook.node.ts) des Knotens.

Bevor Sie SIEM-Einträge oder Benachrichtigungen hinzufügen, richten Sie einen dauerhaften, idempotenten Speicher ein, der mit `event_id` verschlüsselt ist. Beschränken Sie die Bearbeitung von n8n-Workflows und die Aufbewahrung von Ausführungsprotokollen entsprechend den Daten, die Sie zum Versand ausgewählt haben. TgWitness fügt keine eingehenden Befehle hinzu.
