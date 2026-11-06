# Befehlszeile

Canonical page: https://phishdestroy.github.io/TgWitness/de/docs/reference/cli/

Suchen, Kontext lesen, Aktivitäten zählen und gespeicherte Nachrichten aus Skripten und Agenten exportieren – mit --json-Ausgabe, stabilen Exit-Codes und bereichsgebundenen, schreibgeschützten Tokens.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Dokumentation](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md)

![Archive integrations](https://phishdestroy.github.io/TgWitness/assets/chapter-integrations.svg)

[Schreibgeschütztes MCP](https://phishdestroy.github.io/TgWitness/de/docs/reference/mcp/) · [Volltextsuche](https://phishdestroy.github.io/TgWitness/de/docs/reference/search/) · [Wiki](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

**Vorschau.** `tgwitness search`, `context`, `messages`, `stats` sowie `export` Lesen gespeicherter Beobachtungen für Skripte und KI-Agenten. Sie können nichts an Telegram senden, keine Einstellungen ändern und das signierte Protokoll nicht modifizieren.

Dabei `--json`gibt stdout genau ein JSON-Dokument aus (`export` schreibt JSON-Zeilen). Fortschrittsmeldungen, Hinweise und Fehler werden an stderr ausgegeben. Die Exit-Codes sind stabil:

| Code | Bedeutung |
| --- | --- |
| `0` | Erfolg, einschließlich eines leeren Ergebnisses |
| `1` | Fehler: nicht erreichbares Panel, unlesbare Daten, unterbrochener Export |
| `2` | Anwendungsfehler oder ungültige Anfrage: falsches Datum, unbekannte Option, Suchindex deaktiviert |
| `3` | Derzeit nicht verfügbar: Der Arbeitsbereich ist in einem aktiven Panel geöffnet, oder das Panel fordert dazu auf, es später erneut zu versuchen (Ratenbegrenzung, Zeitüberschreitung). |
| `4` | Zugriff verweigert: fehlendes, abgelaufenes oder widerrufenes Token, ein Chat außerhalb des Gültigkeitsbereichs, ein Tool, das dies nicht zulässt |

## Zwei Lesemöglichkeiten

**Über das Panel (`--url`).** Der Befehl nutzt dieselbe scoped archive API wie MCP. Erstellen Sie eine Verbindung unter **„Integrationen“ → „MCP**“: Wählen Sie Arbeitsbereiche und Chats, Tools und eine Gültigkeitsdauer aus und kopieren Sie anschließend einmalig das Token. Die Verbindung ist schreibgeschützt, beschränkt auf diese Chats, auf 60 Anfragen pro Minute begrenzt und kann jederzeit widerrufen oder erneuert werden. Panel-Anmeldetoken und Telegram-Anmeldedaten funktionieren hier nicht.

```
export TGWITNESS_URL=https://panel.example.org      # default http://127.0.0.1:8787
export TGWITNESS_MCP_TOKEN=tgw_mcp_...              # or --token-file path
tgwitness search 'перевод карта' --json
```

Ein Remote-Panel benötigt HTTPS; einfaches HTTP wird nur für `127.0.0.1`, `localhost` und `::1`. Proxy-Umgebungsvariablen werden ignoriert und Weiterleitungen abgelehnt, sodass das Token ausschließlich die von Ihnen angegebene Adresse erreicht.

**Direkt aus einem angehaltenen Arbeitsbereich (`--data-dir`).** Liest das Datenverzeichnis mit vollständigem lokalem Zugriff, ohne Token. Verwenden Sie es auf einer Kopie eines Datenverzeichnisses oder während die Erfassung angehalten ist. Signierte Datensätze werden niemals verändert; wie beim Panel kann das Öffnen eines Arbeitsbereichs dazu führen, dass die daraus abgeleiteten Indizes auf den aktuellen Stand gebracht werden. Wenn das Panel den Arbeitsbereich geöffnet hat, beendet sich der Befehl mit dem Code `3`; lesen Sie stattdessen über das Panel. Ohne `--data-dir`, `TGWITNESS_DATA`, `./data/live` oder das Datenverzeichnis der Installation, auf der der Befehl ausgeführt wird, wird verwendet.

`--workspace ID` wählt einen Arbeitsbereich aus (Standard `default`). `tgwitness messages
--workspaces` listet diejenigen auf, die Sie lesen dürfen.

## Befehle

| Befehl | Ergebnis |
| --- | --- |
| `tgwitness search QUERY [--chat ID] [--since] [--until] [--any] [--limit N] [--offset N]` | Die besten Treffer zuerst, mit Wortformen, exakten Phrasen in Anführungszeichen, Domains und `@username` ([Syntax](https://phishdestroy.github.io/TgWitness/de/docs/reference/search/#search-syntax)) |
| `tgwitness search QUERY --exact [--before SEQ]` | Genauer Wortlaut, neueste Einträge zuerst, ohne Index |
| `tgwitness context CHAT_ID MESSAGE_ID` | Gespeicherte Nachrichten innerhalb von zehn Nachrichten-IDs auf beiden Seiten |
| `tgwitness messages` | Chats, die Sie lesen können |
| `tgwitness messages CHAT_ID [--since] [--until] [--before SEQ]` | Gespeicherte Nachrichten des Chats, die neuesten zuerst |
| `tgwitness messages CHAT_ID --message ID` | Jede gespeicherte Version und jeder Löschdatensatz einer Nachricht |
| `tgwitness stats [--chat ID] [--sender ID] [--since] [--until] [--top N]` | Aktivitätsstatistiken, siehe unten |
| `tgwitness export [--chat ID] [--since] [--until] [--output FILE]` | Gespeicherte Beobachtungen als JSON-Zeilen in der Reihenfolge des Protokolls |

Datumsangaben erfolgen `2026-10-01` (UTC-Mitternacht) oder ISO-Zeiten mit Zeitzone `2026-10-01T09:00+03:00`. Für `search`, `messages` und `export` wählen sie den Beobachtungszeitpunkt. Seiten fassen bis zu 50 Datensätze: Befolgen Sie `next_offset` (`--offset`) für die rangierte Suche und `next_before` (`--before`) an anderer Stelle.

Ranked search stops at 1,000 results. The final page may be shorter than `--limit`; narrow the query, chat or period when more matching observations exist.

Jedes Nachrichtenergebnis enthält `untrusted_content: true`den Arbeitsbereich, den Chat und die Nachrichten-IDs, die Protokollsequenz, den Hash des gespeicherten Datensatzes und einen Panel-Link. Bearbeitungen, Löschhinweise und `missing_on_recheck` sind separate Datensätze. Das Fehlen eines Datensatzes bedeutet nicht, dass ein Ereignis nie stattgefunden hat.

### Aktivitätsstatistiken

`stats` Zählt die gespeicherten Beobachtungen für einen Chat, einen Absender oder alle Chats im Erfassungsbereich:

- Nachrichten nach UTC-Stunde und nach Wochentag (Montag an erster Stelle), verkehrsreichste Stunden und Tage;
- bearbeitet, gelöscht und `missing_on_recheck` Freigaben;
- Absender mit Nachrichtenanzahl sowie Zeitangaben für die erste und letzte Nachricht;
- die häufigsten Domains und `@handles`, einmal pro Nachricht über alle gespeicherten Versionen hinweg gezählt;
- Erfassungsbereich: `coverage.gap` Aufzeichnungen sowie – für den Zugriff auf den gesamten Arbeitsbereich – Zeiträume ohne Heartbeat eines verbundenen Collectors (`collector_liveness`).

Der Zeitraum bezieht sich auf **die von Telegram gemeldete Zeit der Nachricht**. Die Anzahl der Stunden und Wochentage kann dabei helfen, die Zeitzone des Absenders abzuschätzen; sie legt diese jedoch nicht fest. Die Zahlen werden auf Anfrage aus dem Protokoll berechnet und nicht gespeichert. Jedes Ergebnis nennt den Protokollanfang, den es abdeckt, wenn Ihr Zugriff den gesamten Arbeitsbereich umfasst. Das Einlesen endet nach fünf Sekunden über das Bedienfeld oder `--timeout` Sekunden lokal (Standardwert 30); danach `complete` ist „false“ und `partial` bezeichnet den ersten Datensatz, der nicht gelesen wurde. In diesem Fall werden nur die neuesten Datensätze gezählt.

### Exportieren

`export` Schreibt pro gespeicherter Beobachtung (neue Nachrichten, Snapshots, Bearbeitungen, wiederhergestellte Nachrichten, Löschbenachrichtigungen, `missing_on_recheck` und gespeicherte Mediendateien ) in der Reihenfolge des Protokolls. Jede Zeile enthält dieselben Felder wie die anderen Einträge, einschließlich des vollständigen Textes. Bei `--output`wird die Datei unter einem `.partial` Namen abgelegt und erst nach dem Abschlussprotokoll des Panels umbenannt; ein unterbrochener Export hinterlässt keine Datei und beendet den Vorgang mit dem Code `1`. `--output` überschreibt niemals eine vorhandene Datei. Mit `--output` und `--json`wird über stdout eine Zusammenfassung ausgegeben: Datensatzanzahl, letzte Journal- Sequenz und, bei Zugriff auf den gesamten Arbeitsbereich, der Journal-Anfang.

Ein Export über das Panel erfordert eine Verbindung, die **den Export von Nachrichten** zulässt **(nur über die Befehlszeile)**; diese Option ist standardmäßig nicht ausgewählt. Diese Datei ist eine Arbeitskopie und kein Beweismittel: Für eine überprüfbare Übergabe verwenden Sie den signierten Export unter **„Exporte“**, der `python -m tgwitness.verify`überprüft wird.

The panel rechecks access before emitting each record, including the completion record. Revoked or expired access leaves an incomplete export. Lazy page reads share the archive worker limit with other queries and have a bounded wait.

## Agent-Fähigkeit

[`.agents/skills/tgwitness-cli/SKILL.md`](https://github.com/phishdestroy/TgWitness/blob/main/.agents/skills/tgwitness-cli/SKILL.md) erklärt einem Agenten, wie diese Befehle zu verwenden sind, wie Datensätze zu zitieren sind und wie mit erfasstem Text umzugehen ist. Agenten, die `.agents/skills` laden diese aus einem Repository-Checkout . Für Claude Code kopieren Sie den `tgwitness-cli` Ordner in `.claude/skills/` in Ihr Projekt oder `~/.claude/skills/`.

## MCP und die Befehlszeile

Beide nutzen dieselben Verbindungen, Gültigkeitsprüfungen und Beschränkungen. MCP-Ergebnisse sind auf eine 64-KiB-Seite begrenzt, daher bietet MCP keinen Massenexport an; die Befehlszeile gibt die Daten per Stream aus. `get_activity_stats` ist für beide verfügbar.
