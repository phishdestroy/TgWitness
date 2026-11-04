# Scoprite cosa è andato storto

Canonical page: https://phishdestroy.github.io/TgWitness/it/docs/troubleshooting/

Parta dal sintomo e controlli una cosa alla volta.

## Il pannello richiede un token

Chiede il token del pannello dal file indicato dal launcher. Docker: `docker compose exec tgwitness cat /data/panel-token.txt`. Non è un codice Telegram, né un token di bot, né quello del testimone.

## Telegram non si connette

Esegua la verifica di connessione. Con un proxy pubblico ne scelga un altro e salvi. Controlli il tipo di proxy e il formato del segreto. Aggiornare gli elenchi non cambia il percorso da solo.

## Connesso, ma nessun nuovo messaggio

1. L’osservazione è in corso, nello spazio giusto?
2. La fonte è selezionata e visibile a quell’account?
3. Invii un messaggio unico nel gruppo di prova e lo cerchi.
4. Cerchi interruzioni o errori di Telegram nel diario.

Una chat tranquilla semplicemente non ha nulla di nuovo. Se conta la completezza, faccia un test di consegna controllato.

## FloodWait o un intervallo dopo un riavvio

FloodWait è Telegram che dice «più piano». Aspetti che passi e riduca il carico, riconnettersi non aiuta. Dopo un riavvio TgWitness recupera ciò che Telegram ha ancora; il resto è una lacuna, quindi la annoti.

## Il bot è configurato ma non pubblica nulla

Il testimone è in funzione, il bot può pubblicare nel canale, raggiunge il collector e la Bot API? Cerchi nel suo diario i post non riusciti. Un’interrogazione lato collector non significa che il post sia partito.

## Dove si trova l’integrazione del token GitHub?

**In fase di pianificazione.** La sezione «Extras» descrive il flusso di lavoro proposto per il fork e la verifica della compilazione. Attualmente non è disponibile alcun modulo per il token GitHub né alcuna attestazione automatica che confermi la corrispondenza tra un’installazione in esecuzione e un repository. Si prega di consultare lo [stato attuale delle funzionalità](https://phishdestroy.github.io/TgWitness/it/docs/reference/features/).

Segnala un bug? Versione, sistema, passaggi e un errore senza dati personali. Non metta mai sessioni, token, messaggi privati o la cartella dati in una issue pubblica.
