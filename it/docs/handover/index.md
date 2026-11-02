# Preparare una copia da condividere

Canonical page: https://phishdestroy.github.io/TgWitness/it/docs/handover/

Condividere le osservazioni rilevanti mantenendo intatto lo spazio di lavoro originale.

Un "handover" è un estratto separato e firmato. Scegli le chat e le persone, riduci le identità o il testo e decidi quali file e note del team devono essere inclusi nella copia del destinatario. Il relativo manifesto registra la selezione e il numero di record invariati, ridotti e omessi.

## Preparare l’estratto per il destinatario

1. Aprire **Esportazioni → Estratto per il passaggio di consegne**. Indicare lo scopo, selezionare le chat e, facoltativamente, il periodo UTC, quindi selezionare **Carica i partecipanti delle chat selezionate** se sono necessari i nomi dei soggetti.
2. Scegli come gestire tutti gli altri utenti: utilizza pseudonimi, ometti i loro messaggi o mostrali così come sono stati registrati. Imposta il testo dei messaggi e gli allegati in modo indipendente; se lo desideri, maschera i numeri di telefono e gli indirizzi e-mail.
3. Scegliere se includere i segnalibri e le sezioni di Case Board oppure le schede con i commenti. In questo testo, gli alias degli investigatori possono sostituire i nomi dei team.
4. Selezionare **“Scarica estratto di consegna**”. Aprire localmente il report generato e i record selezionati, verificare l’archivio e controllare la copia prima di inviarla.

### Un originale, una copia destinata alla condivisione

Esempio sintetico · solo a scopo illustrativo

1. **Selezionare.** Includere la chat del caso e identificare la persona a cui si riferisce l’estratto.
2. **Ridurre al minimo.** Scegliere come far apparire un altro partecipante nella copia condivisa.
3. **Verificare.** Aprire il rapporto e i record dell’archivio generato prima di inviarlo.
4. **Condivisione.** Consegnare la copia revisionata e comunicare separatamente la sua impronta digitale certificata.

#### Osservazione originale

Nora · utente 71002

«Ho ricevuto il link aggiornato.»

Il diario di origine conserva questa osservazione salvata.

#### Copia per il destinatario

Mostrare come registrato: Nora · utente 71002 · «Ho ricevuto il link aggiornato.»

Pseudonimo: P01 · «Ho ricevuto il link aggiornato.»

Ometti: il messaggio di questo partecipante non viene incluso nel testo.

#### Esaminare i file effettivi

Leggere i file report.html e records.jsonl.

Verificare le identità, il testo, gli allegati e i commenti facoltativi del team.

#### Estratto firmato

Selezione + hash dei file + manifesto firmato

Un pacchetto separato collegato ai confini del registro di origine

## Utilizzare i controlli in combinazione

| Controllo | Impatto sul testo |
| --- | --- |
| Persone | Mantenere identificabili i soggetti selezionati; pseudonimizzare o omettere gli altri partecipanti a discrezione. |
| Testo | Includere tutto il testo, solo il testo delle persone selezionate e dell’account osservatore, oppure omettere il testo dei messaggi e i relativi campi di dettaglio contenenti testo. |
| File | Scegli i file delle persone selezionate e dell’account di osservazione, tutti i file dei messaggi visualizzati oppure nessun file. |
| Case Board | Non utilizzare elementi della bacheca, segnalibri e sezioni, né schede con discussioni di gruppo. |

Verificare il testo libero e il contenuto dei file, nonché le identità: uno pseudonimo non rimuove automaticamente tutti i nomi presenti in un messaggio o in un allegato. Se un file selezionato per la conservazione non è disponibile, ripristinarlo oppure omettere esplicitamente gli allegati prima di generare l’estratto.

## Assicurarsi che il testo sia verificabile in modo indipendente

```
python -m tgwitness.verify handover.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256
```

Conservare separatamente l’archivio originale delle prove firmate e i checkpoint. Il trasferimento registra la propria proiezione, in modo che il destinatario possa verificare la copia consegnata senza ricevere l’intero spazio di lavoro. [Report Studio](https://phishdestroy.github.io/TgWitness/it/docs/reports/) fornisce il proprio layout di lettura; [la verifica dell’esportazione](https://phishdestroy.github.io/TgWitness/it/docs/exports/) spiega i riferimenti attendibili.
