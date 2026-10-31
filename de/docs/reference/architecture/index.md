# Architektur

Canonical page: https://phishdestroy.github.io/TgWitness/de/docs/reference/architecture/

Bestandteile des Collectors, des Panels, des Journals, der Worker und des Witness sowie der Datenfluss zwischen diesen Komponenten.

Ein Python-Prozess hostet das FastAPI-Panel und eine beliebige Anzahl isolierter Arbeitsbereiche, jeweils mit einem Telethon-Benutzerkonto-Client. SQLite verwaltet ein signiertes Ereignisprotokoll, das nur angehängt werden kann, sowie veränderbare Betriebseinstellungen. Ein verschlüsselter Tresor enthält die API-Anmeldedaten, die „StringSession“ und den Signaturschlüssel. Das Frontend besteht aus einem einfachen HTML/CSS/JavaScript-Paket: Es sind weder ein Node-Build noch CDNs oder Frontend-Downloads zur Laufzeit erforderlich.

| Modul | Verantwortung |
| --- | --- |
| collector.py | Autorisierung, Dialogauswahl, Aktualisierungen, Momentaufnahmen, Medienwarteschlange, Verbindungsüberwachung |
| interactions.py / telegram_client.py | Eindeutig definierte Panel-Aktionen, signierte Empfangsbestätigungen, persistente Anfrage-IDs und eine aufgabenbezogene Richtlinie für Rückrufe und erneute Teilnahmesuche |
| message_content.py | Vergleich der beobachtbaren Nachrichten unter Ausschluss von Metadaten zum Transportzugriff |
| workers.py | Warten Sie auf die Mitarbeiter, die die Exportdateien bearbeiten, bevor Sie die Bereinigung nach der Stornierung durchführen |
| store.py | WAL-Transaktionen, geordnete Ereigniskette, Abfragefilter, Betriebseinstellungen |
| security.py | Erstellung privater Dateien, verschlüsselter Tresor, Ed25519-Signatur, Einzelprozess-Sperre |
| evidence.py | Export des vollständigen Protokolls, Derivate, Kontrollpunkte, Überprüfung von Anhängen |
| verify.py | Eigenständiges, schreibgeschütztes Verifizierungsprogramm (stdlib + Kryptografie): Archive, Erfassungsbereich, Witness-Protokolle und Kanalbeiträge, Profildateien |
| app.py | Authentifizierte API, Lebenszyklus, Validierung von Anfragen, statisches Panel |
| profiles.py | Erfassung über mehrere Konten, gemeinsame Zugriffskontrolle, Lebenszyklus pro Arbeitsbereich |
| access.py | Umfangbegrenzte Lizenzen, Berechtigungsprüfungen, IP-Einschränkungen, Sitzungslimits und Administratorkonsole |
| proxy_catalog.py | Momentaufnahmen öffentlicher Feeds, Transportprüfungen, gemeinsamer Proxy-Pool und zustandsbasierte Auswahl |
| provenance.py | Signierte Identitäts-, Code- und Abhängigkeitsmessungen während des Erfassungsvorgangs |
| network.py | Validierte Routen pro Arbeitsbereich; redigierter Status und Beweismaterial; Telethon-Übertragungsoptionen |
| sessions.py | Offline-Konvertierung der geprüften Telethon-SQLite-Schemas in einen schreibgeschützten Modus |
| account_import.py | In-Memory-Erkennung und Normalisierung von unterstützten Kontodateien und JSON-Dateien |
| tdata.py | Begrenzter, moderner TData-ZIP-Reader, Überprüfung von Prüfsummen und Entschlüsselung, keine Extraktion |
| doctor.py | Lokale Bereitschaftsprüfungen ohne Datenerfassung, Anmeldung oder Paketinstallation |
| download.py | Authentifizierter Streaming-Export zum Herunterladen mit begrenzten Lesezugriffen und ohne Überschreibungen |
| monitoring.py | Validierte Ereignisrichtlinien pro Arbeitsbereich und Regeln für Anhänge nach Typ, gemeinsam genutzt von Bearbeitern, Statusangaben und signierten Empfangsbestätigungen |
| scope.py | Überwachungsumfang (ausgewählte Chats, Telegram-Ordner, gesamtes Konto), Quelltypen, Ausschlüsse, Stufen der Nachprüfung |
| dossier.py | Aus gespeicherten Datensätzen erstellte Personenprofile pro Chat: Fakten mit Verweisen auf die Datensätze, SHA-256/pHash des Avatars, Extraktion von Erwähnungen |
| witness_api.py | Schreibgeschützte Witness-Token und der signierte Protokollkopf, den diese abrufen können |
| witness.py | Unabhängiger Zeugenprozess: eigener Schlüssel und eigenes Protokoll, Kopfprüfungen, signierte Kanalbeiträge, Export |
| alerts.py | Apprise-Benachrichtigungen und die Benachrichtigungsliste des Panels |
| logging_config.py | Konsolenprotokollierung und rotierende Serverdiagnose für fensterlose Starts |
| static/ | Responsive Benutzeroberfläche, lokaler Zugriff, Filter, Details, Exporte, Kontoeinrichtung |
| demo.py | Deutlich als synthetisches Protokoll gekennzeichnet, getrennt von der tatsächlichen Datenerfassung |

Beobachtungshandler werden vor der Verbindung registriert. Die Live-Erfassung wird durch die aktive Client-Identität, den expliziten Ausführungsstatus, aktivierte Quellen oder den Beobachtungsumfang (im Ordner- oder Gesamtkonto-Modus wird ein neuer Chat bei seiner ersten Aktualisierung als Quelle hinzugefügt) sowie die Ereignisrichtlinie gesteuert. Abgelehnte und ersetzte Clients können keine Live-Aktualisierungen beitragen. Unverarbeitete Reaktionen und Aktualisierungen der Mitgliedschaft wahren die Sichtbarkeitsgrenzen ein. Der Inhalt eingehender Nachrichten und der zugehörige dauerhafte Medienauftrag werden gemeinsam festgeschrieben. Aufträge bewahren den ursprünglichen TL-Deskriptor und verknüpfen dessen Hash mit der signierten Nachrichtenbeobachtung. Die Semantik von Absender, Bearbeiter und Löschendem wird getrennt behandelt.

Jeder Arbeitsbereich akzeptiert ein Konto und verfügt über ein eigenes Verzeichnis sowie eine eigene Signaturidentität. Der Hauptarbeitsbereich verbleibt aus Kompatibilitätsgründen im Stammverzeichnis; zusätzliche Arbeitsbereiche befinden sich unter profiles/<id>/. Ein Bearer-Token steuert die gesamte Installation; Arbeitsbereiche sind keine separaten Autorisierungsmandanten. Prozesssperren schützen die Verzeichnisse; Datenbanksperren serialisieren das Einfügen von Ereignissen. Jeder Nachtrag wird synchron in das SQLite-WAL im vollsynchronen Modus geschrieben. Trigger für die Aktualisierung/Löschung von Ereignissen verhindern gewöhnliche Bearbeitungen durch Anwendungen; Dateisystemadministratoren bleiben innerhalb der Vertrauensgrenze.

Die API-Autorisierung erfolgt über ein Bearer-Token. Anmeldevorgänge werden serialisiert und sind zeitlich begrenzt. Für Konto-Uploads gelten ein dediziertes Limit von 12 MiB für den codierten Body und ein Limit von 8 MiB für die decodierte Datei; bei normalen API-Anfragen gilt weiterhin das Limit von 16 KiB. Die Konvertierung läuft in einem Worker-Thread, speichert Uploads im Arbeitsspeicher und gibt normalisierte Eingaben an den authentifizierten Browser zurück. Die QR-Anmeldung verfügt über einen workspace-spezifischen Kandidaten, einen kurzlebigen Identifikator, eine Warteschlange sowie eine explizite Abbruchmöglichkeit. Nur die akzeptierte Autorisierung wird zum aktiven Client. Telegram FloodWait wird mit einem „Retry-After“-Wert zurückgegeben; Anmeldedaten und rohe RPC- Fehlermeldungen werden in API-Fehlern nicht offengelegt. Exporte laufen außerhalb der asynchronen Ereignisschleife und werden pro Arbeitsbereich serialisiert. Sie streamen einen stabilen Lese-Snapshot und können neben fortlaufenden WAL-Schreibvorgängen existieren. Arbeitsbereichssammler teilen sich den Prozess bzw. die Ereignisschleife.

Aktuelle Verlaufs-Snapshots und Live-Updates können sich überschneiden. Bei beiden handelt es sich um separate Beobachtungen, die nach Quelle gekennzeichnet sind; Duplikate werden nicht stillschweigend zusammengefasst. Es werden keine Rückschlüsse aus fehlenden IDs, erfundenem gelöschtem Text, erzwungener Mitgliederaufzählung oder automatischem Beitritt zu Gruppen gezogen.

Erläuterungen für Betreiber finden Sie unter [„So funktioniert die Erfassung](https://phishdestroy.github.io/TgWitness/de/docs/reference/collection/)“ sowie unter [„Konten“ und „Sitzungsformate](https://phishdestroy.github.io/TgWitness/de/docs/reference/accounts/)“.

Die Netzwerkkonfiguration befindet sich im verschlüsselten Tresor. Das Anwenden einer Route schließt alte Clients und bricht unvollendete Anmeldungen ab; spätere Verbindungen nutzen diese Route ohne direkten Fallback. Bei einer neuen Installation mit externem Schlüssel wird der Fernet-Schlüssel jedes Arbeitsbereichs mit HKDF-SHA256 aus einer Hauptschlüsseldatei und einem gespeicherten Zufalls-Salt abgeleitet. Dadurch werden Geheimnisse getrennt vom Datenverzeichnis geschützt, nicht jedoch die Protokoll- oder Medieninhalte im Klartext.

Der lokale Demo-Zugriff nutzt eine separat generierte Prozesskapazität, niemals das konfigurierte Panel-Token. Die Ausstellung und Akzeptanz erfordern den expliziten Demo-Modus, eine synthetische Root ohne zusätzliche Arbeitsbereiche oder eine autorisierte Sitzung, einen Loopback-Peer/Host, keine Proxy- Weiterleitungs-Header sowie keine Cross-Origin-Browser-Anfragen. Live-APIs behalten die Bearer-Authentifizierung bei und lehnen Änderungen an der Datenerfassung im Demo-Modus ab.
