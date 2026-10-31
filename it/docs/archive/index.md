# Gestisci l’archivio

Canonical page: https://phishdestroy.github.io/TgWitness/it/docs/archive/

Trova il messaggio. Verifica la fonte. Costruisci il caso.

Questi strumenti sono disponibili nel ramo principale attuale. L'anteprima portatile 0.7.0 è precedente a questi; per questo flusso di lavoro, utilizzare un checkout dal codice sorgente.

01**Inserire la cronologia**

Carica i messaggi precedenti dalle tue fonti abilitate nell’area di lavoro.

02**Segui le fonti**

Effettua una ricerca nell’archivio e apri il messaggio salvato associato a ciascun risultato.

03**Mantenere chiara la transizione**

Salva la tua analisi separatamente ed esporta le prove firmate accanto ad essa.

I dati acquisiti, il testo riconosciuto e le conclusioni degli analisti rimangono ben distinti.

## Carica i messaggi precedenti

1. Aprire **Fonti → Chat nell'ambito**, esaminare le chat abilitate e avviare l’osservazione.
2. Selezionare **«Carica cronologia completa**». L’esecuzione utilizza l’elenco delle fonti selezionato in quel momento.
3. Utilizzare **«Cronologia delle pause»** e **«Cronologia delle riprese»** secondo necessità. Dopo un riavvio, riprendere esplicitamente.
4. Verificare i risultati per ciascuna fonte e la coda degli allegati. Salvare il rapporto sullo stato di avanzamento firmato insieme all’esportazione delle prove.

Questa operazione riempie l’area di lavoro con i messaggi disponibili. L’esportazione in formato HTML/JSON per singola chat è un’operazione separata. [Cronologia e dettagli sul recupero](https://phishdestroy.github.io/TgWitness/it/docs/reference/history/).

## Prima cerca, poi decidi in merito all’IA

1. Aprire **Registro** per la ricerca locale. Scegliere un’area di lavoro e usare i filtri per fonte e periodo.
2. Cerca una frase o un dominio. Apri il record corrispondente e le sue versioni salvate.
3. Per l’analisi tramite IA, l’amministratore abilita e configura un provider in **Integrazioni**. Aprire **Chieda all’archivio** e scegliere le chat e un periodo. Esaminare la sezione **Dati inviati al modello** e deselezionare gli estratti indesiderati prima di approvare la richiesta.
4. Controlla i riferimenti restituiti. Salva la risposta come rapporto e aggiungi le tue revisioni o note.

Le ricerche vengono eseguite localmente senza l’uso dell’intelligenza artificiale. I rapporti analitici conservano i riferimenti alle fonti e la cronologia delle revisioni; sono separati dal registro firmato. [Configurazione del provider e rapporti](https://phishdestroy.github.io/TgWitness/it/docs/reference/analysis/).

## Scegli la connessione che ti serve

| Compito | Apri | Configurazione |
| --- | --- | --- |
| Leggi alcune chat selezionate da un client AI | **Integrazioni → MCP** | [Installare l’extra MCP, generare un token con ambito limitato e connettere il client](https://phishdestroy.github.io/TgWitness/it/docs/reference/mcp/) |
| Riconoscimento del testo nei file multimediali salvati | Un record `media.saved` → **Riconoscere l'allegato** | [Configurare il worker Docker locale e i file di lingua/modello necessari](https://phishdestroy.github.io/TgWitness/it/docs/reference/media-analysis/) |
| Invia gli eventi a n8n o a un SIEM | **Integrazioni → Webhook in uscita** | [Aggiungere un destinatario, verificare l’HMAC ed eliminare i duplicati degli ID evento](https://phishdestroy.github.io/TgWitness/it/docs/reference/webhooks/) |

**Quale token di accesso va dove?**

L'accesso al pannello è riservato alle persone incaricate di esaminare il caso. Gli utenti con connessione MCP ricevono token di archivio separati in sola lettura. Un ricevitore webhook utilizza il proprio segreto HMAC. Nessuno necessita di un file di sessione di Telegram.

[Condividi l'accesso al pannello di controllo](https://phishdestroy.github.io/TgWitness/it/docs/access/) o [configura un client MCP](https://phishdestroy.github.io/TgWitness/it/docs/reference/mcp/).

## Fornire fonti e conclusioni

Conservare il rapporto analitico revisionato insieme al file ZIP contenente le prove firmate. Il rapporto illustra la vostra interpretazione delle fonti; il file ZIP consente al destinatario di verificare la corrispondenza tra la registrazione salvata e un’impronta digitale e un punto di controllo indipendenti e attendibili.

[Esportare e verificare](https://phishdestroy.github.io/TgWitness/it/docs/exports/) · [Svolgimento di un'indagine completa](https://phishdestroy.github.io/TgWitness/it/docs/cases/)
