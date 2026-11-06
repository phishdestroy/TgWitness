# Configurare un bot Witness

Canonical page: https://phishdestroy.github.io/TgWitness/it/docs/witness/

Un processo separato controlla il Suo diario e pubblica punti di controllo firmati in un canale.

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

Crei un bot con BotFather e lo lasci pubblicare nel Suo canale. Esegua il testimone altrove: un altro host, idealmente gestito da qualcun altro, vale molto più di un secondo processo accanto al collector.

## Tre passaggi nella sezione «Extras»

1. **Accesso in sola lettura.** **Extra → Testimone indipendente**, crei un token e salvi il file. Legge punti di controllo e stato, nient’altro.
2. **Canale e intervallo.** Canale Telegram o webhook Discord, più un indirizzo del collector raggiungibile dal testimone. Salvi il file delle impostazioni.
3. **Avvio.** Metta `witness.json`, `witness-token.txt` e `bot-token.txt` insieme sull’host del testimone ed esegua:

```
python -m tgwitness.witness run --config witness.json --check-config
python -m tgwitness.witness run --config witness.json
```

Aspetti il primo post firmato nel canale, poi conservi l’impronta del testimone in un posto sicuro.

Preferisce Discord? Salvi l’URL del webhook come `discord-webhook.txt`. Un testimone pubblica in un solo posto; su Discord i controlli lunghi arrivano come file.

## Scegliete la frequenza di pubblicazione

Pubblicare ogni controllo crea una traccia esterna costante: ogni cinque minuti sono circa 288 post al giorno per spazio. Le impostazioni avanzate permettono di pubblicare solo con modifiche o problemi, usare un proxy o una Bot API propria.

**Cosa attesta effettivamente il bot?**

Chiede al collector un punto di controllo firmato, lo verifica con la chiave attesa e tiene un proprio diario firmato, comprese le risposte mancate e rifiutate.

Controlla lo stato del diario, non osserva Telegram da solo. Per quello faccia un test di consegna controllato.

## Verifichi le prove in un secondo momento

Conservi il diario del testimone, i post e le impronte. [Come verificarli](https://phishdestroy.github.io/TgWitness/it/docs/reference/witness/#verify) rispetto all’esportazione del collector.
