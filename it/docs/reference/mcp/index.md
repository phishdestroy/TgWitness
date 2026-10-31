# MCP di sola lettura

Canonical page: https://phishdestroy.github.io/TgWitness/it/docs/reference/mcp/

Collega un client MCP agli spazi di lavoro e alle chat selezionati con un accesso a scadenza e revocabile.

**Versione principale attuale:** utilizzare un checkout dal codice sorgente; l’anteprima portatile 0.7.0 è precedente a questa funzionalità.

[Guida al flusso di lavoro](https://phishdestroy.github.io/TgWitness/docs/archive/) · [Wiki](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

Installare il server opzionale dalla directory del progetto TgWitness:

```
python -m pip install '.[mcp]'
```

Nel pannello, aprire **Integrazioni → MCP**. Assegnare un nome alla connessione, selezionare i relativi spazi di lavoro e chat e scegliere una scadenza. Copiare il token di archiviazione una sola volta; non potrà essere recuperato in seguito. Revocare i token smarriti ed emetterne di sostitutivi. I token del pannello e le credenziali di Telegram non sono credenziali MCP.

## Collegare un client

Il pannello genera `.vscode/mcp.json` per l’**harness locale di VS Code** utilizzando [la sua configurazione documentata](https://code.visualstudio.com/docs/agents/reference/mcp-configuration). Salvare il file scaricato in quella posizione, eseguire **MCP: List Servers** e avviare TgWitness. VS Code richiede il token tramite l’inserimento di una password. Il file JSON scaricato contiene un riferimento alla richiesta, non il token. Utilizzare l’eseguibile Python dall’ ambiente in cui è installato l’extra MCP.

Per altri clienti di stdio, eseguire:

```
python -m tgwitness.mcp_server --api-url http://127.0.0.1:8787
```

Impostare `TGWITNESS_ARCHIVE_TOKEN` nell’ambiente protetto del cliente. Non inserirlo negli argomenti dei comandi o negli URL. Il bridge legge tramite l’API di archiviazione autorizzata del pannello; non ha accesso diretto al database. Lo stdout trasporta solo messaggi MCP.

Per i client remoti, eseguire il servizio accanto al pannello:

```
python -m tgwitness.mcp_server --transport streamable-http \
  --api-url http://127.0.0.1:8787 --port 8766 \
  --public-url https://archive.example.org/mcp
```

Inoltra `/mcp` tramite un proxy inverso HTTPS a `127.0.0.1:8766/mcp`, conservando l’intestazione `Authorization: Bearer …`. Disattiva la registrazione delle intestazioni di autorizzazione e dei corpi delle richieste/risposte. Effettua il binding oltre il loopback solo quando necessario, utilizzando `--host` e `--public-url`. L’endpoint utilizza Streamable HTTP dall’SDK [Python ufficiale di MCP](https://github.com/modelcontextprotocol/python-sdk). Supporta credenziali bearer configurate esplicitamente, non il discovery OAuth; i client che richiedono esclusivamente OAuth non sono supportati.

**Il controllo del protocollo e l’accesso** avviano un vero client MCP ed elencano gli strumenti. Non recupera i messaggi. Per un controllo remoto, il server MCP scelto riceve il token di archivio. Configurare solo un server gestito dall’utente stesso o di cui ci si fida per tale scopo.

## Ambito e risultati

Strumenti disponibili: `list_workspaces`, `list_chats`, `search_messages`, `get_message_versions`, `get_message_context`, `get_journal_event` e `get_capture_status`. Non sono disponibili azioni su Telegram, modifiche alla configurazione né strumenti di esportazione in blocco. Ad ogni lettura viene ricontrollato l’accesso all’area di lavoro/alla chat; le credenziali scadute e revocate smettono di funzionare. I limiti sono 60 richieste API al minuto per credenziale, 50 record per pagina, una risposta di 64 KiB e un tempo massimo di risposta API di otto secondi.

I risultati dei messaggi includono l’area di lavoro, gli ID delle chat/dei messaggi, la sequenza degli eventi, l’hash salvato e un link al pannello. L’utente che apre un link deve disporre di una propria sessione autorizzata nel pannello. Gli oggetti Telegram grezzi, gli hash di accesso, i riferimenti ai file, il materiale della sessione e le chiavi sono omessi. La ricerca esamina il testo dei messaggi, non i campi grezzi. Il testo è delimitato e il troncamento è contrassegnato. Modifiche, notifiche di cancellazione di Telegram e `missing_on_recheck` rimangono osservazioni separate. L’accesso limitato alla chat non può visualizzare gli eventi operativi a livello dell’area di lavoro; lo stato di acquisizione indica esplicitamente questo limite.

Il testo dell’archivio è un input non attendibile. Le istruzioni contenute nei messaggi non conferiscono alcuna competenza aggiuntiva e non devono essere trattate come istruzioni del cliente. Un modello di IA esterno può ricevere qualsiasi contenuto richiesto dal proprio client MCP. L’accesso in sola lettura impedisce modifiche all’archivio; non impedisce tuttavia a un client di conservare i dati che legge.

Gli hash identificano i record salvati e supportano i controlli di integrità. Non dimostrano in modo autonomo la paternità del messaggio su Telegram né che ogni messaggio sia stato acquisito.
