# Telegram · Riga di comando

Canonical page: https://phishdestroy.github.io/TgWitness/it/docs/reference/cli/

Effettuare ricerche, leggere il contesto, contare le attività ed esportare i messaggi salvati da script e agenti, con output in formato --json, codici di uscita stabili e token di sola lettura con ambito limitato.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Documentazione](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md)

![Integrazioni con gli archivi](https://phishdestroy.github.io/TgWitness/assets/chapter-integrations.svg)

[MCP in sola lettura](https://phishdestroy.github.io/TgWitness/it/docs/reference/mcp/) · [Ricerca full-text](https://phishdestroy.github.io/TgWitness/it/docs/reference/search/) · [Wiki](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

**Anteprima.** `tgwitness search`, `context`, `messages`, `stats` e `export` leggere le osservazioni salvate per script e agenti IA. Non possono inviare nulla a Telegram, cambiare le impostazioni o modificare il registro firmato.

Con `--json`, stdout trasmette esattamente un documento JSON (`export` scrive righe JSON). Lo stato di avanzamento, i suggerimenti e gli errori vengono inviati a stderr. I codici di uscita sono stabili:

| Codice | Significato |
| --- | --- |
| `0` | Esito positivo, compreso un risultato vuoto |
| `1` | Errore: pannello non raggiungibile, dati illeggibili, esportazione interrotta |
| `2` | Errore di utilizzo o richiesta non valida: data errata, opzione sconosciuta, indice di ricerca disattivato |
| `3` | Al momento non disponibile: l'area di lavoro è aperta in un pannello attivo, oppure il pannello richiede di riprovare più tardi (limite di frequenza, timeout) |
| `4` | Accesso negato: token mancante, scaduto o revocato, una chat al di fuori del suo ambito di applicazione, uno strumento non consentito |

## Due modi di leggere

**Tramite il pannello (`--url`).** Il comando utilizza la stessa API di archivio con ambito di MCP. Creare una connessione in **Integrazioni → MCP**: scegliere gli spazi di lavoro e le chat, gli strumenti e una scadenza, quindi copiare il token una volta. La connessione è di sola lettura, limitata a quelle chat, soggetta a un limite di 60 richieste al minuto e può essere revocata o aggiornata in qualsiasi momento. I token di accesso al pannello e le credenziali di Telegram non funzionano in questo caso.

```
export TGWITNESS_URL=https://panel.example.org      # default http://127.0.0.1:8787
export TGWITNESS_MCP_TOKEN=tgw_mcp_...              # or --token-file path
tgwitness search 'перевод карта' --json
```

Un pannello remoto richiede HTTPS; l'HTTP semplice è accettato solo per `127.0.0.1`, `localhost` e `::1`. Le variabili d’ambiente del proxy vengono ignorate e i reindirizzamenti sono rifiutati, in modo che il token raggiunga esclusivamente l’indirizzo specificato.

**Direttamente da uno spazio di lavoro arrestato (`--data-dir`).** Legge la directory dei dati con pieno accesso locale, senza token. Utilizzarlo su una copia della directory dei dati o mentre la raccolta è arrestata. I record firmati non vengono mai modificati; come nel pannello, l’apertura di uno spazio di lavoro può aggiornare gli indici derivati. Quando il pannello ha lo spazio di lavoro aperto, il comando termina con codice `3`; leggere invece tramite il pannello. In assenza di `--data-dir`, `TGWITNESS_DATA`, `./data/live` , viene utilizzata la directory dei dati dell’installazione in cui viene eseguito il comando.

`--workspace ID` seleziona un'area di lavoro (per impostazione predefinita `default`). `tgwitness messages
--workspaces` elenca quelli che è possibile leggere.

## Comandi

| Comando | Risultato |
| --- | --- |
| `tgwitness search QUERY [--chat ID] [--since] [--until] [--any] [--limit N] [--offset N]` | I risultati più pertinenti per primi, con forme delle parole, frasi esatte tra virgolette, domini e `@username` ([sintassi](https://phishdestroy.github.io/TgWitness/it/docs/reference/search/#search-syntax)) |
| `tgwitness search QUERY --exact [--before SEQ]` | Testo esatto, dal più recente al più vecchio, senza l'indice |
| `tgwitness context CHAT_ID MESSAGE_ID` | Messaggi salvati entro dieci ID di messaggio in entrambe le direzioni |
| `tgwitness messages` | Chat che puoi leggere |
| `tgwitness messages CHAT_ID [--since] [--until] [--before SEQ]` | Messaggi salvati della chat, dal più recente al più vecchio |
| `tgwitness messages CHAT_ID --message ID` | Ogni versione salvata e ogni registrazione di cancellazione di un messaggio |
| `tgwitness stats [--chat ID] [--sender ID] [--since] [--until] [--top N]` | Statistiche sulle attività, di seguito |
| `tgwitness export [--chat ID] [--since] [--until] [--output FILE]` | Osservazioni salvate come righe JSON nell’ordine in cui compaiono nel registro |

Le date sono `2026-10-01` (mezzanotte UTC) oppure in formato ISO con indicazione del fuso orario, `2026-10-01T09:00+03:00`. Per quanto riguarda `search`, `messages` e `export` si seleziona l’ora dell’osservazione. Le pagine contengono fino a 50 record: seguire `next_offset` (`--offset`) per la ricerca per ordine di priorità e `next_before` (`--before`) altrove.

La ricerca ordinata si interrompe a 1,000 risultati. L’ultima pagina potrebbe essere più breve di `--limit`; restringere la query, la chat o il periodo quando esistono più osservazioni corrispondenti.

Ogni risultato di messaggio riporta `untrusted_content: true`, gli ID dell’area di lavoro, della chat e del messaggio, la sequenza del registro, l’hash del record salvato e un link al pannello. Le modifiche, le notifiche di cancellazione e `missing_on_recheck` costituiscono record separati. L’assenza di un record non dimostra che un evento non sia mai avvenuto.

### Statistiche sulle attività

`stats` Conta le osservazioni salvate relative a una chat, a un mittente o a tutte le chat incluse nell'ambito di analisi:

- messaggi per ora UTC e per giorno della settimana (a partire dal lunedì), ore e giorni di maggiore traffico;
- modificati, eliminati e `missing_on_recheck` condivisioni;
- mittenti con il numero di messaggi e le date e gli orari del primo e dell’ultimo messaggio;
- i domini più frequenti e `@handles`, conteggiati una volta per messaggio in tutte le sue versioni salvate;
- copertura: `coverage.gap` registrazioni e, per l’accesso all’intero spazio di lavoro, periodi in cui non è presente un segnale di attività del collettore connesso (`collector_liveness`).

Il periodo seleziona **l’ora del messaggio riportata da Telegram**. Il conteggio delle ore e dei giorni della settimana può aiutare a stimare il fuso orario del mittente, ma non lo determina con certezza. I dati vengono calcolati su richiesta dal registro e non vengono memorizzati. Ogni risultato indica l’intestazione del registro a cui si riferisce quando l’accesso copre l’intero spazio di lavoro. La lettura si interrompe dopo cinque secondi di scorrimento nel pannello, oppure `--timeout` a livello locale (impostazione predefinita 30); quindi `complete` è falso e `partial` indica il primo record che non è stato letto. In tal caso vengono contati solo i record più recenti.

### Esporta

`export` scrive un oggetto JSON per ogni osservazione salvata (nuovi messaggi, istantanee, modifiche, messaggi recuperati, avvisi di cancellazione, `missing_on_recheck` e registrazioni multimediali salvate) nell’ordine del registro. Ogni riga presenta gli stessi campi degli altri risultati, con il testo completo. Con `--output`, il file viene salvato con un `.partial` nome e viene rinominato solo dopo il completamento della registrazione del pannello; un’esportazione interrotta non lascia alcun file e termina con il codice `1`. `--output` non sovrascrive mai un file esistente. Con `--output` e `--json`, stdout riporta un riepilogo: numero di record, ultima sequenza del journal e, per l’accesso all’intero spazio di lavoro, l’intestazione del journal.

L'esportazione tramite il pannello richiede una connessione che consenta **l'esportazione dei messaggi (solo da riga di comando)**; questa opzione non è selezionata per impostazione predefinita. Questo file è una copia di lavoro, non una prova: per un trasferimento verificabile utilizzare l'esportazione firmata in **"Esportazioni**", che `python -m tgwitness.verify`effettua le verifiche.

Il pannello ricontrolla l’accesso prima di emettere ogni record, compreso il record di completamento. Un accesso revocato o scaduto comporta un’esportazione incompleta. Le letture differite delle pagine condividono il limite dei worker dell’archivio con altre query e hanno un tempo di attesa limitato.

## Competenze dell’agente

[`.agents/skills/tgwitness-cli/SKILL.md`](https://github.com/phishdestroy/TgWitness/blob/main/.agents/skills/tgwitness-cli/SKILL.md) spiega a un agente come utilizzare questi comandi, come citare i record e come trattare il testo acquisito. Gli agenti che leggono `.agents/skills` lo caricano da un repository checkout. Per Claude Code, copiare la `tgwitness-cli` cartella nel `.claude/skills/` nel tuo progetto oppure `~/.claude/skills/`.

## MCP e la riga di comando

Entrambi utilizzano le stesse connessioni, gli stessi controlli di ambito e gli stessi limiti. I risultati di MCP sono limitati a una pagina da 64 KiB, pertanto MCP non offre l’esportazione in blocco; la riga di comando ne esegue lo streaming. `get_activity_stats` è disponibile per entrambi.
