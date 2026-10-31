# Analisi dell’archivio

Canonical page: https://phishdestroy.github.io/TgWitness/it/docs/reference/analysis/

Cerca i messaggi salvati, esamina i dati forniti dall’intelligenza artificiale e conserva i rapporti analitici con i relativi riferimenti alle fonti.

**Versione principale attuale:** utilizzare un checkout dal codice sorgente; l’anteprima portatile 0.7.0 è precedente a questa funzionalità.

[Guida al flusso di lavoro](https://phishdestroy.github.io/TgWitness/docs/archive/) · [Wiki](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

Aprire **"Ask the archive"** nel pannello. Il selettore dell’area di lavoro consente di scegliere l’account; il modulo permette di selezionare le chat e il periodo di osservazione. La ricerca viene eseguita localmente, senza l’uso dell’intelligenza artificiale. Una frase esatta o un dominio restringono i risultati; l’ID di un messaggio consente di richiedere le versioni salvate. Esaminare gli estratti restituiti e aprire i relativi record del registro o il contesto. Non è presente alcun database vettoriale né alcuna azione automatica su Telegram.

## Fornitori e consenso

L'IA è disattivata per impostazione predefinita in ogni area di lavoro. Solo l'amministratore principale può configurare il modello, l'endpoint, la chiave API crittografata, i limiti di contesto/output, il timeout e il budget giornaliero di richieste. La chiave non viene mai restituita al browser. Lasciare vuoto il campo della chiave per mantenere quella attuale, oppure rimuoverla esplicitamente.

Ollama utilizza il proprio [endpoint `/api/chat`](https://docs.ollama.com/api/chat) documentato con output JSON non in streaming. Il suo indirizzo predefinito è `http://127.0.0.1:11434` sul server di TgWitness. L’operatore può modificarlo utilizzando `TGWITNESS_AI_LOCAL_ENDPOINT`; non si tratta di un indirizzo controllato dal modello. Installare autonomamente il modello selezionato. TgWitness non lo scarica automaticamente.

Il provider compatibile richiede un URL di base che termini con `/v1` e il [protocollo Chat Completions](https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create): `messages`, modalità di risposta JSON, `max_completion_tokens` e `choices[0].message.content`. I servizi privi di questi campi non sono supportati. Il test di connessione invia testo sintetico e viene conteggiato nel budget delle richieste.

Ogni richiesta utilizza il percorso esterno configurato nell’area di lavoro. Un percorso bloccato o un MTProxy esclusivo per Telegram genera un errore; non è previsto alcun nuovo tentativo diretto. Un indirizzo Ollama locale configurato appositamente consente una destinazione privata, pur continuando a utilizzare il percorso scelto. Per altri servizi privati si applica l’attuale opzione di attivazione della destinazione privata a livello di server. Il pannello mostra l’endpoint effettivamente configurato.

Prima della generazione, **i dati inviati al modello** mostrano la richiesta: domanda, estratti selezionati, tipi di evento, orari di osservazione e indicatori di copertura. Le sessioni di Telegram, i campi grezzi, le chiavi del provider, i byte degli allegati e il registro completo non fanno parte di tale contesto. Deselezionare le fonti indesiderate, quindi approvare esplicitamente l’elaborazione. I fornitori esterni possono conservare i contenuti inviati in base alle proprie politiche. L’esecuzione locale significa che l’endpoint è locale; non costituisce una garanzia riguardo al comportamento di un servizio configurato in modo indipendente.

A livello globale sono consentite al massimo due richieste simultanee per provider e una per spazio di lavoro. Un’anteprima scade dopo dieci minuti e può generare una sola risposta. Vengono mostrati i conteggi dei token segnalati dal provider; una stima dei costi appare solo quando sono state configurate sia le tariffe di input che quelle di output. Anche i tentativi falliti consumano il budget giornaliero di richieste. I tentativi automatici di riprova non consumano budget aggiuntivo.

## Fonti e limiti

La funzione di recupero esamina il testo dei messaggi salvati tramite una ricerca lessicale circoscritta. Restituisce fino a 24 fonti e contrassegna gli estratti troncati o i set di risultati incompleti. Il periodo si riferisce al **tempo di osservazione**, non a un'affermazione secondo cui la cronologia di Telegram sia completa. Gli eventi che riguardano l'intero spazio di lavoro non sono accessibili dall'ambito della chat. I dati mancanti vengono indicati come «non trovati nell’archivio disponibile».

Il modello non riceve alcun strumento. I suoi ID di origine vengono confrontati con i record selezionati, gli hash vengono ricontrollati e le stringhe citate devono essere presenti in tali record. ID sconosciuti, citazioni modificate e affermazioni non citate comportano il rifiuto della risposta. L’applicazione crea collegamenti; gli URL generati dal modello non vengono utilizzati come citazioni. Questi controlli stabiliscono l’esistenza della fonte e l’accuratezza della citazione, non la veridicità di un’inferenza. Verificare le inferenze confrontandole con i record prima di fare affidamento su di esse.

## Rapporti

Salva una risposta revisionata come rapporto analitico separato. Esso include il riassunto del modello, la cronologia osservata, i link e gli handle estratti, i registri di modifica/cancellazione, i limiti di copertura e gli hash degli eventi di origine. Sono riportati anche il fornitore, il modello, l’endpoint, l’ora e la versione del modello di prompt. Nessuna identità viene automaticamente associata.

Le revisioni e le note degli analisti vengono archiviate separatamente dal riepilogo del modello. I rapporti sono contenuti in file derivati crittografati, con un indice esterno al flusso di eventi firmato; gli eventi e i file multimediali originali non subiscono modifiche. Solo il proprietario o l’amministratore può aprire un rapporto e l’accesso alla fonte viene nuovamente verificato. Anche il download richiede l’autorizzazione all’esportazione. La versione 1 non firma i rapporti né implica che le conclusioni del modello costituiscano prove verificate. Limiti: 100 rapporti per area di lavoro e 100 revisioni degli analisti per rapporto.

Per l’OCR manuale e le trascrizioni, consultare la sezione [«Elaborazione dei media](https://phishdestroy.github.io/TgWitness/it/docs/reference/media-analysis/)». Per l’accesso dei clienti, consultare la sezione [«MCP](https://phishdestroy.github.io/TgWitness/it/docs/reference/mcp/)».
