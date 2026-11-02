# Archiviazione e ripristino

Canonical page: https://phishdestroy.github.io/TgWitness/it/docs/reference/storage/

Backup, trasferimento dei file più vecchi sul cloud, copie protette da Object Lock e ripristino su un nuovo dispositivo.

Il pannello distingue tre attività:

| Compito | Cosa fa |
| --- | --- |
| Esegui un backup | Copia il registro firmato, i checkpoint, i file conservati e le esportazioni in coda nella destinazione S3 configurata. |
| Spazio locale gratuito | Copia gli allegati più vecchi selezionati su S3 o su un server remoto cloud rclone, rileggili per intero, verifica i byte crittografati, quindi elimina la copia locale verificata. |
| Conserva una copia come prova | Configurare S3 Object Lock e verificare lo stato di conservazione restituito. Il servizio deve confermare la modalità e la data richieste. |

La liberazione di spazio non elimina né sovrascrive mai il registro firmato. Ogni allegato conserva il proprio SHA-256 originale e una ricevuta di recupero. La compressione gzip opzionale avviene prima della crittografia autenticata. I nomi dei file nel cloud non contengono nomi Telegram, ID delle chat o nomi originali degli allegati. Un allegato può arrivare fino a 32 GiB.

Una risposta di caricamento da sola non costituisce autorizzazione alla cancellazione di un file. TgWitness scarica l’oggetto crittografato completo e ne verifica le dimensioni; SHA-256 salva la ricevuta, quindi ricontrolla immediatamente i byte locali prima della rimozione. Un errore di caricamento, una lettura diversa o un trasferimento annullato lasciano il file locale al suo posto. Se un backup delle prove abilitato non ha ancora copiato quel file, anche la rimozione attende che ciò avvenga.

## Collega una destinazione

In **Extra → Archiviazione e spazio su disco → Gestisci archiviazione**, scegli l’attività e la destinazione, salva, quindi seleziona **Prova caricamento e download**. Il test carica un piccolo file di prova casuale e lo rilegge. Non utilizza contenuti di Telegram.

Per S3, utilizzare l’endpoint, la regione e il bucket effettivi del provider. Wasabi, Backblaze, Cloudflare R2 e altri servizi compatibili utilizzano le stesse impostazioni S3. Una API compatibile di per sé non implica il supporto per Object Lock. La modalità Governance può consentire a un amministratore autorizzato di bypassare la conservazione; la modalità Compliance presenta diversi vincoli. Leggere lo stato di Object Lock restituito prima di fare affidamento sulla conservazione.

Per una destinazione rclone, creare un remoto utilizzando la configurazione del provider di rclone e incollare la sezione `[name]` nel pannello. L’helper installato supporta MEGA, Google Drive, OneDrive, Dropbox, Box, pCloud e gli altri provider mostrati nel selettore. Le credenziali vengono salvate nel vault crittografato di questo spazio di lavoro. Gli aggiornamenti OAuth vengono salvati nuovamente nel vault. Le credenziali non vengono aggiunte agli eventi del registro né incluse nei download di ripristino.

L’helper viene installato all’interno dello spazio di lavoro, con una versione fissata e SHA-256. Non viene aggiunto al PATH di sistema. I file di configurazione e i file di lavoro sono file temporanei all’interno di quell’area di lavoro. I remote basati su comandi e su file locali vengono rifiutati. rclone richiede attualmente un percorso **Direct** selezionato esplicitamente per le richieste esterne. Utilizzare l’archiviazione S3 nativa per un percorso SOCKS5 o HTTP dell’area di lavoro; rclone non aggira silenziosamente un percorso non disponibile.

## Conserva il file di ripristino

Scegli l’opzione **“Salva file di ripristino** dopo aver copiato i file” e conservalo in un luogo separato dall’installazione. Contiene la chiave di decrittografia e le ricevute degli oggetti firmate, quindi trattalo come un backup della chiave privata. Conserva separatamente anche la configurazione remota originale e le credenziali di destinazione. Un file di ripristino creato prima di una copia successiva non contiene la ricevuta di quel file successivo.

L’impronta digitale della chiave di firma dovrebbe essere già stata registrata separatamente. Una firma verificata solo rispetto alla chiave fornita all’interno dello stesso file non stabilisce a chi appartenga il file di ripristino.

Per ripristinare le ricevute di archiviazione mancanti in uno spazio di lavoro esistente, aprire **«Recupera file da un file di ripristino salvato**» e selezionare il file. Il pannello verifica la firma e richiede la stessa chiave di firma dello spazio di lavoro. Non accetta la sostituzione con una chiave di archiviazione diversa. Quindi scegliere **«Ripristina tutti i file**». Il ripristino mette in pausa la regola di archiviazione automatica, in modo che il successivo ciclo pianificato non possa rimuovere immediatamente i file ripristinati. Riattivare la regola quando si è terminato con le copie locali.

Il ripristino verifica il testo cifrato, autentica la decrittografia, decomprime se necessario e controlla il testo in chiaro originale SHA-256 prima di inserire un file in `media/`. Un oggetto remoto danneggiato non sostituisce mai un file locale. Un file locale esistente con byte diversi viene conservato per la revisione anziché sovrascritto.

## Ripristino dopo la perdita dell’installazione

Installa TgWitness su un altro computer. Utilizza il file di ripristino privato, l’impronta digitale registrata separatamente e le credenziali di destinazione originali:

```
python -m tgwitness.storage recover \
  --recovery storage-recovery.json \
  --fingerprint TRUSTED_WORKSPACE_SHA256 \
  --credentials original-rclone.conf \
  --output recovered-attachments
```

Per S3, `--credentials` punta a un file JSON privato contenente `access_key` e `secret_key`; il file di ripristino firmato fornisce le impostazioni di destinazione. Il comando utilizza una connessione esterna diretta e scarica l’helper aggiunto ai preferiti quando un remoto rclone ne ha bisogno. Rifiuta una directory di output già esistente.

I byte originali recuperati vengono scritti in `recovered-attachments/media/`, denominati in base al loro SHA-256. `recovery-log.jsonl` è un registro non firmato delle operazioni di recupero. Il comando non ricrea un diario firmato perso né la relativa chiave di firma. Conservare un backup completo dell’area di lavoro per questi elementi. Un file di recupero dell’archivio non è un backup completo dell’area di lavoro .

## Bot operatore e notifiche di completamento

Il bot di Telegram appartiene all’operatore. Crealo tramite BotFather e imposta il suo token, la chat di destinazione e gli ID utente Telegram esplicitamente consentiti nel pannello di controllo. Sia il mittente che la chat devono corrispondere. I messaggi inoltrati e i comandi provenienti da altri bot vengono ignorati.

`/status` e `/stats` sono disponibili nella modalità predefinita "solo stato". La modalità di controllo opzionale aggiunge `/pause`, `/resume` e `/copy`. `/copy` richiede l’esecuzione dell’attività di archiviazione configurata; ciò non significa che il caricamento remoto sia già terminato. I comandi non possono fornire URL, file o programmi shell arbitrari.

Utilizza le impostazioni di notifica separate per gli avvisi e il completamento delle attività. Le notifiche di completamento distinguono un’esportazione dell’account con lacune da un’esportazione completa e mostrano la cronologia e il conteggio degli elementi archiviati. Gli estratti dei messaggi non sono inclusi a meno che non siano stati abilitati separatamente nelle impostazioni di notifica. Il selettore di servizi viene generato dal catalogo Apprise effettivamente installato anziché da un insieme fisso di esempi di provider.
