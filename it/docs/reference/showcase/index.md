# Vetrina pubblica

Canonical page: https://phishdestroy.github.io/TgWitness/it/docs/reference/showcase/

Pubblica i messaggi salvati dei canali pubblici selezionati e le istantanee firmate tramite link a scadenza e revocabili.

[TgWitness](https://github.com/phishdestroy/TgWitness/blob/main/README.md) / [Documentazione](https://github.com/phishdestroy/TgWitness/blob/main/docs/README.md) · [Implementazione e ripristino](https://phishdestroy.github.io/TgWitness/it/docs/reference/deployment/)

![Implementazione e ripristino](https://phishdestroy.github.io/TgWitness/assets/chapter-operate.svg)

**Access → Public showcase** crea una pagina separata, di sola lettura, utilizzando il sistema esistente di token di accesso. Legge le osservazioni salvate dall’installazione. Non avvia un collettore, non effettua l’accesso a Telegram né acquisisce un canale per un visitatore.

## Pubblica una pagina

1. Salva un profilo di origine per ogni canale pubblico che desideri mostrare. Un canale deve avere un nome utente pubblico nel suo ultimo profilo salvato; i gruppi e le chat private non sono ammessi.
2. Apri **Accesso → Vetrina pubblica** (oppure `/showcase-manage.html`) come amministratore.
3. Seleziona i canali in un massimo di 16 spazi di lavoro, inserisci il titolo della pagina pubblica e scegli una durata del link di 1, 7 o 30 giorni. Le etichette interne degli spazi di lavoro non vengono pubblicate. È possibile includere fino a 64 canali.
4. Controlla il testo dei canali selezionati per la pubblicazione, quindi fai clic su **“Anteprima dei record selezionati**”. L’anteprima utilizza la stessa proiezione lato server della pagina dei visitatori.
5. Fai clic su **«Crea link alla vetrina**». Copia il link finché è visibile. Aprilo in un browser separato per controllare la pagina del destinatario prima di distribuirla.

Il link contiene un token di accesso nel frammento dell’URL. La pagina rimuove il frammento prima di effettuare richieste API e lo sostituisce con una sessione del browser. Chiunque disponga del link può aprire il materiale selezionato fino alla scadenza o alla revoca. I nuovi link consentono 100 sessioni simultanee, ciascuna della durata massima di un’ora. I controlli di accesso esistenti possono inoltre applicare restrizioni sugli indirizzi e limiti di accesso tramite l’API grant. L’accesso normale del revisore è una modalità diversa e include comunque i messaggi e i file originariamente consentiti.

## Cosa vedono i visitatori

| Visibile | Mantenuto privato |
| --- | --- |
| Titoli di canali pubblici selezionati, nomi utente e date di osservazione dei profili | Identità degli account, etichette interne degli spazi di lavoro e fonti non selezionate |
| Testo acquisito e ogni modifica salvata | ID mittente strutturati, nomi, nomi utente, numeri di telefono e valori del profilo |
| Osservazioni relative alla cancellazione con il testo salvato in precedenza, se disponibile | Allegati, avatar, miniature, nomi dei file e payload originali |
| Indicatori che segnalano che un autore/profilo o un allegato è stato registrato | Metadati relativi all’inoltro e alle risposte, percorsi di rete, indirizzi IP e credenziali |
| Conteggio degli eventi dei canali selezionati, stati attuali delle raccolte, intervallo tra i segnali di attività e i checkpoint | Controlli sulle raccolte e API standard per l’esportazione delle prove |
| Impronta di firma, checkpoint del registro e prova di coerenza | Chiavi di firma e sessioni Telegram |

**Il testo dei messaggi pubblici non viene automaticamente reso anonimo.** Un nome, una menzione, un numero di telefono o un link inseriti nel messaggio rimangono parte integrante di quel testo. `Redacted`Si applica ai campi strutturati relativi all’autore e al profilo. Controlla il contenuto effettivamente selezionato prima di pubblicarlo, comprese le modifiche e le cancellazioni conservate.

L’idoneità riflette l’**ultimo profilo di origine salvato**, non una ricerca in tempo reale su Telegram. Se un profilo successivo non presenta più un nome utente di canale pubblico, le nuove richieste escludono il canale. Aggiornare i profili di origine quando cambia la visibilità pubblica. I lettori potrebbero aver già salvato materiale ricevuto in precedenza.

I registri originali firmati rimangono invariati. La proiezione visualizzata viene firmata separatamente e contiene hash che fanno riferimento ai registri originali. Una firma della proiezione autentica la dichiarazione visualizzata; non si tratta della firma dell’evento originale apposta sui byte oscurati.

## Verifica delle firme e della continuità

Espandi **"Fingerprint & signed checkpoint**" e scarica uno snapshot. Dopo un aggiornamento della pagina, il download include lo snapshot precedente del browser e una prova di coerenza di Merkle tra i confini dei rispettivi journal. L'aggiornamento automatico avviene una volta al minuto mentre la pagina è visibile e mostra la sua prima pagina di osservazioni.

Una volta installato TgWitness, verifica il file scaricato in modalità offline:

```
python -m tgwitness.showcase_verify showcase.json --fingerprint TRUSTED_COLLECTOR_SHA256
```

L’impronta digitale deve provenire da una fonte di riferimento separata e attendibile. Per effettuare un confronto con uno snapshot che avete conservato voi stessi, utilizzate `--previous earlier.json`; ciò sovrascrive lo snapshot precedente contenuto nel download. La prova attuale deve iniziare da quel confine conservato. I client autenticati possono richiedere tale prova utilizzando `GET /api/showcase/{workspace_id}?challenge=<32-hex-random>&from_count=<retained-count>`. Un registro più breve restituisce un codice di stato HTTP 409 invece di reimpostare silenziosamente il confine.

Il checkpoint firmato viene salvato nell’**intero registro del collettore**, inclusi il numero di record e l’hash opaco dell’intestazione. I conteggi dei messaggi visualizzati si applicano solo ai canali pubblici selezionati. La pagina non elenca mai i contenuti dell’altro registro. Si tratta di conteggi di eventi, non di messaggi unici. Le impostazioni descrivono la configurazione attuale, non ogni intervallo di registrazione precedente.

La verifica della firma e della coerenza è in grado di rilevare modifiche rispetto a un limite prestabilito. Non effettua un riconteggio indipendente dei contatori firmati, non certifica l’origine di Telegram, non dimostra l’acquisizione ininterrotta né sostituisce un testimone indipendente. A tal fine, utilizzare il [verificatore di prove](https://github.com/phishdestroy/TgWitness/blob/main/docs/TRUST.md), [il testimone indipendente](https://phishdestroy.github.io/TgWitness/it/docs/reference/witness/) e [la registrazione su scala testata](https://phishdestroy.github.io/TgWitness/it/docs/reference/verification/). Le installazioni sintetiche sono chiaramente contrassegnate come tali.

## Revoca o ospita la pagina

Utilizza **«Revoke»** nel gestore delle vetrine o nella sezione **«Accesso»** esistente per chiudere il collegamento e terminare tutte le relative sessioni. Il visitatore cancella i record visualizzati quando una richiesta rileva che l’accesso è terminato. La scadenza e le autorizzazioni vengono verificate ad ogni richiesta. Le autorizzazioni alle vetrine non possono essere convertite in accesso ordinario al pannello in loco; crea una nuova autorizzazione per cambiare modalità.

La pagina viene servita tramite l’indirizzo HTTPS esistente dell’installazione. La pubblicazione di un link non apre una nuova porta, non crea un tunnel né modifica il DNS. L’HTML e le API rimangono sull’installazione dell’utente. Un visitatore della vetrina non può utilizzare le normali API relative a messaggi, profili, contenuti multimediali, esportazione o gestione con questo tipo di accesso.
