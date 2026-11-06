# Installazione, verifica e aggiornamento

Canonical page: https://phishdestroy.github.io/TgWitness/it/docs/reference/installation/

Installazione con un solo comando, verifica delle firme e degli hash, aggiornamento e rimozione dell’installazione.

[Progetto](https://github.com/phishdestroy/TgWitness/blob/main/README.md) · [Guida rapida](https://phishdestroy.github.io/TgWitness/it/docs/reference/quickstart/) · [Implementazione](https://phishdestroy.github.io/TgWitness/it/docs/reference/deployment/)

## Installazione con un solo comando

Il programma di installazione guidato include un runtime Python privato. Utilizza lo stesso indirizzo per le installazioni future: ogni pubblicazione aggiorna il programma di installazione, gli hash, le firme e le informazioni sulla build.

**Linux / macOS (Bash):**

```
curl -fsSL https://get.destroy.tools/install.sh | bash
```

Su un server Ubuntu, eseguire il comando come root per installare un servizio in background. Su un computer desktop, eseguire il comando come utente normale.

**Windows (PowerShell o Prompt dei comandi):**

```
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "irm https://get.destroy.tools/install.ps1 | iex"
```

Su Windows non è necessario alcun amministratore. Il processo figlio di PowerShell lascia il terminale aperto con il risultato. Python e le dipendenze rimangono nell’installazione.

Su Ubuntu, scegli **«Questo computer**», **«Link HTTPS temporaneo»** o **«Dominio proprio**». Il programma di installazione visualizza l’indirizzo del pannello e la chiave di accesso. Per ottenere un link temporaneo, apri quell’indirizzo HTTPS nel tuo browser e inserisci la chiave. In caso di accesso locale su un server remoto , utilizza un inoltro SSH dal tuo computer (`ssh -L 8787:127.0.0.1:8787 user@server`) e apri `http://127.0.0.1:8787`. Su macOS e Windows, il pannello locale si apre nel tuo browser; mantieni attivo il terminale.

Accedi a Telegram nel pannello e scegli cosa raccogliere. L’installazione da sola non avvia la raccolta da Telegram.

## Dove tutto funziona

`get.destroy.tools` È un **Cloudflare Worker che gestisce i download statici**. Non contiene il pannello TgWitness, né sessioni Telegram né un database delle prove relative agli utenti. Non viene instradato verso un VPS del progetto. L’applicazione gira sulla macchina su cui si esegue il comando.

| Installazione | Programma | Dati |
| --- | --- | --- |
| Ubuntu come root | `/opt/tgwitness` | Servizio di sistema: `/var/lib/tgwitness-<installation ID>`; utilizzare `tgwitness paths` per il percorso esatto. |
| Utente Linux / macOS | `~/.local/share/tgwitness` | `data/live` nell'ambito di tale installazione. |
| Utente Windows | `%LOCALAPPDATA%\TgWitness` | `data\live` nell'ambito di tale installazione. |

Imposta `TGWITNESS_INSTALL_DIR` per scegliere un’altra cartella. Le versioni installate e i dati sono separati. Il programma di installazione non carica i tuoi account, i messaggi o le chiavi sul sito di download. Scegliendo un tunnel Cloudflare, il traffico del pannello viene instradato attraverso Cloudflare; utilizzando il tuo dominio, il traffico viene indirizzato al tuo server.

Ogni installazione include i file **START-HERE.html** e **START-HERE.txt**, contenenti percorsi locali, comandi e collegamenti al repository. Esegui `tgwitness guide` per aprire la guida. Su Windows, utilizzare `& "$env:LOCALAPPDATA\TgWitness\bin\tgwitness.cmd" guide` in PowerShell.

## Impostazioni della ricerca full-text

[La ricerca full-text](https://phishdestroy.github.io/TgWitness/it/docs/reference/search/) (anteprima) non richiede alcuna configurazione. Il suo indice viene creato in background dopo un aggiornamento.

| Variabile o comando | Effetto |
| --- | --- |
| `TGWITNESS_FULLTEXT=disk` | Impostazione predefinita: l'indice viene conservato in `search/fulltext.sqlite3` di ciascun spazio di lavoro |
| `TGWITNESS_FULLTEXT=memory` | Nessun file di indice; l'indice viene ricostruito ad ogni avvio |
| `TGWITNESS_FULLTEXT=off` | Nessun indice; solo ricerca per testo esatto |
| `tgwitness index status` | Stato dell’indice di ogni area di lavoro |
| `tgwitness stop`, `tgwitness index rebuild`, `tgwitness start` | Ricostruire tutti gli indici a partire dal registro firmato |

La scelta dell'amministratore in **Registro → Filtri → Indice di ricerca** sovrascrive la variabile per quell'area di lavoro. I comandi individuano la directory dei dati dell'installazione che li esegue; altrove, aggiungere `--data-dir` il percorso da `tgwitness paths`. Per un dizionario ucraino completo (dati GPL-3.0), installare `pymorphy3-dicts-uk` nell’ ambiente Python dell’installazione.

## Accesso da riga di comando

La [riga di](https://phishdestroy.github.io/TgWitness/it/docs/reference/cli/) [comando](https://phishdestroy.github.io/TgWitness/it/docs/reference/cli/) (anteprima) legge l’archivio alla ricerca di script e agenti.

| Variabile | Effetto |
| --- | --- |
| `TGWITNESS_URL` | Indirizzo del pannello per `tgwitness search`, `context`, `messages`, `stats` e `export`; impostazione predefinita `http://127.0.0.1:8787` quando è impostato un token |
| `TGWITNESS_MCP_TOKEN` | Archiviare il token di connessione da **Integrazioni → MCP**, condiviso con i client MCP; `--token-file` leggere invece da un file |
| `TGWITNESS_DATA` | La directory dei dati viene letta direttamente quando non `--data-dir`, URL o token specificato |

## Verificare prima dell’esecuzione

Il comando di una riga si affida a HTTPS per lo script iniziale. Tale script verifica SHA-256 e la firma RSA del progetto sull’applicazione e sui vincoli prima dell’ installazione. È anche possibile scaricare e verificare prima lo script iniziale.

La chiave di rilascio pubblica è [release-signing.pub](https://github.com/phishdestroy/TgWitness/blob/main/deploy/installer/release-signing.pub). Il suo SHA-256 è:

```
039d98a658ccda14253e45a00335b4a68d840976d8ec18b8d4355cc7c458447d
```

Conserva questa impronta digitale proveniente da una revisione del repository di cui ti fidi. Un checksum proveniente dallo stesso server di download rileva eventuali discrepanze; la chiave pubblica, considerata affidabile in modo indipendente, è ciò che autentica la firma di una versione.

Utilizza una nuova cartella vuota per i download di verifica riportati di seguito.

**Linux / macOS — eseguire in una nuova directory di download vuota** (richiede curl e OpenSSL):

```
curl -fSLO https://get.destroy.tools/install.sh &&
curl -fSLO https://get.destroy.tools/install.sh.sig &&
curl -fSLO https://get.destroy.tools/release-signing.pub &&
test "$(openssl dgst -sha256 release-signing.pub | awk '{print $NF}')" = \
  '039d98a658ccda14253e45a00335b4a68d840976d8ec18b8d4355cc7c458447d' &&
openssl dgst -sha256 -verify release-signing.pub -signature install.sh.sig install.sh &&
bash install.sh
```

La `&&` catena si interrompe prima dell’esecuzione se un download, l’impronta digitale della chiave o la verifica della firma falliscono. Se la pubblicazione avviene tra il download dello script e la sua firma, scaricare nuovamente entrambi. I vecchi programmi di installazione mantengono i loro URL dei pacchetti immutabili.

**Windows — controlla l'SHA-256 prima dell'esecuzione:**

```
Invoke-WebRequest https://get.destroy.tools/install.ps1 -OutFile install.ps1 -UseBasicParsing
Get-FileHash .\install.ps1 -Algorithm SHA256
Invoke-RestMethod https://get.destroy.tools/SHA256SUMS.txt
```

Confronta l’hash con la `install.ps1` riga. Per una verifica indipendente della firma, utilizza OpenSSL (ad esempio, da Git Bash) e la stessa impronta digitale della chiave pubblica riportata sopra:

```
curl -fSLO https://get.destroy.tools/install.ps1 &&
curl -fSLO https://get.destroy.tools/install.ps1.sig &&
curl -fSLO https://get.destroy.tools/release-signing.pub &&
test "$(openssl dgst -sha256 release-signing.pub | awk '{print $NF}')" = \
  '039d98a658ccda14253e45a00335b4a68d840976d8ec18b8d4355cc7c458447d' &&
openssl dgst -sha256 -verify release-signing.pub -signature install.ps1.sig install.ps1 &&
powershell.exe -NoProfile -ExecutionPolicy Bypass -File install.ps1
```

L’installazione su Windows verifica autonomamente le firme dei pacchetti tramite .NET e non richiede OpenSSL. Si tratta di firme RSA-3072 / SHA-256 separate, non di Authenticode. Il [manifesto](https://get.destroy.tools/manifest.json) registra la versione del software, il commit Git esatto, l’ID di rilascio immutabile e l’SHA-256 di ciascun artefatto. La pagina rimanda alla fonte corrispondente. Anche il manifesto e l’elenco dei checksum presentano firme separate (`manifest.json.sig` e `SHA256SUMS.txt.sig`).

## Aggiornamento di un'installazione esistente

**Una nuova pubblicazione aggiorna il sito di download; i programmi installati si aggiornano quando si esegue nuovamente il programma di installazione.** Non è previsto alcun sistema di aggiornamento automatico né il riavvio automatico di una collezione in esecuzione. Il canale di installazione attuale è **"preview"**; segue le build pubblicate e verificate da `main`, il cui commit può essere più recente dell’ultima versione numerata su GitHub. La versione della pagina deriva dal `pyproject.toml`; il suo commit e l’ID della build distinguono gli aggiornamenti all’interno della stessa versione di anteprima.

Publication is automatic after that exact commit passes the application and security checks and the signed package passes Ubuntu service and Windows PowerShell installation tests. While checks are running, or if they fail, the same commands continue to install the previous checked build. The build manifest shows which commit is currently available; the version number alone may stay the same between preview updates.

Utilizzare la stessa cartella di installazione e lo stesso utente del sistema operativo di prima. Eseguire il backup dell’intera directory dei dati con la raccolta disattivata; `tgwitness paths` identificala. Un’esportazione firmata non costituisce un backup completo dell’installazione.

**Installazione come root su Ubuntu all'indirizzo `/opt/tgwitness`:**

```
curl -fsSL https://get.destroy.tools/install.sh | TGWITNESS_INSTALL_DIR=/opt/tgwitness bash -s -- --no-start
```

Dopo aver completato con successo l’installazione:

```
/opt/tgwitness/bin/tgwitness restart
/opt/tgwitness/bin/tgwitness status
/opt/tgwitness/bin/tgwitness open
```

Per l’installazione da parte di un utente Linux/macOS, utilizzare il file originale `TGWITNESS_INSTALL_DIR` oppure quella predefinita ed eseguire nuovamente il primo comando di installazione. Chiudere un pannello in primo piano prima dell’aggiornamento e riavviarlo al termine. Per un servizio Linux già configurato , eseguire il relativo `tgwitness restart` comando.

**Windows:** chiudere il pannello in esecuzione, eseguire nuovamente il comando di installazione per Windows, quindi aprire `bin\tgwitness.cmd` nella stessa installazione. Il programma di installazione conserva dati, sessioni, impostazioni di accesso e chiavi di firma. Cambia il launcher solo dopo che il nuovo ambiente ha superato i controlli; un’installazione non riuscita lascia il precedente launcher al suo posto. Conservare il backup pre-aggiornamento per eventuali modifiche al formato di archiviazione.

## Comandi di uso quotidiano su Ubuntu

| Comando | Risultato |
| --- | --- |
| `tgwitness open` | URL attuale del pannello e chiave di accesso. |
| `tgwitness paths` | Percorsi esatti di programmi, dati e guide. |
| `tgwitness guide --print` | Istruzioni per l’uso offline. |
| `tgwitness status` / `tgwitness logs` | Disponibilità / registri di servizio. |
| `tgwitness stop` / `tgwitness start` | Interrompi/riprendi il servizio; conserva i dati. |
| `tgwitness token rotate` | Sostituisci la chiave amministratore e chiudi le sessioni del browser. |
| `tgwitness tunnel off` | Disattiva il tunnel rapido pubblico; mantieni il pannello locale. |
| `tgwitness tunnel on` / `tgwitness tunnel restart` | Crea un link quick-tunnel / sostituisci il suo indirizzo. |

Vedi la sezione [Accesso](https://phishdestroy.github.io/TgWitness/it/docs/reference/access/) per i token dei colleghi, le sessioni e le restrizioni IP, e [la sezione Pubblicazione dell’installer](https://github.com/phishdestroy/TgWitness/blob/main/deploy/installer/README.md#automatic-publication-from-github) per il flusso di lavoro di rilascio da GitHub a Cloudflare.

## Rimuovi TgWitness

Non è presente un programma di disinstallazione: è sufficiente chiudere il pannello ed eliminare le relative cartelle. L’eliminazione della cartella dei dati distrugge definitivamente i diari, le chiavi di firma, le sessioni di Telegram e i file salvati. Prima di procedere:

1. Esporta ciò che ti serve (**Esportazioni → Scarica ZIP firmato**) e conserva l’impronta digitale della chiave di firma e i checkpoint al di fuori di questo computer. Per conservare l’area di lavoro stessa, copia l’intera cartella dei dati dopo aver interrotto la raccolta.
2. Elimina i server creati in **«Extras» → «Server 24/7»** dalla sezione **«I tuoi server»** o tramite `python -m tgwitness.cloud destroy`; il provider li addebita fino a quando non vengono eliminati.
3. Chiudi la sessione di ciascun account su Telegram da **Impostazioni → Dispositivi**. L’eliminazione dei file non comporta la disconnessione dalla sessione sul lato di Telegram.

**Installazione come root su Ubuntu.** Prendere nota della cartella dei dati, arrestare il servizio, quindi rimuovere il servizio, le cartelle e il collegamento:

```
/opt/tgwitness/bin/tgwitness paths
/opt/tgwitness/bin/tgwitness stop
systemctl list-unit-files 'tgwitness-*'
systemctl disable tgwitness-<ID>
rm /etc/systemd/system/tgwitness-<ID>.service
systemctl daemon-reload
rm -rf /opt/tgwitness /var/lib/tgwitness-<ID> /usr/local/bin/tgwitness
```

**Installazione per utenti Linux o macOS.** Chiudere il pannello. Un servizio utente Linux configurato viene arrestato con `systemctl --user disable --now tgwitness-<ID>`; la sua unità si trova in `~/.config/systemd/user/`. Quindi eliminare `~/.local/share/tgwitness` (o il tuo `TGWITNESS_INSTALL_DIR`) e il `~/.local/bin/tgwitness` collegamento.

**Windows.** Chiudi il pannello ed elimina `%LOCALAPPDATA%\TgWitness` (o il tuo `TGWITNESS_INSTALL_DIR`). Il programma di installazione non aggiunge alcun servizio, attività pianificata o collegamento.
