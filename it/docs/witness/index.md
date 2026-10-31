# Configurare un bot Witness

Canonical page: https://phishdestroy.github.io/TgWitness/it/docs/witness/

Si consiglia di affidare a un processo separato il controllo del registro e la pubblicazione di checkpoint firmati sul Suo canale.

## Due host, due chiavi di firma

HOST A / COLLECTOR**Account + registro**

Chiave di firma del raccoglitore di sessioni Telegram

Endpoint di checkpoint in sola lettura

← Richiesta di risposta firmata →

HOST B / WITNESS**Verificare + conservare**

Impronta digitale del collettore fissata; chiave di firma separata del testimone

Registro personale + token del bot

Witness → API del bot di Telegram →**Il vostro canale · post firmati TGW1**

Il «witness» esegue autonomamente i controlli. L’accesso del «collector» è di sola lettura. La pubblicazione tramite bot utilizza la connessione e il token del «witness»; al «witness» non viene assegnata alcuna sessione dell’account.

03 / DECISIONI RELATIVE AI PUNTI DI CONTROLLORisposte esemplificative

ULTIMO ACCETTATO**120 record**`head 9c7d…`

RISPOSTA SUCCESSIVA**128 record**`head a4f2…`

Accettato: il conteggio aumenta, la firma viene verificata e la chiave corrisponde. Il testimone mantiene questo nuovo limite.

Tutti gli esempi di risposta presuppongono una firma valida e la chiave fissata. Gli hash qui riportati sono illustrazioni abbreviate. Un numero maggiore di valori non è di per sé sufficiente a dimostrare che l’intero prefisso precedente sia rimasto invariato; si confronti un’esportazione con i checkpoint conservati.

## Preparare un bot e un canale

Creare un bot con BotFather e autorizzarlo a pubblicare in un canale da Lei controllato. Scegliere un computer o un server per il witness. Un host e un operatore separati garantiscono una maggiore indipendenza rispetto a un secondo processo sul server del collettore.

## Tre passaggi nella sezione «Extras»

1. **Accesso in sola lettura.** Aprire **«Extras» → Un bot nel Suo canale**, creare un token di autenticazione e salvare il file di accesso. Consente di leggere i checkpoint e lo stato di integrità, ma non le conversazioni né i controlli del collettore.
2. **Canale e intervallo.** Inserisca il canale e un indirizzo di raccolta raggiungibile dal testimone. Salvi il file delle impostazioni.
3. **Avvio.** Inserisca insieme `witness.json`, `witness-token.txt` e un `bot-token.txt` creati sull’host di Witness. Esegua i comandi riportati di seguito nell’ambiente di progetto installato.

```
python -m tgwitness.witness run --config witness.json --check-config
python -m tgwitness.witness run --config witness.json
```

Il download dei file non avvia il processo di creazione del registro. Verifichi che il primo post firmato compaia nel canale, quindi conservi separatamente l’impronta digitale della chiave pubblica del registro.

## Scegliete la frequenza di pubblicazione

La pubblicazione di ogni controllo crea un registro esterno regolare. A intervalli di cinque minuti, ciò corrisponde a circa 288 post al giorno per ogni spazio di lavoro. Le impostazioni avanzate offrono inoltre la possibilità di pubblicare in caso di modifiche o problemi, un proxy e un indirizzo API personalizzato per il bot.

**Cosa attesta effettivamente il bot?**

Il testimone richiede al raccoglitore un checkpoint firmato, lo verifica confrontandolo con la chiave prevista e tiene un registro separato e firmato. Esso registra sia le risposte mancanti e quelle rifiutate, sia i controlli andati a buon fine. La pubblicazione dipende comunque dal fatto che il testimone sia in esecuzione e riesca a connettersi all’API Bot di Telegram.

Verifica lo stato del registro segnalato dal collettore. Non monitora in modo indipendente ogni singolo messaggio di Telegram. A tal fine, si raccomanda di aggiungere il test di consegna controllata.

## Verifichi le prove in un secondo momento

Conservate il registro delle testimonianze, i post dei canali e le impronte digitali salvate in modo indipendente. La [procedura di verifica completa](https://phishdestroy.github.io/TgWitness/it/docs/reference/witness/#verify) li confronta con l’esportazione firmata dal responsabile della raccolta.
