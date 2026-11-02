# Progettare un report

Canonical page: https://phishdestroy.github.io/TgWitness/it/docs/reports/

Fornire al lettore un percorso chiaro dalla domanda relativa al caso ai record salvati.

Report Studio combina la selezione dei dati, cronologie delle modifiche leggibili, grafici e le conclusioni scritte dall’utente. Otto modelli integrati sono applicabili agli output supportati in formato HTML e PDF nativo. I report in formato HTML, PDF e JSON recano i propri sigilli firmati; il manifesto ZIP raggruppa inoltre i file nel pacchetto. I file HTML e PDF vengono sigillati una volta completato il loro layout finale.

## Creare un rapporto in tre passaggi

1. Aprire **Esportazioni → Configura e visualizza anteprima → Dati**. Utilizzare l’intero spazio di lavoro oppure selezionare chat, autori, date di osservazione UTC incluse e tipi di record. Le date indicano quando TgWitness ha rilevato il record.
2. Nella sezione **“Design e contenuti**”, scegliere un’impostazione predefinita per il design e i contenuti. Selezionare i grafici delle attività, le etichette dei partecipanti, la trascrizione, le modifiche salvate e il materiale opzionale della Case Board. Aggiungere i dettagli del caso e le note relative all’esame.
3. Apri **“Anteprima”** per verificare conteggi, attività, partecipanti, record campionati e intervalli di ID mancanti. Salva le impostazioni, quindi scarica il formato che ti serve.

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

**Le sezioni Classic, Editorial, Briefing, Analytics, Technical, Overview, Reading series e Ledger & margin** presentano gli stessi record sottostanti in composizioni diverse. Modificando il layout si mantengono la selezione dei dati e le note scritte. La lingua del report può essere scelta tra le 25 lingue supportate.

La serie "Lettura" raggruppa il caso, l’ambito, i risultati e le modifiche attorno a una barra laterale. "Ledger & margin" utilizza capitoli numerati e un ampio margine. Entrambe supportano anche le panoramiche HTML degli account e la condivisione delle copie. I PDF nativi vengono generati con i font inclusi nel pacchetto; il computer dell’utente non necessita dell’installazione di un browser o di Node per la creazione dei PDF. I PDF in cinese, giapponese e coreano richiedono inoltre un font adeguato sul server, come Noto Sans CJK, installato a livello di sistema o collocato nella directory `TGWITNESS_FONT_DIR`. In sua assenza, il file ZIP conserva i report in formato HTML e JSON.

## Leggere una modifica nel suo contesto

Le modifiche salvate vengono mostrate prima e dopo. Un avviso di cancellazione può essere accompagnato dall’ultima versione acquisita. Risposte, citazioni, inoltri, reazioni, pulsanti e metadati degli allegati mantengono i riferimenti disponibili. Gli hash SHA-256 dei file e quelli dei record di registro sono etichettati separatamente.

L’anteprima del layout mostra la copertina, la sezione di analisi e i grafici utilizzando record corrispondenti tra i primi 50.000 record di origine. L’anteprima separata dei dati esamina l’istantanea completa e stabile del registro per ottenere il conteggio esatto delle selezioni, con i limiti del campione visualizzati e contrassegnati. Generare un PDF per verificare l’impaginazione finale. L’esportazione completa dell’account include una panoramica in formato HTML; i singoli PDF delle chat utilizzano il layout scelto.

## Scegli con cura la versione destinata al destinatario

I filtri dei report ne determinano la leggibilità. Il file ZIP contenente tutte le prove conserva il registro originale e gli allegati. Utilizzare una [procedura di consegna ridotta al minimo](https://phishdestroy.github.io/TgWitness/it/docs/handover/) quando il destinatario deve ricevere solo i dati selezionati. Visualizzare [il contenuto del report e la verifica](https://phishdestroy.github.io/TgWitness/it/docs/reference/case-reports/) oppure [verificare l’esportazione completata](https://phishdestroy.github.io/TgWitness/it/docs/exports/).
