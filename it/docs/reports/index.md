# Progettare un report

Canonical page: https://phishdestroy.github.io/TgWitness/it/docs/reports/

Porti il lettore dalla domanda del caso direttamente alle voci salvate.

Report studio mette insieme i dati scelti, le cronologie delle modifiche, i grafici e le Sue conclusioni. Otto design, HTML e PDF nativo. Ogni report HTML, PDF e JSON viene sigillato con la Sua chiave.

## Creare un rapporto in tre passaggi

1. **Esportazioni → Configura e anteprima → Dati**: l’intero spazio oppure chat, autori, date (UTC, quando TgWitness ha visto la voce) e tipi di voce scelti.
2. **Design e contenuti**: scelga un design e cosa entra: grafici, partecipanti, trascrizione, modifiche, elementi Case Board, dati del caso e note.
3. **Anteprima**: controlli conteggi, attività, campioni e intervalli di ID mancanti. Salvi, poi scarichi il formato che Le serve.

### Organizzare lo stesso materiale salvato in modo che risulti comprensibile per il lettore

Esempio sintetico · layout schematico, non un report generato

1. **Seleziona.** Scegli due chat e il periodo di osservazione per il caso.
2. **Redigere il testo.** Scegliere un layout e le sezioni che rispondono alla domanda.
3. **Anteprima.** Verificare il numero di parole selezionate e il testo "prima e dopo" salvato.
4. **Verificare.** Generare il file finale e controllarne la firma confrontandola con l’impronta digitale dell’area di lavoro attendibile.

#### Osservazioni selezionate

2 chat · 1 giorno di osservazione

Messaggi, modifiche e avvisi di cancellazione

#### Struttura del rapporto

##### Modifica della destinazione del pagamento

Domanda relativa al caso → ambito → risultati → riferimenti ai record

**Contesto del messaggio**

Osservazione n. 142: «Utilizza il nuovo link di pagamento.»

**Modifiche salvate**

Prima: old.example.invalid → Dopo: new.example.invalid

#### Rivedere la selezione

18 osservazioni · 2 modifiche salvate

Gli orari di invio, modifica e consultazione sono contrassegnati da etichette distinte.

#### Prodotto finale

PDF firmato + JSON firmato, oppure un file ZIP firmato contenente il relativo report leggibile

Il destinatario verifica il file e l’impronta digitale attendibile.

## Scegli uno stile di lettura

**Classic, Editorial, Briefing, Analytics, Technical, Overview, Reading series, and Ledger & margin**: le stesse voci, un aspetto diverso. Cambiando si mantengono selezione e note. Qualsiasi delle 25 lingue.

I PDF si generano con font inclusi, senza browser. Cinese, giapponese e coreano richiedono un font come Noto Sans CJK sul server (di sistema o in `TGWITNESS_FONT_DIR`), altrimenti ottiene solo HTML e JSON.

## Leggere una modifica nel suo contesto

Le modifiche mostrano prima e dopo, le eliminazioni l’ultima versione salvata. Risposte, inoltri, reazioni, pulsanti e allegati conservano i loro riferimenti.

L’anteprima del design usa le prime 50.000 voci, quella dei dati conta tutto esattamente. Per l’impaginazione finale generi il PDF.

## Scegli con cura la versione destinata al destinatario

I filtri danno forma solo al report; lo ZIP delle prove contiene sempre il diario e i file completi. Se il destinatario deve ricevere meno, usi una [consegna ridotta](https://phishdestroy.github.io/TgWitness/it/docs/handover/). Altro: [contenuto del report](https://phishdestroy.github.io/TgWitness/it/docs/reference/case-reports/), [verificare l’esportazione](https://phishdestroy.github.io/TgWitness/it/docs/exports/).
