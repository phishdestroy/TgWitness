# Preparare una copia da condividere

Canonical page: https://phishdestroy.github.io/TgWitness/it/docs/handover/

Condivida solo il necessario, l’originale resta intatto.

Una consegna è un estratto firmato a parte: scelga chat e persone, nasconda identità o testo, decida quali file e note della squadra includere. Il manifest registra cosa è stato tenuto, ridotto e lasciato fuori.

## Preparare l’estratto per il destinatario

1. **Esportazioni → Estratto di consegna**: scriva lo scopo, scelga chat e periodo e usi **Carica le persone delle chat scelte** se servono persone con nome.
2. Tutti gli altri: pseudonimi, esclusi o come registrati. Testo e file sono interruttori separati; telefoni ed e-mail si possono mascherare.
3. Case Board: niente, segnalibri e porzioni, oppure schede con commenti. I nomi della squadra si possono sostituire con alias.
4. **Scarica estratto di consegna**, lo apra, lo verifichi e lo riveda prima di inviarlo.

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
| Persone | Le persone scelte restano con il nome; le altre ricevono pseudonimi o vengono escluse. |
| Testo | Tutto il testo, solo quello delle persone scelte e del Suo account, oppure nessuno. |
| File | File delle persone scelte e del Suo account, tutti i file mostrati oppure nessuno. |
| Case Board | Niente, segnalibri e porzioni, oppure schede con discussione. |

Legga anche testo e file: uno pseudonimo non toglie i nomi scritti dentro un messaggio o un allegato. Se manca un file scelto, lo ripristini o escluda gli allegati.

## Assicurarsi che il testo sia verificabile in modo indipendente

```
python -m tgwitness.verify handover.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256
```

Conservi Lei l’archivio originale e i punti di controllo. Il destinatario può verificare la sua copia senza ricevere l’intero spazio. Design: [Report studio](https://phishdestroy.github.io/TgWitness/it/docs/reports/). Riferimenti affidabili: [verifica dell’esportazione](https://phishdestroy.github.io/TgWitness/it/docs/exports/).
