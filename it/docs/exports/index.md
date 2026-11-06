# Telegram · Esportare e verificare

Canonical page: https://phishdestroy.github.io/TgWitness/it/docs/exports/

Consegni file che il destinatario può verificare da solo rispetto al Suo spazio.

Conservare un riferimentoEsporta ZIP firmatoIl destinatario verifica

Nuovo a firme e punti di controllo? [Modifichi una voce di esempio](https://phishdestroy.github.io/TgWitness/it/docs/concepts/#chain) e veda quali controlli se ne accorgono.

Desidera conservare una copia al di fuori del sistema di raccolta? Si rechi alla [configurazione di S3](https://phishdestroy.github.io/TgWitness/it/docs/exports/#s3), alla funzione [«Object Lock»](https://phishdestroy.github.io/TgWitness/it/docs/exports/#s3-retention) o [al recupero verificato](https://phishdestroy.github.io/TgWitness/it/docs/exports/#s3-restore).

## Conservare un riferimento affidabile

Annoti l’impronta della chiave dello spazio da qualche parte che non sia il collector. Durante la raccolta conservi altrove anche i punti di controllo firmati, oppure usi un [testimone indipendente](https://phishdestroy.github.io/TgWitness/it/docs/witness/). È con questo che il destinatario verifica la chiave e uno stato precedente del diario.

## Scarichi il file ZIP firmato

**Esportazioni** → ZIP di prove firmato. Contiene tutto il diario e un manifest dei file firmato. Dia forma al report leggibile in [Report studio](https://phishdestroy.github.io/TgWitness/it/docs/reports/), oppure invii solo dati selezionati come [estratto di consegna](https://phishdestroy.github.io/TgWitness/it/docs/handover/).

I report HTML, PDF e JSON hanno i propri sigilli. Il CSV è solo una copia di lavoro; per l’integrità usi il CSV dentro lo ZIP verificato.

## Verifichi utilizzando una copia affidabile di TgWitness

Nell’ambiente del progetto, con la Sua impronta e i Suoi percorsi:

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
```

Se va a buon fine vedrà `key_pinned: true` e `checkpoint_checked: true`. Conservi quell’output accanto all’archivio. Il punto di controllo deve trovarsi alla fine dell’esportazione o prima.

## Utilizzare il risultato della verifica

- **File:** il manifest lega i loro hash, le firme legano il diario. Qualsiasi modifica si nota.
- **Identità:** l’impronta che ha conservato dimostra che è la chiave attesa.
- **Stato precedente:** un punto di controllo confronta l’esportazione con un inizio di diario salvato prima della consegna.
- **Copertura:** lacune, risultati di acquisizione e un test invia → modifica → elimina mostrano cosa ha davvero catturato questa configurazione.

Dettagli: [cosa dimostra la verifica e cosa no](https://phishdestroy.github.io/TgWitness/it/docs/reference/evidence/#verification-scope).

## Configurare la copia off-site su S3

**Esportazioni → Copia esterna** nel Suo spazio. Funziona con AWS S3 e qualunque servizio compatibile S3. Copia segmenti del diario, file salvati, punti di controllo con le loro marche temporali ed esportazioni di chat completate, ognuno cifrato con `AES-256-GCM` prima di lasciare il collector.

La demo online mostra questi controlli con il caricamento disattivato. Inserisca credenziali reali solo nella Sua installazione.

[![Pannello completo per il copia fuori sede: endpoint, regione, bucket, chiavi di accesso, pianificazione, Object Lock e controlli delle chiavi di ripristino](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)

Il pannello completo con le opzioni avanzate è espanso. Non vengono visualizzate credenziali di accesso all’archivio.

| Settore | Cosa inserire |
| --- | --- |
| Endpoint | URL dello storage, senza percorso del bucket né credenziali. Esempio: `https://s3.example.invalid`. |
| Regione | Quella richiesta dal Suo provider. Predefinita `us-east-1`. |
| Bucket | Un bucket esistente su cui può scrivere. Esempio: `example-case-backup`. |
| Cartella nel bucket | Prefisso, predefinito `tgwitness`. Si aggiunge un prefisso per spazio. |
| ID chiave di accesso / Chiave di accesso segreta | Entrambe insieme, salvate nel vault. Le lasci vuote in seguito per mantenerle. |
| Indirizzi in formato «path» | Attivo: `endpoint/bucket`. Disattivo: `bucket.endpoint`. Dipende dal provider. |
| Intervallo di copia | Da 1 a 1.440 minuti, predefinito 5. Solo mentre l’app è in funzione. |
| Conservazione dei dati con Object Lock | Giorni e modalità, se il bucket supporta Object Lock. Zero mantiene l’impostazione predefinita del bucket. |

1. Crei il bucket, compili destinazione e credenziali con **Mantieni una copia esterna** non selezionato e prema **Salva copia esterna**.
2. **Testa connessione** carica un oggetto di prova cifrato.
3. **Scarica chiave di cifratura** e la conservi lontano dal collector. Niente chiave, niente recupero.
4. Selezioni **Mantieni una copia esterna**, salvi, poi **Copia ora** oppure lasci girare la pianificazione.

## Verifica lo stato di conservazione e l’avanzamento della copia

In **Altre opzioni** scelga i giorni di conservazione e `GOVERNANCE` o `COMPLIANCE`. TgWitness rilegge la conservazione da un oggetto caricato e Le indica: confermata, assente o verifica non riuscita.

Il pannello mostra l’ultimo passaggio, il numero di oggetti, i byte, il limite del diario copiato e gli errori. Un file locale mancante viene segnalato e ritentato al passaggio successivo; il resto continua a essere copiato.

I caricamenti passano in diretto, via SOCKS5 o HTTP. Con un percorso solo MTProxy la copia resta in attesa con un errore.

## Conservare la chiave di ripristino in un luogo separato

Il JSON della chiave contiene la chiave di decifratura, la destinazione, il prefisso e l’impronta della chiave. Per il recupero Le servono questo più credenziali di storage con accesso in lettura.

Ha cambiato endpoint, bucket o prefisso? Riscarichi la chiave. Nella nuova destinazione parte una copia nuova; le vecchie esportazioni restano dov’erano.

## Ripristino e verifica su un altro computer

Le servono un’installazione di TgWitness affidabile, il JSON della chiave, credenziali di sola lettura e una cartella vuota:

### Windows PowerShell

```
$env:TGWITNESS_S3_ACCESS_KEY = 'YOUR_READ_ACCESS_KEY'
$env:TGWITNESS_S3_SECRET_KEY = 'YOUR_READ_SECRET_KEY'
python -m tgwitness.replica restore --key-file tgwitness-replica-key.json --out restored-evidence
```

### Linux / macOS

```
export TGWITNESS_S3_ACCESS_KEY='YOUR_READ_ACCESS_KEY'
export TGWITNESS_S3_SECRET_KEY='YOUR_READ_SECRET_KEY'
python -m tgwitness.replica restore --key-file tgwitness-replica-key.json --out restored-evidence
```

Prima tutto viene verificato in una cartella temporanea privata: l’intero diario, i punti di controllo, hash e dimensioni dei file. Percorsi non sicuri, segmenti in conflitto o un diario più corto del suo punto di controllo falliscono, e allora non viene scritto nulla.

Se va bene ottiene `events.jsonl`, `media/`, `checkpoints/` ed `exports/`. Conservi con essi l’output JSON del comando e confronti con i punti di controllo o le voci del testimone che conserva Lei.
