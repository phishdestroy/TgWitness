# OCR locale e trascrizione

Canonical page: https://phishdestroy.github.io/TgWitness/it/docs/reference/media-analysis/

Riconoscere le immagini e i file audio acquisiti tramite un worker locale; mantenere il testo derivato collegato al file di origine.

**Versione principale attuale:** utilizzare un checkout dal codice sorgente; l’anteprima portatile 0.7.0 è precedente a questa funzionalità.

[Guida al flusso di lavoro](https://phishdestroy.github.io/TgWitness/docs/archive/) · [Wiki](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

Aprire un record del registro `media.saved`, scegliere **«Riconoscimento allegato**», quindi selezionare «OCR» o «Trascrizione» nella sezione **«Chiedi all’archivio**». L’elaborazione è manuale e locale. Non è prevista alcuna modalità di archiviazione su cloud né il caricamento automatico. I byte originali dell’allegato e il file `media_sha256` rimangono invariati; il testo riconosciuto viene esplicitamente contrassegnato come riconoscimento automatico e archiviato separatamente con l’hash di origine, la versione del motore/modello, la lingua, i parametri e l’ora di completamento. Le trascrizioni mantengono i timestamp restituiti.

Cerca tra questi risultati utilizzando **la funzione “Cerca nel testo riconosciuto”** e il filtro OCR/trascrizione. Si tratta di una ricerca separata su dati derivati; non converte automaticamente il riconoscimento automatico in testo originale di Telegram né lo aggiunge agli eventi firmati.

## Configurazione del worker opzionale

La versione 1 richiede un host Linux con un daemon Docker locale. Le installazioni su Windows possono eseguire TgWitness all’interno di un ambiente VM/WSL Linux con un proprio daemon locale. Il pannello non decodifica mai autonomamente un allegato non attendibile.

```
docker build -f deploy/media-worker/Dockerfile -t tgwitness-media:local .
export TGWITNESS_MEDIA_IMAGE=tgwitness-media:local
```

Impostare queste variabili nell’ambiente di servizio di TgWitness e riavviarlo. Il socket del daemon è impostato di default su `/var/run/docker.sock`; nelle distribuzioni senza privilegi di root è possibile impostare `TGWITNESS_DOCKER_SOCKET`. Il worker utilizza esplicitamente quel socket Unix anziché un contesto Docker remoto. Non esporre un’API Docker agli utenti del pannello né montare il suo socket all’interno del container di riconoscimento.

Per la trascrizione, installare separatamente un modello Whisper compatibile con CTranslate2, quindi impostare `TGWITNESS_WHISPER_MODEL_DIR` sulla relativa directory. Il worker lo carica con `local_files_only=True`; il modello selezionato e l’input vengono montati in sola lettura. Consultare la [documentazione relativa al caricamento dei modelli](https://github.com/SYSTRAN/faster-whisper) del motore. L’immagine OCR fornita include dati di addestramento in inglese e russo. Aggiungere un’altra lingua all’immagine quando necessario; i codici lingua seguono [la CLI di Tesseract](https://tesseract-ocr.github.io/tessdoc/Command-Line-Usage.html).

Durante l’elaborazione non viene recuperato alcun modello. La procedura di compilazione/download potrebbe richiedere l’uso della rete; in ogni singolo contenitore di riconoscimento la connessione di rete è disabilitata. Installare l’immagine prima di abilitarla; il runtime utilizza `--pull=never`.

## Limiti e ripristino

Il container viene eseguito come utente senza privilegi con un root in sola lettura, capacità ridotte, `no-new-privileges` , una CPU, 2 GiB di memoria, un limite di PID e un filesystem temporaneo limitato. Vengono montati solo una copia verificata del file selezionato e una directory modello opzionale. Il database, il vault e la sessione del collettore non vengono montati. I [flag del runtime Docker](https://docs.docker.com/reference/cli/docker/container/run/) impongono questi limiti; si tratta comunque di un confine del container, non di un’enclave hardware.

I file sono limitati a 50 MiB, le immagini a 20 milioni di pixel, i file audio a 30 minuti con durata nota e l’elaborazione a cinque minuti. È attivo un solo worker alla volta, con un massimo di 20 lavori in coda o in esecuzione e 100 lavori conservati per ogni area di lavoro. L’opzione «Cancel» arresta il container; «Retry» crea un nuovo processo collegato al tentativo precedente. I processi interrotti vengono contrassegnati dopo il riavvio. L’elaborazione può fallire quando un modello non rientra nei limiti configurati; non viene eseguita in modo silenzioso senza isolamento.
