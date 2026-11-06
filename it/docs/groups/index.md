# Telegram · Gestire un gruppo di account

Canonical page: https://phishdestroy.github.io/TgWitness/it/docs/groups/

Gestisca più account insieme, ognuno sempre con le proprie voci e la propria chiave.

Un gruppo riunisce in una schermata stato di connessione, avvio/pausa, impostazioni condivise ed esportazioni. Comodo quando più account lavorano sullo stesso caso.

## Apri la panoramica del gruppo

Apra il gruppo in **Account**. Ogni account mostra stato, percorso, latenza e ultimo messaggio salvato. **Richiede attenzione** elenca quelli con problemi, **Correggi** La porta direttamente lì.

**Avvia tutti** / **Metti in pausa tutti** chiedono prima di agire. Le **Impostazioni del gruppo** sono condivise, ma i valori propri di un account restano finché non li sostituisce.

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

1. **Cambia percorso del gruppo**, scelga tipo e impostazioni.
2. **Rivedi selezione**: quali account cambiano e quali hanno un percorso proprio.
3. **Prepara e verifica** prova una nuova connessione a Telegram e, dove possibile, l’IP di uscita.
4. **Applica connessione verificata** e guardi ogni risultato. Gli account attivi riprendono, quelli fermi restano fermi.

La latenza è il tempo per stabilire la connessione a Telegram; l’IP di uscita è quello mostrato dal percorso al momento della verifica. I risultati possono variare per account.

## Utilizzare l’accesso sovrapposto

**Chat viste da più account** elenca le fonti condivise e la loro copertura. Canali e supergruppi si possono esportare con più account insieme tramite **Esporta con … account**. Chat private e gruppi semplici no: lì i numeri dei messaggi sono per account.

## Esporta il gruppo come pacchetto

**Esporta gruppo** fornisce uno ZIP con l’esportazione firmata di ogni account e un elenco firmato di esse. Ognuna conserva la propria impronta per la verifica. La cronologia unificata la costruisce comunque Lei.

Avanti: [report](https://phishdestroy.github.io/TgWitness/it/docs/reports/), [Case Board](https://phishdestroy.github.io/TgWitness/it/docs/case-board/), [verificare le esportazioni](https://phishdestroy.github.io/TgWitness/it/docs/exports/).
