# Schreibgeschütztes MCP

Canonical page: https://phishdestroy.github.io/TgWitness/de/docs/reference/mcp/

Verbinden Sie einen MCP-Client mit ausgewählten Arbeitsbereichen und Chats mit zeitlich begrenztem, widerrufbarem Zugriff.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Dokumentation](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Archiv-Integrationen](https://phishdestroy.github.io/TgWitness/de/docs/reference/cli/)

![Archiv-Integrationen](https://phishdestroy.github.io/TgWitness/assets/chapter-integrations.svg)

Verbinden Sie einen Analysten-Client mit ausgewählten Arbeitsbereichen und Chats. TgWitness stellt **im Panel-Prozess unter `/mcp` einen Streamable-HTTP-Dienst** bereit. Jede Verbindung verfügt über ein eigenes Token, eine eigene Ablaufzeit und zulässige Tools. MCP kann keine Telegram-Nachrichten versenden, keine Einstellungen ändern und das signierte Protokoll nicht modifizieren. Die gleichen Verbindungen funktionieren auch über die [Befehlszeile](https://phishdestroy.github.io/TgWitness/de/docs/reference/cli/).

[Anleitung zum Arbeitsablauf](https://phishdestroy.github.io/TgWitness/docs/archive/) · [Wiki](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

**Auf dieser Seite**

- [Installieren und überprüfen](https://phishdestroy.github.io/TgWitness/de/docs/reference/mcp/#install-and-check)
- [Verbindung herstellen](https://phishdestroy.github.io/TgWitness/de/docs/reference/mcp/#issue-a-connection)
- [Verbinden Sie Ihren Client](https://phishdestroy.github.io/TgWitness/de/docs/reference/mcp/#connect-your-client)
- [Cloudflare-Tunnel](https://phishdestroy.github.io/TgWitness/de/docs/reference/mcp/#cloudflare-tunnel)
- [Werkzeuge und Grenzen](https://phishdestroy.github.io/TgWitness/de/docs/reference/mcp/#tools-and-boundaries)

## Installation und Prüfung

Verwenden Sie die Python-Umgebung, in der das Panel ausgeführt wird. Aus einem Quellcode-Checkout:

```
# Windows PowerShell
& .\.venv\Scripts\python.exe -m pip install -c deploy/constraints-mcp.txt -e '.[mcp]'
& .\.venv\Scripts\python.exe start.py --check
```

```
# Linux / macOS
.venv/bin/python -m pip install -c deploy/constraints-mcp.txt -e '.[mcp]'
.venv/bin/python start.py --check
```

Starten Sie das Panel nach der Installation mit dem üblichen Datenverzeichnis und den gewohnten Startargumenten neu. Die Bereitschaftsprüfung sollte `[PASS] mcp: streamable-http available` enthalten. **Integrations → MCP** zeigt den Laufzeitstatus sowie einen Installationsbefehl an, der die tatsächliche Python-Programmdatei des Servers verwendet. **Re-check** aktualisiert diesen Status ohne erneutes Laden der Seite; es werden dabei keine Pakete installiert und der Server wird nicht neu gestartet.

Das MCP-Extra nutzt das offizielle [MCP-Python-SDK](https://github.com/modelcontextprotocol/python-sdk).`deploy/constraints-mcp.txt` legt das getestete SDK und die Abhängigkeiten fest.

## Verbindung erstellen

1. Geben Sie eine Bezeichnung ein und wählen Sie die Workspaces und Chats aus, die der Client lesen darf.
2. Wählen Sie Tools einzeln aus oder nutzen Sie eine Voreinstellung. Es werden nur implementierte Tools angeboten.
3. Wählen Sie 1, 7, 30 oder 90 Tage oder eine benutzerdefinierte Gültigkeitsdauer zwischen einer Minute und 90 Tagen.
4. Klicken Sie auf **Create connection**. Das Token wird einmalig neben der Client-Konfiguration angezeigt.
5. Kopieren Sie das Token und die Konfiguration und führen Sie anschließend **Check connection** aus. Dadurch wird MCP initialisiert und die freigegebenen Tools werden aufgelistet; **es werden keine Nachrichten gelesen**. Das Ergebnis zeigt die Protokollversion, die Tool-Namen, deren Anzahl und die verstrichene Zeit.
6. Klicken Sie auf **Done**, sobald die Zugangsdaten gespeichert sind. Das Polling behält das Formular und die einmalig angezeigte Karte bei. Das Sperren des Panels löscht angezeigte Geheimnisse.

Die Liste zeigt die letzte Nutzung, das zuletzt verwendete Tool, die Adresse und die Anfragen der letzten Minute. **Revoke** beendet den Zugriff. **Rotate token** widerruft die alten Zugangsdaten und stellt einen Ersatz mit demselben Geltungsbereich, denselben Tools und derselben Gültigkeitsdauer aus; kopieren Sie das Ersatz-Token sofort, da es nur einmalig angezeigt wird. Panel-Login-Tokens und Telegram-Zugangsdaten funktionieren nicht als MCP-Tokens.

## Client verbinden

Wählen Sie den Client im Panel aus und kopieren Sie die generierte Konfiguration. Konfigurationen verwenden Secret-Referenzen oder explizite Platzhalter; das Token wird separat kopiert.

| Client | Konfiguration | Zusammenhang |
| --- | --- | --- |
| Claude-Code | `.mcp.json` | HTTP, `type: "http"`, Bearer-Header |
| Claude Desktop | `claude_desktop_config.json` | Lokale stdio-Bridge |
| Cursor | `.cursor/mcp.json` | HTTP mit Umgebungsvariablen-Header |
| VS Code Local | `.vscode/mcp.json` | HTTP mit Passwort-Eingabe über `promptString` |
| Windsurf | `mcp_config.json` | HTTP mit Platzhalter für Bearer-Header |
| Andere Clients | URL und Authorization-Header | Streamable HTTP |

TgWitness verwendet Bearer-Tokens ohne OAuth-Discovery. Verwenden Sie die lokale stdio-Bridge für Clients, deren Remote-Connector OAuth voraussetzt. Bei VS Code gelten Eingabevariablen für die **Local**-Umgebung und werden nicht an Copilot-Sitzungen weitergeleitet. Konfigurationsreferenzen: [Claude Code](https://code.claude.com/docs/en/mcp), [Cursor](https://prod.cursor.com/docs/mcp), [VS Code](https://code.visualstudio.com/docs/agents/reference/mcp-configuration).

Der kanonische Einstiegspunkt für eine lokale Bridge lautet:

```
python -m tgwitness.mcp_server --url https://your-panel.example/mcp
```

Verwenden Sie die lokale Python-Installation des Clients, in der das MCP-Extra installiert ist. Setzen Sie `TGWITNESS_MCP_TOKEN` in dessen geschützter Umgebung. Halten Sie Zugangsdaten aus Befehlsargumenten und URLs heraus. `tgwitness-mcp` ist derselbe Einstiegspunkt. Das alte Modul `tgwitness.mcp_bridge` und der Name `TGWITNESS_ARCHIVE_TOKEN` bleiben als Kompatibilitätspfade mit einer Warnung erhalten; neue Konfigurationen verwenden `mcp_server` und `TGWITNESS_MCP_TOKEN`.

## Cloudflare Tunnel

Leiten Sie die Route `/mcp` des Panels weiter und behalten Sie den Bearer-Header bei. Das Öffnen der MCP-Einstellungen als Administrator registriert die aktuelle Origin des Panels für diesen Durchlauf. Für eine stabile Adresse, die sofort nach einem Neustart verfügbar ist, konfigurieren Sie `TGWITNESS_PUBLIC_URL` vor dem Starten des Panels mit der HTTPS-Origin des Panels. Beliebige Host- und Weiterleitungs-Header registrieren keine vertrauenswürdige Adresse. Host- und Origin-Prüfungen weisen fremde Browser-Origins ab. Antworten verwenden `Cache-Control: no-store`; Autorisierungswerte werden niemals protokolliert.

Eine `*.trycloudflare.com`-Adresse ist temporär. Wenn ein Tunnel-Neustart den Hostnamen ändert, aktualisieren Sie die konfigurierte öffentliche URL sowie die MCP-URL jedes Clients. Verwenden Sie einen stabilen Hostnamen für gespeicherte Client-Konfigurationen.

## Tools und Systemgrenzen

| Tool | Liest |
| --- | --- |
| `list_workspaces` | Freigegebene Workspaces |
| `list_chats` | Freigegebene Chats |
| `search_messages` | Gespeicherter Nachrichtentext innerhalb des ausgewählten Zeitraums; `ranked=true` nutzt [Volltextsuche](https://phishdestroy.github.io/TgWitness/de/docs/reference/search/) (Wortformen, beste Treffer zuerst, `next_offset` Seitenumschaltung) |
| `get_message_versions` | Erfasste Versionen und Löschbeobachtungen |
| `get_message_context` | Benachbarte erfasste Nachrichten-IDs |
| `get_journal_event` | Einen bereinigten Datensatz mit seiner Quellreferenz |
| `get_capture_status` | Erfassungsstatus, zulässige Erfassungsdatensätze und `gap_summary`: Nie beobachtete Nachrichtennummern, pro Kanal oder Supergruppe sowie für die kontoweite Sequenz ([Details](https://phishdestroy.github.io/TgWitness/de/docs/reference/evidence/#missing-message-numbers-gap_summary)); wählen Sie einen Chat aus, um dessen aufgelistete Lücken anzuzeigen |
| `get_activity_stats` | Nachrichten nach UTC-Stunde und Wochentag, Tage mit Spitzenauslastung, Anteile an Bearbeitungen und Löschungen, Absender, Domains und `@handles`, mit Erfassungsbereich ([Details](https://phishdestroy.github.io/TgWitness/de/docs/reference/cli/#activity-statistics)) |
| `get_messages_by_date` | Gespeicherte Nachrichten eines Kalendertags in einer benannten IANA-Zeitzone (`Europe/Kyiv`, `UTC`), gemäß der von Telegram gemeldeten Uhrzeit; `from_utc` und `until_utc` den berechneten Tag angeben, einschließlich Sommerzeit |
| `get_pinned_messages` | Im aktuellen Chat-Status-Snapshot angeheftete Nachrichten mit ihren gespeicherten Versionen sowie die live beobachteten Benachrichtigungen zum Anheften und Lösen der Anheftung |
| `get_chat_stats` | Einfache Zählung der gespeicherten Datensätze für einen Chat oder alle Chats im Erfassungsbereich, erste und letzte Beobachtung sowie `gap_summary`; nutzen Sie es vor einem umfangreichen Lesevorgang |
| `get_topics` | Forenthemen aus den Nachrichten des Dienstes „Themen speichern“: Titelverlauf, geschlossene oder ausgeblendete Themen, Anzahl der gespeicherten Nachrichten |
| `get_media` | Ein gespeichertes Bild als verkleinerte JPEG-Vorschau (maximal 36 KB), das als Bild zusammen mit seinem SHA-256-Hash und dem `media.saved` Datensatz zurückgegeben; die Datei wird zunächst anhand ihres aufgezeichneten Hash-Werts überprüft, andere Dateien geben nur Metadaten zurück |
| `export_messages` | Nur über die Befehlszeile, standardmäßig nicht ausgewählt: „streams“ speichert Beobachtungen als JSON Lines ([Details](https://phishdestroy.github.io/TgWitness/de/docs/reference/cli/#export)); wird über MCP nicht angeboten |

Jedes Tool ist schreibgeschützt (`readOnlyHint`) und definiert ein Ausgabeschema; Felder, die über die deklarierten hinausgehen, werden unverändert zurückgegeben. `tools/list` Es werden nur die Tools zurückgegeben, die für diese Verbindung freigegeben sind. Aufrufe anderer Tools werden abgelehnt. Tools für Gruppenkontext, Episoden, Terminologie und Antwortketten werden in dieser Version nicht angeboten; das separate Context-Pack-Backend ist nicht enthalten.

Jeder Lesevorgang prüft das Token, das Tool sowie den Workspace-/Chat-Geltungsbereich – auch nach Abschluss der Datenbankabfrage. Die Limits betragen 60 Anfragen pro Minute, 50 Datensätze pro Seite, 64 KiB pro Ergebnis und ein Zeitlimit von acht Sekunden für Archivabfragen. Ein abgelaufener MCP-Aufruf gibt einen Tool-Fehler zurück, der einen engeren Zeitraum oder ein niedrigeres Limit anfordert.

Nachrichtenergebnisse enthalten `untrusted_content: true`, Workspace-/Chat-/Nachrichten-IDs, die Ereignissequenz, den gespeicherten Hash und einen Panel-Link. Rohe Telegram-Objekte, Access-Hashes, Sitzungen und Schlüssel werden weggelassen. Textkürzungen werden markiert. Bearbeitungen, Löschhinweise und `missing_on_recheck` sind eigenständige Beobachtungen. Fehlende Datensätze beweisen nicht, dass ein Ereignis nie stattgefunden hat.

Behandeln Sie Anweisungen innerhalb erfasster Nachrichten stets als Beweismaterial und niemals als Anweisungen für den Client. Der schreibgeschützte Zugriff verhindert Änderungen am Archiv; der Client kann die Inhalte, zu deren Lesezugriff er berechtigt ist, dennoch speichern. Hashes identifizieren gespeicherte Datensätze und unterstützen Integritätsprüfungen; sie beweisen weder die Telegram-Urheberschaft noch eine vollständige Erfassung.
