# Marcatori temporali

Canonical page: https://phishdestroy.github.io/TgWitness/it/docs/reference/timestamp/

Timestamp RFC 3161 per i checkpoint firmati: cosa viene inviato all’autorità e come viene verificata la risposta.

TgWitness prepara richieste RFC 3161 e verifica le risposte dell’autorità di marcatura temporale (TSA). Questa procedura manuale non seleziona una TSA né invia dati; la modalità «evidence» esegue entrambe le operazioni secondo una frequenza prestabilita ([formato «evidence»](https://phishdestroy.github.io/TgWitness/it/docs/reference/evidence/#rfc-3161-preparation-and-response-verification-02)). Una richiesta preparata **non** costituisce **ancora una prova di marcatura temporale**.

## Ciò che le prove dimostrano

Diagramma di flusso · Osservazioni sull’account → Catena SHA-256 e firme Ed25519; Catena SHA-256 e firme Ed25519 → Punto di controllo firmato; Punto di controllo firmato → Hash a byte esatto e nonce casuale; Hash a byte esatto e nonce casuale → Richiesta RFC 3161; Richiesta RFC 3161 → TSA indipendente; TSA indipendente → Risposta firmata della TSA; Punto di controllo firmato → Verifica dei dati, del nonce e della fiducia esplicita nella CA; Risposta firmata della TSA → Verifica dei dati, del nonce e della fiducia esplicita nella CA · Osservazionisull’account · Catena SHA-256 e firmeEd25519 · Punto di controllofirmato · Hash a byte esatto enonce casuale · Richiesta RFC 3161 · TSA indipendente · Risposta firmata dellaTSA · Verifica dei dati, delnonce e della fiduciaesplicita nella CA

**Diagramma sotto forma di testo**

1. Osservazioni sull’account → Catena SHA-256 e firme Ed25519
2. Catena SHA-256 e firme Ed25519 → Punto di controllo firmato
3. Punto di controllo firmato → Hash a byte esatto e nonce casuale
4. Hash a byte esatto e nonce casuale → Richiesta RFC 3161
5. Richiesta RFC 3161 → TSA indipendente
6. TSA indipendente → Risposta firmata della TSA
7. Punto di controllo firmato → Verifica dei dati, del nonce e della fiducia esplicita nella CA
8. Risposta firmata della TSA → Verifica dei dati, del nonce e della fiducia esplicita nella CA

La firma del collettore associa i record alla propria chiave. Una risposta attendibile della TSA può dimostrare che un determinato punto di controllo esisteva all’ora indicata dalla TSA. Il punto di controllo può quindi associare il prefisso del registro. Ciò non stabilisce l’ora di ciascuna azione su Telegram né la veridicità dei contenuti acquisiti.

## Procedura

1. Conservare l’impronta digitale della chiave del collettore tramite un canale affidabile separato. Una chiave fornita esclusivamente dal file ZIP oggetto di analisi non è sufficiente per identificare il collettore.
2. In **Esportazioni → Prepara richiesta di timestamp**, scarichi il file ZIP della richiesta relativo all’area di lavoro selezionata. Estragga i file `checkpoint.json`, `timestamp.tsq`, `SHA256SUMS` e `README.txt`. Non modifichi i byte di checkpoint.
3. Scegliete un TSA adeguato all’indagine. Inviate `timestamp.tsq` utilizzando il relativo metodo documentato, con `application/timestamp-query` per un servizio HTTP. Salvate la risposta binaria originale come `timestamp.tsr`, indicando l’endpoint, l’ora di recupero e l’esito della richiesta. La richiesta contiene un hash e un nonce anziché i messaggi; i metadati di rete rivelano comunque la richiesta.
4. Si ottenga il certificato radice attendibile indipendentemente dalla risposta, oltre a eventuali certificati intermedi necessari. Un certificato presente nella risposta non diventa attendibile semplicemente per il fatto di esservi incluso.
5. Da un’installazione affidabile di TgWitness, verificare:

```
python -m tgwitness.anchor verify --checkpoint checkpoint.json --request timestamp.tsq --response timestamp.tsr --ca trusted-tsa-root.pem
```

Aggiungere `--intermediates tsa-intermediates.pem` o `--openssl /path/to/openssl` se necessario. OpenSSL deve supportare `ts`. Su Windows il verificatore effettua la ricerca anche nell’installazione standard di Git. OpenSSL 3.5.9 è stato testato localmente con una CA/TSA sintetica.

1. Esportare un file ZIP del registro firmato dopo il punto di controllo in modo che includa tale prefisso. Verificare utilizzando l’impronta digitale nota in modo indipendente:

```
python tgwitness/verify.py evidence.zip --fingerprint TRUSTED_SHA256 --checkpoint checkpoint.json
```

1. Conservare il file ZIP, il checkpoint, la richiesta, la risposta, la catena di certificati, i risultati della verifica e il registro di trasferimento al di fuori del collettore. Ripetere la verifica al momento della ricezione.

Per preparare una richiesta a partire da un punto di controllo salvato:

```
python -m tgwitness.anchor prepare checkpoint.json --out timestamp-request.zip
```

La procedura di preparazione canonizza il JSON e include il checkpoint corrispondente nell’archivio. Utilizzi i **byte del checkpoint presenti in tale archivio** per la verifica TSA, anche qualora il file di input presentasse spazi bianchi diversi.

## Limiti della verifica

| Verifica | Comportamento attuale |
| --- | --- |
| Dati | Il valore SHA-256 dei byte esatti del checkpoint deve corrispondere alla risposta |
| Richiesta | Con `--request`, la query originale e il nonce vengono verificati |
| Firma TSA | OpenSSL verifica la firma e la catena di certificati fino alla CA esplicita |
| Firma del responsabile della raccolta | Verificato separatamente dal verificatore del registro tramite una chiave fissata |
| Revoca | Nessun recupero automatico di OCSP/CRL |
| Validità a lungo termine | Nessuna convalida dell’archivio dopo la scadenza del certificato |
| Invio programmato | Modalità «Prove», disattivata per impostazione predefinita |

`--request` è tecnicamente facoltativo, ma la sua omissione impedisce la verifica del nonce originale. Affinché la procedura sia completa, il risultato `request_checked` deve essere vero. La verifica del certificato segue le regole e i tempi di verifica previsti da OpenSSL. La conservazione a lungo termine richiede una politica separata relativa ai certificati e alle prove di revoca.

Una firma crittografica valida non costituisce automaticamente un timestamp qualificato né una determinazione di ammissibilità legale. Se un operatore ha falsificato le osservazioni prima dell’apposizione del timestamp, il TSA fissa tali byte; ciò non ne attesta la veridicità.

## Registro dei passaggi di consegne

Registrare l’identificativo del caso, il mittente e il destinatario, l’ora di trasferimento UTC e la relativa fonte, lo scopo, i nomi dei file/i valori SHA-256, l’impronta digitale del collettore, l’intervallo di sequenza, le lacune note, la versione del verificatore e l’esito della verifica. Firmare e conservare in modo indipendente tale registro secondo la procedura della propria organizzazione. In TgWitness non è implementato un sistema di registrazione della custodia multiutente.

Durante lo sviluppo non è stata contattata alcuna TSA indipendente in tempo reale. I test locali creano una CA/TSA sintetica per verificare la compatibilità e il rifiuto di dati modificati, nonce o CA.
