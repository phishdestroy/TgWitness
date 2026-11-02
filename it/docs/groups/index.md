# Gestire un gruppo di account

Canonical page: https://phishdestroy.github.io/TgWitness/it/docs/groups/

Gestire contemporaneamente più account di raccolta, mantenendo distinti i record e l’identità di firma di ciascun account.

Un gruppo di account riunisce lo stato della connessione, i controlli di monitoraggio, le impostazioni condivise e le esportazioni in un’unica vista operativa. È utile quando più account riguardano la stessa indagine o necessitano di una configurazione operativa coerente.

## Apri la panoramica del gruppo

In **“Accounts”**, aprire il gruppo. Ogni account mostra il proprio stato di monitoraggio, il percorso di connessione, l’ultima latenza del percorso misurata al momento del successo dell’ultimo controllo e l’ultimo messaggio salvato. I link **“Needs attention”** rimandano agli account che richiedono un intervento; **“Fix”** apre l’area di lavoro e i controlli pertinenti.

**Le funzioni “Avvia tutto”** e **“Metti in pausa tutto”** agiscono sugli account idonei dopo la conferma. **Le impostazioni di gruppo** condividono le impostazioni selezionate; gli account con valori propri li mantengono fino a quando non si sceglie di sostituirli.

### Verifica una modifica di percorso all’interno di un gruppo

Esempio sintetico · verifiche illustrative e risultati

1. **Seleziona.** Scegli il gruppo e verifica quali account subiranno modifiche.
2. **Preparazione.** Mantenere il percorso specifico di un account quando deve rimanere separato.
3. **Verificare.** Testare la connessione proposta e controllare i risultati delle misurazioni.
4. **Invia la traduzione.** Ricontrolla prima di salvare e verifica il risultato per ogni account.

#### Team incaricato del caso

Collector per canali · Collector per gruppi · Account di riferimento

3 aree di lavoro separate

#### Selezione revisionata

2 account seguono il percorso proposto.

L'account di riferimento mantiene il proprio percorso.

#### Controlli preliminari

Collector dei canali: tempo di trasmissione su Telegram 84 ms

Collector di gruppo: tempo di trasmissione Telegram 91 ms

Questi numeri sono valori fittizi forniti a titolo esemplificativo.

#### Risultati dell’applicazione

Collector del canale: percorso salvato, osservazione ripresa.

Collector di gruppo: ricontrollo fallito, ripristinate le impostazioni precedenti.

Account di riferimento: percorso originale mantenuto.

## Modificare il percorso aggiungendo una fase di revisione

1. Selezionare **«Modifica il percorso del gruppo**», quindi scegliere il tipo di connessione e le impostazioni.
2. Selezionare **“Revisione**”. Esaminare gli account elencati e le rispettive sostituzioni di percorso individuali.
3. Selezionare **«Prepara e verifica**». La verifica utilizza un nuovo trasporto Telegram; anche i percorsi HTTP supportati riportano la verifica di uscita HTTPS.
4. Selezionare **«Applica connessione selezionata»** e verificare il risultato di ciascun account. L’osservazione precedentemente in corso riprende laddove l’applicazione va a buon fine; gli account inattivi rimangono tali.

La latenza descrive il tempo misurato per l’instaurazione della connessione a Telegram. Un controllo dell’IP di uscita descrive quel percorso al momento del controllo registrato. L’autorizzazione dell’account e lo stato di integrità dell’osservazione hanno i propri indicatori; una modifica al gruppo può portare a esiti diversi a seconda dell’account.

## Utilizzare l’accesso sovrapposto

**La sezione “Chat visibili da più account**” mostra le fonti condivise e la copertura di osservazione disponibile nell’area di lavoro. I canali e i supergruppi idonei possono utilizzare **la funzione “Esporta con … account”** per suddividere l’acquisizione della cronologia di una chat. Le chat private e i gruppi ordinari rimangono associati all’account di partenza poiché i numeri dei messaggi appartengono alla cronologia di quell’account.

## Esporta il gruppo come pacchetto

**Il gruppo “Export”** crea un unico file ZIP contenente l’esportazione firmata di ciascun account e un elenco firmato di tali file. Le identità e le impronte digitali originali dell’area di lavoro rimangono disponibili per la verifica. Costruire una narrazione trasversale tra gli account utilizzando tali riferimenti; una singola cronologia unificata viene comunque assemblata separatamente.

Proseguire con [la progettazione del report](https://phishdestroy.github.io/TgWitness/it/docs/reports/), [un Case Board all’interno di uno spazio di lavoro](https://phishdestroy.github.io/TgWitness/it/docs/case-board/) o [la verifica dell’esportazione](https://phishdestroy.github.io/TgWitness/it/docs/exports/).
