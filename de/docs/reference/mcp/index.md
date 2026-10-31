# Schreibgeschütztes MCP

Canonical page: https://phishdestroy.github.io/TgWitness/de/docs/reference/mcp/

Verbinden Sie einen MCP-Client mit ausgewählten Arbeitsbereichen und Chats mit zeitlich begrenztem, widerrufbarem Zugriff.

**Aktueller Hauptpunkt:** Verwenden Sie einen Source-Checkout; die portable Vorschauversion 0.7.0 stammt aus einer Zeit vor der Einführung dieser Funktion.

[Anleitung zum Arbeitsablauf](https://phishdestroy.github.io/TgWitness/docs/archive/) · [Wiki](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

Installieren Sie den optionalen Server aus dem TgWitness-Projektverzeichnis:

```
python -m pip install '.[mcp]'
```

Öffnen Sie im Panel **„Integrationen“ → „MCP**“. Benennen Sie die Verbindung, wählen Sie die Arbeitsbereiche und Chats aus und legen Sie eine Gültigkeitsdauer fest. Kopieren Sie das Archiv-Token einmalig; es kann später nicht mehr abgerufen werden. Widerrufen Sie verlorene Token und stellen Sie Ersatz-Token aus. Panel-Token und Telegram-Anmeldedaten sind keine MCP-Anmeldedaten.

## Client verbinden

Das Panel generiert „`.vscode/mcp.json`“ für das **VS Code Local-Harness** unter Verwendung der [dokumentierten Konfiguration](https://code.visualstudio.com/docs/agents/reference/mcp-configuration). Speichern Sie die heruntergeladene Datei an diesem Speicherort, führen Sie **„MCP: List Servers“** aus und starten Sie TgWitness. VS Code fordert Sie über eine Passworteingabe zur Eingabe des Tokens auf. Die heruntergeladene JSON-Datei enthält einen Hinweis zur Eingabeaufforderung, nicht das Token selbst. Verwenden Sie die ausführbare Python-Datei aus der Umgebung, in der das MCP-Extra installiert ist.

Für andere stdio-Clients führen Sie folgenden Befehl aus:

```
python -m tgwitness.mcp_server --api-url http://127.0.0.1:8787
```

Legen Sie „`TGWITNESS_ARCHIVE_TOKEN`“ in der geschützten Umgebung des Clients fest. Geben Sie es nicht in Befehlsargumenten oder URLs an. Die Bridge liest über die autorisierte Archiv-API des Panels; sie hat keinen direkten Datenbankzugriff. Stdout überträgt ausschließlich MCP-Nachrichten.

Für Remote-Clients führen Sie den Dienst neben dem Panel aus:

```
python -m tgwitness.mcp_server --transport streamable-http \
  --api-url http://127.0.0.1:8787 --port 8766 \
  --public-url https://archive.example.org/mcp
```

Leite `/mcp` über einen HTTPS-Reverse-Proxy an `127.0.0.1:8766/mcp` weiter, wobei der `Authorization: Bearer …`-Header beibehalten wird. Deaktiviere die Protokollierung von Autorisierungs-Headern sowie von Request- und Response-Inhalten. Führe eine Bindung über den Loopback hinaus nur bei Bedarf durch, unter Verwendung von `--host` und `--public-url`. Der Endpunkt nutzt „Streamable HTTP“ aus dem offiziellen [MCP-Python-SDK](https://github.com/modelcontextprotocol/python-sdk). Es unterstützt explizit konfigurierte Bearer-Anmeldedaten, jedoch keine OAuth-Erkennung; Clients, die ausschließlich OAuth benötigen, werden nicht unterstützt.

**Der Check-Vorgang und der Zugriff** initialisieren einen echten MCP-Client und listen die Tools auf. Dabei werden keine Nachrichten abgerufen. Bei einer Remote-Prüfung erhält der ausgewählte MCP-Server das Archiv-Token. Konfigurieren Sie in diesem Zusammenhang nur einen Server, den Sie selbst betreiben oder dem Sie vertrauen.

## Umfang und Ergebnisse

Verfügbare Tools: `list_workspaces`, `list_chats`, `search_messages`, `get_message_versions`, `get_message_context`, `get_journal_event` und `get_capture_status`. Es gibt keine Telegram-Aktionen, Konfigurationsänderungen oder Tools für den Massenexport. Bei jedem Lesevorgang wird der Zugriff auf den Arbeitsbereich/Chat erneut überprüft; abgelaufene und widerrufene Zugangsdaten funktionieren nicht mehr. Die Limits betragen 60 API-Anfragen pro Minute und Zugangsdaten, 50 Datensätze pro Seite, eine Antwortgröße von 64 KiB und eine API-Zeitüberschreitung von acht Sekunden.

Die Nachrichtenergebnisse umfassen den Arbeitsbereich, Chat-/Nachrichten-IDs, die Abfolge der Ereignisse, den gespeicherten Hash sowie einen Panel-Link. Der Betrachter, der einen Link öffnet, muss über eine eigene autorisierte Panel- Sitzung verfügen. Rohe Telegram-Objekte, Zugriffs-Hashes, Dateiverweise, Sitzungsmaterial und Schlüssel werden weggelassen. Die Suche untersucht den Nachrichtentext, nicht die Rohfelder. Der Text wird begrenzt und Kürzungen werden gekennzeichnet. Bearbeitungen, Telegram-Löschhinweise und „ `missing_on_recheck`“ bleiben separate Beobachtungen. Bei einem auf den Chat beschränkten Zugriff sind arbeitsbereichsweite operative Ereignisse nicht einsehbar; der Erfassungsstatus kennzeichnet diese Einschränkung ausdrücklich.

Archivtext gilt als nicht vertrauenswürdige Eingabe. Anweisungen innerhalb von Nachrichten gewähren keinen zusätzlichen Spielraum und dürfen nicht als Anweisungen des Clients behandelt werden. Ein externes KI-Modell kann jeden Inhalt erhalten, den sein MCP-Client anfordert. Der schreibgeschützte Zugriff verhindert Änderungen am Archiv; er hindert einen Client jedoch nicht daran, die gelesenen Daten zu speichern.

Die Hashes identifizieren gespeicherte Datensätze und unterstützen Integritätsprüfungen. Sie beweisen jedoch nicht unabhängig die Urheberschaft durch Telegram oder, dass jede Nachricht erfasst wurde.
