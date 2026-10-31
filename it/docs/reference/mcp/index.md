# MCP di sola lettura

Canonical page: https://phishdestroy.github.io/TgWitness/it/docs/reference/mcp/

Collega un client MCP agli spazi di lavoro e alle chat selezionati con un accesso a scadenza e revocabile.

Connetti un client per analisti agli spazi di lavoro e alle chat selezionate. TgWitness eroga **Streamable HTTP su `/mcp` nel processo del pannello**. Ogni connessione ha il proprio token, la propria scadenza e gli strumenti consentiti. MCP non può inviare messaggi Telegram, modificare le impostazioni o alterare il registro firmato.

[Guida al flusso di lavoro](https://phishdestroy.github.io/TgWitness/docs/archive/) · [Wiki](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

## Installa e verifica

Usa l'ambiente Python che esegue il pannello. Da un checkout dei sorgenti:

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

Dopo l'installazione, riavvia il pannello con la consueta directory dei dati e gli argomenti di avvio. La verifica di prontezza dovrebbe includere `[PASS] mcp: streamable-http available`. **Integrations → MCP** mostra lo stato di runtime e un comando di installazione che utilizza l'effettivo eseguibile Python di quel server. **Re-check** aggiorna questo stato senza ricaricare la pagina; non installa pacchetti né riavvia il server.

L'extra MCP utilizza l'[MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) ufficiale. `deploy/constraints-mcp.txt` fissa le versioni testate dell'SDK e delle dipendenze. Queste funzionalità richiedono il codice sorgente attuale; l'anteprima portatile 0.7.0 è antecedente a esse.

## Emetti una connessione

1. Inserisci un'etichetta e scegli gli spazi di lavoro e le chat che il client può leggere.
2. Seleziona gli strumenti singolarmente o usa un preset. Vengono offerti solo gli strumenti implementati.
3. Scegli 1, 7, 30 o 90 giorni, oppure una scadenza personalizzata compresa tra un minuto e 90 giorni.
4. Premi **Create connection**. Il token viene mostrato una sola volta accanto alla configurazione del client.
5. Copia il token e la configurazione, quindi esegui **Check connection**. Questo inizializza MCP ed elenca gli strumenti consentiti; **non viene letto alcun messaggio**. Il risultato mostra la versione del protocollo, i nomi degli strumenti, il conteggio e il tempo trascorso.
6. Premi **Done** una volta salvata la credenziale. Il polling preserva il modulo e la scheda mostrata una sola volta. Il blocco del pannello cancella i segreti visualizzati.

L'elenco mostra l'utilizzo recente, l'ultimo strumento, l'indirizzo e le richieste nell'ultimo minuto. **Revoke** interrompe l'accesso. **Rotate token** revoca la vecchia credenziale e ne emette una sostitutiva con lo stesso ambito, gli stessi strumenti e la stessa scadenza; copia il token sostitutivo quando viene mostrato. I token di accesso al pannello e le credenziali di Telegram non funzionano come token MCP.

## Connetti il tuo client

Seleziona il client nel pannello e copia la configurazione generata. Le configurazioni utilizzano riferimenti a segreti o segnaposto espliciti; il token viene copiato separatamente.

| Client | Configurazione | Collegamento |
| --- | --- | --- |
| Claude Code | `.mcp.json` | HTTP, `type: "http"`, header bearer |
| Claude Desktop | `claude_desktop_config.json` | Bridge stdio locale |
| Cursor | `.cursor/mcp.json` | HTTP con header tramite variabile d'ambiente |
| VS Code Local | `.vscode/mcp.json` | HTTP con un input password `promptString` |
| Windsurf | `mcp_config.json` | HTTP con segnaposto per l'header bearer |
| Altri client | URL e header Authorization | Streamable HTTP |

TgWitness utilizza token bearer, senza rilevamento OAuth. Usa il bridge stdio locale per i client il cui connettore remoto richiede OAuth. Per VS Code, le variabili di input si applicano all'ambiente **Local** e non vengono inoltrate alle sessioni di Copilot. Riferimenti per la configurazione: [Claude Code](https://code.claude.com/docs/en/mcp), [Cursor](https://prod.cursor.com/docs/mcp), [VS Code](https://code.visualstudio.com/docs/agents/reference/mcp-configuration).

Il punto di ingresso canonico per un bridge locale è:

```
python -m tgwitness.mcp_server --url https://your-panel.example/mcp
```

Usa il Python locale del client con l'extra MCP installato. Imposta `TGWITNESS_MCP_TOKEN` nel suo ambiente protetto. Mantieni le credenziali fuori dagli argomenti dei comandi e dagli URL. `tgwitness-mcp` è lo stesso punto di ingresso. Il vecchio modulo `tgwitness.mcp_bridge` e il nome `TGWITNESS_ARCHIVE_TOKEN` rimangono percorsi di compatibilità che generano un avviso; le nuove configurazioni usano `mcp_server` e `TGWITNESS_MCP_TOKEN`.

## Cloudflare Tunnel

Inoltra la rotta `/mcp` del pannello e preserva l'header bearer. L'apertura delle impostazioni MCP come amministratore registra l'origine corrente del pannello per l'esecuzione in corso. Per avere un indirizzo stabile immediatamente disponibile dopo il riavvio, configura `TGWITNESS_PUBLIC_URL` con l'origine HTTPS del pannello prima di avviarlo. Header Host e di inoltro arbitrari non registrano un indirizzo attendibile. I controlli su Host e Origin rifiutano origini del browser non correlate. Le risposte usano `Cache-Control: no-store`; i valori di autorizzazione non vengono mai registrati nei log.

Un indirizzo `*.trycloudflare.com` è temporaneo. Quando il riavvio di un tunnel modifica l'hostname, aggiorna l'URL pubblico configurato e l'URL MCP di ciascun client. Usa un hostname stabile per le configurazioni salvate dei client.

## Strumenti e limiti

| Strumento | Cosa legge |
| --- | --- |
| `list_workspaces` | Spazi di lavoro autorizzati |
| `list_chats` | Chat autorizzate |
| `search_messages` | Testo dei messaggi salvati nel periodo selezionato |
| `get_message_versions` | Versioni acquisite e osservazioni di eliminazione |
| `get_message_context` | ID dei messaggi acquisiti circostanti |
| `get_journal_event` | Un record sanificato con il relativo riferimento alla fonte |
| `get_capture_status` | Stato della raccolta e record di copertura consentiti |

`tools/list` restituisce solo gli strumenti concessi a quella connessione. Le chiamate ad altri strumenti vengono rifiutate. Gli strumenti per contesto di gruppo, episodi, terminologia e catene di risposte non sono offerti in questa build; il relativo backend separato per i context-pack non è incluso.

Ogni lettura verifica il token, lo strumento e l'ambito di spazio di lavoro/chat, anche al termine dell'operazione sul database. I limiti sono di 60 richieste al minuto, 50 record per pagina, 64 KiB per risultato e una scadenza di otto secondi per l'archivio. Una chiamata MCP scaduta restituisce un errore dello strumento richiedendo un periodo più ristretto o un limite inferiore.

I risultati dei messaggi riportano `untrusted_content: true`, gli ID di spazio di lavoro/chat/messaggio, la sequenza dell'evento, l'hash salvato e un link al pannello. Gli oggetti Telegram grezzi, gli access hash, le sessioni e le chiavi vengono omessi. Il troncamento del testo viene segnalato. Modifiche, avvisi di eliminazione e `missing_on_recheck` sono osservazioni distinte. L'assenza di record non dimostra che un evento non sia mai accaduto.

Tratta le istruzioni contenute nei messaggi acquisiti come prove, mai come istruzioni per il client. L'accesso in sola lettura impedisce modifiche all'archivio; il client può comunque conservare i contenuti che è autorizzato a leggere. Gli hash identificano i record salvati e supportano i controlli di integrità; non dimostrano la paternità su Telegram né la completezza dell'acquisizione.
