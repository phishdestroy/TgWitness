# Esportare e verificare

Canonical page: https://phishdestroy.github.io/TgWitness/it/docs/exports/

Condividete un registro firmato che possa essere verificato da altri.

Conservare un riferimentoEsporta ZIP firmatoIl destinatario verifica

Non ha familiarità con le firme e i punti di controllo? [Modifichi un record di esempio](https://phishdestroy.github.io/TgWitness/it/docs/concepts/#chain) e verifichi quali controlli lo rilevano.

Desidera conservare una copia al di fuori del sistema di raccolta? Si rechi alla [configurazione di S3](https://phishdestroy.github.io/TgWitness/it/docs/exports/#s3), alla funzione [«Object Lock»](https://phishdestroy.github.io/TgWitness/it/docs/exports/#s3-retention) o [al recupero verificato](https://phishdestroy.github.io/TgWitness/it/docs/exports/#s3-restore).

## Conservare un riferimento affidabile

Salvi l’impronta digitale della chiave pubblica dell’area di lavoro al di fuori del collettore. Durante la raccolta, conservi i checkpoint firmati in un luogo separato oppure ricorra a un [testimone indipendente](https://phishdestroy.github.io/TgWitness/it/docs/witness/). Tali riferimenti consentono al destinatario di verificare la chiave e i confini di un registro precedente.

## Scarichi il file ZIP firmato

Aprire **«Esportazioni»** e creare un file ZIP di prove firmato. Esso include il registro dell’area di lavoro e un manifesto dei file firmato. I filtri del pannello non limitano questa esportazione completa del registro: si prega di esaminare il materiale prima di condividerlo.

I file HTML e CSV scaricabili separatamente sono utili per la lettura e l’analisi. Conservi il file ZIP firmato come originale verificabile; il file HTML o CSV separato non dispone di una firma autonoma.

## Verifichi utilizzando una copia affidabile di TgWitness

Nell’ambiente di progetto installato, sostituisca l’impronta digitale di esempio e i percorsi dei file:

```
python -m tgwitness.verify evidence.zip --fingerprint TRUSTED_PUBLIC_KEY_SHA256 --checkpoint retained-checkpoint.json
```

Quando entrambi i riferimenti superano la verifica, il risultato riporta `key_pinned: true` e `checkpoint_checked: true`. Conservi il risultato della verifica insieme all’archivio originale. Il punto di controllo conservato deve trovarsi al limite dell’esportazione o prima di esso.

## Comprendere il risultato

- **Integrità:** la cronologia registrata e i file esportati corrispondono alle rispettive firme.
- **Osservazione precedente:** un punto di controllo esterno consente di confrontare l’esportazione con un prefisso del registro conservato in precedenza.
- **Procedura:** un test controllato di invio → modifica → cancellazione verifica la corrispondenza di eventi specifici con la registrazione acquisita.

Una firma valida non dimostra che ogni evento su Telegram sia effettivamente avvenuto, che la fonte abbia detto la verità o che l’orologio di chi ha raccolto i dati fosse corretto.

## Configurare la copia off-site su S3

Nell’area di lavoro attiva, apra **Esportazioni → Copia esterna**. Questa funzionalità opzionale è compatibile con AWS S3 e altri servizi compatibili con S3. Copia segmenti del registro, foto e file conservati, punti di controllo con le relative risposte con timestamp e esportazioni di chat completate. Ogni oggetto viene crittografato sul collettore con l’algoritmo `AES-256-GCM` prima del caricamento.

La demo online mostra gli stessi comandi con la funzione di caricamento disabilitata. Inserisca le credenziali di accesso all’archivio solo nel proprio spazio di lavoro attivo.

[![Pannello completo per il copia fuori sede: endpoint, regione, bucket, chiavi di accesso, pianificazione, Object Lock e controlli delle chiavi di ripristino](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)](https://phishdestroy.github.io/TgWitness/assets/off-site-copy.png)

Il pannello completo con le opzioni avanzate è espanso. Non vengono visualizzate credenziali di accesso all’archivio.

| Settore | Cosa inserire |
| --- | --- |
| Endpoint | L’URL del servizio di archiviazione, senza percorso del bucket né credenziali. Esempio fittizio: `https://s3.example.invalid`. |
| Regione | La regione richiesta dal Suo provider. L’impostazione predefinita dell’applicazione è `us-east-1`. |
| Bucket | Un bucket esistente a cui è possibile accedere. Esempio fittizio: `example-case-backup`. |
| Cartella nel bucket | Il prefisso dell’oggetto; valore predefinito `tgwitness`. L’applicazione aggiunge un prefisso derivato dall’impronta digitale della chiave di firma di questo spazio di lavoro. |
| ID chiave di accesso / Chiave di accesso segreta | Inserisca entrambe le credenziali di archiviazione contemporaneamente. Esse vengono salvate nel vault dell’area di lavoro. Lasci entrambi i campi vuoti nei salvataggi successivi per mantenere la coppia salvata. |
| Indirizzi in formato «path» | Utilizzi `endpoint/bucket` se abilitato, oppure `bucket.endpoint` se disabilitato, a seconda del provider. |
| Intervallo di copia | Da 1 a 1.440 minuti; impostazione predefinita: 5 minuti. Per le copie programmate, l’applicazione deve essere in esecuzione. |
| Conservazione dei dati con Object Lock | Giorni di conservazione e modalità per un bucket che supporta Object Lock. L’impostazione “zero giorni” mantiene in vigore la conservazione predefinita del bucket. |

1. Inserisca la destinazione e le credenziali. Lasci deselezionata l’opzione **«Conserva una copia fuori sede»** durante la preparazione, quindi selezioni **«Salva copia fuori sede**».
2. Selezionare **«Verifica connessione**». In questo modo verrà caricato un oggetto di prova crittografato e verrà verificata la risposta del sistema di archiviazione.
3. Selezionare **«Scarica chiave di crittografia**». Conservare tale file separatamente dal programma di raccolta; è necessario per il ripristino.
4. Attivi la casella di controllo **«Conserva una copia fuori sede»** e salvi nuovamente. Selezioni **«Copia ora»** per un’operazione manuale, oppure lasci che la pianificazione proceda automaticamente.

**Non esegue**: non crea un bucket di archiviazione. I caricamenti programmati si interrompono quando l’applicazione viene arrestata.

## Verifica lo stato di conservazione e l’avanzamento della copia

In **«Altre opzioni»**, selezionate i giorni di conservazione e `GOVERNANCE` o `COMPLIANCE` qualora il vostro bucket supporti la funzione Object Lock. TgWitness riporta la modalità di conservazione e la scadenza di un oggetto caricato. Lo stato segnala la conferma, la mancanza di conservazione o un errore di verifica; il semplice caricamento non costituisce di per sé una conferma della conservazione.

Il pannello riporta l’ultimo ciclo di elaborazione, il numero di oggetti, i byte trasferiti, il limite del registro copiato ed eventuali errori. La mancanza o la modifica di supporti locali viene segnalata e si procede a un nuovo tentativo nel ciclo successivo. I file, i checkpoint e le esportazioni in coda successivi a tale supporto possono comunque essere copiati.

I caricamenti utilizzano il percorso Direct, SOCKS5 o HTTP dell’area di lavoro. La copia su S3 non è disponibile tramite MTProxy; l’applicazione non ricorre a una connessione diretta.

**Non** obbliga il fornitore ad applicare l’Object Lock semplicemente perché il caricamento è stato accettato.

## Conservare la chiave di ripristino in un luogo separato

Il file JSON scaricato contiene la chiave di decrittografia, le impostazioni di destinazione, il prefisso dell’oggetto dell’area di lavoro e l’impronta digitale della chiave di firma. Non contiene le credenziali di accesso a S3: il ripristino richiede credenziali separate con accesso in lettura al bucket.

Se modifica l’endpoint, il bucket o il prefisso della cartella, scarichi nuovamente il file della chiave in modo che le impostazioni di destinazione corrispondano. L’applicazione avvia una nuova copia del registro, dei file e dei checkpoint conservati localmente nella nuova destinazione. Le esportazioni delle chat completate già rimosse dalla coda di caricamento locale rimangono nella loro destinazione precedente.

**Non** decrittografa la copia senza la chiave esportata. Le credenziali di accesso all’archivio non possono sostituire tale chiave.

## Ripristino e verifica su un altro computer

Si utilizzi un’installazione affidabile di TgWitness, il file JSON della chiave scaricato, credenziali di accesso all’archivio con autorizzazione in lettura e una directory di output vuota. Sostituiscano i segnaposto fittizi delle credenziali riportati di seguito.

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

I file scaricati e gli oggetti decriptati rimangono in un archivio temporaneo privato mentre vengono verificati l’intero registro, i checkpoint conservati, nonché gli hash e le dimensioni dei file multimediali preservati. Vengono scartati i percorsi non sicuri, i segmenti di registro in conflitto e i registri più brevi del proprio checkpoint. In caso di verifica fallita, non viene pubblicato alcun file ripristinato.

Il recupero riuscito produce `events.jsonl`, `media/`, `checkpoints/` e `exports/` per il materiale disponibile nella copia. Conservi il risultato JSON del comando insieme al materiale recuperato.

**Non** ricostruisce le osservazioni che non sono mai state inserite nel registro né sostituisce un punto di controllo o una testimonianza conservati in modo indipendente.
