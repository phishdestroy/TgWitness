# Analisi dell’archivio

Canonical page: https://phishdestroy.github.io/TgWitness/it/docs/reference/analysis/

Cerca i messaggi salvati, esamina i dati forniti dall’intelligenza artificiale e conserva i rapporti analitici con i relativi riferimenti alle fonti.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Documentazione](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Investigation](https://phishdestroy.github.io/TgWitness/it/docs/reference/investigation/)

![Investigation](https://phishdestroy.github.io/TgWitness/assets/chapter-investigate.svg)

[Guida al flusso di lavoro](https://phishdestroy.github.io/TgWitness/docs/archive/) · [Wiki](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

Utilizzare **il Registro** per la ricerca locale senza IA; [la ricerca full-text](https://phishdestroy.github.io/TgWitness/it/docs/reference/search/) (anteprima) trova corrispondenze tra forme di parole, frasi, domini e @nomi utente. Per **"Chiedi all’archivio**", abilitare e configurare prima un provider in **Integrazioni**. Il selettore dell’area di lavoro sceglie l’ account; il modulo seleziona le chat e il periodo di osservazione. Il recupero avviene localmente. Una frase esatta o un dominio restringe il recupero; un ID messaggio richiede le versioni salvate . Esamina gli estratti e apri i relativi record del registro o il contesto. Non è presente alcun database vettoriale né alcuna azione automatica su Telegram.

## Fornitori e consenso

L'IA è disattivata per impostazione predefinita in ogni area di lavoro. Solo l'amministratore principale può configurare il modello, l'endpoint, la chiave API crittografata, i limiti di contesto/output, il timeout e il budget giornaliero di richieste. La chiave non viene mai restituita al browser. Lasciare vuoto il campo della chiave per mantenere quella attuale, oppure rimuoverla esplicitamente.

Ollama utilizza il proprio [endpoint `/api/chat`](https://docs.ollama.com/api/chat) documentato con output JSON non in streaming. Il suo indirizzo predefinito è `http://127.0.0.1:11434` sul server di TgWitness. L’operatore può modificarlo utilizzando `TGWITNESS_AI_LOCAL_ENDPOINT`; non si tratta di un indirizzo controllato dal modello. Installare autonomamente il modello selezionato. TgWitness non lo scarica automaticamente.

Il provider compatibile richiede un URL di base che termini con `/v1` e il [protocollo Chat Completions](https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create): `messages`, modalità di risposta JSON, `max_completion_tokens` e `choices[0].message.content`. I servizi privi di questi campi non sono supportati. Il test di connessione invia testo sintetico e viene conteggiato nel budget delle richieste.

Ogni richiesta utilizza il percorso esterno configurato nell’area di lavoro. Un percorso bloccato o un MTProxy riservato a Telegram costituisce un errore; non è previsto alcun riprovo diretto. Un indirizzo Ollama locale configurato intenzionalmente consente una destinazione privata. Un endpoint AI di loopback richiede il percorso esterno Direct dell’area di lavoro; i percorsi proxy vengono rifiutati prima della trasmissione. Per altri servizi privati si applica l’opt-in esistente a livello di server per le destinazioni private. L’anteprima mostra l’endpoint e il percorso esterno, incluso l’host proxy, se applicabile. La modifica di tale percorso richiede una nuova anteprima.

Prima della generazione, **i dati inviati al modello** mostrano la richiesta: domanda, estratti selezionati, tipi di evento, orari di osservazione e indicatori di copertura. Le sessioni di Telegram, i campi grezzi, le chiavi del provider, i byte degli allegati e il registro completo non fanno parte di tale contesto. Deselezionare le fonti indesiderate, quindi approvare esplicitamente l’elaborazione. I fornitori esterni possono conservare i contenuti inviati in base alle proprie politiche. L’esecuzione locale significa che l’endpoint è locale; non costituisce una garanzia riguardo al comportamento di un servizio configurato in modo indipendente.

A livello globale sono consentite al massimo due richieste simultanee per provider e una per spazio di lavoro. Un’anteprima scade dopo dieci minuti e può generare una sola risposta. Vengono mostrati i conteggi dei token segnalati dal provider; una stima dei costi appare solo quando sono state configurate sia le tariffe di input che quelle di output. Anche i tentativi falliti consumano il budget giornaliero di richieste. I tentativi automatici di riprova non consumano budget aggiuntivo.

## Fonti e limiti

Il recupero utilizza l’[indice](https://phishdestroy.github.io/TgWitness/it/docs/reference/search/#ask-the-archive-and-mcp) [full-text](https://phishdestroy.github.io/TgWitness/it/docs/reference/search/#ask-the-archive-and-mcp) quando è completo: i migliori riscontri tra le chat selezionate, comprese le forme delle parole. Le domande riguardanti le modifiche recenti o le versioni di un singolo messaggio, così come le ricerche mentre l’indice è in fase di creazione, utilizzano una ricerca lessicale limitata ai record più recenti. L’anteprima indica il metodo utilizzato. Il recupero restituisce fino a 24 fonti; i testi lunghi vengono troncati in corrispondenza del riscontro. Gli estratti troncati e i set di risultati incompleti vengono contrassegnati. Il periodo si riferisce al **tempo di osservazione**, non a un’affermazione secondo cui la cronologia di Telegram sia completa. Gli eventi con copertura a livello di area di lavoro sono esclusi dall’accesso limitato alle chat. I dati mancanti vengono descritti come non trovati nell’archivio disponibile.

Il modello non riceve alcun strumento. I suoi ID di origine vengono confrontati con i record selezionati, gli hash vengono ricontrollati e le stringhe citate devono essere presenti in tali record. ID sconosciuti, citazioni modificate e affermazioni non citate comportano il rifiuto della risposta. L’applicazione crea collegamenti; gli URL generati dal modello non vengono utilizzati come citazioni. Questi controlli stabiliscono l’esistenza della fonte e l’accuratezza della citazione, non la veridicità di un’inferenza. Verificare le inferenze confrontandole con i record prima di fare affidamento su di esse.

## Rapporti

Salva una risposta revisionata come rapporto analitico separato. Esso include il riassunto del modello, la cronologia osservata, i link e gli handle estratti, i registri di modifica/cancellazione, i limiti di copertura e gli hash degli eventi di origine. Sono riportati anche il fornitore, il modello, l’endpoint, l’ora e la versione del modello di prompt. Nessuna identità viene automaticamente associata.

Le revisioni e le note degli analisti vengono archiviate separatamente dal riepilogo del modello. I rapporti sono contenuti in file derivati crittografati, con un indice esterno al flusso di eventi firmato; gli eventi e i file multimediali originali non subiscono modifiche. Solo il proprietario o l’amministratore può aprire un rapporto e l’accesso alla fonte viene nuovamente verificato. Anche il download richiede l’autorizzazione all’esportazione. La versione 1 non firma i rapporti né implica che le conclusioni del modello costituiscano prove verificate. Limiti: 100 rapporti per area di lavoro e 100 revisioni degli analisti per rapporto.

Per l’OCR manuale e le trascrizioni, consultare la sezione [«Elaborazione dei media](https://phishdestroy.github.io/TgWitness/it/docs/reference/media-analysis/)». Per l’accesso dei clienti, consultare la sezione [«MCP](https://phishdestroy.github.io/TgWitness/it/docs/reference/mcp/)».
